<?php
/**
 * Media Library - Admin Page
 * TheHUB V3 - Media & Sponsor System
 *
 * Upload, browse, and manage media files
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/media-functions.php';
require_admin();

global $pdo;

// Check if promotor - they get filtered view
$isPromotorOnly = isRole('promotor');
$promotorEventSlugs = [];
$promotorAllowedFolders = [];

if ($isPromotorOnly && $pdo) {
    // Get promotor's events and their folder slugs
    try {
        $promotorEvents = getPromotorEvents();
        $promotorSeriesSlugs = []; // Track series for series-level access
        foreach ($promotorEvents as $event) {
            // Get series info for folder path
            $eventInfo = $pdo->prepare("
                SELECT e.name as event_name, s.short_name as series_short, s.name as series_name
                FROM events e
                LEFT JOIN series s ON e.series_id = s.id
                WHERE e.id = ?
            ");
            $eventInfo->execute([$event['id']]);
            $info = $eventInfo->fetch(PDO::FETCH_ASSOC);
            if ($info) {
                $seriesSlug = slugify($info['series_short'] ?: $info['series_name'] ?: 'general');
                $eventSlug = slugify($info['event_name']);
                // Add event-specific folder
                $promotorAllowedFolders[] = "sponsors/{$seriesSlug}/{$eventSlug}";
                $promotorEventSlugs[] = $eventSlug;
                // Also allow series-level folder access
                if (!in_array($seriesSlug, $promotorSeriesSlugs)) {
                    $promotorSeriesSlugs[] = $seriesSlug;
                    $promotorAllowedFolders[] = "sponsors/{$seriesSlug}";
                }
            }
        }
    } catch (Exception $e) {
        error_log("Promotor folder access error: " . $e->getMessage());
    }
}

// Get current folder from query
$currentFolder = $_GET['folder'] ?? null;
$searchQuery = $_GET['search'] ?? '';

// Check if we're in a subfolder
$isSubfolder = $currentFolder && strpos($currentFolder, '/') !== false;
$parentFolder = $isSubfolder ? explode('/', $currentFolder)[0] : null;

// Get folder statistics
$folderStats = get_media_stats();
$statsByFolder = [];
$totalFiles = 0;
$totalSize = 0;

foreach ($folderStats as $stat) {
    // For promotors, only count files in their allowed folders
    if ($isPromotorOnly && !empty($promotorAllowedFolders)) {
        $isAllowed = false;
        foreach ($promotorAllowedFolders as $allowed) {
            if (strpos($stat['folder'], $allowed) === 0 || $stat['folder'] === $allowed) {
                $isAllowed = true;
                break;
            }
        }
        if (!$isAllowed) {
            continue;
        }
    }

    // Group subfolders under parent for stats
    $mainFolder = explode('/', $stat['folder'])[0];
    if (!isset($statsByFolder[$mainFolder])) {
        $statsByFolder[$mainFolder] = ['count' => 0, 'total_size' => 0];
    }
    $statsByFolder[$mainFolder]['count'] += (int) $stat['count'];
    $statsByFolder[$mainFolder]['total_size'] += (int) $stat['total_size'];
    $totalFiles += (int) $stat['count'];
    $totalSize += (int) $stat['total_size'];
}

// Get subfolders if viewing sponsors folder
$sponsorSubfolders = [];
if ($currentFolder === 'sponsors' || $parentFolder === 'sponsors') {
    $sponsorSubfolders = get_media_subfolders('sponsors');

    // Filter subfolders for promotors
    if ($isPromotorOnly && !empty($promotorAllowedFolders)) {
        $sponsorSubfolders = array_filter($sponsorSubfolders, function($subfolder) use ($promotorAllowedFolders) {
            foreach ($promotorAllowedFolders as $allowed) {
                // $subfolder is array with 'name', 'path', 'count', 'size'
                // Check if subfolder path matches or is prefix of allowed path
                $subfolderPath = $subfolder['path'] ?? $subfolder['name'] ?? '';
                if ($subfolderPath === $allowed ||
                    strpos($allowed, $subfolderPath . '/') === 0 ||
                    strpos($subfolderPath, $allowed) === 0) {
                    return true;
                }
            }
            return false;
        });
    }
}

// Define folders - promotors only see sponsors
if ($isPromotorOnly) {
    $folders = [
        ['id' => 'sponsors', 'name' => 'Eventmedia', 'icon' => 'handshake']
    ];
    // Force promotors to sponsors folder - ALWAYS
    $currentFolder = 'sponsors';
} else {
    $folders = [
        ['id' => 'branding', 'name' => 'Branding', 'icon' => 'palette'],
        ['id' => 'general', 'name' => 'Allmänt', 'icon' => 'folder'],
        ['id' => 'series', 'name' => 'Serier', 'icon' => 'trophy'],
        ['id' => 'sponsors', 'name' => 'Sponsorer', 'icon' => 'handshake'],
        ['id' => 'ads', 'name' => 'Annonser', 'icon' => 'megaphone'],
        ['id' => 'clubs', 'name' => 'Klubbar', 'icon' => 'users'],
        ['id' => 'events', 'name' => 'Event', 'icon' => 'calendar']
    ];
}

// Add counts to folders
foreach ($folders as &$folder) {
    $folder['count'] = $statsByFolder[$folder['id']]['count'] ?? 0;
    $folder['size'] = format_file_size($statsByFolder[$folder['id']]['total_size'] ?? 0);
}
unset($folder);

// Get media files
if ($searchQuery) {
    $mediaFiles = search_media($searchQuery, $currentFolder, 100, true); // include subfolders
} else {
    // Include subfolders when viewing sponsors folder (to see event subfolders)
    $includeSubfolders = ($currentFolder === 'sponsors' || strpos($currentFolder, 'sponsors/') === 0);
    $mediaFiles = get_media_by_folder($currentFolder, 100, 0, $includeSubfolders);
}

// Filter media files for promotors - only show their event folders
if ($isPromotorOnly && !empty($mediaFiles)) {
    if (!empty($promotorAllowedFolders)) {
        $mediaFiles = array_filter($mediaFiles, function($file) use ($promotorAllowedFolders) {
            foreach ($promotorAllowedFolders as $allowed) {
                // Check if file is in an allowed folder or subfolder
                if (strpos($file['folder'], $allowed) === 0 || $file['folder'] === $allowed) {
                    return true;
                }
            }
            return false;
        });
        $mediaFiles = array_values($mediaFiles); // Re-index array
    } else {
        // Promotor has no events assigned - show empty
        $mediaFiles = [];
    }
}

// Page config
$page_title = 'Mediabibliotek';
$breadcrumbs = [
    ['label' => 'Mediabibliotek', 'url' => '/admin/media']
];

if ($currentFolder) {
    if ($isSubfolder) {
        // Add parent folder first
        $parentName = array_column($folders, 'name', 'id')[$parentFolder] ?? ucfirst($parentFolder);
        $breadcrumbs[] = ['label' => $parentName, 'url' => '/admin/media?folder=' . $parentFolder];
        // Add current subfolder
        $subfolderName = ucfirst(basename($currentFolder));
        $breadcrumbs[] = ['label' => $subfolderName];
    } else {
        $folderName = array_column($folders, 'name', 'id')[$currentFolder] ?? ucfirst($currentFolder);
        $breadcrumbs[] = ['label' => $folderName];
    }
}

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.media-layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: var(--space-lg);
}

@media (max-width: 768px) {
    .media-layout {
        grid-template-columns: 1fr;
    }
}

/* Sidebar */
.media-sidebar {
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    border: 1px solid var(--color-border);
    height: fit-content;
}

.folder-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.folder-item {
    display: flex;
    align-items: center;
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background 0.15s;
    margin-bottom: 2px;
    text-decoration: none;
    color: inherit;
}

.folder-item:hover {
    background: var(--color-bg-hover);
}

.folder-item.active {
    background: var(--color-accent);
    color: white;
}

.folder-icon {
    width: 20px;
    height: 20px;
    margin-right: var(--space-sm);
    opacity: 0.7;
}

.folder-item.active .folder-icon {
    opacity: 1;
}

.folder-name {
    flex: 1;
    font-weight: 500;
}

.folder-count {
    font-size: 0.75rem;
    background: var(--color-bg-sunken);
    padding: 2px 6px;
    border-radius: 10px;
    color: var(--color-text-secondary);
}

.folder-item.active .folder-count {
    background: rgba(255,255,255,0.2);
    color: white;
}

/* Upload area */
.upload-zone {
    background: var(--color-bg-surface);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-xl);
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: var(--space-lg);
}

.upload-zone:hover,
.upload-zone.dragover {
    border-color: var(--color-accent);
    background: var(--color-bg-hover);
}

.upload-zone-icon {
    width: 48px;
    height: 48px;
    margin: 0 auto var(--space-md);
    color: var(--color-text-secondary);
}

.upload-zone-text {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-xs);
}

.upload-zone-hint {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    opacity: 0.7;
}

/* Media grid */
.media-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: var(--space-md);
}

.media-item {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.15s;
    position: relative;
}

.media-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    border-color: var(--color-accent);
}

.media-item.selected {
    border-color: var(--color-accent);
    box-shadow: 0 0 0 2px var(--color-accent);
}

.media-thumbnail {
    aspect-ratio: 1;
    background: var(--color-bg-sunken);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.media-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.media-thumbnail-icon {
    width: 48px;
    height: 48px;
    color: var(--color-text-secondary);
}

.media-info {
    padding: var(--space-sm);
}

.media-filename {
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.media-meta {
    font-size: 0.65rem;
    color: var(--color-text-secondary);
    margin-top: 2px;
}

.media-checkbox {
    position: absolute;
    top: var(--space-xs);
    left: var(--space-xs);
    width: 20px;
    height: 20px;
    background: var(--color-bg-surface);
    border: 2px solid var(--color-border);
    border-radius: 4px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.15s;
}

.media-item:hover .media-checkbox,
.media-item.selected .media-checkbox {
    opacity: 1;
}

.media-item.selected .media-checkbox {
    background: var(--color-accent);
    border-color: var(--color-accent);
}

/* Toolbar */
.media-toolbar {
    display: flex;
    gap: var(--space-md);
    align-items: center;
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}

.media-search {
    flex: 1;
    min-width: 200px;
}

.media-search input {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-surface);
    color: var(--color-text-primary);
}

/* Stats bar */
.media-stats {
    display: flex;
    gap: var(--space-lg);
    padding: var(--space-sm) 0;
    margin-bottom: var(--space-md);
    border-bottom: 1px solid var(--color-border);
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

/* Modal */
.media-modal {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    padding: var(--space-lg);
    overflow-y: auto;
}

.media-modal.active {
    display: flex;
    align-items: center;
    justify-content: center;
}

.media-modal-content {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    max-width: 900px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
}

.media-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.media-modal-close {
    background: none;
    border: none;
    padding: var(--space-xs);
    cursor: pointer;
    color: var(--color-text-secondary);
}

.media-modal-body {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: var(--space-lg);
    padding: var(--space-lg);
}

@media (max-width: 768px) {
    .media-modal-body {
        grid-template-columns: 1fr;
    }
}

.media-preview {
    background: var(--color-bg-sunken);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 300px;
}

.media-preview img {
    max-width: 100%;
    max-height: 400px;
    object-fit: contain;
}

.media-details {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}

.media-detail-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.media-detail-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: var(--color-text-secondary);
    font-weight: 600;
}

.media-detail-value {
    font-size: 0.875rem;
}

.media-detail-input {
    padding: var(--space-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-sunken);
    color: var(--color-text-primary);
}

/* Empty state */
.media-empty {
    text-align: center;
    padding: var(--space-2xl);
    color: var(--color-text-secondary);
}

.media-empty-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto var(--space-md);
    opacity: 0.5;
}

/* Progress bar for uploads */
.upload-progress {
    display: none;
    margin-top: var(--space-md);
}

.upload-progress.active {
    display: block;
}

.progress-bar {
    height: 4px;
    background: var(--color-border);
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: var(--color-accent);
    width: 0;
    transition: width 0.3s;
}

.progress-text {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}
</style>

<div class="media-layout">
    <!-- Sidebar -->
    <aside class="media-sidebar">
        <h3 style="margin: 0 0 var(--space-md); font-size: 0.875rem; text-transform: uppercase; color: var(--color-text-secondary);">Mappar</h3>

        <ul class="folder-list">
            <?php if (!$isPromotorOnly): ?>
            <li>
                <a href="/admin/media" class="folder-item <?= $currentFolder === null ? 'active' : '' ?>">
                    <svg class="folder-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                    <span class="folder-name">Alla filer</span>
                    <span class="folder-count"><?= $totalFiles ?></span>
                </a>
            </li>
            <?php endif; ?>
            <?php foreach ($folders as $folder): ?>
            <li>
                <a href="/admin/media?folder=<?= $folder['id'] ?>" class="folder-item <?= $currentFolder === $folder['id'] || $parentFolder === $folder['id'] ? 'active' : '' ?>">
                    <svg class="folder-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                    <span class="folder-name"><?= htmlspecialchars($folder['name']) ?></span>
                    <span class="folder-count"><?= $folder['count'] ?></span>
                </a>
                <?php if ($folder['id'] === 'sponsors' && !empty($sponsorSubfolders)): ?>
                <!-- Sponsor subfolders -->
                <ul class="subfolder-list" style="margin-left: var(--space-md); margin-top: 2px;">
                    <?php foreach ($sponsorSubfolders as $sub): ?>
                    <li>
                        <a href="/admin/media?folder=<?= urlencode($sub['path']) ?>" class="folder-item <?= $currentFolder === $sub['path'] ? 'active' : '' ?>" style="padding: var(--space-xs) var(--space-sm); font-size: 0.8rem;">
                            <svg class="folder-icon" style="width: 14px; height: 14px;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                            <span class="folder-name"><?= htmlspecialchars(ucfirst($sub['name'])) ?></span>
                            <span class="folder-count" style="font-size: 0.65rem;"><?= $sub['count'] ?></span>
                        </a>
                    </li>
                    <?php endforeach; ?>
                </ul>
                <?php endif; ?>
            </li>
            <?php endforeach; ?>
        </ul>

        <div style="margin-top: var(--space-lg); padding-top: var(--space-md); border-top: 1px solid var(--color-border); font-size: 0.75rem; color: var(--color-text-secondary);">
            <strong>Totalt:</strong> <?= $totalFiles ?> filer<br>
            <strong>Storlek:</strong> <?= format_file_size($totalSize) ?>
        </div>
    </aside>

    <!-- Main content -->
    <div class="media-main">
        <!-- Upload zone -->
        <div class="upload-zone" id="uploadZone">
            <svg class="upload-zone-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" x2="12" y1="3" y2="15"/>
            </svg>
            <p class="upload-zone-text">Dra och släpp filer här eller klicka för att välja</p>
            <p class="upload-zone-hint">Max 10MB. Format: JPG, PNG, GIF, WebP, SVG, PDF</p>
            <p class="upload-zone-hint" style="margin-top: 4px; font-size: 0.7rem;">
                <strong>Rekommenderade storlekar:</strong> Banner 1200×150px · Logo 600×150px · Ikon 300×75px
            </p>
            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.gif,.webp,.svg,.pdf,image/jpeg,image/png,image/gif,image/webp,image/svg+xml,application/pdf" class="hidden">

            <div class="upload-progress" id="uploadProgress">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">Laddar upp...</div>
            </div>
        </div>

        <?php if ($currentFolder === 'sponsors'): ?>
        <!-- Create sponsor subfolder -->
        <div class="create-subfolder-box" style="background: var(--color-bg-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-md); margin-bottom: var(--space-lg);">
            <h4 style="margin: 0 0 var(--space-sm); font-size: 0.875rem; display: flex; align-items: center; gap: var(--space-sm);">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 10v6"/><path d="m15 13-3-3-3 3"/><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2v11z"/></svg>
                Skapa sponsor-mapp
            </h4>
            <p style="font-size: 0.8rem; color: var(--color-text-secondary); margin-bottom: var(--space-sm);">
                Skapa en undermapp för att organisera alla bilder för en sponsor.
            </p>
            <div style="display: flex; gap: var(--space-sm);">
                <input type="text" id="newSubfolderName" placeholder="Sponsornamn (t.ex. Husqvarna)" style="flex: 1; padding: var(--space-sm); border: 1px solid var(--color-border); border-radius: var(--radius-sm);">
                <button type="button" class="btn btn-primary" onclick="createSponsorSubfolder()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
                    Skapa
                </button>
            </div>
        </div>
        <?php endif; ?>

        <!-- Toolbar -->
        <div class="media-toolbar">
            <div class="media-search">
                <form method="get" action="/admin/media" style="display: flex; gap: var(--space-sm);">
                    <?php if ($currentFolder): ?>
                    <input type="hidden" name="folder" value="<?= htmlspecialchars($currentFolder) ?>">
                    <?php endif; ?>
                    <input type="text" name="search" placeholder="Sök filer..." value="<?= htmlspecialchars($searchQuery) ?>">
                    <button type="submit" class="btn btn-sm btn-secondary">Sök</button>
                </form>
            </div>

            <div id="bulkActions" class="hidden">
                <button class="btn btn-sm btn-danger" onclick="deleteSelected()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    Radera valda (<span id="selectedCount">0</span>)
                </button>
            </div>
        </div>

        <!-- Stats -->
        <?php if ($searchQuery): ?>
        <div class="media-stats">
            <span>Sökresultat för "<?= htmlspecialchars($searchQuery) ?>": <?= count($mediaFiles) ?> filer</span>
            <a href="/admin/media<?= $currentFolder ? '?folder=' . $currentFolder : '' ?>">Rensa sökning</a>
        </div>
        <?php endif; ?>

        <!-- Media grid -->
        <?php if (empty($mediaFiles)): ?>
        <div class="media-empty">
            <svg class="media-empty-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                <circle cx="9" cy="9" r="2"/>
                <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
            </svg>
            <h3>Inga filer</h3>
            <p><?= $searchQuery ? 'Inga filer matchar din sökning' : 'Ladda upp filer genom att dra och släppa dem ovan' ?></p>
        </div>
        <?php else: ?>
        <div class="media-grid" id="mediaGrid">
            <?php foreach ($mediaFiles as $media): ?>
            <div class="media-item" data-id="<?= $media['id'] ?>" onclick="openMedia(<?= $media['id'] ?>)">
                <input type="checkbox" class="media-checkbox" onclick="event.stopPropagation(); toggleSelect(<?= $media['id'] ?>)">
                <div class="media-thumbnail">
                    <?php if (str_starts_with($media['mime_type'], 'image/')): ?>
                        <img src="<?= htmlspecialchars(get_media_thumbnail($media['id'], 'small')) ?>" alt="<?= htmlspecialchars($media['alt_text'] ?? $media['original_filename']) ?>" loading="lazy">
                    <?php else: ?>
                        <svg class="media-thumbnail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                            <polyline points="14 2 14 8 20 8"/>
                        </svg>
                    <?php endif; ?>
                </div>
                <div class="media-info">
                    <div class="media-filename" title="<?= htmlspecialchars($media['original_filename']) ?>">
                        <?= htmlspecialchars($media['original_filename']) ?>
                    </div>
                    <div class="media-meta">
                        <?= format_file_size($media['size']) ?>
                        <?php if ($media['width'] && $media['height']): ?>
                            &bull; <?= $media['width'] ?>x<?= $media['height'] ?>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Media detail modal -->
<div class="media-modal" id="mediaModal">
    <div class="media-modal-content">
        <div class="media-modal-header">
            <h3 id="modalTitle">Mediainfo</h3>
            <button class="media-modal-close" onclick="closeModal()">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
        </div>
        <div class="media-modal-body">
            <div class="media-preview">
                <img id="modalImage" src="" alt="">
            </div>
            <div class="media-details">
                <div class="media-detail-group">
                    <span class="media-detail-label">Filnamn</span>
                    <span class="media-detail-value" id="detailFilename"></span>
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">Storlek</span>
                    <span class="media-detail-value" id="detailSize"></span>
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">Dimensioner</span>
                    <span class="media-detail-value" id="detailDimensions"></span>
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">Uppladdad</span>
                    <span class="media-detail-value" id="detailUploaded"></span>
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">Mapp</span>
                    <select class="media-detail-input" id="detailFolder">
                        <?php foreach ($folders as $folder): ?>
                        <option value="<?= $folder['id'] ?>"><?= htmlspecialchars($folder['name']) ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">Alt-text</span>
                    <input type="text" class="media-detail-input" id="detailAltText" placeholder="Beskrivning för tillgänglighet">
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">Bildtext</span>
                    <textarea class="media-detail-input" id="detailCaption" rows="2" placeholder="Valfri bildtext"></textarea>
                </div>
                <div class="media-detail-group">
                    <span class="media-detail-label">URL</span>
                    <input type="text" class="media-detail-input" id="detailUrl" readonly onclick="this.select()">
                </div>

                <div id="detailUsage" class="hidden">
                    <span class="media-detail-label">Används i</span>
                    <ul id="usageList" style="font-size: 0.875rem; margin: var(--space-xs) 0; padding-left: var(--space-md);"></ul>
                </div>

                <div style="display: flex; gap: var(--space-sm); margin-top: auto;">
                    <button class="btn btn-primary" onclick="saveMedia()">Spara</button>
                    <button class="btn btn-danger" id="deleteBtn" onclick="deleteMedia()">Radera</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const currentFolder = <?= json_encode($currentFolder ?? 'general') ?>;

let selectedIds = new Set();
let currentMediaId = null;

// Create sponsor subfolder
async function createSponsorSubfolder() {
    const input = document.getElementById('newSubfolderName');
    const name = input.value.trim();

    if (!name) {
        alert('Ange ett namn för mappen');
        return;
    }

    // Generate slug from name
    let slug = name.toLowerCase()
        .replace(/[åä]/g, 'a')
        .replace(/ö/g, 'o')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');

    if (!slug) {
        alert('Ogiltigt namn');
        return;
    }

    const folderPath = 'sponsors/' + slug;

    try {
        const response = await fetch('/api/media.php?action=create_folder', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ folder: folderPath })
        });

        const result = await response.json();

        if (result.success) {
            // Navigate to the new subfolder
            window.location.href = '/admin/media?folder=' + encodeURIComponent(folderPath);
        } else {
            alert('Fel: ' + (result.error || 'Kunde inte skapa mappen'));
        }
    } catch (error) {
        console.error('Create folder error:', error);
        alert('Ett fel uppstod');
    }
}

// Upload zone events
uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => handleFiles(fileInput.files));

async function handleFiles(files) {
    if (files.length === 0) return;

    uploadProgress.classList.add('active');
    let completed = 0;
    const total = files.length;

    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('folder', currentFolder);

        try {
            progressText.textContent = `Laddar upp ${file.name}... (${completed + 1}/${total})`;

            const response = await fetch('/api/media.php?action=upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            if (!result.success) {
                console.error('Upload failed:', result.error);
                alert(`Kunde inte ladda upp ${file.name}: ${result.error}`);
            }
        } catch (error) {
            console.error('Upload error:', error);
        }

        completed++;
        progressFill.style.width = (completed / total * 100) + '%';
    }

    progressText.textContent = 'Klar!';
    setTimeout(() => {
        uploadProgress.classList.remove('active');
        progressFill.style.width = '0';
        location.reload();
    }, 1000);
}

// Selection
function toggleSelect(id) {
    const item = document.querySelector(`.media-item[data-id="${id}"]`);
    const checkbox = item.querySelector('.media-checkbox');

    if (selectedIds.has(id)) {
        selectedIds.delete(id);
        item.classList.remove('selected');
        checkbox.checked = false;
    } else {
        selectedIds.add(id);
        item.classList.add('selected');
        checkbox.checked = true;
    }

    updateBulkActions();
}

function updateBulkActions() {
    const bulkActions = document.getElementById('bulkActions');
    const count = document.getElementById('selectedCount');

    if (selectedIds.size > 0) {
        bulkActions.style.display = 'block';
        count.textContent = selectedIds.size;
    } else {
        bulkActions.style.display = 'none';
    }
}

async function deleteSelected() {
    if (!confirm(`Vill du radera ${selectedIds.size} filer?`)) return;

    for (const id of selectedIds) {
        try {
            await fetch('/api/media.php?action=delete&id=' + id, { method: 'DELETE' });
        } catch (error) {
            console.error('Delete error:', error);
        }
    }

    location.reload();
}

// Modal
async function openMedia(id) {
    currentMediaId = id;

    try {
        const response = await fetch(`/api/media.php?action=get&id=${id}`);
        const result = await response.json();

        if (!result.success) {
            alert(result.error);
            return;
        }

        const media = result.data;

        document.getElementById('modalTitle').textContent = media.original_filename;
        document.getElementById('modalImage').src = media.url;
        document.getElementById('detailFilename').textContent = media.original_filename;
        document.getElementById('detailSize').textContent = formatFileSize(media.size);
        document.getElementById('detailDimensions').textContent = media.width && media.height
            ? `${media.width} x ${media.height} px`
            : 'N/A';
        document.getElementById('detailUploaded').textContent = new Date(media.uploaded_at).toLocaleString('sv-SE');
        document.getElementById('detailFolder').value = media.folder;
        document.getElementById('detailAltText').value = media.alt_text || '';
        document.getElementById('detailCaption').value = media.caption || '';
        document.getElementById('detailUrl').value = media.url;

        // Show usage
        const usageSection = document.getElementById('detailUsage');
        const usageList = document.getElementById('usageList');
        const deleteBtn = document.getElementById('deleteBtn');

        if (media.usage && media.usage.length > 0) {
            usageSection.style.display = 'block';
            usageList.innerHTML = media.usage.map(u =>
                `<li>${u.entity_type}: ${u.entity_name || u.entity_id} (${u.field})</li>`
            ).join('');
            deleteBtn.disabled = true;
            deleteBtn.title = 'Kan inte radera - filen används';
        } else {
            usageSection.style.display = 'none';
            deleteBtn.disabled = false;
            deleteBtn.title = '';
        }

        document.getElementById('mediaModal').classList.add('active');
    } catch (error) {
        console.error('Error loading media:', error);
        alert('Kunde inte ladda mediainformation');
    }
}

function closeModal() {
    document.getElementById('mediaModal').classList.remove('active');
    currentMediaId = null;
}

async function saveMedia() {
    if (!currentMediaId) return;

    const data = {
        id: currentMediaId,
        folder: document.getElementById('detailFolder').value,
        alt_text: document.getElementById('detailAltText').value,
        caption: document.getElementById('detailCaption').value
    };

    try {
        const response = await fetch('/api/media.php?action=update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (result.success) {
            alert('Sparad!');
            location.reload();
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Save error:', error);
        alert('Kunde inte spara');
    }
}

async function deleteMedia() {
    if (!currentMediaId) return;
    if (!confirm('Vill du radera denna fil?')) return;

    try {
        const response = await fetch(`/api/media.php?action=delete&id=${currentMediaId}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        if (result.success) {
            closeModal();
            location.reload();
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Delete error:', error);
        alert('Kunde inte radera');
    }
}

function formatFileSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB'];
    let unitIndex = 0;
    let size = bytes;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return size.toFixed(1) + ' ' + units[unitIndex];
}

// Close modal on escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
});

// Close modal on backdrop click
document.getElementById('mediaModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('mediaModal')) closeModal();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
