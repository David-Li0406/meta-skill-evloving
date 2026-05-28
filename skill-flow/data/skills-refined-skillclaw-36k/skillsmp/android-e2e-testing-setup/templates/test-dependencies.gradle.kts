// Android E2E Testing Dependencies
// Add these to your app/build.gradle.kts

android {
    // ... existing config ...
    
    defaultConfig {
        // ... existing config ...
        
        // Test instrumentation runner
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        
        // Optional: Enable test orchestrator for better test isolation
        // Uncomment if you want each test to run in a separate instrumentation instance
        // testInstrumentationRunnerArguments["clearPackageData"] = "true"
    }
    
    // Optional: Test orchestrator configuration
    // Uncomment if you enabled clearPackageData above
    testOptions {
        // execution = "ANDROIDX_TEST_ORCHESTRATOR"
        animationsDisabled = true  // Disable animations for faster, more reliable tests
        
        unitTests {
            isIncludeAndroidResources = true  // Enables Robolectric if needed
        }
    }
    
    // ... rest of config ...
}

dependencies {
    // ... existing dependencies ...
    
    // ============================================================
    // Espresso - UI Testing Framework
    // ============================================================
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-intents:3.5.1")
    
    // Optional: For testing web views
    // androidTestImplementation("androidx.test.espresso:espresso-web:3.5.1")
    
    // ============================================================
    // AndroidX Test - Core Testing Libraries
    // ============================================================
    androidTestImplementation("androidx.test:core:1.5.0")
    androidTestImplementation("androidx.test:core-ktx:1.5.0")
    androidTestImplementation("androidx.test:runner:1.5.2")
    androidTestImplementation("androidx.test:rules:1.5.0")
    
    // ============================================================
    // AndroidX Test - JUnit Integration
    // ============================================================
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.ext:junit-ktx:1.1.5")
    
    // ============================================================
    // Kotlin Coroutines Test Support (if using coroutines)
    // ============================================================
    androidTestImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    
    // ============================================================
    // Test Orchestrator (optional but recommended for large test suites)
    // Uncomment if you enabled execution = "ANDROIDX_TEST_ORCHESTRATOR" above
    // ============================================================
    // androidTestUtil("androidx.test:orchestrator:1.4.2")
    
    // ============================================================
    // Hamcrest Matchers (optional, for more readable assertions)
    // ============================================================
    androidTestImplementation("org.hamcrest:hamcrest:2.2")
    
    // ============================================================
    // Screenshot Testing (optional)
    // ============================================================
    androidTestImplementation("androidx.test:runner:1.5.2")  // Already included above
    
    // ============================================================
    // Jetpack Compose Testing (only if using Compose)
    // ============================================================
    // androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.5.4")
    // debugImplementation("androidx.compose.ui:ui-test-manifest:1.5.4")
    
    // ============================================================
    // UI Automator (for testing across multiple apps)
    // ============================================================
    // androidTestImplementation("androidx.test.uiautomator:uiautomator:2.2.0")
}
