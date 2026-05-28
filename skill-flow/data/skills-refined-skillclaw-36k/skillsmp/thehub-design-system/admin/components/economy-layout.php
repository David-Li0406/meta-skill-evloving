<?php
/**
 * EKONOMI LAYOUT
 * Dedikerad layout för biljett-, anmälnings- och betalningssidor
 *
 * Användning:
 *   // 1. Sätt variabler
 *   $economy_page_title = 'Ordrar';
 *   $economy_page_actions = '<button class="btn btn-primary">Exportera</button>'; // Valfritt
 *
 *   // 2. Inkludera denna fil
 *   include __DIR__ . '/components/economy-layout.php';
 *
 *   // 3. Skriv innehåll...
 *
 *   // 4. Stäng med footer
 *   include __DIR__ . '/components/economy-layout-footer.php';
 */

// Ladda konfiguration
require_once __DIR__ . '/../../hub-config.php';
require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/config/economy-tabs-config.php';

// Kräv admin
require_admin();

// Hämta kontext
$economy_context = get_economy_context();
$economy_type = $economy_context['type'];
$economy_id = $economy_context['id'];
$economy_config = $economy_context['config'];

// Behörighetskontroll
if ($economy_type === 'event' && !can_access_event_economy($economy_id)) {
    set_flash('error', 'Du har inte tillgång till detta event.');
    header('Location: /admin/events.php');
    exit;
}

if ($economy_type === 'series' && !can_access_series_economy($economy_id)) {
    set_flash('error', 'Du har inte tillgång till denna serie.');
    header('Location: /admin/series.php');
    exit;
}

// Hämta kontext-info för breadcrumb
$context_info = null;
$context_label = '';

if ($economy_type === 'event' && $economy_id) {
    $context_info = get_economy_event_info($economy_id);
    $context_label = $context_info['name'] ?? "Event #$economy_id";
} elseif ($economy_type === 'series' && $economy_id) {
    $context_info = get_economy_series_info($economy_id);
    $context_label = $context_info['name'] ?? "Serie #$economy_id";
}

// Aktiv tab
$active_tab = get_active_economy_tab($economy_config['tabs']);

// Page title fallback
$page_title = $economy_page_title ?? $economy_config['title'];

// Skapa pageInfo för sidebar
$pageInfo = [
    'page' => 'admin',
    'section' => 'admin',
    'params' => []
];

// Theme
$theme = hub_get_theme();
?>
<!DOCTYPE html>
<html lang="sv" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($page_title) ?> - TheHUB Admin</title>

    <!-- Favicon from branding.json -->
    <?php
    $faviconUrl = '/assets/favicon.svg';
    $faviconBrandingFile = __DIR__ . '/../../uploads/branding.json';
    if (file_exists($faviconBrandingFile)) {
        $faviconBranding = json_decode(file_get_contents($faviconBrandingFile), true);
        if (!empty($faviconBranding['logos']['favicon'])) {
            $faviconUrl = $faviconBranding['logos']['favicon'];
        }
    }
    $faviconExt = strtolower(pathinfo($faviconUrl, PATHINFO_EXTENSION));
    $faviconMime = match($faviconExt) {
        'svg' => 'image/svg+xml',
        'png' => 'image/png',
        'ico' => 'image/x-icon',
        default => 'image/png'
    };
    ?>
    <link rel="icon" type="<?= $faviconMime ?>" href="<?= htmlspecialchars($faviconUrl) ?>">
    <link rel="icon" type="<?= $faviconMime ?>" sizes="32x32" href="<?= htmlspecialchars($faviconUrl) ?>">
    <link rel="apple-touch-icon" href="<?= htmlspecialchars($faviconUrl) ?>">

    <!-- V3 CSS -->
    <link rel="stylesheet" href="<?= hub_asset('css/reset.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/tokens.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/theme.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/layout.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/components.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/tables.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/utilities.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/grid.css') ?>">

    <!-- Admin CSS -->
    <link rel="stylesheet" href="/admin/assets/css/admin.css?v=<?= filemtime(__DIR__ . '/../assets/css/admin.css') ?>">
</head>
<body>
    <a href="#main-content" class="skip-link">Hoppa till huvudinnehåll</a>

    <?php include HUB_ROOT . '/components/header.php'; ?>

    <div class="app-layout">
        <?php include HUB_ROOT . '/components/sidebar.php'; ?>

        <main id="main-content" class="main-content" role="main">

            <!-- EKONOMI TAB BAR -->
            <div class="economy-tabs">
                <div class="economy-tabs-container">
                    <!-- Kontext-info -->
                    <div class="economy-tabs-context">
                        <?php if ($economy_type === 'event'): ?>
                            <span class="economy-context-badge economy-context-event">
                                <i data-lucide="calendar" class="economy-context-icon"></i>
                                <?= htmlspecialchars($context_label) ?>
                            </span>
                        <?php elseif ($economy_type === 'series'): ?>
                            <span class="economy-context-badge economy-context-series">
                                <i data-lucide="medal" class="economy-context-icon"></i>
                                <?= htmlspecialchars($context_label) ?>
                            </span>
                        <?php else: ?>
                            <span class="economy-context-badge economy-context-global">
                                <i data-lucide="wallet" class="economy-context-icon"></i>
                                Ekonomi
                            </span>
                        <?php endif; ?>
                    </div>

                    <!-- Tabs -->
                    <nav class="economy-tabs-nav" role="tablist">
                        <?php foreach ($economy_config['tabs'] as $tab): ?>
                            <?php
                            $tab_url = economy_tab_url($tab['url'], $economy_type, $economy_id);
                            $is_active = $active_tab === $tab['id'];
                            ?>
                            <a href="<?= htmlspecialchars($tab_url) ?>"
                               class="economy-tab<?= $is_active ? ' economy-tab-active' : '' ?>"
                               role="tab"
                               aria-selected="<?= $is_active ? 'true' : 'false' ?>"
                               title="<?= htmlspecialchars($tab['description'] ?? '') ?>">
                                <i data-lucide="<?= htmlspecialchars($tab['icon']) ?>" class="economy-tab-icon"></i>
                                <span class="economy-tab-label"><?= htmlspecialchars($tab['label']) ?></span>
                            </a>
                        <?php endforeach; ?>
                    </nav>
                </div>
            </div>

            <!-- Page Header -->
            <div class="page-header">
                <h1 class="page-title"><?= htmlspecialchars($page_title) ?></h1>
                <?php if (isset($economy_page_actions)): ?>
                    <div class="page-actions">
                        <?= $economy_page_actions ?>
                    </div>
                <?php endif; ?>
            </div>

            <!-- Flash Messages -->
            <?php if (has_flash('success')): ?>
                <div class="alert alert-success">
                    <?= htmlspecialchars(get_flash('success')) ?>
                </div>
            <?php endif; ?>

            <?php if (has_flash('error')): ?>
                <div class="alert alert-error">
                    <?= htmlspecialchars(get_flash('error')) ?>
                </div>
            <?php endif; ?>

            <?php if (has_flash('warning')): ?>
                <div class="alert alert-warning">
                    <?= htmlspecialchars(get_flash('warning')) ?>
                </div>
            <?php endif; ?>

            <!-- Page Content -->
            <div class="page-content admin-content">

<style>
/* ============================================================================
   ECONOMY TABS - Dedikerat fliksystem för Ekonomi
   ============================================================================ */

.economy-tabs {
    background: var(--color-bg-surface, #fff);
    border-bottom: 1px solid var(--color-border, #e5e7eb);
    position: sticky;
    top: 0;
    z-index: 90;
}

.economy-tabs-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: var(--space-md, 1rem);
    padding: 0 var(--space-md, 1rem);
}

/* Kontext Badge */
.economy-tabs-context {
    flex-shrink: 0;
    padding: var(--space-sm, 0.5rem) 0;
}

.economy-context-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs, 0.25rem);
    padding: var(--space-xs, 0.25rem) var(--space-sm, 0.5rem);
    font-size: var(--text-xs, 0.75rem);
    font-weight: var(--weight-semibold, 600);
    border-radius: var(--radius-sm, 6px);
    white-space: nowrap;
}

.economy-context-icon {
    width: 14px;
    height: 14px;
}

.economy-context-global {
    background: var(--color-accent-light, #e8f5e9);
    color: var(--color-accent, #61CE70);
}

.economy-context-event {
    background: #e3f2fd;
    color: #1976d2;
}

.economy-context-series {
    background: #fff3e0;
    color: #f57c00;
}

/* Tab Navigation */
.economy-tabs-nav {
    display: flex;
    gap: 2px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    flex: 1;
}

.economy-tabs-nav::-webkit-scrollbar {
    display: none;
}

.economy-tab {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs, 0.25rem);
    min-height: 48px;
    padding: 0 var(--space-md, 1rem);
    font-size: var(--text-sm, 0.875rem);
    font-weight: var(--weight-medium, 500);
    color: var(--color-text-secondary, #6b7280);
    text-decoration: none;
    white-space: nowrap;
    border-bottom: 2px solid transparent;
    transition: all 0.15s ease;
    margin-bottom: -1px;
}

.economy-tab:hover {
    color: var(--color-text-primary, #171717);
    background: var(--color-bg-hover, rgba(0,0,0,0.04));
}

.economy-tab-active {
    color: var(--color-accent, #61CE70);
    border-bottom-color: var(--color-accent, #61CE70);
    font-weight: var(--weight-semibold, 600);
}

.economy-tab-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
}

/* Mobile */
@media (max-width: 639px) {
    .economy-tabs-container {
        flex-direction: column;
        align-items: stretch;
        gap: 0;
        padding: 0;
    }

    .economy-tabs-context {
        padding: var(--space-sm, 0.5rem) var(--space-md, 1rem);
        border-bottom: 1px solid var(--color-border, #e5e7eb);
    }

    .economy-tabs-nav {
        padding: 0 var(--space-sm, 0.5rem);
    }

    .economy-tab {
        padding: 0 var(--space-sm, 0.5rem);
        min-height: 44px;
    }

    .economy-tab-label {
        display: none;
    }

    .economy-tab-icon {
        width: 20px;
        height: 20px;
    }
}

/* Tablet and up - show labels */
@media (min-width: 640px) {
    .economy-tab-label {
        display: inline;
    }
}
</style>
