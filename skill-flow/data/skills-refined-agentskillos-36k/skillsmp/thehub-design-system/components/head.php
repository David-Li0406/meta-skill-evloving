<?php
$pageTitle = ucfirst($pageInfo['page'] ?? 'Dashboard') . ' – TheHUB';
$currentTheme = 'light'; // Unified theme - dark mode disabled
$themeColor = '#F9F9F9'; // Unified background color for all themes
$hubUrl = defined('HUB_URL') ? HUB_URL : '';

// Fallback for hub_asset if not defined
if (!function_exists('hub_asset')) {
    function hub_asset($path) {
        return '/assets/' . ltrim($path, '/');
    }
}
?>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, user-scalable=no">
<meta name="description" content="TheHUB – Sveriges plattform för gravity cycling">

<!-- CRITICAL: Theme & FOUC Prevention - must be FIRST -->
<script>
(function() {
    // Detect saved theme preference immediately (before CSS loads)
    var theme = 'dark'; // Default
    try {
        var saved = localStorage.getItem('thehub-theme');
        if (saved) theme = saved;
        else {
            var cookie = document.cookie.match(/(^| )hub_theme=([^;]+)/);
            if (cookie) theme = cookie[2];
        }
    } catch(e) {}

    // Resolve 'auto' to actual theme
    if (theme === 'auto') {
        theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Apply immediately to prevent flash
    document.documentElement.setAttribute('data-theme', theme);
})();
</script>
<style>
    /* Hide content until CSS is ready */
    .main-content { opacity: 0; }
    .main-content.css-ready { opacity: 1; transition: opacity 0.1s ease-out; }
    /* Fallback: show after 300ms if JS fails */
    @keyframes fouc-fallback { to { opacity: 1; } }
    .main-content { animation: fouc-fallback 0.1s ease-out 0.3s forwards; }
    /* Prevent layout shift - unified background for all themes (must match theme.css) */
    html, body { margin: 0; padding: 0; background: #F9F9F9; }
</style>

<!-- PWA Meta Tags -->
<meta name="application-name" content="TheHUB">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="<?= $themeColor ?>" id="theme-color-meta">

<!-- iOS PWA Meta Tags (Apple specific) -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="TheHUB">

<!-- iOS Icons -->
<?php
// iOS requires PNG format - use branding favicon if set
// Note: We read branding once here, then reuse for regular favicon below
$appleTouchIcon = '/assets/favicon.svg'; // Default
$brandingJsonFileApple = __DIR__ . '/../uploads/branding.json';
$brandingDataForIcons = null;
if (file_exists($brandingJsonFileApple)) {
    $brandingDataForIcons = json_decode(file_get_contents($brandingJsonFileApple), true);
    if (!empty($brandingDataForIcons['logos']['favicon'])) {
        $appleTouchIcon = $brandingDataForIcons['logos']['favicon'];
    }
}
?>
<link rel="apple-touch-icon" href="<?= htmlspecialchars($appleTouchIcon) ?>">
<link rel="apple-touch-icon" sizes="180x180" href="<?= htmlspecialchars($appleTouchIcon) ?>">
<link rel="apple-touch-icon" sizes="167x167" href="<?= htmlspecialchars($appleTouchIcon) ?>">

<!-- Web App Manifest -->
<link rel="manifest" href="<?= $hubUrl ?>/manifest.json">

<!-- Favicon -->
<?php
// Reuse branding data from iOS icons section above (already read)
$faviconPath = $appleTouchIcon; // Same as apple-touch-icon, already loaded from branding
// Determine icon type based on file extension
$faviconExt = strtolower(pathinfo($faviconPath, PATHINFO_EXTENSION));
$iconType = match($faviconExt) {
    'svg' => 'image/svg+xml',
    'ico' => 'image/x-icon',
    'png' => 'image/png',
    'gif' => 'image/gif',
    'jpg', 'jpeg' => 'image/jpeg',
    'webp' => 'image/webp',
    default => 'image/png'
};
?>
<link rel="icon" type="<?= $iconType ?>" sizes="32x32" href="<?= htmlspecialchars($faviconPath) ?>">
<link rel="icon" type="<?= $iconType ?>" sizes="16x16" href="<?= htmlspecialchars($faviconPath) ?>">
<link rel="icon" type="<?= $iconType ?>" href="<?= htmlspecialchars($faviconPath) ?>">

<!-- Preconnect & Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cabin+Condensed:wght@400;500;600;700&family=Manrope:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

<!-- Lucide Icons - pinned to specific version for stability -->
<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>

<!-- Chart.js for dynamic charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<title><?= htmlspecialchars($pageTitle) ?></title>

<!-- CSS with cache busting (filemtime) -->
<?php
$cssDir = __DIR__ . '/../assets/css/';
$cssVersion = function($file) use ($cssDir) {
    $path = $cssDir . $file;
    return file_exists($path) ? filemtime($path) : time();
};
?>
<link rel="stylesheet" href="<?= hub_asset('css/reset.css') ?>?v=<?= $cssVersion('reset.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/tokens.css') ?>?v=<?= $cssVersion('tokens.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/theme.css') ?>?v=<?= $cssVersion('theme.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/effects.css') ?>?v=<?= $cssVersion('effects.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/layout.css') ?>?v=<?= $cssVersion('layout.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/components.css') ?>?v=<?= $cssVersion('components.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/tables.css') ?>?v=<?= $cssVersion('tables.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/utilities.css') ?>?v=<?= $cssVersion('utilities.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/badge-system.css') ?>?v=<?= $cssVersion('badge-system.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/pwa.css') ?>?v=<?= $cssVersion('pwa.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/viewport.css') ?>?v=<?= $cssVersion('viewport.css') ?>">
<link rel="stylesheet" href="<?= hub_asset('css/theme-enhancement.css') ?>?v=<?= $cssVersion('theme-enhancement.css') ?>">

<!-- Page-Specific CSS (loaded conditionally based on current page) -->
<?php
/**
 * Conditional Page CSS Loader
 *
 * Loads page-specific CSS from /assets/css/pages/ if it exists.
 * This allows gradual migration of inline styles to external files.
 *
 * Naming convention (from router.php):
 *   - Section routes use: {section}-{subpage}.css
 *   - Examples:
 *     /results        -> results-index.css
 *     /results/123    -> results-event.css
 *     /calendar       -> calendar-index.css
 *     /calendar/123   -> calendar-event.css
 *     /database/rider -> database-rider.css
 *     /profile/edit   -> profile-edit.css
 *   - Legacy single pages use: {page}.css
 *     /event/123      -> event.css
 *     /rider/123      -> rider.css
 */
$currentPage = $pageInfo['page'] ?? null;
$pageCssDir = __DIR__ . '/../assets/css/pages/';

if ($currentPage) {
    // Sanitize page name (only allow alphanumeric and hyphens)
    $safePage = preg_replace('/[^a-z0-9\-]/', '', strtolower($currentPage));
    $pageCssFile = $pageCssDir . $safePage . '.css';

    if (file_exists($pageCssFile)) {
        $pageCssVersion = filemtime($pageCssFile);
        echo '<link rel="stylesheet" href="' . hub_asset('css/pages/' . $safePage . '.css') . '?v=' . $pageCssVersion . '">' . "\n";
    }
}
?>

<!-- Dynamic Branding System -->
<?php
/**
 * Load custom colors and responsive settings from admin branding panel
 * File: /uploads/branding.json
 * Admin panel: /admin/branding.php
 */
$brandingFile = __DIR__ . '/../uploads/branding.json';

if (file_exists($brandingFile)) {
    $brandingData = json_decode(file_get_contents($brandingFile), true);

    if (is_array($brandingData)) {
        $cssOutput = '';
        $colorCount = 0;

        // Process custom colors - supports both old flat format and new dark/light format
        $darkColorsCss = '';
        $lightColorsCss = '';

        if (!empty($brandingData['colors'])) {
            $colors = $brandingData['colors'];

            // Check if using new dual-theme format
            if (isset($colors['dark']) || isset($colors['light'])) {
                // New format: colors.dark and colors.light
                if (!empty($colors['dark']) && is_array($colors['dark'])) {
                    foreach ($colors['dark'] as $cssVar => $value) {
                        if (strpos($cssVar, '--') === 0) {
                            $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                            if (preg_match('/^(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-z]+)$/', $value)) {
                                $darkColorsCss .= $cssVar . ':' . $safeValue . ';';
                                $colorCount++;
                            }
                        }
                    }
                }
                if (!empty($colors['light']) && is_array($colors['light'])) {
                    foreach ($colors['light'] as $cssVar => $value) {
                        if (strpos($cssVar, '--') === 0) {
                            $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                            if (preg_match('/^(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-z]+)$/', $value)) {
                                $lightColorsCss .= $cssVar . ':' . $safeValue . ';';
                                $colorCount++;
                            }
                        }
                    }
                }
            } else {
                // Legacy flat format - treat as dark theme colors
                foreach ($colors as $cssVar => $value) {
                    if (strpos($cssVar, '--') === 0) {
                        $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                        if (preg_match('/^(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-z]+)$/', $value)) {
                            $darkColorsCss .= $cssVar . ':' . $safeValue . ';';
                            $colorCount++;
                        }
                    }
                }
            }
        }

        // Process responsive layout settings
        $responsive = $brandingData['responsive'] ?? null;
        $responsiveCss = '';

        if ($responsive) {
            // Desktop defaults (1024px+) - set in :root
            $desktopPadding = intval($responsive['desktop']['padding'] ?? 32);
            $desktopRadius = intval($responsive['desktop']['radius'] ?? 12);

            // Desktop spacing tokens (derived from padding)
            $desktopCardPadding = $desktopPadding;  // Same as container - controlled by branding
            $desktopSpaceMd = 16;  // Standard
            $desktopSpaceSm = 12;
            $desktopSpaceLg = 24;

            $cssOutput .= '--container-padding:' . $desktopPadding . 'px;';
            $cssOutput .= '--card-padding:' . $desktopCardPadding . 'px;';
            $cssOutput .= '--content-padding:' . $desktopCardPadding . 'px;';
            $cssOutput .= '--table-cell-padding-y:' . $desktopSpaceSm . 'px;';
            $cssOutput .= '--table-cell-padding-x:' . $desktopSpaceMd . 'px;';
            $cssOutput .= '--radius-sm:' . $desktopRadius . 'px;';
            $cssOutput .= '--radius-md:' . $desktopRadius . 'px;';
            $cssOutput .= '--radius-lg:' . $desktopRadius . 'px;';
            $cssOutput .= '--radius-xl:' . $desktopRadius . 'px;';

            // Tablet / Landscape (768-1023px)
            $tabletPadding = intval($responsive['tablet']['padding'] ?? 24);
            $tabletRadius = intval($responsive['tablet']['radius'] ?? 8);
            $tabletCardPadding = $tabletPadding;  // Same as container - controlled by branding
            $tabletSpaceSm = 10;
            $tabletSpaceMd = 14;

            $responsiveCss .= '@media (min-width:768px) and (max-width:1023px){';
            $responsiveCss .= ':root{';
            $responsiveCss .= '--container-padding:' . $tabletPadding . 'px;';
            $responsiveCss .= '--card-padding:' . $tabletCardPadding . 'px;';
            $responsiveCss .= '--content-padding:' . $tabletCardPadding . 'px;';
            $responsiveCss .= '--table-cell-padding-y:' . $tabletSpaceSm . 'px;';
            $responsiveCss .= '--table-cell-padding-x:' . $tabletSpaceMd . 'px;';
            $responsiveCss .= '--radius-sm:' . $tabletRadius . 'px;';
            $responsiveCss .= '--radius-md:' . $tabletRadius . 'px;';
            $responsiveCss .= '--radius-lg:' . $tabletRadius . 'px;';
            $responsiveCss .= '--radius-xl:' . $tabletRadius . 'px;';
            $responsiveCss .= '}}';

            // Mobile Portrait (0-767px)
            $mobilePadding = intval($responsive['mobile_portrait']['padding'] ?? 12);
            $mobileRadius = intval($responsive['mobile_portrait']['radius'] ?? 0);
            $mobileCardPadding = $mobilePadding;  // Same as container - controlled by branding
            $mobileSpaceSm = 8;
            $mobileSpaceMd = 12;

            $responsiveCss .= '@media (max-width:767px){';
            $responsiveCss .= ':root{';
            $responsiveCss .= '--container-padding:' . $mobilePadding . 'px;';
            $responsiveCss .= '--card-padding:' . $mobileCardPadding . 'px;';
            $responsiveCss .= '--content-padding:' . $mobileCardPadding . 'px;';
            $responsiveCss .= '--table-cell-padding-y:' . $mobileSpaceSm . 'px;';
            $responsiveCss .= '--table-cell-padding-x:' . $mobileSpaceMd . 'px;';
            $responsiveCss .= '--radius-sm:' . $mobileRadius . 'px;';
            $responsiveCss .= '--radius-md:' . $mobileRadius . 'px;';
            $responsiveCss .= '--radius-lg:' . $mobileRadius . 'px;';
            $responsiveCss .= '--radius-xl:' . $mobileRadius . 'px;';
            $responsiveCss .= '}}';

            // Mobile Landscape (sidebar gap)
            $landscapeSidebarGap = intval($responsive['mobile_landscape']['sidebar_gap'] ?? 4);
            $responsiveCss .= '@media (max-width:1023px) and (orientation:landscape){';
            $responsiveCss .= ':root{';
            $responsiveCss .= '--landscape-sidebar-gap:' . $landscapeSidebarGap . 'px;';
            $responsiveCss .= '}}';
        }

        // Process layout settings (content-max-width, sidebar-width, header-height)
        $layout = $brandingData['layout'] ?? null;
        if ($layout) {
            // Content max width
            $contentMaxWidth = $layout['content_max_width'] ?? '1400';
            if ($contentMaxWidth === 'none') {
                $cssOutput .= '--content-max-width:none;';
            } else {
                $cssOutput .= '--content-max-width:' . intval($contentMaxWidth) . 'px;';
            }

            // Sidebar width
            $sidebarWidth = intval($layout['sidebar_width'] ?? 72);
            $cssOutput .= '--sidebar-width:' . $sidebarWidth . 'px;';

            // Header height
            $headerHeight = intval($layout['header_height'] ?? 60);
            $cssOutput .= '--header-height:' . $headerHeight . 'px;';
        }

        // Process gradient settings (simplified - just colors and angle)
        $gradient = $brandingData['gradient'] ?? null;

        if ($gradient && !empty($gradient['enabled'])) {
            // Gradient angle (0-360 degrees)
            $angle = intval($gradient['angle'] ?? 135);
            $angle = max(0, min(360, $angle));
            $cssOutput .= '--gradient-angle:' . $angle . 'deg;';

            // Gradient colors (validate hex format)
            if (!empty($gradient['start']) && preg_match('/^#[0-9A-Fa-f]{6}$/', $gradient['start'])) {
                $cssOutput .= '--gradient-start:' . htmlspecialchars($gradient['start'], ENT_QUOTES, 'UTF-8') . ';';
            }

            if (!empty($gradient['end']) && preg_match('/^#[0-9A-Fa-f]{6}$/', $gradient['end'])) {
                $cssOutput .= '--gradient-end:' . htmlspecialchars($gradient['end'], ENT_QUOTES, 'UTF-8') . ';';
            }
        }

        // Build theme-specific CSS from branding colors
        $themeColorsCss = '';

        // Dark theme colors (applied to :root and html[data-theme="dark"])
        if ($darkColorsCss) {
            // Apply to :root (default) since dark is the default theme
            $themeColorsCss .= ':root,' . 'html[data-theme="dark"]{' . $darkColorsCss . '}';
        }

        // Light theme colors (applied only to html[data-theme="light"])
        if ($lightColorsCss) {
            $themeColorsCss .= 'html[data-theme="light"]{' . $lightColorsCss . '}';
        }

        // Output if we have anything to output
        if ($colorCount > 0 || $responsiveCss || $layout || $gradient || $themeColorsCss) {
            echo '<style id="custom-branding" data-colors="' . $colorCount . '">';
            // Layout/responsive settings go to :root
            if ($cssOutput) {
                echo ':root{' . $cssOutput . '}';
            }
            // Theme-specific colors
            echo $themeColorsCss;
            echo $responsiveCss;
            echo '</style>';
        }
    }
}
?>
