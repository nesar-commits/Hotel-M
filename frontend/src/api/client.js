import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const TOKEN_STORAGE_KEY = "tastyhub_token";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getRestaurants = (params) => api.get("/restaurants", { params }).then((r) => r.data);

export const getRestaurantCount = (params) =>
  api.get("/restaurants/count", { params }).then((r) => r.data);

export const getNearbyRestaurants = (lat, lng) =>
  api.get("/restaurants/nearby", { params: { lat, lng } }).then((r) => r.data);

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

export const getMyOrders = () => api.get("/orders/me").then((r) => r.data);

export const getOrder = (orderId) => api.get(`/orders/${orderId}`).then((r) => r.data);

export const getKitchenOrders = () => api.get("/orders/kitchen").then((r) => r.data);

export const advanceOrder = (orderId) =>
  api.post(`/orders/${orderId}/advance`).then((r) => r.data);

export const signup = (name, email, password) =>
  api.post("/users/signup", { name, email, password }).then((r) => r.data);

export const login = (email, password) =>
  api.post("/users/login", { email, password }).then((r) => r.data);

export const getMe = () => api.get("/users/me").then((r) => r.data);

export { TOKEN_STORAGE_KEY };
