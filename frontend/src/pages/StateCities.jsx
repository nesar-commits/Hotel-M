import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getStateCities } from "../api/client.js";

export default function StateCities() {
  const { slug } = useParams();
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getStateCities(slug)
      .then(setState)
      .catch(() => setError("Could not find that state or union territory."))
      .finally(() => setLoading(false));
  }, [slug]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <Link to="/cities" className="mb-4 inline-block text-sm font-semibold text-zomato">
        ← All states
      </Link>

      {loading && <p className="text-sm text-gray-500">Loading cities...</p>}
      {error && <p className="text-sm font-medium text-red-600">{error}</p>}

      {state && (
        <>
          <div className="mb-6 rounded-2xl bg-gradient-to-r from-zomato to-zomato-dark p-8 text-white">
            <h1 className="text-3xl font-extrabold">{state.name}</h1>
            <p className="mt-2 text-white/90">{state.cities.length} cities</p>
            {state.note && <p className="mt-2 text-sm text-white/80">{state.note}</p>}
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            {state.cities.map((city) => (
              <Link
                key={city}
                to={`/?city=${encodeURIComponent(city)}`}
                className="rounded-xl bg-white px-4 py-3 text-center text-sm font-semibold text-gray-800 shadow transition hover:bg-zomato-light hover:text-zomato"
              >
                {city}
              </Link>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
