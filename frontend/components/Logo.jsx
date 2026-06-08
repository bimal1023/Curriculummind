export default function Logo({ className = "" }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <span className="grid h-9 w-9 place-items-center rounded-full bg-pin-red shadow-pin">
        <span className="font-display text-[13px] font-extrabold tracking-tight text-white">
          CM
        </span>
      </span>
      <span className="font-display text-[19px] font-extrabold tracking-tight">
        Curriculum<span className="text-pin-red">Mind</span>
      </span>
    </div>
  );
}
