import Foundation

@MainActor
final class HomeViewModel: ObservableObject {
    @Published var query = "" {
        didSet { scheduleSearch() }
    }
    @Published private(set) var restaurants: [RestaurantOut] = []
    @Published private(set) var isLoading = false
    @Published private(set) var isLoadingMore = false
    @Published private(set) var errorMessage: String?

    private var canLoadMore = true
    private var searchTask: Task<Void, Never>?
    private let api = APIClient.shared
    private let pageSize = 24

    init() {
        Task { await load(reset: true) }
    }

    private func scheduleSearch() {
        searchTask?.cancel()
        searchTask = Task {
            try? await Task.sleep(nanoseconds: 350_000_000)
            guard !Task.isCancelled else { return }
            await load(reset: true)
        }
    }

    func retry() {
        Task { await load(reset: true) }
    }

    func loadMore() {
        guard !isLoading, !isLoadingMore, canLoadMore else { return }
        Task { await load(reset: false) }
    }

    private func load(reset: Bool) async {
        if reset { isLoading = true } else { isLoadingMore = true }
        errorMessage = nil
        let offset = reset ? 0 : restaurants.count
        do {
            let page = try await api.getRestaurants(search: query.isEmpty ? nil : query, limit: pageSize, offset: offset)
            restaurants = reset ? page : restaurants + page
            canLoadMore = page.count == pageSize
        } catch let error as APIError {
            errorMessage = error.errorDescription
        } catch {
            errorMessage = "Failed to load restaurants"
        }
        isLoading = false
        isLoadingMore = false
    }
}
