import { useCart } from "../context/CartContext.jsx";

function VegDot({ isVeg }) {
  return (
    <span
      className={`inline-flex h-4 w-4 items-center justify-center border ${
        isVeg ? "border-green-600" : "border-red-600"
      }`}
    >
      <span className={`h-2 w-2 rounded-full ${isVeg ? "bg-green-600" : "bg-red-600"}`} />
    </span>
  );
}

export default function MenuItemCard({ item, restaurant }) {
  const { items, addItem, decrementItem } = useCart();
  const cartItem = items.find((i) => i.id === item.id);
  const quantity = cartItem?.quantity || 0;

  return (
    <div className="flex gap-4 border-b border-gray-100 py-5 last:border-0">
      <div className="flex-1">
        <div className="mb-1 flex items-center gap-2">
          <VegDot isVeg={item.is_veg} />
          {item.rating > 0 && (
            <span className="text-xs font-semibold text-green-700">{item.rating.toFixed(1)} ★</span>
          )}
        </div>
        <h4 className="font-semibold text-gray-900">{item.name}</h4>
        <p className="mt-1 text-sm font-medium text-gray-700">₹{item.price}</p>
        <p className="mt-1 line-clamp-2 text-sm text-gray-500">{item.description}</p>
      </div>

      <div className="relative flex w-32 shrink-0 flex-col items-center">
        {item.image_url && (
          <img
            src={item.image_url}
            alt={item.name}
            className="h-24 w-32 rounded-xl object-cover shadow"
          />
        )}
        {quantity === 0 ? (
          <button
            onClick={() => addItem(item, restaurant)}
            className="absolute -bottom-3 rounded-lg border border-gray-200 bg-white px-6 py-1.5 text-sm font-bold text-zomato shadow hover:bg-zomato-light"
          >
            ADD
          </button>
        ) : (
          <div className="absolute -bottom-3 flex items-center gap-3 rounded-lg bg-zomato px-3 py-1.5 text-sm font-bold text-white shadow">
            <button onClick={() => decrementItem(item.id)}>−</button>
            <span>{quantity}</span>
            <button onClick={() => addItem(item, restaurant)}>+</button>
          </div>
        )}
      </div>
    </div>
  );
}
