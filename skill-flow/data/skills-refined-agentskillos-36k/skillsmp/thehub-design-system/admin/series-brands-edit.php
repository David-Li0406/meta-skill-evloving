<?php
/**
 * Admin Series Brands - Edit Brand
 * Dedicated page for editing series brands
 */
require_once __DIR__ . '/../config.php';
require_admin();

$pdo = $GLOBALS['pdo'];

// Get brand ID from URL
$id = intval($_GET['id'] ?? 0);

if ($id <= 0) {
    $_SESSION['message'] = 'Ogiltigt varumärkes-ID';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/series-brands.php');
    exit;
}

// Check if series_brands table exists
$tableExists = false;
try {
    $check = $pdo->query("SHOW TABLES LIKE 'series_brands'")->fetchAll();
    $tableExists = !empty($check);
} catch (Exception $e) {
    $tableExists = false;
}

if (!$tableExists) {
    $_SESSION['message'] = 'Tabellen series_brands finns inte.';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/series-brands.php');
    exit;
}

// Fetch brand data
$stmt = $pdo->prepare("SELECT * FROM series_brands WHERE id = ?");
$stmt->execute([$id]);
$brand = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$brand) {
    $_SESSION['message'] = 'Varumärke hittades inte';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/series-brands.php');
    exit;
}

// Get series count for this brand
$countStmt = $pdo->prepare("SELECT COUNT(*) as cnt FROM series WHERE brand_id = ?");
$countStmt->execute([$id]);
$seriesCount = $countStmt->fetch(PDO::FETCH_ASSOC)['cnt'] ?? 0;

// Initialize message variables
$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $name = trim($_POST['name'] ?? '');

    if (empty($name)) {
        $message = 'Namn är obligatoriskt';
        $messageType = 'error';
    } else {
        // Handle logo upload
        $logoPath = $brand['logo']; // Keep existing logo by default
        if (isset($_FILES['logo']) && $_FILES['logo']['error'] === UPLOAD_ERR_OK) {
            $uploadDir = __DIR__ . '/../uploads/series-brands/';
            if (!is_dir($uploadDir)) {
                mkdir($uploadDir, 0755, true);
            }

            $fileExtension = strtolower(pathinfo($_FILES['logo']['name'], PATHINFO_EXTENSION));
            $allowedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'];

            if (in_array($fileExtension, $allowedExtensions)) {
                $fileName = uniqid('brand_') . '.' . $fileExtension;
                $targetPath = $uploadDir . $fileName;

                if (move_uploaded_file($_FILES['logo']['tmp_name'], $targetPath)) {
                    // Delete old logo if exists
                    if ($brand['logo'] && file_exists(__DIR__ . '/..' . $brand['logo'])) {
                        @unlink(__DIR__ . '/..' . $brand['logo']);
                    }
                    $logoPath = '/uploads/series-brands/' . $fileName;
                }
            }
        }

        // Handle logo removal
        if (isset($_POST['remove_logo']) && $_POST['remove_logo'] === '1') {
            if ($brand['logo'] && file_exists(__DIR__ . '/..' . $brand['logo'])) {
                @unlink(__DIR__ . '/..' . $brand['logo']);
            }
            $logoPath = null;
        }

        // Generate slug from name
        $slug = strtolower(preg_replace('/[^a-z0-9]+/i', '-', $name));
        $slug = trim($slug, '-');

        try {
            $stmt = $pdo->prepare("
                UPDATE series_brands SET
                    name = ?,
                    slug = ?,
                    description = ?,
                    website = ?,
                    gradient_start = ?,
                    gradient_end = ?,
                    accent_color = ?,
                    active = ?,
                    display_order = ?,
                    logo = ?
                WHERE id = ?
            ");
            $stmt->execute([
                $name,
                $slug,
                trim($_POST['description'] ?? ''),
                trim($_POST['website'] ?? ''),
                $_POST['gradient_start'] ?? '#004A98',
                $_POST['gradient_end'] ?? '#002a5c',
                $_POST['accent_color'] ?? '#61CE70',
                isset($_POST['active']) ? 1 : 0,
                intval($_POST['display_order'] ?? 0),
                $logoPath,
                $id
            ]);

            $_SESSION['message'] = 'Varumärke uppdaterat!';
            $_SESSION['messageType'] = 'success';
            header('Location: /admin/series-brands.php');
            exit;
        } catch (Exception $e) {
            $message = 'Ett fel uppstod: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Page config
$page_title = 'Redigera ' . htmlspecialchars($brand['name']);
$page_group = 'standings';
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series.php'],
    ['label' => 'Varumärken', 'url' => '/admin/series-brands.php'],
    ['label' => 'Redigera']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?>">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<!-- Brand Info Header -->
<div class="brand-header-preview" style="background: linear-gradient(135deg, <?= htmlspecialchars($brand['gradient_start'] ?? '#004A98') ?>, <?= htmlspecialchars($brand['gradient_end'] ?? '#002a5c') ?>);">
    <?php if ($brand['logo']): ?>
        <img src="<?= htmlspecialchars($brand['logo']) ?>" alt="<?= htmlspecialchars($brand['name']) ?>" class="brand-header-logo">
    <?php else: ?>
        <span class="brand-header-name"><?= htmlspecialchars($brand['name']) ?></span>
    <?php endif; ?>
    <div class="brand-header-stats">
        <span class="badge"><?= $seriesCount ?> serier</span>
        <span class="badge <?= $brand['active'] ? 'badge-success' : 'badge-secondary' ?>"><?= $brand['active'] ? 'Aktiv' : 'Inaktiv' ?></span>
    </div>
</div>

<form method="POST" enctype="multipart/form-data">
    <?= csrf_field() ?>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <i data-lucide="info"></i>
                Grunduppgifter
            </h2>
        </div>
        <div class="admin-card-body">
            <div class="admin-form-grid">
                <div class="admin-form-group admin-form-full">
                    <label for="name" class="admin-form-label">Namn <span class="required">*</span></label>
                    <input type="text" id="name" name="name" class="admin-form-input" required
                           placeholder="T.ex. Swecup, GravitySeries Enduro"
                           value="<?= htmlspecialchars($brand['name']) ?>">
                </div>

                <div class="admin-form-group admin-form-full">
                    <label for="description" class="admin-form-label">Beskrivning</label>
                    <textarea id="description" name="description" class="admin-form-textarea" rows="3"
                              placeholder="Kort beskrivning av varumärket..."><?= htmlspecialchars($brand['description'] ?? '') ?></textarea>
                </div>

                <div class="admin-form-group">
                    <label for="website" class="admin-form-label">Webbsida</label>
                    <input type="url" id="website" name="website" class="admin-form-input"
                           placeholder="https://..."
                           value="<?= htmlspecialchars($brand['website'] ?? '') ?>">
                </div>

                <div class="admin-form-group">
                    <label for="display_order" class="admin-form-label">Visningsordning</label>
                    <input type="number" id="display_order" name="display_order" class="admin-form-input"
                           value="<?= intval($brand['display_order'] ?? 0) ?>" min="0">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Status</label>
                    <label class="admin-checkbox">
                        <input type="checkbox" name="active" <?= $brand['active'] ? 'checked' : '' ?>>
                        <span>Aktiv</span>
                    </label>
                </div>
            </div>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <i data-lucide="palette"></i>
                Färg
            </h2>
        </div>
        <div class="admin-card-body">
            <p class="text-secondary mb-lg">Välj en huvudfärg - gradienten skapas automatiskt.</p>

            <div class="color-preview-bar" id="colorPreview" style="height: 80px; border-radius: var(--radius-md); margin-bottom: var(--space-lg);"></div>

            <div class="admin-form-group">
                <label for="brand_color" class="admin-form-label">Huvudfärg</label>
                <div style="display: flex; gap: var(--space-md); align-items: center;">
                    <input type="color" id="brand_color" name="brand_color" class="admin-form-color"
                           value="<?= htmlspecialchars($brand['accent_color'] ?? $brand['gradient_start'] ?? '#004A98') ?>"
                           onchange="updateColorPreview()" style="width: 80px; height: 50px;">
                    <input type="text" id="brand_color_text" class="admin-form-input" style="width: 120px; font-family: monospace;"
                           value="<?= htmlspecialchars($brand['accent_color'] ?? $brand['gradient_start'] ?? '#004A98') ?>"
                           onchange="document.getElementById('brand_color').value = this.value; updateColorPreview();">
                    <span class="text-secondary" style="font-size: var(--text-sm);">Gradienten skapas automatiskt</span>
                </div>
            </div>

            <!-- Hidden fields for generated colors -->
            <input type="hidden" id="gradient_start" name="gradient_start" value="">
            <input type="hidden" id="gradient_end" name="gradient_end" value="">
            <input type="hidden" id="accent_color" name="accent_color" value="">
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2>
                <i data-lucide="image"></i>
                Logotyp
            </h2>
        </div>
        <div class="admin-card-body">
            <?php if ($brand['logo']): ?>
                <div class="current-logo-preview">
                    <img src="<?= htmlspecialchars($brand['logo']) ?>" alt="Nuvarande logotyp">
                    <div class="current-logo-actions">
                        <label class="admin-checkbox">
                            <input type="checkbox" name="remove_logo" value="1">
                            <span>Ta bort logotyp</span>
                        </label>
                    </div>
                </div>
            <?php endif; ?>

            <div class="admin-form-group">
                <label for="logo" class="admin-form-label"><?= $brand['logo'] ? 'Byt logotyp' : 'Ladda upp logotyp' ?></label>
                <input type="file" id="logo" name="logo" class="admin-form-input" accept="image/*">
                <small class="admin-form-hint">Tillåtna format: JPG, PNG, GIF, WebP, SVG. Max 10MB.</small>
            </div>
        </div>
    </div>

    <!-- Action Buttons -->
    <div class="admin-form-actions">
        <a href="/admin/series-brands.php" class="btn-admin btn-admin-secondary">
            <i data-lucide="x"></i>
            Avbryt
        </a>
        <button type="submit" class="btn-admin btn-admin-primary">
            <i data-lucide="save"></i>
            Spara ändringar
        </button>
    </div>
</form>

<style>
.brand-header-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: var(--space-md);
    padding: var(--space-xl);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-lg);
    min-height: 120px;
}

.brand-header-logo {
    max-height: 60px;
    max-width: 200px;
    object-fit: contain;
    filter: brightness(0) invert(1);
}

.brand-header-name {
    color: white;
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    text-transform: uppercase;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.brand-header-stats {
    display: flex;
    gap: var(--space-sm);
}

.brand-header-stats .badge {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
}

.brand-header-stats .badge-success {
    background: var(--color-success);
}

.brand-header-stats .badge-secondary {
    background: rgba(255,255,255,0.3);
}

.current-logo-preview {
    display: flex;
    align-items: center;
    gap: var(--space-lg);
    padding: var(--space-md);
    background: var(--color-bg-tertiary);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-lg);
}

.current-logo-preview img {
    max-width: 150px;
    max-height: 80px;
    object-fit: contain;
}

.admin-form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-lg);
}

.admin-form-full {
    grid-column: 1 / -1;
}

.admin-form-textarea {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-bg);
    color: var(--color-text);
    font-family: inherit;
    font-size: var(--text-sm);
    resize: vertical;
}

.admin-form-textarea:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px var(--color-accent-alpha);
}

.admin-form-color {
    width: 50px;
    height: 40px;
    padding: 4px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    cursor: pointer;
}

.admin-checkbox {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    cursor: pointer;
    padding: var(--space-sm) 0;
}

.admin-checkbox input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--color-accent);
}

.admin-form-hint {
    display: block;
    margin-top: var(--space-xs);
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
}

.admin-form-actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-md);
    padding: var(--space-lg) 0;
}

.required {
    color: var(--color-error);
}
</style>

<script>
// Convert hex to HSL
function hexToHsl(hex) {
    let r = parseInt(hex.slice(1, 3), 16) / 255;
    let g = parseInt(hex.slice(3, 5), 16) / 255;
    let b = parseInt(hex.slice(5, 7), 16) / 255;

    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0;
    } else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
            case g: h = ((b - r) / d + 2) / 6; break;
            case b: h = ((r - g) / d + 4) / 6; break;
        }
    }
    return { h: h * 360, s: s * 100, l: l * 100 };
}

// Convert HSL to hex
function hslToHex(h, s, l) {
    s /= 100;
    l /= 100;
    const a = s * Math.min(l, 1 - l);
    const f = n => {
        const k = (n + h / 30) % 12;
        const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
        return Math.round(255 * color).toString(16).padStart(2, '0');
    };
    return `#${f(0)}${f(8)}${f(4)}`;
}

function updateColorPreview() {
    const baseColor = document.getElementById('brand_color').value;
    document.getElementById('brand_color_text').value = baseColor;

    // Generate gradient colors from base color
    const hsl = hexToHsl(baseColor);

    // Gradient start = base color (slightly lighter)
    const gradientStart = hslToHex(hsl.h, Math.min(hsl.s + 5, 100), Math.min(hsl.l + 5, 95));

    // Gradient end = darker version
    const gradientEnd = hslToHex(hsl.h, hsl.s, Math.max(hsl.l - 25, 10));

    // Accent = base color (used for text/dates)
    const accentColor = baseColor;

    // Update hidden fields
    document.getElementById('gradient_start').value = gradientStart;
    document.getElementById('gradient_end').value = gradientEnd;
    document.getElementById('accent_color').value = accentColor;

    // Update preview
    document.getElementById('colorPreview').style.background = `linear-gradient(135deg, ${gradientStart}, ${gradientEnd})`;
}

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    updateColorPreview();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
