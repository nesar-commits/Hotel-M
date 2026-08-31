package com.tastyhub.android.ui.screens.cart

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.tastyhub.android.cart.CartViewModel

@Composable
fun CartScreen(
    cartViewModel: CartViewModel,
    isLoggedIn: Boolean,
    isPlacingOrder: Boolean,
    orderError: String?,
    onBack: () -> Unit,
    onCheckout: () -> Unit,
    onLoginRequired: () -> Unit,
) {
    val items by cartViewModel.items.collectAsState()
    val restaurantName by cartViewModel.restaurantName.collectAsState()
    val total = items.sumOf { it.price * it.quantity }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Your Cart") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
            )
        },
    ) { padding ->
        if (items.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("Your cart is empty")
            }
            return@Scaffold
        }
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            restaurantName?.let {
                Text(it, style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(16.dp))
            }
            LazyColumn(
                modifier = Modifier.weight(1f),
                contentPadding = PaddingValues(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(items, key = { it.menuItemId }) { item ->
                    Column {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Column {
                                Text(item.name, fontWeight = FontWeight.SemiBold)
                                Text(
                                    "₹${"%.0f".format(item.price)} × ${item.quantity}",
                                    style = MaterialTheme.typography.bodySmall,
                                )
                            }
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                IconButton(onClick = { cartViewModel.decrementItem(item.menuItemId) }) { Text("−") }
                                Text("${item.quantity}")
                                IconButton(onClick = { cartViewModel.incrementItem(item.menuItemId) }) { Text("+") }
                            }
                        }
                        HorizontalDivider()
                    }
                }
            }
            orderError?.let {
                Text(it, color = MaterialTheme.colorScheme.error, modifier = Modifier.padding(horizontal = 16.dp))
            }
            Column(modifier = Modifier.padding(16.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Total", fontWeight = FontWeight.Bold)
                    Text("₹${"%.0f".format(total)}", fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(12.dp))
                Button(
                    onClick = { if (isLoggedIn) onCheckout() else onLoginRequired() },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isPlacingOrder,
                ) {
                    if (isPlacingOrder) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            color = MaterialTheme.colorScheme.onPrimary,
                        )
                    } else {
                        Text(if (isLoggedIn) "Place Order" else "Login to Checkout")
                    }
                }
            }
        }
    }
}
