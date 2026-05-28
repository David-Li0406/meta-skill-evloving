<?php
/**
 * Dynamic PWA Manifest
 * Reads branding settings to serve correct icons
 */
header('Content-Type: application/manifest+json');

require_once __DIR__ . '/config.php';

// Get branding favicon if set
$brandingFavicon = getBranding('logos.favicon');

// Determine icon URL - use branding or default
$iconUrl = $brandingFavicon ?: '/assets/favicon.svg';

// Check if it's a usable format for PWA (PNG preferred)
$iconExt = strtolower(pathinfo($iconUrl, PATHINFO_EXTENSION));
$iconType = match($iconExt) {
    'png' => 'image/png',
    'jpg', 'jpeg' => 'image/jpeg',
    'svg' => 'image/svg+xml',
    'webp' => 'image/webp',
    default => 'image/png'
};

$manifest = [
    'name' => 'TheHUB – GravitySeries',
    'short_name' => 'TheHUB',
    'description' => 'Sveriges plattform för gravity cycling – resultat, serier och åkarprofiler',
    'start_url' => '/',
    'scope' => '/',
    'display' => 'standalone',
    'orientation' => 'any',
    'background_color' => '#F4F5F7',
    'theme_color' => '#004A98',
    'categories' => ['sports', 'lifestyle'],
    'lang' => 'sv-SE',
    'dir' => 'ltr',
    'icons' => [
        [
            'src' => $iconUrl,
            'sizes' => '512x512',
            'type' => $iconType,
            'purpose' => 'any'
        ],
        [
            'src' => $iconUrl,
            'sizes' => '192x192',
            'type' => $iconType,
            'purpose' => 'any'
        ],
        [
            'src' => $iconUrl,
            'sizes' => '512x512',
            'type' => $iconType,
            'purpose' => 'maskable'
        ],
        [
            'src' => $iconUrl,
            'sizes' => '192x192',
            'type' => $iconType,
            'purpose' => 'maskable'
        ]
    ],
    'shortcuts' => [
        [
            'name' => 'Kalender',
            'short_name' => 'Kalender',
            'description' => 'Visa kommande tävlingar',
            'url' => '/calendar',
            'icons' => [['src' => $iconUrl, 'sizes' => '192x192', 'type' => $iconType]]
        ],
        [
            'name' => 'Resultat',
            'short_name' => 'Resultat',
            'description' => 'Visa senaste tävlingsresultat',
            'url' => '/results',
            'icons' => [['src' => $iconUrl, 'sizes' => '192x192', 'type' => $iconType]]
        ],
        [
            'name' => 'Min Sida',
            'short_name' => 'Profil',
            'description' => 'Min profil och anmälningar',
            'url' => '/profile',
            'icons' => [['src' => $iconUrl, 'sizes' => '192x192', 'type' => $iconType]]
        ]
    ],
    'related_applications' => [],
    'prefer_related_applications' => false
];

echo json_encode($manifest, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
