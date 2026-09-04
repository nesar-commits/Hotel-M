import SwiftUI

struct HomeView: View {
    @StateObject private var viewModel = HomeViewModel()

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Image(systemName: "magnifyingglass").foregroundStyle(.secondary)
                TextField("Search restaurants or cuisines", text: $viewModel.query)
                    .textFieldStyle(.plain)
            }
            .padding(10)
            .background(Color(.secondarySystemBackground))
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .padding(.horizontal)
            .padding(.top, 8)

            content
        }
        .navigationTitle("TastyHub")
    }

    @ViewBuilder
    private var content: some View {
        if viewModel.isLoading && viewModel.restaurants.isEmpty {
            Spacer()
            ProgressView()
            Spacer()
        } else if let error = viewModel.errorMessage, viewModel.restaurants.isEmpty {
            Spacer()
            VStack(spacing: 8) {
                Text(error)
                Button("Retry") { viewModel.retry() }
            }
            Spacer()
        } else if viewModel.restaurants.isEmpty {
            Spacer()
            Text("No restaurants found").foregroundStyle(.secondary)
            Spacer()
        } else {
            List {
                ForEach(viewModel.restaurants) { restaurant in
                    NavigationLink(value: restaurant) {
                        RestaurantRow(restaurant: restaurant)
                    }
                    .onAppear {
                        if restaurant.id == viewModel.restaurants.last?.id {
                            viewModel.loadMore()
                        }
                    }
                }
                if viewModel.isLoadingMore {
                    HStack {
                        Spacer()
                        ProgressView()
                        Spacer()
                    }
                }
            }
            .listStyle(.plain)
        }
    }
}

private struct RestaurantRow: View {
    let restaurant: RestaurantOut

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            AsyncImage(url: URL(string: restaurant.imageUrl)) { phase in
                if let image = phase.image {
                    image.resizable().aspectRatio(contentMode: .fill)
                } else {
                    Color(.tertiarySystemFill)
                }
            }
            .frame(width: 84, height: 84)
            .clipShape(RoundedRectangle(cornerRadius: 10))

            VStack(alignment: .leading, spacing: 4) {
                Text(restaurant.name).font(.headline)
                Text(restaurant.cuisineType).font(.subheadline).foregroundStyle(.secondary)
                HStack(spacing: 12) {
                    Label(String(format: "%.1f", restaurant.rating), systemImage: "star.fill")
                        .font(.caption)
                        .foregroundStyle(TastyHubColor.primary)
                    Text("₹\(restaurant.costForTwo) for two").font(.caption)
                }
                Text(restaurant.city).font(.caption).foregroundStyle(.secondary)
                if !restaurant.isOpen {
                    Text("Closed").font(.caption).foregroundStyle(.red)
                }
            }
        }
        .padding(.vertical, 4)
    }
}
