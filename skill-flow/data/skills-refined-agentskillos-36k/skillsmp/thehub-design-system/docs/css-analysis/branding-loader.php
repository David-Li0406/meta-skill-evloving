<?php
/**
 * BRANDING.JSON LOADER
 * Lägg till detta i components/head.php EFTER rad 72 (efter pwa.css)
 * 
 * Detta gör att ändringar i admin/branding.php faktiskt appliceras!
 */
?>

<!-- Custom Branding from admin/branding.php -->
<?php
// Path to branding config
$brandingFile = __DIR__ . '/../uploads/branding.json';

// Only load if file exists
if (file_exists($brandingFile)) {
    // Read and decode JSON
    $brandingData = json_decode(file_get_contents($brandingFile), true);
    
    // Check if we have custom colors
    if (!empty($brandingData['colors']) && is_array($brandingData['colors'])) {
        echo '<style id="custom-branding">';
        echo ':root {';
        
        // Output each custom CSS variable
        foreach ($brandingData['colors'] as $cssVar => $value) {
            // Sanitize variable name (should start with --)
            if (strpos($cssVar, '--') === 0) {
                // Sanitize value (basic XSS protection)
                $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                echo $cssVar . ':' . $safeValue . ';';
            }
        }
        
        echo '}';
        echo '</style>';
        
        // Optional: Add comment for debugging
        echo '<!-- Loaded ' . count($brandingData['colors']) . ' custom colors from branding.json -->';
    }
}
?>

<?php
/**
 * ALTERNATIV VERSION MED CACHING
 * Använd denna om branding.json är stor eller ändras sällan
 */
?>

<!-- Custom Branding with Caching -->
<?php
$brandingFile = __DIR__ . '/../uploads/branding.json';
$cacheKey = 'branding_css_' . md5($brandingFile);

// Try to get from cache (if you have a cache system)
// $cachedCSS = get_cache($cacheKey);

// if ($cachedCSS === false && file_exists($brandingFile)) {
if (file_exists($brandingFile)) {
    $brandingData = json_decode(file_get_contents($brandingFile), true);
    
    if (!empty($brandingData['colors']) && is_array($brandingData['colors'])) {
        $cssOutput = '<style id="custom-branding">:root{';
        
        foreach ($brandingData['colors'] as $cssVar => $value) {
            if (strpos($cssVar, '--') === 0) {
                $cssOutput .= $cssVar . ':' . htmlspecialchars($value, ENT_QUOTES, 'UTF-8') . ';';
            }
        }
        
        $cssOutput .= '}</style>';
        
        // Cache for 1 hour (if you have caching)
        // set_cache($cacheKey, $cssOutput, 3600);
        
        echo $cssOutput;
    }
}
?>

<?php
/**
 * VERSION 3: MED FILEMTIME CACHE BUSTING
 * Rekommenderad version - invaliderar cache när filen ändras
 */
?>

<!-- Custom Branding with Cache Busting -->
<?php
$brandingFile = __DIR__ . '/../uploads/branding.json';

if (file_exists($brandingFile)) {
    // Get file modification time for cache busting
    $fileModTime = filemtime($brandingFile);
    
    $brandingData = json_decode(file_get_contents($brandingFile), true);
    
    if (!empty($brandingData['colors']) && is_array($brandingData['colors'])) {
        echo '<style id="custom-branding" data-version="' . $fileModTime . '">';
        echo ':root{';
        
        foreach ($brandingData['colors'] as $cssVar => $value) {
            if (strpos($cssVar, '--') === 0) {
                $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                echo $cssVar . ':' . $safeValue . ';';
            }
        }
        
        echo '}</style>';
    }
}
?>

<?php
/**
 * TESTFIL: branding-test.json
 * Skapa denna fil i /uploads/ för att testa
 */

// Skapa uploads/branding-test.json med detta innehåll:
/*
{
  "colors": {
    "--color-accent": "#FF0000",
    "--color-accent-hover": "#CC0000",
    "--color-bg-card": "#2A0A0A",
    "--color-text-primary": "#FFB6C1"
  }
}
*/

// Ändra sedan $brandingFile till:
// $brandingFile = __DIR__ . '/../uploads/branding-test.json';

// Ladda om sidan och du bör se:
// - Röd accentfärg
// - Mörkröda kort
// - Rosa text
?>

<?php
/**
 * KOMPLETT IMPLEMENTATION FÖR components/head.php
 * 
 * Hitta rad 72 i components/head.php (efter pwa.css)
 * Lägg till detta block:
 */
?>

<!-- Dynamic Branding System -->
<?php
/**
 * Load custom colors from admin branding panel
 * File: /uploads/branding.json
 * Admin panel: /admin/branding.php
 */
$brandingFile = __DIR__ . '/../uploads/branding.json';

if (file_exists($brandingFile)) {
    $brandingData = json_decode(file_get_contents($brandingFile), true);
    
    // Validate and output custom CSS variables
    if (is_array($brandingData) && !empty($brandingData['colors'])) {
        $colorCount = 0;
        $cssOutput = '';
        
        foreach ($brandingData['colors'] as $cssVar => $value) {
            // Security: Only allow CSS custom properties (start with --)
            if (strpos($cssVar, '--') === 0) {
                // Security: Sanitize value
                $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                
                // Validate it's a reasonable CSS value (hex, rgb, rgba, hsl, etc.)
                if (preg_match('/^(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-z]+)$/', $value)) {
                    $cssOutput .= $cssVar . ':' . $safeValue . ';';
                    $colorCount++;
                }
            }
        }
        
        // Only output if we have valid colors
        if ($colorCount > 0) {
            echo '<style id="custom-branding" data-colors="' . $colorCount . '">';
            echo ':root{' . $cssOutput . '}';
            echo '</style>';
        }
    }
}
?>

<?php
/**
 * DEBUG VERSION
 * Lägg till detta TEMPORÄRT för att se vad som laddas
 */
?>

<!-- Branding Debug Info -->
<?php
$brandingFile = __DIR__ . '/../uploads/branding.json';

if (file_exists($brandingFile)) {
    $brandingData = json_decode(file_get_contents($brandingFile), true);
    
    echo '<!-- Branding Debug:';
    echo '
  File exists: YES';
    echo '
  File size: ' . filesize($brandingFile) . ' bytes';
    echo '
  Modified: ' . date('Y-m-d H:i:s', filemtime($brandingFile));
    
    if (is_array($brandingData)) {
        echo '
  Colors defined: ' . (isset($brandingData['colors']) ? count($brandingData['colors']) : 0);
        
        if (!empty($brandingData['colors'])) {
            echo '
  Colors:';
            foreach ($brandingData['colors'] as $var => $val) {
                echo '
    ' . $var . ' = ' . $val;
            }
        }
    }
    
    echo '
-->';
    
    // Normal loading continues here...
    if (!empty($brandingData['colors'])) {
        echo '<style id="custom-branding">:root{';
        foreach ($brandingData['colors'] as $cssVar => $value) {
            if (strpos($cssVar, '--') === 0) {
                echo $cssVar . ':' . htmlspecialchars($value) . ';';
            }
        }
        echo '}</style>';
    }
} else {
    echo '<!-- Branding file not found: ' . $brandingFile . ' -->';
}
?>

<?php
/**
 * TESTA ATT DET FUNGERAR
 * 
 * 1. Skapa uploads/branding.json manuellt:
 */
/*
{
  "colors": {
    "--color-accent": "#FF00FF"
  }
}
*/

/**
 * 2. Ladda om sidan
 * 
 * 3. Öppna DevTools → Elements → <head>
 * 
 * 4. Leta efter:
 *    <style id="custom-branding">:root{--color-accent:#FF00FF;}</style>
 * 
 * 5. Om du ser det → Det fungerar! ✅
 *    Om du inte ser det → Branding laddas inte ❌
 * 
 * 6. Testa också att ändra en knappfärg i admin/branding.php
 *    och se att den sparas och appliceras
 */
?>
