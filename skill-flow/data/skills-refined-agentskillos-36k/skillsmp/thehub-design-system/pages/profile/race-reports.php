<?php
/**
 * TheHUB V1.0 - Mina Race Reports
 * Rider can create, edit, and manage their race reports
 */

$currentUser = hub_current_user();

if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();

// Include the race report manager
require_once HUB_ROOT . '/includes/RaceReportManager.php';
$reportManager = new RaceReportManager($pdo);

// Handle form submissions
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'create_report') {
        $title = trim($_POST['title'] ?? '');
        $content = trim($_POST['content'] ?? '');
        $eventId = !empty($_POST['event_id']) ? (int)$_POST['event_id'] : null;
        $featuredImage = trim($_POST['featured_image'] ?? '');
        $youtubeUrl = trim($_POST['youtube_url'] ?? '');
        $instagramUrl = trim($_POST['instagram_url'] ?? '');
        $tags = array_filter(array_map('trim', explode(',', $_POST['tags'] ?? '')));

        if (empty($title)) {
            $error = 'Titel krävs';
        } elseif (empty($content) && empty($youtubeUrl) && empty($instagramUrl)) {
            $error = 'Lägg till innehåll, en YouTube-länk eller Instagram-länk';
        } else {
            // Check if user is admin (not a regular rider)
            $isAdminUser = !empty($currentUser['is_admin']) && empty($_SESSION['rider_id']);

            $reportData = [
                'event_id' => $eventId,
                'title' => $title,
                'content' => $content,
                'featured_image' => $featuredImage ?: null,
                'youtube_url' => $youtubeUrl ?: null,
                'instagram_url' => $instagramUrl ?: null,
                'status' => $isAdminUser ? 'published' : 'draft'
            ];

            if ($isAdminUser) {
                // Admin user - use admin_user_id, no rider_id
                $reportData['admin_user_id'] = $_SESSION['admin_id'] ?? $currentUser['id'];
                $reportData['rider_id'] = null;
            } else {
                // Regular rider
                $reportData['rider_id'] = $currentUser['id'];
            }

            $reportId = $reportManager->createReport($reportData, $tags);

            if ($reportId) {
                if ($isAdminUser) {
                    $message = 'Nyhet publicerad!';
                } else {
                    $message = 'Race report skapad! Den granskas av admin innan publicering.';
                }
            } else {
                $error = 'Kunde inte skapa race report.';
            }
        }
    } elseif ($action === 'update_report') {
        $reportId = (int)$_POST['report_id'];
        $title = trim($_POST['title'] ?? '');
        $content = trim($_POST['content'] ?? '');
        $eventId = !empty($_POST['event_id']) ? (int)$_POST['event_id'] : null;
        $featuredImage = trim($_POST['featured_image'] ?? '');

        $report = $reportManager->getReport($reportId, false);

        // Check permission - rider owns post OR admin owns post OR admin's linked rider owns post
        $isAdminUser = !empty($currentUser['is_admin']) && empty($_SESSION['rider_id']);
        $adminId = $_SESSION['admin_id'] ?? $currentUser['id'];

        // Find linked rider for admin
        $updateLinkedRiderId = null;
        if ($isAdminUser && !empty($currentUser['email'])) {
            try {
                $stmt = $pdo->prepare("SELECT id FROM riders WHERE email = ? LIMIT 1");
                $stmt->execute([$currentUser['email']]);
                $lr = $stmt->fetch(PDO::FETCH_ASSOC);
                if ($lr) $updateLinkedRiderId = $lr['id'];
            } catch (Exception $e) {}
        }

        $canEdit = $report && (
            ($report['rider_id'] && $report['rider_id'] == $currentUser['id']) ||
            ($report['admin_user_id'] && $report['admin_user_id'] == $adminId) ||
            ($isAdminUser && $updateLinkedRiderId && $report['rider_id'] == $updateLinkedRiderId)
        );

        if (!$canEdit) {
            $error = 'Du har inte behörighet att redigera denna report.';
        } else {
            $updateData = [
                'title' => $title,
                'content' => $content,
                'event_id' => $eventId,
                'featured_image' => $featuredImage ?: null
            ];

            // Rider posts go back to draft after editing, admin posts stay published
            if (!$isAdminUser && $report['status'] === 'published') {
                $updateData['status'] = 'draft';
            }

            $result = $reportManager->updateReport($reportId, $updateData);
            if ($result) {
                if (!$isAdminUser && $report['status'] === 'published') {
                    $message = 'Race report uppdaterad! Den måste godkännas igen innan publicering.';
                } else {
                    $message = 'Race report uppdaterad!';
                }
            } else {
                $error = 'Kunde inte uppdatera.';
            }
        }
    } elseif ($action === 'delete_report') {
        $reportId = (int)$_POST['report_id'];

        $report = $reportManager->getReport($reportId, false);

        // Check permission - rider owns post OR admin owns post OR admin's linked rider owns post
        $isAdminUser = !empty($currentUser['is_admin']) && empty($_SESSION['rider_id']);
        $adminId = $_SESSION['admin_id'] ?? $currentUser['id'];

        // Find linked rider for admin
        $deleteLinkedRiderId = null;
        if ($isAdminUser && !empty($currentUser['email'])) {
            try {
                $stmt = $pdo->prepare("SELECT id FROM riders WHERE email = ? LIMIT 1");
                $stmt->execute([$currentUser['email']]);
                $lr = $stmt->fetch(PDO::FETCH_ASSOC);
                if ($lr) $deleteLinkedRiderId = $lr['id'];
            } catch (Exception $e) {}
        }

        $canDelete = $report && (
            ($report['rider_id'] && $report['rider_id'] == $currentUser['id']) ||
            ($report['admin_user_id'] && $report['admin_user_id'] == $adminId) ||
            ($isAdminUser && $deleteLinkedRiderId && $report['rider_id'] == $deleteLinkedRiderId)
        );

        if (!$canDelete) {
            $error = 'Du har inte behörighet att ta bort denna report.';
        } elseif (!$isAdminUser && $report['status'] === 'published') {
            $error = 'Publicerade reports kan inte tas bort.';
        } else {
            if ($reportManager->deleteReport($reportId)) {
                $message = 'Race report borttagen.';
            } else {
                $error = 'Kunde inte ta bort.';
            }
        }
    }
}

// Get rider's reports (or admin's reports)
$isAdminUser = !empty($currentUser['is_admin']) && empty($_SESSION['rider_id']);

// For admin users, find linked rider_id via matching email
$linkedRiderId = null;
if ($isAdminUser && !empty($currentUser['email'])) {
    try {
        $stmt = $pdo->prepare("SELECT id FROM riders WHERE email = ? LIMIT 1");
        $stmt->execute([$currentUser['email']]);
        $linkedRider = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($linkedRider) {
            $linkedRiderId = $linkedRider['id'];
        }
    } catch (Exception $e) {
        // Ignore
    }
}

// Build filters - for admin users we need to check both admin_user_id AND linked rider_id
$reportFilters = [
    'include_drafts' => true,
    'per_page' => 50
];

if ($isAdminUser) {
    // Admin user - pass both IDs for OR query
    $reportFilters['admin_user_id'] = $_SESSION['admin_id'] ?? $currentUser['id'];
    if ($linkedRiderId) {
        $reportFilters['linked_rider_id'] = $linkedRiderId;
    }
} else {
    $reportFilters['rider_id'] = $currentUser['id'];
}
$myReports = $reportManager->listReports($reportFilters);

// Get rider's recent events for dropdown
$recentEvents = [];
try {
    $stmt = $pdo->prepare("
        SELECT DISTINCT e.id, e.name, e.date
        FROM events e
        INNER JOIN results r ON e.id = r.event_id
        WHERE r.cyclist_id = ?
        ORDER BY e.date DESC
        LIMIT 20
    ");
    $stmt->execute([$currentUser['id']]);
    $recentEvents = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Ignore
}

// Check if editing
$editReport = null;
if (isset($_GET['edit']) && is_numeric($_GET['edit'])) {
    $editReport = $reportManager->getReport((int)$_GET['edit'], false);
    if ($editReport) {
        // Check permission - rider owns post OR admin owns post OR admin's linked rider owns post
        $adminId = $_SESSION['admin_id'] ?? $currentUser['id'];
        $canEdit = (
            ($editReport['rider_id'] && $editReport['rider_id'] == $currentUser['id']) ||
            ($editReport['admin_user_id'] && $editReport['admin_user_id'] == $adminId) ||
            ($isAdminUser && $linkedRiderId && $editReport['rider_id'] == $linkedRiderId)
        );
        if (!$canEdit) {
            $editReport = null;
        }
    }
}

// Count stats
$publishedCount = 0;
$draftCount = 0;
$totalViews = 0;
$totalLikes = 0;
foreach ($myReports['reports'] as $r) {
    if ($r['status'] === 'published') $publishedCount++;
    if ($r['status'] === 'draft') $draftCount++;
    $totalViews += $r['views'];
    $totalLikes += $r['likes'];
}
?>

<?php if ($message): ?>
    <div class="alert alert-success mb-lg">
        <i data-lucide="check-circle"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<?php if ($error): ?>
    <div class="alert alert-error mb-lg">
        <i data-lucide="alert-circle"></i>
        <?= htmlspecialchars($error) ?>
    </div>
<?php endif; ?>

<!-- Quick Tips Bar -->
<div class="rr-tips-bar">
    <div class="rr-tip">
        <i data-lucide="instagram"></i>
        <span>Dela Instagram-inlägg</span>
    </div>
    <div class="rr-tip">
        <i data-lucide="youtube"></i>
        <span>Dela YouTube-video</span>
    </div>
    <div class="rr-tip">
        <i data-lucide="file-text"></i>
        <span>Skriv egen text</span>
    </div>
    <div class="rr-tip">
        <i data-lucide="link"></i>
        <span>Koppla till event</span>
    </div>
    <div class="rr-tip">
        <i data-lucide="clock"></i>
        <span>Granskning 1-2 dagar</span>
    </div>
</div>

<!-- Create/Edit Form -->
<div class="card rr-form-card">
    <div class="card-header">
        <h2>
            <i data-lucide="<?= $editReport ? 'edit-3' : 'plus-circle' ?>"></i>
            <?= $editReport ? 'Redigera Race Report' : 'Skriv ny Race Report' ?>
        </h2>
        <?php if ($editReport): ?>
        <a href="/profile/race-reports" class="btn btn-ghost btn-sm">
            <i data-lucide="x"></i>
            Avbryt redigering
        </a>
        <?php endif; ?>
    </div>

    <form method="POST" class="card-body rr-form">
        <?php if ($editReport): ?>
            <input type="hidden" name="action" value="update_report">
            <input type="hidden" name="report_id" value="<?= $editReport['id'] ?>">
        <?php else: ?>
            <input type="hidden" name="action" value="create_report">
        <?php endif; ?>

        <!-- Section 1: Basic Info -->
        <div class="rr-section">
            <div class="rr-section-header">
                <span class="rr-section-number">1</span>
                <h3>Grundläggande info</h3>
            </div>
            <div class="rr-section-content">
                <div class="form-group">
                    <label class="form-label">Titel <span class="text-error">*</span></label>
                    <input type="text"
                           name="title"
                           class="form-input form-input-lg"
                           placeholder="T.ex. Min första Enduro-tävling i Åre"
                           value="<?= htmlspecialchars($editReport['title'] ?? '') ?>"
                           required>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Kopplat event</label>
                        <select name="event_id" class="form-select">
                            <option value="">-- Välj event (valfritt) --</option>
                            <?php foreach ($recentEvents as $event): ?>
                                <option value="<?= $event['id'] ?>"
                                        <?= ($editReport && $editReport['event_id'] == $event['id']) ? 'selected' : '' ?>>
                                    <?= htmlspecialchars($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                                </option>
                            <?php endforeach; ?>
                        </select>
                        <small class="form-help">Koppla din report till en tävling du deltog i</small>
                    </div>

                    <?php if (!$editReport): ?>
                    <div class="form-group">
                        <label class="form-label">Taggar</label>
                        <input type="text"
                               name="tags"
                               class="form-input"
                               placeholder="enduro, åre, sm, 2026">
                        <small class="form-help">Kommaseparerade taggar</small>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>

        <!-- Section 2: Content -->
        <div class="rr-section">
            <div class="rr-section-header">
                <span class="rr-section-number">2</span>
                <h3>Innehåll</h3>
            </div>
            <div class="rr-section-content">
                <div class="form-group">
                    <label class="form-label">Din berättelse</label>
                    <textarea name="content"
                              class="form-textarea rr-content-textarea"
                              rows="10"
                              placeholder="Berätta om din tävlingsupplevelse!

Hur förberedde du dig?
Hur gick det på tävlingen?
Vilka utmaningar mötte du?
Vad lärde du dig?

Tipsa gärna andra åkare om banan eller arrangemanget."><?= htmlspecialchars($editReport['content'] ?? '') ?></textarea>
                    <small class="form-help">Skriv fritt - ditt inlägg kan vara kort eller långt</small>
                </div>
            </div>
        </div>

        <!-- Section 3: Media -->
        <div class="rr-section">
            <div class="rr-section-header">
                <span class="rr-section-number">3</span>
                <h3>Media <span class="rr-optional">(valfritt)</span></h3>
            </div>
            <div class="rr-section-content">
                <div class="rr-media-grid">
                    <!-- YouTube -->
                    <div class="rr-media-card">
                        <div class="rr-media-icon rr-media-youtube">
                            <i data-lucide="youtube"></i>
                        </div>
                        <div class="rr-media-content">
                            <label class="form-label">YouTube-video</label>
                            <input type="url"
                                   name="youtube_url"
                                   id="youtube_url"
                                   class="form-input"
                                   placeholder="https://www.youtube.com/watch?v=..."
                                   value="<?= htmlspecialchars($editReport['youtube_url'] ?? '') ?>"
                                   onchange="previewYoutube(this.value)">
                        </div>
                    </div>

                    <!-- Instagram -->
                    <div class="rr-media-card">
                        <div class="rr-media-icon rr-media-instagram">
                            <i data-lucide="instagram"></i>
                        </div>
                        <div class="rr-media-content">
                            <label class="form-label">Instagram-inlägg</label>
                            <input type="url"
                                   name="instagram_url"
                                   id="instagram_url"
                                   class="form-input"
                                   placeholder="https://www.instagram.com/p/..."
                                   value="<?= htmlspecialchars($editReport['instagram_url'] ?? '') ?>">
                        </div>
                    </div>

                    <!-- Featured Image -->
                    <div class="rr-media-card">
                        <div class="rr-media-icon rr-media-image">
                            <i data-lucide="image"></i>
                        </div>
                        <div class="rr-media-content">
                            <label class="form-label">Omslagsbild</label>
                            <input type="url"
                                   name="featured_image"
                                   class="form-input"
                                   placeholder="https://imgur.com/..."
                                   value="<?= htmlspecialchars($editReport['featured_image'] ?? '') ?>">
                            <small class="form-help">Länk till bild (Imgur, Google Photos etc)</small>
                        </div>
                    </div>
                </div>

                <!-- YouTube Preview -->
                <div id="youtube-preview" class="rr-preview" style="display: none;">
                    <div class="rr-preview-label"><i data-lucide="eye"></i> Förhandsgranskning</div>
                    <div id="youtube-embed"></div>
                </div>
            </div>
        </div>

        <!-- Submit -->
        <div class="rr-submit-section">
            <button type="submit" class="btn btn-primary btn-xl">
                <i data-lucide="<?= $editReport ? 'save' : 'send' ?>"></i>
                <?= $editReport ? 'Spara ändringar' : 'Skicka in för granskning' ?>
            </button>

            <?php if (!$editReport): ?>
            <p class="rr-submit-notice">
                <i data-lucide="shield-check"></i>
                Din report sparas som utkast och granskas av admin innan publicering.
            </p>
            <?php endif; ?>
        </div>
    </form>
</div>

<!-- My Reports List -->
<?php if (!empty($myReports['reports'])): ?>
<div class="card rr-list-card">
    <div class="card-header">
        <h2>
            <i data-lucide="folder"></i>
            Mina reports
        </h2>
        <div class="rr-header-stats">
            <span class="rr-mini-stat"><i data-lucide="check-circle"></i> <?= $publishedCount ?></span>
            <span class="rr-mini-stat"><i data-lucide="clock"></i> <?= $draftCount ?></span>
            <span class="rr-mini-stat"><i data-lucide="eye"></i> <?= number_format($totalViews) ?></span>
            <span class="rr-mini-stat"><i data-lucide="heart"></i> <?= number_format($totalLikes) ?></span>
        </div>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="rr-list">
            <?php foreach ($myReports['reports'] as $report): ?>
                <?php
                $statusConfigs = [
                    'published' => ['class' => 'rr-status-published', 'icon' => 'check-circle', 'text' => 'Publicerad'],
                    'draft' => ['class' => 'rr-status-draft', 'icon' => 'clock', 'text' => 'Väntar'],
                    'archived' => ['class' => 'rr-status-archived', 'icon' => 'archive', 'text' => 'Arkiverad']
                ];
                $statusConfig = $statusConfigs[$report['status']] ?? ['class' => '', 'icon' => 'circle', 'text' => $report['status']];
                ?>
                <div class="rr-item <?= $statusConfig['class'] ?>">
                    <div class="rr-item-thumb">
                        <?php if ($report['featured_image']): ?>
                            <img src="<?= htmlspecialchars($report['featured_image']) ?>" alt="">
                        <?php elseif ($report['youtube_video_id']): ?>
                            <img src="https://img.youtube.com/vi/<?= htmlspecialchars($report['youtube_video_id']) ?>/mqdefault.jpg" alt="">
                            <span class="rr-item-play"><i data-lucide="play"></i></span>
                        <?php else: ?>
                            <div class="rr-item-placeholder">
                                <i data-lucide="file-text"></i>
                            </div>
                        <?php endif; ?>
                    </div>
                    <div class="rr-item-body">
                        <div class="rr-item-top">
                            <h3 class="rr-item-title"><?= htmlspecialchars($report['title']) ?></h3>
                            <span class="rr-item-status">
                                <i data-lucide="<?= $statusConfig['icon'] ?>"></i>
                                <?= $statusConfig['text'] ?>
                            </span>
                        </div>
                        <div class="rr-item-meta">
                            <span><i data-lucide="calendar"></i> <?= date('j M Y', strtotime($report['created_at'])) ?></span>
                            <span><i data-lucide="eye"></i> <?= number_format($report['views']) ?></span>
                            <span><i data-lucide="heart"></i> <?= number_format($report['likes']) ?></span>
                        </div>
                    </div>
                    <div class="rr-item-actions">
                        <?php if ($report['status'] === 'published'): ?>
                            <a href="/news/<?= htmlspecialchars($report['slug']) ?>" class="btn btn-sm btn-primary" target="_blank" title="Visa">
                                <i data-lucide="external-link"></i>
                            </a>
                        <?php endif; ?>
                        <a href="?edit=<?= $report['id'] ?>" class="btn btn-sm btn-secondary" title="Redigera">
                            <i data-lucide="edit-2"></i>
                        </a>
                        <form method="POST" style="display: inline;" onsubmit="return confirm('Ta bort denna report?');">
                            <input type="hidden" name="action" value="delete_report">
                            <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                            <button type="submit" class="btn btn-sm btn-ghost text-error" title="Ta bort">
                                <i data-lucide="trash-2"></i>
                            </button>
                        </form>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</div>
<?php else: ?>
<div class="rr-empty-state">
    <div class="rr-empty-icon">
        <i data-lucide="pen-tool"></i>
    </div>
    <h3>Inga reports ännu</h3>
    <p>Du har inte skrivit några race reports. Fyll i formuläret ovan för att dela din första tävlingsupplevelse!</p>
</div>
<?php endif; ?>

<style>
/* Race Reports Page - Premium Desktop & Mobile Design */

/* Container for max-width on desktop */
.rr-container {
    max-width: 900px;
    margin: 0 auto;
}

/* Tips Bar - Compact horizontal strip */
.rr-tips-bar {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: var(--space-md) var(--space-xl);
    padding: var(--space-md) var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-xl);
}

.rr-tip {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: 0.8125rem;
    color: var(--color-text-secondary);
    white-space: nowrap;
}

.rr-tip i {
    width: 16px;
    height: 16px;
    color: var(--color-accent);
    flex-shrink: 0;
}

/* Form Card - Clean white card */
.rr-form-card {
    margin-bottom: var(--space-xl);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.rr-form-card .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-lg) var(--space-xl);
    background: var(--color-bg-surface);
    border-bottom: 1px solid var(--color-border);
}

.rr-form-card .card-header h2 {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin: 0;
    font-size: 1.25rem;
}

.rr-form-card .card-body {
    padding: var(--space-xl);
}

/* Sections - Clear visual separation */
.rr-section {
    margin-bottom: var(--space-xl);
    padding-bottom: var(--space-xl);
    border-bottom: 1px solid var(--color-border);
}

.rr-section:last-of-type {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.rr-section-header {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.rr-section-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: var(--color-accent);
    color: white;
    font-weight: 700;
    font-size: 0.8125rem;
    border-radius: 50%;
    flex-shrink: 0;
}

.rr-section-header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-primary);
}

.rr-optional {
    font-weight: 400;
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    margin-left: var(--space-xs);
}

.rr-section-content {
    padding-left: calc(28px + var(--space-md));
}

/* Form Elements - Clean inputs */
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-lg);
}

.form-input-lg {
    font-size: 1rem;
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md);
}

.rr-content-textarea {
    font-size: 0.9375rem;
    line-height: 1.7;
    min-height: 200px;
    resize: vertical;
    border-radius: var(--radius-md);
}

.form-help {
    display: block;
    margin-top: var(--space-xs);
    font-size: 0.75rem;
    color: var(--color-text-muted);
}

/* Media Grid - 3-column on desktop, stacked on mobile */
.rr-media-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-md);
}

.rr-media-card {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    padding: var(--space-md);
    background: var(--color-bg-hover);
    border-radius: var(--radius-md);
    border: 1px solid transparent;
    transition: border-color 0.2s ease;
}

.rr-media-card:focus-within {
    border-color: var(--color-accent);
}

.rr-media-card-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.rr-media-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.rr-media-icon i {
    width: 18px;
    height: 18px;
}

.rr-media-youtube {
    background: rgba(255, 0, 0, 0.1);
    color: #ff0000;
}

.rr-media-instagram {
    background: linear-gradient(135deg, rgba(131, 58, 180, 0.15), rgba(253, 29, 29, 0.15));
    color: #c13584;
}

.rr-media-image {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

.rr-media-content {
    flex: 1;
    min-width: 0;
}

.rr-media-content .form-label {
    font-size: 0.8125rem;
    font-weight: 500;
    margin-bottom: 0;
    color: var(--color-text-primary);
}

.rr-media-content .form-input {
    font-size: 0.8125rem;
    padding: var(--space-xs) var(--space-sm);
    margin-top: var(--space-xs);
}

/* Preview */
.rr-preview {
    margin-top: var(--space-lg);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
}

.rr-preview-label {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    margin-bottom: var(--space-sm);
}

.rr-preview-label i {
    width: 12px;
    height: 12px;
}

/* Submit Section */
.rr-submit-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-md);
    padding-top: var(--space-xl);
    border-top: 1px solid var(--color-border);
    margin-top: var(--space-xl);
}

.btn-xl {
    padding: var(--space-md) var(--space-2xl);
    font-size: 1rem;
    font-weight: 600;
    border-radius: var(--radius-md);
}

.rr-submit-notice {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    margin: 0;
}

.rr-submit-notice i {
    width: 16px;
    height: 16px;
    color: var(--color-accent);
}

/* Reports List */
.rr-list-card .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.rr-header-stats {
    display: flex;
    gap: var(--space-md);
}

.rr-mini-stat {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
    font-size: 0.8125rem;
    color: var(--color-text-muted);
}

.rr-mini-stat i {
    width: 14px;
    height: 14px;
}

.rr-list {
    display: flex;
    flex-direction: column;
}

.rr-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
    transition: background 0.15s ease;
}

.rr-item:last-child {
    border-bottom: none;
}

.rr-item:hover {
    background: var(--color-bg-hover);
}

.rr-item-thumb {
    width: 80px;
    height: 56px;
    flex-shrink: 0;
    border-radius: var(--radius-sm);
    overflow: hidden;
    position: relative;
    background: var(--color-bg-surface);
}

.rr-item-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.rr-item-play {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.4);
    color: white;
}

.rr-item-play i {
    width: 20px;
    height: 20px;
}

.rr-item-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-muted);
}

.rr-item-placeholder i {
    width: 24px;
    height: 24px;
}

.rr-item-body {
    flex: 1;
    min-width: 0;
}

.rr-item-top {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-2xs);
}

.rr-item-title {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.rr-item-status {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
    font-size: 0.6875rem;
    padding: 2px 8px;
    border-radius: var(--radius-full);
    white-space: nowrap;
    flex-shrink: 0;
}

.rr-item-status i {
    width: 10px;
    height: 10px;
}

.rr-status-published .rr-item-status {
    background: rgba(16, 185, 129, 0.15);
    color: var(--color-success);
}

.rr-status-draft .rr-item-status {
    background: rgba(251, 191, 36, 0.15);
    color: var(--color-warning);
}

.rr-status-archived .rr-item-status {
    background: rgba(107, 114, 128, 0.15);
    color: var(--color-text-muted);
}

.rr-item-meta {
    display: flex;
    gap: var(--space-md);
    font-size: 0.75rem;
    color: var(--color-text-muted);
}

.rr-item-meta span {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
}

.rr-item-meta i {
    width: 12px;
    height: 12px;
}

.rr-item-actions {
    display: flex;
    gap: var(--space-xs);
    flex-shrink: 0;
}

/* Empty State */
.rr-empty-state {
    text-align: center;
    padding: var(--space-3xl) var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
}

.rr-empty-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto var(--space-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-bg-hover);
    border-radius: 50%;
    color: var(--color-text-muted);
}

.rr-empty-icon i {
    width: 36px;
    height: 36px;
}

.rr-empty-state h3 {
    font-size: 1.25rem;
    margin: 0 0 var(--space-sm);
    color: var(--color-text-primary);
}

.rr-empty-state p {
    color: var(--color-text-secondary);
    max-width: 400px;
    margin: 0 auto;
}

/* YouTube Preview Card */
.rr-youtube-card {
    display: block;
    text-decoration: none;
    max-width: 480px;
    margin: 0 auto;
    border-radius: var(--radius-md);
    overflow: hidden;
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    transition: all 0.2s ease;
}

.rr-youtube-card:hover {
    border-color: var(--color-accent);
    transform: translateY(-2px);
}

.rr-youtube-thumbnail {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #000;
}

.rr-youtube-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.rr-youtube-play {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.9;
}

.rr-youtube-info {
    padding: var(--space-md);
    text-align: center;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

/* Responsive */
@media (max-width: 1024px) {
    .rr-media-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 767px) {
    .rr-tips-bar {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-sm);
        text-align: center;
        margin-left: calc(-1 * var(--space-md));
        margin-right: calc(-1 * var(--space-md));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .rr-tip {
        flex-direction: column;
        gap: var(--space-2xs);
        font-size: 0.6875rem;
    }

    .rr-section-content {
        padding-left: 0;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .rr-item {
        flex-wrap: wrap;
        padding: var(--space-md);
    }

    .rr-item-thumb {
        width: 60px;
        height: 42px;
    }

    .rr-item-body {
        flex: 1;
        min-width: calc(100% - 80px - var(--space-md));
    }

    .rr-item-actions {
        width: 100%;
        justify-content: flex-end;
        margin-top: var(--space-sm);
        padding-top: var(--space-sm);
        border-top: 1px solid var(--color-border);
    }

    .rr-header-stats {
        display: none;
    }
}

@media (max-width: 480px) {
    .rr-tips-bar {
        grid-template-columns: repeat(2, 1fr);
    }

    .rr-tips-bar .rr-tip:last-child {
        grid-column: span 2;
    }
}
</style>

<script>
// YouTube preview
function previewYoutube(url) {
    const previewContainer = document.getElementById('youtube-preview');
    const embedContainer = document.getElementById('youtube-embed');

    if (!url) {
        previewContainer.style.display = 'none';
        embedContainer.innerHTML = '';
        return;
    }

    // Extract video ID from URL
    let videoId = null;
    const patterns = [
        /youtube\.com\/watch\?v=([^&\s]+)/,
        /youtu\.be\/([^?\s]+)/,
        /youtube\.com\/embed\/([^?\s]+)/,
        /youtube\.com\/shorts\/([^?\s]+)/
    ];

    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) {
            videoId = match[1];
            break;
        }
    }

    if (!videoId) {
        previewContainer.style.display = 'block';
        embedContainer.innerHTML = '<p class="text-muted">Kunde inte tolka YouTube-länken.</p>';
        return;
    }

    previewContainer.style.display = 'block';
    embedContainer.innerHTML = `
        <a href="${url}" target="_blank" class="rr-youtube-card">
            <div class="rr-youtube-thumbnail">
                <img src="https://img.youtube.com/vi/${videoId}/maxresdefault.jpg"
                     alt="YouTube video"
                     onerror="this.src='https://img.youtube.com/vi/${videoId}/hqdefault.jpg'">
                <div class="rr-youtube-play">
                    <svg viewBox="0 0 68 48" width="68" height="48">
                        <path fill="#f00" d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79.13 34 0 34 0S12.21.13 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C.06 13.05 0 24 0 24s.06 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 47.87 34 48 34 48s21.79-.13 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C67.94 34.95 68 24 68 24s-.06-10.95-1.48-16.26z"/>
                        <path fill="#fff" d="M45 24L27 14v20"/>
                    </svg>
                </div>
            </div>
            <div class="rr-youtube-info">Klicka för att öppna på YouTube</div>
        </a>
    `;

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Check existing YouTube URL on load
document.addEventListener('DOMContentLoaded', function() {
    const youtubeInput = document.getElementById('youtube_url');
    if (youtubeInput && youtubeInput.value) {
        previewYoutube(youtubeInput.value);
    }
});
</script>
