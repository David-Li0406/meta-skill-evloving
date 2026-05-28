<?php
/**
 * TheHUB V1.0 - Betygsatt Events
 * Rider can rate events they have participated in
 */

$currentUser = hub_current_user();

if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();

// Configuration
$RATING_WINDOW_DAYS = 30; // Days after event that rating is allowed

// Handle form submissions
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'submit_rating') {
        $eventId = (int)($_POST['event_id'] ?? 0);
        $overallRating = (int)($_POST['overall_rating'] ?? 0);
        $comment = trim($_POST['comment'] ?? '');
        $questionScores = $_POST['question'] ?? [];

        // Validate
        if (!$eventId) {
            $error = 'Ogiltigt event.';
        } elseif ($overallRating < 1 || $overallRating > 10) {
            $error = 'Valj ett betyg mellan 1-10.';
        } else {
            // Verify rider has result for this event
            $checkStmt = $pdo->prepare("
                SELECT COUNT(*) FROM results
                WHERE cyclist_id = ? AND event_id = ?
            ");
            $checkStmt->execute([$currentUser['id'], $eventId]);
            $hasResult = $checkStmt->fetchColumn() > 0;

            if (!$hasResult) {
                $error = 'Du kan bara betygsatta events du har deltagit i.';
            } else {
                // Check if already rated
                $existsStmt = $pdo->prepare("
                    SELECT id FROM event_ratings WHERE rider_id = ? AND event_id = ?
                ");
                $existsStmt->execute([$currentUser['id'], $eventId]);
                $existingId = $existsStmt->fetchColumn();

                try {
                    $pdo->beginTransaction();

                    if ($existingId) {
                        // Update existing rating
                        $updateStmt = $pdo->prepare("
                            UPDATE event_ratings
                            SET overall_rating = ?, comment = ?, submitted_at = NOW()
                            WHERE id = ?
                        ");
                        $updateStmt->execute([$overallRating, $comment ?: null, $existingId]);
                        $ratingId = $existingId;

                        // Delete old answers
                        $pdo->prepare("DELETE FROM event_rating_answers WHERE rating_id = ?")->execute([$ratingId]);
                    } else {
                        // Insert new rating
                        $insertStmt = $pdo->prepare("
                            INSERT INTO event_ratings (event_id, rider_id, overall_rating, comment)
                            VALUES (?, ?, ?, ?)
                        ");
                        $insertStmt->execute([$eventId, $currentUser['id'], $overallRating, $comment ?: null]);
                        $ratingId = $pdo->lastInsertId();
                    }

                    // Insert question answers
                    if (!empty($questionScores)) {
                        $answerStmt = $pdo->prepare("
                            INSERT INTO event_rating_answers (rating_id, question_id, score)
                            VALUES (?, ?, ?)
                        ");
                        foreach ($questionScores as $questionId => $score) {
                            $score = (int)$score;
                            if ($score >= 1 && $score <= 10) {
                                $answerStmt->execute([$ratingId, (int)$questionId, $score]);
                            }
                        }
                    }

                    $pdo->commit();
                    $message = $existingId ? 'Ditt betyg har uppdaterats!' : 'Tack for ditt betyg!';
                } catch (Exception $e) {
                    $pdo->rollBack();
                    $error = 'Kunde inte spara betyget. Forsok igen.';
                }
            }
        }
    }
}

// Get questions
$questions = [];
try {
    $qStmt = $pdo->query("
        SELECT * FROM event_rating_questions
        WHERE active = 1
        ORDER BY sort_order ASC
    ");
    $questions = $qStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Table might not exist yet
}

// Get events that can be rated (recent events with results)
$ratableEvents = [];
try {
    $eventStmt = $pdo->prepare("
        SELECT DISTINCT
            e.id, e.name, e.date, e.location,
            s.name AS series_name,
            CASE WHEN er.id IS NOT NULL THEN 1 ELSE 0 END AS already_rated,
            er.overall_rating AS my_rating,
            er.submitted_at AS rated_at
        FROM events e
        INNER JOIN results r ON e.id = r.event_id AND r.cyclist_id = ?
        LEFT JOIN series s ON e.series_id = s.id
        LEFT JOIN event_ratings er ON e.id = er.event_id AND er.rider_id = ?
        WHERE e.date <= CURDATE()
          AND e.date >= DATE_SUB(CURDATE(), INTERVAL ? DAY)
        ORDER BY e.date DESC
    ");
    $eventStmt->execute([$currentUser['id'], $currentUser['id'], $RATING_WINDOW_DAYS]);
    $ratableEvents = $eventStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Ignore
}

// Get all past ratings
$pastRatings = [];
try {
    $pastStmt = $pdo->prepare("
        SELECT
            er.id, er.event_id, er.overall_rating, er.comment, er.submitted_at,
            e.name AS event_name, e.date AS event_date,
            s.name AS series_name
        FROM event_ratings er
        JOIN events e ON er.event_id = e.id
        LEFT JOIN series s ON e.series_id = s.id
        WHERE er.rider_id = ?
        ORDER BY er.submitted_at DESC
    ");
    $pastStmt->execute([$currentUser['id']]);
    $pastRatings = $pastStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Ignore
}

// Count stats
$totalRatings = count($pastRatings);
$avgRating = $totalRatings > 0 ? round(array_sum(array_column($pastRatings, 'overall_rating')) / $totalRatings, 1) : 0;
// PHP 5.x/7.x compatible - use traditional function instead of arrow function
$unratedCount = count(array_filter($ratableEvents, function($e) { return !$e['already_rated']; }));

// Check if rating a specific event
$ratingEvent = null;
$existingAnswers = [];
if (isset($_GET['event']) && is_numeric($_GET['event'])) {
    $eventId = (int)$_GET['event'];
    // Verify can rate this event
    foreach ($ratableEvents as $e) {
        if ($e['id'] == $eventId) {
            $ratingEvent = $e;
            break;
        }
    }

    // Load existing answers if editing
    if ($ratingEvent && $ratingEvent['already_rated']) {
        $ansStmt = $pdo->prepare("
            SELECT era.question_id, era.score
            FROM event_rating_answers era
            JOIN event_ratings er ON era.rating_id = er.id
            WHERE er.rider_id = ? AND er.event_id = ?
        ");
        $ansStmt->execute([$currentUser['id'], $eventId]);
        while ($row = $ansStmt->fetch(PDO::FETCH_ASSOC)) {
            $existingAnswers[$row['question_id']] = $row['score'];
        }

        // Get existing overall rating and comment
        $erStmt = $pdo->prepare("SELECT overall_rating, comment FROM event_ratings WHERE rider_id = ? AND event_id = ?");
        $erStmt->execute([$currentUser['id'], $eventId]);
        $existingRating = $erStmt->fetch(PDO::FETCH_ASSOC);
    }
}
?>

<!-- Page Header -->
<div class="er-header">
    <div class="er-header-content">
        <div class="er-header-icon">
            <i data-lucide="star"></i>
        </div>
        <div>
            <h1 class="er-title">Betygsatt Events</h1>
            <p class="er-subtitle">Hjalp arrangorer att forbattra genom din feedback</p>
        </div>
    </div>
    <div class="er-stats">
        <div class="er-stat">
            <span class="er-stat-value"><?= $totalRatings ?></span>
            <span class="er-stat-label">Betygsatta</span>
        </div>
        <div class="er-stat">
            <span class="er-stat-value"><?= $unratedCount ?></span>
            <span class="er-stat-label">Att betygsatta</span>
        </div>
        <?php if ($avgRating > 0): ?>
        <div class="er-stat">
            <span class="er-stat-value"><?= $avgRating ?></span>
            <span class="er-stat-label">Ditt snitt</span>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if ($message): ?>
    <div class="alert alert-success mb-lg">
        <i data-lucide="check-circle"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<?php if ($error): ?>
    <div class="alert alert-danger mb-lg">
        <i data-lucide="alert-circle"></i>
        <?= htmlspecialchars($error) ?>
    </div>
<?php endif; ?>

<?php if (empty($questions)): ?>
    <div class="alert alert-warning">
        <i data-lucide="alert-triangle"></i>
        Betygsattningssystemet ar inte aktiverat annu. Kontakta admin.
    </div>
<?php elseif ($ratingEvent): ?>
    <!-- Rating Form -->
    <div class="card er-form-card">
        <div class="card-header">
            <h2>
                <i data-lucide="<?= $ratingEvent['already_rated'] ? 'edit-3' : 'star' ?>"></i>
                <?= $ratingEvent['already_rated'] ? 'Uppdatera betyg' : 'Betygsatt event' ?>
            </h2>
        </div>
        <div class="card-body">
            <div class="er-event-info">
                <div class="er-event-name"><?= htmlspecialchars($ratingEvent['name']) ?></div>
                <div class="er-event-meta">
                    <span><i data-lucide="calendar"></i> <?= date('j M Y', strtotime($ratingEvent['date'])) ?></span>
                    <?php if ($ratingEvent['series_name']): ?>
                        <span><i data-lucide="trophy"></i> <?= htmlspecialchars($ratingEvent['series_name']) ?></span>
                    <?php endif; ?>
                    <?php if ($ratingEvent['location']): ?>
                        <span><i data-lucide="map-pin"></i> <?= htmlspecialchars($ratingEvent['location']) ?></span>
                    <?php endif; ?>
                </div>
            </div>

            <form method="POST" class="er-form">
                <input type="hidden" name="action" value="submit_rating">
                <input type="hidden" name="event_id" value="<?= $ratingEvent['id'] ?>">

                <!-- Question-based ratings -->
                <div class="er-questions">
                    <h3 class="er-section-title">Betygsatt foljande (1-10)</h3>
                    <?php foreach ($questions as $q): ?>
                        <div class="er-question">
                            <label class="er-question-label"><?= htmlspecialchars($q['question_text']) ?></label>
                            <div class="er-rating-slider">
                                <input type="range"
                                       name="question[<?= $q['id'] ?>]"
                                       min="1" max="10"
                                       value="<?= $existingAnswers[$q['id']] ?? 5 ?>"
                                       class="er-slider"
                                       oninput="this.nextElementSibling.textContent = this.value">
                                <span class="er-slider-value"><?= $existingAnswers[$q['id']] ?? 5 ?></span>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <!-- Overall rating -->
                <div class="er-overall">
                    <h3 class="er-section-title">Overgripande betyg</h3>
                    <p class="er-help">Hur skulle du betygsatta detta event overlag?</p>
                    <div class="er-overall-rating">
                        <?php for ($i = 1; $i <= 10; $i++): ?>
                            <label class="er-rating-option">
                                <input type="radio"
                                       name="overall_rating"
                                       value="<?= $i ?>"
                                       <?= (($existingRating['overall_rating'] ?? 0) == $i) ? 'checked' : '' ?>
                                       required>
                                <span class="er-rating-number"><?= $i ?></span>
                            </label>
                        <?php endfor; ?>
                    </div>
                    <div class="er-rating-labels">
                        <span>Mycket daligt</span>
                        <span>Utmarkt</span>
                    </div>
                </div>

                <!-- Comment -->
                <div class="er-comment">
                    <h3 class="er-section-title">Kommentar (valfritt)</h3>
                    <textarea name="comment"
                              class="form-textarea"
                              rows="3"
                              placeholder="Dela med dig av dina tankar om eventet..."><?= htmlspecialchars($existingRating['comment'] ?? '') ?></textarea>
                    <p class="er-help">Din feedback ar anonym och hjalper arrangorer att forbattra.</p>
                </div>

                <div class="er-form-actions">
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i data-lucide="send"></i>
                        <?= $ratingEvent['already_rated'] ? 'Uppdatera betyg' : 'Skicka betyg' ?>
                    </button>
                    <a href="/profile/event-ratings" class="btn btn-secondary">
                        <i data-lucide="x"></i>
                        Avbryt
                    </a>
                </div>
            </form>
        </div>
    </div>

<?php else: ?>
    <!-- Events to Rate -->
    <?php if (!empty($ratableEvents)): ?>
        <div class="card">
            <div class="card-header">
                <h2><i data-lucide="calendar-check"></i> Events att betygsatta</h2>
                <span class="badge"><?= $unratedCount ?> nya</span>
            </div>
            <div class="card-body">
                <?php if ($unratedCount == 0): ?>
                    <div class="er-empty">
                        <div class="er-empty-icon">
                            <i data-lucide="check-circle-2"></i>
                        </div>
                        <h3>Alla events betygsatta!</h3>
                        <p>Du har betygsatt alla dina senaste events. Bra jobbat!</p>
                    </div>
                <?php else: ?>
                    <div class="er-event-list">
                        <?php foreach ($ratableEvents as $event): ?>
                            <?php if (!$event['already_rated']): ?>
                                <a href="?event=<?= $event['id'] ?>" class="er-event-item">
                                    <div class="er-event-date">
                                        <span class="er-day"><?= date('j', strtotime($event['date'])) ?></span>
                                        <span class="er-month"><?= strftime('%b', strtotime($event['date'])) ?></span>
                                    </div>
                                    <div class="er-event-details">
                                        <span class="er-event-title"><?= htmlspecialchars($event['name']) ?></span>
                                        <?php if ($event['series_name']): ?>
                                            <span class="er-event-series"><?= htmlspecialchars($event['series_name']) ?></span>
                                        <?php endif; ?>
                                    </div>
                                    <div class="er-event-action">
                                        <i data-lucide="star"></i>
                                        Betygsatt
                                    </div>
                                </a>
                            <?php endif; ?>
                        <?php endforeach; ?>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    <?php endif; ?>

    <!-- Past Ratings -->
    <?php if (!empty($pastRatings)): ?>
        <div class="card mt-lg">
            <div class="card-header">
                <h2><i data-lucide="history"></i> Dina betyg</h2>
                <span class="badge"><?= count($pastRatings) ?></span>
            </div>
            <div class="card-body">
                <div class="er-ratings-list">
                    <?php foreach ($pastRatings as $rating): ?>
                        <div class="er-rating-item">
                            <div class="er-rating-score">
                                <span class="er-score-value"><?= $rating['overall_rating'] ?></span>
                                <span class="er-score-max">/10</span>
                            </div>
                            <div class="er-rating-details">
                                <span class="er-rating-event"><?= htmlspecialchars($rating['event_name']) ?></span>
                                <span class="er-rating-meta">
                                    <?= date('j M Y', strtotime($rating['event_date'])) ?>
                                    <?php if ($rating['series_name']): ?>
                                        &middot; <?= htmlspecialchars($rating['series_name']) ?>
                                    <?php endif; ?>
                                </span>
                            </div>
                            <?php
                            // Check if this event can still be edited
                            $canEdit = false;
                            foreach ($ratableEvents as $re) {
                                if ($re['id'] == $rating['event_id']) {
                                    $canEdit = true;
                                    break;
                                }
                            }
                            ?>
                            <?php if ($canEdit): ?>
                                <a href="?event=<?= $rating['event_id'] ?>" class="btn btn-sm btn-ghost">
                                    <i data-lucide="edit-2"></i>
                                </a>
                            <?php endif; ?>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    <?php endif; ?>

    <!-- Empty State -->
    <?php if (empty($ratableEvents) && empty($pastRatings)): ?>
        <div class="card">
            <div class="card-body">
                <div class="er-empty">
                    <div class="er-empty-icon">
                        <i data-lucide="calendar-x"></i>
                    </div>
                    <h3>Inga events att betygsatta</h3>
                    <p>Du har inga nyligen genomforda events att betygsatta. Nar du har deltagit i ett event kan du betygsatta det har.</p>
                    <a href="/calendar" class="btn btn-primary mt-md">
                        <i data-lucide="calendar"></i>
                        Se kommande events
                    </a>
                </div>
            </div>
        </div>
    <?php endif; ?>
<?php endif; ?>

<style>
/* Event Ratings Page Styles */

.er-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
    flex-wrap: wrap;
}

.er-header-content {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.er-header-icon {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-accent), var(--color-accent-hover));
    border-radius: var(--radius-lg);
    color: white;
}

.er-header-icon i {
    width: 28px;
    height: 28px;
}

.er-title {
    font-size: 1.75rem;
    margin: 0;
    color: var(--color-text-primary);
}

.er-subtitle {
    margin: var(--space-2xs) 0 0;
    color: var(--color-text-secondary);
}

.er-stats {
    display: flex;
    gap: var(--space-lg);
}

.er-stat {
    text-align: center;
}

.er-stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-accent);
}

.er-stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
}

/* Form Card */
.er-form-card {
    border: 2px solid var(--color-accent-light);
}

.er-event-info {
    padding: var(--space-lg);
    background: var(--color-bg-page);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-xl);
}

.er-event-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-xs);
}

.er-event-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

.er-event-meta span {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
}

.er-event-meta i {
    width: 14px;
    height: 14px;
}

/* Questions */
.er-questions {
    margin-bottom: var(--space-xl);
}

.er-section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 var(--space-md);
}

.er-question {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md) 0;
    border-bottom: 1px solid var(--color-border);
}

.er-question:last-child {
    border-bottom: none;
}

.er-question-label {
    flex: 1;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

.er-rating-slider {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    min-width: 150px;
}

.er-slider {
    flex: 1;
    height: 6px;
    border-radius: var(--radius-full);
    background: var(--color-bg-hover);
    appearance: none;
    cursor: pointer;
}

.er-slider::-webkit-slider-thumb {
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--color-accent);
    cursor: pointer;
    transition: transform 0.15s;
}

.er-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
}

.er-slider-value {
    min-width: 24px;
    text-align: center;
    font-weight: 600;
    color: var(--color-accent);
}

/* Overall Rating */
.er-overall {
    margin-bottom: var(--space-xl);
    padding: var(--space-lg);
    background: var(--color-bg-page);
    border-radius: var(--radius-md);
}

.er-help {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    margin: var(--space-xs) 0 var(--space-md);
}

.er-overall-rating {
    display: flex;
    justify-content: space-between;
    gap: var(--space-xs);
}

.er-rating-option {
    flex: 1;
}

.er-rating-option input {
    display: none;
}

.er-rating-number {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 48px;
    background: var(--color-bg-surface);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    font-weight: 600;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all 0.15s;
}

.er-rating-option:hover .er-rating-number {
    border-color: var(--color-accent);
    color: var(--color-accent);
}

.er-rating-option input:checked + .er-rating-number {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

.er-rating-labels {
    display: flex;
    justify-content: space-between;
    margin-top: var(--space-xs);
    font-size: 0.75rem;
    color: var(--color-text-muted);
}

/* Comment */
.er-comment {
    margin-bottom: var(--space-lg);
}

.er-comment .form-textarea {
    resize: vertical;
}

.er-form-actions {
    display: flex;
    gap: var(--space-md);
}

/* Event List */
.er-event-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.er-event-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-page);
    border-radius: var(--radius-md);
    text-decoration: none;
    transition: all 0.15s;
}

.er-event-item:hover {
    background: var(--color-bg-hover);
}

.er-event-date {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 50px;
    padding: var(--space-sm);
    background: var(--color-accent-light);
    border-radius: var(--radius-sm);
}

.er-day {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-accent);
    line-height: 1;
}

.er-month {
    font-size: 0.75rem;
    color: var(--color-accent-text);
    text-transform: uppercase;
}

.er-event-details {
    flex: 1;
    min-width: 0;
}

.er-event-title {
    display: block;
    font-weight: 500;
    color: var(--color-text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.er-event-series {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.er-event-action {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-accent);
    color: white;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 500;
}

.er-event-action i {
    width: 16px;
    height: 16px;
}

/* Ratings List */
.er-ratings-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.er-rating-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-page);
    border-radius: var(--radius-md);
}

.er-rating-score {
    display: flex;
    align-items: baseline;
    min-width: 60px;
}

.er-score-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-accent);
}

.er-score-max {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.er-rating-details {
    flex: 1;
    min-width: 0;
}

.er-rating-event {
    display: block;
    font-weight: 500;
    color: var(--color-text-primary);
}

.er-rating-meta {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

/* Empty State */
.er-empty {
    text-align: center;
    padding: var(--space-2xl);
}

.er-empty-icon {
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

.er-empty-icon i {
    width: 36px;
    height: 36px;
}

.er-empty h3 {
    font-size: 1.25rem;
    margin: 0 0 var(--space-sm);
    color: var(--color-text-primary);
}

.er-empty p {
    color: var(--color-text-secondary);
    max-width: 400px;
    margin: 0 auto;
}

/* Mobile */
@media (max-width: 768px) {
    .er-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .er-stats {
        width: 100%;
        justify-content: space-around;
    }

    .er-question {
        flex-direction: column;
        align-items: flex-start;
        gap: var(--space-sm);
    }

    .er-rating-slider {
        width: 100%;
    }

    .er-overall-rating {
        flex-wrap: wrap;
    }

    .er-rating-option {
        flex: 0 0 calc(20% - var(--space-xs));
    }

    .er-form-actions {
        flex-direction: column;
    }

    .er-event-item {
        flex-wrap: wrap;
    }

    .er-event-action {
        width: 100%;
        justify-content: center;
        margin-top: var(--space-sm);
    }
}

@media (max-width: 480px) {
    .er-header-icon {
        width: 48px;
        height: 48px;
    }

    .er-title {
        font-size: 1.5rem;
    }

    .er-rating-option {
        flex: 0 0 calc(20% - var(--space-xs));
    }

    .er-rating-number {
        height: 40px;
        font-size: 0.875rem;
    }
}
</style>
