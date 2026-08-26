import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext.jsx";

export default function Navbar({ onCartClick }) {
  const { itemCount } = useCart();

  return (
    <header className="sticky top-0 z-30 bg-white shadow-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2">
          <span className="text-2xl font-extrabold tracking-tight text-zomato">TastyHub</span>
        </Link>
        <Link
          to="/cities"
          className="text-sm font-semibold text-gray-700 hover:text-zomato"
        >
          Cities
        </Link>
        <button
          onClick={onCartClick}
          className="relative flex items-center gap-2 rounded-full bg-zomato px-4 py-2 text-sm font-semibold text-white shadow hover:bg-zomato-dark"
        >
          Cart
          {itemCount > 0 && (
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-white text-xs font-bold text-zomato">
              {itemCount}
            </span>
          )}
        </button>
      </div>
    </header>
  );
}
