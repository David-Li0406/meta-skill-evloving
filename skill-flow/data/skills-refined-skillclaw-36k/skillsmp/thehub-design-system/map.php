<?php
/**
 * Fullscreen Event Map - Standalone page without header/footer
 *
 * URL: /map.php?id=242 or /map/242
 */
define('THEHUB_INIT', true);
require_once __DIR__ . '/config.php';

global $pdo;

// Get event ID
$eventId = intval($_GET['id'] ?? 0);
if ($eventId <= 0) {
    header('Location: /');
    exit;
}

// Get event info
$db = getDB();
$event = $db->getRow("SELECT id, name, date FROM events WHERE id = ?", [$eventId]);
if (!$event) {
    header('Location: /');
    exit;
}

// Check if map exists
require_once INCLUDES_PATH . '/map_functions.php';
$mapData = getEventMapDataMultiTrack($pdo, $eventId);
if (!$mapData) {
    // No map, redirect to event page
    header('Location: /event/' . $eventId);
    exit;
}

$tracks = $mapData['tracks'] ?? [];
$pois = $mapData['pois'] ?? [];
$poiTypes = $mapData['poi_types'] ?? [];

// Group POIs by type with icon info
$poiGroups = [];
foreach ($pois as $poi) {
    $type = $poi['poi_type'];
    if (!isset($poiGroups[$type])) {
        $typeConfig = $poiTypes[$type] ?? [];
        $poiGroups[$type] = [
            'label' => $typeConfig['label'] ?? $poi['type_label'] ?? $type,
            'icon' => $typeConfig['icon'] ?? 'map-pin',
            'color' => $typeConfig['color'] ?? '#F59E0B',
            'items' => []
        ];
    }
    $poiGroups[$type]['items'][] = $poi;
}

$eventName = htmlspecialchars($event['name']);
?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#1a1a1a">
    <title>Karta - <?= $eventName ?></title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --color-primary: #171717;
            --color-secondary: #323539;
            --color-accent: #61CE70;
            --color-icon: #F59E0B;
            --color-text: #7A7A7A;
            --color-text-dark: #171717;
            --color-border: #e5e7eb;
            --color-bg: #ffffff;
            --color-bg-sunken: #f8f9fa;
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--color-bg-sunken);
        }

        /* Map container */
        #map {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 1;
        }

        /* Sponsor Banner */
        .sponsor-banner {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1001;
            background: var(--color-bg);
            border-bottom: 1px solid var(--color-border);
            box-shadow: var(--shadow-sm);
            padding: calc(env(safe-area-inset-top) + var(--space-md)) var(--space-md) var(--space-md);
            display: none;
            animation: slideDown 0.3s ease;
        }
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-100%); }
            to { opacity: 1; transform: translateY(0); }
        }
        .sponsor-banner.visible {
            display: block;
        }
        .sponsor-banner-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-md);
        }
        .sponsor-banner-label {
            font-size: 0.7rem;
            color: var(--color-text);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .sponsor-banner-logo {
            height: 48px;
            width: auto;
            max-width: 180px;
            object-fit: contain;
            display: none;
        }
        .sponsor-banner-name {
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--color-text-dark);
            display: none;
        }
        @media (min-width: 769px) {
            .sponsor-banner {
                left: 340px;
                padding-top: var(--space-md);
            }
        }

        /* Desktop sidebar - card style matching admin */
        .sidebar {
            display: none;
        }
        @media (min-width: 769px) {
            .sidebar {
                position: fixed;
                top: var(--space-md);
                left: var(--space-md);
                width: 320px;
                max-height: calc(100vh - var(--space-lg) * 2);
                background: var(--color-bg);
                border-radius: var(--radius-lg);
                box-shadow: var(--shadow-lg);
                z-index: 1000;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border: 1px solid var(--color-border);
            }
            .sidebar-header {
                padding: var(--space-md);
                border-bottom: 1px solid var(--color-border);
                background: var(--color-bg);
            }
            .sidebar-header h1 {
                font-size: 1rem;
                font-weight: 600;
                color: var(--color-text-dark);
                margin: 0;
                display: flex;
                align-items: center;
                gap: var(--space-sm);
            }
            .sidebar-header h1::before {
                content: '';
                width: 4px;
                height: 18px;
                background: var(--color-accent);
                border-radius: 2px;
            }
            .sidebar-body {
                flex: 1;
                overflow-y: auto;
                padding: var(--space-md);
            }
            .section {
                margin-bottom: var(--space-lg);
            }
            .section:last-child {
                margin-bottom: 0;
            }
            .section-title {
                font-size: 0.7rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--color-text);
                margin-bottom: var(--space-sm);
                display: flex;
                align-items: center;
                gap: var(--space-xs);
            }
            .track-list {
                display: flex;
                flex-direction: column;
                gap: var(--space-xs);
            }
            .track-item {
                display: flex;
                align-items: center;
                gap: var(--space-sm);
                padding: var(--space-sm) var(--space-md);
                border-radius: var(--radius-sm);
                cursor: pointer;
                border: 1px solid var(--color-border);
                background: var(--color-bg);
                transition: all 0.15s ease;
            }
            .track-item:hover {
                background: var(--color-bg-sunken);
                border-color: var(--color-accent);
            }
            .track-item.active {
                background: rgba(97, 206, 112, 0.1);
                border-color: var(--color-accent);
            }
            .track-dot {
                width: 12px;
                height: 12px;
                border-radius: 3px;
                flex-shrink: 0;
            }
            .track-info {
                flex: 1;
                min-width: 0;
            }
            .track-name {
                font-weight: 500;
                font-size: 0.9rem;
                color: var(--color-text-dark);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .track-meta {
                font-size: 0.75rem;
                color: var(--color-text);
            }
        }

        /* Mobile bottom bar */
        .mobile-bottom-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--color-bg);
            z-index: 1000;
            display: flex;
            align-items: stretch;
            justify-content: space-around;
            padding-bottom: env(safe-area-inset-bottom, 0);
            box-shadow: 0 -1px 0 var(--color-border), var(--shadow-md);
            border-top: 1px solid var(--color-border);
        }
        @media (min-width: 769px) {
            .mobile-bottom-bar { display: none; }
        }
        .nav-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2px;
            padding: var(--space-sm) var(--space-xs);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 0.65rem;
            font-weight: 500;
            color: var(--color-text);
            text-decoration: none;
            transition: color 0.2s;
        }
        .nav-item:active {
            background: var(--color-bg-sunken);
        }
        .nav-item.active {
            color: var(--color-accent);
        }
        .nav-item .nav-icon {
            width: 20px;
            height: 20px;
            stroke-width: 2;
            color: var(--color-icon);
        }
        .nav-item.loading .nav-icon {
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Mobile dropdown menus */
        .controls-top {
            position: fixed;
            z-index: 1000;
        }
        .dropdown-menu {
            background: var(--color-bg);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--color-border);
            overflow: hidden;
        }
        .dropdown-section-title {
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--color-text);
            padding: var(--space-sm) var(--space-md);
            background: var(--color-bg-sunken);
            border-bottom: 1px solid var(--color-border);
        }
        .dropdown-item {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-sm) var(--space-md);
            cursor: pointer;
            border-bottom: 1px solid var(--color-border);
            font-size: 0.85rem;
            color: var(--color-text-dark);
            transition: background 0.15s;
        }
        .dropdown-item:last-child {
            border-bottom: none;
        }
        .dropdown-item:active {
            background: var(--color-bg-sunken);
        }
        .dropdown-item.active {
            background: rgba(97, 206, 112, 0.1);
        }
        .dropdown-item .dot {
            width: 10px;
            height: 10px;
            border-radius: 3px;
            flex-shrink: 0;
        }
        .segment-item {
            padding-left: calc(var(--space-md) + 16px);
        }
        .segment-item .seg-info {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }
        .segment-item .seg-name {
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: var(--space-xs);
        }
        .segment-item .seg-meta {
            font-size: 0.7rem;
            color: var(--color-text);
        }

        /* Desktop controls */
        .controls-bottom {
            position: fixed;
            bottom: var(--space-lg);
            right: var(--space-md);
            z-index: 1000;
            display: none;
            gap: var(--space-sm);
        }
        @media (min-width: 769px) {
            .controls-bottom { display: flex; }
        }
        .btn-circle {
            width: 44px;
            height: 44px;
            background: var(--color-bg);
            border: 1px solid var(--color-border);
            border-radius: 50%;
            box-shadow: var(--shadow-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            color: var(--color-text-dark);
            text-decoration: none;
        }
        .btn-circle:hover {
            border-color: var(--color-accent);
            background: var(--color-bg-sunken);
        }
        .btn-circle:active {
            transform: scale(0.95);
        }
        .btn-circle.active {
            background: var(--color-accent);
            border-color: var(--color-accent);
            color: white;
        }

        /* Elevation panel */
        .elevation {
            position: fixed;
            bottom: calc(52px + env(safe-area-inset-bottom, 0));
            left: 0;
            right: 0;
            background: var(--color-bg);
            z-index: 900;
            border-top: 1px solid var(--color-border);
            box-shadow: 0 -4px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, opacity 0.3s ease;
        }
        @media (min-width: 769px) {
            .elevation {
                bottom: 0;
                left: 340px;
                border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            }
        }
        .elevation.hidden {
            transform: translateY(100%);
            opacity: 0;
            pointer-events: none;
        }
        .elevation-header {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-sm) var(--space-md);
            border-bottom: 1px solid var(--color-border);
        }
        .elevation-header span {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--color-text-dark);
            flex: 1;
        }
        .elevation-close {
            background: none;
            border: none;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            color: var(--color-text);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.15s;
        }
        .elevation-close:hover {
            background: var(--color-bg-sunken);
        }
        .elevation-stats {
            display: flex;
            gap: var(--space-lg);
            padding: var(--space-xs) var(--space-md);
            font-size: 0.75rem;
            color: var(--color-text);
            border-bottom: 1px solid var(--color-border);
            background: var(--color-bg-sunken);
        }
        .elevation-stats .stat {
            display: flex;
            align-items: center;
            gap: var(--space-xs);
        }
        .elevation-stats .stat-value {
            font-weight: 600;
            color: var(--color-text-dark);
        }
        .elevation-content {
            height: 100px;
            padding: var(--space-sm);
        }
        @media (min-width: 769px) {
            .elevation-content {
                height: 120px;
            }
        }
        .elevation canvas {
            width: 100%;
            height: 100%;
        }

        /* Leaflet overrides */
        .leaflet-control-zoom {
            border: 1px solid var(--color-border) !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: var(--shadow-sm) !important;
            overflow: hidden;
        }
        .leaflet-control-zoom a {
            background: var(--color-bg) !important;
            color: var(--color-text-dark) !important;
            border-bottom: 1px solid var(--color-border) !important;
        }
        .leaflet-control-zoom a:last-child {
            border-bottom: none !important;
        }
        .leaflet-control-zoom a:hover {
            background: var(--color-bg-sunken) !important;
        }
        @media (max-width: 768px) {
            .leaflet-bottom.leaflet-left {
                bottom: calc(52px + env(safe-area-inset-bottom, 0) + var(--space-sm)) !important;
            }
        }

        /* POI markers */
        .poi-marker-container {
            background: transparent !important;
            border: none !important;
        }
        .poi-marker {
            width: 28px;
            height: 28px;
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-md);
            border: 2px solid white;
        }
        .poi-marker i {
            transform: rotate(45deg);
        }

        /* Leaflet popup styling */
        .leaflet-popup-content-wrapper {
            border-radius: var(--radius-sm) !important;
            box-shadow: var(--shadow-md) !important;
        }
        .leaflet-popup-content {
            margin: var(--space-sm) var(--space-md) !important;
            font-size: 0.85rem !important;
        }

        /* Start/Finish marker icons */
        .marker-icon-container {
            background: transparent !important;
            border: none !important;
        }
        .marker-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            box-shadow: var(--shadow-md);
            border: 3px solid white;
        }
        .marker-icon.start-marker {
            background: #22C55E;
        }
        .marker-icon.finish-marker {
            background: #171717;
            position: relative;
            overflow: hidden;
        }
        .marker-icon.finish-marker::before {
            content: '';
            position: absolute;
            inset: 0;
            background:
                linear-gradient(45deg, #fff 25%, transparent 25%),
                linear-gradient(-45deg, #fff 25%, transparent 25%),
                linear-gradient(45deg, transparent 75%, #fff 75%),
                linear-gradient(-45deg, transparent 75%, #fff 75%);
            background-size: 8px 8px;
            background-position: 0 0, 0 4px, 4px -4px, -4px 0;
            border-radius: 50%;
        }
        .marker-icon i {
            position: relative;
            z-index: 1;
        }

        /* 3D Map */
        .map3d {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 2000;
            display: none;
            background: #1a1a1a;
        }
        .map3d.active {
            display: block;
        }
        .map3d-controls {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 2001;
            padding: calc(env(safe-area-inset-top) + var(--space-sm)) var(--space-md) var(--space-sm);
            background: linear-gradient(180deg, rgba(0,0,0,0.7) 0%, transparent 100%);
            display: none;
        }
        .map3d.active ~ .map3d-controls,
        .map3d-controls.active {
            display: block;
        }
        .map3d-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: white;
            font-weight: 600;
        }
        .btn-close-3d {
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: white;
        }
        .btn-close-3d:hover {
            background: rgba(255,255,255,0.3);
        }
        .map3d-actions {
            margin-top: var(--space-sm);
        }
        .btn-flyover {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            background: var(--color-accent);
            color: white;
            border: none;
            padding: var(--space-sm) var(--space-md);
            border-radius: var(--radius-sm);
            font-weight: 500;
            font-size: 0.85rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-flyover:hover {
            background: #4db85e;
        }
        .btn-flyover:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .btn-flyover.playing {
            background: var(--color-danger);
        }

        /* 3D Loading indicator */
        .map3d-loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
        }
        .map3d-loading .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(255,255,255,0.2);
            border-top-color: var(--color-accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto var(--space-sm);
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="map3d" class="map3d"></div>

    <!-- 3D Controls overlay -->
    <div id="map3d-controls" class="map3d-controls">
        <div class="map3d-header">
            <span>3D-vy</span>
            <button class="btn-close-3d" onclick="toggle3DMode()"><i data-lucide="x" style="width: 20px; height: 20px;"></i></button>
        </div>
        <div class="map3d-actions">
            <button class="btn-flyover" onclick="startFlyover()" id="btn-flyover">
                <i data-lucide="plane" style="width: 16px; height: 16px;"></i>
                <span>Starta överflygning</span>
            </button>
        </div>
    </div>

    <!-- Sponsor Banner (shown when segment with sponsor is selected) -->
    <div id="sponsor-banner" class="sponsor-banner">
        <div class="sponsor-banner-content">
            <span class="sponsor-banner-label">Sponsrad av</span>
            <img id="sponsor-banner-logo" src="" alt="" class="sponsor-banner-logo">
            <span id="sponsor-banner-name" class="sponsor-banner-name"></span>
        </div>
    </div>

    <!-- Desktop Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <h1><?= $eventName ?></h1>
        </div>
        <div class="sidebar-body">
            <?php if (count($tracks) > 0): ?>
            <div class="section">
                <div class="section-title">Banor</div>
                <?php foreach ($tracks as $track): ?>
                <div class="track-item <?= $track['is_primary'] ? 'active' : '' ?>" data-track-id="<?= $track['id'] ?>" onclick="toggleTrack(<?= $track['id'] ?>)">
                    <span class="track-dot" style="background: <?= htmlspecialchars($track['color'] ?? '#3B82F6') ?>;"></span>
                    <div>
                        <div class="track-name"><?= htmlspecialchars($track['route_label'] ?? $track['name']) ?></div>
                        <div class="track-meta"><?= number_format($track['total_distance_km'], 1) ?> km · +<?= number_format($track['total_elevation_m']) ?> m</div>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>

            <?php if (!empty($poiGroups)): ?>
            <?php foreach ($poiGroups as $type => $group): ?>
            <div class="section">
                <div class="section-title"><i data-lucide="<?= htmlspecialchars($group['icon']) ?>" style="width: 12px; height: 12px; color: <?= htmlspecialchars($group['color']) ?>;"></i> <?= htmlspecialchars($group['label']) ?> (<?= count($group['items']) ?>)</div>
                <?php foreach ($group['items'] as $idx => $poi):
                    $poiName = $poi['label'] ?: $group['label'];
                    if (count($group['items']) > 1 && !$poi['label']) {
                        $poiName = $group['label'] . ' ' . ($idx + 1);
                    }
                ?>
                <div class="track-item" onclick="zoomToPoi(<?= $poi['lat'] ?>, <?= $poi['lng'] ?>, '<?= htmlspecialchars(addslashes($poiName)) ?>', '<?= htmlspecialchars($group['icon']) ?>', '<?= htmlspecialchars($group['color']) ?>')">
                    <div>
                        <div class="track-name"><?= htmlspecialchars($poiName) ?></div>
                        <?php if (!empty($poi['description'])): ?>
                        <div class="track-meta"><?= htmlspecialchars($poi['description']) ?></div>
                        <?php endif; ?>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endforeach; ?>
            <?php endif; ?>
        </div>
    </div>

    <!-- Mobile dropdowns (positioned from bottom bar) -->
    <div class="controls-top" id="mobile-dropdowns">
        <!-- Track & Segment dropdown menu (opens from bottom bar) -->
        <?php if (count($tracks) > 0): ?>
        <div class="dropdown" id="track-dropdown" style="position: fixed; bottom: calc(56px + env(safe-area-inset-bottom) + 170px + var(--space-sm)); left: var(--space-sm); display: none; max-width: calc(100vw - var(--space-md));">
            <div class="dropdown-menu" style="position: static; display: block; max-height: 40vh; overflow-y: auto;">
                <div class="dropdown-section-title">Banor</div>
                <?php foreach ($tracks as $track): ?>
                <div class="dropdown-item <?= $track['is_primary'] ? 'active' : '' ?>" data-track-id="<?= $track['id'] ?>" onclick="selectTrack(<?= $track['id'] ?>)">
                    <span class="dot" style="background: <?= htmlspecialchars($track['color'] ?? '#3B82F6') ?>; width: 12px; height: 12px; border-radius: 3px;"></span>
                    <?= htmlspecialchars($track['route_label'] ?? $track['name']) ?>
                    <span style="margin-left: auto; font-size: 0.8em; opacity: 0.7;"><?= number_format($track['total_distance_km'], 1) ?> km</span>
                </div>
                <?php endforeach; ?>

                <?php
                // Collect all segments from all tracks
                $allSegments = [];
                foreach ($tracks as $track) {
                    if (!empty($track['segments'])) {
                        foreach ($track['segments'] as $seg) {
                            $seg['track_id'] = $track['id'];
                            $seg['track_color'] = $track['color'] ?? '#3B82F6';
                            $allSegments[] = $seg;
                        }
                    }
                }
                // Sort by sequence_number to ensure correct order
                usort($allSegments, fn($a, $b) => ($a['sequence_number'] ?? 0) - ($b['sequence_number'] ?? 0));

                if (!empty($allSegments)): ?>
                <div class="dropdown-section-title">Sträckor</div>
                <?php
                $stageCounter = 0;
                $transportCounter = 0;
                $liftCounter = 0;
                foreach ($allSegments as $seg):
                    $segType = $seg['segment_type'] ?? 'stage';  // DB default is 'stage'
                    $typeIconName = $segType === 'stage' ? 'flag' : ($segType === 'lift' ? 'cable-car' : 'route');

                    // Count segments by type for auto-naming
                    if ($segType === 'stage') $stageCounter++;
                    elseif ($segType === 'lift') $liftCounter++;
                    else $transportCounter++;

                    // Get segment name - check both 'segment_name' and 'name' keys
                    $segName = $seg['segment_name'] ?? $seg['name'] ?? null;
                    if (empty($segName)) {
                        if ($segType === 'stage') {
                            $segName = 'SS' . $stageCounter;
                        } elseif ($segType === 'lift') {
                            $segName = 'Lift ' . $liftCounter;
                        } else {
                            $segName = 'Transport ' . $transportCounter;
                        }
                    }

                    // Sponsor info
                    $segSponsorName = $seg['sponsor_name'] ?? null;
                    $segDisplayName = $segSponsorName ? ($segName . ' By ' . $segSponsorName) : $segName;

                    // Transport/liaison shows HM (climb), Stage shows FHM (descent)
                    $segHeight = $segType === 'stage'
                        ? ($seg['elevation_loss_m'] ?? $seg['elevation_drop_m'] ?? 0)
                        : ($seg['elevation_gain_m'] ?? 0);
                    $segHeightLabel = $segType === 'stage' ? 'FHM' : 'HM';

                    // Format distance - show meters if under 1km
                    $distKm = $seg['distance_km'] ?? 0;
                    if ($distKm < 1) {
                        $distStr = number_format($distKm * 1000, 0) . ' m';
                    } else {
                        $distStr = number_format($distKm, 2) . ' km';
                    }
                ?>
                <div class="dropdown-item segment-item" data-segment-id="<?= $seg['id'] ?>" data-track-id="<?= $seg['track_id'] ?>" onclick="selectSegment(<?= $seg['id'] ?>, <?= $seg['track_id'] ?>)">
                    <div class="seg-info">
                        <span class="seg-name"><i data-lucide="<?= $typeIconName ?>" style="width: 14px; height: 14px; color: var(--color-icon); vertical-align: middle;"></i> <?= htmlspecialchars($segDisplayName) ?></span>
                        <span class="seg-meta"><?= $distStr ?><?php if ($segType !== 'lift'): ?> · <?= number_format($segHeight) ?> m <?= $segHeightLabel ?><?php else: ?> · <em>ej i höjdprofil</em><?php endif; ?></span>
                    </div>
                </div>
                <?php endforeach; ?>
                <?php endif; ?>
            </div>
        </div>
        <?php endif; ?>

        <!-- POI dropdown menu (opens from bottom bar) -->
        <?php if (!empty($pois)): ?>
        <div class="dropdown" id="poi-dropdown" style="position: fixed; bottom: calc(56px + env(safe-area-inset-bottom) + 170px + var(--space-sm)); left: 50%; transform: translateX(-50%); display: none; max-width: calc(100vw - var(--space-md));">
            <div class="dropdown-menu" style="position: static; display: block; max-height: 40vh;">
                <?php foreach ($poiGroups as $type => $group): ?>
                <div class="dropdown-section-title"><i data-lucide="<?= htmlspecialchars($group['icon']) ?>" style="width: 12px; height: 12px; color: <?= htmlspecialchars($group['color']) ?>; vertical-align: middle;"></i> <?= htmlspecialchars($group['label']) ?> (<?= count($group['items']) ?>)</div>
                <?php foreach ($group['items'] as $idx => $poi):
                    $poiName = $poi['label'] ?: $group['label'];
                    if (count($group['items']) > 1 && !$poi['label']) {
                        $poiName = $group['label'] . ' ' . ($idx + 1);
                    }
                ?>
                <div class="dropdown-item" onclick="zoomToPoi(<?= $poi['lat'] ?>, <?= $poi['lng'] ?>, '<?= htmlspecialchars(addslashes($poiName)) ?>', '<?= htmlspecialchars($group['icon']) ?>', '<?= htmlspecialchars($group['color']) ?>')">
                    <?= htmlspecialchars($poiName) ?>
                </div>
                <?php endforeach; ?>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>
    </div>

    <!-- Mobile bottom bar -->
    <div class="mobile-bottom-bar">
        <a href="/event/<?= $eventId ?>" class="nav-item" title="Tillbaka">
            <i data-lucide="arrow-left" class="nav-icon"></i>
            <span>Tillbaka</span>
        </a>
        <?php if (count($tracks) > 0): ?>
        <button class="nav-item" onclick="toggleMobileMenu('track-dropdown')" id="nav-tracks">
            <i data-lucide="map" class="nav-icon"></i>
            <span>Banor</span>
        </button>
        <?php endif; ?>
        <?php if (!empty($poiGroups)): ?>
        <button class="nav-item" onclick="toggleMobileMenu('poi-dropdown')" id="nav-pois">
            <i data-lucide="map-pin" class="nav-icon"></i>
            <span>POIs</span>
        </button>
        <?php endif; ?>
        <button class="nav-item" onclick="toggleElevation()" id="nav-elevation">
            <i data-lucide="mountain" class="nav-icon"></i>
            <span>Höjd</span>
        </button>
        <!-- 3D temporarily disabled - needs improvement
        <button class="nav-item" onclick="toggle3DMode()" id="nav-3d">
            <i data-lucide="box" class="nav-icon"></i>
            <span>3D</span>
        </button>
        -->
        <button class="nav-item" id="nav-location" onclick="toggleLocation()">
            <i data-lucide="locate" class="nav-icon"></i>
            <span>Din plats</span>
        </button>
    </div>

    <!-- Desktop bottom controls -->
    <div class="controls-bottom">
        <a href="/event/<?= $eventId ?>" class="btn-circle" title="Tillbaka till event" style="text-decoration: none;"><i data-lucide="x" style="width: 20px; height: 20px;"></i></a>
        <!-- 3D temporarily disabled - needs improvement
        <button class="btn-circle" id="btn-3d" onclick="toggle3DMode()" title="3D-vy"><i data-lucide="box" style="width: 20px; height: 20px;"></i></button>
        -->
        <button class="btn-circle" id="location-btn" onclick="toggleLocation()" title="Min plats"><i data-lucide="locate" style="width: 20px; height: 20px;"></i></button>
    </div>

    <!-- Elevation -->
    <div class="elevation" id="elevation">
        <div class="elevation-header">
            <i data-lucide="mountain" style="width: 18px; height: 18px; color: var(--color-icon);"></i>
            <span id="elevation-title">Höjdprofil</span>
            <button class="elevation-close" id="elevation-clear-btn" onclick="clearSegmentSelection()" class="hidden" title="Visa hela banan"><i data-lucide="rotate-ccw" style="width: 14px; height: 14px;"></i></button>
        </div>
        <div class="elevation-stats" id="elevation-stats">
            <div class="stat">
                <span>Distans:</span>
                <span class="stat-value" id="stat-distance">-</span>
            </div>
            <div class="stat">
                <span>FHM:</span>
                <span class="stat-value" id="stat-fhm">-</span>
            </div>
            <div class="stat">
                <span>Stigning:</span>
                <span class="stat-value" id="stat-climb">-</span>
            </div>
        </div>
        <div class="elevation-content">
            <canvas id="elevation-canvas"></canvas>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <script>
    const mapData = <?= json_encode($mapData) ?>;
    let map, trackLayers = {}, poiLayers = {}, segmentLayers = {};
    let locationMarker, locationCircle, watchId;
    let visibleTracks = new Set();
    let visiblePoiTypes = new Set();
    let selectedSegment = null;
    let highlightLayer = null;
    let startMarker = null;
    let finishMarker = null;

    // Init
    document.addEventListener('DOMContentLoaded', () => {
        map = L.map('map', { zoomControl: false }).setView([62, 15], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
        L.control.zoom({ position: 'bottomleft' }).addTo(map);

        // Draw tracks
        if (mapData.tracks) {
            mapData.tracks.forEach(track => {
                const layer = L.layerGroup();
                if (track.geojson && track.geojson.features) {
                    L.geoJSON(track.geojson, {
                        style: f => ({ color: f.properties.color || track.color || '#3B82F6', weight: 4, opacity: 0.9 }),
                        onEachFeature: (f, l) => { if (f.properties.name) l.bindPopup('<strong>' + f.properties.name + '</strong><br>' + f.properties.distance_km + ' km'); }
                    }).addTo(layer);
                }
                trackLayers[track.id] = layer;
                if (track.is_primary) { layer.addTo(map); visibleTracks.add(track.id); }
            });
        }

        // Draw POIs with styled markers using POI type icons
        const poiTypes = mapData.poi_types || {};
        if (mapData.pois) {
            mapData.pois.forEach(poi => {
                const type = poi.poi_type;
                const typeConfig = poiTypes[type] || {};
                const color = typeConfig.color || '#F59E0B';
                const icon = typeConfig.icon || 'map-pin';

                if (!poiLayers[type]) { poiLayers[type] = L.layerGroup().addTo(map); visiblePoiTypes.add(type); }

                // Create marker with Lucide icon
                const markerHtml = `<div class="poi-marker" style="background: ${color};">
                    <i data-lucide="${icon}" style="width: 14px; height: 14px; color: white; stroke-width: 2.5;"></i>
                </div>`;

                L.marker([poi.lat, poi.lng], {
                    icon: L.divIcon({
                        className: 'poi-marker-container',
                        html: markerHtml,
                        iconSize: [28, 28], iconAnchor: [14, 28]
                    })
                }).bindPopup('<strong>' + (poi.label || poi.type_label || type) + '</strong>' +
                    (poi.description ? '<br><small>' + poi.description + '</small>' : '')).addTo(poiLayers[type]);
            });
        }

        if (mapData.bounds) map.fitBounds(mapData.bounds, { padding: [50, 50] });
        updateElevation();

        // Initialize Lucide icons
        lucide.createIcons();

        // Set elevation button as active since elevation is visible by default
        document.getElementById('nav-elevation')?.classList.add('active');

        // Close dropdowns and mobile menus when clicking on map
        document.addEventListener('click', e => {
            if (!e.target.closest('.dropdown')) document.querySelectorAll('.dropdown.open').forEach(d => d.classList.remove('open'));
            // Close mobile menus when clicking outside
            if (!e.target.closest('.dropdown') && !e.target.closest('.mobile-bottom-bar') && !e.target.closest('.nav-item')) {
                document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');
            }
        });
    });

    function toggleTrack(id) {
        const layer = trackLayers[id];
        if (!layer) return;
        const item = document.querySelector('[data-track-id="' + id + '"]');
        if (visibleTracks.has(id)) {
            map.removeLayer(layer); visibleTracks.delete(id);
            if (item) item.classList.remove('active');
        } else {
            layer.addTo(map); visibleTracks.add(id);
            if (item) item.classList.add('active');
        }
        updateElevation();
    }

    function selectTrack(id) {
        // Clear selected segment and markers
        selectedSegment = null;
        if (highlightLayer) { map.removeLayer(highlightLayer); highlightLayer = null; }
        if (startMarker) { map.removeLayer(startMarker); startMarker = null; }
        if (finishMarker) { map.removeLayer(finishMarker); finishMarker = null; }

        // Hide sponsor banner
        document.getElementById('sponsor-banner').classList.remove('visible');

        // Show only this track
        Object.keys(trackLayers).forEach(tid => {
            const layer = trackLayers[tid], intId = parseInt(tid);
            if (intId === id) {
                if (!map.hasLayer(layer)) layer.addTo(map);
                visibleTracks.add(intId);
            } else {
                if (map.hasLayer(layer)) map.removeLayer(layer);
                visibleTracks.delete(intId);
            }
        });

        // Zoom to track bounds using the Leaflet layer's actual bounds
        const track = mapData.tracks.find(t => t.id === id);
        const layer = trackLayers[id];
        if (layer && layer.getBounds) {
            const bounds = layer.getBounds();
            if (bounds.isValid()) {
                map.fitBounds(bounds, { padding: [50, 50] });
            }
        } else if (track && track.bounds) {
            // Fallback to pre-calculated bounds if available
            map.fitBounds(track.bounds, { padding: [50, 50] });
        }

        // Update UI
        document.querySelectorAll('#track-dropdown .dropdown-item[data-track-id]').forEach(i => {
            i.classList.toggle('active', parseInt(i.dataset.trackId) === id && !i.classList.contains('segment-item'));
        });
        document.querySelectorAll('.segment-item').forEach(i => i.classList.remove('active'));

        // Close mobile menu
        document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');

        // Update elevation title and hide clear button
        document.getElementById('elevation-title').textContent = track ? (track.route_label || track.name) : 'Höjdprofil';
        document.getElementById('elevation-clear-btn').style.display = 'none';

        updateElevation();
    }

    function selectSegment(segmentId, trackId) {
        // First make sure the parent track is visible
        const layer = trackLayers[trackId];
        if (layer && !map.hasLayer(layer)) {
            layer.addTo(map);
            visibleTracks.add(trackId);
        }

        // Find the segment
        const track = mapData.tracks.find(t => t.id === trackId);
        const segment = track?.segments?.find(s => s.id === segmentId);
        if (!segment) return;

        selectedSegment = { trackId, segmentId, segment };

        // Remove old highlight and markers
        if (highlightLayer) { map.removeLayer(highlightLayer); highlightLayer = null; }
        if (startMarker) { map.removeLayer(startMarker); startMarker = null; }
        if (finishMarker) { map.removeLayer(finishMarker); finishMarker = null; }

        // Highlight the segment
        if (segment.coordinates && segment.coordinates.length > 0) {
            const coords = segment.coordinates.map(c => [c.lat, c.lng]);
            highlightLayer = L.polyline(coords, {
                color: '#F59E0B',
                weight: 8,
                opacity: 1,
                lineCap: 'round',
                lineJoin: 'round'
            }).addTo(map);

            // Add start marker (green with play icon)
            const startPoint = segment.coordinates[0];
            startMarker = L.marker([startPoint.lat, startPoint.lng], {
                icon: L.divIcon({
                    className: 'marker-icon-container',
                    html: '<div class="marker-icon start-marker"><i data-lucide="play" style="width: 14px; height: 14px; color: white; margin-left: 2px;"></i></div>',
                    iconSize: [32, 32],
                    iconAnchor: [16, 16]
                })
            }).addTo(map).bindTooltip('Start', { permanent: false, direction: 'top', offset: [0, -16] });

            // Add finish marker (checkered flag pattern)
            const endPoint = segment.coordinates[segment.coordinates.length - 1];
            finishMarker = L.marker([endPoint.lat, endPoint.lng], {
                icon: L.divIcon({
                    className: 'marker-icon-container',
                    html: '<div class="marker-icon finish-marker"><i data-lucide="flag" style="width: 14px; height: 14px; color: white;"></i></div>',
                    iconSize: [32, 32],
                    iconAnchor: [16, 16]
                })
            }).addTo(map).bindTooltip('Mål', { permanent: false, direction: 'top', offset: [0, -16] });

            // Re-initialize Lucide icons for markers
            setTimeout(() => lucide.createIcons(), 50);

            // Zoom to segment with padding for sponsor banner (top) and elevation (bottom)
            // Top: ~100px for sponsor banner, Bottom: ~220px for elevation + bottom bar
            map.fitBounds(highlightLayer.getBounds(), {
                paddingTopLeft: [40, 120],
                paddingBottomRight: [40, 240],
                maxZoom: 16
            });
        }

        // Show sponsor banner if segment has sponsor
        const banner = document.getElementById('sponsor-banner');
        if (segment.sponsor_name) {
            const logoEl = document.getElementById('sponsor-banner-logo');
            const nameEl = document.getElementById('sponsor-banner-name');

            if (segment.sponsor_logo) {
                logoEl.src = segment.sponsor_logo;
                logoEl.alt = segment.sponsor_name;
                logoEl.style.display = 'block';
                nameEl.style.display = 'none';
            } else {
                logoEl.style.display = 'none';
                nameEl.textContent = segment.sponsor_name;
                nameEl.style.display = 'block';
            }
            banner.classList.add('visible');
        } else {
            banner.classList.remove('visible');
        }

        // Update UI
        document.querySelectorAll('#track-dropdown .dropdown-item').forEach(i => i.classList.remove('active'));
        document.querySelector(`.segment-item[data-segment-id="${segmentId}"]`)?.classList.add('active');

        // Close mobile menu
        document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');

        // Update elevation title and show clear button
        const segName = segment.segment_name || segment.name || (segment.segment_type === 'stage' ? 'SS' : 'Transport');
        document.getElementById('elevation-title').textContent = segName;
        document.getElementById('elevation-clear-btn').style.display = 'flex';

        // Show elevation for this segment only
        updateElevation(segment);
    }

    function clearSegmentSelection() {
        // Clear selected segment
        selectedSegment = null;
        if (highlightLayer) { map.removeLayer(highlightLayer); highlightLayer = null; }
        if (startMarker) { map.removeLayer(startMarker); startMarker = null; }
        if (finishMarker) { map.removeLayer(finishMarker); finishMarker = null; }

        // Hide sponsor banner
        document.getElementById('sponsor-banner').classList.remove('visible');

        // Reset UI
        document.querySelectorAll('#track-dropdown .dropdown-item').forEach(i => i.classList.remove('active'));
        // Re-activate visible tracks
        document.querySelectorAll('#track-dropdown .dropdown-item[data-track-id]:not(.segment-item)').forEach(i => {
            if (visibleTracks.has(parseInt(i.dataset.trackId))) {
                i.classList.add('active');
            }
        });

        // Reset elevation title and hide clear button
        document.getElementById('elevation-title').textContent = 'Höjdprofil';
        document.getElementById('elevation-clear-btn').style.display = 'none';

        // Update elevation to show all visible tracks
        updateElevation();
    }

    function zoomToPoi(lat, lng, label, icon = 'map-pin', color = '#F59E0B') {
        // Zoom to POI location with smooth animation
        map.flyTo([lat, lng], 18, { duration: 0.5 });

        // Close mobile menu
        document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');

        // Show popup with icon
        const popupContent = `<div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 24px; height: 24px; background: ${color}; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <i data-lucide="${icon}" style="width: 14px; height: 14px; color: white;"></i>
            </div>
            <strong>${label}</strong>
        </div>`;

        L.popup({ offset: [0, -10] })
            .setLatLng([lat, lng])
            .setContent(popupContent)
            .openOn(map);

        // Re-initialize Lucide icons for popup
        setTimeout(() => lucide.createIcons(), 50);
    }

    function toggleDropdown(id) {
        const d = document.getElementById(id), wasOpen = d.classList.contains('open');
        document.querySelectorAll('.dropdown.open').forEach(x => x.classList.remove('open'));
        if (!wasOpen) d.classList.add('open');
    }

    function toggleMobileMenu(id) {
        const menu = document.getElementById(id);
        if (!menu) return;
        const isVisible = menu.style.display !== 'none';
        // Hide all menus first
        document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');
        // Toggle the clicked menu
        if (!isVisible) {
            menu.style.display = 'block';
        }
    }

    function toggleElevation() {
        const el = document.getElementById('elevation');
        const navBtn = document.getElementById('nav-elevation');
        // Hide menus when showing elevation
        document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');

        el.classList.toggle('hidden');
        navBtn?.classList.toggle('active', !el.classList.contains('hidden'));
        if (!el.classList.contains('hidden')) {
            setTimeout(updateElevation, 350);
        }
    }

    function toggleLocation() {
        const btn = document.getElementById('location-btn');
        const navBtn = document.getElementById('nav-location');
        // Hide menus when toggling location
        document.querySelectorAll('#mobile-dropdowns .dropdown').forEach(d => d.style.display = 'none');

        if (watchId) {
            navigator.geolocation.clearWatch(watchId); watchId = null;
            if (locationMarker) map.removeLayer(locationMarker);
            if (locationCircle) map.removeLayer(locationCircle);
            locationMarker = locationCircle = null;
            btn?.classList.remove('active', 'loading');
            navBtn?.classList.remove('active', 'loading');
            return;
        }
        if (!navigator.geolocation) { alert('Geolocation stöds inte'); return; }
        btn?.classList.add('loading');
        navBtn?.classList.add('loading');
        watchId = navigator.geolocation.watchPosition(
            pos => {
                const { latitude, longitude, accuracy } = pos.coords;
                btn?.classList.remove('loading'); btn?.classList.add('active');
                navBtn?.classList.remove('loading'); navBtn?.classList.add('active');
                if (!locationMarker) {
                    locationMarker = L.circleMarker([latitude, longitude], { radius: 8, fillColor: '#3B82F6', fillOpacity: 1, color: 'white', weight: 3 }).addTo(map);
                    locationCircle = L.circle([latitude, longitude], { radius: accuracy, fillColor: '#3B82F6', fillOpacity: 0.1, color: '#3B82F6', weight: 1 }).addTo(map);
                    map.setView([latitude, longitude], 15);
                } else {
                    locationMarker.setLatLng([latitude, longitude]);
                    locationCircle.setLatLng([latitude, longitude]).setRadius(accuracy);
                }
            },
            () => { btn?.classList.remove('loading'); navBtn?.classList.remove('loading'); alert('Kunde inte hämta position'); },
            { enableHighAccuracy: true, maximumAge: 10000 }
        );
    }


    function updateElevation(singleSegment = null) {
        const canvas = document.getElementById('elevation-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width * 2; canvas.height = rect.height * 2;
        ctx.scale(2, 2);

        // Segment colors: stage=red, liaison=green, lift=yellow
        const segColors = { stage: '#EF4444', liaison: '#61CE70', lift: '#F59E0B' };
        let allEle = [], allDist = [], segmentTypes = [];

        // If no segment passed but one is selected, use the selected segment
        if (!singleSegment && selectedSegment && selectedSegment.segment) {
            singleSegment = selectedSegment.segment;
        }

        if (singleSegment) {
            // Show single segment elevation
            const ele = singleSegment.elevation_data || [];
            const coords = singleSegment.coordinates || [];
            const segType = singleSegment.segment_type || 'stage';
            let dist = 0;
            coords.forEach((c, i) => {
                if (i > 0) dist += haversine(coords[i-1].lat, coords[i-1].lng, c.lat, c.lng);
                allDist.push(dist);
                allEle.push(ele[i] ?? c.ele ?? 0);
                segmentTypes.push(segType);
            });
        } else if (mapData.tracks) {
            // Show all visible tracks including lift
            mapData.tracks.forEach(track => {
                if (!visibleTracks.has(track.id)) return;
                (track.segments || []).forEach(seg => {
                    const ele = seg.elevation_data || [], coords = seg.coordinates || [];
                    const segType = seg.segment_type || 'stage';
                    let dist = allDist.length ? allDist[allDist.length - 1] : 0;
                    coords.forEach((c, i) => {
                        if (i > 0) dist += haversine(coords[i-1].lat, coords[i-1].lng, c.lat, c.lng);
                        allDist.push(dist);
                        allEle.push(ele[i] ?? c.ele ?? 0);
                        segmentTypes.push(segType);
                    });
                });
            });
        }

        // Calculate stats - exclude lift segments
        const totalDist = allDist.length > 0 ? allDist[allDist.length - 1] : 0;
        let totalClimb = 0, totalDescent = 0;
        for (let i = 1; i < allEle.length; i++) {
            // Skip elevation changes in lift segments
            if (segmentTypes[i] === 'lift' || segmentTypes[i-1] === 'lift') continue;
            const diff = allEle[i] - allEle[i-1];
            if (diff > 0) totalClimb += diff;
            else totalDescent += Math.abs(diff);
        }
        const fhm = totalDescent; // Fall Height Meters

        // Update stats display
        document.getElementById('stat-distance').textContent = totalDist.toFixed(2) + ' km';
        document.getElementById('stat-fhm').textContent = Math.round(fhm) + ' m';
        document.getElementById('stat-climb').textContent = '+' + Math.round(totalClimb) + ' m';

        if (allEle.length < 2) {
            ctx.fillStyle = '#999'; ctx.font = '12px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText('Ingen höjddata', rect.width / 2, rect.height / 2);
            return;
        }

        const minE = Math.min(...allEle), maxE = Math.max(...allEle), maxD = Math.max(...allDist), range = maxE - minE || 1;
        const pad = { t: 10, r: 10, b: 20, l: 40 }, w = rect.width - pad.l - pad.r, h = rect.height - pad.t - pad.b;

        // Draw segments with different colors
        let currentType = segmentTypes[0];
        let segStart = 0;

        for (let i = 1; i <= allDist.length; i++) {
            if (i === allDist.length || segmentTypes[i] !== currentType) {
                // Draw this segment
                const color = segColors[currentType] || '#61CE70';
                const fillColor = color + '40'; // Add alpha

                // Fill
                ctx.fillStyle = fillColor;
                ctx.beginPath();
                ctx.moveTo(pad.l + (allDist[segStart] / maxD) * w, pad.t + h);
                for (let j = segStart; j < i; j++) {
                    ctx.lineTo(pad.l + (allDist[j] / maxD) * w, pad.t + h - ((allEle[j] - minE) / range) * h);
                }
                ctx.lineTo(pad.l + (allDist[i-1] / maxD) * w, pad.t + h);
                ctx.closePath();
                ctx.fill();

                // Stroke
                ctx.strokeStyle = color;
                ctx.lineWidth = 2;
                ctx.beginPath();
                for (let j = segStart; j < i; j++) {
                    const x = pad.l + (allDist[j] / maxD) * w;
                    const y = pad.t + h - ((allEle[j] - minE) / range) * h;
                    j === segStart ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
                }
                ctx.stroke();

                if (i < allDist.length) {
                    currentType = segmentTypes[i];
                    segStart = i;
                }
            }
        }

        // Draw axis labels
        ctx.fillStyle = '#666'; ctx.font = '10px sans-serif';
        ctx.textAlign = 'right'; ctx.fillText(Math.round(maxE) + ' m', pad.l - 4, pad.t + 10); ctx.fillText(Math.round(minE) + ' m', pad.l - 4, pad.t + h);
        ctx.textAlign = 'center'; ctx.fillText('0', pad.l, pad.t + h + 14); ctx.fillText(maxD.toFixed(1) + ' km', pad.l + w, pad.t + h + 14);
    }

    function haversine(lat1, lon1, lat2, lon2) {
        const R = 6371, dLat = (lat2 - lat1) * Math.PI / 180, dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2)**2 + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2)**2;
        return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    }

    window.addEventListener('resize', () => setTimeout(updateElevation, 100));

    // ============================================
    // 3D MAP FUNCTIONALITY (loads on-demand)
    // ============================================
    let map3d = null;
    let map3dLoaded = false;
    let flyoverAnimation = null;
    let is3DMode = false;

    function toggle3DMode() {
        const container = document.getElementById('map3d');
        const controls = document.getElementById('map3d-controls');
        const nav3d = document.getElementById('nav-3d');
        const btn3d = document.getElementById('btn-3d');

        is3DMode = !is3DMode;

        if (is3DMode) {
            container.classList.add('active');
            controls.classList.add('active');
            nav3d?.classList.add('active');
            btn3d?.classList.add('active');

            // Load MapLibre on first use
            if (!map3dLoaded) {
                load3DMap();
            } else if (map3d) {
                map3d.resize();
            }
        } else {
            container.classList.remove('active');
            controls.classList.remove('active');
            nav3d?.classList.remove('active');
            btn3d?.classList.remove('active');
            stopFlyover();
        }
    }

    function load3DMap() {
        const container = document.getElementById('map3d');

        // Show loading
        container.innerHTML = '<div class="map3d-loading"><div class="spinner"></div><div>Laddar 3D-karta...</div></div>';

        // Load MapLibre CSS
        const css = document.createElement('link');
        css.rel = 'stylesheet';
        css.href = 'https://unpkg.com/maplibre-gl@4.1.0/dist/maplibre-gl.css';
        document.head.appendChild(css);

        // Load MapLibre JS
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/maplibre-gl@4.1.0/dist/maplibre-gl.js';
        script.onload = () => {
            init3DMap();
        };
        script.onerror = () => {
            container.innerHTML = '<div class="map3d-loading"><div>Kunde inte ladda 3D-kartan.<br>Kontrollera din internetanslutning.</div></div>';
        };
        document.head.appendChild(script);
    }

    function init3DMap() {
        const container = document.getElementById('map3d');
        container.innerHTML = '';

        // Get center from current bounds
        const bounds = mapData.bounds;
        const center = bounds ? [(bounds[0][1] + bounds[1][1]) / 2, (bounds[0][0] + bounds[1][0]) / 2] : [15, 62];

        // Create MapLibre map with 3D terrain
        map3d = new maplibregl.Map({
            container: 'map3d',
            style: {
                version: 8,
                sources: {
                    'osm': {
                        type: 'raster',
                        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
                        tileSize: 256,
                        attribution: '&copy; OpenStreetMap'
                    },
                    'terrain': {
                        type: 'raster-dem',
                        tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],
                        tileSize: 256,
                        encoding: 'terrarium'
                    }
                },
                layers: [
                    {
                        id: 'osm-layer',
                        type: 'raster',
                        source: 'osm',
                        minzoom: 0,
                        maxzoom: 19
                    }
                ],
                terrain: {
                    source: 'terrain',
                    exaggeration: 1.5
                },
                sky: {}
            },
            center: center,
            zoom: 13,
            pitch: 60,
            bearing: 0,
            maxPitch: 85
        });

        map3d.on('load', () => {
            map3dLoaded = true;
            add3DTracks();

            // Add navigation controls
            map3d.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');
        });
    }

    function add3DTracks() {
        if (!map3d || !mapData.tracks) return;

        // Collect all coordinates for tracks
        const allCoords = [];

        mapData.tracks.forEach((track, trackIdx) => {
            if (!track.segments) return;

            track.segments.forEach((segment, segIdx) => {
                if (!segment.coordinates || segment.coordinates.length < 2) return;

                const coords = segment.coordinates.map((c, i) => {
                    const ele = segment.elevation_data?.[i] ?? c.ele ?? 0;
                    allCoords.push([c.lng, c.lat, ele]);
                    return [c.lng, c.lat, ele];
                });

                const segType = segment.segment_type || 'stage';
                const color = segType === 'stage' ? '#EF4444' : segType === 'lift' ? '#F59E0B' : '#61CE70';

                // Add line source and layer
                const sourceId = `track-${trackIdx}-seg-${segIdx}`;
                map3d.addSource(sourceId, {
                    type: 'geojson',
                    data: {
                        type: 'Feature',
                        geometry: {
                            type: 'LineString',
                            coordinates: coords
                        }
                    }
                });

                map3d.addLayer({
                    id: sourceId,
                    type: 'line',
                    source: sourceId,
                    paint: {
                        'line-color': color,
                        'line-width': 4,
                        'line-opacity': 0.9
                    }
                });
            });
        });

        // Fit to bounds
        if (allCoords.length > 0) {
            const lngs = allCoords.map(c => c[0]);
            const lats = allCoords.map(c => c[1]);
            map3d.fitBounds([
                [Math.min(...lngs), Math.min(...lats)],
                [Math.max(...lngs), Math.max(...lats)]
            ], { padding: 50, pitch: 60, duration: 1000 });
        }
    }

    // Collect all track coordinates for flyover
    function getTrackCoordinates() {
        const coords = [];
        if (!mapData.tracks) return coords;

        mapData.tracks.forEach(track => {
            if (!track.segments) return;
            track.segments.forEach(segment => {
                if (!segment.coordinates) return;
                segment.coordinates.forEach((c, i) => {
                    const ele = segment.elevation_data?.[i] ?? c.ele ?? 0;
                    coords.push({ lng: c.lng, lat: c.lat, ele: ele });
                });
            });
        });
        return coords;
    }

    function startFlyover() {
        if (!map3d) return;

        const btn = document.getElementById('btn-flyover');
        if (flyoverAnimation) {
            stopFlyover();
            return;
        }

        const coords = getTrackCoordinates();
        if (coords.length < 2) return;

        btn.classList.add('playing');
        btn.querySelector('span').textContent = 'Stoppa';

        let currentIdx = 0;
        const step = Math.max(1, Math.floor(coords.length / 200)); // ~200 steps total

        function animate() {
            if (currentIdx >= coords.length - 1) {
                stopFlyover();
                return;
            }

            const current = coords[currentIdx];
            const next = coords[Math.min(currentIdx + step, coords.length - 1)];

            // Calculate bearing
            const bearing = calculateBearing(current.lat, current.lng, next.lat, next.lng);

            map3d.easeTo({
                center: [current.lng, current.lat],
                bearing: bearing,
                pitch: 70,
                zoom: 15,
                duration: 100
            });

            currentIdx += step;
            flyoverAnimation = setTimeout(animate, 100);
        }

        // Start from beginning
        map3d.easeTo({
            center: [coords[0].lng, coords[0].lat],
            bearing: calculateBearing(coords[0].lat, coords[0].lng, coords[1].lat, coords[1].lng),
            pitch: 70,
            zoom: 15,
            duration: 1000
        });

        setTimeout(animate, 1000);
    }

    function stopFlyover() {
        if (flyoverAnimation) {
            clearTimeout(flyoverAnimation);
            flyoverAnimation = null;
        }

        const btn = document.getElementById('btn-flyover');
        btn?.classList.remove('playing');
        if (btn) btn.querySelector('span').textContent = 'Starta överflygning';
    }

    function calculateBearing(lat1, lng1, lat2, lng2) {
        const toRad = x => x * Math.PI / 180;
        const toDeg = x => x * 180 / Math.PI;

        const dLng = toRad(lng2 - lng1);
        const y = Math.sin(dLng) * Math.cos(toRad(lat2));
        const x = Math.cos(toRad(lat1)) * Math.sin(toRad(lat2)) - Math.sin(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.cos(dLng);
        return (toDeg(Math.atan2(y, x)) + 360) % 360;
    }
    </script>
</body>
</html>
