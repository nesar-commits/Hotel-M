import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getMyOrders } from "../api/client.js";
import { STATUS_LABELS } from "../constants/orderStatus.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Orders() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (authLoading) return;
    if (!user) {
      navigate("/login");
      return;
    }
    getMyOrders()
      .then(setOrders)
      .catch(() => setError("Could not load your orders."))
      .finally(() => setLoading(false));
  }, [user, authLoading, navigate]);

  return (
    <div className="mx-auto max-w-3xl px-4 py-6">
      <h1 className="mb-4 text-2xl font-extrabold text-gray-900">Your Orders</h1>

      {loading && <p className="text-sm text-gray-500">Loading orders...</p>}
      {error && <p className="text-sm font-medium text-red-600">{error}</p>}
      {!loading && !error && orders.length === 0 && (
        <p className="text-sm text-gray-500">You haven't placed any orders yet.</p>
      )}

      <div className="space-y-3">
        {orders.map((order) => (
          <Link
            key={order.id}
            to={`/orders/${order.id}`}
            className="flex items-center justify-between rounded-xl bg-white p-4 shadow hover:shadow-md"
          >
            <div>
              <p className="font-semibold text-gray-900">{order.restaurant_name}</p>
              <p className="text-sm text-gray-500">
                {order.items.length} item{order.items.length !== 1 ? "s" : ""} · ₹
                {order.total_amount.toFixed(2)}
              </p>
              <p className="text-xs text-gray-400">
                {new Date(order.created_at).toLocaleString()}
              </p>
            </div>
            <span
              className={`rounded-full px-3 py-1 text-xs font-bold ${
                order.status === "delivered"
                  ? "bg-green-100 text-green-700"
                  : order.status === "cancelled"
                    ? "bg-red-100 text-red-700"
                    : "bg-zomato-light text-zomato"
              }`}
            >
              {STATUS_LABELS[order.status] || order.status}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
