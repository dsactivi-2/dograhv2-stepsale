"use client";

import { AlertTriangle, Info } from "lucide-react";
import Link from "next/link";

export type AggregationSampleMeta = {
  truncated?: boolean;
  total_matching_runs?: number;
  sampled_runs?: number;
  sample_limit?: number;
  total_matching_campaigns?: number;
  sampled_campaigns?: number;
  truncation_note?: string | null;
};

export function TruncationBanner({
  meta,
  entityLabel = "Runs",
}: {
  meta: AggregationSampleMeta | null | undefined;
  entityLabel?: string;
}) {
  if (!meta?.truncated) return null;
  const total =
    meta.total_matching_runs ?? meta.total_matching_campaigns ?? 0;
  const sampled = meta.sampled_runs ?? meta.sampled_campaigns ?? 0;
  const note =
    meta.truncation_note ||
    `Aggregated from the newest ${sampled} of ${total} matching ${entityLabel}. Narrow the date range for full coverage.`;
  return (
    <div className="flex gap-3 rounded-lg border border-amber-300 bg-amber-50 p-4 dark:border-amber-800 dark:bg-amber-950/40">
      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-700 dark:text-amber-400" />
      <div className="text-sm text-amber-950 dark:text-amber-100">
        <p className="font-medium">Incomplete sample</p>
        <p className="mt-1 text-amber-900/90 dark:text-amber-200/90">{note}</p>
      </div>
    </div>
  );
}

export function ScopeHint({
  variant,
}: {
  variant: "billing" | "costs" | "qa" | "campaign-ops";
}) {
  const content = {
    billing: {
      title: "Billing ≠ Costs",
      body: (
        <>
          This page shows <strong>MPS credit balance and ledger</strong> (what you
          are charged in credits). Run-level model costs live under{" "}
          <Link href="/costs" className="font-medium underline underline-offset-2">
            Costs
          </Link>
          . The two numbers can differ.
        </>
      ),
    },
    costs: {
      title: "Costs ≠ Billing",
      body: (
        <>
          This page aggregates <strong>cost_info / usage_info on Agent Runs</strong>.
          Credit purchases and ledger balance are under{" "}
          <Link href="/billing" className="font-medium underline underline-offset-2">
            Billing
          </Link>
          . Missing cost fields on runs reduce coverage.
        </>
      ),
    },
    qa: {
      title: "QA Center reads Agent Runs",
      body: (
        <>
          Review scores and overrides come from{" "}
          <strong>workflow run annotations</strong> (post-call QA), not from the
          Campaign Ops funnel. Filter by campaign_id when you need campaign-scoped
          QA. Campaign dial health is under{" "}
          <Link
            href="/campaigns/ops"
            className="font-medium underline underline-offset-2"
          >
            Campaign Ops
          </Link>
          .
        </>
      ),
    },
    "campaign-ops": {
      title: "Campaign Ops ≠ QA Center",
      body: (
        <>
          This page shows queue/funnel/retry health for campaigns. Call quality
          review is in the{" "}
          <Link
            href="/qa-center"
            className="font-medium underline underline-offset-2"
          >
            QA Center
          </Link>{" "}
          (optionally filter by the same campaign id).
        </>
      ),
    },
  }[variant];

  return (
    <div className="flex gap-3 rounded-lg border border-sky-200 bg-sky-50 p-4 dark:border-sky-900/50 dark:bg-sky-950/30">
      <Info className="mt-0.5 h-4 w-4 shrink-0 text-sky-700 dark:text-sky-400" />
      <div className="text-sm text-sky-950 dark:text-sky-100">
        <p className="font-medium">{content.title}</p>
        <p className="mt-1 text-sky-900/90 dark:text-sky-200/90">{content.body}</p>
      </div>
    </div>
  );
}
