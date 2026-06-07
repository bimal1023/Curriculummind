export default function SectionHeading({ kicker, title, count }) {
  return (
    <div className="mb-7 flex items-end justify-between gap-4">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.18em] text-pin-red">
          {kicker}
        </p>
        <h2 className="mt-1 font-display text-2xl font-extrabold tracking-tight sm:text-3xl">
          {title}
        </h2>
      </div>
      {count != null && (
        <span className="shrink-0 rounded-full bg-pin-ink px-3.5 py-1.5 text-sm font-extrabold text-white">
          {count}
        </span>
      )}
    </div>
  );
}
