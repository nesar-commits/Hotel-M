import { useEffect, useRef, useState } from "react";
import { useUserLocation } from "../context/UserLocationContext.jsx";

export default function LocationBar() {
  const { location, status, detectLocation, searchLocations, setManualLocation } =
    useUserLocation();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const boxRef = useRef(null);

  useEffect(() => {
    function onClickOutside(e) {
      if (boxRef.current && !boxRef.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  useEffect(() => {
    if (query.trim().length < 3) {
      setResults([]);
      setSearching(false);
      return;
    }
    setSearching(true);
    const handle = setTimeout(() => {
      searchLocations(query)
        .then(setResults)
        .catch(() => setResults([]))
        .finally(() => setSearching(false));
    }, 500);
    return () => clearTimeout(handle);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);

  const handleDetect = () => {
    detectLocation()
      .then(() => setOpen(false))
      .catch(() => {});
  };

  const handlePick = (loc) => {
    setManualLocation(loc);
    setOpen(false);
    setQuery("");
    setResults([]);
  };

  return (
    <div className="relative" ref={boxRef}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex max-w-[200px] items-center gap-1.5 rounded-full border border-gray-200 px-3 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50"
      >
        <span>📍</span>
        <span className="truncate">
          {status === "locating" ? "Locating..." : location?.label || "Set location"}
        </span>
        <span className="text-xs text-gray-400">▾</span>
      </button>

      {open && (
        <div className="absolute left-0 top-full z-40 mt-2 w-80 rounded-xl bg-white p-4 shadow-xl">
          <button
            onClick={handleDetect}
            disabled={status === "locating"}
            className="mb-3 flex w-full items-center gap-2 rounded-lg bg-zomato-light px-3 py-2.5 text-sm font-bold text-zomato hover:brightness-95 disabled:opacity-60"
          >
            🎯 {status === "locating" ? "Detecting your location..." : "Use current location"}
          </button>

          {status === "denied" && (
            <p className="mb-3 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-600">
              Location access was denied. Allow it in your browser's site settings, or search for
              an area below.
            </p>
          )}
          {status === "error" && (
            <p className="mb-3 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-600">
              Couldn't determine your location. Try again, or search for an area below.
            </p>
          )}

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for area, city..."
            autoFocus
            className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-zomato"
          />

          {searching && <p className="mt-2 text-xs text-gray-400">Searching...</p>}

          {!searching && query.trim().length >= 3 && results.length === 0 && (
            <p className="mt-2 text-xs text-gray-400">No matches found.</p>
          )}

          {results.length > 0 && (
            <ul className="mt-2 max-h-56 space-y-0.5 overflow-y-auto">
              {results.map((r, i) => (
                <li key={i}>
                  <button
                    onClick={() => handlePick(r)}
                    className="w-full rounded-lg px-2 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                  >
                    📍 {r.label}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
