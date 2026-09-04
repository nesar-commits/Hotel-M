# TastyHub — iOS (Swift + SwiftUI)

Native iOS client for the TastyHub API (`../backend`), consuming the same FastAPI
backend as the web frontend and the Android app. Covers the core customer flow:
browse/search restaurants, view a restaurant's menu, build a cart, sign up / log
in, place an order, and track it live. Staff/kitchen screens are not included —
same as Android, the web app's `/kitchen` page is the tool for that today.

> This was scaffolded on a machine with only the Xcode Command Line Tools
> installed (no full Xcode, no iOS SDK), so none of it has been built, run, or
> verified in a simulator yet. Every file was type-checked with `swiftc
> -typecheck` against the macOS SDK as a sanity check (catches real syntax/type
> errors), but that can't catch iOS-SDK-specific issues — open it in Xcode to
> build/verify.

## Structure

```
TastyHub/
  Config.swift              API base URL
  Models/Models.swift        Codable structs mirroring backend/app/schemas.py
  Networking/APIClient.swift  URLSession + async/await, snake_case <-> camelCase via
                               JSONDecoder/Encoder's convertFromSnakeCase/convertToSnakeCase
  Networking/TokenStore.swift Keychain-backed JWT storage
  State/AuthStore.swift       Session state — login/signup/logout, restores session on launch
  State/CartStore.swift       In-memory cart, app-scoped (mirrors CartContext.jsx)
  State/OrderStore.swift      Place order, order history, live order polling
  Theme/Theme.swift           TastyHub red, matches the Android/web palette
  Navigation/RootTabView.swift TabView (Home/Orders/Cart/Account) wiring everything together
  Screens/                    One folder per screen, each with a View + (where needed) a ViewModel
```

Architecture: SwiftUI `View` → per-screen `ObservableObject` view model (`@Published`
state, `async`/`await` calls) → `APIClient` directly (no repository layer — same
reasoning as the Android app: the API surface is small enough that the extra
indirection isn't worth it). `AuthStore`, `CartStore` and `OrderStore` are created
once in `TastyHubApp` and injected via `.environmentObject`, so they survive
navigation between tabs; per-screen view models (`HomeViewModel`,
`RestaurantMenuViewModel`) are owned by their screen via `@StateObject`.

One deliberate difference from Android: login/signup are a single modal sheet
(`AuthSheetView`, toggled between the two modes) rather than two pushed screens —
a sheet is the more idiomatic iOS pattern for an auth gate reached from several
different tabs (Cart checkout, Orders tab, Account tab).

## Running it

Requires **Xcode** (not just the Command Line Tools) with an iOS SDK — this
environment only has the Command Line Tools, so nothing here has been build- or
run-verified. To get it running:

1. In Xcode: **File → New → Project → iOS → App**. Name it `TastyHub`,
   interface **SwiftUI**, language **Swift**.
2. Delete the auto-generated `ContentView.swift` and the auto-generated
   `TastyHubApp.swift` (ours already declares `@main` — keeping both causes a
   duplicate-entry-point build error).
3. Drag the `ios/TastyHub` folder into the project navigator ("Copy items if
   needed" checked, added to the `TastyHub` target).
4. Build & run on a **simulator**. The Simulator shares the host Mac's network
   stack, so `http://127.0.0.1:8000` (already set in `Config.swift`) reaches a
   backend running locally with **no config change needed** — run
   `cd ../backend && uvicorn app.main:app --reload` first.
5. Running on a **physical device** instead: change `AppConfig.apiBaseURL` in
   `Config.swift` to your machine's LAN IP (e.g. `http://192.168.1.20:8000`) and
   run the backend with `--host 0.0.0.0`. This is no longer loopback traffic, so
   iOS's App Transport Security will block plain HTTP by default — add an ATS
   exception for that IP in the target's Info tab (`NSAppTransportSecurity` →
   `NSExceptionDomains`), or switch the target to HTTPS.

## Known gaps / next steps

- No automated tests yet (same as Android and the web frontend).
- Search is debounced client-side (350ms) but doesn't support the web app's
  city filter or the `/restaurants/nearby` geolocation endpoint — matches
  Android's current scope, not a regression.
- Recommendation endpoints (`/recommendations/*`) aren't wired into any screen
  — the Android app doesn't call them either; the ML-powered "Popular Dishes" /
  "Recommended for you" sections are web-only for now.
- No app icon / launch screen art — uses Xcode's default placeholder.
- Staff/kitchen queue screens (`GET /orders/kitchen`, advance-order) aren't
  built — add a `Screens/Kitchen` folder following the same pattern if needed.
- Cart is in-memory only (matches Android and the web app's `CartContext`) —
  lost if the app is force-quit.
