package com.tastyhub.android.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.tastyhub.android.data.TokenManager
import com.tastyhub.android.data.model.LoginRequest
import com.tastyhub.android.data.model.UserCreate
import com.tastyhub.android.data.model.UserOut
import com.tastyhub.android.data.remote.TastyHubApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

sealed interface AuthUiState {
    data object Loading : AuthUiState
    data class LoggedIn(val user: UserOut) : AuthUiState
    data object LoggedOut : AuthUiState
}

class AuthViewModel(
    private val api: TastyHubApi,
    private val tokenManager: TokenManager,
) : ViewModel() {

    private val _uiState = MutableStateFlow<AuthUiState>(AuthUiState.Loading)
    val uiState: StateFlow<AuthUiState> = _uiState

    private val _isSubmitting = MutableStateFlow(false)
    val isSubmitting: StateFlow<Boolean> = _isSubmitting

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage

    init {
        viewModelScope.launch {
            val token = tokenManager.token.value
            if (token.isNullOrBlank()) {
                _uiState.value = AuthUiState.LoggedOut
            } else {
                runCatching { api.getMe() }
                    .onSuccess { _uiState.value = AuthUiState.LoggedIn(it) }
                    .onFailure {
                        tokenManager.clearToken()
                        _uiState.value = AuthUiState.LoggedOut
                    }
            }
        }
    }

    fun login(email: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            _isSubmitting.value = true
            _errorMessage.value = null
            runCatching { api.login(LoginRequest(email, password)) }
                .onSuccess {
                    tokenManager.saveToken(it.accessToken)
                    _uiState.value = AuthUiState.LoggedIn(it.user)
                    _isSubmitting.value = false
                    onSuccess()
                }
                .onFailure {
                    _isSubmitting.value = false
                    _errorMessage.value = "Invalid email or password"
                }
        }
    }

    fun signup(name: String, email: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            _isSubmitting.value = true
            _errorMessage.value = null
            runCatching { api.signup(UserCreate(name, email, password)) }
                .onSuccess {
                    tokenManager.saveToken(it.accessToken)
                    _uiState.value = AuthUiState.LoggedIn(it.user)
                    _isSubmitting.value = false
                    onSuccess()
                }
                .onFailure {
                    _isSubmitting.value = false
                    _errorMessage.value = it.message ?: "Signup failed"
                }
        }
    }

    fun logout() {
        tokenManager.clearToken()
        _uiState.value = AuthUiState.LoggedOut
    }
}

class AuthViewModelFactory(
    private val api: TastyHubApi,
    private val tokenManager: TokenManager,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T = AuthViewModel(api, tokenManager) as T
}
