import { SeverityBadge, Pill } from "./Badge";

export default function GapCard({ gap, index }) {
  return (
    <article
      className="group animate-fade-up rounded-4xl border border-pin-line bg-white p-6 shadow-pin transition duration-300 hover:-translate-y-1 hover:shadow-pin-hover"
      style={{ animationDelay: `${index * 0.06}s` }}
    >
      <div className="flex items-start justify-between gap-3">
        <SeverityBadge level={gap.severity} />
        <span className="font-display text-3xl font-extrabold text-pin-line transition group-hover:text-pin-red/20">
          {String(index + 1).padStart(2, "0")}
        </span>
      </div>

      <h3 className="mt-3 font-display text-xl font-extrabold leading-tight text-balance">
        {gap.concept}
      </h3>

      <p className="mt-2.5 text-sm leading-relaxed text-pin-muted">
        {gap.evidence}
      </p>

      {gap.prerequisite_for?.length > 0 && (
        <div className="mt-4 border-t border-pin-line pt-4">
          <p className="mb-2 text-[11px] font-bold uppercase tracking-wide text-pin-muted">
            Unlocks
          </p>
          <div className="flex flex-wrap gap-1.5">
            {gap.prerequisite_for.map((p) => (
              <Pill key={p}>{p}</Pill>
            ))}
          </div>
        </div>
      )}
    </article>
  );
}
