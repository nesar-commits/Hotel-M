# TastyHub — Android (Kotlin + Jetpack Compose)

Native Android client for the TastyHub API (`../backend`), consuming the same
FastAPI backend as the web frontend. Covers the core customer flow: browse
and search restaurants, view a restaurant's menu, build a cart, sign
up / log in, place an order, and track it live. Staff/kitchen screens are
not included — the web app's `/kitchen` page is the tool for that today.

> This was scaffolded on a machine with no Android SDK installed, so none of
> it has been built, run, or verified in an emulator yet. Open it in Android
> Studio to build/verify (see below).

## Structure

```
app/src/main/java/com/tastyhub/android/
  data/model/        Kotlin data classes mirroring backend/app/schemas.py
  data/remote/        Retrofit API interface + auth interceptor
  data/TokenManager   SharedPreferences-backed JWT storage
  di/AppContainer      Manual DI: builds Retrofit/OkHttp/TokenManager once
  auth/                AuthViewModel — signup/login/logout, session check on launch
  cart/                CartViewModel — in-memory cart, app-scoped (mirrors CartContext.jsx)
  ui/screens/          One package per screen (home, restaurant, cart, auth, orders, account)
  ui/navigation/       NavHost + bottom nav wiring all screens together
  ui/theme/            Material3 theme (dynamic color on Android 12+, TastyHub red fallback)
```

Architecture: Compose UI → per-screen `ViewModel` (StateFlow-based) → Retrofit
`TastyHubApi` directly (no repository layer — this is a small enough surface
that the extra indirection wasn't worth it). `AuthViewModel`, `CartViewModel`
and `OrderViewModel` are hoisted once in `TastyHubNavHost` so they survive
navigation between screens; per-screen ViewModels (Home, RestaurantMenu) are
scoped to their `composable {}` entry as usual.

## Running it

Requires Android Studio (Ladybird/Koala or newer) with an Android SDK
installed — this environment doesn't have one, so the Gradle wrapper jar
isn't checked in. Opening the project in Android Studio will offer to
generate it; alternatively, if you have a local Gradle install:

```bash
cd android
gradle wrapper --gradle-version 8.9
```

Then, with the backend running (`cd ../backend && uvicorn app.main:app --reload`):

1. Open `android/` as a project in Android Studio.
2. Run on an emulator — it talks to `http://10.0.2.2:8000/`, which is the
   emulator's alias for your host machine's `localhost`, so no config change
   needed if the backend is running locally.
3. Running on a **physical device** instead: change `API_BASE_URL` in
   `app/build.gradle.kts` to your machine's LAN IP (e.g.
   `http://192.168.1.20:8000/`) — the device and backend need to be on the
   same network, and the backend needs to bind to `0.0.0.0`, not just
   `127.0.0.1` (`uvicorn app.main:app --host 0.0.0.0 --reload`).

## Known gaps / next steps

- No automated tests yet (the web frontend doesn't have any either, so
  nothing to port).
- `getRestaurants` search is client-triggered with a 350ms debounce but
  doesn't yet support the web app's city filter or the `/restaurants/nearby`
  geolocation endpoint.
- The app icon (`res/drawable/ic_launcher.xml`) is a placeholder vector,
  not real launcher art.
- Staff/kitchen queue screens (`GET /orders/kitchen`, advance-order) aren't
  built — add an `ui/screens/kitchen` package following the same pattern if
  needed.
- Cart is in-memory only (matches the web app's `CartContext`, which also
  doesn't persist across a refresh) — it's lost if the app process dies.
