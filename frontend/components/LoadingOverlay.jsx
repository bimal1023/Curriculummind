"use client";

import { useEffect, useState } from "react";

const STEPS = [
  { key: "diagnose", label: "Diagnosing your gaps", agent: "DiagnosticAnalyzer" },
  { key: "plan", label: "Planning milestones", agent: "GoalPlanner" },
  { key: "curate", label: "Curating resources", agent: "ContentCurator" },
  { key: "pace", label: "Pacing your weeks", agent: "PaceReasoner" },
  { key: "verify", label: "Verifying the plan", agent: "Verifier" },
];

export default function LoadingOverlay() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setActive((a) => (a < STEPS.length - 1 ? a + 1 : a));
    }, 2600);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-pin-cream/85 px-5 backdrop-blur-md">
      <div className="w-full max-w-md animate-pop-in rounded-4xl border border-pin-line bg-white p-8 shadow-pin-hover">
        <div className="flex items-center gap-3">
          <div className="relative grid h-12 w-12 place-items-center">
            <span className="absolute inset-0 animate-ping rounded-full bg-pin-red/20" />
            <span className="grid h-12 w-12 place-items-center rounded-full bg-pin-red text-white">
              <svg
                className="animate-spin"
                width="22"
                height="22"
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="9"
                  stroke="currentColor"
                  strokeWidth="3"
                  opacity="0.25"
                />
                <path
                  d="M21 12a9 9 0 0 0-9-9"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
            </span>
          </div>
          <div>
            <p className="font-display text-lg font-extrabold">
              Building your board…
            </p>
            <p className="text-sm text-pin-muted">This usually takes ~30 seconds</p>
          </div>
        </div>

        <ol className="mt-8 space-y-1">
          {STEPS.map((step, i) => {
            const done = i < active;
            const current = i === active;
            return (
              <li
                key={step.key}
                className={`flex items-center gap-3 rounded-2xl px-3 py-2.5 transition ${
                  current ? "bg-pin-red/5" : ""
                }`}
              >
                <span
                  className={`grid h-7 w-7 shrink-0 place-items-center rounded-full text-xs font-bold transition ${
                    done
                      ? "bg-emerald-500 text-white"
                      : current
                      ? "bg-pin-red text-white"
                      : "bg-pin-surface text-pin-muted"
                  }`}
                >
                  {done ? "✓" : i + 1}
                </span>
                <div className="min-w-0 flex-1">
                  <p
                    className={`truncate text-sm font-bold transition ${
                      done || current ? "text-pin-ink" : "text-pin-muted"
                    }`}
                  >
                    {step.label}
                  </p>
                  <p className="truncate text-[11px] font-medium text-pin-muted">
                    {step.agent}
                  </p>
                </div>
                {current && (
                  <span className="flex gap-1">
                    {[0, 1, 2].map((d) => (
                      <span
                        key={d}
                        className="h-1.5 w-1.5 animate-pulse rounded-full bg-pin-red"
                        style={{ animationDelay: `${d * 0.2}s` }}
                      />
                    ))}
                  </span>
                )}
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}
