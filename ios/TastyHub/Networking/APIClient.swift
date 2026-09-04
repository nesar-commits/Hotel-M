import Foundation

enum APIError: LocalizedError {
    case invalidResponse
    case http(status: Int, message: String?)
    case decoding(Error)

    var errorDescription: String? {
        switch self {
        case .invalidResponse: return "Invalid response from server"
        case .http(_, let message): return message ?? "Something went wrong"
        case .decoding: return "Failed to parse server response"
        }
    }
}

final class APIClient {
    static let shared = APIClient()

    /// Set by AuthStore after login/signup/session-restore; read on every request.
    var authToken: String?

    private let session = URLSession(configuration: .default)

    private let decoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder
    }()

    private let encoder: JSONEncoder = {
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        return encoder
    }()

    private init() {}

    private func url(_ path: String, query: [String: String?] = [:]) -> URL {
        var components = URLComponents(
            url: AppConfig.apiBaseURL.appendingPathComponent(path),
            resolvingAgainstBaseURL: false
        )!
        let items = query.compactMapValues { $0 }.map { URLQueryItem(name: $0.key, value: $0.value) }
        if !items.isEmpty { components.queryItems = items }
        return components.url!
    }

    private func send<T: Decodable>(_ request: URLRequest) async throws -> T {
        var request = request
        if let authToken, !authToken.isEmpty {
            request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        }
        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse else { throw APIError.invalidResponse }
        guard (200..<300).contains(http.statusCode) else {
            let detail = try? JSONDecoder().decode([String: String].self, from: data)
            throw APIError.http(status: http.statusCode, message: detail?["detail"])
        }
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw APIError.decoding(error)
        }
    }

    private func get<T: Decodable>(_ path: String, query: [String: String?] = [:]) async throws -> T {
        try await send(URLRequest(url: url(path, query: query)))
    }

    private func post<Body: Encodable, T: Decodable>(_ path: String, body: Body) async throws -> T {
        var request = URLRequest(url: url(path))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try encoder.encode(body)
        return try await send(request)
    }

    // MARK: Restaurants

    func getRestaurants(search: String? = nil, city: String? = nil, limit: Int = 24, offset: Int = 0) async throws -> [RestaurantOut] {
        try await get("restaurants", query: [
            "search": search,
            "city": city,
            "limit": String(limit),
            "offset": String(offset),
        ])
    }

    func getRestaurantCount(search: String? = nil, city: String? = nil) async throws -> RestaurantCountOut {
        try await get("restaurants/count", query: ["search": search, "city": city])
    }

    func getRestaurant(id: Int) async throws -> RestaurantDetailOut {
        try await get("restaurants/\(id)")
    }

    func getMenuItems(restaurantId: Int, categoryId: Int? = nil, isVeg: Bool? = nil, search: String? = nil) async throws -> [MenuItemOut] {
        try await get("restaurants/\(restaurantId)/menu", query: [
            "category_id": categoryId.map(String.init),
            "is_veg": isVeg.map { $0 ? "true" : "false" },
            "search": search,
        ])
    }

    // MARK: Auth

    func signup(name: String, email: String, password: String) async throws -> TokenOut {
        try await post("users/signup", body: UserCreate(name: name, email: email, password: password))
    }

    func login(email: String, password: String) async throws -> TokenOut {
        try await post("users/login", body: LoginRequest(email: email, password: password))
    }

    func getMe() async throws -> UserOut {
        try await get("users/me")
    }

    // MARK: Orders

    func placeOrder(restaurantId: Int, items: [OrderItemCreate]) async throws -> OrderOut {
        try await post("orders", body: OrderCreate(restaurantId: restaurantId, items: items))
    }

    func getMyOrders() async throws -> [OrderOut] {
        try await get("orders/me")
    }

    func getOrder(id: Int) async throws -> OrderOut {
        try await get("orders/\(id)")
    }
}
