import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { placeOrder } from "../api/client.js";
import { useAuth } from "../context/AuthContext.jsx";
import { useCart } from "../context/CartContext.jsx";

export default function CartDrawer({ open, onClose }) {
  const { items, total, addItem, decrementItem, clearCart, restaurantId } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [placing, setPlacing] = useState(false);
  const [placed, setPlaced] = useState(null);
  const [error, setError] = useState(null);

  const handleCheckout = async () => {
    if (!restaurantId || items.length === 0) return;
    if (!user) {
      onClose();
      navigate("/login");
      return;
    }
    setError(null);
    setPlacing(true);
    try {
      const order = await placeOrder({
        restaurant_id: restaurantId,
        items: items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity })),
      });
      setPlaced(order);
      clearCart();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not place order. Is the backend running?");
    } finally {
      setPlacing(false);
    }
  };

  return (
    <>
      <div
        onClick={onClose}
        className={`fixed inset-0 z-40 bg-black/40 transition-opacity ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      />
      <aside
        className={`fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-white shadow-2xl transition-transform ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
          <h2 className="text-lg font-bold">Your Cart</h2>
          <button onClick={onClose} className="text-2xl leading-none text-gray-400">
            ×
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-4">
          {placed && (
            <div className="mb-4 rounded-lg bg-green-50 p-3 text-sm font-medium text-green-700">
              Order placed!{" "}
              <Link to={`/orders/${placed.id}`} onClick={onClose} className="underline">
                Track it here
              </Link>
              .
            </div>
          )}
          {error && (
            <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}
          {items.length === 0 ? (
            <p className="text-sm text-gray-500">Your cart is empty. Add some delicious food!</p>
          ) : (
            <ul className="space-y-4">
              {items.map((item) => (
                <li key={item.id} className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold text-gray-900">{item.name}</p>
                    <p className="text-xs text-gray-500">₹{item.price}</p>
                  </div>
                  <div className="flex items-center gap-3 rounded-lg bg-zomato-light px-3 py-1 text-sm font-bold text-zomato">
                    <button onClick={() => decrementItem(item.id)}>−</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => addItem(item, { id: restaurantId })}>+</button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {items.length > 0 && (
          <div className="border-t border-gray-100 px-5 py-4">
            <div className="mb-3 flex items-center justify-between text-sm font-semibold text-gray-700">
              <span>Total</span>
              <span>₹{total.toFixed(2)}</span>
            </div>
            <button
              onClick={handleCheckout}
              disabled={placing}
              className="w-full rounded-xl bg-zomato py-3 text-sm font-bold text-white shadow hover:bg-zomato-dark disabled:opacity-60"
            >
              {placing ? "Placing order..." : user ? "Place Order" : "Log In to Order"}
            </button>
          </div>
        )}
      </aside>
    </>
  );
}
