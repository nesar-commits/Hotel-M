import SwiftUI

struct RestaurantMenuView: View {
    let restaurantId: Int
    let restaurantName: String
    let onGoToCart: () -> Void

    @StateObject private var viewModel: RestaurantMenuViewModel
    @EnvironmentObject private var cartStore: CartStore
    @State private var conflictItem: MenuItemOut?

    init(restaurantId: Int, restaurantName: String, onGoToCart: @escaping () -> Void) {
        self.restaurantId = restaurantId
        self.restaurantName = restaurantName
        self.onGoToCart = onGoToCart
        _viewModel = StateObject(wrappedValue: RestaurantMenuViewModel(restaurantId: restaurantId))
    }

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else if let error = viewModel.errorMessage {
                VStack(spacing: 8) {
                    Text(error)
                    Button("Retry") { Task { await viewModel.load() } }
                }
            } else if let restaurant = viewModel.restaurant {
                menuContent(restaurant)
            }
        }
        .navigationTitle(restaurantName)
        .navigationBarTitleDisplayMode(.inline)
        .safeAreaInset(edge: .bottom) {
            if !cartStore.items.isEmpty {
                HStack {
                    Text("\(cartStore.totalCount) item(s) · ₹\(cartStore.totalPrice, specifier: "%.0f")")
                        .fontWeight(.semibold)
                    Spacer()
                    Button("View Cart", action: onGoToCart)
                        .buttonStyle(.borderedProminent)
                }
                .padding()
                .background(.bar)
            }
        }
        .alert(
            "Start a new cart?",
            isPresented: Binding(get: { conflictItem != nil }, set: { if !$0 { conflictItem = nil } })
        ) {
            Button("Clear & Add") {
                if let item = conflictItem, let restaurant = viewModel.restaurant {
                    cartStore.replaceCartWith(item, restaurantId: restaurant.id, restaurantName: restaurant.name)
                }
                conflictItem = nil
            }
            Button("Cancel", role: .cancel) { conflictItem = nil }
        } message: {
            Text("Your cart has items from another restaurant. Clear it and add this item instead?")
        }
    }

    @ViewBuilder
    private func menuContent(_ restaurant: RestaurantDetailOut) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            VStack(alignment: .leading, spacing: 6) {
                Text(restaurant.cuisineType).font(.subheadline)
                Text("\(restaurant.address) · \(restaurant.city)").font(.caption).foregroundStyle(.secondary)

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        FilterChip(title: "Veg only", isSelected: viewModel.vegOnly) {
                            viewModel.vegOnly.toggle()
                        }
                        FilterChip(title: "All", isSelected: viewModel.selectedCategoryId == nil) {
                            viewModel.selectedCategoryId = nil
                        }
                        ForEach(restaurant.categories.sorted { $0.sortOrder < $1.sortOrder }) { category in
                            FilterChip(title: category.name, isSelected: viewModel.selectedCategoryId == category.id) {
                                viewModel.selectedCategoryId = category.id
                            }
                        }
                    }
                }

                TextField("Search dishes", text: $viewModel.searchQuery)
                    .textFieldStyle(.roundedBorder)
            }
            .padding()

            List(viewModel.filteredItems) { item in
                MenuItemRow(
                    item: item,
                    quantity: cartStore.quantity(for: item.id),
                    onAdd: {
                        if cartStore.wouldConflict(restaurantId: restaurant.id) {
                            conflictItem = item
                        } else {
                            cartStore.addItem(item, restaurantId: restaurant.id, restaurantName: restaurant.name)
                        }
                    },
                    onRemove: { cartStore.decrement(item.id) }
                )
            }
            .listStyle(.plain)
        }
    }
}

private struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.caption)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isSelected ? TastyHubColor.primary : Color(.secondarySystemBackground))
                .foregroundStyle(isSelected ? .white : .primary)
                .clipShape(Capsule())
        }
        .buttonStyle(.plain)
    }
}

private struct MenuItemRow: View {
    let item: MenuItemOut
    let quantity: Int
    let onAdd: () -> Void
    let onRemove: () -> Void

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 4) {
                    Image(systemName: item.isVeg ? "leaf.fill" : "flame.fill")
                        .foregroundStyle(item.isVeg ? .green : .red)
                        .font(.caption2)
                    Text(item.name).fontWeight(.semibold)
                }
                if !item.description.isEmpty {
                    Text(item.description).font(.caption).foregroundStyle(.secondary).lineLimit(2)
                }
                Text("₹\(item.price, specifier: "%.0f")").font(.subheadline)
            }
            Spacer()
            if quantity == 0 {
                Button("ADD", action: onAdd)
                    .buttonStyle(.bordered)
                    .disabled(!item.isAvailable)
            } else {
                HStack(spacing: 12) {
                    Button(action: onRemove) { Image(systemName: "minus.circle.fill") }
                    Text("\(quantity)")
                    Button(action: onAdd) { Image(systemName: "plus.circle.fill") }
                }
                .foregroundStyle(TastyHubColor.primary)
            }
        }
        .padding(.vertical, 4)
    }
}
