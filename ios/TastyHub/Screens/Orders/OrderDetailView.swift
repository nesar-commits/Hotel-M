import SwiftUI

private let statusFlow = ["placed", "confirmed", "preparing", "ready", "out_for_delivery", "delivered"]

struct OrderDetailView: View {
    let orderId: Int
    @EnvironmentObject private var orderStore: OrderStore

    var body: some View {
        Group {
            if let order = orderStore.selectedOrder, order.id == orderId {
                ScrollView {
                    VStack(alignment: .leading, spacing: 16) {
                        Text(order.restaurantName).font(.title2).fontWeight(.bold)

                        if order.status == "cancelled" {
                            Text("Order cancelled").foregroundStyle(.red).fontWeight(.semibold)
                        } else {
                            let currentIndex = statusFlow.firstIndex(of: order.status) ?? -1
                            VStack(alignment: .leading, spacing: 10) {
                                ForEach(Array(statusFlow.enumerated()), id: \.offset) { index, status in
                                    let reached = index <= currentIndex
                                    HStack {
                                        ZStack {
                                            Circle()
                                                .fill(reached ? TastyHubColor.primary : Color(.systemGray4))
                                                .frame(width: 24, height: 24)
                                            if reached {
                                                Image(systemName: "checkmark")
                                                    .font(.system(size: 12, weight: .bold))
                                                    .foregroundStyle(.white)
                                            }
                                        }
                                        Text(status.replacingOccurrences(of: "_", with: " ").capitalized)
                                            .fontWeight(index == currentIndex ? .bold : .regular)
                                    }
                                }
                            }
                        }

                        Text("Items").fontWeight(.semibold)
                        ForEach(order.items) { item in
                            HStack {
                                Text("\(item.menuItemName) × \(item.quantity)")
                                Spacer()
                                Text("₹\(item.price * Double(item.quantity), specifier: "%.0f")")
                            }
                        }
                        Divider()
                        HStack {
                            Text("Total").fontWeight(.bold)
                            Spacer()
                            Text("₹\(order.totalAmount, specifier: "%.0f")").fontWeight(.bold)
                        }
                    }
                    .padding()
                }
            } else {
                ProgressView()
            }
        }
        .navigationTitle("Order #\(orderId)")
        .navigationBarTitleDisplayMode(.inline)
        .task(id: orderId) { await orderStore.watchOrder(orderId) }
    }
}
