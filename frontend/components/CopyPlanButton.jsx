"use client";

import { useState } from "react";
import { planToMarkdown } from "@/lib/exportPlan";

export default function CopyPlanButton({ plan }) {
  const [state, setState] = useState("idle"); // idle | copied | error

  const copy = async () => {
    const md = planToMarkdown(plan);
    try {
      await navigator.clipboard.writeText(md);
      setState("copied");
    } catch {
      // Fallback for older browsers / insecure contexts
      try {
        const ta = document.createElement("textarea");
        ta.value = md;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        setState("copied");
      } catch {
        setState("error");
      }
    }
    setTimeout(() => setState("idle"), 2000);
  };

  const label =
    state === "copied"
      ? "✓ Copied!"
      : state === "error"
      ? "Couldn't copy"
      : "Copy as Markdown";

  return (
    <button
      onClick={copy}
      className={`rounded-full px-4 py-2 text-xs font-bold shadow-sm transition ${
        state === "copied"
          ? "bg-emerald-500 text-white"
          : "border border-pin-line bg-white text-pin-ink hover:border-pin-red hover:text-pin-red"
      }`}
    >
      {state === "idle" && (
        <svg
          className="mr-1 inline-block align-[-2px]"
          width="13"
          height="13"
          viewBox="0 0 24 24"
          fill="none"
        >
          <rect
            x="9"
            y="9"
            width="11"
            height="11"
            rx="2"
            stroke="currentColor"
            strokeWidth="2"
          />
          <path
            d="M5 15V5a2 2 0 0 1 2-2h10"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      )}
      {label}
    </button>
  );
}
