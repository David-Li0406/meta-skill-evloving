<?php
/**
 * TheHUB Checkout Page
 *
 * Displays payment options for event registrations:
 * - Swish (direct link on mobile, QR on desktop)
 * - Card via WooCommerce (fallback)
 * - Discount codes and Gravity ID discounts
 */

require_once __DIR__ . '/../hub-config.php';
require_once __DIR__ . '/../includes/payment.php';

// Get order ID from URL
$orderId = isset($_GET['order']) ? intval($_GET['order']) : 0;

// Or create order from registration IDs (event registrations)
$registrationIds = isset($_GET['registration']) ? explode(',', $_GET['registration']) : [];
$registrationIds = array_filter(array_map('intval', $registrationIds));

// Or handle series registration
$seriesRegistrationId = isset($_GET['type']) && $_GET['type'] === 'series' ? intval($_GET['id'] ?? 0) : 0;

// Discount code from form
$discountCode = isset($_POST['discount_code']) ? trim($_POST['discount_code']) : null;
$discountCode = $discountCode ?: (isset($_GET['discount_code']) ? trim($_GET['discount_code']) : null);

$order = null;
$error = null;
$appliedDiscounts = [];
$gravityIdInfo = null;
$isSeries = false;
$seriesInfo = null;

try {
    if ($orderId) {
        // Load existing order
        $order = getOrder($orderId);
        if (!$order) {
            $error = 'Order hittades inte.';
        }
    } elseif ($seriesRegistrationId) {
        // Handle series registration checkout
        if (!hub_is_logged_in()) {
            header('Location: /login?redirect=' . urlencode($_SERVER['REQUEST_URI']));
            exit;
        }

        $currentUser = hub_current_user();
        $pdo = hub_db();

        // Get series registration
        $stmt = $pdo->prepare("
            SELECT sr.*, s.name as series_name, s.logo as series_logo,
                   c.name as class_name, c.display_name as class_display_name
            FROM series_registrations sr
            JOIN series s ON sr.series_id = s.id
            JOIN classes c ON sr.class_id = c.id
            WHERE sr.id = ?
        ");
        $stmt->execute([$seriesRegistrationId]);
        $seriesReg = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$seriesReg) {
            $error = 'Serie-registrering hittades inte.';
        } elseif ($seriesReg['rider_id'] !== $currentUser['id'] &&
                  !hub_is_parent_of($currentUser['id'], $seriesReg['rider_id'])) {
            $error = 'Du har inte behörighet att betala för denna registrering.';
        } else {
            $isSeries = true;
            $seriesInfo = $seriesReg;

            // Check if order already exists
            if (!empty($seriesReg['order_id'])) {
                $order = getOrder($seriesReg['order_id']);
            }

            if (!$order) {
                // Create new series order
                $orderData = createSeriesOrder($seriesRegistrationId, $seriesReg['rider_id']);
                $order = getOrder($orderData['order_id']);

                // Add payment URLs to order
                $order['swish_url'] = $orderData['swish_url'];
                $order['swish_qr'] = $orderData['swish_qr'];
                $order['swish_available'] = $orderData['swish_available'];
                $order['card_available'] = $orderData['card_available'];
            }
        }
    } elseif (!empty($registrationIds)) {
        // Check user is logged in
        if (!hub_is_logged_in()) {
            header('Location: /login?redirect=' . urlencode($_SERVER['REQUEST_URI']));
            exit;
        }

        $currentUser = hub_current_user();

        // Verify user owns these registrations
        $pdo = hub_db();
        $placeholders = implode(',', array_fill(0, count($registrationIds), '?'));
        $stmt = $pdo->prepare("
            SELECT er.*, e.id as event_id
            FROM event_registrations er
            JOIN events e ON er.event_id = e.id
            WHERE er.id IN ({$placeholders})
        ");
        $stmt->execute($registrationIds);
        $registrations = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($registrations)) {
            $error = 'Inga giltiga registreringar hittades.';
        } else {
            // Verify ownership
            foreach ($registrations as $reg) {
                if ($reg['rider_id'] !== $currentUser['id'] &&
                    !hub_is_parent_of($currentUser['id'], $reg['rider_id'])) {
                    $error = 'Du har inte behörighet att betala för dessa registreringar.';
                    break;
                }
            }

            if (!$error) {
                $eventId = $registrations[0]['event_id'];

                // Check for Gravity ID (for display before order creation)
                $gravityIdInfo = checkGravityIdDiscount($currentUser['id'], $eventId);

                // Check if order already exists
                $stmt = $pdo->prepare("
                    SELECT order_id FROM event_registrations
                    WHERE id = ? AND order_id IS NOT NULL
                ");
                $stmt->execute([$registrationIds[0]]);
                $existingOrderId = $stmt->fetchColumn();

                if ($existingOrderId) {
                    // Use existing order
                    $order = getOrder($existingOrderId);
                } else {
                    // Create new order with discount code
                    $orderData = createOrder($registrationIds, $currentUser['id'], $eventId, $discountCode);
                    $order = getOrder($orderData['order_id']);
                    $appliedDiscounts = $orderData['applied_discounts'] ?? [];

                    // Add payment URLs to order
                    $order['swish_url'] = $orderData['swish_url'];
                    $order['swish_qr'] = $orderData['swish_qr'];
                    $order['swish_available'] = $orderData['swish_available'];
                    $order['card_available'] = $orderData['card_available'];
                    $order['applied_discounts'] = $appliedDiscounts;
                }
            }
        }
    } else {
        $error = 'Ingen order eller registrering angiven.';
    }

    // If order exists but doesn't have swish URLs, generate them
    if ($order && empty($order['swish_url']) && !empty($order['swish_number'])) {
        $order['swish_url'] = generateSwishUrl(
            $order['swish_number'],
            $order['total_amount'],
            $order['swish_message']
        );
        $order['swish_qr'] = generateSwishQR(
            $order['swish_number'],
            $order['total_amount'],
            $order['swish_message']
        );
        $order['swish_available'] = true;
    }

} catch (Exception $e) {
    $error = 'Ett fel uppstod: ' . $e->getMessage();
}

// Page setup
$pageInfo = [
    'title' => 'Betalning',
    'section' => 'checkout'
];

include __DIR__ . '/../components/header.php';
?>

<main class="main-content">
    <div class="container container--sm">
        <?php if ($error): ?>
            <div class="card">
                <div class="card-body text-center py-xl">
                    <i data-lucide="alert-circle" class="icon-xl text-error mb-md"></i>
                    <h1 class="text-xl mb-sm">Ett fel uppstod</h1>
                    <p class="text-secondary mb-lg"><?= htmlspecialchars($error) ?></p>
                    <a href="/calendar" class="btn btn--primary">
                        <i data-lucide="calendar"></i>
                        Till kalendern
                    </a>
                </div>
            </div>

        <?php elseif ($order && $order['payment_status'] === 'paid'): ?>
            <!-- Already paid -->
            <div class="card">
                <div class="card-body text-center py-xl">
                    <i data-lucide="check-circle" class="icon-xl text-success mb-md"></i>
                    <h1 class="text-xl mb-sm">Betalning genomförd!</h1>
                    <p class="text-secondary mb-lg">
                        Order <strong><?= htmlspecialchars($order['order_number']) ?></strong> är betald.
                    </p>
                    <a href="/profile/registrations" class="btn btn--primary">
                        <i data-lucide="ticket"></i>
                        Mina anmälningar
                    </a>
                </div>
            </div>

        <?php elseif ($order): ?>
            <!-- Order summary -->
            <div class="card mb-lg">
                <div class="card-header">
                    <h1 class="text-lg">
                        <i data-lucide="shopping-cart"></i>
                        Betalning
                    </h1>
                </div>
                <div class="card-body">
                    <!-- Series info (for series registration) -->
                    <?php if ($isSeries && $seriesInfo): ?>
                    <div class="mb-md pb-md border-bottom">
                        <div class="flex items-center gap-md">
                            <?php if (!empty($seriesInfo['series_logo'])): ?>
                            <img src="<?= htmlspecialchars($seriesInfo['series_logo']) ?>" alt="" style="width:48px;height:48px;object-fit:contain;">
                            <?php endif; ?>
                            <div>
                                <div class="text-sm text-secondary">Serie-pass</div>
                                <div class="font-medium"><?= htmlspecialchars($seriesInfo['series_name']) ?></div>
                                <div class="text-sm text-secondary">
                                    <?= htmlspecialchars($seriesInfo['class_display_name'] ?: $seriesInfo['class_name']) ?>
                                </div>
                            </div>
                        </div>
                    </div>
                    <?php elseif (!empty($order['event_name'])): ?>
                    <!-- Event info -->
                    <div class="mb-md pb-md border-bottom">
                        <div class="text-sm text-secondary">Event</div>
                        <div class="font-medium"><?= htmlspecialchars($order['event_name']) ?></div>
                        <div class="text-sm text-secondary">
                            <?= date('j M Y', strtotime($order['event_date'])) ?>
                        </div>
                    </div>
                    <?php endif; ?>

                    <!-- Order items -->
                    <div class="mb-md">
                        <div class="text-sm text-secondary mb-sm">Anmälningar</div>
                        <?php foreach ($order['items'] as $item): ?>
                        <div class="flex justify-between items-center py-sm">
                            <span><?= htmlspecialchars($item['description']) ?></span>
                            <span class="font-medium"><?= number_format($item['total_price'], 0) ?> kr</span>
                        </div>
                        <?php endforeach; ?>
                    </div>

                    <!-- Subtotal -->
                    <div class="flex justify-between items-center py-sm border-top">
                        <span>Delsumma</span>
                        <span class="font-medium"><?= number_format($order['subtotal'], 0) ?> kr</span>
                    </div>

                    <!-- Applied discounts -->
                    <?php if (!empty($order['applied_discounts']) || !empty($appliedDiscounts)): ?>
                        <?php $discounts = !empty($order['applied_discounts']) ? $order['applied_discounts'] : $appliedDiscounts; ?>
                        <?php foreach ($discounts as $discount): ?>
                        <div class="flex justify-between items-center py-sm text-success">
                            <span>
                                <i data-lucide="<?= $discount['type'] === 'gravity_id' ? 'badge-check' : 'tag' ?>" class="icon-sm"></i>
                                <?= htmlspecialchars($discount['label']) ?>
                            </span>
                            <span class="font-medium">-<?= number_format($discount['amount'], 0) ?> kr</span>
                        </div>
                        <?php endforeach; ?>
                    <?php elseif ($order['discount'] > 0): ?>
                        <div class="flex justify-between items-center py-sm text-success">
                            <span>
                                <i data-lucide="tag" class="icon-sm"></i>
                                Rabatt
                            </span>
                            <span class="font-medium">-<?= number_format($order['discount'], 0) ?> kr</span>
                        </div>
                    <?php endif; ?>

                    <!-- Show Gravity ID badge if applicable but no discount yet applied -->
                    <?php if ($gravityIdInfo && $gravityIdInfo['has_gravity_id'] && empty($appliedDiscounts)): ?>
                    <div class="flex justify-between items-center py-sm text-success">
                        <span>
                            <i data-lucide="badge-check" class="icon-sm"></i>
                            Gravity ID: <?= htmlspecialchars($gravityIdInfo['gravity_id']) ?>
                        </span>
                        <span class="font-medium">-<?= number_format($gravityIdInfo['discount'], 0) ?> kr</span>
                    </div>
                    <?php endif; ?>

                    <!-- Total -->
                    <div class="flex justify-between items-center pt-md border-top">
                        <span class="font-semibold">Att betala</span>
                        <span class="text-xl font-bold"><?= number_format($order['total_amount'], 0) ?> kr</span>
                    </div>

                    <!-- Order reference -->
                    <div class="mt-md pt-md border-top text-sm text-secondary">
                        Order: <strong><?= htmlspecialchars($order['order_number']) ?></strong>
                    </div>
                </div>
            </div>

            <!-- Discount code input (if order not yet paid) -->
            <?php if ($order['payment_status'] !== 'paid' && empty($order['discount_code_id'])): ?>
            <div class="card mb-lg">
                <div class="card-header">
                    <h2 class="text-lg">
                        <i data-lucide="tag"></i>
                        Rabattkod
                    </h2>
                </div>
                <div class="card-body">
                    <form method="GET" action="/checkout" id="discount-form" class="flex gap-sm">
                        <input type="hidden" name="order" value="<?= $order['id'] ?>">
                        <input type="text"
                               name="discount_code"
                               id="discount-code-input"
                               placeholder="Ange rabattkod"
                               class="form-input flex-1"
                               value="<?= htmlspecialchars($discountCode ?? '') ?>"
                               style="text-transform: uppercase;">
                        <button type="submit" class="btn btn--secondary" id="apply-discount-btn">
                            <i data-lucide="check"></i>
                            Använd
                        </button>
                    </form>
                    <div id="discount-message" class="mt-sm text-sm" style="display: none;"></div>
                </div>
            </div>
            <?php endif; ?>

            <!-- Payment options -->
            <div class="card">
                <div class="card-header">
                    <h2 class="text-lg">
                        <i data-lucide="credit-card"></i>
                        Välj betalningsmetod
                    </h2>
                </div>
                <div class="card-body">
                    <?php if (!empty($order['swish_available'])): ?>
                    <!-- Swish payment -->
                    <div class="payment-option payment-option--swish mb-lg">
                        <div class="flex items-center gap-md mb-md">
                            <img src="/assets/images/swish-logo.svg" alt="Swish" class="payment-logo" onerror="this.style.display='none'">
                            <div>
                                <h3 class="font-medium">Betala med Swish</h3>
                                <p class="text-sm text-secondary">Direkt betalning till arrangören</p>
                            </div>
                        </div>

                        <!-- Mobile: Swish link button -->
                        <div class="swish-mobile mb-md">
                            <a href="<?= htmlspecialchars($order['swish_url']) ?>"
                               class="btn btn--swish btn--lg w-full"
                               id="swish-button">
                                <i data-lucide="smartphone"></i>
                                Öppna Swish - <?= number_format($order['total_amount'], 0) ?> kr
                            </a>
                        </div>

                        <!-- Desktop: QR code -->
                        <div class="swish-desktop text-center">
                            <p class="text-sm text-secondary mb-md">Scanna QR-koden med Swish-appen</p>
                            <div class="swish-qr-container">
                                <img src="<?= htmlspecialchars($order['swish_qr']) ?>"
                                     alt="Swish QR-kod"
                                     class="swish-qr"
                                     width="200"
                                     height="200">
                            </div>
                        </div>

                        <!-- Payment details -->
                        <div class="swish-details mt-md p-md bg-muted rounded-md">
                            <div class="grid grid-cols-2 gap-sm text-sm">
                                <div>
                                    <span class="text-secondary">Mottagare:</span><br>
                                    <strong><?= htmlspecialchars($order['swish_name'] ?? formatSwishNumber($order['swish_number'])) ?></strong>
                                </div>
                                <div>
                                    <span class="text-secondary">Swish-nummer:</span><br>
                                    <strong><?= formatSwishNumber($order['swish_number']) ?></strong>
                                </div>
                                <div>
                                    <span class="text-secondary">Belopp:</span><br>
                                    <strong><?= number_format($order['total_amount'], 0) ?> kr</strong>
                                </div>
                                <div>
                                    <span class="text-secondary">Meddelande:</span><br>
                                    <strong><?= htmlspecialchars($order['swish_message']) ?></strong>
                                </div>
                            </div>
                        </div>

                        <div class="mt-md p-md bg-warning-subtle rounded-md text-sm">
                            <i data-lucide="info" class="icon-sm"></i>
                            <strong>Viktigt:</strong> Ange meddelandet <strong><?= htmlspecialchars($order['swish_message']) ?></strong>
                            så vi kan koppla betalningen till din anmälan.
                        </div>
                    </div>
                    <?php endif; ?>

                    <?php if (!empty($order['card_available'])): ?>
                    <!-- Card payment via WooCommerce -->
                    <div class="payment-option payment-option--card">
                        <div class="flex items-center gap-md mb-md">
                            <i data-lucide="credit-card" class="icon-lg"></i>
                            <div>
                                <h3 class="font-medium">Betala med kort</h3>
                                <p class="text-sm text-secondary">Visa, Mastercard, etc.</p>
                            </div>
                        </div>
                        <button type="button"
                                class="btn btn--secondary btn--lg w-full"
                                onclick="WooCommerce.openCheckout('<?= WC_CHECKOUT_URL ?>?order=<?= $order['id'] ?>')">
                            <i data-lucide="external-link"></i>
                            Betala med kort
                        </button>
                    </div>
                    <?php endif; ?>
                </div>
            </div>

            <!-- Payment confirmation info -->
            <div class="card mt-lg">
                <div class="card-body">
                    <h3 class="font-medium mb-sm">
                        <i data-lucide="clock"></i>
                        Efter betalning
                    </h3>
                    <p class="text-sm text-secondary">
                        Din anmälan bekräftas automatiskt när betalningen är genomförd.
                        Du får ett bekräftelsemail till <strong><?= htmlspecialchars($order['customer_email']) ?></strong>.
                    </p>
                    <p class="text-sm text-secondary mt-sm">
                        Swish-betalningar bekräftas vanligtvis inom några minuter.
                        Har du frågor? Kontakta arrangören.
                    </p>
                </div>
            </div>
        <?php endif; ?>
    </div>
</main>

<script>
// Discount code AJAX handling
document.addEventListener('DOMContentLoaded', function() {
    const discountForm = document.getElementById('discount-form');
    const discountInput = document.getElementById('discount-code-input');
    const discountMessage = document.getElementById('discount-message');
    const applyBtn = document.getElementById('apply-discount-btn');

    if (discountForm) {
        discountForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const code = discountInput.value.trim().toUpperCase();
            if (!code) {
                showMessage('Ange en rabattkod', 'error');
                return;
            }

            // Disable button while processing
            applyBtn.disabled = true;
            applyBtn.innerHTML = '<i data-lucide="loader" class="spin"></i> Kontrollerar...';
            lucide.createIcons();

            try {
                const formData = new FormData();
                formData.append('order_id', '<?= $order['id'] ?? 0 ?>');
                formData.append('code', code);

                const response = await fetch('/api/apply-discount.php', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    showMessage('Rabattkod tillämpad! Du sparade ' + data.discount_amount + ' kr', 'success');

                    // Reload page to show updated totals
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    showMessage(data.error || 'Ogiltig rabattkod', 'error');
                }
            } catch (error) {
                showMessage('Något gick fel. Försök igen.', 'error');
            }

            applyBtn.disabled = false;
            applyBtn.innerHTML = '<i data-lucide="check"></i> Använd';
            lucide.createIcons();
        });
    }

    function showMessage(text, type) {
        discountMessage.textContent = text;
        discountMessage.className = 'mt-sm text-sm ' + (type === 'success' ? 'text-success' : 'text-error');
        discountMessage.style.display = 'block';
    }
});
</script>

<?php include __DIR__ . '/../components/footer.php'; ?>
