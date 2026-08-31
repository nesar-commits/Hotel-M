package com.tastyhub.android.ui.screens.orders

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.tastyhub.android.data.model.OrderOut

@Composable
fun OrdersScreen(
    viewModel: OrderViewModel,
    onOrderClick: (OrderOut) -> Unit,
) {
    val orders by viewModel.myOrders.collectAsState()
    val isLoading by viewModel.isLoadingOrders.collectAsState()

    LaunchedEffect(Unit) { viewModel.loadMyOrders() }

    Column(modifier = Modifier.fillMaxSize()) {
        Text(
            "Your Orders",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(16.dp),
        )
        when {
            isLoading && orders.isEmpty() -> {
                Box(Modifier.fillMaxWidth().weight(1f), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
            }
            orders.isEmpty() -> {
                Box(Modifier.fillMaxWidth().weight(1f), contentAlignment = Alignment.Center) { Text("No orders yet") }
            }
            else -> {
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    items(orders, key = { it.id }) { order ->
                        ElevatedCard(onClick = { onOrderClick(order) }, modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text(order.restaurantName, fontWeight = FontWeight.SemiBold)
                                Text(
                                    "Order #${order.id} · ${order.status.replace('_', ' ')}",
                                    style = MaterialTheme.typography.bodySmall,
                                )
                                Text("₹${"%.0f".format(order.totalAmount)}", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    }
                }
            }
        }
    }
}
