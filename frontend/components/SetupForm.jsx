"use client";

import { useState } from "react";
import { RESOURCE_TYPES } from "@/lib/api";
import Logo from "./Logo";

const SAMPLE = {
  name: "Bimal Thapa",
  goal: "Pass the AZ-900 Microsoft Azure Fundamentals exam in 6 weeks and understand core cloud concepts",
  target_deadline_weeks: 6,
  hours_per_week: 10,
  prior_courses: "AWS Cloud Practitioner Essentials, Python for Data Science",
  preferred_resource_types: ["official_docs", "video", "practice"],
  assessment_results: [
    { topic: "Cloud concepts", score: 55, total_questions: 20 },
    { topic: "Azure architecture", score: 40, total_questions: 25 },
    { topic: "Security and compliance", score: 35, total_questions: 20 },
  ],
};

const EMPTY = {
  name: "",
  goal: "",
  target_deadline_weeks: 6,
  hours_per_week: 8,
  prior_courses: "",
  preferred_resource_types: ["official_docs"],
  assessment_results: [{ topic: "", score: 50, total_questions: 20 }],
};

const field =
  "w-full rounded-2xl border border-pin-line bg-white px-4 py-3 text-sm font-medium text-pin-ink outline-none transition placeholder:text-pin-muted/60 focus:border-pin-red focus:ring-4 focus:ring-pin-red/10";
const label = "mb-1.5 block text-xs font-bold uppercase tracking-wide text-pin-muted";

export default function SetupForm({ onSubmit, error }) {
  const [form, setForm] = useState(EMPTY);

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const setAssessment = (i, k, v) =>
    setForm((f) => ({
      ...f,
      assessment_results: f.assessment_results.map((a, idx) =>
        idx === i ? { ...a, [k]: v } : a
      ),
    }));

  const addAssessment = () =>
    setForm((f) => ({
      ...f,
      assessment_results: [
        ...f.assessment_results,
        { topic: "", score: 50, total_questions: 20 },
      ],
    }));

  const removeAssessment = (i) =>
    setForm((f) => ({
      ...f,
      assessment_results: f.assessment_results.filter((_, idx) => idx !== i),
    }));

  const toggleType = (value) =>
    setForm((f) => ({
      ...f,
      preferred_resource_types: f.preferred_resource_types.includes(value)
        ? f.preferred_resource_types.filter((t) => t !== value)
        : [...f.preferred_resource_types, value],
    }));

  const submit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <div className="relative z-[2] mx-auto max-w-6xl px-5 py-10 sm:py-16">
      {/* Top bar */}
      <header className="flex items-center justify-between">
        <Logo />
        <button
          type="button"
          onClick={() => setForm(SAMPLE)}
          className="rounded-full border border-pin-line bg-white px-4 py-2 text-xs font-bold text-pin-ink shadow-sm transition hover:border-pin-red hover:text-pin-red"
        >
          ✨ Fill sample
        </button>
      </header>

      {/* Hero */}
      <section className="mt-14 text-center sm:mt-20">
        <span className="inline-flex animate-pop-in items-center gap-2 rounded-full bg-pin-red/10 px-4 py-1.5 text-xs font-bold uppercase tracking-wide text-pin-red">
          <span className="h-2 w-2 animate-pulse rounded-full bg-pin-red" />
          Reasoned by 5 AI agents
        </span>
        <h1 className="mx-auto mt-6 max-w-3xl animate-fade-up font-display text-4xl font-extrabold leading-[1.05] tracking-tight text-balance sm:text-6xl">
          Pin your goal.
          <br />
          We&apos;ll build the{" "}
          <span className="relative whitespace-nowrap text-pin-red">
            study board
            <svg
              className="absolute -bottom-2 left-0 w-full"
              viewBox="0 0 200 12"
              fill="none"
              aria-hidden
            >
              <path
                d="M2 9C50 3 150 3 198 8"
                stroke="#E60023"
                strokeWidth="3"
                strokeLinecap="round"
                opacity="0.4"
              />
            </svg>
          </span>
          .
        </h1>
        <p
          className="mx-auto mt-6 max-w-xl animate-fade-up text-base text-pin-muted sm:text-lg"
          style={{ animationDelay: "0.1s" }}
        >
          Tell us your goal and how your diagnostic went. CurriculumMind finds
          your gaps and curates a verified, week-by-week plan.
        </p>
      </section>

      {/* Form card */}
      <form
        onSubmit={submit}
        className="mx-auto mt-12 max-w-3xl animate-fade-up rounded-4xl border border-pin-line bg-white/80 p-6 shadow-pin backdrop-blur sm:p-9"
        style={{ animationDelay: "0.2s" }}
      >
        {error && (
          <div className="mb-6 rounded-2xl border border-pin-red/20 bg-pin-red/5 px-4 py-3 text-sm font-semibold text-pin-red">
            {error}
          </div>
        )}

        <div className="grid gap-5 sm:grid-cols-2">
          <div>
            <label className={label}>Your name</label>
            <input
              className={field}
              value={form.name}
              onChange={(e) => set("name", e.target.value)}
              placeholder="Bimal Thapa"
              required
            />
          </div>
          <div>
            <label className={label}>Prior courses (comma-separated)</label>
            <input
              className={field}
              value={form.prior_courses}
              onChange={(e) => set("prior_courses", e.target.value)}
              placeholder="AWS Cloud Practitioner, Python…"
            />
          </div>
        </div>

        <div className="mt-5">
          <label className={label}>What&apos;s your goal?</label>
          <textarea
            className={`${field} min-h-[88px] resize-none`}
            value={form.goal}
            onChange={(e) => set("goal", e.target.value)}
            placeholder="Pass the AZ-900 exam in 6 weeks and understand core cloud concepts"
            minLength={10}
            required
          />
        </div>

        <div className="mt-5 grid gap-5 sm:grid-cols-2">
          <div>
            <label className={label}>Deadline (weeks)</label>
            <input
              type="number"
              min={1}
              max={52}
              className={field}
              value={form.target_deadline_weeks}
              onChange={(e) => set("target_deadline_weeks", e.target.value)}
              required
            />
          </div>
          <div>
            <label className={label}>Hours per week</label>
            <input
              type="number"
              min={1}
              max={40}
              step="0.5"
              className={field}
              value={form.hours_per_week}
              onChange={(e) => set("hours_per_week", e.target.value)}
              required
            />
          </div>
        </div>

        {/* Assessment results */}
        <div className="mt-8">
          <div className="mb-3 flex items-center justify-between">
            <label className={`${label} mb-0`}>Diagnostic results</label>
            <button
              type="button"
              onClick={addAssessment}
              className="rounded-full bg-pin-surface px-3 py-1.5 text-xs font-bold text-pin-ink transition hover:bg-pin-red hover:text-white"
            >
              + Add topic
            </button>
          </div>

          <div className="space-y-3">
            {form.assessment_results.map((a, i) => (
              <div
                key={i}
                className="grid grid-cols-12 items-center gap-2 rounded-2xl bg-pin-cream p-2"
              >
                <input
                  className={`${field} col-span-6`}
                  value={a.topic}
                  onChange={(e) => setAssessment(i, "topic", e.target.value)}
                  placeholder="Topic, e.g. Cloud concepts"
                  required
                />
                <div className="col-span-3 flex items-center gap-1 rounded-2xl border border-pin-line bg-white px-3">
                  <input
                    type="number"
                    min={0}
                    max={100}
                    className="w-full bg-transparent py-3 text-sm font-semibold outline-none"
                    value={a.score}
                    onChange={(e) => setAssessment(i, "score", e.target.value)}
                  />
                  <span className="text-xs font-bold text-pin-muted">%</span>
                </div>
                <div className="col-span-2 flex items-center gap-1 rounded-2xl border border-pin-line bg-white px-3">
                  <input
                    type="number"
                    min={1}
                    className="w-full bg-transparent py-3 text-sm font-semibold outline-none"
                    value={a.total_questions}
                    onChange={(e) =>
                      setAssessment(i, "total_questions", e.target.value)
                    }
                  />
                  <span className="text-xs font-bold text-pin-muted">Qs</span>
                </div>
                <button
                  type="button"
                  onClick={() => removeAssessment(i)}
                  disabled={form.assessment_results.length === 1}
                  className="col-span-1 grid h-9 w-9 place-items-center justify-self-center rounded-full text-pin-muted transition hover:bg-pin-red/10 hover:text-pin-red disabled:opacity-30"
                  aria-label="Remove topic"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Resource preferences */}
        <div className="mt-8">
          <label className={label}>Preferred resources</label>
          <div className="flex flex-wrap gap-2">
            {RESOURCE_TYPES.map((rt) => {
              const active = form.preferred_resource_types.includes(rt.value);
              return (
                <button
                  type="button"
                  key={rt.value}
                  onClick={() => toggleType(rt.value)}
                  className={`rounded-full px-4 py-2 text-sm font-bold transition ${
                    active
                      ? "bg-pin-ink text-white shadow-pin"
                      : "border border-pin-line bg-white text-pin-muted hover:border-pin-ink hover:text-pin-ink"
                  }`}
                >
                  {rt.label}
                </button>
              );
            })}
          </div>
        </div>

        <button
          type="submit"
          className="mt-10 flex w-full items-center justify-center gap-2 rounded-full bg-pin-red py-4 text-base font-bold text-white shadow-pin transition hover:bg-pin-dark hover:shadow-pin-hover active:scale-[0.99]"
        >
          Build my study board
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden>
            <path
              d="M5 12h14M13 6l6 6-6 6"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </form>

      <p className="mt-8 text-center text-xs text-pin-muted">
        Powered by Microsoft Agent Framework · Azure AI Foundry · Azure AI Search
      </p>
    </div>
  );
}
