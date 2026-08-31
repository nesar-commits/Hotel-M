package com.tastyhub.android.data

import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

/**
 * Backed by plain SharedPreferences (not DataStore) so the auth interceptor can read the
 * current token synchronously on the OkHttp dispatcher thread without suspending.
 */
class TokenManager(context: Context) {
    private val prefs = context.getSharedPreferences("tastyhub_prefs", Context.MODE_PRIVATE)

    private val _token = MutableStateFlow(prefs.getString(KEY_TOKEN, null))
    val token: StateFlow<String?> = _token

    fun saveToken(token: String) {
        prefs.edit().putString(KEY_TOKEN, token).apply()
        _token.value = token
    }

    fun clearToken() {
        prefs.edit().remove(KEY_TOKEN).apply()
        _token.value = null
    }

    companion object {
        private const val KEY_TOKEN = "access_token"
    }
}
