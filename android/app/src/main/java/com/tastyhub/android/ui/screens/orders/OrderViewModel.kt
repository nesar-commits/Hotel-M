package com.tastyhub.android.ui.screens.orders

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.tastyhub.android.data.model.OrderCreate
import com.tastyhub.android.data.model.OrderItemCreate
import com.tastyhub.android.data.model.OrderOut
import com.tastyhub.android.data.remote.TastyHubApi
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

private val ACTIVE_STATUSES = setOf("placed", "confirmed", "preparing", "ready", "out_for_delivery")

class OrderViewModel(private val api: TastyHubApi) : ViewModel() {

    private val _isPlacingOrder = MutableStateFlow(false)
    val isPlacingOrder: StateFlow<Boolean> = _isPlacingOrder

    private val _placeOrderError = MutableStateFlow<String?>(null)
    val placeOrderError: StateFlow<String?> = _placeOrderError

    private val _myOrders = MutableStateFlow<List<OrderOut>>(emptyList())
    val myOrders: StateFlow<List<OrderOut>> = _myOrders

    private val _isLoadingOrders = MutableStateFlow(false)
    val isLoadingOrders: StateFlow<Boolean> = _isLoadingOrders

    private val _selectedOrder = MutableStateFlow<OrderOut?>(null)
    val selectedOrder: StateFlow<OrderOut?> = _selectedOrder

    fun placeOrder(restaurantId: Int, items: List<OrderItemCreate>, onSuccess: (OrderOut) -> Unit) {
        viewModelScope.launch {
            _isPlacingOrder.value = true
            _placeOrderError.value = null
            runCatching { api.placeOrder(OrderCreate(restaurantId, items)) }
                .onSuccess {
                    _isPlacingOrder.value = false
                    onSuccess(it)
                }
                .onFailure {
                    _isPlacingOrder.value = false
                    _placeOrderError.value = it.message ?: "Could not place order"
                }
        }
    }

    fun loadMyOrders() {
        viewModelScope.launch {
            _isLoadingOrders.value = true
            runCatching { api.getMyOrders() }
                .onSuccess { orders -> _myOrders.value = orders.sortedByDescending { it.id } }
            _isLoadingOrders.value = false
        }
    }

    /** Polls the order every 4s until it reaches a terminal status. Caller must cancel the returned [Job]
     *  (e.g. from a DisposableEffect) when leaving the screen, since this ViewModel outlives one screen. */
    fun watchOrder(orderId: Int): Job = viewModelScope.launch {
        while (true) {
            val order = runCatching { api.getOrder(orderId) }.getOrNull()
            if (order != null) _selectedOrder.value = order
            if (order == null || order.status !in ACTIVE_STATUSES) break
            delay(4000)
        }
    }
}

class OrderViewModelFactory(private val api: TastyHubApi) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T = OrderViewModel(api) as T
}
