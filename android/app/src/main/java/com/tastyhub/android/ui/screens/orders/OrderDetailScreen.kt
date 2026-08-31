package com.tastyhub.android.ui.screens.orders

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

private val STATUS_FLOW = listOf("placed", "confirmed", "preparing", "ready", "out_for_delivery", "delivered")

@Composable
fun OrderDetailScreen(
    viewModel: OrderViewModel,
    orderId: Int,
    onBack: () -> Unit,
) {
    val order by viewModel.selectedOrder.collectAsState()

    DisposableEffect(orderId) {
        val job = viewModel.watchOrder(orderId)
        onDispose { job.cancel() }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Order #$orderId") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
            )
        },
    ) { padding ->
        val current = order
        if (current == null || current.id != orderId) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
            return@Scaffold
        }
        Column(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)) {
            Text(current.restaurantName, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(16.dp))

            if (current.status == "cancelled") {
                Text("Order cancelled", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.SemiBold)
            } else {
                val currentIndex = STATUS_FLOW.indexOf(current.status)
                STATUS_FLOW.forEachIndexed { index, status ->
                    val reached = index <= currentIndex
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 6.dp)) {
                        Box(
                            modifier = Modifier
                                .size(24.dp)
                                .background(
                                    if (reached) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                    shape = CircleShape,
                                ),
                            contentAlignment = Alignment.Center,
                        ) {
                            if (reached) {
                                Icon(
                                    Icons.Filled.Check,
                                    contentDescription = null,
                                    tint = Color.White,
                                    modifier = Modifier.size(14.dp),
                                )
                            }
                        }
                        Spacer(Modifier.width(12.dp))
                        Text(
                            status.replace('_', ' ').replaceFirstChar { it.uppercase() },
                            fontWeight = if (index == currentIndex) FontWeight.Bold else FontWeight.Normal,
                        )
                    }
                }
            }

            Spacer(Modifier.height(24.dp))
            Text("Items", fontWeight = FontWeight.SemiBold)
            LazyColumn(modifier = Modifier.weight(1f)) {
                items(current.items, key = { it.id }) { item ->
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Text("${item.menuItemName} × ${item.quantity}")
                        Text("₹${"%.0f".format(item.price * item.quantity)}")
                    }
                }
            }
            HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Total", fontWeight = FontWeight.Bold)
                Text("₹${"%.0f".format(current.totalAmount)}", fontWeight = FontWeight.Bold)
            }
        }
    }
}
