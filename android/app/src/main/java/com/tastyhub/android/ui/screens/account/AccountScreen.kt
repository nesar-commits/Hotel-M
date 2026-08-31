package com.tastyhub.android.ui.screens.account

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.tastyhub.android.auth.AuthUiState
import com.tastyhub.android.auth.AuthViewModel

@Composable
fun AccountScreen(
    viewModel: AuthViewModel,
    onLoginClick: () -> Unit,
) {
    val state by viewModel.uiState.collectAsState()
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        when (val current = state) {
            is AuthUiState.LoggedIn -> {
                Text(current.user.name, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text(current.user.email, style = MaterialTheme.typography.bodyMedium)
                Spacer(Modifier.height(24.dp))
                OutlinedButton(onClick = viewModel::logout) { Text("Log Out") }
            }
            is AuthUiState.LoggedOut -> {
                Text("You're not logged in")
                Spacer(Modifier.height(16.dp))
                Button(onClick = onLoginClick) { Text("Log In / Sign Up") }
            }
            AuthUiState.Loading -> CircularProgressIndicator()
        }
    }
}
