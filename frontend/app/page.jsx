"use client";

import { useState } from "react";
import { generatePlan } from "@/lib/api";
import SetupForm from "@/components/SetupForm";
import LoadingOverlay from "@/components/LoadingOverlay";
import Results from "@/components/Results";

export default function Home() {
  const [view, setView] = useState("setup"); // setup | loading | results
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (form) => {
    setError("");
    setView("loading");
    try {
      const result = await generatePlan(form);
      setPlan(result);
      setView("results");
    } catch (err) {
      setError(
        err.message ||
          "Couldn't reach the backend. Is it running on http://localhost:8000?"
      );
      setView("setup");
    }
  };

  const reset = () => {
    setPlan(null);
    setError("");
    setView("setup");
  };

  return (
    <main>
      {view === "loading" && <LoadingOverlay />}
      {view === "results" && plan ? (
        <Results plan={plan} onReset={reset} />
      ) : (
        <SetupForm onSubmit={handleSubmit} error={error} />
      )}
    </main>
  );
}
