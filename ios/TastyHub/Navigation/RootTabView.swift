import SwiftUI

enum AppTab: Hashable {
    case home, orders, cart, account
}

struct RootTabView: View {
    @EnvironmentObject private var cartStore: CartStore
    @State private var selectedTab: AppTab = .home
    @State private var showingAuthSheet = false
    @State private var cartPath = NavigationPath()

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack {
                HomeView()
                    .navigationDestination(for: RestaurantOut.self) { restaurant in
                        RestaurantMenuView(
                            restaurantId: restaurant.id,
                            restaurantName: restaurant.name,
                            onGoToCart: { selectedTab = .cart }
                        )
                    }
            }
            .tabItem { Label("Home", systemImage: "house.fill") }
            .tag(AppTab.home)

            NavigationStack {
                OrdersTabContent(showingAuthSheet: $showingAuthSheet)
                    .navigationDestination(for: Int.self) { orderId in
                        OrderDetailView(orderId: orderId)
                    }
            }
            .tabItem { Label("Orders", systemImage: "receipt") }
            .tag(AppTab.orders)

            NavigationStack(path: $cartPath) {
                CartView(
                    onLoginRequired: { showingAuthSheet = true },
                    onOrderPlaced: { orderId in cartPath.append(orderId) }
                )
                .navigationDestination(for: Int.self) { orderId in
                    OrderDetailView(orderId: orderId)
                }
            }
            .tabItem { Label("Cart", systemImage: "cart.fill") }
            .badge(cartStore.totalCount)
            .tag(AppTab.cart)

            NavigationStack {
                AccountView(onLoginClick: { showingAuthSheet = true })
            }
            .tabItem { Label("Account", systemImage: "person.fill") }
            .tag(AppTab.account)
        }
        .sheet(isPresented: $showingAuthSheet) {
            AuthSheetView()
        }
    }
}

private struct OrdersTabContent: View {
    @EnvironmentObject private var authStore: AuthStore
    @Binding var showingAuthSheet: Bool

    var body: some View {
        if authStore.isLoggedIn {
            OrdersView()
        } else {
            VStack(spacing: 12) {
                Text("Log in to see your orders")
                Button("Log In") { showingAuthSheet = true }
                    .buttonStyle(.borderedProminent)
            }
        }
    }
}
