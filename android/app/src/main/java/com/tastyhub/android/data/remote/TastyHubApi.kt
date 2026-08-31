package com.tastyhub.android.data.remote

import com.tastyhub.android.data.model.LoginRequest
import com.tastyhub.android.data.model.MenuItemOut
import com.tastyhub.android.data.model.OrderCreate
import com.tastyhub.android.data.model.OrderOut
import com.tastyhub.android.data.model.RestaurantCountOut
import com.tastyhub.android.data.model.RestaurantDetailOut
import com.tastyhub.android.data.model.RestaurantOut
import com.tastyhub.android.data.model.TokenOut
import com.tastyhub.android.data.model.UserCreate
import com.tastyhub.android.data.model.UserOut
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface TastyHubApi {
    @GET("restaurants")
    suspend fun getRestaurants(
        @Query("city") city: String? = null,
        @Query("search") search: String? = null,
        @Query("limit") limit: Int = 24,
        @Query("offset") offset: Int = 0,
    ): List<RestaurantOut>

    @GET("restaurants/count")
    suspend fun getRestaurantCount(
        @Query("city") city: String? = null,
        @Query("search") search: String? = null,
    ): RestaurantCountOut

    @GET("restaurants/{id}")
    suspend fun getRestaurant(@Path("id") id: Int): RestaurantDetailOut

    @GET("restaurants/{restaurantId}/menu")
    suspend fun getMenuItems(
        @Path("restaurantId") restaurantId: Int,
        @Query("category_id") categoryId: Int? = null,
        @Query("is_veg") isVeg: Boolean? = null,
        @Query("search") search: String? = null,
    ): List<MenuItemOut>

    @POST("users/signup")
    suspend fun signup(@Body body: UserCreate): TokenOut

    @POST("users/login")
    suspend fun login(@Body body: LoginRequest): TokenOut

    @GET("users/me")
    suspend fun getMe(): UserOut

    @POST("orders")
    suspend fun placeOrder(@Body order: OrderCreate): OrderOut

    @GET("orders/me")
    suspend fun getMyOrders(): List<OrderOut>

    @GET("orders/{id}")
    suspend fun getOrder(@Path("id") id: Int): OrderOut
}
