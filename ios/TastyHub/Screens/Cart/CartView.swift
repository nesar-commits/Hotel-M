import SwiftUI

struct CartView: View {
    let onLoginRequired: () -> Void
    let onOrderPlaced: (Int) -> Void

    @EnvironmentObject private var cartStore: CartStore
    @EnvironmentObject private var authStore: AuthStore
    @EnvironmentObject private var orderStore: OrderStore

    var body: some View {
        Group {
            if cartStore.items.isEmpty {
                VStack {
                    Spacer()
                    Text("Your cart is empty").foregroundStyle(.secondary)
                    Spacer()
                }
            } else {
                VStack(spacing: 0) {
                    if let name = cartStore.restaurantName {
                        Text(name)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding()
                    }
                    List {
                        ForEach(cartStore.items) { item in
                            HStack {
                                VStack(alignment: .leading) {
                                    Text(item.name).fontWeight(.semibold)
                                    Text("₹\(item.price, specifier: "%.0f") × \(item.quantity)")
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                                Button(action: { cartStore.decrement(item.menuItemId) }) {
                                    Image(systemName: "minus.circle.fill")
                                }
                                Text("\(item.quantity)")
                                Button(action: { cartStore.increment(item.menuItemId) }) {
                                    Image(systemName: "plus.circle.fill")
                                }
                            }
                        }
                    }
                    .listStyle(.plain)

                    if let error = orderStore.placeOrderError {
                        Text(error).foregroundStyle(.red).font(.caption).padding(.horizontal)
                    }

                    VStack(spacing: 12) {
                        HStack {
                            Text("Total").fontWeight(.bold)
                            Spacer()
                            Text("₹\(cartStore.totalPrice, specifier: "%.0f")").fontWeight(.bold)
                        }
                        Button {
                            checkout()
                        } label: {
                            if orderStore.isPlacingOrder {
                                ProgressView().tint(.white)
                            } else {
                                Text(authStore.isLoggedIn ? "Place Order" : "Login to Checkout")
                                    .frame(maxWidth: .infinity)
                            }
                        }
                        .buttonStyle(.borderedProminent)
                        .disabled(orderStore.isPlacingOrder)
                    }
                    .padding()
                }
            }
        }
        .navigationTitle("Your Cart")
    }

    private func checkout() {
        guard authStore.isLoggedIn else {
            onLoginRequired()
            return
        }
        guard let restaurantId = cartStore.restaurantId else { return }
        let items = cartStore.items.map { OrderItemCreate(menuItemId: $0.menuItemId, quantity: $0.quantity) }
        Task {
            if let order = await orderStore.placeOrder(restaurantId: restaurantId, items: items) {
                cartStore.clear()
                onOrderPlaced(order.id)
            }
        }
    }
}
