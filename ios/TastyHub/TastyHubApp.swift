import SwiftUI

@main
struct TastyHubApp: App {
    @StateObject private var authStore = AuthStore()
    @StateObject private var cartStore = CartStore()
    @StateObject private var orderStore = OrderStore()

    var body: some Scene {
        WindowGroup {
            RootTabView()
                .environmentObject(authStore)
                .environmentObject(cartStore)
                .environmentObject(orderStore)
                .tint(TastyHubColor.primary)
        }
    }
}
