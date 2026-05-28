<?php
/**
 * Admin Rider Claims - Review and approve profile merge requests
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/mail.php';
require_admin();

$db = getDB();

$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';
    $claimId = (int)($_POST['claim_id'] ?? 0);

    if ($claimId > 0) {
        $claim = $db->getRow("SELECT * FROM rider_claims WHERE id = ?", [$claimId]);

        if ($claim) {
            if ($action === 'approve') {
                // Approve: Connect email to target profile and send password reset
                try {
                    $targetId = $claim['target_rider_id'];
                    $emailToConnect = $claim['claimant_email'];

                    // Get target rider
                    $target = $db->getRow("SELECT * FROM riders WHERE id = ?", [$targetId]);

                    if (!$target) {
                        throw new Exception("Profilen kunde inte hittas");
                    }

                    if (!empty($target['email'])) {
                        throw new Exception("Profilen har redan en e-postadress kopplad");
                    }

                    // Build updates from claim data
                    $updates = [
                        'email' => $emailToConnect,
                        'updated_at' => date('Y-m-d H:i:s')
                    ];

                    // Add phone if provided in claim
                    if (!empty($claim['phone'])) {
                        $updates['phone'] = $claim['phone'];
                    }

                    // Add social media if provided
                    if (!empty($claim['instagram'])) {
                        $updates['social_instagram'] = $claim['instagram'];
                    }
                    if (!empty($claim['facebook'])) {
                        $updates['social_facebook'] = $claim['facebook'];
                    }

                    // Generate password reset token
                    $token = bin2hex(random_bytes(32));
                    $expires = date('Y-m-d H:i:s', strtotime('+24 hours'));
                    $updates['password_reset_token'] = $token;
                    $updates['password_reset_expires'] = $expires;

                    // Update the rider
                    $db->update('riders', $updates, 'id = ?', [$targetId]);

                    // Update claim status
                    $db->update('rider_claims', [
                        'status' => 'approved',
                        'reviewed_by' => $_SESSION['admin_id'],
                        'reviewed_at' => date('Y-m-d H:i:s'),
                        'admin_notes' => trim($_POST['admin_notes'] ?? '') ?: 'Godkänd'
                    ], 'id = ?', [$claimId]);

                    // Send password reset email
                    $resetLink = 'https://thehub.gravityseries.se/reset-password?token=' . $token;
                    $riderName = trim($target['firstname'] . ' ' . $target['lastname']);
                    $emailSent = hub_send_password_reset_email($emailToConnect, $riderName, $resetLink);

                    $emailStatus = $emailSent ? ' Mail med lösenordslänk skickat!' : ' Kunde inte skicka mail.';
                    $message = "E-post kopplad till {$riderName}!{$emailStatus}";
                    $messageType = 'success';

                    // Log the action
                    error_log("CLAIM APPROVED: Admin {$_SESSION['admin_id']} connected '{$emailToConnect}' to rider {$targetId} ({$riderName})");

                } catch (Exception $e) {
                    $message = 'Fel: ' . $e->getMessage();
                    $messageType = 'error';
                }

            } elseif ($action === 'reject') {
                $adminNotes = trim($_POST['admin_notes'] ?? '');

                $db->update('rider_claims', [
                    'status' => 'rejected',
                    'reviewed_by' => $_SESSION['admin_id'],
                    'reviewed_at' => date('Y-m-d H:i:s'),
                    'admin_notes' => $adminNotes
                ], 'id = ?', [$claimId]);

                $message = 'Förfrågan avvisad';
                $messageType = 'info';

            } elseif ($action === 'delete') {
                $db->delete('rider_claims', 'id = ?', [$claimId]);
                $message = 'Förfrågan borttagen';
                $messageType = 'info';
            }
        }
    }
}

// Get pending claims
$pendingClaims = $db->getAll("
    SELECT
        rc.*,
        r_target.firstname as target_firstname,
        r_target.lastname as target_lastname,
        r_target.email as target_email,
        r_target.birth_year as target_birth_year,
        r_target.license_number as target_license,
        c.name as target_club,
        (SELECT COUNT(*) FROM results WHERE cyclist_id = rc.target_rider_id) as target_results,
        -- Claimant info (if claimant_rider_id exists)
        r_claimant.firstname as claimant_firstname,
        r_claimant.lastname as claimant_lastname,
        r_claimant.email as claimant_email_actual,
        r_claimant.birth_year as claimant_birth_year,
        r_claimant.license_number as claimant_license,
        (SELECT COUNT(*) FROM results WHERE cyclist_id = rc.claimant_rider_id) as claimant_results
    FROM rider_claims rc
    JOIN riders r_target ON rc.target_rider_id = r_target.id
    LEFT JOIN riders r_claimant ON rc.claimant_rider_id = r_claimant.id
    LEFT JOIN clubs c ON r_target.club_id = c.id
    WHERE rc.status = 'pending'
    ORDER BY rc.created_at DESC
");

// Get recent resolved claims
$resolvedClaims = $db->getAll("
    SELECT
        rc.*,
        r_claimant.firstname as claimant_firstname,
        r_claimant.lastname as claimant_lastname,
        r_target.firstname as target_firstname,
        r_target.lastname as target_lastname,
        au.full_name as reviewer_name
    FROM rider_claims rc
    LEFT JOIN riders r_claimant ON rc.claimant_rider_id = r_claimant.id
    LEFT JOIN riders r_target ON rc.target_rider_id = r_target.id
    LEFT JOIN admin_users au ON rc.reviewed_by = au.id
    WHERE rc.status != 'pending'
    ORDER BY rc.reviewed_at DESC
    LIMIT 20
");

$page_title = 'Profilförfrågningar';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Profilförfrågningar']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'danger' : 'info') ?> mb-lg">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Pending Claims -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="user-check"></i> Väntande förfrågningar (<?= count($pendingClaims) ?>)</h3>
    </div>
    <div class="card-body">
        <?php if (empty($pendingClaims)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Inga väntande förfrågningar!
        </div>
        <?php else: ?>

        <?php foreach ($pendingClaims as $claim): ?>
        <div class="card mb-md" style="border: 2px solid var(--color-warning);">
            <div class="card-body">
                <?php if ($claim['claimant_rider_id']): ?>
                <!-- TWO PROFILE MERGE MODE -->
                <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: var(--space-lg); align-items: start;">

                    <!-- Claimant (new profile with email) -->
                    <div>
                        <h4 class="text-secondary mb-sm">Ny profil (vill behålla)</h4>
                        <p class="mb-xs">
                            <strong>
                                <a href="/admin/rider-edit/<?= $claim['claimant_rider_id'] ?>" target="_blank">
                                    <?= h(($claim['claimant_firstname'] ?? '') . ' ' . ($claim['claimant_lastname'] ?? '')) ?>
                                </a>
                            </strong>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="mail" style="width: 14px;"></i>
                            <?= h($claim['claimant_email_actual'] ?? $claim['claimant_email'] ?? 'Ingen e-post') ?>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="calendar" style="width: 14px;"></i>
                            Född: <?= ($claim['claimant_birth_year'] ?? '') ?: '-' ?>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="trophy" style="width: 14px;"></i>
                            <?= $claim['claimant_results'] ?? 0 ?> resultat
                        </p>
                        <p class="text-secondary">
                            <i data-lucide="id-card" style="width: 14px;"></i>
                            <?= h(($claim['claimant_license'] ?? '') ?: 'Inget UCI') ?>
                        </p>
                    </div>

                    <!-- Arrow -->
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: var(--space-xl);">
                        <i data-lucide="arrow-right" style="width: 32px; height: 32px; color: var(--color-warning);"></i>
                        <span class="text-secondary" style="font-size: 12px;">slå ihop med</span>
                    </div>

                    <!-- Target (historical profile) -->
                    <div>
                        <h4 class="text-secondary mb-sm">Historisk profil (ta över data)</h4>
                        <p class="mb-xs">
                            <strong>
                                <a href="/admin/rider-edit/<?= $claim['target_rider_id'] ?>" target="_blank">
                                    <?= h($claim['target_firstname'] . ' ' . $claim['target_lastname']) ?>
                                </a>
                            </strong>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="mail" style="width: 14px;"></i>
                            <?= h($claim['target_email'] ?: 'Ingen e-post') ?>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="calendar" style="width: 14px;"></i>
                            Född: <?= $claim['target_birth_year'] ?: '-' ?>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="trophy" style="width: 14px;"></i>
                            <strong><?= $claim['target_results'] ?> resultat</strong>
                        </p>
                        <p class="text-secondary">
                            <i data-lucide="id-card" style="width: 14px;"></i>
                            <?= h($claim['target_license'] ?: 'Inget UCI') ?>
                        </p>
                    </div>
                </div>
                <?php else: ?>
                <!-- EMAIL CLAIM MODE (no existing profile, just claiming historical one) -->
                <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: var(--space-lg); align-items: start;">

                    <!-- Request info -->
                    <div>
                        <h4 class="text-secondary mb-sm">Förfrågan</h4>
                        <p class="mb-xs">
                            <strong><?= h($claim['claimant_name'] ?: 'Okänt namn') ?></strong>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="mail" style="width: 14px;"></i>
                            <?= h($claim['claimant_email']) ?>
                        </p>
                        <?php if (!empty($claim['phone'])): ?>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="phone" style="width: 14px;"></i>
                            <?= h($claim['phone']) ?>
                        </p>
                        <?php endif; ?>
                        <?php if (!empty($claim['instagram'])): ?>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="instagram" style="width: 14px;"></i>
                            <?= h($claim['instagram']) ?>
                        </p>
                        <?php endif; ?>
                    </div>

                    <!-- Arrow -->
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: var(--space-xl);">
                        <i data-lucide="arrow-right" style="width: 32px; height: 32px; color: var(--color-success);"></i>
                        <span class="text-secondary" style="font-size: 12px;">vill koppla till</span>
                    </div>

                    <!-- Target (profile to claim) -->
                    <div>
                        <h4 class="text-secondary mb-sm">Profil att aktivera</h4>
                        <p class="mb-xs">
                            <strong>
                                <a href="/admin/rider-edit/<?= $claim['target_rider_id'] ?>" target="_blank">
                                    <?= h($claim['target_firstname'] . ' ' . $claim['target_lastname']) ?>
                                </a>
                            </strong>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="mail" style="width: 14px;"></i>
                            <?= h($claim['target_email'] ?: 'Ingen e-post (läggs till)') ?>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="calendar" style="width: 14px;"></i>
                            Född: <?= $claim['target_birth_year'] ?: '-' ?>
                        </p>
                        <p class="text-secondary mb-xs">
                            <i data-lucide="trophy" style="width: 14px;"></i>
                            <strong><?= $claim['target_results'] ?> resultat</strong>
                        </p>
                        <p class="text-secondary">
                            <i data-lucide="id-card" style="width: 14px;"></i>
                            <?= h($claim['target_license'] ?: 'Inget UCI') ?>
                        </p>
                    </div>
                </div>
                <?php endif; ?>

                <?php if ($claim['reason']): ?>
                <div class="mt-md" style="background: var(--color-bg-secondary); padding: var(--space-sm); border-radius: var(--radius-sm);">
                    <strong>Användarens kommentar:</strong><br>
                    <?= nl2br(h($claim['reason'])) ?>
                </div>
                <?php endif; ?>

                <div class="mt-md" style="display: flex; gap: var(--space-sm); justify-content: flex-end; border-top: 1px solid var(--color-border); padding-top: var(--space-md);">
                    <span class="text-secondary" style="flex: 1;">
                        Skapad: <?= date('Y-m-d H:i', strtotime($claim['created_at'])) ?>
                    </span>

                    <!-- Reject form -->
                    <form method="POST" style="display: inline;" onsubmit="return confirm('Avvisa denna förfrågan?');">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="reject">
                        <input type="hidden" name="claim_id" value="<?= $claim['id'] ?>">
                        <button type="submit" class="btn btn-secondary">
                            <i data-lucide="x"></i> Avvisa
                        </button>
                    </form>

                    <!-- Approve form -->
                    <?php if ($claim['claimant_rider_id']): ?>
                    <form method="POST" style="display: inline;" onsubmit="return confirm('Godkänn och slå ihop profilerna?\n\nDetta kommer:\n- Flytta resultat från ny profil till historisk profil\n- Kopiera e-post/kontaktinfo till historisk profil\n- Ta bort den nya profilen\n\nDetta kan inte ångras!');">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="approve">
                        <input type="hidden" name="claim_id" value="<?= $claim['id'] ?>">
                        <button type="submit" class="btn btn-primary">
                            <i data-lucide="check"></i> Godkänn & Slå ihop
                        </button>
                    </form>
                    <?php else: ?>
                    <form method="POST" style="display: inline;" onsubmit="return confirm('Godkänn profilkoppling?\n\nDetta kommer:\n- Koppla e-postadressen till profilen\n- Skicka lösenordslänk till användaren\n- Användaren kan sedan logga in');">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="approve">
                        <input type="hidden" name="claim_id" value="<?= $claim['id'] ?>">
                        <button type="submit" class="btn btn-primary">
                            <i data-lucide="check"></i> Godkänn & Aktivera
                        </button>
                    </form>
                    <?php endif; ?>
                </div>
            </div>
        </div>
        <?php endforeach; ?>

        <?php endif; ?>
    </div>
</div>

<!-- Recent resolved -->
<?php if (!empty($resolvedClaims)): ?>
<div class="card">
    <div class="card-header">
        <h3>Senaste hanterade</h3>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Datum</th>
                        <th>Från</th>
                        <th>Till</th>
                        <th>Status</th>
                        <th>Hanterad av</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($resolvedClaims as $claim): ?>
                    <tr>
                        <td><?= date('Y-m-d', strtotime($claim['reviewed_at'])) ?></td>
                        <td><?= h(($claim['claimant_firstname'] ?? '[Raderad]') . ' ' . ($claim['claimant_lastname'] ?? '')) ?></td>
                        <td><?= h(($claim['target_firstname'] ?? '[Raderad]') . ' ' . ($claim['target_lastname'] ?? '')) ?></td>
                        <td>
                            <?php if ($claim['status'] === 'approved'): ?>
                                <span class="badge badge-success">Godkänd</span>
                            <?php else: ?>
                                <span class="badge badge-secondary">Avvisad</span>
                            <?php endif; ?>
                        </td>
                        <td><?= h($claim['reviewer_name'] ?? '-') ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
