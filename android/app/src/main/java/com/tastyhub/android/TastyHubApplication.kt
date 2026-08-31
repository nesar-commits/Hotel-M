package com.tastyhub.android

import android.app.Application
import com.tastyhub.android.di.AppContainer

class TastyHubApplication : Application() {
    lateinit var container: AppContainer
        private set

    override fun onCreate() {
        super.onCreate()
        container = AppContainer(this)
    }
}
