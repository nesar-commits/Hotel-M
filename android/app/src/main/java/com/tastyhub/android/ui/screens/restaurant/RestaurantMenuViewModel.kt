package com.tastyhub.android.ui.screens.restaurant

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.tastyhub.android.data.model.RestaurantDetailOut
import com.tastyhub.android.data.remote.TastyHubApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class RestaurantMenuUiState(
    val restaurant: RestaurantDetailOut? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val vegOnly: Boolean = false,
    val selectedCategoryId: Int? = null,
    val searchQuery: String = "",
)

class RestaurantMenuViewModel(
    private val api: TastyHubApi,
    private val restaurantId: Int,
) : ViewModel() {
    private val _uiState = MutableStateFlow(RestaurantMenuUiState())
    val uiState: StateFlow<RestaurantMenuUiState> = _uiState

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            runCatching { api.getRestaurant(restaurantId) }
                .onSuccess { _uiState.value = _uiState.value.copy(restaurant = it, isLoading = false) }
                .onFailure {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = it.message ?: "Failed to load restaurant",
                    )
                }
        }
    }

    fun toggleVegOnly() {
        _uiState.value = _uiState.value.copy(vegOnly = !_uiState.value.vegOnly)
    }

    fun selectCategory(categoryId: Int?) {
        _uiState.value = _uiState.value.copy(selectedCategoryId = categoryId)
    }

    fun onSearchChange(query: String) {
        _uiState.value = _uiState.value.copy(searchQuery = query)
    }
}

class RestaurantMenuViewModelFactory(
    private val api: TastyHubApi,
    private val restaurantId: Int,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T =
        RestaurantMenuViewModel(api, restaurantId) as T
}
