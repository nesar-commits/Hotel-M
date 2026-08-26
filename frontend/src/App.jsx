import { useState } from "react";
import { Route, Routes } from "react-router-dom";
import CartDrawer from "./components/CartDrawer.jsx";
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import RestaurantMenu from "./pages/RestaurantMenu.jsx";
import StateCities from "./pages/StateCities.jsx";
import States from "./pages/States.jsx";

export default function App() {
  const [cartOpen, setCartOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#f5f5f5]">
      <Navbar onCartClick={() => setCartOpen(true)} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/restaurant/:id" element={<RestaurantMenu />} />
        <Route path="/cities" element={<States />} />
        <Route path="/cities/:slug" element={<StateCities />} />
      </Routes>
      <CartDrawer open={cartOpen} onClose={() => setCartOpen(false)} />
    </div>
  );
}
