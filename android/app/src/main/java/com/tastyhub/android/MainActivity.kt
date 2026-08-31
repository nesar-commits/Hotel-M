package com.tastyhub.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.tastyhub.android.ui.navigation.TastyHubNavHost
import com.tastyhub.android.ui.theme.TastyHubTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val container = (application as TastyHubApplication).container
        setContent {
            TastyHubTheme {
                TastyHubNavHost(container = container)
            }
        }
    }
}
