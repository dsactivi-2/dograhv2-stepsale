"""Schemas for Cost Attribution dashboard (P3)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CostBucket(BaseModel):
    """One aggregation dimension row (workflow / campaign / definition)."""

    key: str
    label: str
    group_type: Literal["workflow", "campaign", "definition", "unattributed"]
    workflow_id: int | None = None
    campaign_id: int | None = None
    definition_id: int | None = None
    run_count: int = 0
    runs_with_cost: int = 0
    runs_missing_cost: int = 0
    total_duration_seconds: float = 0.0
    total_cost_usd: float | None = None
    total_charge_usd: float | None = None
    total_dograh_tokens: float = 0.0
    avg_cost_usd: float | None = None
    cost_coverage_pct: float = 0.0


class CostAttributionSummary(BaseModel):
    from_date: str
    to_date: str
    timezone: str
    workflow_id: int | None = None
    campaign_id: int | None = None
    group_by: Literal["workflow", "campaign", "definition"] = "workflow"
    total_runs: int = 0
    runs_with_cost: int = 0
    runs_missing_cost: int = 0
    cost_coverage_pct: float = 0.0
    total_duration_seconds: float = 0.0
    total_cost_usd: float | None = None
    total_charge_usd: float | None = None
    total_dograh_tokens: float = 0.0
    buckets: list[CostBucket] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    total_matching_runs: int = 0
    sampled_runs: int = 0
    sample_limit: int = 0
    truncated: bool = False
    truncation_note: str | None = None
