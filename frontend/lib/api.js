// Talks to the CurriculumMind FastAPI backend.
// Override with NEXT_PUBLIC_API_URL if your backend runs elsewhere.

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "http://localhost:8000";

export const RESOURCE_TYPES = [
  { value: "official_docs", label: "Official docs" },
  { value: "video", label: "Video" },
  { value: "practice", label: "Practice" },
  { value: "article", label: "Article" },
  { value: "book", label: "Book" },
];

export async function generatePlan(form) {
  const payload = {
    student_id:
      form.student_id?.trim() ||
      `student_${Math.random().toString(36).slice(2, 9)}`,
    name: form.name.trim(),
    goal: form.goal.trim(),
    target_deadline_weeks: Number(form.target_deadline_weeks),
    hours_per_week: Number(form.hours_per_week),
    assessment_results: form.assessment_results
      .filter((a) => a.topic.trim())
      .map((a) => ({
        topic: a.topic.trim(),
        score: Number(a.score),
        total_questions: Number(a.total_questions),
      })),
    prior_courses: form.prior_courses
      .split(",")
      .map((c) => c.trim())
      .filter(Boolean),
    preferred_resource_types: form.preferred_resource_types,
  };

  const res = await fetch(`${API_BASE}/api/v1/plans/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg =
      data?.detail || data?.error || `Request failed (${res.status})`;
    throw new Error(msg);
  }

  return data;
}
