// Android Release Build Signing Configuration
// This configuration supports dual-source credentials:
// 1. Environment variables (CI/CD priority)
// 2. gradle.properties (local development fallback)

signingConfigs {
    create("release") {
        // Priority: environment variables (CI/CD) > gradle.properties (local dev)
        val keystorePath = System.getenv("SIGNING_KEY_STORE_PATH")
            ?: project.findProperty("SIGNING_KEY_STORE_PATH")?.toString()
        val storePass = System.getenv("SIGNING_STORE_PASSWORD")
            ?: project.findProperty("SIGNING_STORE_PASSWORD")?.toString()
        val alias = System.getenv("SIGNING_KEY_ALIAS")
            ?: project.findProperty("SIGNING_KEY_ALIAS")?.toString()
        val keyPass = System.getenv("SIGNING_KEY_PASSWORD")
            ?: project.findProperty("SIGNING_KEY_PASSWORD")?.toString()

        if (keystorePath != null && storePass != null && alias != null && keyPass != null) {
            storeFile = file(keystorePath)
            storePassword = storePass
            keyAlias = alias
            keyPassword = keyPass
        }
    }
}

buildTypes {
    release {
        signingConfig = signingConfigs.getByName("release")
        isMinifyEnabled = true
        isShrinkResources = true
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
    }
}

// Validate signing config only when building release variants
tasks.matching { it.name.contains("Release") }.configureEach {
    doFirst {
        val releaseConfig = android.signingConfigs.getByName("release")
        if (releaseConfig.storeFile == null) {
            throw GradleException(
                """
                Release signing not configured!

                For CI/CD: Set environment variables:
                  - SIGNING_KEY_STORE_PATH
                  - SIGNING_STORE_PASSWORD
                  - SIGNING_KEY_ALIAS
                  - SIGNING_KEY_PASSWORD

                For local development: Add to ~/.gradle/gradle.properties:
                  SIGNING_KEY_STORE_PATH=/path/to/local-dev-release.jks
                  SIGNING_STORE_PASSWORD=your-password
                  SIGNING_KEY_ALIAS=local-dev
                  SIGNING_KEY_PASSWORD=your-password
                  
                See gradle.properties.template for more details.
                """.trimIndent()
            )
        }
    }
}
