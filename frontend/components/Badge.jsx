const SEVERITY = {
  high: "bg-pin-red/10 text-pin-red ring-pin-red/20",
  medium: "bg-amber-500/10 text-amber-600 ring-amber-500/20",
  low: "bg-emerald-500/10 text-emerald-600 ring-emerald-500/20",
};

const RESOURCE = {
  official_docs: "bg-blue-500/10 text-blue-600 ring-blue-500/20",
  video: "bg-pin-red/10 text-pin-red ring-pin-red/20",
  practice: "bg-violet-500/10 text-violet-600 ring-violet-500/20",
  article: "bg-amber-500/10 text-amber-600 ring-amber-500/20",
  book: "bg-emerald-500/10 text-emerald-600 ring-emerald-500/20",
};

const RESOURCE_LABEL = {
  official_docs: "Official docs",
  video: "Video",
  practice: "Practice",
  article: "Article",
  book: "Book",
};

export function SeverityBadge({ level }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide ring-1 ${
        SEVERITY[level] || SEVERITY.low
      }`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {level} priority
    </span>
  );
}

export function ResourceBadge({ type }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide ring-1 ${
        RESOURCE[type] || RESOURCE.article
      }`}
    >
      {RESOURCE_LABEL[type] || type}
    </span>
  );
}

export function Pill({ children, className = "" }) {
  return (
    <span
      className={`inline-flex items-center rounded-full bg-pin-surface px-3 py-1 text-xs font-semibold text-pin-muted ${className}`}
    >
      {children}
    </span>
  );
}
