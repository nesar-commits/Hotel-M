import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext.jsx";
import Logo from "./Logo.jsx";

export default function Navbar({ onCartClick }) {
  const { itemCount } = useCart();

  return (
    <header className="sticky top-0 z-30 bg-white shadow-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/">
          <Logo />
        </Link>
        <div className="flex items-center gap-3">
          <Link
            to="/cities"
            className="rounded-full bg-zomato px-4 py-2 text-sm font-semibold text-white shadow hover:bg-zomato-dark"
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
      </div>
    </header>
  );
}
