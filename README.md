# TastyHub — Hotel/Restaurant Menu App (Zomato-inspired)

A food ordering platform: browse restaurants (5,000+ seeded, across every
Indian state), filter and search by city or location, add items to a cart,
sign up / log in, place an order, and track it live through a kitchen
pipeline — plus content-based recommendations ("Popular Dishes",
"Recommended for you") powered by a lightweight ML engine.

## Structure

```
backend/    FastAPI + PostgreSQL + JWT auth + scikit-learn recommendation engine
frontend/   React + Vite + Tailwind (Zomato-style UI)
```

Native **Android (Kotlin)** and **iOS (Swift)** apps, plus a deeper AI/ML/DL
layer, are still future phases — this machine has no Android SDK and no full
Xcode/simulator, so that work isn't buildable or testable here.

## Backend setup

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# create a Postgres database, then:
cp .env.example .env   # edit DATABASE_URL if needed
python -m app.seed     # loads sample restaurants + menu items
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

Key endpoints:
- `GET /restaurants` — paginated list/search (`limit`, `offset`, `city`, `search`)
- `GET /restaurants/count` — total for the current filter, used to drive "Load more"
- `GET /restaurants/nearby?lat=&lng=` — sorted by real distance from a point
- `GET /restaurants/{id}` — restaurant detail with categories + menu items
- `GET /restaurants/{id}/menu` — filter menu by category/veg/search
- `POST /users/signup`, `POST /users/login` — return a JWT + user
- `GET /users/me` — current user from the bearer token
- `POST /orders` — place an order (requires auth; user is taken from the token)
- `GET /orders/me` — the logged-in user's orders
- `GET /orders/{id}` — one order (owner or staff only)
- `GET /orders/kitchen`, `POST /orders/{id}/advance` — staff-only kitchen queue and status pipeline
- `GET /recommendations/popular/{restaurant_id}` — top-rated dishes
- `GET /recommendations/similar/{menu_item_id}` — "you might also like"
- `GET /recommendations/user/{user_id}` — personalized picks from order history
- `GET /locations/states`, `GET /locations/states/{slug}/cities` — India states/UTs → cities

## Running the tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

Tests run against an isolated SQLite file (`test_tastyhub.db`, auto-created
and reset per test) via `DATABASE_URL` override in `tests/conftest.py` — they
never touch your local Postgres dev data.

## Frontend setup

```bash
cd frontend
npm install
cp .env.example .env   # points at the backend URL
npm run dev
```

App: http://localhost:5173

## Recommendation engine

`backend/app/ml/recommender.py` builds TF-IDF vectors from each dish's name,
description, tags, category and veg/non-veg status, then uses cosine
similarity for:
- **Item-to-item**: dishes similar to one you're viewing
- **Personalized**: a taste profile built from a user's past orders, ranked
  against the full catalog
- **Popularity fallback** for new users with no order history (cold start)

## Auth & order tracking

- **JWT auth**: signup/login return a bearer token (`backend/app/auth.py`); the
  frontend stores it in `localStorage` and attaches it via an axios
  interceptor (`frontend/src/api/client.js`). Checkout, `/orders`, and
  `/orders/:id` all require login and redirect to `/login` otherwise.
- **Order status pipeline**: `placed → confirmed → preparing → ready →
  out_for_delivery → delivered` (`backend/app/order_status.py`). Customers see
  a live-updating stepper on `/orders/:id` (polls every 4s); kitchen staff
  work the queue at `/kitchen` (polls every 5s) with an "Advance to Next
  Stage" button per order.
- **Staff role**: `User.is_staff` gates `/orders/kitchen` and the
  advance/status-update endpoints (403 for regular users). The seeded
  `staff@tastyhub.dev` / `staff1234` account is staff; `demo@tastyhub.dev` /
  `demo1234` is a regular customer.
- **Ownership checks**: `GET /orders/{id}` 403s for anyone who isn't the
  order's owner or staff.

## Roadmap

- [ ] Android app (Kotlin, Jetpack Compose) consuming the same API
- [ ] iOS app (Swift, SwiftUI) consuming the same API
- [ ] Deeper ML: collaborative filtering, image-based dish tagging
- [ ] Payment integration (currently orders are placed with no payment step)
