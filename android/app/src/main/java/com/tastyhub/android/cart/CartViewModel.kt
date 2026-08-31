package com.tastyhub.android.cart

import androidx.lifecycle.ViewModel
import com.tastyhub.android.data.model.MenuItemOut
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update

data class CartItem(
    val menuItemId: Int,
    val name: String,
    val price: Double,
    val quantity: Int,
)

/** App-scoped (survives navigation, cleared on process death) — mirrors the web app's CartContext. */
class CartViewModel : ViewModel() {
    private val _restaurantId = MutableStateFlow<Int?>(null)
    val restaurantId: StateFlow<Int?> = _restaurantId

    private val _restaurantName = MutableStateFlow<String?>(null)
    val restaurantName: StateFlow<String?> = _restaurantName

    private val _items = MutableStateFlow<List<CartItem>>(emptyList())
    val items: StateFlow<List<CartItem>> = _items

    /** True if adding this item would mix restaurants — caller should confirm before calling [replaceCartWith]. */
    fun wouldConflict(restaurantId: Int): Boolean =
        _restaurantId.value != null && _restaurantId.value != restaurantId && _items.value.isNotEmpty()

    fun addItem(menuItem: MenuItemOut, restaurantId: Int, restaurantName: String) {
        _restaurantId.value = restaurantId
        _restaurantName.value = restaurantName
        _items.update { current ->
            val existing = current.find { it.menuItemId == menuItem.id }
            if (existing != null) {
                current.map { if (it.menuItemId == menuItem.id) it.copy(quantity = it.quantity + 1) else it }
            } else {
                current + CartItem(menuItem.id, menuItem.name, menuItem.price, 1)
            }
        }
    }

    fun replaceCartWith(menuItem: MenuItemOut, restaurantId: Int, restaurantName: String) {
        _restaurantId.value = restaurantId
        _restaurantName.value = restaurantName
        _items.value = listOf(CartItem(menuItem.id, menuItem.name, menuItem.price, 1))
    }

    fun incrementItem(menuItemId: Int) {
        _items.update { current ->
            current.map { if (it.menuItemId == menuItemId) it.copy(quantity = it.quantity + 1) else it }
        }
    }

    fun decrementItem(menuItemId: Int) {
        _items.update { current ->
            current.mapNotNull {
                if (it.menuItemId == menuItemId) {
                    val newQuantity = it.quantity - 1
                    if (newQuantity > 0) it.copy(quantity = newQuantity) else null
                } else {
                    it
                }
            }
        }
        if (_items.value.isEmpty()) {
            _restaurantId.value = null
            _restaurantName.value = null
        }
    }

    fun clearCart() {
        _items.value = emptyList()
        _restaurantId.value = null
        _restaurantName.value = null
    }
}
