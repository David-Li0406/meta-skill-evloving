<?php
/**
 * POI Type Configuration for TheHUB Event Maps
 *
 * This file defines all available POI (Point of Interest) types
 * with their labels, icons, and colors.
 *
 * @since 2025-12-09
 */

// Prevent direct access
if (!defined('THEHUB_INIT')) {
    die('Direct access not allowed');
}

/**
 * POI Types Definition
 * Each type has: label (Swedish), icon (Lucide), color (hex), description
 */
define('POI_TYPES', [
    'tech_zone' => [
        'label' => 'Teknisk zon',
        'icon' => 'settings',
        'color' => '#EA4335',
        'description' => 'Teknisk assistans'
    ],
    'parking' => [
        'label' => 'Parkering',
        'icon' => 'car',
        'color' => '#0B5394',
        'description' => 'Parkeringsplats'
    ],
    'start' => [
        'label' => 'Start',
        'icon' => 'play',
        'color' => '#61CE70',
        'description' => 'Startplats'
    ],
    'finish' => [
        'label' => 'Mål',
        'icon' => 'flag',
        'color' => '#61CE70',
        'description' => 'Målgång'
    ],
    'water' => [
        'label' => 'Vatten',
        'icon' => 'droplet',
        'color' => '#3C78D8',
        'description' => 'Vattenpunkt'
    ],
    'food' => [
        'label' => 'Mat',
        'icon' => 'utensils',
        'color' => '#674EA7',
        'description' => 'Matställe'
    ],
    'bike_wash' => [
        'label' => 'Cykeltvätt',
        'icon' => 'spray-can',
        'color' => '#46BDC6',
        'description' => 'Cykeltvättstation'
    ],
    'secretariat' => [
        'label' => 'Sekretariat',
        'icon' => 'clipboard-list',
        'color' => '#F4B400',
        'description' => 'Registrering och information'
    ],
    'medical' => [
        'label' => 'Sjukvård',
        'icon' => 'heart-pulse',
        'color' => '#990000',
        'description' => 'Första hjälpen'
    ],
    'toilet' => [
        'label' => 'Toalett',
        'icon' => 'door-open',
        'color' => '#6B7280',
        'description' => 'WC'
    ],
    'shower' => [
        'label' => 'Dusch',
        'icon' => 'droplets',
        'color' => '#46BDC6',
        'description' => 'Dusch'
    ]
]);

/**
 * Segment type colors
 */
define('SEGMENT_COLORS', [
    'stage' => '#EF4444',    // Red for SS/tävlingssträcka
    'liaison' => '#61CE70',  // Green for transport
    'lift' => '#F59E0B'      // Orange for lift
]);

/**
 * Get POI type info
 *
 * @param string $type POI type key
 * @return array|null POI type configuration or null if not found
 */
function getPoiType($type) {
    $types = POI_TYPES;
    return $types[$type] ?? null;
}

/**
 * Get all POI types for admin dropdown
 *
 * @return array Associative array of type => label (no emoji, icons handled by Lucide)
 */
function getPoiTypesForSelect() {
    $options = [];
    foreach (POI_TYPES as $key => $config) {
        $options[$key] = $config['label'];
    }
    return $options;
}

/**
 * Get segment color by type
 *
 * @param string $type 'stage' or 'liaison'
 * @return string Hex color code
 */
function getSegmentColor($type) {
    return SEGMENT_COLORS[$type] ?? SEGMENT_COLORS['stage'];
}

/**
 * Get all POI types as array for JavaScript
 *
 * @return array Full POI types configuration
 */
function getPoiTypesArray() {
    return POI_TYPES;
}
