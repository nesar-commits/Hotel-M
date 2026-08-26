import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getRestaurants } from "../api/client.js";
import RestaurantCard from "../components/RestaurantCard.jsx";
import SearchBar from "../components/SearchBar.jsx";

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  const city = searchParams.get("city") || "";
  const [restaurants, setRestaurants] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (search) params.search = search;
    if (city) params.city = city;
    getRestaurants(params)
      .then(setRestaurants)
      .catch(() =>
        setError(
          "Could not reach the backend API. Make sure it's running at http://localhost:8000.",
        ),
      )
      .finally(() => setLoading(false));
  }, [search, city]);

  const clearCity = () => setSearchParams({});

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <div className="mb-6 rounded-2xl bg-gradient-to-r from-zomato to-zomato-dark p-8 text-white">
        <h1 className="text-3xl font-extrabold">
          {city ? `Restaurants in ${city}` : "Order food from your favourite restaurants"}
        </h1>
        <p className="mt-2 text-white/90">Fast delivery. Great taste. Zero fuss.</p>
        <div className="mt-4 flex max-w-md items-center gap-3">
          <SearchBar value={search} onChange={setSearch} placeholder="Search restaurants..." />
        </div>
        {city && (
          <button
            onClick={clearCity}
            className="mt-3 rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white hover:bg-white/30"
          >
            × Clear "{city}" filter
          </button>
        )}
      </div>

      {error && <p className="mb-4 text-sm font-medium text-red-600">{error}</p>}
      {loading && <p className="text-sm text-gray-500">Loading restaurants...</p>}

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => (
          <RestaurantCard key={r.id} restaurant={r} />
        ))}
      </div>

      {!loading && !error && restaurants.length === 0 && (
        <p className="text-sm text-gray-500">
          {city
            ? `No restaurants listed in ${city} yet.`
            : "No restaurants found."}
        </p>
      )}
    </div>
  );
}
