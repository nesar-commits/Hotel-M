import Foundation

@MainActor
final class RestaurantMenuViewModel: ObservableObject {
    @Published private(set) var restaurant: RestaurantDetailOut?
    @Published private(set) var isLoading = true
    @Published private(set) var errorMessage: String?
    @Published var vegOnly = false
    @Published var selectedCategoryId: Int?
    @Published var searchQuery = ""

    private let restaurantId: Int
    private let api = APIClient.shared

    init(restaurantId: Int) {
        self.restaurantId = restaurantId
        Task { await load() }
    }

    func load() async {
        isLoading = true
        errorMessage = nil
        do {
            restaurant = try await api.getRestaurant(id: restaurantId)
        } catch let error as APIError {
            errorMessage = error.errorDescription
        } catch {
            errorMessage = "Failed to load restaurant"
        }
        isLoading = false
    }

    var filteredItems: [MenuItemOut] {
        guard let restaurant else { return [] }
        return restaurant.menuItems.filter { item in
            (!vegOnly || item.isVeg)
                && (selectedCategoryId == nil || item.categoryId == selectedCategoryId)
                && (searchQuery.isEmpty || item.name.localizedCaseInsensitiveContains(searchQuery))
        }
    }
}
