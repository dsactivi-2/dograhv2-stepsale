from pydantic import BaseModel, Field


class OrganizationPreferences(BaseModel):
    test_phone_number: str | None = None
    timezone: str | None = None
    external_pbx_integrations_enabled: bool = False
    # When non-empty, only these emails (+ superusers) may override QA
    # or approve/reject scripts. Empty = legacy: any org member.
    ops_reviewer_emails: list[str] = Field(default_factory=list)
