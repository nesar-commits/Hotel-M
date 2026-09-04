import Foundation

struct CartItem: Identifiable, Hashable {
    let menuItemId: Int
    var name: String
    var price: Double
    var quantity: Int
    var id: Int { menuItemId }
}

/// App-scoped, in-memory only (lost on relaunch) — mirrors the web app's CartContext and the
/// Android app's CartViewModel.
@MainActor
final class CartStore: ObservableObject {
    @Published private(set) var restaurantId: Int?
    @Published private(set) var restaurantName: String?
    @Published private(set) var items: [CartItem] = []

    var totalCount: Int { items.reduce(0) { $0 + $1.quantity } }
    var totalPrice: Double { items.reduce(0) { $0 + $1.price * Double($1.quantity) } }

    /// True if adding an item from a different restaurant would mix carts — caller should confirm
    /// before calling replaceCartWith.
    func wouldConflict(restaurantId: Int) -> Bool {
        self.restaurantId != nil && self.restaurantId != restaurantId && !items.isEmpty
    }

    func addItem(_ item: MenuItemOut, restaurantId: Int, restaurantName: String) {
        self.restaurantId = restaurantId
        self.restaurantName = restaurantName
        if let index = items.firstIndex(where: { $0.menuItemId == item.id }) {
            items[index].quantity += 1
        } else {
            items.append(CartItem(menuItemId: item.id, name: item.name, price: item.price, quantity: 1))
        }
    }

    func replaceCartWith(_ item: MenuItemOut, restaurantId: Int, restaurantName: String) {
        self.restaurantId = restaurantId
        self.restaurantName = restaurantName
        items = [CartItem(menuItemId: item.id, name: item.name, price: item.price, quantity: 1)]
    }

    func increment(_ menuItemId: Int) {
        if let index = items.firstIndex(where: { $0.menuItemId == menuItemId }) {
            items[index].quantity += 1
        }
    }

    func decrement(_ menuItemId: Int) {
        if let index = items.firstIndex(where: { $0.menuItemId == menuItemId }) {
            items[index].quantity -= 1
            if items[index].quantity <= 0 { items.remove(at: index) }
        }
        if items.isEmpty {
            restaurantId = nil
            restaurantName = nil
        }
    }

    func quantity(for menuItemId: Int) -> Int {
        items.first(where: { $0.menuItemId == menuItemId })?.quantity ?? 0
    }

    func clear() {
        items = []
        restaurantId = nil
        restaurantName = nil
    }
}
