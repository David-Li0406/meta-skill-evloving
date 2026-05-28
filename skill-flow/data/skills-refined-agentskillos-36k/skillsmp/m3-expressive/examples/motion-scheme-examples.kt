/**
 * Material 3 Expressive - Motion Scheme Examples
 *
 * MotionScheme の使用例とカスタマイズ方法のデモ。
 */

package com.example.m3expressive.examples

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.LocalMotionScheme
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import kotlin.math.roundToInt

// =============================================================================
// Expressive vs Standard Comparison
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MotionSchemeComparisonDemo() {
    var useExpressive by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Motion Scheme: ${if (useExpressive) "Expressive" else "Standard"}",
            style = MaterialTheme.typography.headlineSmall
        )

        Spacer(modifier = Modifier.height(16.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { useExpressive = true }) {
                Text("Expressive")
            }
            Button(onClick = { useExpressive = false }) {
                Text("Standard")
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Apply different motion schemes
        MaterialExpressiveTheme(
            motionScheme = if (useExpressive) MotionScheme.expressive() else MotionScheme.standard()
        ) {
            AnimatedCard()
        }
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun AnimatedCard() {
    var isExpanded by remember { mutableStateOf(false) }
    val motionScheme = LocalMotionScheme.current

    // Spatial animation for size
    val size by animateDpAsState(
        targetValue = if (isExpanded) 200.dp else 100.dp,
        animationSpec = motionScheme.defaultSpatialSpec(),
        label = "size"
    )

    // Effects animation for color
    val backgroundColor by animateColorAsState(
        targetValue = if (isExpanded)
            MaterialTheme.colorScheme.primaryContainer
        else
            MaterialTheme.colorScheme.surfaceVariant,
        animationSpec = motionScheme.defaultEffectsSpec(),
        label = "color"
    )

    Card(
        modifier = Modifier
            .size(size)
            .clickable { isExpanded = !isExpanded },
        colors = androidx.compose.material3.CardDefaults.cardColors(
            containerColor = backgroundColor
        )
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = if (isExpanded) "Expanded" else "Tap me",
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
}

// =============================================================================
// Spatial vs Effects Animation
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SpatialVsEffectsDemo() {
    val motionScheme = LocalMotionScheme.current
    var isActive by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        Text(
            text = "Spatial vs Effects Animation",
            style = MaterialTheme.typography.titleLarge
        )

        Button(onClick = { isActive = !isActive }) {
            Text("Toggle Animation")
        }

        // Spatial Animation Example
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("Spatial (Size/Position)", style = MaterialTheme.typography.labelMedium)

            val size by animateDpAsState(
                targetValue = if (isActive) 120.dp else 80.dp,
                animationSpec = motionScheme.defaultSpatialSpec(),
                label = "spatialSize"
            )

            Box(
                modifier = Modifier
                    .size(size)
                    .background(
                        MaterialTheme.colorScheme.primary,
                        RoundedCornerShape(16.dp)
                    )
            )
        }

        // Effects Animation Example
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("Effects (Color/Alpha)", style = MaterialTheme.typography.labelMedium)

            val color by animateColorAsState(
                targetValue = if (isActive)
                    MaterialTheme.colorScheme.tertiary
                else
                    MaterialTheme.colorScheme.secondary,
                animationSpec = motionScheme.defaultEffectsSpec(),
                label = "effectsColor"
            )

            Box(
                modifier = Modifier
                    .size(80.dp)
                    .background(color, RoundedCornerShape(16.dp))
            )
        }
    }
}

// =============================================================================
// Spring Speed Comparison
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SpringSpeedDemo() {
    val motionScheme = LocalMotionScheme.current
    var isActive by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Spring Speeds",
            style = MaterialTheme.typography.titleLarge
        )

        Button(onClick = { isActive = !isActive }) {
            Text("Animate All")
        }

        // Fast Spring (small components)
        SpringSpeedItem(
            label = "Fast (Small components)",
            isActive = isActive,
            animationSpec = motionScheme.fastSpatialSpec()
        )

        // Default Spring (medium components)
        SpringSpeedItem(
            label = "Default (Medium components)",
            isActive = isActive,
            animationSpec = motionScheme.defaultSpatialSpec()
        )

        // Slow Spring (large components/screens)
        SpringSpeedItem(
            label = "Slow (Large/Screen transitions)",
            isActive = isActive,
            animationSpec = motionScheme.slowSpatialSpec()
        )
    }
}

@Composable
private fun <T> SpringSpeedItem(
    label: String,
    isActive: Boolean,
    animationSpec: androidx.compose.animation.core.AnimationSpec<Float>
) {
    val offset by animateFloatAsState(
        targetValue = if (isActive) 100f else 0f,
        animationSpec = animationSpec,
        label = label
    )

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.Start
    ) {
        Text(label, style = MaterialTheme.typography.labelSmall)

        Box(
            modifier = Modifier
                .offset { IntOffset(offset.roundToInt(), 0) }
                .size(48.dp)
                .background(
                    MaterialTheme.colorScheme.primary,
                    RoundedCornerShape(8.dp)
                )
        )
    }
}

// =============================================================================
// Custom Spring Configuration
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CustomSpringDemo() {
    var isActive by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Custom Spring Configurations",
            style = MaterialTheme.typography.titleLarge
        )

        Button(onClick = { isActive = !isActive }) {
            Text("Animate")
        }

        // High Bounce
        CustomSpringItem(
            label = "High Bounce (DampingRatio: 0.2)",
            isActive = isActive,
            stiffness = Spring.StiffnessMedium,
            dampingRatio = Spring.DampingRatioHighBouncy
        )

        // Medium Bounce
        CustomSpringItem(
            label = "Medium Bounce (DampingRatio: 0.5)",
            isActive = isActive,
            stiffness = Spring.StiffnessMedium,
            dampingRatio = Spring.DampingRatioMediumBouncy
        )

        // No Bounce
        CustomSpringItem(
            label = "No Bounce (DampingRatio: 1.0)",
            isActive = isActive,
            stiffness = Spring.StiffnessMedium,
            dampingRatio = Spring.DampingRatioNoBouncy
        )

        // High Stiffness
        CustomSpringItem(
            label = "High Stiffness (Fast)",
            isActive = isActive,
            stiffness = Spring.StiffnessHigh,
            dampingRatio = Spring.DampingRatioMediumBouncy
        )

        // Low Stiffness
        CustomSpringItem(
            label = "Low Stiffness (Slow)",
            isActive = isActive,
            stiffness = Spring.StiffnessLow,
            dampingRatio = Spring.DampingRatioMediumBouncy
        )
    }
}

@Composable
private fun CustomSpringItem(
    label: String,
    isActive: Boolean,
    stiffness: Float,
    dampingRatio: Float
) {
    val scale by animateFloatAsState(
        targetValue = if (isActive) 1.5f else 1f,
        animationSpec = spring(
            stiffness = stiffness,
            dampingRatio = dampingRatio
        ),
        label = label
    )

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.Start
    ) {
        Text(label, style = MaterialTheme.typography.labelSmall)

        Box(
            modifier = Modifier
                .scale(scale)
                .size(40.dp)
                .background(
                    MaterialTheme.colorScheme.tertiary,
                    RoundedCornerShape(8.dp)
                )
        )
    }
}

// =============================================================================
// Interruptible Animation Demo
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun InterruptibleAnimationDemo() {
    val motionScheme = LocalMotionScheme.current
    var targetIndex by remember { mutableStateOf(0) }
    val positions = listOf(0f, 100f, 200f, 50f)

    val offset by animateFloatAsState(
        targetValue = positions[targetIndex],
        animationSpec = motionScheme.defaultSpatialSpec(),
        label = "interruptible"
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Interruptible Animation",
            style = MaterialTheme.typography.titleLarge
        )

        Text(
            text = "Tap buttons rapidly to see interruption",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            positions.forEachIndexed { index, _ ->
                Button(onClick = { targetIndex = index }) {
                    Text("Pos ${index + 1}")
                }
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(60.dp)
        ) {
            Box(
                modifier = Modifier
                    .offset { IntOffset(offset.roundToInt(), 0) }
                    .size(48.dp)
                    .background(
                        MaterialTheme.colorScheme.primary,
                        RoundedCornerShape(24.dp)
                    )
            )
        }
    }
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun MotionSchemeComparisonPreview() {
    MaterialExpressiveTheme {
        MotionSchemeComparisonDemo()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun SpatialVsEffectsPreview() {
    MaterialExpressiveTheme {
        SpatialVsEffectsDemo()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun SpringSpeedPreview() {
    MaterialExpressiveTheme {
        SpringSpeedDemo()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun CustomSpringPreview() {
    MaterialExpressiveTheme {
        CustomSpringDemo()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun InterruptibleAnimationPreview() {
    MaterialExpressiveTheme {
        InterruptibleAnimationDemo()
    }
}
