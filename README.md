# TastyHub — Hotel/Restaurant Menu App (Zomato-inspired)

A food ordering platform: browse restaurants, filter and search a menu by category,
add items to a cart, place an order, and get content-based recommendations
("Popular Dishes", "Recommended for you") powered by a lightweight ML engine.

## Structure

```
backend/    FastAPI + PostgreSQL + scikit-learn recommendation engine
frontend/   React + Vite + Tailwind (Zomato-style UI)
```

Native **Android (Kotlin)** and **iOS (Swift)** apps, plus a deeper AI/ML/DL
layer, are planned as later phases once this web + backend core is solid —
they aren't built yet.

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
- `GET /restaurants` — list/search restaurants
- `GET /restaurants/{id}` — restaurant detail with categories + menu items
- `GET /restaurants/{id}/menu` — filter menu by category/veg/search
- `POST /orders` — place an order
- `GET /recommendations/popular/{restaurant_id}` — top-rated dishes
- `GET /recommendations/similar/{menu_item_id}` — "you might also like"
- `GET /recommendations/user/{user_id}` — personalized picks from order history

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

## Roadmap

- [ ] Auth with JWT sessions (signup/login endpoints already exist)
- [ ] Order status tracking / kitchen dashboard
- [ ] Android app (Kotlin, Jetpack Compose) consuming the same API
- [ ] iOS app (Swift, SwiftUI) consuming the same API
- [ ] Deeper ML: collaborative filtering, image-based dish tagging
# Hotel-M
