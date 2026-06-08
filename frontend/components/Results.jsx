"use client";

import { useEffect, useState } from "react";
import Logo from "./Logo";
import GapCard from "./GapCard";
import MilestoneCard from "./MilestoneCard";
import ResourceCard from "./ResourceCard";
import SectionHeading from "./SectionHeading";
import ReasoningTrace from "./ReasoningTrace";
import CopyPlanButton from "./CopyPlanButton";
import Reveal from "./Reveal";
import { loadChecked, saveChecked, objectiveKey } from "@/lib/progress";

function VerificationBanner({ verification }) {
  const approved = verification?.status === "approved";
  return (
    <div
      className={`flex flex-col gap-3 rounded-4xl border p-6 shadow-pin sm:flex-row sm:items-center ${
        approved
          ? "border-emerald-200 bg-emerald-50"
          : "border-amber-200 bg-amber-50"
      }`}
    >
      <span
        className={`grid h-12 w-12 shrink-0 place-items-center rounded-full text-white ${
          approved ? "bg-emerald-500" : "bg-amber-500"
        }`}
      >
        {approved ? (
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path
              d="M5 12.5l4 4 10-10"
              stroke="currentColor"
              strokeWidth="2.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        ) : (
          <span className="text-lg font-extrabold">!</span>
        )}
      </span>
      <div className="min-w-0 flex-1">
        <p className="font-display text-lg font-extrabold">
          {approved ? "Plan verified by AI auditor" : "Flagged for revision"}
        </p>
        <p className="mt-0.5 text-sm leading-relaxed text-pin-muted">
          {verification?.reasoning}
        </p>
        {verification?.issues?.length > 0 && (
          <ul className="mt-2 list-inside list-disc text-sm text-amber-700">
            {verification.issues.map((issue, i) => (
              <li key={i}>{issue}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default function Results({ plan, onReset }) {
  const gaps = plan?.gap_analysis?.gaps || [];
  const milestones = plan?.milestone_plan?.milestones || [];
  const adjustments = plan?.milestone_plan?.adjustments_made || [];
  const byGap = plan?.resources?.by_gap || {};
  const meta = plan?.generation_metadata || {};

  // ── Weekly checklist progress (persisted to localStorage by goal) ──────────
  const namespace = plan?.goal || "";
  const [checked, setChecked] = useState(() => new Set());

  useEffect(() => {
    setChecked(loadChecked(namespace));
  }, [namespace]);

  const isChecked = (key) => checked.has(key);

  const toggle = (key) => {
    setChecked((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      saveChecked(namespace, next);
      return next;
    });
  };

  const totalObjectives = milestones.reduce(
    (sum, m) => sum + (m.objectives?.length || 0),
    0
  );
  const doneObjectives = milestones.reduce(
    (sum, m) =>
      sum +
      (m.objectives || []).filter((o, i) =>
        checked.has(objectiveKey(m.week, i, o))
      ).length,
    0
  );
  const pct =
    totalObjectives > 0
      ? Math.round((doneObjectives / totalObjectives) * 100)
      : 0;

  return (
    <div className="relative z-[2] mx-auto max-w-6xl px-5 py-10">
      {/* Bar */}
      <header className="flex flex-wrap items-center justify-between gap-3">
        <Logo />
        <div className="flex items-center gap-2">
          <CopyPlanButton plan={plan} />
          <button
            onClick={onReset}
            className="rounded-full border border-pin-line bg-white px-4 py-2 text-xs font-bold text-pin-ink shadow-sm transition hover:border-pin-red hover:text-pin-red"
          >
            ← New board
          </button>
        </div>
      </header>

      {/* Hero summary */}
      <section className="mt-12 animate-fade-up">
        <span className="inline-flex items-center gap-2 rounded-full bg-pin-red/10 px-4 py-1.5 text-xs font-bold uppercase tracking-wide text-pin-red">
          Your study board is ready
        </span>
        <h1 className="mt-4 max-w-3xl font-display text-3xl font-extrabold leading-[1.1] tracking-tight text-balance sm:text-5xl">
          {plan.goal}
        </h1>
        <div className="mt-5 flex flex-wrap gap-2">
          <span className="rounded-full bg-pin-surface px-4 py-2 text-sm font-bold">
            🎯 {gaps.length} gaps found
          </span>
          <span className="rounded-full bg-pin-surface px-4 py-2 text-sm font-bold">
            📅 {milestones.length} weekly milestones
          </span>
          {meta.elapsed_seconds != null && (
            <span className="rounded-full bg-pin-surface px-4 py-2 text-sm font-bold">
              ⚡ Built in {meta.elapsed_seconds}s
            </span>
          )}
        </div>
      </section>

      {/* Verification */}
      <section className="mt-10">
        <VerificationBanner verification={plan.verification} />
      </section>

      {/* Reasoning trace — the multi-step thinking behind the plan */}
      {plan.reasoning_trace?.length > 0 && (
        <Reveal className="mt-12">
          <ReasoningTrace trace={plan.reasoning_trace} />
        </Reveal>
      )}

      {/* Gaps — masonry board */}
      {gaps.length > 0 && (
        <Reveal className="mt-16">
          <SectionHeading
            kicker="Diagnosis"
            title="Where you're losing points"
            count={gaps.length}
          />
          <div className="masonry masonry-2 masonry-3">
            {gaps.map((gap, i) => (
              <GapCard key={i} gap={gap} index={i} />
            ))}
          </div>
          {plan.gap_analysis?.reasoning && (
            <p className="mt-6 rounded-4xl bg-pin-surface px-6 py-5 text-sm leading-relaxed text-pin-muted">
              <span className="font-bold text-pin-ink">Analyst's note — </span>
              {plan.gap_analysis.reasoning}
            </p>
          )}
        </Reveal>
      )}

      {/* Milestones — timeline with tick-off checklist */}
      {milestones.length > 0 && (
        <Reveal className="mt-16">
          <SectionHeading
            kicker="The plan"
            title="Your week-by-week path"
            count={`${milestones.length} wks`}
          />

          {/* Overall progress tracker */}
          {totalObjectives > 0 && (
            <div className="mb-7 rounded-4xl border border-pin-line bg-white p-5 shadow-pin sm:p-6">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="font-display text-lg font-extrabold">
                    {pct === 100 ? "🎉 Plan complete!" : "Your progress"}
                  </p>
                  <p className="text-sm text-pin-muted">
                    {doneObjectives} of {totalObjectives} objectives done — tick
                    them off as you study
                  </p>
                </div>
                <span
                  className={`grid h-14 w-14 shrink-0 place-items-center rounded-full font-display text-lg font-extrabold ${
                    pct === 100
                      ? "bg-emerald-500 text-white"
                      : "bg-pin-red/10 text-pin-red"
                  }`}
                >
                  {pct}%
                </span>
              </div>
              <div className="mt-4 h-2.5 overflow-hidden rounded-full bg-pin-surface">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    pct === 100 ? "bg-emerald-500" : "bg-pin-red"
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          )}

          <div className="space-y-5">
            {milestones.map((m, i) => (
              <MilestoneCard
                key={i}
                milestone={m}
                index={i}
                last={i === milestones.length - 1}
                isChecked={isChecked}
                onToggle={toggle}
              />
            ))}
          </div>
          {adjustments.length > 0 && (
            <div className="mt-6 rounded-4xl border border-pin-line bg-white px-6 py-5">
              <p className="mb-2 text-xs font-bold uppercase tracking-wide text-pin-red">
                Pacing adjustments
              </p>
              <ul className="space-y-1.5 text-sm text-pin-muted">
                {adjustments.map((a, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="text-pin-red">→</span>
                    {a}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </Reveal>
      )}

      {/* Resources — grouped boards */}
      {Object.keys(byGap).length > 0 && (
        <Reveal className="mt-16">
          <SectionHeading
            kicker="Curated"
            title="Resources, pinned per gap"
          />
          <div className="space-y-10">
            {Object.entries(byGap).map(([concept, resources]) => (
              <div key={concept}>
                <div className="mb-4 flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-pin-red" />
                  <h3 className="font-display text-lg font-extrabold">
                    {concept}
                  </h3>
                  <span className="text-sm font-semibold text-pin-muted">
                    · {resources.length} pinned
                  </span>
                </div>
                <div className="masonry masonry-2 masonry-3">
                  {resources.map((r, i) => (
                    <ResourceCard key={i} resource={r} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Reveal>
      )}

      <footer className="mt-20 border-t border-pin-line pt-8 text-center">
        <Logo className="justify-center" />
        <p className="mt-3 text-xs text-pin-muted">
          Reasoned by {meta.agent_count || 5} agents on{" "}
          {meta.framework || "Microsoft Agent Framework"}
        </p>
        <button
          onClick={onReset}
          className="mt-6 rounded-full bg-pin-red px-6 py-3 text-sm font-bold text-white shadow-pin transition hover:bg-pin-dark"
        >
          Build another board
        </button>
      </footer>
    </div>
  );
}
