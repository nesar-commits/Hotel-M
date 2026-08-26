import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { getPopularItems, getRestaurant } from "../api/client.js";
import CategoryTabs from "../components/CategoryTabs.jsx";
import MenuItemCard from "../components/MenuItemCard.jsx";
import SearchBar from "../components/SearchBar.jsx";

export default function RestaurantMenu() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [popular, setPopular] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [vegOnly, setVegOnly] = useState(false);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([getRestaurant(id), getPopularItems(id).catch(() => [])])
      .then(([r, pop]) => {
        setRestaurant(r);
        setPopular(pop);
      })
      .catch(() => setError("Could not load this restaurant. Is the backend running?"))
      .finally(() => setLoading(false));
  }, [id]);

  const filteredItems = useMemo(() => {
    if (!restaurant) return [];
    return restaurant.menu_items.filter((item) => {
      if (activeCategory && item.category_id !== activeCategory) return false;
      if (vegOnly && !item.is_veg) return false;
      if (search && !item.name.toLowerCase().includes(search.toLowerCase())) return false;
      return true;
    });
  }, [restaurant, activeCategory, vegOnly, search]);

  if (loading) return <p className="p-6 text-sm text-gray-500">Loading menu...</p>;
  if (error) return <p className="p-6 text-sm font-medium text-red-600">{error}</p>;
  if (!restaurant) return null;

  const sortedCategories = [...restaurant.categories].sort((a, b) => a.sort_order - b.sort_order);

  return (
    <div>
      <div className="relative h-56 w-full overflow-hidden">
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
        <div className="absolute bottom-4 left-4 text-white">
          <h1 className="text-2xl font-extrabold">{restaurant.name}</h1>
          <p className="text-sm text-white/90">{restaurant.cuisine_type}</p>
          <p className="text-sm text-white/80">
            {restaurant.city} · ₹{restaurant.cost_for_two} for two ·{" "}
            <span className="font-bold text-green-400">{restaurant.rating.toFixed(1)} ★</span>
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-3xl px-4 pb-4 pt-4">
        <SearchBar value={search} onChange={setSearch} placeholder="Search dishes..." />
        <label className="mt-3 flex w-fit items-center gap-2 text-sm font-medium text-gray-700">
          <input
            type="checkbox"
            checked={vegOnly}
            onChange={(e) => setVegOnly(e.target.checked)}
            className="h-4 w-4 accent-green-600"
          />
          Veg only
        </label>
      </div>

      {popular.length > 0 && !search && !activeCategory && (
        <div className="mx-auto max-w-3xl px-4 pb-2">
          <h2 className="mb-2 text-lg font-bold text-gray-900">Popular Dishes</h2>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {popular.slice(0, 6).map((item) => (
              <div key={item.id} className="w-40 shrink-0 rounded-xl bg-white p-3 shadow">
                {item.image_url && (
                  <img
                    src={item.image_url}
                    alt={item.name}
                    className="mb-2 h-20 w-full rounded-lg object-cover"
                  />
                )}
                <p className="truncate text-sm font-semibold text-gray-900">{item.name}</p>
                <p className="text-xs text-gray-500">₹{item.price}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <CategoryTabs
        categories={sortedCategories}
        activeId={activeCategory}
        onSelect={setActiveCategory}
      />

      <div className="mx-auto max-w-3xl px-4 pb-10">
        {filteredItems.length === 0 ? (
          <p className="py-6 text-sm text-gray-500">No dishes match your filters.</p>
        ) : (
          filteredItems.map((item) => (
            <MenuItemCard key={item.id} item={item} restaurant={restaurant} />
          ))
        )}
      </div>
    </div>
  );
}
