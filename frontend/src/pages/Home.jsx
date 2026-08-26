import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
<<<<<<< HEAD
import { getRestaurants } from "../api/client.js";
=======
import { getNearbyRestaurants, getRestaurants } from "../api/client.js";
>>>>>>> bed6d3f (second commit)
import RestaurantCard from "../components/RestaurantCard.jsx";
import SearchBar from "../components/SearchBar.jsx";

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams();
  const city = searchParams.get("city") || "";
  const [restaurants, setRestaurants] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
<<<<<<< HEAD

  useEffect(() => {
=======
  const [nearbyMode, setNearbyMode] = useState(false);
  const [locating, setLocating] = useState(false);
  const [locationError, setLocationError] = useState(null);

  useEffect(() => {
    if (nearbyMode) return;
>>>>>>> bed6d3f (second commit)
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
<<<<<<< HEAD
  }, [search, city]);

  const clearCity = () => setSearchParams({});

=======
  }, [search, city, nearbyMode]);

  const clearCity = () => setSearchParams({});

  const useMyLocation = () => {
    setLocationError(null);

    if (!navigator.geolocation) {
      setLocationError("Your browser doesn't support location detection.");
      return;
    }

    setLocating(true);
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        getNearbyRestaurants(coords.latitude, coords.longitude)
          .then((data) => {
            setRestaurants(data);
            setNearbyMode(true);
            setSearchParams({});
          })
          .catch(() => setLocationError("Could not fetch nearby restaurants."))
          .finally(() => setLocating(false));
      },
      (err) => {
        setLocating(false);
        if (err.code === err.PERMISSION_DENIED) {
          setLocationError("Location access was denied. Enable it in your browser to use this.");
        } else {
          setLocationError("Could not determine your location. Please try again.");
        }
      },
      { enableHighAccuracy: true, timeout: 10000 },
    );
  };

  const exitNearbyMode = () => {
    setNearbyMode(false);
    setLocationError(null);
  };

>>>>>>> bed6d3f (second commit)
  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <div className="mb-6 rounded-2xl bg-gradient-to-r from-zomato to-zomato-dark p-8 text-white">
        <h1 className="text-3xl font-extrabold">
<<<<<<< HEAD
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
=======
          {nearbyMode
            ? "Restaurants near you"
            : city
              ? `Restaurants in ${city}`
              : "Order food from your favourite restaurants"}
        </h1>
        <p className="mt-2 text-white/90">Fast delivery. Great taste. Zero fuss.</p>

        {!nearbyMode && (
          <div className="mt-4 flex max-w-md items-center gap-3">
            <SearchBar value={search} onChange={setSearch} placeholder="Search restaurants..." />
          </div>
        )}

        <div className="mt-3 flex flex-wrap items-center gap-3">
          {!nearbyMode && (
            <button
              onClick={useMyLocation}
              disabled={locating}
              className="rounded-full bg-white px-4 py-1.5 text-xs font-bold text-zomato shadow hover:bg-zomato-light disabled:opacity-60"
            >
              {locating ? "Locating..." : "📍 Use my location"}
            </button>
          )}
          {nearbyMode && (
            <button
              onClick={exitNearbyMode}
              className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white hover:bg-white/30"
            >
              × Back to browsing
            </button>
          )}
          {city && !nearbyMode && (
            <button
              onClick={clearCity}
              className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white hover:bg-white/30"
            >
              × Clear "{city}" filter
            </button>
          )}
        </div>

        {locationError && <p className="mt-3 text-sm font-medium text-yellow-100">{locationError}</p>}
      </div>

      {error && <p className="mb-4 text-sm font-medium text-red-600">{error}</p>}
      {loading && !nearbyMode && <p className="text-sm text-gray-500">Loading restaurants...</p>}
>>>>>>> bed6d3f (second commit)

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => (
          <RestaurantCard key={r.id} restaurant={r} />
        ))}
      </div>

      {!loading && !error && restaurants.length === 0 && (
        <p className="text-sm text-gray-500">
<<<<<<< HEAD
          {city
            ? `No restaurants listed in ${city} yet.`
            : "No restaurants found."}
=======
          {nearbyMode
            ? "No restaurants found near you."
            : city
              ? `No restaurants listed in ${city} yet.`
              : "No restaurants found."}
>>>>>>> bed6d3f (second commit)
        </p>
      )}
    </div>
  );
}
