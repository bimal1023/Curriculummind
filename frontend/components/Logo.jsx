export default function Logo({ className = "" }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <span className="grid h-9 w-9 place-items-center rounded-full bg-pin-red text-white shadow-pin">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden>
          <path
            d="M12 2C6.5 2 3 5.7 3 10.3c0 3.5 2 5.4 3.2 5.4.5 0 .8-1.4.8-1.8 0-.5-1.2-1.6-1.2-3.8 0-2.9 2.2-5 5.7-5 3 0 4.7 1.8 4.7 4.2 0 3.2-1.4 5.8-3.5 5.8-1.1 0-2-.9-1.7-2.1.4-1.4 1-2.8 1-3.8 0-2.3-3.3-2-3.3 1.1 0 .6.2 1.1.2 1.1S10.7 18 10.4 19.3c-.5 2.2 0 4.9 0 5.1.05.1.16.13.22.05.1-.13 1.4-1.7 1.84-3.3.12-.45.7-2.74.7-2.74.35.66 1.36 1.23 2.44 1.23 3.2 0 5.4-2.93 5.4-6.85C21 5.85 17.8 2 12 2Z"
            fill="currentColor"
          />
        </svg>
      </span>
      <span className="font-display text-[19px] font-extrabold tracking-tight">
        Curriculum<span className="text-pin-red">Mind</span>
      </span>
    </div>
  );
}
