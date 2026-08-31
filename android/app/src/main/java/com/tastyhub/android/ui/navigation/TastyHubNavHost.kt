package com.tastyhub.android.ui.navigation

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Receipt
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.Badge
import androidx.compose.material3.BadgedBox
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.tastyhub.android.auth.AuthUiState
import com.tastyhub.android.auth.AuthViewModel
import com.tastyhub.android.auth.AuthViewModelFactory
import com.tastyhub.android.cart.CartViewModel
import com.tastyhub.android.data.model.OrderItemCreate
import com.tastyhub.android.di.AppContainer
import com.tastyhub.android.ui.screens.account.AccountScreen
import com.tastyhub.android.ui.screens.auth.LoginScreen
import com.tastyhub.android.ui.screens.auth.SignupScreen
import com.tastyhub.android.ui.screens.cart.CartScreen
import com.tastyhub.android.ui.screens.home.HomeScreen
import com.tastyhub.android.ui.screens.home.HomeViewModel
import com.tastyhub.android.ui.screens.home.HomeViewModelFactory
import com.tastyhub.android.ui.screens.orders.OrderDetailScreen
import com.tastyhub.android.ui.screens.orders.OrderViewModel
import com.tastyhub.android.ui.screens.orders.OrderViewModelFactory
import com.tastyhub.android.ui.screens.orders.OrdersScreen
import com.tastyhub.android.ui.screens.restaurant.RestaurantMenuScreen
import com.tastyhub.android.ui.screens.restaurant.RestaurantMenuViewModel
import com.tastyhub.android.ui.screens.restaurant.RestaurantMenuViewModelFactory

private object Routes {
    const val HOME = "home"
    const val RESTAURANT = "restaurant/{restaurantId}"
    const val CART = "cart"
    const val LOGIN = "login"
    const val SIGNUP = "signup"
    const val ORDERS = "orders"
    const val ORDER_DETAIL = "order/{orderId}"
    const val ACCOUNT = "account"
}

private fun restaurantRoute(id: Int) = "restaurant/$id"
private fun orderDetailRoute(id: Int) = "order/$id"

private data class BottomDestination(val route: String, val label: String, val icon: ImageVector)

private val BOTTOM_DESTINATIONS = listOf(
    BottomDestination(Routes.HOME, "Home", Icons.Filled.Home),
    BottomDestination(Routes.ORDERS, "Orders", Icons.Filled.Receipt),
    BottomDestination(Routes.CART, "Cart", Icons.Filled.ShoppingCart),
    BottomDestination(Routes.ACCOUNT, "Account", Icons.Filled.Person),
)

@Composable
fun TastyHubNavHost(container: AppContainer) {
    val navController = rememberNavController()
    val authViewModel: AuthViewModel = viewModel(factory = AuthViewModelFactory(container.api, container.tokenManager))
    val cartViewModel: CartViewModel = viewModel()
    val orderViewModel: OrderViewModel = viewModel(factory = OrderViewModelFactory(container.api))

    val authState by authViewModel.uiState.collectAsState()
    val cartItems by cartViewModel.items.collectAsState()
    val cartCount = cartItems.sumOf { it.quantity }

    Scaffold(
        bottomBar = {
            val backStackEntry by navController.currentBackStackEntryAsState()
            val currentRoute = backStackEntry?.destination?.route
            if (BOTTOM_DESTINATIONS.any { it.route == currentRoute }) {
                NavigationBar {
                    BOTTOM_DESTINATIONS.forEach { dest ->
                        NavigationBarItem(
                            selected = currentRoute == dest.route,
                            onClick = {
                                navController.navigate(dest.route) {
                                    popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            icon = {
                                if (dest.route == Routes.CART && cartCount > 0) {
                                    BadgedBox(badge = { Badge { Text("$cartCount") } }) {
                                        Icon(dest.icon, contentDescription = dest.label)
                                    }
                                } else {
                                    Icon(dest.icon, contentDescription = dest.label)
                                }
                            },
                            label = { Text(dest.label) },
                        )
                    }
                }
            }
        },
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Routes.HOME,
            modifier = Modifier.padding(padding),
        ) {
            composable(Routes.HOME) {
                val homeViewModel: HomeViewModel = viewModel(factory = HomeViewModelFactory(container.api))
                HomeScreen(
                    viewModel = homeViewModel,
                    onRestaurantClick = { navController.navigate(restaurantRoute(it.id)) },
                )
            }
            composable(
                Routes.RESTAURANT,
                arguments = listOf(navArgument("restaurantId") { type = NavType.IntType }),
            ) { backStackEntry ->
                val restaurantId = backStackEntry.arguments?.getInt("restaurantId") ?: return@composable
                val menuViewModel: RestaurantMenuViewModel = viewModel(
                    key = "restaurant_$restaurantId",
                    factory = RestaurantMenuViewModelFactory(container.api, restaurantId),
                )
                RestaurantMenuScreen(
                    viewModel = menuViewModel,
                    cartViewModel = cartViewModel,
                    onBack = { navController.popBackStack() },
                    onGoToCart = { navController.navigate(Routes.CART) },
                )
            }
            composable(Routes.CART) {
                val isPlacingOrder by orderViewModel.isPlacingOrder.collectAsState()
                val placeOrderError by orderViewModel.placeOrderError.collectAsState()
                CartScreen(
                    cartViewModel = cartViewModel,
                    isLoggedIn = authState is AuthUiState.LoggedIn,
                    isPlacingOrder = isPlacingOrder,
                    orderError = placeOrderError,
                    onBack = { navController.popBackStack() },
                    onCheckout = {
                        val restaurantId = cartViewModel.restaurantId.value
                        if (restaurantId != null) {
                            val items = cartItems.map { OrderItemCreate(it.menuItemId, it.quantity) }
                            orderViewModel.placeOrder(restaurantId, items) { order ->
                                cartViewModel.clearCart()
                                navController.navigate(orderDetailRoute(order.id)) {
                                    popUpTo(Routes.HOME)
                                }
                            }
                        }
                    },
                    onLoginRequired = { navController.navigate(Routes.LOGIN) },
                )
            }
            composable(Routes.LOGIN) {
                LoginScreen(
                    viewModel = authViewModel,
                    onLoggedIn = { navController.popBackStack() },
                    onGoToSignup = { navController.navigate(Routes.SIGNUP) },
                )
            }
            composable(Routes.SIGNUP) {
                SignupScreen(
                    viewModel = authViewModel,
                    onSignedUp = { navController.popBackStack() },
                    onGoToLogin = { navController.popBackStack() },
                )
            }
            composable(Routes.ORDERS) {
                when (authState) {
                    is AuthUiState.LoggedIn -> OrdersScreen(
                        viewModel = orderViewModel,
                        onOrderClick = { navController.navigate(orderDetailRoute(it.id)) },
                    )
                    else -> LoginPrompt(onLogin = { navController.navigate(Routes.LOGIN) })
                }
            }
            composable(
                Routes.ORDER_DETAIL,
                arguments = listOf(navArgument("orderId") { type = NavType.IntType }),
            ) { backStackEntry ->
                val orderId = backStackEntry.arguments?.getInt("orderId") ?: return@composable
                OrderDetailScreen(
                    viewModel = orderViewModel,
                    orderId = orderId,
                    onBack = { navController.popBackStack() },
                )
            }
            composable(Routes.ACCOUNT) {
                AccountScreen(
                    viewModel = authViewModel,
                    onLoginClick = { navController.navigate(Routes.LOGIN) },
                )
            }
        }
    }
}

@Composable
private fun LoginPrompt(onLogin: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Spacer(Modifier.height(120.dp))
        Text("Log in to see your orders")
        Spacer(Modifier.height(12.dp))
        Button(onClick = onLogin) { Text("Log In") }
    }
}
