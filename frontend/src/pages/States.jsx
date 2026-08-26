import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getStates } from "../api/client.js";
import SearchBar from "../components/SearchBar.jsx";

export default function States() {
  const [states, setStates] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getStates()
      .then(setStates)
      .catch(() =>
        setError(
          "Could not reach the backend API. Make sure it's running at http://localhost:8000.",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(
    () => states.filter((s) => s.name.toLowerCase().includes(search.toLowerCase())),
    [states, search],
  );

  const statesList = filtered.filter((s) => s.type === "state");
  const utList = filtered.filter((s) => s.type === "union_territory");

  const renderGrid = (list) => (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
      {list.map((s) => (
        <Link
          key={s.slug}
          to={`/cities/${s.slug}`}
          className="flex flex-col justify-between rounded-xl bg-white p-4 shadow transition hover:shadow-lg"
        >
          <h3 className="font-semibold text-gray-900">{s.name}</h3>
          <p className="mt-2 text-sm text-gray-500">{s.city_count} cities</p>
        </Link>
      ))}
    </div>
  );

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <div className="mb-6 rounded-2xl bg-gradient-to-r from-zomato to-zomato-dark p-8 text-white">
        <h1 className="text-3xl font-extrabold">Browse by State</h1>
        <p className="mt-2 text-white/90">
          Pick a state or union territory to see its major cities.
        </p>
        <div className="mt-4 max-w-md">
          <SearchBar value={search} onChange={setSearch} placeholder="Search states..." />
        </div>
      </div>

      {error && <p className="mb-4 text-sm font-medium text-red-600">{error}</p>}
      {loading && <p className="text-sm text-gray-500">Loading states...</p>}

      {!loading && !error && (
        <>
          <h2 className="mb-3 text-lg font-bold text-gray-900">
            States <span className="font-normal text-gray-400">({statesList.length})</span>
          </h2>
          {renderGrid(statesList)}

          {utList.length > 0 && (
            <>
              <h2 className="mb-3 mt-8 text-lg font-bold text-gray-900">
                Union Territories{" "}
                <span className="font-normal text-gray-400">({utList.length})</span>
              </h2>
              {renderGrid(utList)}
            </>
          )}

          {filtered.length === 0 && (
            <p className="text-sm text-gray-500">No states match your search.</p>
          )}
        </>
      )}
    </div>
  );
}
