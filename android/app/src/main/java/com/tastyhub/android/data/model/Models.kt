package com.tastyhub.android.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class RestaurantOut(
    val id: Int,
    val name: String,
    val description: String = "",
    @SerialName("cuisine_type") val cuisineType: String = "",
    val city: String = "",
    val address: String = "",
    val rating: Double = 0.0,
    @SerialName("cost_for_two") val costForTwo: Int = 0,
    @SerialName("image_url") val imageUrl: String = "",
    @SerialName("is_open") val isOpen: Boolean = true,
    val latitude: Double = 0.0,
    val longitude: Double = 0.0,
    @SerialName("created_at") val createdAt: String = "",
)

@Serializable
data class CategoryOut(
    val id: Int,
    @SerialName("restaurant_id") val restaurantId: Int,
    val name: String,
    @SerialName("sort_order") val sortOrder: Int = 0,
)

@Serializable
data class MenuItemOut(
    val id: Int,
    @SerialName("restaurant_id") val restaurantId: Int,
    @SerialName("category_id") val categoryId: Int,
    val name: String,
    val description: String = "",
    val price: Double,
    @SerialName("is_veg") val isVeg: Boolean = true,
    @SerialName("is_available") val isAvailable: Boolean = true,
    @SerialName("image_url") val imageUrl: String = "",
    val rating: Double = 0.0,
    val tags: String = "",
)

@Serializable
data class RestaurantDetailOut(
    val id: Int,
    val name: String,
    val description: String = "",
    @SerialName("cuisine_type") val cuisineType: String = "",
    val city: String = "",
    val address: String = "",
    val rating: Double = 0.0,
    @SerialName("cost_for_two") val costForTwo: Int = 0,
    @SerialName("image_url") val imageUrl: String = "",
    @SerialName("is_open") val isOpen: Boolean = true,
    val latitude: Double = 0.0,
    val longitude: Double = 0.0,
    @SerialName("created_at") val createdAt: String = "",
    val categories: List<CategoryOut> = emptyList(),
    @SerialName("menu_items") val menuItems: List<MenuItemOut> = emptyList(),
)

@Serializable
data class RestaurantCountOut(val total: Int)

@Serializable
data class UserOut(
    val id: Int,
    val name: String,
    val email: String,
    @SerialName("is_staff") val isStaff: Boolean = false,
)

@Serializable
data class TokenOut(
    @SerialName("access_token") val accessToken: String,
    @SerialName("token_type") val tokenType: String = "bearer",
    val user: UserOut,
)

@Serializable
data class UserCreate(val name: String, val email: String, val password: String)

@Serializable
data class LoginRequest(val email: String, val password: String)

@Serializable
data class OrderItemCreate(@SerialName("menu_item_id") val menuItemId: Int, val quantity: Int = 1)

@Serializable
data class OrderCreate(@SerialName("restaurant_id") val restaurantId: Int, val items: List<OrderItemCreate>)

@Serializable
data class OrderItemOut(
    val id: Int,
    @SerialName("menu_item_id") val menuItemId: Int,
    @SerialName("menu_item_name") val menuItemName: String = "",
    val quantity: Int,
    val price: Double,
)

@Serializable
data class OrderOut(
    val id: Int,
    @SerialName("user_id") val userId: Int,
    @SerialName("restaurant_id") val restaurantId: Int,
    @SerialName("restaurant_name") val restaurantName: String = "",
    val status: String,
    @SerialName("total_amount") val totalAmount: Double,
    @SerialName("created_at") val createdAt: String,
    val items: List<OrderItemOut> = emptyList(),
)
