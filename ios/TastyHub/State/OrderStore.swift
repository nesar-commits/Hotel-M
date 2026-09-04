import Foundation

private let activeStatuses: Set<String> = ["placed", "confirmed", "preparing", "ready", "out_for_delivery"]

@MainActor
final class OrderStore: ObservableObject {
    @Published private(set) var isPlacingOrder = false
    @Published var placeOrderError: String?
    @Published private(set) var myOrders: [OrderOut] = []
    @Published private(set) var isLoadingOrders = false
    @Published private(set) var selectedOrder: OrderOut?

    private let api = APIClient.shared

    func placeOrder(restaurantId: Int, items: [OrderItemCreate]) async -> OrderOut? {
        isPlacingOrder = true
        placeOrderError = nil
        defer { isPlacingOrder = false }
        do {
            return try await api.placeOrder(restaurantId: restaurantId, items: items)
        } catch let error as APIError {
            placeOrderError = error.errorDescription
            return nil
        } catch {
            placeOrderError = "Could not place order"
            return nil
        }
    }

    func loadMyOrders() async {
        isLoadingOrders = true
        defer { isLoadingOrders = false }
        if let orders = try? await api.getMyOrders() {
            myOrders = orders.sorted { $0.id > $1.id }
        }
    }

    /// Polls every 4s until the order reaches a terminal status. Driven from a `.task(id:)` view
    /// modifier, which cancels this automatically when the view disappears or `orderId` changes.
    func watchOrder(_ orderId: Int) async {
        while !Task.isCancelled {
            guard let order = try? await api.getOrder(id: orderId) else { break }
            selectedOrder = order
            if !activeStatuses.contains(order.status) { break }
            try? await Task.sleep(nanoseconds: 4_000_000_000)
        }
    }
}
