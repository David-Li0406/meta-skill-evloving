<?php
/**
 * TheHUB V1.0 - Edit Profile with Social Profiles and Avatar Upload
 */

$currentUser = hub_current_user();
if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();
$message = '';
$error = '';

// Include social profile sanitizer
$rebuildPath = dirname(dirname(__DIR__)) . '/includes/rebuild-rider-stats.php';
if (file_exists($rebuildPath)) {
    require_once $rebuildPath;
}

// Include avatar helper functions
$avatarHelperPath = dirname(dirname(__DIR__)) . '/includes/get-avatar.php';
if (file_exists($avatarHelperPath)) {
    require_once $avatarHelperPath;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $firstName = trim($_POST['firstname'] ?? '');
    $lastName = trim($_POST['lastname'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $clubId = intval($_POST['club_id'] ?? 0) ?: null;

    // New profile fields
    $birthYear = intval($_POST['birth_year'] ?? 0) ?: null;
    $phone = trim($_POST['phone'] ?? '');
    $uciId = trim($_POST['uci_id'] ?? '');
    $iceName = trim($_POST['ice_name'] ?? '');
    $icePhone = trim($_POST['ice_phone'] ?? '');

    // Address fields for purchases/receipts
    $address = trim($_POST['address'] ?? '');
    $postalCode = trim($_POST['postal_code'] ?? '');
    $postalCity = trim($_POST['postal_city'] ?? '');

    // Social profiles
    $socialInstagram = trim($_POST['social_instagram'] ?? '');
    $socialStrava = trim($_POST['social_strava'] ?? '');
    $socialFacebook = trim($_POST['social_facebook'] ?? '');
    $socialYoutube = trim($_POST['social_youtube'] ?? '');
    $socialTiktok = trim($_POST['social_tiktok'] ?? '');

    // Sanitize social handles if function exists
    if (function_exists('sanitizeSocialHandle')) {
        $socialInstagram = sanitizeSocialHandle($socialInstagram, 'instagram');
        $socialStrava = sanitizeSocialHandle($socialStrava, 'strava');
        $socialFacebook = sanitizeSocialHandle($socialFacebook, 'facebook');
        $socialYoutube = sanitizeSocialHandle($socialYoutube, 'youtube');
        $socialTiktok = sanitizeSocialHandle($socialTiktok, 'tiktok');
    }

    if (empty($firstName) || empty($lastName)) {
        $error = 'Förnamn och efternamn krävs.';
    } else {
        try {
            // Build dynamic update query based on which columns exist
            // Start with core fields that always exist
            $updateFields = [
                'firstname = ?', 'lastname = ?', 'email = ?', 'club_id = ?'
            ];
            $updateValues = [
                $firstName, $lastName, $email, $clubId
            ];

            // Check which optional columns exist
            $existingColumns = [];
            $colStmt = $pdo->query("SHOW COLUMNS FROM riders");
            while ($col = $colStmt->fetch(PDO::FETCH_ASSOC)) {
                $existingColumns[] = $col['Field'];
            }

            // Add social columns if they exist
            $socialColumns = [
                'social_instagram' => $socialInstagram ?: null,
                'social_strava' => $socialStrava ?: null,
                'social_facebook' => $socialFacebook ?: null,
                'social_youtube' => $socialYoutube ?: null,
                'social_tiktok' => $socialTiktok ?: null
            ];
            foreach ($socialColumns as $colName => $colValue) {
                if (in_array($colName, $existingColumns)) {
                    $updateFields[] = "$colName = ?";
                    $updateValues[] = $colValue;
                }
            }

            // Add new profile fields if they exist
            if (in_array('phone', $existingColumns)) {
                $updateFields[] = 'birth_year = ?';
                $updateFields[] = 'phone = ?';
                $updateValues[] = $birthYear;
                $updateValues[] = $phone ?: null;
            }
            if (in_array('ice_name', $existingColumns)) {
                $updateFields[] = 'ice_name = ?';
                $updateValues[] = $iceName ?: null;
            }
            if (in_array('ice_phone', $existingColumns)) {
                $updateFields[] = 'ice_phone = ?';
                $updateValues[] = $icePhone ?: null;
            }

            // Address fields for purchases/receipts
            if (in_array('address', $existingColumns)) {
                $updateFields[] = 'address = ?';
                $updateValues[] = $address ?: null;
            }
            if (in_array('postal_code', $existingColumns)) {
                $updateFields[] = 'postal_code = ?';
                $updateValues[] = $postalCode ?: null;
            }
            if (in_array('postal_city', $existingColumns)) {
                $updateFields[] = 'postal_city = ?';
                $updateValues[] = $postalCity ?: null;
            }

            // UCI ID - only allow setting if not already set (prevent overwrites)
            if (in_array('uci_id', $existingColumns) && empty($currentUser['uci_id']) && !empty($uciId)) {
                $updateFields[] = 'uci_id = ?';
                $updateValues[] = $uciId;
            }

            $updateValues[] = $currentUser['id'];

            $stmt = $pdo->prepare("
                UPDATE riders
                SET " . implode(', ', $updateFields) . "
                WHERE id = ?
            ");
            $stmt->execute($updateValues);
            $message = 'Profilen har uppdaterats!';

            // Refresh user data
            $currentUser = hub_get_rider_by_id($currentUser['id']);
        } catch (PDOException $e) {
            $error = 'Kunde inte uppdatera profilen: ' . $e->getMessage();
            error_log("Profile update error: " . $e->getMessage());
        }
    }
}

// Get active clubs for dropdown
$clubs = $pdo->query("SELECT id, name FROM clubs WHERE active = 1 ORDER BY name")->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="page-header">
    <nav class="breadcrumb">
        <a href="/profile">Min Sida</a>
        <span class="breadcrumb-sep">›</span>
        <span>Redigera profil</span>
    </nav>
    <h1 class="page-title">Redigera profil</h1>
</div>

<?php if ($message): ?>
    <div class="alert alert-success"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>

<?php if ($error): ?>
    <div class="alert alert-error"><?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<!-- Avatar Upload Section -->
<div class="card avatar-section">
    <div class="card-body">
        <h2>Profilbild</h2>
        <p class="form-help">Ladda upp en profilbild som visas på din profil och i resultatlistor.</p>

        <div class="avatar-upload-wrapper">
            <?php
            // Get current avatar URL
            $avatarUrl = '';
            if (function_exists('get_rider_avatar')) {
                $avatarUrl = get_rider_avatar($currentUser, 200);
            } elseif (!empty($currentUser['avatar_url'])) {
                $avatarUrl = $currentUser['avatar_url'];
            }

            $initials = '';
            if (function_exists('get_rider_initials')) {
                $initials = get_rider_initials($currentUser);
            } else {
                $initials = strtoupper(
                    substr($currentUser['firstname'] ?? '', 0, 1) .
                    substr($currentUser['lastname'] ?? '', 0, 1)
                );
            }
            ?>

            <div class="avatar-upload-container" id="avatarContainer">
                <div class="avatar-preview" id="avatarPreview" style="width: 200px; height: 200px;">
                    <?php if (!empty($currentUser['avatar_url'])): ?>
                        <img src="<?= htmlspecialchars($currentUser['avatar_url']) ?>" alt="Din profilbild" class="avatar-image" id="avatarImage">
                    <?php elseif ($avatarUrl): ?>
                        <img src="<?= htmlspecialchars($avatarUrl) ?>" alt="Din profilbild" class="avatar-image" id="avatarImage">
                    <?php else: ?>
                        <div class="avatar-fallback" id="avatarFallback">
                            <span class="avatar-initials"><?= htmlspecialchars($initials) ?></span>
                        </div>
                    <?php endif; ?>
                </div>

                <div class="avatar-upload-overlay" id="avatarOverlay">
                    <i data-lucide="camera"></i>
                </div>

                <div class="avatar-loading" id="avatarLoading" style="display: none;"></div>

                <input type="file"
                       id="avatarInput"
                       class="avatar-upload-input"
                       accept="image/jpeg,image/png,image/gif,image/webp"
                       aria-label="Välj profilbild">
            </div>

            <div class="avatar-upload-info">
                <p class="text-secondary text-sm">Klicka för att välja en bild</p>
                <p class="text-secondary text-xs">Max 2MB. JPG, PNG, GIF eller WebP.</p>
            </div>

            <div class="avatar-upload-status" id="avatarStatus" style="display: none;"></div>
        </div>
    </div>
</div>

<form method="POST" class="profile-form">
    <div class="form-section">
        <h2>Personuppgifter</h2>
        <p class="form-help">Denna information används för att förifylla anmälningsformulär.</p>

        <div class="form-row">
            <div class="form-group">
                <label for="firstname">Förnamn *</label>
                <input type="text" id="firstname" name="firstname"
                       value="<?= htmlspecialchars($currentUser['firstname'] ?? '') ?>" required>
            </div>
            <div class="form-group">
                <label for="lastname">Efternamn *</label>
                <input type="text" id="lastname" name="lastname"
                       value="<?= htmlspecialchars($currentUser['lastname'] ?? '') ?>" required>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="email">E-post</label>
                <input type="email" id="email" name="email"
                       value="<?= htmlspecialchars($currentUser['email'] ?? '') ?>"
                       placeholder="din@email.se">
            </div>
            <div class="form-group">
                <label for="phone">Telefon</label>
                <input type="tel" id="phone" name="phone"
                       value="<?= htmlspecialchars($currentUser['phone'] ?? '') ?>"
                       placeholder="07X XXX XX XX">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="birth_year">Födelseår</label>
                <input type="number" id="birth_year" name="birth_year"
                       value="<?= htmlspecialchars($currentUser['birth_year'] ?? '') ?>"
                       min="1920" max="<?= date('Y') ?>"
                       placeholder="ÅÅÅÅ">
            </div>
            <div class="form-group">
                <label for="uci_id">UCI ID</label>
                <?php if (!empty($currentUser['uci_id'])): ?>
                    <input type="text" id="uci_id" name="uci_id"
                           value="<?= htmlspecialchars($currentUser['uci_id']) ?>"
                           readonly disabled
                           class="input-disabled">
                    <small class="form-help">UCI ID kan inte ändras efter att det sparats.</small>
                <?php else: ?>
                    <input type="text" id="uci_id" name="uci_id"
                           value=""
                           placeholder="SWE19901231">
                    <small class="form-help">Fyll i ditt UCI ID om du har ett.</small>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <div class="form-section">
        <h2>Klubb</h2>

        <div class="form-group">
            <label for="club_id">Cykelklubb</label>
            <?php if (!empty($currentUser['club_id'])): ?>
            <?php
                $currentClubName = '';
                foreach ($clubs as $club) {
                    if ($club['id'] == $currentUser['club_id']) {
                        $currentClubName = $club['name'];
                        break;
                    }
                }
            ?>
            <input type="text" value="<?= htmlspecialchars($currentClubName) ?>" readonly disabled class="input-disabled">
            <input type="hidden" name="club_id" value="<?= $currentUser['club_id'] ?>">
            <small class="form-help">Klubb kan inte ändras. Kontakta admin vid behov.</small>
            <?php else: ?>
            <select id="club_id" name="club_id">
                <option value="">Ingen klubb</option>
                <?php foreach ($clubs as $club): ?>
                    <option value="<?= $club['id'] ?>">
                        <?= htmlspecialchars($club['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
            <?php endif; ?>
        </div>
    </div>

    <div class="form-section">
        <h2>Nödkontakt (ICE)</h2>
        <p class="form-help">In Case of Emergency - kontaktperson vid olycka.</p>

        <div class="form-row">
            <div class="form-group">
                <label for="ice_name">Kontaktperson</label>
                <input type="text" id="ice_name" name="ice_name"
                       value="<?= htmlspecialchars($currentUser['ice_name'] ?? '') ?>"
                       placeholder="Namn på anhörig">
            </div>
            <div class="form-group">
                <label for="ice_phone">Telefon (ICE)</label>
                <input type="tel" id="ice_phone" name="ice_phone"
                       value="<?= htmlspecialchars($currentUser['ice_phone'] ?? '') ?>"
                       placeholder="07X XXX XX XX">
            </div>
        </div>
    </div>

    <div class="form-section">
        <h2>Leveransadress</h2>
        <p class="form-help">Används vid köp för leverans och kvitton. Sparas för framtida köp.</p>

        <div class="form-group">
            <label for="address">Adress</label>
            <input type="text" id="address" name="address"
                   value="<?= htmlspecialchars($currentUser['address'] ?? '') ?>"
                   placeholder="Gatuadress 123">
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="postal_code">Postnummer</label>
                <input type="text" id="postal_code" name="postal_code"
                       value="<?= htmlspecialchars($currentUser['postal_code'] ?? '') ?>"
                       placeholder="123 45"
                       pattern="[0-9\s]{5,6}"
                       maxlength="6">
            </div>
            <div class="form-group">
                <label for="postal_city">Postort</label>
                <input type="text" id="postal_city" name="postal_city"
                       value="<?= htmlspecialchars($currentUser['postal_city'] ?? '') ?>"
                       placeholder="Stockholm">
            </div>
        </div>
    </div>

    <div class="form-section">
        <h2>Sociala profiler</h2>
        <p class="form-help">Länka dina sociala profiler så att andra kan hitta dig.</p>

        <div class="form-group">
            <label for="social_instagram">
                <span class="social-icon instagram">📷</span> Instagram
            </label>
            <input type="text" id="social_instagram" name="social_instagram"
                   value="<?= htmlspecialchars($currentUser['social_instagram'] ?? '') ?>"
                   placeholder="användarnamn (utan @)">
        </div>

        <div class="form-group">
            <label for="social_strava">
                <i data-lucide="bike" class="social-icon strava"></i> Strava
            </label>
            <input type="text" id="social_strava" name="social_strava"
                   value="<?= htmlspecialchars($currentUser['social_strava'] ?? '') ?>"
                   placeholder="athlete ID eller profil-URL">
        </div>

        <div class="form-group">
            <label for="social_facebook">
                <i data-lucide="facebook" class="social-icon facebook"></i> Facebook
            </label>
            <input type="text" id="social_facebook" name="social_facebook"
                   value="<?= htmlspecialchars($currentUser['social_facebook'] ?? '') ?>"
                   placeholder="profil-URL eller användarnamn">
        </div>

        <div class="form-group">
            <label for="social_youtube">
                <span class="social-icon youtube">🎬</span> YouTube
            </label>
            <input type="text" id="social_youtube" name="social_youtube"
                   value="<?= htmlspecialchars($currentUser['social_youtube'] ?? '') ?>"
                   placeholder="@kanal eller kanal-ID">
        </div>

        <div class="form-group">
            <label for="social_tiktok">
                <span class="social-icon tiktok">🎵</span> TikTok
            </label>
            <input type="text" id="social_tiktok" name="social_tiktok"
                   value="<?= htmlspecialchars($currentUser['social_tiktok'] ?? '') ?>"
                   placeholder="användarnamn (utan @)">
        </div>
    </div>

    <div class="form-actions">
        <button type="submit" class="btn btn--primary">Spara ändringar</button>
        <a href="/profile" class="btn btn-outline">Avbryt</a>
    </div>
</form>

<!-- Avatar Upload Styles -->
<style>
.avatar-section {
    margin-bottom: var(--space-lg);
}

.avatar-upload-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-lg) 0;
}

.avatar-upload-container {
    position: relative;
    cursor: pointer;
}

.avatar-preview {
    border-radius: 50%;
    overflow: hidden;
    background: var(--color-accent, #61CE70);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.avatar-upload-container:hover .avatar-preview {
    transform: scale(1.02);
    box-shadow: var(--shadow-lg);
}

.avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-accent, #61CE70);
    color: #ffffff;
}

.avatar-initials {
    font-size: 4rem;
    font-weight: 700;
    text-transform: uppercase;
}

.avatar-upload-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.avatar-upload-container:hover .avatar-upload-overlay {
    opacity: 1;
}

.avatar-upload-overlay i,
.avatar-upload-overlay svg {
    color: #ffffff;
    width: 48px;
    height: 48px;
}

.avatar-upload-input {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    border-radius: 50%;
}

.avatar-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
}

.avatar-loading::after {
    content: '';
    width: 48px;
    height: 48px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: avatar-spin 0.8s linear infinite;
}

@keyframes avatar-spin {
    to { transform: rotate(360deg); }
}

.avatar-upload-info {
    text-align: center;
}

.avatar-upload-status {
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-sm);
    text-align: center;
    max-width: 300px;
}

.avatar-upload-status.success {
    background: rgba(97, 206, 112, 0.1);
    color: var(--color-success, #61CE70);
    border: 1px solid var(--color-success, #61CE70);
}

.avatar-upload-status.error {
    background: rgba(239, 68, 68, 0.1);
    color: var(--color-danger, #ef4444);
    border: 1px solid var(--color-danger, #ef4444);
}

/* Responsive */
@media (min-width: 768px) {
    .avatar-upload-wrapper {
        flex-direction: row;
        justify-content: flex-start;
        gap: var(--space-xl);
    }

    .avatar-upload-info {
        text-align: left;
    }
}

/* Form row for side-by-side inputs */
.form-row {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-md);
}

@media (min-width: 768px) {
    .form-row {
        grid-template-columns: 1fr 1fr;
    }
}

/* Disabled input styling */
.input-disabled,
input:disabled {
    background: var(--color-bg-sunken, #f5f5f5);
    color: var(--color-text-secondary, #6b7280);
    cursor: not-allowed;
    opacity: 0.7;
}

/* Form section spacing */
.form-section {
    margin-bottom: var(--space-xl);
    padding-bottom: var(--space-lg);
    border-bottom: 1px solid var(--color-border, #e5e7eb);
}

.form-section:last-of-type {
    border-bottom: none;
}

.form-section h2 {
    margin-bottom: var(--space-sm);
    font-size: 1.125rem;
}

.form-help {
    color: var(--color-text-secondary, #6b7280);
    font-size: 0.875rem;
    margin-bottom: var(--space-md);
}

.form-group small.form-help {
    margin-top: var(--space-xs);
    margin-bottom: 0;
    display: block;
}
</style>

<!-- Avatar Upload JavaScript -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const avatarInput = document.getElementById('avatarInput');
    const avatarPreview = document.getElementById('avatarPreview');
    const avatarLoading = document.getElementById('avatarLoading');
    const avatarStatus = document.getElementById('avatarStatus');

    if (!avatarInput) return;

    avatarInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            showStatus('Otillåten filtyp. Välj JPG, PNG, GIF eller WebP.', 'error');
            return;
        }

        // Validate file size (2MB max)
        const maxSize = 2 * 1024 * 1024;
        if (file.size > maxSize) {
            showStatus('Filen är för stor. Max 2MB tillåten.', 'error');
            return;
        }

        // Show preview immediately
        const reader = new FileReader();
        reader.onload = function(e) {
            showPreviewImage(e.target.result);
        };
        reader.readAsDataURL(file);

        // Show loading state
        avatarLoading.style.display = 'flex';
        hideStatus();

        // Upload to server
        const formData = new FormData();
        formData.append('avatar', file);

        try {
            const response = await fetch('/api/update-avatar.php', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                showStatus('Profilbilden har uppdaterats!', 'success');
                // Update the preview with the ImgBB URL
                if (result.avatar_url) {
                    showPreviewImage(result.avatar_url);
                }
            } else {
                showStatus(result.error || 'Något gick fel', 'error');
            }
        } catch (error) {
            console.error('Avatar upload error:', error);
            showStatus('Kunde inte ladda upp bilden. Försök igen.', 'error');
        } finally {
            avatarLoading.style.display = 'none';
        }
    });

    function showPreviewImage(src) {
        // Remove existing content
        avatarPreview.innerHTML = '';

        // Create and add new image
        const img = document.createElement('img');
        img.src = src;
        img.alt = 'Din profilbild';
        img.className = 'avatar-image';
        img.id = 'avatarImage';
        avatarPreview.appendChild(img);
    }

    function showStatus(message, type) {
        avatarStatus.textContent = message;
        avatarStatus.className = 'avatar-upload-status ' + type;
        avatarStatus.style.display = 'block';

        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(hideStatus, 5000);
        }
    }

    function hideStatus() {
        avatarStatus.style.display = 'none';
    }

    // Reinitialize Lucide icons for the camera icon
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
</script>

<!-- CSS loaded from /assets/css/pages/profile-edit.css -->
