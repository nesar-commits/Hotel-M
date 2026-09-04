import SwiftUI

struct OrdersView: View {
    @EnvironmentObject private var orderStore: OrderStore

    var body: some View {
        Group {
            if orderStore.isLoadingOrders && orderStore.myOrders.isEmpty {
                ProgressView()
            } else if orderStore.myOrders.isEmpty {
                Text("No orders yet").foregroundStyle(.secondary)
            } else {
                List(orderStore.myOrders) { order in
                    NavigationLink(value: order.id) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(order.restaurantName).fontWeight(.semibold)
                            Text("Order #\(order.id) · \(order.status.replacingOccurrences(of: "_", with: " "))")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                            Text("₹\(order.totalAmount, specifier: "%.0f")").font(.caption)
                        }
                    }
                }
                .listStyle(.plain)
            }
        }
        .navigationTitle("Your Orders")
        .task { await orderStore.loadMyOrders() }
    }
}
