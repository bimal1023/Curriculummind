import { Pill } from "./Badge";
import { objectiveKey } from "@/lib/progress";

export default function MilestoneCard({
  milestone,
  index,
  last,
  isChecked,
  onToggle,
}) {
  const objectives = milestone.objectives || [];
  const doneCount = objectives.filter((o, i) =>
    isChecked(objectiveKey(milestone.week, i, o))
  ).length;
  const allDone = objectives.length > 0 && doneCount === objectives.length;

  return (
    <div
      className="relative animate-fade-up pl-12"
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      {/* timeline rail */}
      {!last && (
        <span className="absolute left-[18px] top-12 h-[calc(100%-1rem)] w-0.5 bg-gradient-to-b from-pin-red/40 to-pin-line" />
      )}
      <span
        className={`absolute left-0 top-1 grid h-9 w-9 place-items-center rounded-full text-sm font-extrabold text-white shadow-pin transition ${
          allDone ? "bg-emerald-500" : "bg-pin-red"
        }`}
      >
        {allDone ? "✓" : milestone.week}
      </span>

      <article
        className={`rounded-4xl border bg-white p-6 shadow-pin transition hover:shadow-pin-hover ${
          allDone ? "border-emerald-200" : "border-pin-line"
        }`}
      >
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] font-bold uppercase tracking-wide text-pin-red">
            Week {milestone.week}
          </span>
          {milestone.closes_gaps?.map((g) => (
            <Pill key={g} className="bg-pin-red/5 text-pin-red">
              {g}
            </Pill>
          ))}
          {objectives.length > 0 && (
            <span
              className={`ml-auto rounded-full px-2.5 py-1 text-[11px] font-bold transition ${
                allDone
                  ? "bg-emerald-500/10 text-emerald-600"
                  : "bg-pin-surface text-pin-muted"
              }`}
            >
              {doneCount}/{objectives.length} done
            </span>
          )}
        </div>

        <h3 className="mt-2 font-display text-xl font-extrabold leading-tight text-balance">
          {milestone.title}
        </h3>

        {objectives.length > 0 && (
          <ul className="mt-4 space-y-1.5">
            {objectives.map((o, i) => {
              const key = objectiveKey(milestone.week, i, o);
              const checked = isChecked(key);
              return (
                <li key={i}>
                  <button
                    onClick={() => onToggle(key)}
                    className="flex w-full items-start gap-3 rounded-2xl px-3 py-2 text-left text-sm transition hover:bg-pin-cream"
                  >
                    <span
                      className={`mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-md border-2 transition ${
                        checked
                          ? "border-emerald-500 bg-emerald-500 text-white"
                          : "border-pin-line bg-white text-transparent"
                      }`}
                    >
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                        <path
                          d="M5 12.5l4 4 10-10"
                          stroke="currentColor"
                          strokeWidth="3"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </span>
                    <span
                      className={`leading-snug transition ${
                        checked
                          ? "text-pin-muted line-through"
                          : "text-pin-ink"
                      }`}
                    >
                      {o}
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        )}

        {milestone.reasoning && (
          <p className="mt-4 rounded-2xl bg-pin-cream px-4 py-3 text-xs italic leading-relaxed text-pin-muted">
            💭 {milestone.reasoning}
          </p>
        )}
      </article>
    </div>
  );
}
