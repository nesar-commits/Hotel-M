export default function Logo({ className = "" }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <svg
        width="36"
        height="36"
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="tastyhub-badge" x1="0" y1="0" x2="40" y2="40">
            <stop stopColor="#E23744" />
            <stop offset="1" stopColor="#CB202D" />
          </linearGradient>
        </defs>
        <rect width="40" height="40" rx="11" fill="url(#tastyhub-badge)" />
        {/* chef's hat */}
        <circle cx="13.5" cy="16.5" r="6" fill="white" />
        <circle cx="20" cy="10.5" r="7.5" fill="white" />
        <circle cx="26.5" cy="16.5" r="6" fill="white" />
        <rect x="10.5" y="15" width="19" height="8" fill="white" />
        <rect x="9.5" y="23" width="21" height="7" rx="2.5" fill="white" />
        <rect x="9.5" y="26.7" width="21" height="1.3" fill="#E23744" opacity="0.25" />
      </svg>
      <span className="text-2xl font-extrabold tracking-tight">
        <span className="text-gray-900">Tasty</span>
        <span className="text-zomato">Hub</span>
      </span>
    </div>
  );
}
