<?php
/**
 * TheHUB V1.0 - Win-Back Survey
 * Survey for churned riders with automatic discount code generation
 */

$currentUser = hub_current_user();

if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();

// Check if winback tables exist
$tablesExist = false;
try {
    $check = $pdo->query("SHOW TABLES LIKE 'winback_campaigns'");
    $tablesExist = $check->rowCount() > 0;
} catch (Exception $e) {}

if (!$tablesExist) {
    // Show message that feature is not available
    ?>
    <div class="page-header">
        <h1 class="page-title">
            <i data-lucide="clipboard-list" class="page-icon"></i>
            Feedback-enkat
        </h1>
    </div>
    <div class="alert alert-info">
        <i data-lucide="info"></i>
        <div>Denna funktion ar inte aktiverad annu. Kontakta admin.</div>
    </div>
    <?php
    return;
}

// Find applicable campaign for this user
$campaign = null;
$alreadyResponded = false;
$existingResponse = null;

try {
    // Get active campaigns
    $campStmt = $pdo->query("
        SELECT * FROM winback_campaigns
        WHERE is_active = 1
        ORDER BY id ASC
    ");
    $campaigns = $campStmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($campaigns as $c) {
        $brandIds = json_decode($c['brand_ids'] ?? '[]', true) ?: [];

        // Check if user qualifies: competed in start_year-end_year but NOT in target_year
        // For this brand's series

        if (empty($brandIds)) {
            // All brands - just check years
            $checkSql = "
                SELECT COUNT(DISTINCT e.id) as cnt
                FROM results r
                JOIN events e ON r.event_id = e.id
                WHERE r.cyclist_id = ?
                  AND YEAR(e.date) BETWEEN ? AND ?
            ";
            $stmt = $pdo->prepare($checkSql);
            $stmt->execute([$currentUser['id'], $c['start_year'], $c['end_year']]);
            $historicalCount = (int)$stmt->fetchColumn();

            $checkSql2 = "
                SELECT COUNT(*) as cnt
                FROM results r
                JOIN events e ON r.event_id = e.id
                WHERE r.cyclist_id = ?
                  AND YEAR(e.date) = ?
            ";
            $stmt2 = $pdo->prepare($checkSql2);
            $stmt2->execute([$currentUser['id'], $c['target_year']]);
            $targetYearCount = (int)$stmt2->fetchColumn();
        } else {
            // Specific brands
            $placeholders = implode(',', array_fill(0, count($brandIds), '?'));

            $checkSql = "
                SELECT COUNT(DISTINCT e.id) as cnt
                FROM results r
                JOIN events e ON r.event_id = e.id
                JOIN series s ON e.series_id = s.id
                JOIN brand_series_map bsm ON s.id = bsm.series_id
                WHERE r.cyclist_id = ?
                  AND YEAR(e.date) BETWEEN ? AND ?
                  AND bsm.brand_id IN ($placeholders)
            ";
            $params = array_merge([$currentUser['id'], $c['start_year'], $c['end_year']], $brandIds);
            $stmt = $pdo->prepare($checkSql);
            $stmt->execute($params);
            $historicalCount = (int)$stmt->fetchColumn();

            $checkSql2 = "
                SELECT COUNT(*) as cnt
                FROM results r
                JOIN events e ON r.event_id = e.id
                JOIN series s ON e.series_id = s.id
                JOIN brand_series_map bsm ON s.id = bsm.series_id
                WHERE r.cyclist_id = ?
                  AND YEAR(e.date) = ?
                  AND bsm.brand_id IN ($placeholders)
            ";
            $params2 = array_merge([$currentUser['id'], $c['target_year']], $brandIds);
            $stmt2 = $pdo->prepare($checkSql2);
            $stmt2->execute($params2);
            $targetYearCount = (int)$stmt2->fetchColumn();
        }

        // User qualifies if they competed historically but NOT in target year
        if ($historicalCount > 0 && $targetYearCount == 0) {
            $campaign = $c;

            // Check if already responded
            $respStmt = $pdo->prepare("
                SELECT * FROM winback_responses
                WHERE rider_id = ? AND campaign_id = ?
            ");
            $respStmt->execute([$currentUser['id'], $c['id']]);
            $existingResponse = $respStmt->fetch(PDO::FETCH_ASSOC);
            $alreadyResponded = (bool)$existingResponse;

            break;
        }
    }
} catch (Exception $e) {
    // Ignore errors, just don't show survey
}

// No applicable campaign
if (!$campaign) {
    ?>
    <div class="page-header">
        <h1 class="page-title">
            <i data-lucide="clipboard-list" class="page-icon"></i>
            Feedback-enkat
        </h1>
    </div>
    <div class="card">
        <div class="card-body" style="text-align: center; padding: var(--space-2xl);">
            <div style="width: 80px; height: 80px; margin: 0 auto var(--space-lg); display: flex; align-items: center; justify-content: center; background: var(--color-bg-hover); border-radius: 50%;">
                <i data-lucide="check-circle" style="width: 36px; height: 36px; color: var(--color-success);"></i>
            </div>
            <h3>Ingen enkat tillganglig</h3>
            <p style="color: var(--color-text-secondary);">
                Just nu finns det ingen feedback-enkat for dig. Tack for att du ar aktiv!
            </p>
            <a href="/profile" class="btn btn-primary" style="margin-top: var(--space-md);">
                <i data-lucide="arrow-left"></i> Tillbaka till profilen
            </a>
        </div>
    </div>
    <?php
    return;
}

// Get questions
$questions = [];
try {
    $qStmt = $pdo->prepare("
        SELECT * FROM winback_questions
        WHERE active = 1 AND (campaign_id IS NULL OR campaign_id = ?)
        ORDER BY sort_order ASC
    ");
    $qStmt->execute([$campaign['id']]);
    $questions = $qStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {}

// Handle form submission
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !$alreadyResponded) {
    $action = $_POST['action'] ?? '';

    if ($action === 'submit_survey') {
        try {
            $pdo->beginTransaction();

            // Generate unique discount code
            $discountCode = 'WB' . strtoupper(substr(md5($currentUser['id'] . $campaign['id'] . time()), 0, 8));

            // Create discount code in discount_codes table
            $discountStmt = $pdo->prepare("
                INSERT INTO discount_codes (code, description, discount_type, discount_value, max_uses, max_uses_per_user, valid_until, applicable_to, is_active, created_by)
                VALUES (?, ?, ?, ?, 1, 1, ?, ?, 1, NULL)
            ");
            $discountStmt->execute([
                $discountCode,
                'Win-back: ' . $campaign['name'] . ' - ' . $currentUser['firstname'] . ' ' . $currentUser['lastname'],
                $campaign['discount_type'],
                $campaign['discount_value'],
                $campaign['discount_valid_until'],
                $campaign['discount_applicable_to']
            ]);
            $discountCodeId = $pdo->lastInsertId();

            // Create response
            $respStmt = $pdo->prepare("
                INSERT INTO winback_responses (campaign_id, rider_id, discount_code_id, discount_code, ip_hash)
                VALUES (?, ?, ?, ?, ?)
            ");
            $ipHash = hash('sha256', $_SERVER['REMOTE_ADDR'] ?? '');
            $respStmt->execute([$campaign['id'], $currentUser['id'], $discountCodeId, $discountCode, $ipHash]);
            $responseId = $pdo->lastInsertId();

            // Save answers
            $answerStmt = $pdo->prepare("
                INSERT INTO winback_answers (response_id, question_id, answer_value, answer_scale)
                VALUES (?, ?, ?, ?)
            ");

            foreach ($questions as $q) {
                $fieldName = 'q_' . $q['id'];
                $value = $_POST[$fieldName] ?? null;

                if ($q['question_type'] === 'checkbox' && is_array($value)) {
                    $answerStmt->execute([$responseId, $q['id'], json_encode($value), null]);
                } elseif ($q['question_type'] === 'scale') {
                    $answerStmt->execute([$responseId, $q['id'], null, (int)$value]);
                } else {
                    $answerStmt->execute([$responseId, $q['id'], $value, null]);
                }
            }

            $pdo->commit();

            // Reload response
            $respStmt = $pdo->prepare("SELECT * FROM winback_responses WHERE id = ?");
            $respStmt->execute([$responseId]);
            $existingResponse = $respStmt->fetch(PDO::FETCH_ASSOC);
            $alreadyResponded = true;
            $message = 'Tack for din feedback!';

        } catch (Exception $e) {
            $pdo->rollBack();
            $error = 'Kunde inte spara enkaten. Forsok igen.';
        }
    }
}
?>

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="clipboard-list" class="page-icon"></i>
        Feedback-enkat
    </h1>
    <p class="page-subtitle">Hjalp oss forbattra - fa en rabattkod som tack!</p>
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

<?php if ($alreadyResponded && $existingResponse): ?>
<!-- Already responded - show discount code -->
<div class="card wb-success-card">
    <div class="card-body">
        <div class="wb-success-icon">
            <i data-lucide="gift"></i>
        </div>
        <h2>Tack for din feedback!</h2>
        <p class="wb-success-text">
            Din rost ar viktig for oss. Som tack far du en personlig rabattkod.
        </p>

        <div class="wb-discount-box">
            <div class="wb-discount-label">Din rabattkod</div>
            <div class="wb-discount-code" onclick="copyCode(this)"><?= htmlspecialchars($existingResponse['discount_code']) ?></div>
            <div class="wb-discount-value">
                <?php if ($campaign['discount_type'] === 'percentage'): ?>
                    <?= intval($campaign['discount_value']) ?>% rabatt
                <?php else: ?>
                    <?= number_format($campaign['discount_value'], 0) ?> kr rabatt
                <?php endif; ?>
            </div>
            <?php if ($campaign['discount_valid_until']): ?>
                <div class="wb-discount-expires">
                    Giltig t.o.m. <?= date('j M Y', strtotime($campaign['discount_valid_until'])) ?>
                </div>
            <?php endif; ?>
        </div>

        <p class="wb-help">Klicka pa koden for att kopiera. Anvand vid anmalan.</p>

        <a href="/calendar" class="btn btn-primary btn-lg" style="margin-top: var(--space-lg);">
            <i data-lucide="calendar"></i> Se kommande tavlingar
        </a>
    </div>
</div>

<?php else: ?>
<!-- Survey form -->
<div class="card wb-form-card">
    <div class="card-header">
        <h2>
            <i data-lucide="message-square"></i>
            Vi saknar dig!
        </h2>
    </div>
    <div class="card-body">
        <div class="wb-intro">
            <p>
                Vi har sett att du inte tavlade <?= $campaign['target_year'] ?> och vill garna hora vad vi kan gora battre.
                Svara pa nagra korta fragor sa far du en <strong>rabattkod</strong> som tack!
            </p>
            <div class="wb-reward-preview">
                <i data-lucide="gift"></i>
                <span>
                    <?php if ($campaign['discount_type'] === 'percentage'): ?>
                        <?= intval($campaign['discount_value']) ?>% rabatt pa din nasta anmalan
                    <?php else: ?>
                        <?= number_format($campaign['discount_value'], 0) ?> kr rabatt pa din nasta anmalan
                    <?php endif; ?>
                </span>
            </div>
        </div>

        <form method="POST" class="wb-form">
            <input type="hidden" name="action" value="submit_survey">

            <?php foreach ($questions as $q): ?>
                <div class="wb-question">
                    <label class="wb-question-label">
                        <?= htmlspecialchars($q['question_text']) ?>
                        <?php if ($q['is_required']): ?>
                            <span class="wb-required">*</span>
                        <?php endif; ?>
                    </label>

                    <?php if ($q['question_type'] === 'checkbox'): ?>
                        <?php $options = json_decode($q['options'] ?? '[]', true) ?: []; ?>
                        <div class="wb-checkbox-group">
                            <?php foreach ($options as $i => $opt): ?>
                                <label class="wb-checkbox-option">
                                    <input type="checkbox" name="q_<?= $q['id'] ?>[]" value="<?= htmlspecialchars($opt) ?>">
                                    <span class="wb-checkbox-label"><?= htmlspecialchars($opt) ?></span>
                                </label>
                            <?php endforeach; ?>
                        </div>

                    <?php elseif ($q['question_type'] === 'radio'): ?>
                        <?php $options = json_decode($q['options'] ?? '[]', true) ?: []; ?>
                        <div class="wb-radio-group">
                            <?php foreach ($options as $i => $opt): ?>
                                <label class="wb-radio-option">
                                    <input type="radio" name="q_<?= $q['id'] ?>" value="<?= htmlspecialchars($opt) ?>" <?= $q['is_required'] ? 'required' : '' ?>>
                                    <span class="wb-radio-label"><?= htmlspecialchars($opt) ?></span>
                                </label>
                            <?php endforeach; ?>
                        </div>

                    <?php elseif ($q['question_type'] === 'scale'): ?>
                        <div class="wb-scale">
                            <div class="wb-scale-options">
                                <?php for ($i = 1; $i <= 10; $i++): ?>
                                    <label class="wb-scale-option">
                                        <input type="radio" name="q_<?= $q['id'] ?>" value="<?= $i ?>" <?= $q['is_required'] ? 'required' : '' ?>>
                                        <span class="wb-scale-number"><?= $i ?></span>
                                    </label>
                                <?php endfor; ?>
                            </div>
                            <div class="wb-scale-labels">
                                <span>Mycket osannolikt</span>
                                <span>Definitivt</span>
                            </div>
                        </div>

                    <?php elseif ($q['question_type'] === 'text'): ?>
                        <textarea name="q_<?= $q['id'] ?>"
                                  class="form-textarea"
                                  rows="3"
                                  placeholder="Skriv har..."
                                  <?= $q['is_required'] ? 'required' : '' ?>></textarea>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>

            <div class="wb-form-footer">
                <p class="wb-privacy">
                    <i data-lucide="shield"></i>
                    Din feedback ar anonym och anvands endast for att forbattra vara arrangemang.
                </p>
                <button type="submit" class="btn btn-primary btn-lg">
                    <i data-lucide="send"></i>
                    Skicka och hamta rabattkod
                </button>
            </div>
        </form>
    </div>
</div>
<?php endif; ?>

<style>
/* Win-Back Survey Styles */
.page-subtitle {
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}

.wb-form-card {
    border: 2px solid var(--color-accent-light);
}

.wb-intro {
    margin-bottom: var(--space-xl);
    padding: var(--space-lg);
    background: var(--color-bg-page);
    border-radius: var(--radius-md);
}

.wb-intro p {
    margin-bottom: var(--space-md);
    line-height: 1.6;
}

.wb-reward-preview {
    display: inline-flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-accent-light);
    border-radius: var(--radius-md);
    color: var(--color-accent);
    font-weight: 600;
}

.wb-reward-preview i {
    width: 20px;
    height: 20px;
}

.wb-question {
    margin-bottom: var(--space-xl);
    padding-bottom: var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.wb-question:last-of-type {
    border-bottom: none;
}

.wb-question-label {
    display: block;
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-md);
}

.wb-required {
    color: var(--color-error);
}

/* Checkbox group */
.wb-checkbox-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.wb-checkbox-option {
    display: flex;
    align-items: flex-start;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-page);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s;
}

.wb-checkbox-option:hover {
    background: var(--color-bg-hover);
}

.wb-checkbox-option input {
    margin-top: 2px;
    accent-color: var(--color-accent);
}

.wb-checkbox-option input:checked + .wb-checkbox-label {
    color: var(--color-accent);
    font-weight: 500;
}

/* Radio group */
.wb-radio-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.wb-radio-option {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-page);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s;
}

.wb-radio-option:hover {
    background: var(--color-bg-hover);
}

.wb-radio-option input {
    accent-color: var(--color-accent);
}

/* Scale */
.wb-scale {
    margin-top: var(--space-sm);
}

.wb-scale-options {
    display: flex;
    justify-content: space-between;
    gap: var(--space-xs);
}

.wb-scale-option {
    flex: 1;
}

.wb-scale-option input {
    display: none;
}

.wb-scale-number {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 48px;
    background: var(--color-bg-page);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    font-weight: 600;
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: all 0.15s;
}

.wb-scale-option:hover .wb-scale-number {
    border-color: var(--color-accent);
    color: var(--color-accent);
}

.wb-scale-option input:checked + .wb-scale-number {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

.wb-scale-labels {
    display: flex;
    justify-content: space-between;
    margin-top: var(--space-xs);
    font-size: 0.75rem;
    color: var(--color-text-muted);
}

/* Form footer */
.wb-form-footer {
    margin-top: var(--space-xl);
    padding-top: var(--space-lg);
    border-top: 1px solid var(--color-border);
}

.wb-privacy {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.wb-privacy i {
    width: 16px;
    height: 16px;
    color: var(--color-success);
}

/* Success card */
.wb-success-card {
    text-align: center;
    border: 2px solid var(--color-success);
}

.wb-success-card .card-body {
    padding: var(--space-2xl);
}

.wb-success-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto var(--space-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-accent), var(--color-accent-hover));
    border-radius: 50%;
    color: white;
}

.wb-success-icon i {
    width: 40px;
    height: 40px;
}

.wb-success-text {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-xl);
}

.wb-discount-box {
    background: var(--color-bg-page);
    border: 2px dashed var(--color-accent);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    margin-bottom: var(--space-md);
}

.wb-discount-label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    margin-bottom: var(--space-sm);
}

.wb-discount-code {
    font-family: monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent);
    letter-spacing: 2px;
    cursor: pointer;
    padding: var(--space-sm);
    border-radius: var(--radius-sm);
    transition: background 0.15s;
}

.wb-discount-code:hover {
    background: var(--color-accent-light);
}

.wb-discount-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-success);
    margin-top: var(--space-sm);
}

.wb-discount-expires {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}

.wb-help {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

/* Mobile */
@media (max-width: 768px) {
    .wb-scale-options {
        flex-wrap: wrap;
    }

    .wb-scale-option {
        flex: 0 0 calc(20% - var(--space-xs));
    }

    .wb-scale-number {
        height: 40px;
        font-size: 0.875rem;
    }

    .wb-discount-code {
        font-size: 1.5rem;
    }
}

@media (max-width: 480px) {
    .wb-scale-option {
        flex: 0 0 calc(20% - 4px);
    }

    .wb-scale-number {
        height: 36px;
        font-size: 0.75rem;
    }
}
</style>

<script>
function copyCode(el) {
    const code = el.textContent.trim();
    navigator.clipboard.writeText(code).then(() => {
        const original = el.textContent;
        el.textContent = 'Kopierad!';
        el.style.background = 'var(--color-success)';
        el.style.color = 'white';
        setTimeout(() => {
            el.textContent = original;
            el.style.background = '';
            el.style.color = '';
        }, 1500);
    });
}
</script>
