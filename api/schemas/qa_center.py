"""QA Center + Compliance schemas (P4)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from api.schemas.outcomes import QaRunOutcome


class ComplianceFlag(BaseModel):
    key: str
    label: str
    status: Literal["pass", "fail", "unknown"] = "unknown"
    source: str = "inferred"  # inferred|override|raw_field|tag
    detail: str = ""


class QaManualOverridePayload(BaseModel):
    """Body for reviewer override (audit trail stored in annotations)."""

    overall_score: float | None = Field(default=None, ge=0, le=100)
    sentiment: str | None = None
    tags: list[str] = Field(default_factory=list)
    summary: str = ""
    notes: str = ""
    # Free-form compliance map: true=pass, false=fail, null/omit=unknown
    compliance_flags: dict[str, bool | None] = Field(default_factory=dict)


class QaManualOverrideRecord(BaseModel):
    schema_version: Literal[1] = 1
    overall_score: float | None = None
    sentiment: str | None = None
    tags: list[str] = Field(default_factory=list)
    summary: str = ""
    notes: str = ""
    compliance_flags: dict[str, bool | None] = Field(default_factory=dict)
    reviewer_user_id: int
    reviewer_email: str | None = None
    created_at: str
    previous: dict[str, Any] | None = None  # prior override snapshot (audit chain)


class QaCenterRunRow(BaseModel):
    run_id: int
    workflow_id: int
    workflow_name: str = ""
    campaign_id: int | None = None
    created_at: datetime | None = None
    is_completed: bool = False
    disposition: str = "UNKNOWN"
    phone_number: str = ""
    duration_seconds: float | None = None
    # Auto QA (schema v1)
    qa: QaRunOutcome
    # Effective after override
    effective_score: float | None = None
    effective_sentiment: str | None = None
    effective_tags: list[str] = Field(default_factory=list)
    effective_summary: str = ""
    has_override: bool = False
    override: QaManualOverrideRecord | None = None
    # Queue / review
    needs_review: bool = False
    review_reasons: list[str] = Field(default_factory=list)
    # Compliance
    compliance_flags: list[ComplianceFlag] = Field(default_factory=list)
    compliance_fail_count: int = 0
    compliance_unknown_count: int = 0


class TagCount(BaseModel):
    tag: str
    count: int


class SentimentBucket(BaseModel):
    sentiment: str
    count: int
    percentage: float


class ScoreBucket(BaseModel):
    bucket: str  # e.g. "1-3", "4-6", "7-8", "9-10", "unknown"
    count: int


class ComplianceFlagSummary(BaseModel):
    key: str
    label: str
    pass_count: int = 0
    fail_count: int = 0
    unknown_count: int = 0


class QaCenterSummary(BaseModel):
    from_date: str
    to_date: str
    timezone: str
    workflow_id: int | None = None
    campaign_id: int | None = None
    total_runs: int
    runs_with_qa: int
    runs_without_qa: int
    coverage_pct: float
    average_score: float | None = None
    low_score_count: int = 0
    problem_tag_count: int = 0
    override_count: int = 0
    needs_review_count: int = 0
    compliance_fail_runs: int = 0
    top_tags: list[TagCount] = Field(default_factory=list)
    sentiment_distribution: list[SentimentBucket] = Field(default_factory=list)
    score_distribution: list[ScoreBucket] = Field(default_factory=list)
    compliance_summary: list[ComplianceFlagSummary] = Field(default_factory=list)
    max_score_threshold: float = 6.0
    problem_tags: list[str] = Field(default_factory=list)
    total_matching_runs: int = 0
    sampled_runs: int = 0
    sample_limit: int = 0
    truncated: bool = False
    truncation_note: str | None = None


class QaCenterQueueResponse(BaseModel):
    total: int
    page: int
    limit: int
    max_score_threshold: float
    problem_tags: list[str]
    runs: list[QaCenterRunRow]
    campaign_id: int | None = None
    total_matching_runs: int = 0
    sampled_runs: int = 0
    sample_limit: int = 0
    truncated: bool = False
    truncation_note: str | None = None


class QaCenterDetailResponse(BaseModel):
    run: QaCenterRunRow
    audit_history: list[dict[str, Any]] = Field(default_factory=list)


class QaRerunResponse(BaseModel):
    run_id: int
    status: Literal["queued", "unavailable"] = "queued"
    message: str = ""
