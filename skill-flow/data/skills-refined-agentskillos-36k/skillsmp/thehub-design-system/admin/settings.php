<?php
/**
 * Admin Settings - V3 Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $publicRidersDisplay = $_POST['public_riders_display'] ?? 'with_results';

    // Update settings file
    $settingsContent = "<?php\n";
    $settingsContent .= "/**\n";
    $settingsContent .= " * Public Display Settings\n";
    $settingsContent .= " * Configure what data is visible on the public website\n";
    $settingsContent .= " */\n\n";
    $settingsContent .= "return [\n";
    $settingsContent .= "    // Show all riders publicly or only those with results\n";
    $settingsContent .= "    // Options: 'all' or 'with_results'\n";
    $settingsContent .= "    'public_riders_display' => '{$publicRidersDisplay}',\n\n";
    $settingsContent .= "    // Minimum number of results required to show rider (when 'with_results' is selected)\n";
    $settingsContent .= "    'min_results_to_show' => 1,\n";
    $settingsContent .= "];\n";

    if (file_put_contents(__DIR__ . '/../config/public_settings.php', $settingsContent)) {
        set_flash('success', 'Inställningar sparade!');
        redirect('/admin/settings');
    } else {
        $message = 'Kunde inte spara inställningar';
        $messageType = 'error';
    }
}

// Load current settings
$currentSettings = require __DIR__ . '/../config/public_settings.php';

// Page config for V3 admin layout
$page_title = 'Inställningar';
$breadcrumbs = [
    ['label' => 'Inställningar']
];

// Include unified layout (uses same layout as public site)
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType ?>">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <?php if ($messageType === 'success'): ?>
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
            <?php else: ?>
                <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>
            <?php endif; ?>
        </svg>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<!-- Public Display Settings -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Publik Visning</h2>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <?= csrf_field() ?>

            <div class="admin-form-group">
                <label class="admin-form-label">
                    Visa deltagare publikt
                </label>
                <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
                    Välj vilka deltagare som ska visas på den publika deltagarsidan
                </p>

                <div style="display: flex; flex-direction: column; gap: var(--space-md);">
                    <label style="display: flex; align-items: flex-start; gap: var(--space-md); padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md); cursor: pointer;">
                        <input type="radio"
                            name="public_riders_display"
                            value="with_results"
                            <?= ($currentSettings['public_riders_display'] ?? 'with_results') === 'with_results' ? 'checked' : '' ?>
                            style="margin-top: 4px;">
                        <span>
                            <strong style="display: block;">Endast deltagare med resultat</strong>
                            <span style="color: var(--color-text-secondary); font-size: var(--text-sm);">
                                Visar bara cyklister som har minst ett tävlingsresultat uppladdat
                            </span>
                        </span>
                    </label>

                    <label style="display: flex; align-items: flex-start; gap: var(--space-md); padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md); cursor: pointer;">
                        <input type="radio"
                            name="public_riders_display"
                            value="all"
                            <?= ($currentSettings['public_riders_display'] ?? 'with_results') === 'all' ? 'checked' : '' ?>
                            style="margin-top: 4px;">
                        <span>
                            <strong style="display: block;">Alla aktiva deltagare</strong>
                            <span style="color: var(--color-text-secondary); font-size: var(--text-sm);">
                                Visar alla cyklister i databasen, även de utan resultat
                            </span>
                        </span>
                    </label>
                </div>
            </div>

            <div class="admin-form-actions">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                    Spara Inställningar
                </button>
                <a href="/admin/dashboard" class="btn-admin btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
                    Tillbaka
                </a>
            </div>
        </form>
    </div>
</div>

<!-- Admin Tools -->
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="shield"></i>
            Behörigheter & Roller
        </h2>
    </div>
    <div class="card-body">
        <div class="flex flex-col gap-md">
            <a href="/admin/role-management.php" class="btn btn--secondary w-full justify-start">
                <i data-lucide="star"></i>
                Rollhantering (Promotörer)
            </a>
            <a href="/admin/club-admins.php" class="btn btn--secondary w-full justify-start">
                <i data-lucide="building"></i>
                Klubb-administratörer
            </a>
            <a href="/admin/tools.php" class="btn btn--secondary w-full justify-start">
                <i data-lucide="wrench"></i>
                Verktyg
            </a>
        </div>
    </div>
</div>

<!-- Info Box -->
<div class="alert alert-info">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>
    </svg>
    <div>
        <strong>Information:</strong>
        <ul style="margin: var(--space-sm) 0 0 var(--space-lg); list-style: disc;">
            <li>Ändringarna träder i kraft omedelbart på den publika sidan</li>
            <li>Admin-sidan visar alltid alla deltagare oavsett denna inställning</li>
            <li>Deltagare med SWE-ID (ingen licens) visas med röd badge</li>
        </ul>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
