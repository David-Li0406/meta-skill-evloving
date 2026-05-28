/**
 * Material 3 Expressive - Basic Setup Example
 *
 * MaterialExpressiveTheme を使用した基本的なアプリセットアップ例。
 */

package com.example.m3expressive

import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

// =============================================================================
// Activity
// =============================================================================

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            M3ExpressiveApp()
        }
    }
}

// =============================================================================
// Theme
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun M3ExpressiveTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    motionScheme: MotionScheme = MotionScheme.expressive(),
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> darkColorScheme()
        else -> lightColorScheme()
    }

    MaterialExpressiveTheme(
        colorScheme = colorScheme,
        motionScheme = motionScheme,
        content = content
    )
}

// =============================================================================
// App
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun M3ExpressiveApp() {
    M3ExpressiveTheme {
        Scaffold(
            modifier = Modifier.fillMaxSize(),
            floatingActionButton = {
                FloatingActionButton(
                    onClick = { /* action */ }
                ) {
                    Icon(
                        imageVector = Icons.Default.Add,
                        contentDescription = "Add"
                    )
                }
            }
        ) { innerPadding ->
            MainContent(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
            )
        }
    }
}

// =============================================================================
// Main Content
// =============================================================================

@Composable
fun MainContent(modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically)
        ) {
            Text(
                text = "Material 3 Expressive",
                style = MaterialTheme.typography.headlineLarge,
                color = MaterialTheme.colorScheme.onBackground
            )

            Text(
                text = "Spring-based animations enabled",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Button(
                onClick = { /* action */ }
            ) {
                Text("Expressive Button")
            }
        }
    }
}

// =============================================================================
// MotionScheme Options
// =============================================================================

/**
 * 異なる MotionScheme オプションのデモ
 */
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MotionSchemeDemo() {
    // Expressive: バウンス感のあるアニメーション（推奨）
    M3ExpressiveTheme(motionScheme = MotionScheme.expressive()) {
        // ヒーローモーメントや主要インタラクション向け
    }

    // Standard: 控えめなアニメーション
    M3ExpressiveTheme(motionScheme = MotionScheme.standard()) {
        // ユーティリティアプリやフォーマルなUI向け
    }
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(name = "Light Mode")
@Composable
private fun M3ExpressiveAppLightPreview() {
    M3ExpressiveTheme(darkTheme = false) {
        MainContent()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(name = "Dark Mode")
@Composable
private fun M3ExpressiveAppDarkPreview() {
    M3ExpressiveTheme(darkTheme = true) {
        MainContent()
    }
}

// =============================================================================
// Usage Notes
// =============================================================================

/*
依存関係（build.gradle.kts）:

dependencies {
    implementation("androidx.compose.material3:material3:1.4.0-alpha15")
    // または BOM を使用
    implementation(platform("androidx.compose:compose-bom:2024.12.01"))
    implementation("androidx.compose.material3:material3")
}

重要なポイント:
1. @OptIn(ExperimentalMaterial3ExpressiveApi::class) が必要
2. MotionScheme.expressive() がデフォルト推奨
3. Dynamic Color は Android 12+ で利用可能
4. enableEdgeToEdge() でエッジツーエッジ表示
*/
