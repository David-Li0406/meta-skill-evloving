<?php
/**
 * Branding / Design System Admin Page
 * View and customize site colors and typography
 * Version: v1.0.0 [2025-12-13]
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Branding settings file
$brandingFile = __DIR__ . '/../uploads/branding.json';

// Load current branding
function loadBranding($file) {
    if (file_exists($file)) {
        $data = json_decode(file_get_contents($file), true);
        return is_array($data) ? $data : [];
    }
    return [];
}

// Save branding
function saveBranding($file, $data) {
    $dir = dirname($file);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }

    // Encode to JSON first to catch any issues
    $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    if ($json === false) {
        error_log('saveBranding: JSON encode failed - ' . json_last_error_msg());
        return false;
    }

    // Write to file
    $result = file_put_contents($file, $json);
    if ($result === false) {
        error_log('saveBranding: file_put_contents failed for ' . $file);
    }

    return $result;
}

$branding = loadBranding($brandingFile);
$message = '';
$messageType = '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? 'save';

    if ($action === 'reset') {
        // Reset to defaults
        $branding = [];
        saveBranding($brandingFile, $branding);
        $message = 'Branding återställt till standard!';
        $messageType = 'success';
    } else {
        // Save custom colors for both themes
        $darkColors = [];
        $lightColors = [];

        foreach ($_POST as $key => $value) {
            // Dark theme colors: dark_color_bg_page
            if (strpos($key, 'dark_color_') === 0 && !empty($value)) {
                $varName = str_replace('_', '-', substr($key, 11)); // dark_color_bg_page -> bg-page
                $varName = '--color-' . $varName;
                if (preg_match('/^#[0-9A-Fa-f]{6}$/', $value) || preg_match('/^rgba?\(/', $value)) {
                    $darkColors[$varName] = $value;
                }
            }
            // Light theme colors: light_color_bg_page
            if (strpos($key, 'light_color_') === 0 && !empty($value)) {
                $varName = str_replace('_', '-', substr($key, 12)); // light_color_bg_page -> bg-page
                $varName = '--color-' . $varName;
                if (preg_match('/^#[0-9A-Fa-f]{6}$/', $value) || preg_match('/^rgba?\(/', $value)) {
                    $lightColors[$varName] = $value;
                }
            }
        }

        $branding['colors'] = [
            'dark' => $darkColors,
            'light' => $lightColors
        ];

        // Save responsive layout settings
        $branding['responsive'] = [
            'mobile_portrait' => [
                'padding' => $_POST['mobile_portrait_padding'] ?? '12',
                'radius' => $_POST['mobile_portrait_radius'] ?? '0'
            ],
            'mobile_landscape' => [
                'sidebar_gap' => $_POST['mobile_landscape_sidebar_gap'] ?? '4'
            ],
            'tablet' => [
                'padding' => $_POST['tablet_padding'] ?? '24',
                'radius' => $_POST['tablet_radius'] ?? '8'
            ],
            'desktop' => [
                'padding' => $_POST['desktop_padding'] ?? '32',
                'radius' => $_POST['desktop_radius'] ?? '12'
            ]
        ];

        // Save layout settings
        $branding['layout'] = [
            'content_max_width' => $_POST['content_max_width'] ?? '1400',
            'sidebar_width' => $_POST['sidebar_width'] ?? '72',
            'header_height' => $_POST['header_height'] ?? '60'
        ];

        // Save logo settings
        $branding['logos'] = [
            'sidebar' => trim($_POST['logo_sidebar'] ?? ''),
            'homepage' => trim($_POST['logo_homepage'] ?? ''),
            'favicon' => trim($_POST['logo_favicon'] ?? '')
        ];

        // Debug: Log what we're saving
        error_log('Branding save - logos POST data: ' . json_encode([
            'logo_sidebar' => $_POST['logo_sidebar'] ?? '(not set)',
            'logo_homepage' => $_POST['logo_homepage'] ?? '(not set)',
            'logo_favicon' => $_POST['logo_favicon'] ?? '(not set)'
        ]));
        error_log('Branding save - full data: ' . json_encode($branding));

        $saveResult = saveBranding($brandingFile, $branding);
        error_log('Branding save result: ' . ($saveResult !== false ? 'success (' . $saveResult . ' bytes)' : 'FAILED'));

        if ($saveResult !== false) {
            $message = 'Branding sparad!';
            $messageType = 'success';

            // Show more details if logos were set
            $logoCount = count(array_filter($branding['logos']));
            if ($logoCount > 0) {
                $message .= " ({$logoCount} logotyp(er) sparade)";
            }
        } else {
            $message = 'Fel: Kunde inte spara branding. Kontrollera filrättigheter.';
            $messageType = 'error';
        }
    }
}

// Define color groups for display - MUST match theme.css values exactly!
// Updated 2026-01-18: Unified colors - same for both dark and light (light theme always)
$colorGroups = [
    'Bakgrunder' => [
        'bg-page' => ['label' => 'Sidbakgrund', 'dark' => '#F9F9F9', 'light' => '#F9F9F9'],
        'bg-surface' => ['label' => 'Ytor (header, menyer)', 'dark' => '#FFFFFF', 'light' => '#FFFFFF'],
        'bg-card' => ['label' => 'Kort', 'dark' => '#FFFFFF', 'light' => '#FFFFFF'],
        'bg-sunken' => ['label' => 'Nedsänkta ytor', 'dark' => '#F0F0F0', 'light' => '#F0F0F0'],
    ],
    'Text' => [
        'text-primary' => ['label' => 'Primär text', 'dark' => '#0b131e', 'light' => '#0b131e'],
        'text-secondary' => ['label' => 'Sekundär text', 'dark' => '#495057', 'light' => '#495057'],
        'text-tertiary' => ['label' => 'Tertiär text', 'dark' => '#6c757d', 'light' => '#6c757d'],
        'text-muted' => ['label' => 'Dämpad text', 'dark' => '#868e96', 'light' => '#868e96'],
    ],
    'Accent & Knappar' => [
        'accent' => ['label' => 'Accentfärg', 'dark' => '#0066CC', 'light' => '#0066CC'],
        'accent-hover' => ['label' => 'Accent hover', 'dark' => '#0052A3', 'light' => '#0052A3'],
        'accent-light' => ['label' => 'Accent ljus', 'dark' => 'rgba(0, 102, 204, 0.08)', 'light' => 'rgba(0, 102, 204, 0.08)'],
    ],
    'Status' => [
        'success' => ['label' => 'Framgång', 'dark' => '#059669', 'light' => '#059669'],
        'warning' => ['label' => 'Varning', 'dark' => '#d97706', 'light' => '#d97706'],
        'error' => ['label' => 'Fel', 'dark' => '#dc2626', 'light' => '#dc2626'],
        'info' => ['label' => 'Info', 'dark' => '#0284c7', 'light' => '#0284c7'],
    ],
    'Kanter' => [
        'border' => ['label' => 'Kant', 'dark' => 'rgba(0, 0, 0, 0.1)', 'light' => 'rgba(0, 0, 0, 0.1)'],
        'border-strong' => ['label' => 'Stark kant', 'dark' => 'rgba(0, 0, 0, 0.15)', 'light' => 'rgba(0, 0, 0, 0.15)'],
    ],
];

// Typography settings
$fonts = [
    'heading' => ['label' => 'Rubriker (H1)', 'value' => 'Oswald', 'example' => 'THEHUB GRAVITY'],
    'heading-secondary' => ['label' => 'Underrubriker (H2-H3)', 'value' => 'Cabin Condensed', 'example' => 'Kalender & Event'],
    'body' => ['label' => 'Brödtext', 'value' => 'Manrope', 'example' => 'Detta är ett exempel på brödtext som visas på sidan.'],
    'link' => ['label' => 'Länkar', 'value' => 'Roboto', 'example' => 'Klicka här för mer info'],
];

$spacings = [
    '2xs' => '4px',
    'xs' => '8px',
    'sm' => '12px',
    'md' => '16px',
    'lg' => '24px',
    'xl' => '32px',
    '2xl' => '48px',
    '3xl' => '64px',
];

$radii = [
    'sm' => '6px',
    'md' => '10px',
    'lg' => '14px',
    'xl' => '20px',
    'full' => '9999px',
];

// Page config
$page_title = 'Branding';
$breadcrumbs = [
    ['label' => 'System', 'url' => '/admin/'],
    ['label' => 'Branding']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.branding-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-lg);
}

.color-group {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
}

.color-group h3 {
    margin: 0 0 var(--space-md);
    font-size: var(--text-lg);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.color-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-sm) 0;
    border-bottom: 1px solid var(--color-border);
}

.color-item:last-child {
    border-bottom: none;
}

/* Color swatch button - opens advanced picker */
.color-swatch-btn {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-md);
    border: 2px solid var(--color-border);
    flex-shrink: 0;
    cursor: pointer;
    transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.1s ease;
}

.color-swatch-btn:hover {
    border-color: var(--color-accent);
    transform: scale(1.05);
}

.color-swatch-btn:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px var(--color-accent-light);
}

.color-info {
    flex: 1;
    min-width: 0;
}

.color-label {
    font-weight: var(--weight-medium);
    font-size: var(--text-sm);
}

.color-value {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
}

.color-input {
    width: 90px;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    padding: var(--space-xs);
    background: var(--color-bg-sunken);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    color: var(--color-text-primary);
}

/* Typography Section */
.font-preview {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
}

.font-preview h4 {
    margin: 0 0 var(--space-xs);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.font-sample {
    padding: var(--space-md);
    background: var(--color-bg-sunken);
    border-radius: var(--radius-md);
    margin-top: var(--space-sm);
}

.font-sample.heading { font-family: var(--font-heading); font-size: var(--text-2xl); text-transform: uppercase; }
.font-sample.heading-secondary { font-family: var(--font-heading-secondary); font-size: var(--text-xl); }
.font-sample.body { font-family: var(--font-body); font-size: var(--text-base); }
.font-sample.link { font-family: var(--font-link); font-size: var(--text-base); color: var(--color-accent); }

/* Spacing Preview */
.spacing-grid {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
}

.spacing-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm);
    background: var(--color-bg-sunken);
    border-radius: var(--radius-sm);
}

.spacing-bar {
    height: 20px;
    background: var(--color-accent);
    border-radius: var(--radius-sm);
}

.spacing-label {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    min-width: 60px;
}

/* Radius Preview */
.radius-grid {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
}

.radius-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-xs);
}

.radius-sample {
    width: 60px;
    height: 60px;
    background: var(--color-accent);
}

.radius-label {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
}

/* Live Preview */
.live-preview {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    margin-top: var(--space-lg);
}

.preview-buttons {
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
}

.preview-alerts {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    margin-top: var(--space-md);
}

/* Theme Tabs */
.theme-tabs {
    display: flex;
    gap: var(--space-xs);
    background: var(--color-bg-sunken);
    padding: var(--space-xs);
    border-radius: var(--radius-md);
    width: fit-content;
}

.theme-tab {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-lg);
    border: none;
    background: transparent;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s ease;
}

.theme-tab:hover {
    color: var(--color-text-primary);
}

.theme-tab.active {
    background: var(--color-bg-card);
    color: var(--color-text-primary);
    box-shadow: var(--shadow-sm);
}

.theme-tab i {
    width: 16px;
    height: 16px;
}

.theme-panel {
    animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Default Colors Reference Section */
.default-colors-reference {
    background: var(--color-bg-sunken);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.default-colors-toggle {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-md);
    cursor: pointer;
    font-weight: var(--weight-medium);
    color: var(--color-text-secondary);
    list-style: none;
    transition: background 0.15s ease;
}

.default-colors-toggle::-webkit-details-marker {
    display: none;
}

.default-colors-toggle:hover {
    background: var(--color-bg-hover);
    color: var(--color-text-primary);
}

.default-colors-toggle .toggle-icon {
    margin-left: auto;
    transition: transform 0.2s ease;
}

.default-colors-reference[open] .toggle-icon {
    transform: rotate(180deg);
}

.default-colors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--space-md);
    padding: var(--space-md);
    padding-top: 0;
    border-top: 1px solid var(--color-border);
}

.default-color-group h4 {
    font-size: var(--text-sm);
    font-weight: var(--weight-semibold);
    color: var(--color-text-primary);
    margin: 0 0 var(--space-xs);
}

.default-color-row {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    padding: var(--space-2xs) 0;
}

.default-swatch {
    width: 20px;
    height: 20px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--color-border);
    flex-shrink: 0;
}

.default-color-row code {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    background: var(--color-bg-card);
    padding: 1px 4px;
    border-radius: 3px;
}

</style>

<?php if ($message): ?>
<div class="alert alert--<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<form method="POST" id="brandingForm">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="save">

    <!-- Action Buttons -->
    <div class="flex gap-md mb-lg justify-end">
        <button type="button" class="btn btn--secondary" onclick="if(confirm('Återställa alla färger till standard?')) { document.querySelector('[name=action]').value='reset'; document.getElementById('brandingForm').submit(); }">
            <i data-lucide="rotate-ccw"></i>
            Återställ standard
        </button>
        <button type="submit" class="btn btn--primary">
            <i data-lucide="save"></i>
            Spara ändringar
        </button>
    </div>

    <!-- Logos Section -->
    <?php
    $logos = $branding['logos'] ?? [];
    $sidebarLogo = $logos['sidebar'] ?? '';
    $homepageLogo = $logos['homepage'] ?? '';
    $faviconLogo = $logos['favicon'] ?? '';
    ?>
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="image"></i>
                Logotyper
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-lg">
                Välj logotyper från <a href="/admin/media?folder=branding">Mediabiblioteket</a> eller ladda upp nya där först.
            </p>

            <div class="branding-grid grid-auto-280">
                <!-- Sidebar Logo -->
                <div class="color-group">
                    <h3>
                        <i data-lucide="sidebar"></i>
                        Sidebar-logga
                    </h3>
                    <p class="text-secondary text-sm mb-md">Visas i navigationens övre del på alla sidor.</p>
                    <input type="hidden" name="logo_sidebar" id="logoSidebarInput" value="<?= h($sidebarLogo) ?>">
                    <div id="logoSidebarPreview" class="logo-preview-box" onclick="openMediaPicker('sidebar')">
                        <?php if ($sidebarLogo): ?>
                            <img src="<?= h($sidebarLogo) ?>" alt="Sidebar logo">
                        <?php else: ?>
                            <span class="logo-preview-placeholder">Klicka för att välja bild</span>
                        <?php endif; ?>
                    </div>
                    <div class="flex gap-sm mt-sm">
                        <button type="button" class="btn btn--secondary btn--sm" onclick="openMediaPicker('sidebar')">
                            <i data-lucide="image"></i> Välj bild
                        </button>
                        <button type="button" class="btn btn--ghost btn--sm" onclick="clearLogo('sidebar')" <?= $sidebarLogo ? '' : 'disabled' ?>>
                            <i data-lucide="x"></i> Ta bort
                        </button>
                    </div>
                </div>

                <!-- Homepage Logo -->
                <div class="color-group">
                    <h3>
                        <i data-lucide="home"></i>
                        Startsida-logga
                    </h3>
                    <p class="text-secondary text-sm mb-md">Visas endast på startsidan (stor logga).</p>
                    <input type="hidden" name="logo_homepage" id="logoHomepageInput" value="<?= h($homepageLogo) ?>">
                    <div id="logoHomepagePreview" class="logo-preview-box" onclick="openMediaPicker('homepage')">
                        <?php if ($homepageLogo): ?>
                            <img src="<?= h($homepageLogo) ?>" alt="Homepage logo">
                        <?php else: ?>
                            <span class="logo-preview-placeholder">Klicka för att välja bild</span>
                        <?php endif; ?>
                    </div>
                    <div class="flex gap-sm mt-sm">
                        <button type="button" class="btn btn--secondary btn--sm" onclick="openMediaPicker('homepage')">
                            <i data-lucide="image"></i> Välj bild
                        </button>
                        <button type="button" class="btn btn--ghost btn--sm" onclick="clearLogo('homepage')" <?= $homepageLogo ? '' : 'disabled' ?>>
                            <i data-lucide="x"></i> Ta bort
                        </button>
                    </div>
                </div>

                <!-- Favicon -->
                <div class="color-group">
                    <h3>
                        <i data-lucide="star"></i>
                        Favicon
                    </h3>
                    <p class="text-secondary text-sm mb-md">Ikon som visas i webbläsarfliken (SVG rekommenderas).</p>
                    <input type="hidden" name="logo_favicon" id="logoFaviconInput" value="<?= h($faviconLogo) ?>">
                    <div id="logoFaviconPreview" class="logo-preview-box" onclick="openMediaPicker('favicon')">
                        <?php if ($faviconLogo): ?>
                            <img src="<?= h($faviconLogo) ?>" alt="Favicon">
                        <?php else: ?>
                            <span class="logo-preview-placeholder">Klicka för att välja bild</span>
                        <?php endif; ?>
                    </div>
                    <div class="flex gap-sm mt-sm">
                        <button type="button" class="btn btn--secondary btn--sm" onclick="openMediaPicker('favicon')">
                            <i data-lucide="image"></i> Välj bild
                        </button>
                        <button type="button" class="btn btn--ghost btn--sm" onclick="clearLogo('favicon')" <?= $faviconLogo ? '' : 'disabled' ?>>
                            <i data-lucide="x"></i> Ta bort
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Colors Section -->
    <?php
    // Get saved colors or use defaults
    $savedColors = $branding['colors'] ?? [];
    // Handle legacy format (flat array) vs new format (dark/light arrays)
    if (!isset($savedColors['dark']) && !isset($savedColors['light'])) {
        // Legacy format - treat as dark theme
        $savedDarkColors = $savedColors;
        $savedLightColors = [];
    } else {
        $savedDarkColors = $savedColors['dark'] ?? [];
        $savedLightColors = $savedColors['light'] ?? [];
    }
    ?>
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="palette"></i>
                Färger
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-md">
                Anpassa färger för mörkt och ljust tema. Klicka på en färgruta för att välja ny färg.
            </p>

            <!-- Theme Tabs -->
            <div class="theme-tabs mb-lg">
                <button type="button" class="theme-tab active" data-theme="dark" onclick="switchThemeTab('dark')">
                    <i data-lucide="moon"></i>
                    Mörkt tema
                </button>
                <button type="button" class="theme-tab" data-theme="light" onclick="switchThemeTab('light')">
                    <i data-lucide="sun"></i>
                    Ljust tema
                </button>
            </div>

            <!-- Dark Theme Colors -->
            <div class="theme-panel" id="dark-theme-panel">
                <div class="branding-grid">
                    <?php foreach ($colorGroups as $groupName => $colors): ?>
                    <div class="color-group">
                        <h3>
                            <i data-lucide="<?= $groupName === 'Bakgrunder' ? 'square' : ($groupName === 'Text' ? 'type' : ($groupName === 'Status' ? 'check-circle' : 'minus')) ?>"></i>
                            <?= h($groupName) ?>
                        </h3>
                        <?php foreach ($colors as $varKey => $colorInfo):
                            $fullVar = '--color-' . $varKey;
                            $currentValue = $savedDarkColors[$fullVar] ?? $colorInfo['dark'];
                            $inputName = 'dark_color_' . str_replace('-', '_', $varKey);
                            $isHex = preg_match('/^#[0-9A-Fa-f]{6}$/', $currentValue);
                        ?>
                        <div class="color-item">
                            <button type="button"
                                    class="color-swatch-btn"
                                    style="background: <?= h($currentValue) ?>;"
                                    data-var="<?= $varKey ?>"
                                    data-theme="dark"
                                    onclick="openColorPicker(this, 'dark', '<?= $varKey ?>')">
                            </button>
                            <input type="hidden" name="<?= $inputName ?>" value="<?= h($currentValue) ?>">
                            <div class="color-info">
                                <div class="color-label"><?= h($colorInfo['label']) ?></div>
                            </div>
                            <input type="text"
                                   class="color-input"
                                   value="<?= h($currentValue) ?>"
                                   data-var="<?= $varKey ?>"
                                   data-theme="dark"
                                   onchange="updateFromText(this, 'dark')">
                        </div>
                        <?php endforeach; ?>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>

            <!-- Light Theme Colors -->
            <div class="theme-panel" id="light-theme-panel" style="display: none;">
                <div class="branding-grid">
                    <?php foreach ($colorGroups as $groupName => $colors): ?>
                    <div class="color-group">
                        <h3>
                            <i data-lucide="<?= $groupName === 'Bakgrunder' ? 'square' : ($groupName === 'Text' ? 'type' : ($groupName === 'Status' ? 'check-circle' : 'minus')) ?>"></i>
                            <?= h($groupName) ?>
                        </h3>
                        <?php foreach ($colors as $varKey => $colorInfo):
                            $fullVar = '--color-' . $varKey;
                            $currentValue = $savedLightColors[$fullVar] ?? $colorInfo['light'];
                            $inputName = 'light_color_' . str_replace('-', '_', $varKey);
                            $isHex = preg_match('/^#[0-9A-Fa-f]{6}$/', $currentValue);
                        ?>
                        <div class="color-item">
                            <button type="button"
                                    class="color-swatch-btn"
                                    style="background: <?= h($currentValue) ?>;"
                                    data-var="<?= $varKey ?>"
                                    data-theme="light"
                                    onclick="openColorPicker(this, 'light', '<?= $varKey ?>')">
                            </button>
                            <input type="hidden" name="<?= $inputName ?>" value="<?= h($currentValue) ?>">
                            <div class="color-info">
                                <div class="color-label"><?= h($colorInfo['label']) ?></div>
                            </div>
                            <input type="text"
                                   class="color-input"
                                   value="<?= h($currentValue) ?>"
                                   data-var="<?= $varKey ?>"
                                   data-theme="light"
                                   onchange="updateFromText(this, 'light')">
                        </div>
                        <?php endforeach; ?>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>

            <!-- Default Colors Reference -->
            <details class="default-colors-reference mt-lg">
                <summary class="default-colors-toggle">
                    <i data-lucide="palette"></i>
                    <span>Visa standardfärger (referens)</span>
                    <i data-lucide="chevron-down" class="toggle-icon"></i>
                </summary>
                <div class="default-colors-grid">
                    <div class="default-color-group">
                        <h4>Bakgrunder</h4>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #F9F9F9;"></span>
                            <span>Sidbakgrund: <code>#F9F9F9</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #FFFFFF;"></span>
                            <span>Ytor (menyer): <code>#FFFFFF</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #FFFFFF;"></span>
                            <span>Kort: <code>#FFFFFF</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #F0F0F0;"></span>
                            <span>Nedsänkt: <code>#F0F0F0</code></span>
                        </div>
                    </div>
                    <div class="default-color-group">
                        <h4>Text</h4>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #0b131e;"></span>
                            <span>Primär: <code>#0b131e</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #495057;"></span>
                            <span>Sekundär: <code>#495057</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #868e96;"></span>
                            <span>Dämpad: <code>#868e96</code></span>
                        </div>
                    </div>
                    <div class="default-color-group">
                        <h4>Accent & Knappar</h4>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #0066CC;"></span>
                            <span>Accent: <code>#0066CC</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #0052A3;"></span>
                            <span>Hover: <code>#0052A3</code></span>
                        </div>
                    </div>
                    <div class="default-color-group">
                        <h4>Status</h4>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #059669;"></span>
                            <span>Framgång: <code>#059669</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #d97706;"></span>
                            <span>Varning: <code>#d97706</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #dc2626;"></span>
                            <span>Fel: <code>#dc2626</code></span>
                        </div>
                        <div class="default-color-row">
                            <span class="default-swatch" style="background: #0284c7;"></span>
                            <span>Info: <code>#0284c7</code></span>
                        </div>
                    </div>
                </div>
            </details>
        </div>
    </div>

    <!-- Responsive Layout Section -->
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="layout"></i>
                Responsiv Layout
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-lg">
                Justera padding och rundning för varje plattform. Samma värde appliceras på alla kort/element inom plattformen.
            </p>

            <?php
            $responsive = $branding['responsive'] ?? [];
            $mobilePortrait = $responsive['mobile_portrait'] ?? ['padding' => '12', 'radius' => '0'];
            $mobileLandscape = $responsive['mobile_landscape'] ?? ['sidebar_gap' => '4'];
            $tablet = $responsive['tablet'] ?? ['padding' => '24', 'radius' => '8'];
            $desktop = $responsive['desktop'] ?? ['padding' => '32', 'radius' => '12'];
            ?>

            <!-- MOBILE PORTRAIT (0-767px) -->
            <div class="device-settings device-settings--blue">
                <h4 class="device-settings-header">
                    <i data-lucide="smartphone"></i>
                    Mobile Portrait (0-767px)
                </h4>

                <div class="grid-2-col">
                    <div>
                        <label class="form-label-block">Container Padding</label>
                        <select name="mobile_portrait_padding" class="form-control w-full" onchange="previewResponsive('portrait', 'padding', this.value)">
                            <option value="8" <?= $mobilePortrait['padding'] === '8' ? 'selected' : '' ?>>8px - Extra Tight</option>
                            <option value="10" <?= $mobilePortrait['padding'] === '10' ? 'selected' : '' ?>>10px - Tight</option>
                            <option value="12" <?= $mobilePortrait['padding'] === '12' ? 'selected' : '' ?>>12px - Compact</option>
                            <option value="16" <?= $mobilePortrait['padding'] === '16' ? 'selected' : '' ?>>16px - Normal</option>
                        </select>
                    </div>
                    <div>
                        <label class="form-label-block">Border Radius</label>
                        <select name="mobile_portrait_radius" class="form-control w-full" onchange="previewResponsive('portrait', 'radius', this.value)">
                            <option value="0" <?= $mobilePortrait['radius'] === '0' ? 'selected' : '' ?>>0px - Kantigt (Edge-to-edge)</option>
                            <option value="4" <?= $mobilePortrait['radius'] === '4' ? 'selected' : '' ?>>4px - Lätt rundat</option>
                            <option value="6" <?= $mobilePortrait['radius'] === '6' ? 'selected' : '' ?>>6px - Rundat</option>
                            <option value="8" <?= $mobilePortrait['radius'] === '8' ? 'selected' : '' ?>>8px - Mycket rundat</option>
                        </select>
                    </div>
                </div>
                <small>Rekommenderat: 12px padding + 0px radius för edge-to-edge känsla</small>
            </div>

            <!-- MOBILE LANDSCAPE (0-1023px landscape) -->
            <div class="device-settings device-settings--orange">
                <h4 class="device-settings-header">
                    <i data-lucide="smartphone" class="rotate-90"></i>
                    Mobile Landscape (0-1023px liggande)
                </h4>

                <div class="grid-1-col">
                    <div>
                        <label class="form-label-block">Avstånd mellan sidebar och innehåll</label>
                        <select name="mobile_landscape_sidebar_gap" class="form-control w-full">
                            <option value="0" <?= $mobileLandscape['sidebar_gap'] === '0' ? 'selected' : '' ?>>0px - Ingen marginal</option>
                            <option value="4" <?= $mobileLandscape['sidebar_gap'] === '4' ? 'selected' : '' ?>>4px - Minimal</option>
                            <option value="8" <?= $mobileLandscape['sidebar_gap'] === '8' ? 'selected' : '' ?>>8px - Liten</option>
                            <option value="12" <?= $mobileLandscape['sidebar_gap'] === '12' ? 'selected' : '' ?>>12px - Normal</option>
                            <option value="16" <?= $mobileLandscape['sidebar_gap'] === '16' ? 'selected' : '' ?>>16px - Luftig</option>
                        </select>
                    </div>
                </div>
                <small>I liggande läge visas en kompakt sidebar istället för botten-navigation</small>
            </div>

            <!-- TABLET / LANDSCAPE (768-1023px) -->
            <div class="device-settings device-settings--green">
                <h4 class="device-settings-header">
                    <i data-lucide="tablet"></i>
                    Landscape / Tablet (768-1023px)
                </h4>

                <div class="grid-2-col">
                    <div>
                        <label class="form-label-block">Container Padding</label>
                        <select name="tablet_padding" class="form-control w-full" onchange="previewResponsive('tablet', 'padding', this.value)">
                            <option value="16" <?= $tablet['padding'] === '16' ? 'selected' : '' ?>>16px - Compact</option>
                            <option value="20" <?= $tablet['padding'] === '20' ? 'selected' : '' ?>>20px - Normal</option>
                            <option value="24" <?= $tablet['padding'] === '24' ? 'selected' : '' ?>>24px - Luftigt</option>
                            <option value="32" <?= $tablet['padding'] === '32' ? 'selected' : '' ?>>32px - Extra luftigt</option>
                        </select>
                    </div>
                    <div>
                        <label class="form-label-block">Border Radius</label>
                        <select name="tablet_radius" class="form-control w-full" onchange="previewResponsive('tablet', 'radius', this.value)">
                            <option value="0" <?= $tablet['radius'] === '0' ? 'selected' : '' ?>>0px - Kantigt</option>
                            <option value="6" <?= $tablet['radius'] === '6' ? 'selected' : '' ?>>6px - Lätt rundat</option>
                            <option value="8" <?= $tablet['radius'] === '8' ? 'selected' : '' ?>>8px - Rundat</option>
                            <option value="12" <?= $tablet['radius'] === '12' ? 'selected' : '' ?>>12px - Mycket rundat</option>
                            <option value="16" <?= $tablet['radius'] === '16' ? 'selected' : '' ?>>16px - Extra rundat</option>
                        </select>
                    </div>
                </div>
                <small>Rekommenderat: 24px padding + 8px radius för balanserad design</small>
            </div>

            <!-- DESKTOP (1024px+) -->
            <div class="device-settings device-settings--purple">
                <h4 class="device-settings-header">
                    <i data-lucide="monitor"></i>
                    Desktop (1024px+)
                </h4>

                <div class="grid-2-col">
                    <div>
                        <label class="form-label-block">Container Padding</label>
                        <select name="desktop_padding" class="form-control w-full" onchange="previewResponsive('desktop', 'padding', this.value)">
                            <option value="24" <?= $desktop['padding'] === '24' ? 'selected' : '' ?>>24px - Compact</option>
                            <option value="32" <?= $desktop['padding'] === '32' ? 'selected' : '' ?>>32px - Normal</option>
                            <option value="40" <?= $desktop['padding'] === '40' ? 'selected' : '' ?>>40px - Luftigt</option>
                            <option value="48" <?= $desktop['padding'] === '48' ? 'selected' : '' ?>>48px - Extra luftigt</option>
                        </select>
                    </div>
                    <div>
                        <label class="form-label-block">Border Radius</label>
                        <select name="desktop_radius" class="form-control w-full" onchange="previewResponsive('desktop', 'radius', this.value)">
                            <option value="6" <?= $desktop['radius'] === '6' ? 'selected' : '' ?>>6px - Lätt rundat</option>
                            <option value="8" <?= $desktop['radius'] === '8' ? 'selected' : '' ?>>8px - Rundat</option>
                            <option value="12" <?= $desktop['radius'] === '12' ? 'selected' : '' ?>>12px - Mycket rundat</option>
                            <option value="16" <?= $desktop['radius'] === '16' ? 'selected' : '' ?>>16px - Extra rundat</option>
                            <option value="20" <?= $desktop['radius'] === '20' ? 'selected' : '' ?>>20px - Max rundat</option>
                        </select>
                    </div>
                </div>
                <small>Rekommenderat: 32px padding + 12px radius för professionell look</small>
            </div>

            <!-- Info Box -->
            <div class="info-box mt-lg">
                <p>
                    <i data-lucide="info"></i>
                    <span>
                        <strong>Så fungerar det:</strong> Samma radius appliceras på ALLA kort, knappar och containers inom varje plattform.
                        Spara och ladda om sidan för att se effekten, eller ändra din browser-storlek för att testa olika breakpoints.
                    </span>
                </p>
            </div>
        </div>
    </div>

    <!-- Layout Section -->
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="maximize-2"></i>
                Layout-dimensioner
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-lg">
                Styr bredden pa huvudinnehallet och andra globala layout-dimensioner.
            </p>

            <?php
            $layout = $branding['layout'] ?? [];
            $contentMaxWidth = $layout['content_max_width'] ?? '1400';
            $sidebarWidth = $layout['sidebar_width'] ?? '72';
            $headerHeight = $layout['header_height'] ?? '60';
            ?>

            <div class="grid-auto-250">
                <!-- Content Max Width -->
                <div class="device-settings device-settings--orange">
                    <h4 class="device-settings-header">
                        <i data-lucide="monitor"></i>
                        Max innehallsbredd
                    </h4>
                    <div>
                        <label class="form-label-block">Desktop (1024px+)</label>
                        <select name="content_max_width" class="form-control w-full">
                            <option value="1200" <?= $contentMaxWidth === '1200' ? 'selected' : '' ?>>1200px - Kompakt</option>
                            <option value="1400" <?= $contentMaxWidth === '1400' ? 'selected' : '' ?>>1400px - Standard</option>
                            <option value="1600" <?= $contentMaxWidth === '1600' ? 'selected' : '' ?>>1600px - Bred</option>
                            <option value="1800" <?= $contentMaxWidth === '1800' ? 'selected' : '' ?>>1800px - Extra bred</option>
                            <option value="none" <?= $contentMaxWidth === 'none' ? 'selected' : '' ?>>Ingen grans (full bredd)</option>
                        </select>
                    </div>
                    <small>Begransar bredden pa huvudinnehallet. Paverkar inte Event-sidor.</small>
                </div>

                <!-- Sidebar Width -->
                <div class="device-settings device-settings--green">
                    <h4 class="device-settings-header">
                        <i data-lucide="sidebar"></i>
                        Sidopanelens bredd
                    </h4>
                    <div>
                        <label class="form-label-block">Desktop sidebar</label>
                        <select name="sidebar_width" class="form-control w-full">
                            <option value="56" <?= $sidebarWidth === '56' ? 'selected' : '' ?>>56px - Kompakt</option>
                            <option value="72" <?= $sidebarWidth === '72' ? 'selected' : '' ?>>72px - Standard</option>
                            <option value="88" <?= $sidebarWidth === '88' ? 'selected' : '' ?>>88px - Bred</option>
                        </select>
                    </div>
                    <small>Endast synlig pa desktop (900px+)</small>
                </div>

                <!-- Header Height -->
                <div class="device-settings device-settings--purple">
                    <h4 class="device-settings-header">
                        <i data-lucide="panel-top"></i>
                        Headerns hojd
                    </h4>
                    <div>
                        <label class="form-label-block">Global header</label>
                        <select name="header_height" class="form-control w-full">
                            <option value="48" <?= $headerHeight === '48' ? 'selected' : '' ?>>48px - Kompakt</option>
                            <option value="56" <?= $headerHeight === '56' ? 'selected' : '' ?>>56px - Lag</option>
                            <option value="60" <?= $headerHeight === '60' ? 'selected' : '' ?>>60px - Standard</option>
                            <option value="64" <?= $headerHeight === '64' ? 'selected' : '' ?>>64px - Hog</option>
                        </select>
                    </div>
                    <small>Paverkar toppbaren pa alla sidor</small>
                </div>
            </div>

            <!-- Info Box -->
            <div class="info-box mt-lg">
                <p>
                    <i data-lucide="info"></i>
                    <span>
                        <strong>CSS-variabler:</strong> Dessa varden satter <code>--content-max-width</code>, <code>--sidebar-width</code> och <code>--header-height</code>.
                    </span>
                </p>
            </div>
        </div>
    </div>
</form>

<!-- Display-only Design System Reference Sections -->

<!-- Typography Section -->
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="type"></i>
                Typografi
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-lg">
                Förhandsvisning av de olika typsnitten som används på sidan.
            </p>

            <?php foreach ($fonts as $fontKey => $fontInfo): ?>
            <div class="font-preview">
                <h4><?= h($fontInfo['label']) ?> - <?= h($fontInfo['value']) ?></h4>
                <code class="text-secondary text-sm">var(--font-<?= $fontKey ?>)</code>
                <div class="font-sample <?= $fontKey ?>">
                    <?= h($fontInfo['example']) ?>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>

    <!-- Spacing Section -->
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="ruler"></i>
                Spacing
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-lg">
                Standardiserade avstånd som används för marginaler och padding.
            </p>

            <div class="spacing-grid">
                <?php foreach ($spacings as $name => $value): ?>
                <div class="spacing-item">
                    <div class="spacing-bar" style="width: <?= $value ?>;"></div>
                    <div class="spacing-label">
                        --space-<?= $name ?><br>
                        <strong><?= $value ?></strong>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <!-- Radius Section -->
    <div class="card mb-lg">
        <div class="card-header">
            <h2>
                <i data-lucide="square"></i>
                Border Radius
            </h2>
        </div>
        <div class="card-body">
            <p class="text-secondary mb-lg">
                Standardiserade hörnradier för knappar, kort och andra element.
            </p>

            <div class="radius-grid">
                <?php foreach ($radii as $name => $value): ?>
                <div class="radius-item">
                    <div class="radius-sample" style="border-radius: <?= $value ?>;"></div>
                    <div class="radius-label">
                        --radius-<?= $name ?><br>
                        <?= $value ?>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <!-- Live Preview -->
    <div class="live-preview">
        <h3 class="mb-md">
            <i data-lucide="eye"></i>
            Live Preview
        </h3>

        <div class="preview-buttons">
            <button type="button" class="btn btn--primary">Primär knapp</button>
            <button type="button" class="btn btn--secondary">Sekundär knapp</button>
            <button type="button" class="btn btn--ghost">Ghost knapp</button>
            <span class="badge badge--primary">Badge</span>
            <span class="badge badge--success">Success</span>
            <span class="badge badge--warning">Warning</span>
            <span class="badge badge--error">Error</span>
        </div>

        <div class="preview-alerts">
            <div class="alert alert--success">
                <i data-lucide="check-circle"></i>
                Detta är ett framgångsmeddelande
            </div>
            <div class="alert alert--warning">
                <i data-lucide="alert-triangle"></i>
                Detta är en varning
            </div>
            <div class="alert alert--error">
                <i data-lucide="x-circle"></i>
                Detta är ett felmeddelande
            </div>
            <div class="alert alert--info">
                <i data-lucide="info"></i>
                Detta är ett informationsmeddelande
            </div>
        </div>
    </div>

<!-- Color Picker CSS & JS -->
<link rel="stylesheet" href="/assets/css/color-picker.css">
<script src="/assets/js/color-picker.js"></script>

<script>
// Theme tab switching
function switchThemeTab(theme) {
    // Update tabs
    document.querySelectorAll('.theme-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.theme === theme);
    });

    // Update panels
    document.getElementById('dark-theme-panel').style.display = theme === 'dark' ? 'block' : 'none';
    document.getElementById('light-theme-panel').style.display = theme === 'light' ? 'block' : 'none';

    // Re-initialize Lucide icons for the new panel
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Open advanced color picker
function openColorPicker(btn, theme, varKey) {
    const currentValue = btn.style.backgroundColor;
    const row = btn.closest('.color-item');
    const hiddenInput = row.querySelector('input[type="hidden"]');
    const textInput = row.querySelector('.color-input');

    // Get hex value from text input or convert from rgb
    let hexValue = textInput.value;
    if (!hexValue.startsWith('#')) {
        hexValue = '#000000';
    }

    HubColorPicker.open(hexValue, (newColor) => {
        // Update swatch
        btn.style.backgroundColor = newColor;

        // Update hidden input (for form submission)
        hiddenInput.value = newColor;

        // Update text input
        textInput.value = newColor;

        // Apply live preview if editing current theme
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        if (theme === currentTheme) {
            document.documentElement.style.setProperty('--color-' + varKey, newColor);
        }
    }, btn);
}

// Update from text input
function updateFromText(input, theme) {
    const varKey = input.dataset.var;
    const value = input.value;
    const row = input.closest('.color-item');
    const swatch = row.querySelector('.color-swatch-btn');
    const hiddenInput = row.querySelector('input[type="hidden"]');

    // Update swatch background
    swatch.style.backgroundColor = value;

    // Update hidden input
    hiddenInput.value = value;

    // Apply live preview if editing current theme
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    if (theme === currentTheme) {
        document.documentElement.style.setProperty('--color-' + varKey, value);
    }
}

// Live preview for responsive settings
function previewResponsive(device, type, value) {
    const width = window.innerWidth;

    // Determine if current viewport matches device
    let applies = false;
    if (device === 'portrait' && width <= 767) applies = true;
    if (device === 'tablet' && width >= 768 && width <= 1023) applies = true;
    if (device === 'desktop' && width >= 1024) applies = true;

    if (!applies) {
        console.log(`Preview skipped - current viewport (${width}px) doesn't match ${device}`);
        return;
    }

    // Apply preview
    if (type === 'padding') {
        document.documentElement.style.setProperty('--container-padding', value + 'px');
    } else if (type === 'radius') {
        document.documentElement.style.setProperty('--radius-sm', value + 'px');
        document.documentElement.style.setProperty('--radius-md', value + 'px');
        document.documentElement.style.setProperty('--radius-lg', value + 'px');
        document.documentElement.style.setProperty('--radius-xl', value + 'px');
    }
}

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// ============================================================================
// MEDIA PICKER FUNCTIONS
// ============================================================================

let currentLogoField = null;
let mediaData = [];

async function openMediaPicker(field) {
    currentLogoField = field;
    const modal = document.getElementById('mediaPickerModal');
    const grid = document.getElementById('mediaGrid');

    grid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--color-text-secondary);">Laddar bilder...</div>';
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    try {
        const response = await fetch('/api/media.php?action=list&folder=branding&limit=100');
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            mediaData = result.data;
            renderMediaGrid();
        } else {
            grid.innerHTML = `
                <div style="text-align: center; padding: 40px; color: var(--color-text-secondary); grid-column: 1/-1;">
                    <p class="mb-md">Inga bilder i branding-mappen.</p>
                    <a href="/admin/media?folder=branding" target="_blank" class="btn btn--primary">
                        <i data-lucide="upload"></i>
                        Ladda upp bilder
                    </a>
                </div>
            `;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } catch (error) {
        console.error('Error loading media:', error);
        grid.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--color-danger);">Kunde inte ladda bilder</div>';
    }
}

function renderMediaGrid() {
    const grid = document.getElementById('mediaGrid');
    grid.innerHTML = mediaData.map(media => `
        <div class="media-item" onclick="selectMedia('${media.filepath}')">
            <img src="/${media.filepath}" alt="${media.original_filename || ''}">
            <div class="media-item-name">${media.original_filename || 'Bild'}</div>
        </div>
    `).join('');
}

function selectMedia(filepath) {
    if (!currentLogoField) return;

    const capitalizedField = currentLogoField.charAt(0).toUpperCase() + currentLogoField.slice(1);
    const inputId = 'logo' + capitalizedField + 'Input';
    const previewId = 'logo' + capitalizedField + 'Preview';
    const url = '/' + filepath.replace(/^\//, '');

    document.getElementById(inputId).value = url;
    document.getElementById(previewId).innerHTML = `<img src="${url}" alt="Logo">`;

    // Enable remove button
    const colorGroup = document.getElementById(previewId).closest('.color-group');
    const removeBtn = colorGroup.querySelector('button[onclick*="clearLogo"]');
    if (removeBtn) removeBtn.disabled = false;

    closeMediaModal();
}

function clearLogo(field) {
    const capitalizedField = field.charAt(0).toUpperCase() + field.slice(1);
    const inputId = 'logo' + capitalizedField + 'Input';
    const previewId = 'logo' + capitalizedField + 'Preview';

    document.getElementById(inputId).value = '';
    document.getElementById(previewId).innerHTML = `<span class="logo-preview-placeholder">Klicka för att välja bild</span>`;

    // Disable remove button
    const colorGroup = document.getElementById(previewId).closest('.color-group');
    const removeBtn = colorGroup.querySelector('button[onclick*="clearLogo"]');
    if (removeBtn) removeBtn.disabled = true;
}

function closeMediaModal() {
    const modal = document.getElementById('mediaPickerModal');
    modal.style.display = 'none';
    document.body.style.overflow = '';
    currentLogoField = null;
}

// Close modal on escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeMediaModal();
    }
});

// Close modal on backdrop click
document.addEventListener('DOMContentLoaded', function() {
    const pickerModal = document.getElementById('mediaPickerModal');
    if (pickerModal) {
        pickerModal.addEventListener('click', (e) => {
            if (e.target.id === 'mediaPickerModal') closeMediaModal();
        });
    }
});

// Hover effect for preview boxes
document.querySelectorAll('.logo-preview-box').forEach(box => {
    box.addEventListener('mouseenter', () => box.style.borderColor = 'var(--color-accent)');
    box.addEventListener('mouseleave', () => box.style.borderColor = 'var(--color-border)');
});

// Move modal to body for proper fixed positioning
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('mediaPickerModal');
    if (modal) {
        document.body.appendChild(modal);
    }
});
</script>

<!-- Media Picker Modal (will be moved to body via JS) -->
<div class="media-picker-modal-overlay admin-modal" id="mediaPickerModal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 99999; align-items: center; justify-content: center;">
    <div class="admin-modal-content modal-content" style="background: var(--color-bg-surface); border-radius: var(--radius-lg); max-width: 700px; width: 90%; max-height: 80vh; display: flex; flex-direction: column; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);">
        <div class="admin-modal-header modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: var(--space-lg); border-bottom: 1px solid var(--color-border);">
            <h3 style="margin: 0; font-size: var(--text-lg);">Välj bild från Mediabiblioteket</h3>
            <button type="button" class="modal-close admin-modal-close" onclick="closeMediaModal()" style="background: none; border: none; cursor: pointer; padding: var(--space-sm); color: var(--color-text-secondary); min-width: 44px; min-height: 44px;">
                <i data-lucide="x"></i>
            </button>
        </div>
        <div class="admin-modal-body modal-body" style="padding: var(--space-lg); overflow-y: auto; flex: 1; -webkit-overflow-scrolling: touch;">
            <div id="mediaGrid" class="media-grid">
                <!-- Media items will be loaded here -->
            </div>
        </div>
        <div class="admin-modal-footer modal-footer" style="display: flex; justify-content: space-between; align-items: center; padding: var(--space-md) var(--space-lg); border-top: 1px solid var(--color-border); background: var(--color-bg-sunken); gap: var(--space-sm); flex-wrap: wrap;">
            <a href="/admin/media?folder=branding" target="_blank" class="btn btn--secondary btn--sm">
                <i data-lucide="external-link"></i>
                Öppna Mediabiblioteket
            </a>
            <button type="button" class="btn btn--ghost btn--sm" onclick="closeMediaModal()">Avbryt</button>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
