import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getOrder } from "../api/client.js";
import OrderStatusStepper from "../components/OrderStatusStepper.jsx";
import { useAuth } from "../context/AuthContext.jsx";

const POLL_INTERVAL_MS = 4000;

export default function OrderDetail() {
  const { id } = useParams();
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (authLoading) return;
    if (!user) {
      navigate("/login");
      return;
    }
    let cancelled = false;

    const fetchOrder = () => {
      getOrder(id)
        .then((data) => {
          if (!cancelled) setOrder(data);
        })
        .catch(() => {
          if (!cancelled) setError("Could not load this order.");
        });
    };

    fetchOrder();
    const interval = setInterval(fetchOrder, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [id, user, authLoading, navigate]);

  if (error) return <p className="p-6 text-sm font-medium text-red-600">{error}</p>;
  if (!order) return <p className="p-6 text-sm text-gray-500">Loading order...</p>;

  return (
    <div className="mx-auto max-w-2xl px-4 py-6">
      <h1 className="mb-1 text-2xl font-extrabold text-gray-900">Order #{order.id}</h1>
      <p className="mb-6 text-sm text-gray-500">{order.restaurant_name}</p>

      <div className="mb-6 rounded-2xl bg-white p-6 shadow">
        <OrderStatusStepper status={order.status} />
      </div>

      <div className="rounded-2xl bg-white p-6 shadow">
        <h2 className="mb-3 font-bold text-gray-900">Items</h2>
        <ul className="divide-y divide-gray-100">
          {order.items.map((item) => (
            <li key={item.id} className="flex justify-between py-2 text-sm">
              <span className="text-gray-700">
                {item.menu_item_name} × {item.quantity}
              </span>
              <span className="font-medium text-gray-900">
                ₹{(item.price * item.quantity).toFixed(2)}
              </span>
            </li>
          ))}
        </ul>
        <div className="mt-3 flex justify-between border-t border-gray-100 pt-3 text-sm font-bold text-gray-900">
          <span>Total</span>
          <span>₹{order.total_amount.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
