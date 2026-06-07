import { ResourceBadge } from "./Badge";

export default function ResourceCard({ resource }) {
  return (
    <a
      href={resource.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group block animate-fade-up rounded-3xl border border-pin-line bg-white p-5 shadow-pin transition duration-300 hover:-translate-y-1 hover:shadow-pin-hover"
    >
      <div className="flex items-center justify-between gap-2">
        <ResourceBadge type={resource.resource_type} />
        <span className="rounded-full bg-pin-cream px-2.5 py-1 text-[11px] font-bold text-pin-muted">
          ~{resource.estimated_hours}h
        </span>
      </div>

      <h4 className="mt-3 font-display text-base font-extrabold leading-snug text-balance transition group-hover:text-pin-red">
        {resource.title}
      </h4>

      <p className="mt-2 text-sm leading-relaxed text-pin-muted">
        {resource.relevance_reason}
      </p>

      <span className="mt-3 inline-flex items-center gap-1 text-xs font-bold text-pin-red opacity-0 transition group-hover:opacity-100">
        Open resource
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
          <path
            d="M7 17 17 7M9 7h8v8"
            stroke="currentColor"
            strokeWidth="2.4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </span>
    </a>
  );
}
