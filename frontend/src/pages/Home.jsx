import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getNearbyRestaurants, getRestaurantCount, getRestaurants } from "../api/client.js";
import RestaurantCard from "../components/RestaurantCard.jsx";
import SearchBar from "../components/SearchBar.jsx";
import { useUserLocation } from "../context/UserLocationContext.jsx";

const PAGE_SIZE = 30;

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  const city = searchParams.get("city") || "";
  const { location } = useUserLocation();
  const [restaurants, setRestaurants] = useState([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(null);
  const [forceBrowse, setForceBrowse] = useState(false);

  const nearbyMode = !!location && !search && !city && !forceBrowse;

  useEffect(() => {
    setError(null);
    setLoading(true);

    if (nearbyMode) {
      getNearbyRestaurants(location.lat, location.lng)
        .then((data) => {
          setRestaurants(data);
          setTotal(data.length);
        })
        .catch(() => setError("Could not fetch nearby restaurants."))
        .finally(() => setLoading(false));
      return;
    }

    const params = { limit: PAGE_SIZE, offset: 0 };
    if (search) params.search = search;
    if (city) params.city = city;
    Promise.all([getRestaurants(params), getRestaurantCount(params)])
      .then(([list, countRes]) => {
        setRestaurants(list);
        setTotal(countRes.total);
      })
      .catch(() =>
        setError(
          "Could not reach the backend API. Make sure it's running at http://localhost:8000.",
        ),
      )
      .finally(() => setLoading(false));
  }, [search, city, nearbyMode, location?.lat, location?.lng]);

  const loadMore = () => {
    setLoadingMore(true);
    const params = { limit: PAGE_SIZE, offset: restaurants.length };
    if (search) params.search = search;
    if (city) params.city = city;
    getRestaurants(params)
      .then((more) => setRestaurants((prev) => [...prev, ...more]))
      .catch(() => setError("Could not load more restaurants."))
      .finally(() => setLoadingMore(false));
  };

  const clearCity = () => setSearchParams({});

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <div className="mb-6 rounded-2xl bg-gradient-to-r from-zomato to-zomato-dark p-8 text-white">
        <h1 className="text-3xl font-extrabold">
          {nearbyMode
            ? `Restaurants near ${location.label}`
            : city
              ? `Restaurants in ${city}`
              : "Order food from your favourite restaurants"}
        </h1>
        <p className="mt-2 text-white/90">Fast delivery. Great taste. Zero fuss.</p>

        <div className="mt-4 flex max-w-md items-center gap-3">
          <SearchBar value={search} onChange={setSearch} placeholder="Search restaurants..." />
        </div>

        <div className="mt-3 flex flex-wrap items-center gap-3">
          {nearbyMode && (
            <button
              onClick={() => setForceBrowse(true)}
              className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white hover:bg-white/30"
            >
              Browse all restaurants instead
            </button>
          )}
          {!nearbyMode && location && (forceBrowse || city) && (
            <button
              onClick={() => {
                setForceBrowse(false);
                clearCity();
              }}
              className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white hover:bg-white/30"
            >
              × Back to "{location.label}"
            </button>
          )}
          {city && !nearbyMode && !location && (
            <button
              onClick={clearCity}
              className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white hover:bg-white/30"
            >
              × Clear "{city}" filter
            </button>
          )}
        </div>
      </div>

      {error && <p className="mb-4 text-sm font-medium text-red-600">{error}</p>}
      {loading && <p className="text-sm text-gray-500">Loading restaurants...</p>}
      {!loading && !nearbyMode && total > 0 && (
        <p className="mb-3 text-sm text-gray-500">
          Showing {restaurants.length} of {total} restaurants
        </p>
      )}

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => (
          <RestaurantCard key={r.id} restaurant={r} />
        ))}
      </div>

      {!loading && !nearbyMode && restaurants.length < total && (
        <div className="mt-6 flex justify-center">
          <button
            onClick={loadMore}
            disabled={loadingMore}
            className="rounded-full bg-white px-6 py-2 text-sm font-bold text-zomato shadow hover:bg-zomato-light disabled:opacity-60"
          >
            {loadingMore ? "Loading..." : "Load more"}
          </button>
        </div>
      )}

      {!loading && !error && restaurants.length === 0 && (
        <p className="text-sm text-gray-500">
          {nearbyMode
            ? "No restaurants found near you."
            : city
              ? `No restaurants listed in ${city} yet.`
              : "No restaurants found."}
        </p>
      )}
    </div>
  );
}
