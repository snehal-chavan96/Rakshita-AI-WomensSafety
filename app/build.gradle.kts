plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.example.rakshika"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.rakshika"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        viewBinding = true
    }
}
dependencies {

    implementation(libs.appcompat)
    implementation(libs.material)
    implementation(libs.activity)
    implementation(libs.constraintlayout)
    implementation(libs.recyclerview)
    implementation(libs.lifecycle.livedata.ktx)
    implementation(libs.lifecycle.viewmodel.ktx)
    implementation(libs.navigation.fragment)
    implementation(libs.navigation.ui)
    implementation(libs.firebase.inappmessaging)

    testImplementation(libs.junit)
    androidTestImplementation(libs.ext.junit)
    androidTestImplementation(libs.espresso.core)


    // Google Maps SDK
    implementation("com.google.android.gms:play-services-maps:18.2.0")
    implementation("com.google.android.libraries.places:places:2.6.0")
    implementation("com.google.maps:google-maps-services:0.15.0")

    implementation("com.squareup.okhttp3:okhttp:4.12.0")

//    implementation("com.google.android.gms:play-services-maps:17.0.1")
//    implementation("com.google.android.libraries.places:places:2.7.0")
//    implementation("com.google.maps:google-maps-services:0.12.0")
}
