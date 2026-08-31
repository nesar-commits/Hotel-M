package com.tastyhub.android.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.tastyhub.android.data.model.RestaurantOut
import com.tastyhub.android.data.remote.TastyHubApi
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

private const val PAGE_SIZE = 24

data class HomeUiState(
    val restaurants: List<RestaurantOut> = emptyList(),
    val query: String = "",
    val isLoading: Boolean = false,
    val isLoadingMore: Boolean = false,
    val canLoadMore: Boolean = true,
    val error: String? = null,
)

class HomeViewModel(private val api: TastyHubApi) : ViewModel() {
    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState

    private var searchJob: Job? = null

    init {
        loadRestaurants(reset = true)
    }

    fun onQueryChange(query: String) {
        _uiState.value = _uiState.value.copy(query = query)
        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            delay(350)
            loadRestaurants(reset = true)
        }
    }

    fun loadMore() {
        val state = _uiState.value
        if (state.isLoading || state.isLoadingMore || !state.canLoadMore) return
        loadRestaurants(reset = false)
    }

    fun retry() = loadRestaurants(reset = true)

    private fun loadRestaurants(reset: Boolean) {
        viewModelScope.launch {
            val state = _uiState.value
            _uiState.value = state.copy(isLoading = reset, isLoadingMore = !reset, error = null)
            val offset = if (reset) 0 else state.restaurants.size
            val search = state.query.ifBlank { null }
            runCatching { api.getRestaurants(search = search, limit = PAGE_SIZE, offset = offset) }
                .onSuccess { page ->
                    _uiState.value = _uiState.value.copy(
                        restaurants = if (reset) page else _uiState.value.restaurants + page,
                        isLoading = false,
                        isLoadingMore = false,
                        canLoadMore = page.size == PAGE_SIZE,
                    )
                }
                .onFailure {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        isLoadingMore = false,
                        error = it.message ?: "Failed to load restaurants",
                    )
                }
        }
    }
}

class HomeViewModelFactory(private val api: TastyHubApi) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T = HomeViewModel(api) as T
}
