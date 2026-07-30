"""Stable Outcomes / QA schemas for internal voice-ops tools (P0)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class QaNodeOutcome(BaseModel):
    """Normalized single-node (or whole-call) QA result."""

    node_id: str
    node_name: str = ""
    score: Optional[float] = None
    tags: list[str] = Field(default_factory=list)
    summary: str = ""
    sentiment: Optional[str] = None  # positive|neutral|negative|…
    error: Optional[str] = None
    raw: dict[str, Any] = Field(default_factory=dict)


class QaRunOutcome(BaseModel):
    """Normalized QA payload for one workflow run."""

    schema_version: Literal[1] = 1
    run_id: int
    workflow_id: Optional[int] = None
    has_qa: bool = False
    overall_score: Optional[float] = None
    sentiment: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    nodes: list[QaNodeOutcome] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    source_keys: list[str] = Field(default_factory=list)


class OutcomeRunRow(BaseModel):
    run_id: int
    workflow_id: int
    workflow_name: str = ""
    created_at: Optional[datetime] = None
    is_completed: bool = False
    disposition: str = "UNKNOWN"
    phone_number: str = ""
    duration_seconds: Optional[float] = None
    call_tags: list[str] = Field(default_factory=list)
    qa: QaRunOutcome
    campaign_id: Optional[int] = None


class AggregationSampleMeta(BaseModel):
    """Shared sample/truncation fields for in-memory aggregates."""

    total_matching_runs: int = 0
    sampled_runs: int = 0
    sample_limit: int = 0
    truncated: bool = False
    truncation_note: Optional[str] = None


class OutcomesSummaryResponse(BaseModel):
    from_date: str
    to_date: str
    timezone: str
    workflow_id: Optional[int] = None
    campaign_id: Optional[int] = None
    total_runs: int
    completed_runs: int
    disposition_distribution: list[dict[str, Any]]
    qa_coverage: dict[str, Any]
    average_qa_score: Optional[float] = None
    top_qa_tags: list[dict[str, Any]]
    total_matching_runs: int = 0
    sampled_runs: int = 0
    sample_limit: int = 0
    truncated: bool = False
    truncation_note: Optional[str] = None


class OutcomesListResponse(BaseModel):
    total: int
    page: int
    limit: int
    runs: list[OutcomeRunRow]
