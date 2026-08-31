import { createContext, useContext, useEffect, useState } from "react";

const STORAGE_KEY = "tastyhub_location";
const GEOCODE_BASE = "https://nominatim.openstreetmap.org";

const UserLocationContext = createContext(null);

async function reverseGeocode(lat, lng) {
  try {
    const res = await fetch(`${GEOCODE_BASE}/reverse?lat=${lat}&lon=${lng}&format=json`);
    const data = await res.json();
    const addr = data.address || {};
    const area =
      addr.suburb || addr.neighbourhood || addr.city_district || addr.town || addr.village;
    const city = addr.city || addr.county || "";
    if (area && city && area !== city) return `${area}, ${city}`;
    return area || city || data.display_name?.split(",")[0] || "Current location";
  } catch {
    return "Current location";
  }
}

export function UserLocationProvider({ children }) {
  const [location, setLocationState] = useState(null); // { label, lat, lng }
  const [status, setStatus] = useState("idle"); // idle | locating | denied | error

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setLocationState(JSON.parse(saved));
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
  }, []);

  const persist = (loc) => {
    setLocationState(loc);
    if (loc) localStorage.setItem(STORAGE_KEY, JSON.stringify(loc));
    else localStorage.removeItem(STORAGE_KEY);
  };

  const detectLocation = ({ silent = false } = {}) => {
    if (!silent) setStatus("locating");
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        if (!silent) setStatus("error");
        reject(new Error("unsupported"));
        return;
      }
      navigator.geolocation.getCurrentPosition(
        async ({ coords }) => {
          const label = await reverseGeocode(coords.latitude, coords.longitude);
          const loc = { label, lat: coords.latitude, lng: coords.longitude };
          persist(loc);
          setStatus("idle");
          resolve(loc);
        },
        (err) => {
          if (!silent) setStatus(err.code === err.PERMISSION_DENIED ? "denied" : "error");
          reject(err);
        },
        { enableHighAccuracy: true, timeout: 10000 },
      );
    });
  };

  // Try once, quietly, on first-ever visit — mirrors how Uber/Zomato ask for
  // location as soon as you land, but never surfaces an error banner for
  // this automatic attempt (only an explicit click shows denied/error state).
  useEffect(() => {
    const alreadyDecided = localStorage.getItem(STORAGE_KEY) || sessionStorage.getItem("tastyhub_location_prompted");
    if (alreadyDecided) return;
    sessionStorage.setItem("tastyhub_location_prompted", "1");
    detectLocation({ silent: true }).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const searchLocations = async (query) => {
    if (!query || query.trim().length < 3) return [];
    const res = await fetch(
      `${GEOCODE_BASE}/search?q=${encodeURIComponent(query)}&format=json&limit=6&countrycodes=in`,
    );
    const data = await res.json();
    return data.map((d) => ({
      label: d.display_name.split(",").slice(0, 3).join(","),
      lat: parseFloat(d.lat),
      lng: parseFloat(d.lon),
    }));
  };

  const setManualLocation = (loc) => {
    persist(loc);
    setStatus("idle");
  };

  const clearLocation = () => {
    persist(null);
    setStatus("idle");
  };

  return (
    <UserLocationContext.Provider
      value={{ location, status, detectLocation, searchLocations, setManualLocation, clearLocation }}
    >
      {children}
    </UserLocationContext.Provider>
  );
}

export function useUserLocation() {
  const ctx = useContext(UserLocationContext);
  if (!ctx) throw new Error("useUserLocation must be used within UserLocationProvider");
  return ctx;
}
