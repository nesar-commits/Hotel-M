import { useEffect, useState } from "react";
import { advanceOrder, getKitchenOrders } from "../api/client.js";
import { STATUS_LABELS } from "../constants/orderStatus.js";
import { useAuth } from "../context/AuthContext.jsx";

const POLL_INTERVAL_MS = 5000;

export default function Kitchen() {
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);
  const [advancing, setAdvancing] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const fetchOrders = () => {
      getKitchenOrders()
        .then((data) => {
          if (!cancelled) setOrders(data);
        })
        .catch(() => {
          if (!cancelled) setError("Could not load kitchen orders.");
        });
    };
    fetchOrders();
    const interval = setInterval(fetchOrders, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const handleAdvance = async (orderId) => {
    setAdvancing(orderId);
    try {
      const updated = await advanceOrder(orderId);
      setOrders((prev) => prev.map((o) => (o.id === orderId ? updated : o)));
    } catch {
      setError("Could not advance that order.");
    } finally {
      setAdvancing(null);
    }
  };

  if (!user?.is_staff) {
    return (
      <p className="p-6 text-sm font-medium text-red-600">
        This page is only available to kitchen staff.
      </p>
    );
  }

  const activeOrders = orders.filter((o) => o.status !== "delivered" && o.status !== "cancelled");

  return (
    <div className="mx-auto max-w-4xl px-4 py-6">
      <h1 className="mb-1 text-2xl font-extrabold text-gray-900">Kitchen Dashboard</h1>
      <p className="mb-6 text-sm text-gray-500">
        {activeOrders.length} active order{activeOrders.length !== 1 ? "s" : ""}
      </p>

      {error && <p className="mb-4 text-sm font-medium text-red-600">{error}</p>}

      {activeOrders.length === 0 && (
        <p className="text-sm text-gray-500">No active orders right now.</p>
      )}

      <div className="space-y-3">
        {activeOrders.map((order) => (
          <div key={order.id} className="rounded-xl bg-white p-4 shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-gray-900">
                  Order #{order.id} · {order.restaurant_name}
                </p>
                <p className="text-sm text-gray-500">
                  {order.items.map((i) => `${i.menu_item_name} ×${i.quantity}`).join(", ")}
                </p>
              </div>
              <span className="rounded-full bg-zomato-light px-3 py-1 text-xs font-bold text-zomato">
                {STATUS_LABELS[order.status] || order.status}
              </span>
            </div>
            <button
              onClick={() => handleAdvance(order.id)}
              disabled={advancing === order.id}
              className="mt-3 rounded-lg bg-zomato px-4 py-2 text-sm font-bold text-white hover:bg-zomato-dark disabled:opacity-60"
            >
              {advancing === order.id ? "Updating..." : "Advance to Next Stage →"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
