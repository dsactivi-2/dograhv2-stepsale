"""Ops / reviewer permission helpers for MANAGE write actions (QA, scripts)."""

from __future__ import annotations

from fastapi import HTTPException

from api.db.models import UserModel
from api.services.organization_preferences import get_organization_preferences


async def can_perform_ops_review(user: UserModel) -> bool:
    """True if user may override QA or approve/reject scripts.

    Rules:
    - Superuser always allowed
    - If org preference ``ops_reviewer_emails`` is non-empty: email must match
    - If empty: any authenticated org member (legacy / unconfigured orgs)
    """
    if getattr(user, "is_superuser", False):
        return True
    org_id = getattr(user, "selected_organization_id", None)
    if not org_id:
        return False
    prefs = await get_organization_preferences(int(org_id))
    emails = list(getattr(prefs, "ops_reviewer_emails", None) or [])
    if not emails:
        return True
    user_email = (getattr(user, "email", None) or "").strip().lower()
    allowed = {e.strip().lower() for e in emails if e and str(e).strip()}
    return bool(user_email and user_email in allowed)


async def require_ops_reviewer(user: UserModel) -> None:
    """Raise 403 if the user is not allowed to perform ops review actions."""
    if await can_perform_ops_review(user):
        return
    raise HTTPException(
        status_code=403,
        detail=(
            "Ops reviewer permission required. Ask an admin to add your email to "
            "organization preferences ops_reviewer_emails, or use a superuser account."
        ),
    )
