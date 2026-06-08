import { ResourceBadge } from "./Badge";

const TRUSTED_DOMAINS = [
  "learn.microsoft.com",
  "docs.microsoft.com",
  "docs.aws.amazon.com",
  "aws.amazon.com",
  "cloud.google.com",
  "developers.google.com",
  "developer.mozilla.org",
  "youtube.com",
  "youtu.be",
  "coursera.org",
  "edx.org",
  "udemy.com",
  "freecodecamp.org",
  "kaggle.com",
  "github.com",
];

function isTrusted(url) {
  try {
    const host = new URL(url).hostname.replace(/^www\./, "");
    return TRUSTED_DOMAINS.some((d) => host === d || host.endsWith("." + d));
  } catch {
    return false;
  }
}

export default function ResourceCard({ resource }) {
  const trusted = isTrusted(resource.url);

  return (
    <a
      href={resource.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group block animate-fade-up rounded-3xl border border-pin-line bg-white p-5 shadow-pin transition duration-300 hover:-translate-y-1 hover:shadow-pin-hover"
    >
      <div className="flex items-center justify-between gap-2">
        <ResourceBadge type={resource.resource_type} />
        <div className="flex items-center gap-2">
          {!trusted && (
            <span
              title="URL may not be verified — double-check before using"
              className="rounded-full bg-amber-50 px-2.5 py-1 text-[11px] font-bold text-amber-500 ring-1 ring-amber-200"
            >
              ⚠ unverified
            </span>
          )}
          <span className="rounded-full bg-pin-cream px-2.5 py-1 text-[11px] font-bold text-pin-muted">
            ~{resource.estimated_hours}h
          </span>
        </div>
      </div>

      <h4 className="mt-3 font-display text-base font-extrabold leading-snug text-balance transition group-hover:text-pin-red">
        {resource.title}
      </h4>

      <p className="mt-2 text-sm leading-relaxed text-pin-muted">
        {resource.relevance_reason}
      </p>

      <div className="mt-3 flex items-center justify-between">
        <span className="truncate text-[11px] text-pin-muted/60">
          {resource.url}
        </span>
        <span className="ml-2 inline-flex shrink-0 items-center gap-1 text-xs font-bold text-pin-red opacity-0 transition group-hover:opacity-100">
          Open
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
      </div>
    </a>
  );
}
