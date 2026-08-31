package com.tastyhub.android.di

import android.content.Context
import com.tastyhub.android.BuildConfig
import com.tastyhub.android.data.TokenManager
import com.tastyhub.android.data.remote.AuthInterceptor
import com.tastyhub.android.data.remote.TastyHubApi
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory

/** Simple hand-rolled DI container, instantiated once in [com.tastyhub.android.TastyHubApplication]. */
class AppContainer(context: Context) {
    val tokenManager = TokenManager(context)

    private val json = Json {
        ignoreUnknownKeys = true
        explicitNulls = false
    }

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY else HttpLoggingInterceptor.Level.NONE
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(AuthInterceptor(tokenManager))
        .addInterceptor(loggingInterceptor)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    val api: TastyHubApi = retrofit.create(TastyHubApi::class.java)
}
