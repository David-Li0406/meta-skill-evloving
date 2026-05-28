<?php
/**
 * TheHUB V1.0 - Payment Functions
 *
 * Handles payment configuration, Swish links/QR, and order management.
 * Supports flexible payment config hierarchy: event > series > promotor > fallback
 */

require_once __DIR__ . '/../config.php';

// ============================================================================
// PAYMENT CONFIGURATION
// ============================================================================

/**
 * Get payment configuration for an event
 * Checks in order:
 * 1. Event's payment_recipient_id (new system)
 * 2. Series' payment_recipient_id (new system)
 * 3. Event-specific payment_configs (legacy)
 * 4. Series payment_configs (legacy)
 * 5. Promotor config (legacy)
 * 6. WooCommerce fallback
 *
 * @param int $eventId Event ID
 * @return array|null Payment config or null for WooCommerce fallback
 */
function getPaymentConfig(int $eventId): ?array {
    $pdo = hub_db();

    // Check if payment_recipients table exists (new system)
    $newSystemAvailable = false;
    try {
        $check = $pdo->query("SHOW TABLES LIKE 'payment_recipients'");
        $newSystemAvailable = $check->rowCount() > 0;
    } catch (Exception $e) {}

    if ($newSystemAvailable) {
        // 1. Check event's own payment_recipient_id
        try {
            $stmt = $pdo->prepare("
                SELECT pr.*, 'event_recipient' as config_source, e.name as source_name, 1 as swish_enabled
                FROM events e
                JOIN payment_recipients pr ON e.payment_recipient_id = pr.id
                WHERE e.id = ? AND pr.active = 1
            ");
            $stmt->execute([$eventId]);
            if ($config = $stmt->fetch(PDO::FETCH_ASSOC)) {
                return $config;
            }
        } catch (Exception $e) {}

        // 2. Check series' payment_recipient_id (if event has no recipient but belongs to series)
        try {
            $stmt = $pdo->prepare("
                SELECT pr.*, 'series_recipient' as config_source, s.name as source_name, 1 as swish_enabled
                FROM events e
                JOIN series s ON e.series_id = s.id
                JOIN payment_recipients pr ON s.payment_recipient_id = pr.id
                WHERE e.id = ? AND pr.active = 1 AND (e.payment_recipient_id IS NULL)
            ");
            $stmt->execute([$eventId]);
            if ($config = $stmt->fetch(PDO::FETCH_ASSOC)) {
                return $config;
            }
        } catch (Exception $e) {}
    }

    // Legacy system fallback (payment_configs table)

    // 3. Check event-specific config
    $stmt = $pdo->prepare("
        SELECT pc.*, 'event' as config_source
        FROM payment_configs pc
        WHERE pc.event_id = ?
    ");
    $stmt->execute([$eventId]);
    if ($config = $stmt->fetch(PDO::FETCH_ASSOC)) {
        return $config;
    }

    // 4. Check series config (if event belongs to a series)
    $stmt = $pdo->prepare("
        SELECT pc.*, 'series' as config_source, s.name as source_name
        FROM payment_configs pc
        JOIN series s ON s.id = pc.series_id
        JOIN events e ON e.series_id = s.id
        WHERE e.id = ?
    ");
    $stmt->execute([$eventId]);
    if ($config = $stmt->fetch(PDO::FETCH_ASSOC)) {
        return $config;
    }

    // 5. Check promotor config (user assigned to this event)
    $stmt = $pdo->prepare("
        SELECT pc.*, 'promotor' as config_source, au.full_name as source_name
        FROM payment_configs pc
        JOIN admin_users au ON au.id = pc.promotor_user_id
        JOIN promotor_events pe ON pe.user_id = au.id
        WHERE pe.event_id = ? AND pc.swish_enabled = 1
        LIMIT 1
    ");
    $stmt->execute([$eventId]);
    if ($config = $stmt->fetch(PDO::FETCH_ASSOC)) {
        return $config;
    }

    // 6. Check if any promotor for this event has swish directly on their profile
    $stmt = $pdo->prepare("
        SELECT au.swish_number, au.swish_name, au.full_name as source_name,
               'promotor_direct' as config_source, 1 as swish_enabled
        FROM admin_users au
        JOIN promotor_events pe ON pe.user_id = au.id
        WHERE pe.event_id = ? AND au.swish_number IS NOT NULL
        LIMIT 1
    ");
    $stmt->execute([$eventId]);
    if ($config = $stmt->fetch(PDO::FETCH_ASSOC)) {
        return $config;
    }

    // 7. No config found - use WooCommerce fallback
    return null;
}

/**
 * Check if Swish is available for an event
 */
function isSwishAvailable(int $eventId): bool {
    $config = getPaymentConfig($eventId);
    return $config !== null && !empty($config['swish_number']) && $config['swish_enabled'];
}

/**
 * Check if card payment is available for an event
 */
function isCardAvailable(int $eventId): bool {
    $config = getPaymentConfig($eventId);
    // Card is available via WooCommerce (fallback) or if explicitly enabled
    return $config === null || !empty($config['card_enabled']);
}

// ============================================================================
// SWISH LINK & QR GENERATION
// ============================================================================

/**
 * Generate Swish payment URL (opens Swish app on mobile)
 *
 * @param string $recipientNumber Swish number (with or without dashes)
 * @param float $amount Amount in SEK
 * @param string $message Payment reference/message (max 50 chars)
 * @return string Swish URL
 */
function generateSwishUrl(string $recipientNumber, float $amount, string $message = ''): string {
    // Clean phone number (remove spaces, dashes)
    $cleanNumber = preg_replace('/[^0-9]/', '', $recipientNumber);

    // Ensure it starts with 46 (Swedish country code) if it starts with 0
    if (substr($cleanNumber, 0, 1) === '0') {
        $cleanNumber = '46' . substr($cleanNumber, 1);
    }

    // Truncate message to 50 chars (Swish limit)
    $message = mb_substr($message, 0, 50);

    // Build Swish URL
    // Format: https://app.swish.nu/1/p/sw/?sw=PHONE&amt=AMOUNT&msg=MESSAGE
    $params = [
        'sw' => $cleanNumber,
        'amt' => number_format($amount, 0, '', ''),
        'msg' => $message
    ];

    return 'https://app.swish.nu/1/p/sw/?' . http_build_query($params);
}

/**
 * Generate Swish QR code data URL
 * Uses the Swish QR format for scanning with Swish app
 *
 * @param string $recipientNumber Swish number
 * @param float $amount Amount in SEK
 * @param string $message Payment reference
 * @param int $size QR code size in pixels
 * @return string Data URL for QR code image (SVG)
 */
function generateSwishQR(string $recipientNumber, float $amount, string $message = '', int $size = 200): string {
    // Clean phone number
    $cleanNumber = preg_replace('/[^0-9]/', '', $recipientNumber);
    if (substr($cleanNumber, 0, 1) === '0') {
        $cleanNumber = '46' . substr($cleanNumber, 1);
    }

    // Swish QR payload format
    // C = Create payment, phone number, amount (in öre), message
    $amountOre = (int)($amount * 100);
    $message = mb_substr($message, 0, 50);

    $payload = "C{$cleanNumber};{$amountOre};{$message}";

    // Use Google Charts API for QR generation (simple approach)
    // In production, consider using a PHP QR library like endroid/qr-code
    $qrUrl = 'https://chart.googleapis.com/chart?' . http_build_query([
        'cht' => 'qr',
        'chs' => "{$size}x{$size}",
        'chl' => $payload,
        'choe' => 'UTF-8'
    ]);

    return $qrUrl;
}

/**
 * Format Swish number for display
 */
function formatSwishNumber(string $number): string {
    $clean = preg_replace('/[^0-9]/', '', $number);

    // Mobile number format: 070-123 45 67
    if (strlen($clean) === 10 && substr($clean, 0, 1) === '0') {
        return substr($clean, 0, 3) . '-' .
               substr($clean, 3, 3) . ' ' .
               substr($clean, 6, 2) . ' ' .
               substr($clean, 8, 2);
    }

    // Company number format: 123-XXX XX XX
    if (strlen($clean) >= 7) {
        return substr($clean, 0, 3) . '-' .
               substr($clean, 3, 3) . ' ' .
               substr($clean, 6, 2) . ' ' .
               substr($clean, 8);
    }

    return $number;
}

// ============================================================================
// ORDER MANAGEMENT
// ============================================================================

/**
 * Generate unique order number
 * Format: ORD-YYYY-NNNNNN
 */
function generateOrderNumber(): string {
    $pdo = hub_db();
    $year = date('Y');

    // Get next sequence number for this year
    $stmt = $pdo->prepare("
        SELECT COUNT(*) + 1 as next_num
        FROM orders
        WHERE order_number LIKE ?
    ");
    $stmt->execute(["ORD-{$year}-%"]);
    $nextNum = $stmt->fetchColumn();

    return sprintf("ORD-%s-%06d", $year, $nextNum);
}

/**
 * Create a new order from registrations
 *
 * @param array $registrationIds Array of registration IDs
 * @param int $riderId Rider making the purchase
 * @param int $eventId Event ID
 * @param string|null $discountCode Optional discount code
 * @return array Order data with order_id and payment info
 */
function createOrder(array $registrationIds, int $riderId, int $eventId, ?string $discountCode = null): array {
    $pdo = hub_db();

    // Get rider info
    $stmt = $pdo->prepare("SELECT firstname, lastname, email FROM riders WHERE id = ?");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        throw new Exception('Rider not found');
    }

    // Get payment config for this event
    $paymentConfig = getPaymentConfig($eventId);

    // Get registrations with pricing
    $placeholders = implode(',', array_fill(0, count($registrationIds), '?'));
    $stmt = $pdo->prepare("
        SELECT er.id, er.first_name, er.last_name, er.category,
               COALESCE(epr.base_price, 0) as price
        FROM event_registrations er
        LEFT JOIN classes c ON c.name = er.category
        LEFT JOIN event_pricing_rules epr ON epr.event_id = er.event_id AND epr.class_id = c.id
        WHERE er.id IN ({$placeholders})
    ");
    $stmt->execute($registrationIds);
    $registrations = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Calculate subtotal
    $subtotal = array_sum(array_column($registrations, 'price'));

    // Initialize discount tracking
    $discountCodeId = null;
    $discountCodeAmount = 0;
    $gravityIdAmount = 0;
    $appliedDiscounts = [];

    // Check for Gravity ID discount
    $gravityCheck = checkGravityIdDiscount($riderId, $eventId);
    if ($gravityCheck['has_gravity_id'] && $gravityCheck['discount'] > 0) {
        $gravityIdAmount = $gravityCheck['discount'];
        $appliedDiscounts[] = [
            'type' => 'gravity_id',
            'label' => 'Gravity ID-rabatt',
            'amount' => $gravityIdAmount,
            'gravity_id' => $gravityCheck['gravity_id']
        ];
    }

    // Validate and apply discount code (if provided)
    if ($discountCode) {
        $codeValidation = validateDiscountCode($discountCode, $eventId, $riderId, $subtotal);
        if ($codeValidation['valid']) {
            $discountCodeId = $codeValidation['discount']['id'];
            $discountCodeAmount = calculateDiscountAmount($codeValidation['discount'], $subtotal);
            $appliedDiscounts[] = [
                'type' => 'discount_code',
                'label' => 'Rabattkod: ' . $codeValidation['discount']['code'],
                'amount' => $discountCodeAmount,
                'code' => $codeValidation['discount']['code']
            ];
        }
    }

    // Calculate total discount and final amount
    $totalDiscount = $discountCodeAmount + $gravityIdAmount;
    $total = max(0, $subtotal - $totalDiscount);

    // Generate order number and Swish message
    $orderNumber = generateOrderNumber();
    $swishMessage = substr($orderNumber, 4); // Remove "ORD-" prefix for shorter message

    $pdo->beginTransaction();

    try {
        // Create order with discount information
        $stmt = $pdo->prepare("
            INSERT INTO orders (
                order_number, rider_id, customer_email, customer_name,
                event_id, subtotal, discount, total_amount, currency,
                payment_method, payment_status,
                discount_code_id, gravity_id_discount,
                swish_number, swish_message,
                expires_at, created_at
            ) VALUES (
                ?, ?, ?, ?,
                ?, ?, ?, ?, 'SEK',
                'swish', 'pending',
                ?, ?,
                ?, ?,
                DATE_ADD(NOW(), INTERVAL 24 HOUR), NOW()
            )
        ");
        $stmt->execute([
            $orderNumber,
            $riderId,
            $rider['email'],
            $rider['firstname'] . ' ' . $rider['lastname'],
            $eventId,
            $subtotal,
            $totalDiscount,
            $total,
            $discountCodeId,
            $gravityIdAmount > 0 ? $gravityIdAmount : null,
            $paymentConfig['swish_number'] ?? null,
            $swishMessage
        ]);

        $orderId = $pdo->lastInsertId();

        // Create order items
        foreach ($registrations as $reg) {
            $stmt = $pdo->prepare("
                INSERT INTO order_items (
                    order_id, item_type, registration_id,
                    description, unit_price, quantity, total_price
                ) VALUES (?, 'registration', ?, ?, ?, 1, ?)
            ");

            $description = $reg['first_name'] . ' ' . $reg['last_name'] . ' - ' . $reg['category'];
            $stmt->execute([
                $orderId,
                $reg['id'],
                $description,
                $reg['price'],
                $reg['price']
            ]);
        }

        // Update registrations with order_id
        $stmt = $pdo->prepare("
            UPDATE event_registrations
            SET order_id = ?
            WHERE id IN ({$placeholders})
        ");
        $stmt->execute(array_merge([$orderId], $registrationIds));

        // Record discount code usage if applicable
        if ($discountCodeId && $discountCodeAmount > 0) {
            recordDiscountUsage($discountCodeId, $orderId, $riderId, $discountCodeAmount);
        }

        $pdo->commit();

        // Generate payment links
        $swishUrl = null;
        $swishQR = null;

        if ($paymentConfig && !empty($paymentConfig['swish_number'])) {
            $swishUrl = generateSwishUrl(
                $paymentConfig['swish_number'],
                $total,
                $swishMessage
            );
            $swishQR = generateSwishQR(
                $paymentConfig['swish_number'],
                $total,
                $swishMessage
            );
        }

        return [
            'success' => true,
            'order_id' => $orderId,
            'order_number' => $orderNumber,
            'subtotal' => $subtotal,
            'discount' => $totalDiscount,
            'total' => $total,
            'applied_discounts' => $appliedDiscounts,
            'swish_available' => $swishUrl !== null,
            'swish_url' => $swishUrl,
            'swish_qr' => $swishQR,
            'swish_number' => $paymentConfig['swish_number'] ?? null,
            'swish_name' => $paymentConfig['swish_name'] ?? null,
            'swish_message' => $swishMessage,
            'card_available' => isCardAvailable($eventId)
        ];

    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

/**
 * Mark order as paid
 *
 * @param int $orderId Order ID
 * @param string $paymentReference External reference (Swish ref, etc)
 * @return bool Success
 */
function markOrderPaid(int $orderId, string $paymentReference = ''): bool {
    $pdo = hub_db();

    $pdo->beginTransaction();

    try {
        // Update order
        $stmt = $pdo->prepare("
            UPDATE orders
            SET payment_status = 'paid',
                payment_reference = ?,
                paid_at = NOW()
            WHERE id = ? AND payment_status = 'pending'
        ");
        $stmt->execute([$paymentReference, $orderId]);

        if ($stmt->rowCount() === 0) {
            $pdo->rollBack();
            return false;
        }

        // Update linked event registrations
        $stmt = $pdo->prepare("
            UPDATE event_registrations
            SET payment_status = 'paid', status = 'confirmed', confirmed_date = NOW()
            WHERE order_id = ?
        ");
        $stmt->execute([$orderId]);

        // Update linked series registrations
        $stmt = $pdo->prepare("
            UPDATE series_registrations
            SET payment_status = 'paid', status = 'confirmed', paid_at = NOW()
            WHERE order_id = ?
        ");
        $stmt->execute([$orderId]);

        $pdo->commit();
        return true;

    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

/**
 * Create order for series registration
 *
 * @param int $seriesRegistrationId Series registration ID
 * @param int $riderId Rider ID
 * @return array Order data
 */
function createSeriesOrder(int $seriesRegistrationId, int $riderId): array {
    $pdo = hub_db();

    // Get series registration
    $stmt = $pdo->prepare("
        SELECT sr.*, s.name as series_name, s.id as series_id,
               c.name as class_name, c.display_name as class_display_name
        FROM series_registrations sr
        JOIN series s ON sr.series_id = s.id
        JOIN classes c ON sr.class_id = c.id
        WHERE sr.id = ?
    ");
    $stmt->execute([$seriesRegistrationId]);
    $registration = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$registration) {
        throw new Exception('Series registration not found');
    }

    // Check if order already exists
    if (!empty($registration['order_id'])) {
        $existingOrder = getOrder($registration['order_id']);
        if ($existingOrder) {
            return [
                'success' => true,
                'order_id' => $registration['order_id'],
                'order_number' => $existingOrder['order_number'],
                'existing' => true
            ];
        }
    }

    // Get rider info
    $stmt = $pdo->prepare("SELECT firstname, lastname, email FROM riders WHERE id = ?");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        throw new Exception('Rider not found');
    }

    // Get payment config for series (use first event or series config)
    $paymentConfig = null;
    try {
        // Try to get payment recipient from series
        $stmt = $pdo->prepare("
            SELECT pr.*, 'series_recipient' as config_source, s.name as source_name, 1 as swish_enabled
            FROM series s
            JOIN payment_recipients pr ON s.payment_recipient_id = pr.id
            WHERE s.id = ? AND pr.active = 1
        ");
        $stmt->execute([$registration['series_id']]);
        $paymentConfig = $stmt->fetch(PDO::FETCH_ASSOC);

        // Fallback: try first event in series
        if (!$paymentConfig) {
            $stmt = $pdo->prepare("
                SELECT e.id FROM events e
                WHERE e.series_id = ?
                ORDER BY e.date ASC LIMIT 1
            ");
            $stmt->execute([$registration['series_id']]);
            $firstEventId = $stmt->fetchColumn();
            if ($firstEventId) {
                $paymentConfig = getPaymentConfig($firstEventId);
            }
        }
    } catch (Exception $e) {}

    // Generate order
    $subtotal = $registration['final_price'];
    $total = $subtotal;
    $orderNumber = generateOrderNumber();
    $swishMessage = substr($orderNumber, 4);

    $pdo->beginTransaction();

    try {
        // Create order (series_id instead of event_id)
        $stmt = $pdo->prepare("
            INSERT INTO orders (
                order_number, rider_id, customer_email, customer_name,
                series_id, subtotal, discount, total_amount, currency,
                payment_method, payment_status,
                swish_number, swish_message,
                expires_at, created_at
            ) VALUES (
                ?, ?, ?, ?,
                ?, ?, 0, ?, 'SEK',
                'swish', 'pending',
                ?, ?,
                DATE_ADD(NOW(), INTERVAL 24 HOUR), NOW()
            )
        ");
        $stmt->execute([
            $orderNumber,
            $riderId,
            $rider['email'],
            $rider['firstname'] . ' ' . $rider['lastname'],
            $registration['series_id'],
            $subtotal,
            $total,
            $paymentConfig['swish_number'] ?? null,
            $swishMessage
        ]);

        $orderId = $pdo->lastInsertId();

        // Create order item
        $description = $registration['series_name'] . ' - Serie-pass - ' .
                       ($registration['class_display_name'] ?: $registration['class_name']);

        $stmt = $pdo->prepare("
            INSERT INTO order_items (
                order_id, item_type, series_registration_id,
                description, unit_price, quantity, total_price
            ) VALUES (?, 'series_registration', ?, ?, ?, 1, ?)
        ");
        $stmt->execute([
            $orderId,
            $seriesRegistrationId,
            $description,
            $subtotal,
            $subtotal
        ]);

        // Update series registration with order_id
        $stmt = $pdo->prepare("
            UPDATE series_registrations SET order_id = ? WHERE id = ?
        ");
        $stmt->execute([$orderId, $seriesRegistrationId]);

        $pdo->commit();

        // Generate Swish links
        $swishUrl = null;
        $swishQR = null;

        if ($paymentConfig && !empty($paymentConfig['swish_number'])) {
            $swishUrl = generateSwishUrl(
                $paymentConfig['swish_number'],
                $total,
                $swishMessage
            );
            $swishQR = generateSwishQR(
                $paymentConfig['swish_number'],
                $total,
                $swishMessage
            );
        }

        return [
            'success' => true,
            'order_id' => $orderId,
            'order_number' => $orderNumber,
            'subtotal' => $subtotal,
            'discount' => 0,
            'total' => $total,
            'swish_available' => $swishUrl !== null,
            'swish_url' => $swishUrl,
            'swish_qr' => $swishQR,
            'swish_number' => $paymentConfig['swish_number'] ?? null,
            'swish_name' => $paymentConfig['swish_name'] ?? null,
            'swish_message' => $swishMessage,
            'card_available' => false
        ];

    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

/**
 * Get order by ID
 */
function getOrder(int $orderId): ?array {
    $pdo = hub_db();

    $stmt = $pdo->prepare("
        SELECT o.*,
               e.name as event_name, e.date as event_date,
               s.name as series_name, s.logo as series_logo
        FROM orders o
        LEFT JOIN events e ON o.event_id = e.id
        LEFT JOIN series s ON o.series_id = s.id
        WHERE o.id = ?
    ");
    $stmt->execute([$orderId]);
    $order = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$order) {
        return null;
    }

    // Get order items
    $stmt = $pdo->prepare("
        SELECT * FROM order_items WHERE order_id = ?
    ");
    $stmt->execute([$orderId]);
    $order['items'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    return $order;
}

/**
 * Get order by order number
 */
function getOrderByNumber(string $orderNumber): ?array {
    $pdo = hub_db();

    $stmt = $pdo->prepare("SELECT id FROM orders WHERE order_number = ?");
    $stmt->execute([$orderNumber]);
    $orderId = $stmt->fetchColumn();

    if (!$orderId) {
        return null;
    }

    return getOrder($orderId);
}

/**
 * Get pending orders for an event (for admin confirmation)
 */
function getPendingOrders(int $eventId): array {
    $pdo = hub_db();

    $stmt = $pdo->prepare("
        SELECT o.*, r.firstname, r.lastname
        FROM orders o
        LEFT JOIN riders r ON o.rider_id = r.id
        WHERE o.event_id = ? AND o.payment_status = 'pending'
        ORDER BY o.created_at DESC
    ");
    $stmt->execute([$eventId]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// ============================================================================
// DISCOUNT & GRAVITY ID FUNCTIONS
// ============================================================================

/**
 * Validate and get discount code details
 *
 * @param string $code The discount code to validate
 * @param int $eventId Event ID (for event-specific codes)
 * @param int|null $riderId Rider ID (for per-user limits)
 * @param float $orderAmount Order subtotal (for minimum amount check)
 * @return array ['valid' => bool, 'discount' => array|null, 'error' => string|null]
 */
function validateDiscountCode(string $code, int $eventId, ?int $riderId = null, float $orderAmount = 0): array {
    $pdo = hub_db();

    // Check if discount_codes table exists
    try {
        $check = $pdo->query("SHOW TABLES LIKE 'discount_codes'");
        if ($check->rowCount() === 0) {
            return ['valid' => false, 'discount' => null, 'error' => 'Rabattkodssystemet är inte aktiverat'];
        }
    } catch (Exception $e) {
        return ['valid' => false, 'discount' => null, 'error' => 'Rabattkodssystemet är inte tillgängligt'];
    }

    // Look up the code
    $stmt = $pdo->prepare("
        SELECT dc.*, e.series_id
        FROM discount_codes dc
        LEFT JOIN events e ON e.id = ?
        WHERE dc.code = ? AND dc.is_active = 1
    ");
    $stmt->execute([$eventId, strtoupper(trim($code))]);
    $discount = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$discount) {
        return ['valid' => false, 'discount' => null, 'error' => 'Ogiltig rabattkod'];
    }

    // Check validity period
    $now = date('Y-m-d H:i:s');
    if ($discount['valid_from'] && $now < $discount['valid_from']) {
        return ['valid' => false, 'discount' => null, 'error' => 'Rabattkoden har inte börjat gälla ännu'];
    }
    if ($discount['valid_until'] && $now > $discount['valid_until']) {
        return ['valid' => false, 'discount' => null, 'error' => 'Rabattkoden har gått ut'];
    }

    // Check max uses
    if ($discount['max_uses'] !== null && $discount['current_uses'] >= $discount['max_uses']) {
        return ['valid' => false, 'discount' => null, 'error' => 'Rabattkoden har använts för många gånger'];
    }

    // Check per-user limit
    if ($riderId && $discount['max_uses_per_user']) {
        $stmt = $pdo->prepare("
            SELECT COUNT(*) FROM discount_code_usage
            WHERE discount_code_id = ? AND rider_id = ?
        ");
        $stmt->execute([$discount['id'], $riderId]);
        $userUses = $stmt->fetchColumn();
        if ($userUses >= $discount['max_uses_per_user']) {
            return ['valid' => false, 'discount' => null, 'error' => 'Du har redan använt denna rabattkod'];
        }
    }

    // Check minimum order amount
    if ($discount['min_order_amount'] && $orderAmount < $discount['min_order_amount']) {
        return [
            'valid' => false,
            'discount' => null,
            'error' => 'Minsta orderbelopp är ' . number_format($discount['min_order_amount'], 0) . ' kr'
        ];
    }

    // Check event/series restriction
    if ($discount['applicable_to'] === 'event' && $discount['event_id'] && $discount['event_id'] != $eventId) {
        return ['valid' => false, 'discount' => null, 'error' => 'Rabattkoden gäller inte för detta event'];
    }
    if ($discount['applicable_to'] === 'series' && $discount['series_id'] && $discount['series_id'] != $discount['series_id']) {
        return ['valid' => false, 'discount' => null, 'error' => 'Rabattkoden gäller inte för denna serie'];
    }

    return ['valid' => true, 'discount' => $discount, 'error' => null];
}

/**
 * Calculate discount amount from a discount code
 *
 * @param array $discount Discount code data
 * @param float $subtotal Order subtotal
 * @return float Discount amount in SEK
 */
function calculateDiscountAmount(array $discount, float $subtotal): float {
    if ($discount['discount_type'] === 'percentage') {
        return round($subtotal * ($discount['discount_value'] / 100), 2);
    }
    // Fixed amount - but never more than subtotal
    return min($discount['discount_value'], $subtotal);
}

/**
 * Check if rider has valid Gravity ID and calculate discount
 *
 * Works with existing gravity_id column in riders table.
 * Discount can be configured per event, per series, or globally.
 * If gravity_id_discount = 0, the discount is explicitly disabled for that event.
 *
 * @param int $riderId Rider ID
 * @param int $eventId Event ID (to check if Gravity ID discount applies)
 * @return array ['has_gravity_id' => bool, 'discount' => float, 'gravity_id' => string|null, 'enabled' => bool]
 */
function checkGravityIdDiscount(int $riderId, int $eventId): array {
    $pdo = hub_db();

    // Check if rider has Gravity ID
    $rider = null;
    try {
        $stmt = $pdo->prepare("
            SELECT gravity_id FROM riders
            WHERE id = ? AND gravity_id IS NOT NULL AND gravity_id != ''
        ");
        $stmt->execute([$riderId]);
        $rider = $stmt->fetch(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        return ['has_gravity_id' => false, 'discount' => 0, 'gravity_id' => null, 'enabled' => false];
    }

    if (!$rider || empty($rider['gravity_id'])) {
        return ['has_gravity_id' => false, 'discount' => 0, 'gravity_id' => null, 'enabled' => false];
    }

    // Default is 0 (inactive) - must be explicitly enabled per event or series
    $discount = 0.0;

    // Priority: 1. Event setting, 2. Series setting, 3. Global setting
    try {
        $stmt = $pdo->prepare("SELECT gravity_id_discount, series_id FROM events WHERE id = ?");
        $stmt->execute([$eventId]);
        $event = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($event) {
            // Check event-specific setting first
            if ($event['gravity_id_discount'] !== null && floatval($event['gravity_id_discount']) > 0) {
                $discount = floatval($event['gravity_id_discount']);
            }
            // If event has no setting, check series
            elseif (!empty($event['series_id'])) {
                try {
                    $stmt = $pdo->prepare("SELECT gravity_id_discount FROM series WHERE id = ?");
                    $stmt->execute([$event['series_id']]);
                    $seriesDiscount = $stmt->fetchColumn();
                    if ($seriesDiscount !== false && floatval($seriesDiscount) > 0) {
                        $discount = floatval($seriesDiscount);
                    }
                } catch (Exception $e) {
                    // series.gravity_id_discount column doesn't exist
                }
            }
        }
    } catch (Exception $e) {
        // gravity_id_discount column doesn't exist in events
    }

    // If still 0, check global setting (but global default is also 0)
    if ($discount == 0) {
        try {
            $stmt = $pdo->query("SELECT setting_value FROM gravity_id_settings WHERE setting_key = 'default_discount'");
            $globalDiscount = $stmt->fetchColumn();
            if ($globalDiscount && floatval($globalDiscount) > 0) {
                $discount = floatval($globalDiscount);
            }
        } catch (Exception $e) {
            // Settings table doesn't exist
        }
    }

    return [
        'has_gravity_id' => true,
        'discount' => $discount,
        'gravity_id' => $rider['gravity_id'],
        'enabled' => $discount > 0
    ];
}

/**
 * Record discount code usage
 *
 * @param int $discountCodeId Discount code ID
 * @param int $orderId Order ID
 * @param int|null $riderId Rider ID
 * @param float $discountAmount Amount discounted
 */
function recordDiscountUsage(int $discountCodeId, int $orderId, ?int $riderId, float $discountAmount): void {
    $pdo = hub_db();

    try {
        // Insert usage record
        $stmt = $pdo->prepare("
            INSERT INTO discount_code_usage (discount_code_id, order_id, rider_id, discount_amount)
            VALUES (?, ?, ?, ?)
        ");
        $stmt->execute([$discountCodeId, $orderId, $riderId, $discountAmount]);

        // Increment usage counter
        $stmt = $pdo->prepare("
            UPDATE discount_codes SET current_uses = current_uses + 1 WHERE id = ?
        ");
        $stmt->execute([$discountCodeId]);
    } catch (Exception $e) {
        // Log but don't fail the order
        error_log("Failed to record discount usage: " . $e->getMessage());
    }
}

/**
 * Apply a discount code to an existing pending order
 *
 * @param int $orderId Order ID
 * @param string $code Discount code
 * @param int|null $riderId Rider ID (for validation)
 * @return array ['success' => bool, 'error' => string|null, 'new_total' => float|null]
 */
function applyDiscountToOrder(int $orderId, string $code, ?int $riderId = null): array {
    $pdo = hub_db();

    // Get the order
    $order = getOrder($orderId);
    if (!$order) {
        return ['success' => false, 'error' => 'Order hittades inte'];
    }

    // Check if already paid
    if ($order['payment_status'] === 'paid') {
        return ['success' => false, 'error' => 'Ordern är redan betald'];
    }

    // Check if discount already applied
    if (!empty($order['discount_code_id'])) {
        return ['success' => false, 'error' => 'En rabattkod är redan använd på denna order'];
    }

    // Validate the discount code
    $validation = validateDiscountCode($code, $order['event_id'], $riderId, $order['subtotal']);
    if (!$validation['valid']) {
        return ['success' => false, 'error' => $validation['error']];
    }

    $discount = $validation['discount'];
    $discountAmount = calculateDiscountAmount($discount, $order['subtotal']);

    // Calculate new totals
    $currentDiscount = floatval($order['discount'] ?? 0);
    $newDiscount = $currentDiscount + $discountAmount;
    $newTotal = max(0, $order['subtotal'] - $newDiscount);

    $pdo->beginTransaction();

    try {
        // Update order
        $stmt = $pdo->prepare("
            UPDATE orders
            SET discount = ?,
                total_amount = ?,
                discount_code_id = ?
            WHERE id = ? AND payment_status = 'pending'
        ");
        $stmt->execute([$newDiscount, $newTotal, $discount['id'], $orderId]);

        // Record usage
        recordDiscountUsage($discount['id'], $orderId, $riderId, $discountAmount);

        $pdo->commit();

        return [
            'success' => true,
            'discount_amount' => $discountAmount,
            'new_discount' => $newDiscount,
            'new_total' => $newTotal
        ];

    } catch (Exception $e) {
        $pdo->rollBack();
        return ['success' => false, 'error' => 'Kunde inte tillämpa rabattkod: ' . $e->getMessage()];
    }
}
