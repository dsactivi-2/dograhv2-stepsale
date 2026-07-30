"""Shared aggregation sampling / truncation metadata for MANAGE dashboards."""

from __future__ import annotations

from typing import Any


def sample_meta(
    *,
    total_matching: int,
    sampled: int,
    sample_limit: int,
) -> dict[str, Any]:
    """Build consistent truncation fields for summary responses."""
    total = max(0, int(total_matching))
    used = max(0, int(sampled))
    limit = max(0, int(sample_limit))
    truncated = total > used
    return {
        "total_matching_runs": total,
        "sampled_runs": used,
        "sample_limit": limit,
        "truncated": truncated,
        "truncation_note": (
            f"Aggregated from the newest {used} of {total} matching runs "
            f"(limit {limit}). Narrow the date range for full coverage."
            if truncated
            else None
        ),
    }
