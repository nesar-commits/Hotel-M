import { Link } from "react-router-dom";

export default function RestaurantCard({ restaurant }) {
  return (
    <Link
      to={`/restaurant/${restaurant.id}`}
      className="group overflow-hidden rounded-2xl bg-white shadow transition hover:shadow-lg"
    >
      <div className="relative h-44 w-full overflow-hidden">
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
        />
        {!restaurant.is_open && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/60">
            <span className="text-sm font-semibold text-white">Currently Closed</span>
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-base font-bold text-gray-900">{restaurant.name}</h3>
          <span className="flex shrink-0 items-center gap-1 rounded bg-green-600 px-1.5 py-0.5 text-xs font-bold text-white">
            {restaurant.rating.toFixed(1)} ★
          </span>
        </div>
        <p className="mt-1 truncate text-sm text-gray-500">{restaurant.cuisine_type}</p>
        <p className="mt-1 text-sm text-gray-500">
          {restaurant.city} · ₹{restaurant.cost_for_two} for two
<<<<<<< HEAD
=======
          {restaurant.distance_km != null && ` · ${restaurant.distance_km} km away`}
>>>>>>> bed6d3f (second commit)
        </p>
      </div>
    </Link>
  );
}
