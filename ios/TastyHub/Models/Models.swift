import Foundation

// Mirrors backend/app/schemas.py. All fields are non-optional because FastAPI/Pydantic always
// serializes model fields (including defaults) on output, so the JSON payload is never missing
// a key — JSONDecoder's convertFromSnakeCase strategy (configured in APIClient) maps
// `cuisine_type` -> `cuisineType` etc. without needing explicit CodingKeys.

struct CategoryOut: Codable, Identifiable, Hashable {
    let id: Int
    let restaurantId: Int
    let name: String
    let sortOrder: Int
}

struct MenuItemOut: Codable, Identifiable, Hashable {
    let id: Int
    let restaurantId: Int
    let categoryId: Int
    let name: String
    let description: String
    let price: Double
    let isVeg: Bool
    let isAvailable: Bool
    let imageUrl: String
    let rating: Double
    let tags: String
}

struct RestaurantOut: Codable, Identifiable, Hashable {
    let id: Int
    let name: String
    let description: String
    let cuisineType: String
    let city: String
    let address: String
    let rating: Double
    let costForTwo: Int
    let imageUrl: String
    let isOpen: Bool
    let latitude: Double
    let longitude: Double
    let createdAt: String
}

struct RestaurantDetailOut: Codable, Identifiable, Hashable {
    let id: Int
    let name: String
    let description: String
    let cuisineType: String
    let city: String
    let address: String
    let rating: Double
    let costForTwo: Int
    let imageUrl: String
    let isOpen: Bool
    let latitude: Double
    let longitude: Double
    let createdAt: String
    let categories: [CategoryOut]
    let menuItems: [MenuItemOut]
}

struct RestaurantCountOut: Codable {
    let total: Int
}

struct UserOut: Codable, Hashable {
    let id: Int
    let name: String
    let email: String
    let isStaff: Bool
}

struct TokenOut: Codable {
    let accessToken: String
    let tokenType: String
    let user: UserOut
}

struct UserCreate: Codable {
    let name: String
    let email: String
    let password: String
}

struct LoginRequest: Codable {
    let email: String
    let password: String
}

struct OrderItemCreate: Codable {
    let menuItemId: Int
    let quantity: Int
}

struct OrderCreate: Codable {
    let restaurantId: Int
    let items: [OrderItemCreate]
}

struct OrderItemOut: Codable, Identifiable, Hashable {
    let id: Int
    let menuItemId: Int
    let menuItemName: String
    let quantity: Int
    let price: Double
}

struct OrderOut: Codable, Identifiable, Hashable {
    let id: Int
    let userId: Int
    let restaurantId: Int
    let restaurantName: String
    let status: String
    let totalAmount: Double
    let createdAt: String
    let items: [OrderItemOut]
}
