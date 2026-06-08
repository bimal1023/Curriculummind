"use client";

import { useState } from "react";

// Each agent gets a glyph so the trace reads at a glance.
const GLYPH = {
  DiagnosticAnalyzer: "🔍",
  GoalPlanner: "🗺️",
  ContentCurator: "📚",
  PaceReasoner: "⏱️",
  Verifier: "✓",
};

function ThoughtRow({ thought, last }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative pl-14">
      {/* rail */}
      {!last && (
        <span className="absolute left-[26px] top-12 h-[calc(100%-1.5rem)] w-0.5 bg-gradient-to-b from-pin-red/30 to-pin-line" />
      )}

      {/* node */}
      <span className="absolute left-2 top-1 grid h-10 w-10 place-items-center rounded-2xl bg-white text-lg shadow-pin ring-1 ring-pin-line">
        {GLYPH[thought.agent] || "🧠"}
      </span>

      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full rounded-3xl border border-pin-line bg-white p-5 text-left shadow-pin transition hover:shadow-pin-hover"
      >
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-display text-base font-extrabold">
            {thought.agent}
          </span>
          {thought.parallel && (
            <span className="rounded-full bg-violet-500/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-violet-600 ring-1 ring-violet-500/20">
              ⇄ parallel
            </span>
          )}
          <span className="ml-auto text-[11px] font-bold uppercase tracking-wide text-pin-muted">
            Step {thought.step}
          </span>
        </div>

        <p className="mt-1 text-xs font-semibold text-pin-muted">
          {thought.role}
        </p>

        <p className="mt-3 flex items-start gap-2 text-sm font-bold text-pin-ink">
          <span className="text-pin-red">→</span>
          {thought.summary}
        </p>

        {/* reasoning narrative — collapsible */}
        <div
          className={`grid transition-all duration-300 ${
            open ? "mt-3 grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
          }`}
        >
          <div className="overflow-hidden">
            <p className="rounded-2xl bg-pin-cream px-4 py-3 text-sm italic leading-relaxed text-pin-muted">
              💭 {thought.reasoning}
            </p>
          </div>
        </div>

        <span className="mt-3 inline-flex items-center gap-1 text-[11px] font-bold text-pin-red">
          {open ? "Hide reasoning" : "Read its reasoning"}
          <svg
            className={`transition ${open ? "rotate-180" : ""}`}
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              strokeWidth="2.4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
      </button>
    </div>
  );
}

export default function ReasoningTrace({ trace = [] }) {
  if (!trace.length) return null;

  return (
    <div className="rounded-4xl border border-pin-line bg-pin-surface/50 p-6 sm:p-8">
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-pin-red">
            Show your work
          </p>
          <h2 className="mt-1 font-display text-2xl font-extrabold tracking-tight sm:text-3xl">
            How {trace.length} agents reasoned this
          </h2>
          <p className="mt-1 text-sm text-pin-muted">
            Each step is a separate AI agent. Click any to read its thinking.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {trace.map((t, i) => (
          <ThoughtRow
            key={t.step}
            thought={t}
            last={i === trace.length - 1}
          />
        ))}
      </div>
    </div>
  );
}
