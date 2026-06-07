import { Pill } from "./Badge";

export default function MilestoneCard({ milestone, index, last }) {
  return (
    <div
      className="relative animate-fade-up pl-12"
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      {/* timeline rail */}
      {!last && (
        <span className="absolute left-[18px] top-12 h-[calc(100%-1rem)] w-0.5 bg-gradient-to-b from-pin-red/40 to-pin-line" />
      )}
      <span className="absolute left-0 top-1 grid h-9 w-9 place-items-center rounded-full bg-pin-red text-sm font-extrabold text-white shadow-pin">
        {milestone.week}
      </span>

      <article className="rounded-4xl border border-pin-line bg-white p-6 shadow-pin transition hover:shadow-pin-hover">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] font-bold uppercase tracking-wide text-pin-red">
            Week {milestone.week}
          </span>
          {milestone.closes_gaps?.map((g) => (
            <Pill key={g} className="bg-pin-red/5 text-pin-red">
              {g}
            </Pill>
          ))}
        </div>

        <h3 className="mt-2 font-display text-xl font-extrabold leading-tight text-balance">
          {milestone.title}
        </h3>

        {milestone.objectives?.length > 0 && (
          <ul className="mt-4 space-y-2">
            {milestone.objectives.map((o, i) => (
              <li key={i} className="flex gap-2.5 text-sm text-pin-ink">
                <svg
                  className="mt-0.5 shrink-0 text-pin-red"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <path
                    d="M5 12.5l4 4 10-10"
                    stroke="currentColor"
                    strokeWidth="2.4"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <span className="leading-snug">{o}</span>
              </li>
            ))}
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
