<?php
/**
 * TheHUB V1.0 - Min Sida (Profile)
 * Shows user profile, children, registrations, etc.
 */

$currentUser = hub_current_user();

if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();

// Include avatar helper functions
$avatarHelperPath = dirname(dirname(__DIR__)) . '/includes/get-avatar.php';
if (file_exists($avatarHelperPath)) {
    require_once $avatarHelperPath;
}

// Get linked children
$linkedChildren = hub_get_linked_children($currentUser['id']);

// Get admin clubs
$adminClubs = hub_get_admin_clubs($currentUser['id']);

// Get upcoming registrations (if table exists)
$upcomingRegs = [];
try {
    $tableCheck = $pdo->query("SHOW TABLES LIKE 'event_registrations'");
    if ($tableCheck->rowCount() > 0) {
        $regStmt = $pdo->prepare("
            SELECT r.*, e.name as event_name, e.date as event_date, e.location,
                   cls.display_name as class_name
            FROM event_registrations r
            JOIN events e ON r.event_id = e.id
            LEFT JOIN classes cls ON r.class_id = cls.id
            WHERE r.rider_id = ? AND e.date >= CURDATE() AND r.status != 'cancelled'
            ORDER BY e.date ASC
            LIMIT 5
        ");
        $regStmt->execute([$currentUser['id']]);
        $upcomingRegs = $regStmt->fetchAll(PDO::FETCH_ASSOC);
    }
} catch (PDOException $e) {
    $upcomingRegs = [];
}

// Get recent results
$resultStmt = $pdo->prepare("
    SELECT res.*, e.name as event_name, e.date as event_date,
           cls.display_name as class_name
    FROM results res
    JOIN events e ON res.event_id = e.id
    LEFT JOIN classes cls ON res.class_id = cls.id
    WHERE res.cyclist_id = ?
    ORDER BY e.date DESC
    LIMIT 5
");
$resultStmt->execute([$currentUser['id']]);
$recentResults = $resultStmt->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="user" class="page-icon"></i>
        Min Sida
    </h1>
</div>

<!-- Profile Card -->
<div class="profile-card">
    <div class="profile-avatar">
        <?php
        // Check for avatar image
        $avatarUrl = $currentUser['avatar_url'] ?? null;
        $initials = function_exists('get_rider_initials')
            ? get_rider_initials($currentUser)
            : strtoupper(substr($currentUser['firstname'] ?? '', 0, 1) . substr($currentUser['lastname'] ?? '', 0, 1));

        if ($avatarUrl):
        ?>
            <img src="<?= htmlspecialchars($avatarUrl) ?>"
                 alt="Din profilbild"
                 class="profile-avatar-image"
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <span class="profile-avatar-fallback" style="display: none;"><?= htmlspecialchars($initials) ?></span>
        <?php elseif (function_exists('get_rider_avatar')): ?>
            <img src="<?= htmlspecialchars(get_rider_avatar($currentUser, 80)) ?>"
                 alt="Din profilbild"
                 class="profile-avatar-image">
        <?php else: ?>
            <?= htmlspecialchars($initials) ?>
        <?php endif; ?>
    </div>
    <div class="profile-info">
        <h2 class="profile-name"><?= htmlspecialchars($currentUser['firstname'] . ' ' . $currentUser['lastname']) ?></h2>
        <?php if ($currentUser['email']): ?>
            <p class="profile-email"><?= htmlspecialchars($currentUser['email']) ?></p>
        <?php endif; ?>
        <?php if ($currentUser['club_id']): ?>
            <?php
            $clubStmt = $pdo->prepare("SELECT name FROM clubs WHERE id = ?");
            $clubStmt->execute([$currentUser['club_id']]);
            $clubName = $clubStmt->fetchColumn();
            ?>
            <p class="profile-club"><i data-lucide="shield" class="icon-xs align-middle"></i> <?= htmlspecialchars($clubName) ?></p>
        <?php endif; ?>
    </div>
    <a href="/profile/edit" class="btn btn-outline">Redigera profil</a>
</div>

<!-- Quick Links -->
<div class="quick-links">
    <a href="/profile/registrations" class="quick-link">
        <span class="quick-link-icon"><i data-lucide="clipboard-list"></i></span>
        <span class="quick-link-label">Mina anmälningar</span>
        <span class="quick-link-arrow">›</span>
    </a>
    <a href="/rider/<?= $currentUser['id'] ?>" class="quick-link">
        <span class="quick-link-icon"><i data-lucide="flag"></i></span>
        <span class="quick-link-label">Mina resultat</span>
        <span class="quick-link-arrow">›</span>
    </a>
    <a href="/profile/receipts" class="quick-link">
        <span class="quick-link-icon"><i data-lucide="receipt"></i></span>
        <span class="quick-link-label">Kvitton</span>
        <span class="quick-link-arrow">›</span>
    </a>
    <a href="/profile/race-reports" class="quick-link">
        <span class="quick-link-icon"><i data-lucide="file-text"></i></span>
        <span class="quick-link-label">Mina Race Reports</span>
        <span class="quick-link-arrow">›</span>
    </a>
    <a href="/profile/event-ratings" class="quick-link">
        <span class="quick-link-icon"><i data-lucide="star"></i></span>
        <span class="quick-link-label">Betygsatt Events</span>
        <span class="quick-link-arrow">›</span>
    </a>
    <?php if (!empty($linkedChildren)): ?>
        <a href="/profile/children" class="quick-link">
            <span class="quick-link-icon"><i data-lucide="users"></i></span>
            <span class="quick-link-label">Kopplade barn (<?= count($linkedChildren) ?>)</span>
            <span class="quick-link-arrow">›</span>
        </a>
    <?php endif; ?>
    <?php if (!empty($adminClubs)): ?>
        <a href="/profile/club-admin" class="quick-link">
            <span class="quick-link-icon"><i data-lucide="settings"></i></span>
            <span class="quick-link-label">Klubb-admin</span>
            <span class="quick-link-arrow">›</span>
        </a>
    <?php endif; ?>
</div>

<!-- Upcoming Registrations -->
<?php if (!empty($upcomingRegs)): ?>
    <div class="section">
        <div class="section-header">
            <h2>Kommande tävlingar</h2>
            <a href="/profile/registrations" class="section-link">Visa alla</a>
        </div>
        <div class="upcoming-list">
            <?php foreach ($upcomingRegs as $reg): ?>
                <a href="/calendar/<?= $reg['event_id'] ?>" class="upcoming-item">
                    <div class="upcoming-date">
                        <span class="upcoming-day"><?= date('j', strtotime($reg['event_date'])) ?></span>
                        <span class="upcoming-month"><?= hub_month_short($reg['event_date']) ?></span>
                    </div>
                    <div class="upcoming-info">
                        <span class="upcoming-name"><?= htmlspecialchars($reg['event_name']) ?></span>
                        <span class="upcoming-class"><?= htmlspecialchars($reg['class_name'] ?? '') ?></span>
                    </div>
                    <span class="upcoming-status status-<?= $reg['status'] ?>">
                        <?= $reg['status'] === 'confirmed' ? '✓' : '⏳' ?>
                    </span>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
<?php endif; ?>

<!-- Recent Results -->
<?php if (!empty($recentResults)): ?>
    <div class="section">
        <div class="section-header">
            <h2>Senaste resultat</h2>
            <a href="/rider/<?= $currentUser['id'] ?>" class="section-link">Visa alla</a>
        </div>
        <div class="results-list">
            <?php foreach ($recentResults as $result): ?>
                <a href="/results/<?= $result['event_id'] ?>" class="result-item">
                    <div class="result-position">
                        <?php if ($result['position'] == 1): ?>
                            <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                        <?php elseif ($result['position'] == 2): ?>
                            <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                        <?php elseif ($result['position'] == 3): ?>
                            <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                        <?php else: ?>
                            #<?= $result['position'] ?>
                        <?php endif; ?>
                    </div>
                    <div class="result-info">
                        <span class="result-event"><?= htmlspecialchars($result['event_name']) ?></span>
                        <span class="result-class"><?= htmlspecialchars($result['class_name'] ?? '') ?></span>
                    </div>
                    <span class="result-date"><?= date('j M', strtotime($result['event_date'])) ?></span>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
<?php endif; ?>

<!-- Theme Settings - DISABLED: Always light theme -->
<!-- Theme selector removed to prevent issues -->

<!-- Logout -->
<div class="logout-section">
    <a href="/logout" class="btn btn-outline btn-danger">Logga ut</a>
</div>


<!-- Avatar image styles -->
<style>
.profile-avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.profile-avatar-fallback {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}
</style>

<!-- CSS loaded from /assets/css/pages/profile-index.css -->
