package com.tastyhub.android.ui.screens.restaurant

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
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.tastyhub.android.cart.CartViewModel
import com.tastyhub.android.data.model.MenuItemOut

@Composable
fun RestaurantMenuScreen(
    viewModel: RestaurantMenuViewModel,
    cartViewModel: CartViewModel,
    onBack: () -> Unit,
    onGoToCart: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsState()
    val cartItems by cartViewModel.items.collectAsState()
    var conflictDialogItem by remember { mutableStateOf<MenuItemOut?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(uiState.restaurant?.name ?: "Menu") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
            )
        },
        bottomBar = {
            if (cartItems.isNotEmpty()) {
                val total = cartItems.sumOf { it.price * it.quantity }
                val count = cartItems.sumOf { it.quantity }
                Surface(shadowElevation = 8.dp) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Text("$count item(s) · ₹${"%.0f".format(total)}", fontWeight = FontWeight.SemiBold)
                        Button(onClick = onGoToCart) { Text("View Cart") }
                    }
                }
            }
        },
    ) { padding ->
        when {
            uiState.isLoading -> {
                Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }
            uiState.error != null -> {
                Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(uiState.error ?: "")
                        Spacer(Modifier.height(8.dp))
                        Button(onClick = viewModel::load) { Text("Retry") }
                    }
                }
            }
            uiState.restaurant != null -> {
                val restaurant = uiState.restaurant!!
                val filteredItems = restaurant.menuItems.filter { item ->
                    (!uiState.vegOnly || item.isVeg) &&
                        (uiState.selectedCategoryId == null || item.categoryId == uiState.selectedCategoryId) &&
                        (uiState.searchQuery.isBlank() || item.name.contains(uiState.searchQuery, ignoreCase = true))
                }
                Column(modifier = Modifier.fillMaxSize().padding(padding)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(restaurant.cuisineType, style = MaterialTheme.typography.bodyMedium)
                        Text("${restaurant.address} · ${restaurant.city}", style = MaterialTheme.typography.bodySmall)
                        Spacer(Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            FilterChip(
                                selected = uiState.vegOnly,
                                onClick = viewModel::toggleVegOnly,
                                label = { Text("Veg only") },
                            )
                            Spacer(Modifier.width(8.dp))
                            FilterChip(
                                selected = uiState.selectedCategoryId == null,
                                onClick = { viewModel.selectCategory(null) },
                                label = { Text("All") },
                            )
                        }
                        Spacer(Modifier.height(8.dp))
                        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            items(restaurant.categories.sortedBy { it.sortOrder }, key = { it.id }) { category ->
                                FilterChip(
                                    selected = uiState.selectedCategoryId == category.id,
                                    onClick = { viewModel.selectCategory(category.id) },
                                    label = { Text(category.name) },
                                )
                            }
                        }
                        Spacer(Modifier.height(8.dp))
                        OutlinedTextField(
                            value = uiState.searchQuery,
                            onValueChange = viewModel::onSearchChange,
                            placeholder = { Text("Search dishes") },
                            singleLine = true,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                    LazyColumn(
                        modifier = Modifier.weight(1f),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        items(filteredItems, key = { it.id }) { item ->
                            val cartQuantity = cartItems.find { it.menuItemId == item.id }?.quantity ?: 0
                            MenuItemRow(
                                item = item,
                                quantity = cartQuantity,
                                onAdd = {
                                    if (cartViewModel.wouldConflict(restaurant.id)) {
                                        conflictDialogItem = item
                                    } else {
                                        cartViewModel.addItem(item, restaurant.id, restaurant.name)
                                    }
                                },
                                onRemove = { cartViewModel.decrementItem(item.id) },
                            )
                        }
                    }
                }
            }
        }
    }

    conflictDialogItem?.let { item ->
        val restaurant = uiState.restaurant
        AlertDialog(
            onDismissRequest = { conflictDialogItem = null },
            title = { Text("Start a new cart?") },
            text = { Text("Your cart has items from another restaurant. Clear it and add this item instead?") },
            confirmButton = {
                TextButton(onClick = {
                    if (restaurant != null) {
                        cartViewModel.replaceCartWith(item, restaurant.id, restaurant.name)
                    }
                    conflictDialogItem = null
                }) { Text("Clear & Add") }
            },
            dismissButton = {
                TextButton(onClick = { conflictDialogItem = null }) { Text("Cancel") }
            },
        )
    }
}

@Composable
private fun MenuItemRow(
    item: MenuItemOut,
    quantity: Int,
    onAdd: () -> Unit,
    onRemove: () -> Unit,
) {
    ElevatedCard(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(item.name, fontWeight = FontWeight.SemiBold)
                if (item.description.isNotBlank()) {
                    Text(item.description, style = MaterialTheme.typography.bodySmall, maxLines = 2)
                }
                Text("₹${"%.0f".format(item.price)}", style = MaterialTheme.typography.bodyMedium)
            }
            Spacer(Modifier.width(12.dp))
            if (quantity == 0) {
                OutlinedButton(onClick = onAdd, enabled = item.isAvailable) { Text("ADD") }
            } else {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onRemove) { Text("−") }
                    Text("$quantity")
                    IconButton(onClick = onAdd) { Text("+") }
                }
            }
        }
    }
}
