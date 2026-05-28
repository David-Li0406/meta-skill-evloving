<?php
/**
 * TheHUB - Series Registration Page
 *
 * Mobile-first registration flow for series (season pass) tickets.
 * Displays series info, eligible classes with pricing, and handles checkout.
 *
 * URL: /register/series/{series_id}
 *
 * @since 2026-01-11
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    require_once dirname(dirname(__DIR__)) . '/hub-config.php';
}

require_once HUB_ROOT . '/includes/series-registration.php';

$pdo = hub_db();

// Get series ID from URL
$seriesId = intval($pageInfo['params']['id'] ?? $_GET['series_id'] ?? 0);

if (!$seriesId) {
    include HUB_ROOT . '/pages/404.php';
    return;
}

// Get series details
$stmt = $pdo->prepare("
    SELECT s.*,
           sb.name AS brand_name,
           sb.logo AS brand_logo,
           sb.gradient_start,
           sb.gradient_end,
           sb.accent_color
    FROM series s
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE s.id = ? AND s.active = 1
");
$stmt->execute([$seriesId]);
$series = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$series) {
    include HUB_ROOT . '/pages/404.php';
    return;
}

// Get events in series
$events = getSeriesEventsWithPrices($pdo, $seriesId, 1); // Default class for now
$eventCount = count($events);

// Check registration status
$registrationOpen = true;
$registrationMessage = null;
$now = new DateTime();

if (!($series['allow_series_registration'] ?? false)) {
    $registrationOpen = false;
    $registrationMessage = 'Serieanmälan är inte aktiverad för denna serie';
}

if ($series['registration_opens'] && $registrationOpen) {
    $opens = new DateTime($series['registration_opens']);
    if ($series['registration_opens_time']) {
        $opens = DateTime::createFromFormat('Y-m-d H:i:s', $series['registration_opens'] . ' ' . $series['registration_opens_time']);
    }
    if ($now < $opens) {
        $registrationOpen = false;
        $registrationMessage = 'Anmälan öppnar ' . $opens->format('j M Y');
    }
}

if ($series['registration_closes'] && $registrationOpen) {
    $closes = new DateTime($series['registration_closes']);
    if ($series['registration_closes_time']) {
        $closes = DateTime::createFromFormat('Y-m-d H:i:s', $series['registration_closes'] . ' ' . $series['registration_closes_time']);
    }
    if ($now > $closes) {
        $registrationOpen = false;
        $registrationMessage = 'Anmälan stängde ' . $closes->format('j M Y');
    }
}

// Check if user is logged in
$isLoggedIn = hub_is_logged_in();
$currentUser = $isLoggedIn ? hub_current_user() : null;
$rider = null;
$eligibleClasses = [];
$existingRegistration = null;

if ($isLoggedIn && $currentUser) {
    // Get rider details
    $stmt = $pdo->prepare("
        SELECT r.*, c.name AS club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ");
    $stmt->execute([$currentUser['id']]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    // Check if already registered
    $stmt = $pdo->prepare("
        SELECT * FROM series_registrations
        WHERE rider_id = ? AND series_id = ? AND status != 'cancelled'
    ");
    $stmt->execute([$currentUser['id'], $seriesId]);
    $existingRegistration = $stmt->fetch(PDO::FETCH_ASSOC);

    // Get eligible classes
    if (!$existingRegistration) {
        $eligibleClasses = getEligibleSeriesClasses($pdo, $seriesId, $currentUser['id']);
    }
}

// Get all classes with pricing (for display)
$stmt = $pdo->prepare("
    SELECT c.id, c.name, c.display_name, c.gender, c.min_age, c.max_age
    FROM classes c
    WHERE c.active = 1
    ORDER BY c.sort_order ASC, c.name ASC
");
$stmt->execute();
$allClasses = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Add pricing to each class
foreach ($allClasses as &$class) {
    $pricing = calculateSeriesPrice($pdo, $seriesId, $class['id']);
    $class['price'] = $pricing['final_price'] ?? 0;
    $class['original_price'] = $pricing['base_price'] ?? 0;
    $class['discount'] = $pricing['discount_amount'] ?? 0;
    $class['event_count'] = $pricing['event_count'] ?? $eventCount;
}
unset($class);

// Page setup
$pageInfo = [
    'title' => 'Anmälan - ' . $series['name'],
    'section' => 'register'
];

include HUB_ROOT . '/components/header.php';
?>

<style>
/* Mobile-first series registration styles */
.register-hero {
    background: linear-gradient(135deg,
        <?= $series['gradient_start'] ?? 'var(--color-bg-surface)' ?>,
        <?= $series['gradient_end'] ?? 'var(--color-bg-card)' ?>);
    padding: var(--space-xl) var(--space-md);
    margin: calc(-1 * var(--space-md));
    margin-bottom: var(--space-lg);
    text-align: center;
}

@media (min-width: 768px) {
    .register-hero {
        padding: var(--space-2xl) var(--space-xl);
        border-radius: var(--radius-lg);
        margin: 0 0 var(--space-xl) 0;
    }
}

.register-hero__logo {
    width: 80px;
    height: 80px;
    object-fit: contain;
    margin-bottom: var(--space-md);
}

.register-hero__title {
    font-family: var(--font-heading);
    font-size: 1.75rem;
    color: #fff;
    margin: 0 0 var(--space-xs) 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.register-hero__subtitle {
    color: rgba(255,255,255,0.8);
    font-size: 1rem;
}

.register-hero__badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    background: rgba(255,255,255,0.15);
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    color: #fff;
    margin-top: var(--space-md);
}

/* Price card */
.price-card {
    background: var(--color-bg-card);
    border: 2px solid var(--color-accent);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    text-align: center;
    margin-bottom: var(--space-lg);
}

.price-card__label {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-xs);
}

.price-card__amount {
    font-family: var(--font-heading);
    font-size: 3rem;
    color: var(--color-accent);
    line-height: 1;
}

.price-card__currency {
    font-size: 1.5rem;
    margin-left: var(--space-2xs);
}

.price-card__original {
    font-size: 1rem;
    color: var(--color-text-muted);
    text-decoration: line-through;
    margin-top: var(--space-xs);
}

.price-card__savings {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2xs);
    background: var(--color-success);
    color: #fff;
    padding: var(--space-2xs) var(--space-sm);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    font-weight: 600;
    margin-top: var(--space-sm);
}

/* Class selector */
.class-grid {
    display: grid;
    gap: var(--space-sm);
    margin-bottom: var(--space-lg);
}

.class-option {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    background: var(--color-bg-card);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    cursor: pointer;
    transition: all 0.2s ease;
}

.class-option:hover {
    border-color: var(--color-accent);
}

.class-option.selected {
    border-color: var(--color-accent);
    background: var(--color-accent-light);
}

.class-option.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.class-option__radio {
    width: 24px;
    height: 24px;
    border: 2px solid var(--color-border);
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.class-option.selected .class-option__radio {
    border-color: var(--color-accent);
    background: var(--color-accent);
}

.class-option.selected .class-option__radio::after {
    content: '';
    width: 8px;
    height: 8px;
    background: #fff;
    border-radius: 50%;
}

.class-option__info {
    flex: 1;
    min-width: 0;
}

.class-option__name {
    font-weight: 600;
    color: var(--color-text-primary);
}

.class-option__meta {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.class-option__price {
    text-align: right;
    flex-shrink: 0;
}

.class-option__price-value {
    font-weight: 700;
    color: var(--color-accent);
}

.class-option__price-original {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-decoration: line-through;
}

.class-option__error {
    font-size: 0.75rem;
    color: var(--color-error);
    margin-top: var(--space-2xs);
}

/* Events list */
.events-preview {
    margin-bottom: var(--space-lg);
}

.events-preview__title {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-sm);
}

.event-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) 0;
    border-bottom: 1px solid var(--color-border);
}

.event-item:last-child {
    border-bottom: none;
}

.event-item__date {
    width: 50px;
    text-align: center;
    flex-shrink: 0;
}

.event-item__day {
    font-family: var(--font-heading);
    font-size: 1.25rem;
    color: var(--color-text-primary);
    line-height: 1;
}

.event-item__month {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
}

.event-item__info {
    flex: 1;
    min-width: 0;
}

.event-item__name {
    font-weight: 500;
    color: var(--color-text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.event-item__location {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.event-item__price {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

/* CTA section */
.register-cta {
    position: sticky;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--color-bg-card);
    border-top: 1px solid var(--color-border);
    padding: var(--space-md);
    margin: var(--space-lg) calc(-1 * var(--space-md)) 0;
}

@media (min-width: 768px) {
    .register-cta {
        position: static;
        border-radius: var(--radius-lg);
        margin: var(--space-xl) 0 0 0;
    }
}

.register-cta__button {
    width: 100%;
    padding: var(--space-md) var(--space-lg);
    font-size: 1.125rem;
}

/* Already registered */
.already-registered {
    background: var(--color-accent-light);
    border: 1px solid var(--color-accent);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    text-align: center;
}

.already-registered__icon {
    width: 48px;
    height: 48px;
    color: var(--color-accent);
    margin-bottom: var(--space-md);
}

/* Login prompt */
.login-prompt {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    text-align: center;
}

.login-prompt__icon {
    width: 64px;
    height: 64px;
    color: var(--color-text-muted);
    margin-bottom: var(--space-md);
}
</style>

<main class="main-content">
    <div class="container container--sm">

        <!-- Hero section -->
        <div class="register-hero">
            <?php if ($series['logo'] || $series['brand_logo']): ?>
                <img src="<?= htmlspecialchars($series['logo'] ?: $series['brand_logo']) ?>"
                     alt="<?= htmlspecialchars($series['name']) ?>"
                     class="register-hero__logo">
            <?php endif; ?>
            <h1 class="register-hero__title"><?= htmlspecialchars($series['name']) ?></h1>
            <p class="register-hero__subtitle">Säsong <?= htmlspecialchars($series['year'] ?? date('Y')) ?></p>
            <div class="register-hero__badge">
                <i data-lucide="calendar"></i>
                <?= $eventCount ?> event
            </div>
        </div>

        <?php if ($existingRegistration): ?>
            <!-- Already registered -->
            <div class="already-registered">
                <i data-lucide="check-circle" class="already-registered__icon"></i>
                <h2>Du är redan anmäld!</h2>
                <p class="text-secondary mb-md">
                    Du har redan köpt ett serie-pass för <?= htmlspecialchars($series['name']) ?>.
                </p>
                <a href="/profile/tickets" class="btn btn--primary">
                    <i data-lucide="ticket"></i>
                    Visa mina biljetter
                </a>
            </div>

        <?php elseif (!$registrationOpen): ?>
            <!-- Registration closed -->
            <div class="card">
                <div class="card-body text-center py-xl">
                    <i data-lucide="clock" class="icon-xl text-warning mb-md"></i>
                    <h2>Anmälan stängd</h2>
                    <p class="text-secondary"><?= htmlspecialchars($registrationMessage) ?></p>
                </div>
            </div>

        <?php elseif (!$isLoggedIn): ?>
            <!-- Not logged in -->
            <div class="login-prompt">
                <i data-lucide="user" class="login-prompt__icon"></i>
                <h2>Logga in för att anmäla dig</h2>
                <p class="text-secondary mb-lg">
                    Du behöver ett konto för att köpa ett serie-pass.
                </p>
                <a href="/login?redirect=<?= urlencode($_SERVER['REQUEST_URI']) ?>" class="btn btn--primary btn--lg">
                    <i data-lucide="log-in"></i>
                    Logga in
                </a>
                <p class="text-sm text-muted mt-md">
                    Inget konto? <a href="/rider-register">Skapa konto</a>
                </p>
            </div>

        <?php else: ?>
            <!-- Registration form -->
            <form id="seriesRegistrationForm" method="POST" action="/api/series-registration.php">
                <input type="hidden" name="action" value="register">
                <input type="hidden" name="series_id" value="<?= $seriesId ?>">
                <input type="hidden" name="rider_id" value="<?= $currentUser['id'] ?>">

                <!-- Price card -->
                <div class="price-card" id="priceCard">
                    <div class="price-card__label">Serie-pass</div>
                    <div class="price-card__amount">
                        <span id="finalPrice">-</span>
                        <span class="price-card__currency">kr</span>
                    </div>
                    <div class="price-card__original" id="originalPrice"></div>
                    <div class="price-card__savings" id="savingsAmount" style="display: none;">
                        <i data-lucide="tag"></i>
                        <span>Spara <span id="savingsValue">0</span> kr!</span>
                    </div>
                </div>

                <!-- Class selection -->
                <div class="card mb-lg">
                    <div class="card-header">
                        <h3>Välj klass</h3>
                    </div>
                    <div class="card-body">
                        <p class="text-secondary text-sm mb-md">
                            <strong><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
                            <?php if ($rider['license_type']): ?>
                                &middot; <?= htmlspecialchars($rider['license_type']) ?>
                            <?php endif; ?>
                        </p>

                        <div class="class-grid">
                            <?php foreach ($eligibleClasses as $class): ?>
                                <label class="class-option <?= !$class['eligible'] ? 'disabled' : '' ?>"
                                       data-class-id="<?= $class['id'] ?>"
                                       data-price="<?= $class['price'] ?>"
                                       data-original="<?= $class['original_price'] ?>"
                                       data-discount="<?= $class['discount'] ?>">
                                    <div class="class-option__radio"></div>
                                    <div class="class-option__info">
                                        <div class="class-option__name"><?= htmlspecialchars($class['name']) ?></div>
                                        <div class="class-option__meta">
                                            <?php
                                            $meta = [];
                                            if ($class['gender'] === 'M') $meta[] = 'Herrar';
                                            elseif ($class['gender'] === 'K' || $class['gender'] === 'F') $meta[] = 'Damer';
                                            if ($class['min_age'] || $class['max_age']) {
                                                if ($class['min_age'] && $class['max_age']) {
                                                    $meta[] = $class['min_age'] . '-' . $class['max_age'] . ' år';
                                                } elseif ($class['min_age']) {
                                                    $meta[] = $class['min_age'] . '+ år';
                                                } elseif ($class['max_age']) {
                                                    $meta[] = 'max ' . $class['max_age'] . ' år';
                                                }
                                            }
                                            echo implode(' &middot; ', $meta);
                                            ?>
                                        </div>
                                        <?php if (!$class['eligible'] && !empty($class['errors'])): ?>
                                            <div class="class-option__error">
                                                <?= htmlspecialchars($class['errors'][0]) ?>
                                            </div>
                                        <?php endif; ?>
                                    </div>
                                    <div class="class-option__price">
                                        <?php if ($class['eligible']): ?>
                                            <div class="class-option__price-value"><?= number_format($class['price'], 0, ',', ' ') ?> kr</div>
                                            <?php if ($class['discount'] > 0): ?>
                                                <div class="class-option__price-original"><?= number_format($class['original_price'], 0, ',', ' ') ?> kr</div>
                                            <?php endif; ?>
                                        <?php else: ?>
                                            <div class="class-option__price-value text-muted">-</div>
                                        <?php endif; ?>
                                    </div>
                                    <?php if ($class['eligible']): ?>
                                        <input type="radio" name="class_id" value="<?= $class['id'] ?>" style="display: none;">
                                    <?php endif; ?>
                                </label>
                            <?php endforeach; ?>
                        </div>
                    </div>
                </div>

                <!-- Events preview -->
                <div class="events-preview">
                    <div class="events-preview__title">
                        <i data-lucide="calendar"></i>
                        Ingående event
                    </div>
                    <?php foreach ($events as $event): ?>
                        <?php
                        $date = new DateTime($event['date']);
                        $months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'];
                        ?>
                        <div class="event-item">
                            <div class="event-item__date">
                                <div class="event-item__day"><?= $date->format('j') ?></div>
                                <div class="event-item__month"><?= $months[$date->format('n')-1] ?></div>
                            </div>
                            <div class="event-item__info">
                                <div class="event-item__name"><?= htmlspecialchars($event['name']) ?></div>
                                <div class="event-item__location">
                                    <i data-lucide="map-pin" style="width: 12px; height: 12px;"></i>
                                    <?= htmlspecialchars($event['city'] ?: $event['location']) ?>
                                </div>
                            </div>
                            <div class="event-item__price">
                                <?= number_format($event['price'], 0, ',', ' ') ?> kr
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <!-- CTA -->
                <div class="register-cta">
                    <button type="submit" class="btn btn--primary register-cta__button" id="submitBtn" disabled>
                        <i data-lucide="ticket"></i>
                        <span>Välj en klass</span>
                    </button>
                </div>
            </form>
        <?php endif; ?>

    </div>
</main>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('seriesRegistrationForm');
    if (!form) return;

    const classOptions = document.querySelectorAll('.class-option:not(.disabled)');
    const priceEl = document.getElementById('finalPrice');
    const originalEl = document.getElementById('originalPrice');
    const savingsEl = document.getElementById('savingsAmount');
    const savingsValueEl = document.getElementById('savingsValue');
    const submitBtn = document.getElementById('submitBtn');

    let selectedClassId = null;

    classOptions.forEach(option => {
        option.addEventListener('click', function() {
            if (this.classList.contains('disabled')) return;

            // Deselect all
            classOptions.forEach(o => o.classList.remove('selected'));

            // Select this one
            this.classList.add('selected');
            const radio = this.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;

            selectedClassId = this.dataset.classId;

            // Update price display
            const price = parseFloat(this.dataset.price);
            const original = parseFloat(this.dataset.original);
            const discount = parseFloat(this.dataset.discount);

            priceEl.textContent = formatNumber(price);

            if (discount > 0) {
                originalEl.textContent = formatNumber(original) + ' kr';
                originalEl.style.display = 'block';
                savingsValueEl.textContent = formatNumber(discount);
                savingsEl.style.display = 'inline-flex';
            } else {
                originalEl.style.display = 'none';
                savingsEl.style.display = 'none';
            }

            // Enable submit
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = 'Fortsätt till betalning';
        });
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        if (!selectedClassId) {
            alert('Välj en klass först');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.querySelector('span').textContent = 'Bearbetar...';

        try {
            const response = await fetch('/api/series-registration.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'register',
                    series_id: <?= $seriesId ?>,
                    rider_id: <?= $currentUser['id'] ?? 0 ?>,
                    class_id: selectedClassId
                })
            });

            const data = await response.json();

            if (data.success) {
                // Redirect to checkout
                window.location.href = data.checkout_url || '/checkout.php?type=series&id=' + data.registration_id;
            } else {
                alert('Fel: ' + (data.errors?.join(', ') || data.error || 'Okänt fel'));
                submitBtn.disabled = false;
                submitBtn.querySelector('span').textContent = 'Fortsätt till betalning';
            }
        } catch (error) {
            alert('Ett fel uppstod. Försök igen.');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = 'Fortsätt till betalning';
        }
    });

    function formatNumber(num) {
        return Math.round(num).toLocaleString('sv-SE');
    }
});
</script>

<?php include HUB_ROOT . '/components/footer.php'; ?>
