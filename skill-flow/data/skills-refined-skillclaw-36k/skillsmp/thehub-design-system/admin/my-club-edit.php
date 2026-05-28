<?php
/**
 * My Club Edit - Club Admin Edit Page
 * Allows users with club_admin permissions to edit their assigned clubs
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$currentUser = getCurrentAdmin();

// Get club ID
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : 0;

if (!$id) {
    header('Location: /admin/my-clubs.php');
    exit;
}

// Check permissions
$perms = getClubAdminPermissions($id);
if (!$perms) {
    $_SESSION['message'] = 'Du har inte behörighet att redigera denna klubb.';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/my-clubs.php');
    exit;
}

// Fetch club data
$club = $db->getRow("SELECT * FROM clubs WHERE id = ?", [$id]);

if (!$club) {
    $_SESSION['message'] = 'Klubb hittades inte.';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/my-clubs.php');
    exit;
}

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    // Check edit permission
    if (!$perms['can_edit_profile']) {
        $message = 'Du har inte behörighet att redigera klubbinformation.';
        $messageType = 'error';
    } else {
        $name = trim($_POST['name'] ?? '');

        if (empty($name)) {
            $message = 'Klubbnamn är obligatoriskt.';
            $messageType = 'error';
        } else {
            $logoValue = trim($_POST['logo'] ?? '');
            $clubData = [
                'name' => $name,
                'short_name' => trim($_POST['short_name'] ?? ''),
                'org_number' => trim($_POST['org_number'] ?? ''),
                'region' => trim($_POST['region'] ?? ''),
                'city' => trim($_POST['city'] ?? ''),
                'country' => trim($_POST['country'] ?? 'Sverige'),
                'address' => trim($_POST['address'] ?? ''),
                'postal_code' => trim($_POST['postal_code'] ?? ''),
                'website' => trim($_POST['website'] ?? ''),
                'email' => trim($_POST['email'] ?? ''),
                'phone' => trim($_POST['phone'] ?? ''),
                'contact_person' => trim($_POST['contact_person'] ?? ''),
                'description' => trim($_POST['description'] ?? ''),
                'facebook' => trim($_POST['facebook'] ?? ''),
                'instagram' => trim($_POST['instagram'] ?? ''),
                'youtube' => trim($_POST['youtube'] ?? ''),
                'tiktok' => trim($_POST['tiktok'] ?? ''),
                'swish_number' => trim($_POST['swish_number'] ?? ''),
                'swish_name' => trim($_POST['swish_name'] ?? ''),
            ];

            // Only update logo if user has permission
            if ($perms['can_upload_logo']) {
                $clubData['logo'] = $logoValue;
                $clubData['logo_url'] = $logoValue;
            }

            try {
                $db->update('clubs', $clubData, 'id = ?', [$id]);
                $message = 'Klubb uppdaterad!';
                $messageType = 'success';

                // Refresh club data
                $club = $db->getRow("SELECT * FROM clubs WHERE id = ?", [$id]);
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get rider count
$riderCount = $db->getRow("SELECT COUNT(*) as count FROM riders WHERE club_id = ?", [$id])['count'] ?? 0;

$page_title = 'Redigera ' . h($club['name']);
$breadcrumbs = [
    ['label' => 'Mina Klubbar', 'url' => '/admin/my-clubs.php'],
    ['label' => h($club['name'])]
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
<div class="alert alert--<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Permission info -->
<?php if (!hasRole('admin')): ?>
<div class="alert alert--info mb-lg">
    <i data-lucide="info"></i>
    <div>
        <strong>Dina behörigheter för denna klubb:</strong>
        <div class="flex gap-sm flex-wrap mt-sm">
            <?php if ($perms['can_edit_profile']): ?>
            <span class="badge badge-success"><i data-lucide="check" class="icon-xs"></i> Redigera information</span>
            <?php else: ?>
            <span class="badge badge-secondary"><i data-lucide="x" class="icon-xs"></i> Redigera information</span>
            <?php endif; ?>
            <?php if ($perms['can_upload_logo']): ?>
            <span class="badge badge-success"><i data-lucide="check" class="icon-xs"></i> Ladda upp logotyp</span>
            <?php else: ?>
            <span class="badge badge-secondary"><i data-lucide="x" class="icon-xs"></i> Ladda upp logotyp</span>
            <?php endif; ?>
            <?php if ($perms['can_manage_members']): ?>
            <span class="badge badge-success"><i data-lucide="check" class="icon-xs"></i> Hantera medlemmar</span>
            <?php else: ?>
            <span class="badge badge-secondary"><i data-lucide="x" class="icon-xs"></i> Hantera medlemmar</span>
            <?php endif; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<form method="POST">
    <?= csrf_field() ?>

    <div class="club-edit-layout">
        <!-- Main Content -->
        <div class="club-edit-main">
            <!-- Basic Information -->
            <div class="card mb-lg">
                <div class="card-header">
                    <h2 class="text-primary">
                        <i data-lucide="info"></i>
                        Grundläggande information
                    </h2>
                </div>
                <div class="card-body">
                    <div class="grid gap-md">
                        <!-- Name -->
                        <div>
                            <label for="name" class="label">Klubbnamn <span class="text-error">*</span></label>
                            <input type="text" id="name" name="name" class="input" required
                                   value="<?= h($club['name']) ?>"
                                   <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                        </div>

                        <!-- Short Name and Org Number -->
                        <div class="form-row">
                            <div>
                                <label for="short_name" class="label">Förkortning</label>
                                <input type="text" id="short_name" name="short_name" class="input"
                                       value="<?= h($club['short_name'] ?? '') ?>"
                                       placeholder="T.ex. UCK"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="org_number" class="label">Organisationsnummer</label>
                                <input type="text" id="org_number" name="org_number" class="input"
                                       value="<?= h($club['org_number'] ?? '') ?>"
                                       placeholder="123456-7890"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                        </div>

                        <!-- Members count (readonly) -->
                        <div>
                            <label class="label">Medlemmar</label>
                            <input type="text" class="input" value="<?= $riderCount ?> aktiva" disabled>
                        </div>

                        <!-- Description -->
                        <div>
                            <label for="description" class="label">Beskrivning</label>
                            <textarea id="description" name="description" class="input" rows="3"
                                      placeholder="Beskriv klubben..."
                                      <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>><?= h($club['description'] ?? '') ?></textarea>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Logo -->
            <?php if ($perms['can_upload_logo']): ?>
            <div class="card mb-lg">
                <div class="card-header">
                    <h2 class="text-primary">
                        <i data-lucide="image"></i>
                        Logotyp
                    </h2>
                </div>
                <div class="card-body">
                    <?php $logoUrl = $club['logo_url'] ?? $club['logo'] ?? ''; ?>
                    <div class="flex items-start gap-lg">
                        <div class="club-logo-container" style="position: relative;">
                            <div class="logo-preview" id="clubLogoPreview" style="width: 150px; height: 100px; border-radius: var(--radius-md); background: var(--color-bg-sunken); display: flex; align-items: center; justify-content: center; overflow: hidden; cursor: pointer; border: 2px dashed var(--color-border);" onclick="document.getElementById('clubLogoInput').click()">
                                <?php if ($logoUrl): ?>
                                <img src="<?= h($logoUrl) ?>" alt="Klubblogotyp" id="clubLogoImage" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                                <?php else: ?>
                                <div class="text-center">
                                    <i data-lucide="image" style="width: 32px; height: 32px; color: var(--color-text-secondary);"></i>
                                    <p class="text-xs text-secondary mt-sm">Klicka för att ladda upp</p>
                                </div>
                                <?php endif; ?>
                            </div>
                            <div id="clubLogoLoading" style="display: none; position: absolute; inset: 0; background: rgba(0,0,0,0.6); border-radius: var(--radius-md); align-items: center; justify-content: center;">
                                <div style="width: 24px; height: 24px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
                            </div>
                        </div>
                        <div style="flex: 1;">
                            <label class="btn btn-secondary" style="cursor: pointer; display: inline-flex;">
                                <i data-lucide="upload" style="width: 16px; height: 16px;"></i>
                                Ladda upp ny logotyp
                                <input type="file" id="clubLogoInput" accept="image/jpeg,image/png,image/gif,image/webp" style="display: none;">
                            </label>
                            <span id="clubLogoStatus" style="font-size: 0.875rem; display: block; margin-top: 0.5rem;"></span>
                            <input type="hidden" name="logo" id="logoUrlInput" value="<?= h($logoUrl) ?>">
                            <p class="text-secondary text-sm mt-md">
                                Max 2MB. Tillåtna format: JPG, PNG, GIF, WebP.<br>
                                Rekommenderad storlek: 400x300 pixlar.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <?php endif; ?>

            <!-- Contact Information -->
            <div class="card mb-lg">
                <div class="card-header">
                    <h2 class="text-primary">
                        <i data-lucide="phone"></i>
                        Kontaktinformation
                    </h2>
                </div>
                <div class="card-body">
                    <div class="grid gap-md">
                        <!-- Contact Person -->
                        <div>
                            <label for="contact_person" class="label">Kontaktperson</label>
                            <input type="text" id="contact_person" name="contact_person" class="input"
                                   value="<?= h($club['contact_person'] ?? '') ?>"
                                   placeholder="Namn på kontaktperson"
                                   <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                        </div>

                        <!-- Email and Phone -->
                        <div class="form-row">
                            <div>
                                <label for="email" class="label">E-post</label>
                                <input type="email" id="email" name="email" class="input"
                                       value="<?= h($club['email'] ?? '') ?>"
                                       placeholder="info@klubb.se"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="phone" class="label">Telefon</label>
                                <input type="tel" id="phone" name="phone" class="input"
                                       value="<?= h($club['phone'] ?? '') ?>"
                                       placeholder="070-123 45 67"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                        </div>

                        <!-- Address -->
                        <div>
                            <label for="address" class="label">Adress</label>
                            <input type="text" id="address" name="address" class="input"
                                   value="<?= h($club['address'] ?? '') ?>"
                                   placeholder="Gatuadress"
                                   <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                        </div>

                        <!-- Postal code and City -->
                        <div class="form-row">
                            <div>
                                <label for="postal_code" class="label">Postnummer</label>
                                <input type="text" id="postal_code" name="postal_code" class="input"
                                       value="<?= h($club['postal_code'] ?? '') ?>"
                                       placeholder="123 45"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="city" class="label">Stad</label>
                                <input type="text" id="city" name="city" class="input"
                                       value="<?= h($club['city'] ?? '') ?>"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                        </div>

                        <!-- Region and Country -->
                        <div class="form-row">
                            <div>
                                <label for="region" class="label">Region/Län</label>
                                <input type="text" id="region" name="region" class="input"
                                       value="<?= h($club['region'] ?? '') ?>"
                                       placeholder="T.ex. Stockholms län"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="country" class="label">Land</label>
                                <select id="country" name="country" class="input" <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                                    <option value="Sverige" <?= ($club['country'] ?? '') === 'Sverige' ? 'selected' : '' ?>>Sverige</option>
                                    <option value="Norge" <?= ($club['country'] ?? '') === 'Norge' ? 'selected' : '' ?>>Norge</option>
                                    <option value="Danmark" <?= ($club['country'] ?? '') === 'Danmark' ? 'selected' : '' ?>>Danmark</option>
                                    <option value="Finland" <?= ($club['country'] ?? '') === 'Finland' ? 'selected' : '' ?>>Finland</option>
                                </select>
                            </div>
                        </div>

                        <!-- Website -->
                        <div>
                            <label for="website" class="label">Webbplats</label>
                            <input type="url" id="website" name="website" class="input"
                                   value="<?= h($club['website'] ?? '') ?>"
                                   placeholder="https://klubb.se"
                                   <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                        </div>

                        <!-- Social Media -->
                        <div class="form-row">
                            <div>
                                <label for="facebook" class="label">
                                    <i data-lucide="facebook" class="icon-sm"></i> Facebook
                                </label>
                                <input type="url" id="facebook" name="facebook" class="input"
                                       value="<?= h($club['facebook'] ?? '') ?>"
                                       placeholder="https://facebook.com/..."
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="instagram" class="label">
                                    <i data-lucide="instagram" class="icon-sm"></i> Instagram
                                </label>
                                <input type="text" id="instagram" name="instagram" class="input"
                                       value="<?= h($club['instagram'] ?? '') ?>"
                                       placeholder="@användarnamn"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                        </div>
                        <div class="form-row">
                            <div>
                                <label for="youtube" class="label">
                                    <i data-lucide="youtube" class="icon-sm"></i> YouTube
                                </label>
                                <input type="url" id="youtube" name="youtube" class="input"
                                       value="<?= h($club['youtube'] ?? '') ?>"
                                       placeholder="https://youtube.com/..."
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="tiktok" class="label">
                                    <i data-lucide="music" class="icon-sm"></i> TikTok
                                </label>
                                <input type="text" id="tiktok" name="tiktok" class="input"
                                       value="<?= h($club['tiktok'] ?? '') ?>"
                                       placeholder="@användarnamn"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Swish/Payment Information -->
            <div class="card mb-lg">
                <div class="card-header">
                    <h2 class="text-primary">
                        <i data-lucide="credit-card"></i>
                        Betalningsinformation
                    </h2>
                </div>
                <div class="card-body">
                    <div class="grid gap-md">
                        <div class="form-row">
                            <div>
                                <label for="swish_number" class="label">Swish-nummer</label>
                                <input type="tel" id="swish_number" name="swish_number" class="input"
                                       value="<?= h($club['swish_number'] ?? '') ?>"
                                       placeholder="070-123 45 67"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                            <div>
                                <label for="swish_name" class="label">Swish-namn</label>
                                <input type="text" id="swish_name" name="swish_name" class="input"
                                       value="<?= h($club['swish_name'] ?? '') ?>"
                                       placeholder="Klubbens namn i Swish"
                                       <?= !$perms['can_edit_profile'] ? 'disabled' : '' ?>>
                            </div>
                        </div>
                        <p class="text-sm text-secondary">
                            Swish-uppgifter används för att ta emot betalningar vid tävlingar som klubben arrangerar.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sidebar -->
        <div class="club-edit-sidebar">
            <!-- Actions -->
            <div class="card mb-lg">
                <div class="card-body">
                    <?php if ($perms['can_edit_profile']): ?>
                    <button type="submit" class="btn btn--primary w-full mb-sm">
                        <i data-lucide="save"></i>
                        Spara ändringar
                    </button>
                    <?php endif; ?>
                    <a href="/club/<?= $id ?>" target="_blank" class="btn btn--secondary w-full mb-sm">
                        <i data-lucide="eye"></i>
                        Visa publik sida
                    </a>
                    <a href="/admin/my-clubs.php" class="btn btn--secondary w-full">
                        <i data-lucide="arrow-left"></i>
                        Tillbaka
                    </a>
                </div>
            </div>

            <!-- Club Info -->
            <div class="card">
                <div class="card-header">
                    <h3>Information</h3>
                </div>
                <div class="card-body">
                    <p class="text-sm text-secondary mb-sm">
                        <strong>Medlemmar:</strong> <?= $riderCount ?>
                    </p>
                    <p class="text-sm text-secondary mb-sm">
                        <strong>Status:</strong>
                        <span class="badge <?= $club['active'] ? 'badge-success' : 'badge-secondary' ?>">
                            <?= $club['active'] ? 'Aktiv' : 'Inaktiv' ?>
                        </span>
                    </p>
                    <?php if (!empty($club['scf_id'])): ?>
                    <p class="text-sm text-secondary">
                        <strong>SCF-ID:</strong> <?= h($club['scf_id']) ?>
                    </p>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>
</form>

<style>
/* Mobile-first CSS */
@keyframes spin { to { transform: rotate(360deg); } }

/* Layout - Mobile first (single column) */
.club-edit-layout {
    display: flex;
    flex-direction: column;
    gap: var(--space-lg);
}

.club-edit-main {
    width: 100%;
}

.club-edit-sidebar {
    width: 100%;
}

/* Form rows - stack on mobile */
.form-row {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}

.form-row > div {
    width: 100%;
}

/* Logo preview responsive */
.logo-preview {
    width: 100%;
    max-width: 150px;
    height: 100px;
}

/* Desktop styles (min-width: 768px) */
@media (min-width: 768px) {
    .club-edit-layout {
        flex-direction: row;
        flex-wrap: wrap;
    }

    .club-edit-main {
        flex: 2;
        min-width: 0;
    }

    .club-edit-sidebar {
        flex: 1;
        min-width: 280px;
        max-width: 350px;
    }

    .form-row {
        flex-direction: row;
    }

    .form-row > div {
        flex: 1;
    }
}
</style>

<?php if ($perms['can_upload_logo']): ?>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const logoInput = document.getElementById('clubLogoInput');
    const logoPreview = document.getElementById('clubLogoPreview');
    const logoLoading = document.getElementById('clubLogoLoading');
    const logoStatus = document.getElementById('clubLogoStatus');
    const urlInput = document.getElementById('logoUrlInput');
    const clubId = <?= intval($id) ?>;

    if (!logoInput) return;

    logoInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            showStatus('Otillaten filtyp', 'error');
            return;
        }

        if (file.size > 2 * 1024 * 1024) {
            showStatus('Max 2MB', 'error');
            return;
        }

        logoLoading.style.display = 'flex';
        showStatus('Laddar upp...', 'info');

        const formData = new FormData();
        formData.append('logo', file);
        formData.append('club_id', clubId);

        try {
            const response = await fetch('/api/update-club-logo.php', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();

            if (result.success) {
                showStatus('Uppladdad!', 'success');
                updatePreview(result.logo_url);
                urlInput.value = result.logo_url;
            } else {
                showStatus(result.error || 'Fel', 'error');
            }
        } catch (error) {
            showStatus('Uppladdning misslyckades', 'error');
        } finally {
            logoLoading.style.display = 'none';
        }
    });

    function updatePreview(src) {
        logoPreview.innerHTML = '<img src="' + src + '" alt="Klubblogotyp" style="max-width: 100%; max-height: 100%; object-fit: contain;">';
        logoPreview.style.border = 'none';
    }

    function showStatus(msg, type) {
        logoStatus.textContent = msg;
        logoStatus.style.color = type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#6b7280';
        if (type === 'success') setTimeout(() => { logoStatus.textContent = ''; }, 3000);
    }
});
</script>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
