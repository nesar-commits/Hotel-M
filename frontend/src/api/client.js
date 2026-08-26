import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getRestaurants = (params) => api.get("/restaurants", { params }).then((r) => r.data);

<<<<<<< HEAD
=======
export const getNearbyRestaurants = (lat, lng) =>
  api.get("/restaurants/nearby", { params: { lat, lng } }).then((r) => r.data);

>>>>>>> bed6d3f (second commit)
export const getRestaurant = (id) => api.get(`/restaurants/${id}`).then((r) => r.data);

export const getMenuItems = (restaurantId, params) =>
  api.get(`/restaurants/${restaurantId}/menu`, { params }).then((r) => r.data);

export const getPopularItems = (restaurantId) =>
  api.get(`/recommendations/popular/${restaurantId}`).then((r) => r.data);

export const getRecommendationsForUser = (userId) =>
  api.get(`/recommendations/user/${userId}`).then((r) => r.data);

export const getSimilarItems = (menuItemId) =>
  api.get(`/recommendations/similar/${menuItemId}`).then((r) => r.data);

export const placeOrder = (order) => api.post("/orders", order).then((r) => r.data);

export const getStates = () => api.get("/locations/states").then((r) => r.data);

export const getStateCities = (slug) =>
  api.get(`/locations/states/${slug}/cities`).then((r) => r.data);
