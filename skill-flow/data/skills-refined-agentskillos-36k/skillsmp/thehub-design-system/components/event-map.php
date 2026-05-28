<?php
/**
 * Event Map Component - Responsive Fullscreen Design
 *
 * Desktop: Full map with sidebar for track/segment/POI selection
 * Mobile: Fullscreen with floating dropdown menus
 *
 * @since 2025-12-10
 */

// Prevent direct access
if (!defined('THEHUB_INIT')) {
    die('Direct access not allowed');
}

// Include map functions if not already loaded
if (!function_exists('getEventMapDataMultiTrack')) {
    require_once INCLUDES_PATH . '/map_functions.php';
}

if (!function_exists('render_event_map')) {
    /**
     * Render an event map (fullscreen responsive version)
     */
    function render_event_map(int $eventId, PDO $pdo, array $options = []): void {
        // Try multi-track first, fall back to single track
        $mapData = getEventMapDataMultiTrack($pdo, $eventId);

        if (!$mapData) {
            // Fallback to old single-track function
            $mapData = getEventMapData($pdo, $eventId);
        }

        if (!$mapData) {
            ?>
            <div class="event-map-empty" style="padding: var(--space-2xl); text-align: center; color: var(--color-text);">
                <p>Ingen karta tillgänglig för detta event.</p>
            </div>
            <?php
            return;
        }

        $mapId = 'emap_' . $eventId . '_' . substr(uniqid(), -6);

        // Handle both multi-track and single-track data formats
        $tracks = $mapData['tracks'] ?? [];
        if (empty($tracks) && isset($mapData['track'])) {
            // Convert single track format to multi-track format
            $tracks = [[
                'id' => $mapData['track']['id'],
                'name' => $mapData['track']['name'],
                'route_label' => $mapData['track']['name'],
                'color' => '#3B82F6',
                'is_primary' => true,
                'total_distance_km' => $mapData['track']['total_distance_km'],
                'total_elevation_m' => $mapData['track']['total_elevation_m'],
                'segments' => $mapData['segments'] ?? [],
                'geojson' => $mapData['geojson'] ?? null
            ]];
            $mapData['tracks'] = $tracks;
        }

        $pois = $mapData['pois'] ?? [];

        // POI type to Lucide icon mapping
        $poiIconMap = [
            'tech_zone' => 'settings',
            'parking' => 'car',
            'start' => 'play',
            'finish' => 'flag',
            'water' => 'droplet',
            'food' => 'utensils',
            'bike_wash' => 'spray-can',
            'secretariat' => 'clipboard-list',
            'medical' => 'heart-pulse',
            'toilet' => 'door-open',
            'shower' => 'droplets',
        ];

        // Group POIs by type
        $poiGroups = [];
        foreach ($pois as $poi) {
            $type = $poi['poi_type'];
            if (!isset($poiGroups[$type])) {
                $poiGroups[$type] = [
                    'label' => $poi['type_label'] ?? $type,
                    'icon' => $poiIconMap[$type] ?? ($poi['type_icon'] ?? 'map-pin'),
                    'items' => []
                ];
            }
            $poiGroups[$type]['items'][] = $poi;
        }

        $fullscreen = $options['fullscreen'] ?? false;
        $showClose = $options['show_close'] ?? $fullscreen;
        $eventName = $options['event_name'] ?? 'Event';
        $height = $options['height'] ?? ($fullscreen ? '100dvh' : 'clamp(500px, 70vh, 800px)');
        ?>

<style>
.emap-container {
    position: relative;
    width: 100%;
    background: var(--color-bg-sunken, #f8f9fa);
    overflow: hidden;
    border-radius: var(--radius-md, 10px);
}
/* Desktop layout - sidebar beside map, not overlapping */
@media (min-width: 769px) {
    .emap-container {
        display: flex;
        flex-direction: row;
        height: <?= $height ?>;
        min-height: 500px;
    }
    .emap-sidebar {
        position: relative;
        top: auto;
        left: auto;
        bottom: auto;
        width: 280px;
        min-width: 280px;
        max-width: 280px;
        background: var(--color-bg-card, #fff);
        border-right: 1px solid var(--color-border);
        z-index: 100;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border-radius: var(--radius-md, 10px) 0 0 var(--radius-md, 10px);
    }
    .emap-sidebar-header {
        padding: var(--space-md);
        border-bottom: 1px solid var(--color-border);
        flex-shrink: 0;
    }
    .emap-sidebar-body {
        flex: 1;
        overflow-y: auto;
        padding: var(--space-md);
    }
    .emap-main {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
        position: relative;
    }
    .emap-map {
        position: relative;
        flex: 1;
        min-height: 0;
    }
    .emap-elevation {
        position: relative !important;
        bottom: auto !important;
        left: auto !important;
        right: auto !important;
        background: var(--color-bg-card, #fff) !important;
        z-index: 200 !important;
        flex-shrink: 0;
        border-top: 1px solid var(--color-border);
        min-height: 40px;
        transform: none !important;
    }
    .emap-elevation.collapsed {
        transform: none !important;
    }
    .emap-elevation.collapsed .emap-elevation-content {
        display: none;
    }
    .emap-main {
        overflow: visible;
    }
    .emap-location-btn {
        position: absolute;
        bottom: 60px;
        right: var(--space-md);
        z-index: 100;
    }
    .emap-close {
        position: absolute;
        top: var(--space-md);
        right: var(--space-md);
        z-index: 100;
    }
    .emap-mobile-controls { display: none; }
}
/* Mobile layout - original overlay behavior */
@media (max-width: 768px) {
    .emap-container {
        height: <?= $height ?>;
    }
    .emap-main {
        position: absolute;
        inset: 0;
    }
    .emap-map {
        position: absolute;
        inset: 0;
        z-index: 1;
    }
    .emap-sidebar { display: none; }
    .emap-mobile-controls {
        position: absolute;
        top: var(--space-sm);
        left: var(--space-sm);
        right: 50px;
        z-index: 100;
        display: flex;
        gap: var(--space-sm);
        flex-wrap: wrap;
    }
    .emap-elevation {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255,255,255,0.97);
        backdrop-filter: blur(10px);
        z-index: 90;
        transition: transform 0.3s ease;
    }
    .emap-elevation.collapsed {
        transform: translateY(calc(100% - 40px));
    }
}
<?php if ($fullscreen): ?>
@media (max-width: 768px) {
    .emap-container {
        position: fixed;
        inset: 0;
        height: 100%;
        height: 100dvh;
        border-radius: 0;
    }
}
<?php endif; ?>
/* Mobile floating controls */
@media (max-width: 768px) {
    .emap-sidebar { display: none; }
    .emap-mobile-controls {
        position: absolute;
        top: var(--space-sm);
        left: var(--space-sm);
        right: 50px;
        z-index: 100;
        display: flex;
        gap: var(--space-sm);
        flex-wrap: wrap;
    }
    .emap-dropdown {
        position: relative;
    }
    .emap-dropdown-btn {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        padding: var(--space-sm) var(--space-md);
        background: rgba(255,255,255,0.97);
        backdrop-filter: blur(10px);
        border: none;
        border-radius: var(--radius-full);
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        box-shadow: var(--shadow-md);
        white-space: nowrap;
    }
    .emap-dropdown-btn .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    .emap-dropdown-menu {
        position: absolute;
        top: calc(100% + var(--space-xs));
        left: 0;
        min-width: 200px;
        max-height: 300px;
        overflow-y: auto;
        background: rgba(255,255,255,0.98);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        display: none;
        z-index: 200;
    }
    .emap-dropdown.open .emap-dropdown-menu {
        display: block;
    }
    .emap-dropdown-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-sm) var(--space-md);
        cursor: pointer;
        border-bottom: 1px solid var(--color-border);
    }
    .emap-dropdown-item:last-child { border-bottom: none; }
    .emap-dropdown-item:hover { background: var(--color-border); }
    .emap-dropdown-item.active { background: rgba(97,206,112,0.1); }
}
.emap-section {
    margin-bottom: var(--space-md);
}
/* Section headers */
.emap-section-header {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text);
    padding: var(--space-sm) 0;
    margin-top: var(--space-md);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}
.emap-section-header:first-child { margin-top: 0; }
.emap-section-header i { width: 12px; height: 12px; }
/* Collapsible sections */
.emap-collapsible {
    margin-bottom: var(--space-sm);
}
.emap-collapsible-header {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-xs) 0;
    cursor: pointer;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: var(--color-text-secondary);
    user-select: none;
    list-style: none;
    border-bottom: 1px solid var(--color-border);
    margin-bottom: var(--space-xs);
}
.emap-collapsible-header::-webkit-details-marker { display: none; }
.emap-collapsible-header:hover { color: var(--color-text); }
.emap-collapsible-header i { width: 12px; height: 12px; flex-shrink: 0; }
.emap-collapse-icon { transition: transform 0.2s; }
.emap-collapsible:not([open]) .emap-collapse-icon { transform: rotate(-90deg); }
.emap-collapsible-content {
    max-height: 280px;
    overflow-y: auto;
}
/* POI items - simple clickable list */
.emap-poi-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) var(--space-sm);
    font-size: 0.85rem;
    color: var(--color-text);
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: background 0.15s ease;
}
.emap-poi-item i {
    width: 16px;
    height: 16px;
    color: var(--color-accent);
    flex-shrink: 0;
}
.emap-poi-item:hover {
    background: var(--color-bg-hover, #f0f0f0);
}
.emap-poi-item:hover span {
    color: var(--color-accent);
}
.emap-section-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text);
    margin: 0;
}
.emap-track-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm);
    border-radius: var(--radius-sm);
    cursor: pointer;
    margin-bottom: var(--space-xs);
    transition: background 0.2s;
}
.emap-track-item:hover { background: var(--color-border); }
.emap-track-item.active { background: rgba(97,206,112,0.15); }
.emap-track-dot {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    flex-shrink: 0;
}
.emap-track-info { flex: 1; min-width: 0; }
.emap-track-name { font-weight: 500; font-size: 0.9rem; }
.emap-track-meta { font-size: 0.8rem; color: var(--color-text); }
.emap-checkbox {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) 0;
    cursor: pointer;
    font-size: 0.9rem;
}
.emap-checkbox input { width: 16px; height: 16px; }
/* Segments list */
.emap-segments-list {
    max-height: 200px;
    overflow-y: auto;
}
.emap-segment-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) 0;
    cursor: pointer;
    transition: background 0.2s;
    text-decoration: none;
    color: inherit;
}
.emap-segment-item:hover .emap-segment-name { color: var(--color-accent); text-decoration: underline; }
.emap-segment-item.active { background: rgba(97, 206, 112, 0.1); padding-left: var(--space-xs); padding-right: var(--space-xs); border-radius: var(--radius-sm); }
.emap-segment-icon { width: 14px; height: 14px; flex-shrink: 0; color: var(--color-text-secondary); }
.emap-segment-info { flex: 1; min-width: 0; }
.emap-segment-name { font-size: 0.85rem; font-weight: 500; display: flex; align-items: center; gap: 4px; }
.emap-segment-sponsor { height: 16px; width: auto; max-width: 50px; object-fit: contain; }
.emap-segment-meta { font-size: 0.7rem; color: var(--color-text-secondary); }
.emap-segment-dot {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    flex-shrink: 0;
}
/* POI items - mobile overrides handled by main styles above */
.emap-location-btn {
    position: absolute;
    bottom: var(--space-lg);
    right: var(--space-md);
    width: 44px;
    height: 44px;
    background: white;
    border: none;
    border-radius: 50%;
    box-shadow: var(--shadow-md);
    cursor: pointer;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    transition: all 0.2s;
}
.emap-location-btn:hover { background: var(--color-border); }
.emap-location-btn.active { background: var(--color-accent); color: white; }
.emap-location-btn.loading { animation: emap-pulse 1s infinite; }
@keyframes emap-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
.emap-elevation {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255,255,255,0.97);
    backdrop-filter: blur(10px);
    z-index: 90;
    transition: transform 0.3s ease;
}
.emap-elevation.collapsed {
    transform: translateY(calc(100% - 40px));
}
.emap-elevation-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 40px;
    cursor: pointer;
    border-bottom: 1px solid var(--color-border);
    font-size: 0.85rem;
    font-weight: 500;
    gap: var(--space-sm);
}
.emap-elevation-toggle .chevron {
    transition: transform 0.3s;
}
.emap-title-sponsor {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-weight: 400;
    font-style: italic;
    color: var(--color-text);
    margin-left: 4px;
}
.emap-title-sponsor img {
    height: 18px;
    width: auto;
    max-width: 60px;
    object-fit: contain;
    vertical-align: middle;
}
.emap-elevation.collapsed .emap-elevation-toggle .chevron {
    transform: rotate(180deg);
}
.emap-elevation-clear {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    margin-left: auto;
    color: var(--color-text);
    opacity: 0.7;
}
.emap-elevation-clear:hover { opacity: 1; }
.emap-elevation-content {
    height: 120px;
    padding: var(--space-sm);
}
.emap-elevation canvas { width: 100%; height: 100%; }
.emap-close {
    position: absolute;
    top: var(--space-md);
    right: var(--space-md);
    width: 40px;
    height: 40px;
    background: rgba(255,255,255,0.97);
    border: none;
    border-radius: 50%;
    box-shadow: var(--shadow-md);
    cursor: pointer;
    z-index: 100;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
<?php if ($fullscreen): ?>
@media (max-width: 768px) {
    .emap-close {
        position: fixed;
        top: auto;
        bottom: var(--space-lg);
        right: 60px;
    }
    .emap-location-btn {
        position: fixed;
        bottom: var(--space-lg);
        right: var(--space-md);
    }
    /* Gold icons on mobile bottom buttons */
    .emap-location-btn,
    .emap-close {
        background: rgba(0, 0, 0, 0.75);
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    .emap-location-btn svg,
    .emap-close svg,
    .emap-location-btn i,
    .emap-close i {
        color: #FFD700 !important;
    }
    .emap-location-btn:hover,
    .emap-close:hover {
        background: rgba(0, 0, 0, 0.85);
    }
    .emap-location-btn.active {
        background: rgba(255, 215, 0, 0.2);
        border-color: #FFD700;
    }
    .emap-elevation {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
    }
    .emap-mobile-controls {
        position: fixed;
        top: var(--space-sm);
        left: var(--space-sm);
        right: var(--space-sm);
    }
}
<?php endif; ?>
@media (max-width: 768px) {
    .emap-elevation.collapsed {
        transform: translateY(calc(100% - 36px));
    }
    .emap-elevation-toggle { height: 36px; }
    .emap-elevation-content { height: 100px; }
}
/* Sponsor Banner */
.emap-sponsor-banner {
    position: absolute;
    top: var(--space-sm);
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-radius: var(--radius-md);
    padding: var(--space-xs) var(--space-md);
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.emap-sponsor-banner a {
    display: flex;
    align-items: center;
}
.emap-sponsor-banner img {
    max-height: 40px;
    max-width: 150px;
    object-fit: contain;
}
.emap-sponsor-close {
    background: none;
    border: none;
    cursor: pointer;
    padding: var(--space-2xs);
    color: var(--color-text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
}
.emap-sponsor-close:hover {
    background: var(--color-bg-secondary);
    color: var(--color-text);
}
@media (max-width: 768px) {
    .emap-sponsor-banner {
        top: auto;
        bottom: 150px;
        left: var(--space-sm);
        right: var(--space-sm);
        transform: none;
        justify-content: center;
    }
}
</style>

<div class="emap-container" id="<?= $mapId ?>-container">
    <!-- Desktop Sidebar -->
    <div class="emap-sidebar">
        <div class="emap-sidebar-header">
            <strong><?= htmlspecialchars($eventName) ?></strong>
            <?php if (!empty($tracks)): ?>
            <div style="font-size: 0.85rem; color: var(--color-text); margin-top: var(--space-2xs);">
                <?= number_format($tracks[0]['total_distance_km'], 1) ?> km · <?= number_format($tracks[0]['total_elevation_m']) ?>m
            </div>
            <?php endif; ?>
        </div>
        <div class="emap-sidebar-body">
            <?php if (count($tracks) > 1): ?>
            <div class="emap-section">
                <div class="emap-section-title">Banor</div>
                <?php foreach ($tracks as $i => $track): ?>
                <div class="emap-track-item <?= $track['is_primary'] ? 'active' : '' ?>"
                     data-track-id="<?= $track['id'] ?>"
                     onclick="<?= $mapId ?>_toggleTrack(<?= $track['id'] ?>)">
                    <span class="emap-track-dot" style="background: <?= htmlspecialchars($track['color'] ?? '#3B82F6') ?>;"></span>
                    <div class="emap-track-info">
                        <div class="emap-track-name"><?= htmlspecialchars($track['route_label'] ?? $track['name']) ?></div>
                        <div class="emap-track-meta"><?= number_format($track['total_distance_km'], 1) ?> km</div>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>

            <?php
            // Get segments for display
            $allSegments = [];
            foreach ($tracks as $track) {
                if (!empty($track['segments'])) {
                    foreach ($track['segments'] as $seg) {
                        $allSegments[] = $seg;
                    }
                }
            }
            ?>
            <?php if (!empty($allSegments)): ?>
            <details class="emap-collapsible" open>
                <summary class="emap-collapsible-header">
                    <i data-lucide="chevron-down" class="emap-collapse-icon"></i>
                    <i data-lucide="route"></i>
                    <span>Sträckor (<?= count($allSegments) ?>)</span>
                </summary>
                <div class="emap-collapsible-content">
                    <?php foreach ($allSegments as $seg):
                        $segType = $seg['segment_type'] ?? 'liaison';
                        $segColor = $seg['color'] ?? ($segType === 'stage' ? '#EF4444' : ($segType === 'lift' ? '#F59E0B' : '#61CE70'));
                        $segName = $seg['segment_name'] ?? ($segType === 'stage' ? 'SS' : 'Transport');
                        $segDist = number_format($seg['distance_km'] ?? 0, 1);
                        $segIconName = $segType === 'stage' ? 'flag' : ($segType === 'lift' ? 'cable-car' : 'route');
                        $segHeight = $segType === 'stage'
                            ? ($seg['elevation_loss_m'] ?? 0)
                            : ($seg['elevation_gain_m'] ?? 0);
                        $segHeightLabel = $segType === 'stage' ? 'fhm' : 'hm';
                        $segSponsorName = $seg['sponsor_name'] ?? null;
                        $segSponsorLogo = $seg['sponsor_logo'] ?? null;
                        $segSponsorUrl = $seg['sponsor_website'] ?? null;
                        $segDisplayName = $segSponsorName ? ($segName . ' By ' . $segSponsorName) : $segName;
                    ?>
                    <div class="emap-segment-item" onclick="<?= $mapId ?>_zoomToSegment(<?= $seg['id'] ?? 0 ?>, <?= $segSponsorLogo ? "'" . htmlspecialchars(addslashes($segSponsorLogo)) . "'" : 'null' ?>, <?= $segSponsorUrl ? "'" . htmlspecialchars(addslashes($segSponsorUrl)) . "'" : 'null' ?>)" data-segment-id="<?= $seg['id'] ?? 0 ?>">
                        <span class="emap-segment-dot" style="background: <?= $segColor ?>;"></span>
                        <div class="emap-segment-info">
                            <div class="emap-segment-name">
                                <?= htmlspecialchars($segName) ?>
                                <?php if ($segSponsorName): ?>
                                <span style="color: var(--color-text-secondary); font-weight: 400; font-size: 0.75rem;">By <?= htmlspecialchars($segSponsorName) ?></span>
                                <?php endif; ?>
                            </div>
                            <div class="emap-segment-meta"><?= $segDist ?> km · <?= $segHeight ?> <?= $segHeightLabel ?></div>
                        </div>
                    </div>
                    <?php endforeach; ?>
                </div>
            </details>
            <?php endif; ?>

            <?php if (!empty($pois)): ?>
            <details class="emap-collapsible">
                <summary class="emap-collapsible-header">
                    <i data-lucide="chevron-down" class="emap-collapse-icon"></i>
                    <i data-lucide="map-pin"></i>
                    <span>Platser (<?= count($pois) ?>)</span>
                </summary>
                <div class="emap-collapsible-content">
                    <?php foreach ($pois as $poi):
                        $poiIcon = $poiIconMap[$poi['poi_type']] ?? ($poi['type_icon'] ?? 'map-pin');
                        $poiLabel = $poi['label'] ?: ($poi['type_label'] ?? $poi['poi_type']);
                    ?>
                    <div class="emap-poi-item" onclick="<?= $mapId ?>_zoomToPoi(<?= $poi['lat'] ?>, <?= $poi['lng'] ?>)">
                        <i data-lucide="<?= htmlspecialchars($poiIcon) ?>"></i>
                        <span><?= htmlspecialchars($poiLabel) ?></span>
                    </div>
                    <?php endforeach; ?>
                </div>
            </details>
            <?php endif; ?>
        </div>
    </div>

    <!-- Main content area (map + elevation) -->
    <div class="emap-main">
        <div class="emap-map" id="<?= $mapId ?>"></div>

        <!-- Sponsor Banner -->
        <div class="emap-sponsor-banner" id="<?= $mapId ?>-sponsor-banner" class="hidden">
        <a id="<?= $mapId ?>-sponsor-link" href="#" target="_blank" rel="noopener">
            <img id="<?= $mapId ?>-sponsor-logo" src="" alt="Sponsor">
        </a>
        <button type="button" class="emap-sponsor-close" onclick="<?= $mapId ?>_hideSponsorBanner()">
            <i data-lucide="x" style="width: 14px; height: 14px;"></i>
        </button>
    </div>

    <!-- Mobile Controls -->
    <div class="emap-mobile-controls">
        <?php if (count($tracks) > 1): ?>
        <div class="emap-dropdown" id="<?= $mapId ?>-track-dropdown">
            <button class="emap-dropdown-btn" onclick="<?= $mapId ?>_toggleDropdown('<?= $mapId ?>-track-dropdown')">
                <span class="dot" id="<?= $mapId ?>-current-dot" style="background: <?= htmlspecialchars($tracks[0]['color'] ?? '#3B82F6') ?>;"></span>
                <span id="<?= $mapId ?>-current-name"><?= htmlspecialchars($tracks[0]['route_label'] ?? $tracks[0]['name']) ?></span>
                <i data-lucide="chevron-down" style="width: 12px; height: 12px;"></i>
            </button>
            <div class="emap-dropdown-menu">
                <?php foreach ($tracks as $track): ?>
                <div class="emap-dropdown-item <?= $track['is_primary'] ? 'active' : '' ?>"
                     data-track-id="<?= $track['id'] ?>"
                     onclick="<?= $mapId ?>_selectTrack(<?= $track['id'] ?>, '<?= htmlspecialchars(addslashes($track['route_label'] ?? $track['name'])) ?>', '<?= $track['color'] ?? '#3B82F6' ?>')">
                    <span class="dot" style="background: <?= htmlspecialchars($track['color'] ?? '#3B82F6') ?>; width: 12px; height: 12px; border-radius: 3px;"></span>
                    <?= htmlspecialchars($track['route_label'] ?? $track['name']) ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>

        <?php if (!empty($poiGroups)): ?>
        <div class="emap-dropdown" id="<?= $mapId ?>-poi-dropdown">
            <button class="emap-dropdown-btn" onclick="<?= $mapId ?>_toggleDropdown('<?= $mapId ?>-poi-dropdown')">
                <i data-lucide="map-pin" style="width: 14px; height: 14px;"></i> POIs <i data-lucide="chevron-down" style="width: 12px; height: 12px;"></i>
            </button>
            <div class="emap-dropdown-menu">
                <?php foreach ($poiGroups as $type => $group): ?>
                <div class="emap-dropdown-item active" data-poi-type="<?= htmlspecialchars($type) ?>" onclick="<?= $mapId ?>_togglePoiTypeMobile('<?= htmlspecialchars($type) ?>', this)">
                    <input type="checkbox" checked style="pointer-events: none;">
                    <i data-lucide="<?= htmlspecialchars($group['icon']) ?>" style="width: 14px; height: 14px;"></i> <?= htmlspecialchars($group['label']) ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>

        <?php if (!empty($allSegments)): ?>
        <div class="emap-dropdown" id="<?= $mapId ?>-segment-dropdown">
            <button class="emap-dropdown-btn" onclick="<?= $mapId ?>_toggleDropdown('<?= $mapId ?>-segment-dropdown')">
                <i data-lucide="list" style="width: 14px; height: 14px;"></i> Sektioner <i data-lucide="chevron-down" style="width: 12px; height: 12px;"></i>
            </button>
            <div class="emap-dropdown-menu emap-dropdown-scrollable">
                <?php foreach ($allSegments as $seg):
                    $segType = $seg['segment_type'] ?? 'liaison';
                    $segColor = $seg['color'] ?? ($segType === 'stage' ? '#EF4444' : ($segType === 'lift' ? '#F59E0B' : '#61CE70'));
                    $segName = $seg['segment_name'] ?? ($segType === 'stage' ? 'SS' : 'Transport');
                    $segIconName = $segType === 'stage' ? 'flag' : ($segType === 'lift' ? 'cable-car' : 'route');
                    $segHeight = $segType === 'stage' ? ($seg['elevation_loss_m'] ?? 0) : ($seg['elevation_gain_m'] ?? 0);
                    $segHeightLabel = $segType === 'stage' ? 'fhm' : 'hm';
                    $segSponsorName = $seg['sponsor_name'] ?? null;
                    $segDisplayName = $segSponsorName ? ($segName . ' By ' . $segSponsorName) : $segName;
                ?>
                <div class="emap-dropdown-item" data-segment-id="<?= $seg['id'] ?? 0 ?>" onclick="<?= $mapId ?>_zoomToSegment(<?= $seg['id'] ?? 0 ?>); <?= $mapId ?>_toggleDropdown('<?= $mapId ?>-segment-dropdown')">
                    <span class="dot" style="background: <?= $segColor ?>; width: 10px; height: 10px; border-radius: 2px;"></span>
                    <span style="flex: 1;"><?= htmlspecialchars($segDisplayName) ?></span>
                    <span style="font-size: 0.7rem; color: var(--color-text);"><?= $segHeight ?> <?= $segHeightLabel ?></span>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>
    </div>

    <!-- Location Button -->
    <button class="emap-location-btn" id="<?= $mapId ?>-location-btn" onclick="<?= $mapId ?>_toggleLocation()" title="Min plats">
        <i data-lucide="crosshair" style="width: 20px; height: 20px;"></i>
    </button>

    <?php if ($showClose): ?>
    <button class="emap-close" onclick="history.back()" title="Tillbaka">
        <i data-lucide="x" style="width: 20px; height: 20px;"></i>
    </button>
    <?php endif; ?>

    <!-- Elevation Profile -->
    <?php if (!empty($tracks)): ?>
    <div class="emap-elevation collapsed" id="<?= $mapId ?>-elevation">
        <div class="emap-elevation-toggle" onclick="<?= $mapId ?>_toggleElevation()">
            <i data-lucide="chevron-up" class="chevron" style="width: 16px; height: 16px;"></i>
            <span id="<?= $mapId ?>-elevation-title">Höjdprofil</span>
            <button class="emap-elevation-clear" id="<?= $mapId ?>-elevation-clear" onclick="event.stopPropagation(); <?= $mapId ?>_clearSegmentSelection()" class="hidden">
                <i data-lucide="x" style="width: 14px; height: 14px;"></i>
            </button>
        </div>
        <div class="emap-elevation-content">
            <canvas id="<?= $mapId ?>-canvas"></canvas>
        </div>
    </div>
    <?php endif; ?>
    </div><!-- /.emap-main -->
</div><!-- /.emap-container -->

<script>
(function() {
    const mapId = '<?= $mapId ?>';
    const mapData = <?= json_encode($mapData) ?>;
    let map, trackLayers = {}, poiLayers = {};
    let selectedSegmentId = null; // Track selected segment for elevation profile
    let locationMarker, locationCircle, watchId;
    let visibleTracks = new Set();
    let visiblePoiTypes = new Set();

    function init() {
        map = L.map(mapId, { zoomControl: false }).setView([62, 15], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
        L.control.zoom({ position: 'bottomleft' }).addTo(map);

        // Draw tracks
        if (mapData.tracks) {
            mapData.tracks.forEach(track => {
                const layer = L.layerGroup();
                if (track.geojson && track.geojson.features) {
                    L.geoJSON(track.geojson, {
                        style: f => ({
                            color: f.properties.color || track.color || '#3B82F6',
                            weight: 4,
                            opacity: 0.9
                        }),
                        onEachFeature: (feature, layer) => {
                            if (feature.properties.name) {
                                layer.bindPopup('<strong>' + feature.properties.name + '</strong><br>' + feature.properties.distance_km + ' km');
                            }
                        }
                    }).addTo(layer);
                }
                trackLayers[track.id] = layer;
                if (track.is_primary) {
                    layer.addTo(map);
                    visibleTracks.add(track.id);
                }
            });
        }

        // POI icon SVGs
        const poiIcons = {
            parking: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.5 2.8c-.4.6-.6 1.3-.6 2V16c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
            start: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2"><polygon points="6 3 20 12 6 21 6 3"/></svg>',
            finish: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/></svg>',
            food: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3"/><path d="M18 22v-7"/></svg>',
            water: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/></svg>',
            wc: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M13 4h3a2 2 0 0 1 2 2v14"/><path d="M2 20h3"/><path d="M13 20h9"/><path d="M10 12v.01"/><path d="M13 4.562v16.157a1 1 0 0 1-1.242.97L5 20V5.562a2 2 0 0 1 1.515-1.94l4-1A2 2 0 0 1 13 4.562Z"/></svg>',
            toilet: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M13 4h3a2 2 0 0 1 2 2v14"/><path d="M2 20h3"/><path d="M13 20h9"/><path d="M10 12v.01"/><path d="M13 4.562v16.157a1 1 0 0 1-1.242.97L5 20V5.562a2 2 0 0 1 1.515-1.94l4-1A2 2 0 0 1 13 4.562Z"/></svg>',
            medical: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M11 2a2 2 0 0 0-2 2v5H4a2 2 0 0 0-2 2v2c0 1.1.9 2 2 2h5v5c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2v-5h5a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-5V4a2 2 0 0 0-2-2h-2z"/></svg>',
            first_aid: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M11 2a2 2 0 0 0-2 2v5H4a2 2 0 0 0-2 2v2c0 1.1.9 2 2 2h5v5c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2v-5h5a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-5V4a2 2 0 0 0-2-2h-2z"/></svg>',
            info: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
            camping: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M3.5 21 14 3"/><path d="M20.5 21 10 3"/><path d="M15.5 21 12 15l-3.5 6"/><path d="M2 21h20"/></svg>',
            lift: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M4 4h16"/><path d="M6 4v16"/><path d="M18 4v16"/><rect x="8" y="8" width="8" height="6" rx="1"/></svg>',
            default: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>'
        };

        function getPoiIcon(type) {
            return poiIcons[type] || poiIcons.default;
        }

        // Draw POIs
        if (mapData.pois) {
            mapData.pois.forEach(poi => {
                const type = poi.poi_type;
                if (!poiLayers[type]) {
                    poiLayers[type] = L.layerGroup().addTo(map);
                    visiblePoiTypes.add(type);
                }
                const iconSvg = getPoiIcon(type);
                const marker = L.marker([poi.lat, poi.lng], {
                    icon: L.divIcon({
                        className: 'emap-poi-marker',
                        html: '<div style="width: 32px; height: 32px; background: var(--color-accent, #61CE70); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">' + iconSvg + '</div>',
                        iconSize: [32, 32],
                        iconAnchor: [16, 16]
                    })
                }).bindPopup('<strong>' + (poi.label || poi.type_label || poi.poi_type) + '</strong>' + (poi.description ? '<br>' + poi.description : ''));
                marker.addTo(poiLayers[type]);
            });
        }

        if (mapData.bounds) map.fitBounds(mapData.bounds, { padding: [50, 50] });
        updateElevation();

        // Close dropdowns on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.emap-dropdown')) {
                document.querySelectorAll('.emap-dropdown.open').forEach(d => d.classList.remove('open'));
            }
        });
    }

    window[mapId + '_toggleTrack'] = function(trackId) {
        const layer = trackLayers[trackId];
        if (!layer) return;
        const item = document.querySelector('#' + mapId + '-container [data-track-id="' + trackId + '"]');
        if (visibleTracks.has(trackId)) {
            map.removeLayer(layer);
            visibleTracks.delete(trackId);
            if (item) item.classList.remove('active');
        } else {
            layer.addTo(map);
            visibleTracks.add(trackId);
            if (item) item.classList.add('active');
        }
        updateElevation();
    };

    window[mapId + '_selectTrack'] = function(trackId, name, color) {
        Object.keys(trackLayers).forEach(id => {
            const layer = trackLayers[id];
            const intId = parseInt(id);
            if (intId === trackId) {
                if (!map.hasLayer(layer)) layer.addTo(map);
                visibleTracks.add(intId);
            } else {
                if (map.hasLayer(layer)) map.removeLayer(layer);
                visibleTracks.delete(intId);
            }
        });
        // Zoom to selected track bounds
        const selectedLayer = trackLayers[trackId];
        if (selectedLayer && selectedLayer.getBounds) {
            const bounds = selectedLayer.getBounds();
            if (bounds.isValid()) {
                map.fitBounds(bounds, { padding: [50, 50] });
            }
        }
        document.getElementById(mapId + '-current-name').textContent = name;
        document.getElementById(mapId + '-current-dot').style.background = color;
        document.querySelectorAll('#' + mapId + '-track-dropdown .emap-dropdown-item').forEach(item => {
            item.classList.toggle('active', parseInt(item.dataset.trackId) === trackId);
        });
        document.getElementById(mapId + '-track-dropdown').classList.remove('open');
        updateElevation();
    };

    window[mapId + '_togglePoiType'] = function(type) {
        const layer = poiLayers[type];
        if (!layer) return;
        if (visiblePoiTypes.has(type)) {
            map.removeLayer(layer);
            visiblePoiTypes.delete(type);
        } else {
            layer.addTo(map);
            visiblePoiTypes.add(type);
        }
    };

    window[mapId + '_togglePoiTypeMobile'] = function(type, el) {
        window[mapId + '_togglePoiType'](type);
        el.classList.toggle('active');
        el.querySelector('input').checked = visiblePoiTypes.has(type);
    };

    window[mapId + '_toggleDropdown'] = function(id) {
        const dropdown = document.getElementById(id);
        const wasOpen = dropdown.classList.contains('open');
        document.querySelectorAll('.emap-dropdown.open').forEach(d => d.classList.remove('open'));
        if (!wasOpen) dropdown.classList.add('open');
    };

    // Hide sponsor banner
    window[mapId + '_hideSponsorBanner'] = function() {
        const banner = document.getElementById(mapId + '-sponsor-banner');
        if (banner) banner.style.display = 'none';
    };

    // Show sponsor banner
    function showSponsorBanner(logoUrl, websiteUrl) {
        const banner = document.getElementById(mapId + '-sponsor-banner');
        const logo = document.getElementById(mapId + '-sponsor-logo');
        const link = document.getElementById(mapId + '-sponsor-link');
        if (!banner || !logo || !logoUrl) {
            if (banner) banner.style.display = 'none';
            return;
        }
        // Handle both media library paths and legacy paths
        let fullPath = logoUrl;
        if (logoUrl.startsWith('uploads/')) {
            fullPath = '/' + logoUrl;
        } else if (!logoUrl.startsWith('/')) {
            fullPath = '/uploads/sponsors/' + logoUrl;
        }
        logo.src = fullPath;
        if (link && websiteUrl) {
            link.href = websiteUrl;
            link.style.pointerEvents = 'auto';
        } else if (link) {
            link.href = '#';
            link.style.pointerEvents = 'none';
        }
        banner.style.display = 'flex';
        // Re-init Lucide icons for the close button
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    // Zoom to segment by ID
    window[mapId + '_zoomToSegment'] = function(segmentId, sponsorLogo, sponsorUrl) {
        if (!mapData.tracks) return;
        for (const track of mapData.tracks) {
            if (!track.segments) continue;
            for (const seg of track.segments) {
                if (seg.id == segmentId && seg.coordinates && seg.coordinates.length) {
                    const bounds = L.latLngBounds(seg.coordinates.map(c => [c.lat, c.lng]));
                    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
                    // Highlight segment in list
                    document.querySelectorAll('.emap-segment-item, .emap-dropdown-item[data-segment-id]').forEach(el => el.classList.remove('active'));
                    document.querySelectorAll('[data-segment-id="' + segmentId + '"]').forEach(el => el.classList.add('active'));
                    // Lock elevation profile to this segment
                    selectedSegmentId = segmentId;
                    // Update title with sponsor logo if available
                    const segSponsorName = seg.sponsor_name;
                    const segSponsorLogo = sponsorLogo || seg.sponsor_logo;
                    const segName = seg.segment_name || (seg.segment_type === 'stage' ? 'SS' : 'Transport');
                    const titleEl = document.getElementById(mapId + '-elevation-title');
                    const clearBtn = document.getElementById(mapId + '-elevation-clear');
                    if (titleEl) {
                        if (segSponsorName) {
                            titleEl.innerHTML = segName + ' <span class="emap-title-sponsor">By ' + segSponsorName + '</span>';
                        } else {
                            titleEl.textContent = segName;
                        }
                    }
                    if (clearBtn) clearBtn.style.display = 'block';
                    // Show sponsor banner if logo exists
                    const logoToShow = segSponsorLogo;
                    const urlToShow = sponsorUrl || seg.sponsor_website;
                    if (logoToShow) {
                        showSponsorBanner(logoToShow, urlToShow);
                    } else {
                        window[mapId + '_hideSponsorBanner']();
                    }
                    // Open elevation panel and update
                    const elevPanel = document.getElementById(mapId + '-elevation');
                    if (elevPanel) {
                        elevPanel.classList.remove('collapsed');
                        setTimeout(updateElevation, 100);
                    }
                    return;
                }
            }
        }
    };

    // Clear segment selection (show full track profile)
    window[mapId + '_clearSegmentSelection'] = function() {
        selectedSegmentId = null;
        document.querySelectorAll('.emap-segment-item, .emap-dropdown-item[data-segment-id]').forEach(el => el.classList.remove('active'));
        // Reset title and hide clear button
        const titleEl = document.getElementById(mapId + '-elevation-title');
        const clearBtn = document.getElementById(mapId + '-elevation-clear');
        if (titleEl) titleEl.textContent = 'Höjdprofil';
        if (clearBtn) clearBtn.style.display = 'none';
        // Hide sponsor banner
        window[mapId + '_hideSponsorBanner']();
        updateElevation();
    };

    // Zoom to POI by coordinates
    window[mapId + '_zoomToPoi'] = function(lat, lng) {
        map.setView([lat, lng], 16);
    };

    window[mapId + '_toggleLocation'] = function() {
        const btn = document.getElementById(mapId + '-location-btn');
        if (watchId) {
            navigator.geolocation.clearWatch(watchId);
            watchId = null;
            if (locationMarker) map.removeLayer(locationMarker);
            if (locationCircle) map.removeLayer(locationCircle);
            locationMarker = locationCircle = null;
            btn.classList.remove('active', 'loading');
            return;
        }
        if (!navigator.geolocation) { alert('Geolocation stöds inte'); return; }
        btn.classList.add('loading');
        watchId = navigator.geolocation.watchPosition(
            (pos) => {
                const { latitude, longitude, accuracy } = pos.coords;
                btn.classList.remove('loading');
                btn.classList.add('active');
                if (!locationMarker) {
                    locationMarker = L.circleMarker([latitude, longitude], {
                        radius: 8, fillColor: '#3B82F6', fillOpacity: 1, color: 'white', weight: 3
                    }).addTo(map);
                    locationCircle = L.circle([latitude, longitude], {
                        radius: accuracy, fillColor: '#3B82F6', fillOpacity: 0.1, color: '#3B82F6', weight: 1
                    }).addTo(map);
                    map.setView([latitude, longitude], 15);
                } else {
                    locationMarker.setLatLng([latitude, longitude]);
                    locationCircle.setLatLng([latitude, longitude]).setRadius(accuracy);
                }
            },
            (err) => { btn.classList.remove('loading'); alert('Kunde inte hämta position'); },
            { enableHighAccuracy: true, maximumAge: 10000 }
        );
    };

    window[mapId + '_toggleElevation'] = function() {
        document.getElementById(mapId + '-elevation').classList.toggle('collapsed');
        setTimeout(updateElevation, 350);
    };

    function updateElevation() {
        const canvas = document.getElementById(mapId + '-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width * 2;
        canvas.height = rect.height * 2;
        ctx.scale(2, 2);

        let allElevations = [], allDistances = [];
        let segmentName = null;

        if (mapData.tracks) {
            mapData.tracks.forEach(track => {
                if (!visibleTracks.has(track.id)) return;
                (track.segments || []).forEach(seg => {
                    // If a segment is selected, only show that segment
                    if (selectedSegmentId !== null && seg.id != selectedSegmentId) return;

                    if (selectedSegmentId !== null && seg.id == selectedSegmentId) {
                        segmentName = seg.segment_name || (seg.segment_type === 'stage' ? 'SS' : 'Transport');
                    }

                    const elevData = seg.elevation_data || [];
                    const coords = seg.coordinates || [];
                    let dist = allDistances.length > 0 ? allDistances[allDistances.length - 1] : 0;
                    coords.forEach((coord, i) => {
                        if (i > 0) {
                            const prev = coords[i-1];
                            dist += haversine(prev.lat, prev.lng, coord.lat, coord.lng);
                        }
                        allDistances.push(dist);
                        allElevations.push(elevData[i] ?? coord.ele ?? 0);
                    });
                });
            });
        }

        if (allElevations.length < 2) {
            ctx.fillStyle = '#999';
            ctx.font = '12px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Ingen höjddata', rect.width / 2, rect.height / 2);
            return;
        }

        const minEle = Math.min(...allElevations);
        const maxEle = Math.max(...allElevations);
        const maxDist = Math.max(...allDistances);
        const eleRange = maxEle - minEle || 1;
        const padding = { top: 10, right: 10, bottom: 20, left: 40 };
        const w = rect.width - padding.left - padding.right;
        const h = rect.height - padding.top - padding.bottom;

        ctx.fillStyle = 'rgba(97, 206, 112, 0.3)';
        ctx.strokeStyle = '#61CE70';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(padding.left, padding.top + h);
        allDistances.forEach((dist, i) => {
            const x = padding.left + (dist / maxDist) * w;
            const y = padding.top + h - ((allElevations[i] - minEle) / eleRange) * h;
            ctx.lineTo(x, y);
        });
        ctx.lineTo(padding.left + w, padding.top + h);
        ctx.closePath();
        ctx.fill();

        ctx.beginPath();
        allDistances.forEach((dist, i) => {
            const x = padding.left + (dist / maxDist) * w;
            const y = padding.top + h - ((allElevations[i] - minEle) / eleRange) * h;
            if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        });
        ctx.stroke();

        ctx.fillStyle = '#666';
        ctx.font = '10px sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(Math.round(maxEle) + ' m', padding.left - 4, padding.top + 10);
        ctx.fillText(Math.round(minEle) + ' m', padding.left - 4, padding.top + h);
        ctx.textAlign = 'center';
        ctx.fillText('0 km', padding.left, padding.top + h + 14);
        ctx.fillText(maxDist.toFixed(1) + ' km', padding.left + w, padding.top + h + 14);
    }

    function haversine(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon/2) * Math.sin(dLon/2);
        return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            init();
            if (typeof lucide !== 'undefined') lucide.createIcons();
        });
    } else {
        init();
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
    window.addEventListener('resize', () => setTimeout(updateElevation, 100));
})();
</script>
        <?php
    }
}

/**
 * Output Leaflet.js dependencies
 */
if (!function_exists('render_map_head')) {
    function render_map_head(): void {
        ?>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
        <?php
    }
}

/**
 * Output Leaflet.js scripts
 */
if (!function_exists('render_map_scripts')) {
    function render_map_scripts(): void {
        ?>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
        <?php
    }
}
