<?php
/**
 * TheHUB Order Manager - Multi-Rider Support
 *
 * Hanterar ordrar med flera deltagare i samma betalning.
 * En förälder kan anmäla flera barn, en klubb kan anmäla ett helt lag.
 *
 * @since 2026-01-12
 */

require_once __DIR__ . '/../hub-config.php';
require_once __DIR__ . '/payment.php';

/**
 * Generera unik order-referens (ex: "A5F2J0112")
 */
function generateOrderReference(): string {
    $chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    $ref = '';
    for ($i = 0; $i < 5; $i++) {
        $ref .= $chars[random_int(0, strlen($chars) - 1)];
    }
    $ref .= date('md'); // Lägg till månad och dag
    return $ref;
}

/**
 * Skapa en multi-rider order
 *
 * @param array $buyerData Köparens info: name, email, phone, user_id
 * @param array $items Lista av registreringar: [{type, rider_id, event_id/series_id, class_id}, ...]
 * @param string|null $discountCode Rabattkod (valfritt)
 * @return array ['success' => bool, 'order' => array|null, 'error' => string|null]
 */
function createMultiRiderOrder(array $buyerData, array $items, ?string $discountCode = null): array {
    $pdo = hub_db();

    if (empty($items)) {
        return ['success' => false, 'error' => 'Inga deltagare valda'];
    }

    $pdo->beginTransaction();

    try {
        // Generera unik referens
        $orderReference = generateOrderReference();

        // Kolla att referensen är unik
        $checkStmt = $pdo->prepare("SELECT id FROM orders WHERE order_number = ?");
        $checkStmt->execute([$orderReference]);
        while ($checkStmt->fetch()) {
            $orderReference = generateOrderReference();
            $checkStmt->execute([$orderReference]);
        }

        // Hämta payment config från första event (för Swish-nummer)
        $firstEventId = null;
        foreach ($items as $item) {
            if (($item['type'] ?? 'event') === 'event' && !empty($item['event_id'])) {
                $firstEventId = intval($item['event_id']);
                break;
            }
        }

        $swishNumber = null;
        $swishMessage = $orderReference;
        if ($firstEventId && function_exists('getPaymentConfig')) {
            $paymentConfig = getPaymentConfig($firstEventId);
            if ($paymentConfig && !empty($paymentConfig['swish_number'])) {
                $swishNumber = $paymentConfig['swish_number'];
            }
        }

        // Skapa order
        $orderStmt = $pdo->prepare("
            INSERT INTO orders (
                order_number, rider_id, customer_email, customer_name,
                event_id, subtotal, discount, total_amount, currency,
                payment_method, payment_status,
                swish_number, swish_message,
                expires_at, created_at
            ) VALUES (
                ?, ?, ?, ?,
                ?, 0, 0, 0, 'SEK',
                'swish', 'pending',
                ?, ?,
                DATE_ADD(NOW(), INTERVAL 24 HOUR), NOW()
            )
        ");
        $orderStmt->execute([
            $orderReference,
            $buyerData['user_id'] ?? null,
            $buyerData['email'],
            $buyerData['name'],
            $firstEventId,
            $swishNumber,
            $swishMessage
        ]);

        $orderId = $pdo->lastInsertId();

        $subtotal = 0;
        $registrations = [];
        $orderItems = [];

        // Processa varje item
        foreach ($items as $item) {
            $itemType = $item['type'] ?? 'event';
            $riderId = intval($item['rider_id']);
            $classId = intval($item['class_id']);

            // Hämta rider-info
            $riderStmt = $pdo->prepare("
                SELECT firstname, lastname, email, birth_year, gender, club_id
                FROM riders WHERE id = ?
            ");
            $riderStmt->execute([$riderId]);
            $rider = $riderStmt->fetch(PDO::FETCH_ASSOC);

            if (!$rider) {
                throw new Exception("Rider med ID {$riderId} hittades inte");
            }

            // Hämta klubbnamn
            $clubName = '';
            if ($rider['club_id']) {
                $clubStmt = $pdo->prepare("SELECT name FROM clubs WHERE id = ?");
                $clubStmt->execute([$rider['club_id']]);
                $clubName = $clubStmt->fetchColumn() ?: '';
            }

            // Hämta klassnamn
            $classStmt = $pdo->prepare("SELECT name, display_name FROM classes WHERE id = ?");
            $classStmt->execute([$classId]);
            $classRow = $classStmt->fetch(PDO::FETCH_ASSOC);
            $className = $classRow['display_name'] ?: $classRow['name'];

            if ($itemType === 'event') {
                $eventId = intval($item['event_id']);

                // Kolla om redan anmäld
                $checkRegStmt = $pdo->prepare("
                    SELECT id FROM event_registrations
                    WHERE event_id = ? AND rider_id = ? AND status != 'cancelled'
                ");
                $checkRegStmt->execute([$eventId, $riderId]);
                if ($checkRegStmt->fetch()) {
                    throw new Exception("{$rider['firstname']} {$rider['lastname']} är redan anmäld till detta event");
                }

                // Hämta event-info och pris
                $eventStmt = $pdo->prepare("
                    SELECT e.name as event_name, e.date as event_date,
                           epr.base_price, epr.early_bird_price, epr.late_fee,
                           e.early_bird_deadline, e.late_fee_start
                    FROM events e
                    LEFT JOIN event_pricing_rules epr ON epr.event_id = e.id AND epr.class_id = ?
                    WHERE e.id = ?
                ");
                $eventStmt->execute([$classId, $eventId]);
                $eventInfo = $eventStmt->fetch(PDO::FETCH_ASSOC);

                if (!$eventInfo) {
                    throw new Exception("Event med ID {$eventId} hittades inte");
                }

                // Beräkna pris
                $basePrice = floatval($eventInfo['base_price'] ?? 0);
                $finalPrice = $basePrice;
                $earlyBirdDiscount = 0;
                $lateFee = 0;

                $now = time();
                if (!empty($eventInfo['early_bird_deadline']) && $now < strtotime($eventInfo['early_bird_deadline'])) {
                    if ($eventInfo['early_bird_price']) {
                        $earlyBirdDiscount = $basePrice - floatval($eventInfo['early_bird_price']);
                        $finalPrice = floatval($eventInfo['early_bird_price']);
                    }
                } elseif (!empty($eventInfo['late_fee_start']) && $now >= strtotime($eventInfo['late_fee_start'])) {
                    if ($eventInfo['late_fee']) {
                        $lateFee = floatval($eventInfo['late_fee']);
                        $finalPrice = $basePrice + $lateFee;
                    }
                }

                // Skapa event_registration
                $regStmt = $pdo->prepare("
                    INSERT INTO event_registrations (
                        event_id, rider_id, first_name, last_name, email,
                        birth_year, gender, club_name, category,
                        status, payment_status, registration_date, registered_by, order_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', 'unpaid', NOW(), ?, ?)
                ");
                $regStmt->execute([
                    $eventId,
                    $riderId,
                    $rider['firstname'],
                    $rider['lastname'],
                    $rider['email'],
                    $rider['birth_year'],
                    $rider['gender'],
                    $clubName,
                    $className,
                    $buyerData['user_id'] ?? null,
                    $orderId
                ]);

                $registrationId = $pdo->lastInsertId();

                // Skapa order_item
                $description = "{$rider['firstname']} {$rider['lastname']} - {$eventInfo['event_name']} - {$className}";
                $itemStmt = $pdo->prepare("
                    INSERT INTO order_items (
                        order_id, item_type, registration_id,
                        description, unit_price, quantity, total_price
                    ) VALUES (?, 'registration', ?, ?, ?, 1, ?)
                ");
                $itemStmt->execute([$orderId, $registrationId, $description, $finalPrice, $finalPrice]);

                $subtotal += $finalPrice;

                $registrations[] = [
                    'type' => 'event',
                    'registration_id' => $registrationId,
                    'rider_name' => "{$rider['firstname']} {$rider['lastname']}",
                    'event_name' => $eventInfo['event_name'],
                    'class_name' => $className,
                    'price' => $finalPrice
                ];

            } elseif ($itemType === 'series') {
                $seriesId = intval($item['series_id']);

                // Kolla om redan anmäld till serien
                $checkSeriesStmt = $pdo->prepare("
                    SELECT id FROM series_registrations
                    WHERE series_id = ? AND rider_id = ? AND status != 'cancelled'
                ");
                $checkSeriesStmt->execute([$seriesId, $riderId]);
                if ($checkSeriesStmt->fetch()) {
                    throw new Exception("{$rider['firstname']} {$rider['lastname']} har redan ett serie-pass för denna serie");
                }

                // Hämta serie-info
                $seriesStmt = $pdo->prepare("
                    SELECT s.name as series_name, s.series_discount_percent
                    FROM series s
                    WHERE s.id = ?
                ");
                $seriesStmt->execute([$seriesId]);
                $seriesInfo = $seriesStmt->fetch(PDO::FETCH_ASSOC);

                if (!$seriesInfo) {
                    throw new Exception("Serie med ID {$seriesId} hittades inte");
                }

                // Beräkna seriepris (summa av alla event-priser minus rabatt)
                $seriesPriceStmt = $pdo->prepare("
                    SELECT SUM(COALESCE(epr.base_price, 0)) as total_price
                    FROM events e
                    LEFT JOIN event_pricing_rules epr ON epr.event_id = e.id AND epr.class_id = ?
                    WHERE e.series_id = ?
                ");
                $seriesPriceStmt->execute([$classId, $seriesId]);
                $priceRow = $seriesPriceStmt->fetch(PDO::FETCH_ASSOC);
                $basePrice = floatval($priceRow['total_price'] ?? 0);

                $discountPercent = floatval($seriesInfo['series_discount_percent'] ?? 15);
                $discountAmount = round($basePrice * ($discountPercent / 100), 2);
                $finalPrice = $basePrice - $discountAmount;

                // Skapa series_registration
                $seriesRegStmt = $pdo->prepare("
                    INSERT INTO series_registrations (
                        rider_id, series_id, class_id,
                        base_price, discount_percent, discount_amount, final_price,
                        order_id, payment_status, status, registration_source, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', 'active', 'web', NOW())
                ");
                $seriesRegStmt->execute([
                    $riderId,
                    $seriesId,
                    $classId,
                    $basePrice,
                    $discountPercent,
                    $discountAmount,
                    $finalPrice,
                    $orderId
                ]);

                $seriesRegId = $pdo->lastInsertId();

                // Skapa event-kopplingar för alla event i serien
                $eventsStmt = $pdo->prepare("SELECT id FROM events WHERE series_id = ?");
                $eventsStmt->execute([$seriesId]);
                while ($eventRow = $eventsStmt->fetch(PDO::FETCH_ASSOC)) {
                    $linkStmt = $pdo->prepare("
                        INSERT INTO series_registration_events (series_registration_id, event_id, status)
                        VALUES (?, ?, 'registered')
                    ");
                    $linkStmt->execute([$seriesRegId, $eventRow['id']]);
                }

                // Skapa order_item
                $description = "{$rider['firstname']} {$rider['lastname']} - {$seriesInfo['series_name']} (Serie-pass) - {$className}";
                $itemStmt = $pdo->prepare("
                    INSERT INTO order_items (
                        order_id, item_type, series_registration_id,
                        description, unit_price, quantity, total_price
                    ) VALUES (?, 'series_registration', ?, ?, ?, 1, ?)
                ");
                $itemStmt->execute([$orderId, $seriesRegId, $description, $finalPrice, $finalPrice]);

                $subtotal += $finalPrice;

                $registrations[] = [
                    'type' => 'series',
                    'registration_id' => $seriesRegId,
                    'rider_name' => "{$rider['firstname']} {$rider['lastname']}",
                    'series_name' => $seriesInfo['series_name'],
                    'class_name' => $className,
                    'price' => $finalPrice,
                    'discount' => $discountAmount
                ];
            }
        }

        // Beräkna totalt
        $totalDiscount = 0;
        $totalAmount = $subtotal - $totalDiscount;

        // Uppdatera order med summor
        $updateStmt = $pdo->prepare("
            UPDATE orders SET
                subtotal = ?,
                discount = ?,
                total_amount = ?
            WHERE id = ?
        ");
        $updateStmt->execute([$subtotal, $totalDiscount, $totalAmount, $orderId]);

        $pdo->commit();

        return [
            'success' => true,
            'order' => [
                'id' => $orderId,
                'order_reference' => $orderReference,
                'subtotal' => $subtotal,
                'discount' => $totalDiscount,
                'total_amount' => $totalAmount,
                'registrations' => $registrations,
                'checkout_url' => "/checkout?order={$orderId}"
            ]
        ];

    } catch (Exception $e) {
        $pdo->rollBack();
        return [
            'success' => false,
            'error' => $e->getMessage()
        ];
    }
}

/**
 * Hämta riders som användaren kan anmäla
 * Returnerar: sig själv + sina barn (family members)
 */
function getRegistrableRiders(int $userId): array {
    $pdo = hub_db();

    $riders = [];

    // Hämta användarens egen rider-profil
    $selfStmt = $pdo->prepare("
        SELECT r.id, r.firstname, r.lastname, r.birth_year, r.gender,
               r.license_number, r.license_type, c.name as club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ");
    $selfStmt->execute([$userId]);
    $self = $selfStmt->fetch(PDO::FETCH_ASSOC);

    if ($self) {
        $self['relation'] = 'self';
        $riders[] = $self;
    }

    // Hämta familjemedlemmar (barn)
    try {
        $familyStmt = $pdo->prepare("
            SELECT r.id, r.firstname, r.lastname, r.birth_year, r.gender,
                   r.license_number, r.license_type, c.name as club_name
            FROM family_members fm
            JOIN riders r ON fm.child_rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE fm.parent_rider_id = ?
        ");
        $familyStmt->execute([$userId]);
        while ($family = $familyStmt->fetch(PDO::FETCH_ASSOC)) {
            $family['relation'] = 'child';
            $riders[] = $family;
        }
    } catch (PDOException $e) {
        // family_members table might not exist yet
    }

    return $riders;
}

/**
 * Hämta tillgängliga klasser för en rider i ett event
 */
function getEligibleClassesForEvent(int $eventId, int $riderId): array {
    $pdo = hub_db();

    // Hämta rider-info
    $riderStmt = $pdo->prepare("
        SELECT birth_year, gender, license_type FROM riders WHERE id = ?
    ");
    $riderStmt->execute([$riderId]);
    $rider = $riderStmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        return [];
    }

    // Hämta event-datum för åldersberäkning
    $eventStmt = $pdo->prepare("SELECT date FROM events WHERE id = ?");
    $eventStmt->execute([$eventId]);
    $eventDate = $eventStmt->fetchColumn();

    $riderAge = date('Y', strtotime($eventDate)) - intval($rider['birth_year']);
    $riderGender = strtoupper($rider['gender']);

    // Hämta klasser med priser
    $classStmt = $pdo->prepare("
        SELECT c.id as class_id, c.name, c.display_name, c.gender, c.min_age, c.max_age,
               epr.base_price, epr.early_bird_price, epr.late_fee
        FROM event_pricing_rules epr
        JOIN classes c ON epr.class_id = c.id
        WHERE epr.event_id = ?
        ORDER BY c.sort_order, c.name
    ");
    $classStmt->execute([$eventId]);

    $classes = [];
    while ($class = $classStmt->fetch(PDO::FETCH_ASSOC)) {
        $eligible = true;
        $reason = '';

        // Kolla kön
        if ($class['gender'] && $class['gender'] !== $riderGender) {
            $eligible = false;
            $reason = $class['gender'] === 'M' ? 'Endast herrar' : 'Endast damer';
        }

        // Kolla ålder
        if ($eligible && $class['min_age'] && $riderAge < $class['min_age']) {
            $eligible = false;
            $reason = "Minst {$class['min_age']} år";
        }
        if ($eligible && $class['max_age'] && $riderAge > $class['max_age']) {
            $eligible = false;
            $reason = "Max {$class['max_age']} år";
        }

        $classes[] = [
            'class_id' => $class['class_id'],
            'name' => $class['display_name'] ?: $class['name'],
            'base_price' => floatval($class['base_price']),
            'early_bird_price' => $class['early_bird_price'] ? floatval($class['early_bird_price']) : null,
            'late_fee' => $class['late_fee'] ? floatval($class['late_fee']) : null,
            'eligible' => $eligible,
            'reason' => $reason
        ];
    }

    return $classes;
}

/**
 * Hämta tillgängliga klasser för en rider i en serie
 */
function getEligibleClassesForSeries(int $seriesId, int $riderId): array {
    $pdo = hub_db();

    // Hämta rider-info
    $riderStmt = $pdo->prepare("
        SELECT birth_year, gender, license_type FROM riders WHERE id = ?
    ");
    $riderStmt->execute([$riderId]);
    $rider = $riderStmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        return [];
    }

    // Använd nuvarande år för ålder
    $riderAge = date('Y') - intval($rider['birth_year']);
    $riderGender = strtoupper($rider['gender']);

    // Hämta serie-rabatt
    $seriesStmt = $pdo->prepare("SELECT series_discount_percent FROM series WHERE id = ?");
    $seriesStmt->execute([$seriesId]);
    $discountPercent = floatval($seriesStmt->fetchColumn() ?: 15);

    // Hämta klasser som finns i seriens event
    $classStmt = $pdo->prepare("
        SELECT DISTINCT c.id as class_id, c.name, c.display_name, c.gender, c.min_age, c.max_age,
               (SELECT SUM(epr2.base_price)
                FROM event_pricing_rules epr2
                JOIN events e2 ON epr2.event_id = e2.id
                WHERE e2.series_id = ? AND epr2.class_id = c.id) as total_price
        FROM events e
        JOIN event_pricing_rules epr ON epr.event_id = e.id
        JOIN classes c ON epr.class_id = c.id
        WHERE e.series_id = ?
        GROUP BY c.id
        ORDER BY c.sort_order, c.name
    ");
    $classStmt->execute([$seriesId, $seriesId]);

    $classes = [];
    while ($class = $classStmt->fetch(PDO::FETCH_ASSOC)) {
        $eligible = true;
        $reason = '';

        // Kolla kön
        if ($class['gender'] && $class['gender'] !== $riderGender) {
            $eligible = false;
            $reason = $class['gender'] === 'M' ? 'Endast herrar' : 'Endast damer';
        }

        // Kolla ålder
        if ($eligible && $class['min_age'] && $riderAge < $class['min_age']) {
            $eligible = false;
            $reason = "Minst {$class['min_age']} år";
        }
        if ($eligible && $class['max_age'] && $riderAge > $class['max_age']) {
            $eligible = false;
            $reason = "Max {$class['max_age']} år";
        }

        $basePrice = floatval($class['total_price'] ?? 0);
        $discountAmount = round($basePrice * ($discountPercent / 100), 2);
        $finalPrice = $basePrice - $discountAmount;

        $classes[] = [
            'class_id' => $class['class_id'],
            'name' => $class['display_name'] ?: $class['name'],
            'base_price' => $basePrice,
            'discount_percent' => $discountPercent,
            'discount_amount' => $discountAmount,
            'final_price' => $finalPrice,
            'eligible' => $eligible,
            'reason' => $reason
        ];
    }

    return $classes;
}

/**
 * Skapa en ny rider från anmälningsflödet
 */
function createRiderFromRegistration(array $data, int $parentUserId): array {
    $pdo = hub_db();

    $pdo->beginTransaction();

    try {
        // Validera obligatoriska fält
        if (empty($data['firstname']) || empty($data['lastname']) || empty($data['email'])) {
            throw new Exception('Förnamn, efternamn och e-post krävs');
        }

        // Kolla om email redan finns
        $checkStmt = $pdo->prepare("SELECT id FROM riders WHERE email = ?");
        $checkStmt->execute([$data['email']]);
        if ($checkStmt->fetch()) {
            throw new Exception('E-postadressen är redan registrerad');
        }

        // Beräkna födelseår från födelsedatum
        $birthYear = null;
        if (!empty($data['birth_date'])) {
            $birthYear = date('Y', strtotime($data['birth_date']));
        } elseif (!empty($data['birth_year'])) {
            $birthYear = intval($data['birth_year']);
        }

        // Skapa rider
        $insertStmt = $pdo->prepare("
            INSERT INTO riders (
                firstname, lastname, email, birth_year, gender,
                license_type, license_number, club_id, active, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, NOW())
        ");
        $insertStmt->execute([
            $data['firstname'],
            $data['lastname'],
            $data['email'],
            $birthYear,
            $data['gender'] ?? null,
            $data['license_type'] ?? null,
            $data['license_number'] ?? null,
            $data['club_id'] ?? null
        ]);

        $riderId = $pdo->lastInsertId();

        // Skapa family_member-koppling om det finns en förälder
        if ($parentUserId) {
            try {
                $familyStmt = $pdo->prepare("
                    INSERT INTO family_members (parent_rider_id, child_rider_id, created_at)
                    VALUES (?, ?, NOW())
                ");
                $familyStmt->execute([$parentUserId, $riderId]);
            } catch (PDOException $e) {
                // family_members table might not exist - that's ok
            }
        }

        $pdo->commit();

        return [
            'success' => true,
            'rider' => [
                'id' => $riderId,
                'firstname' => $data['firstname'],
                'lastname' => $data['lastname'],
                'email' => $data['email'],
                'birth_year' => $birthYear,
                'gender' => $data['gender'] ?? null
            ]
        ];

    } catch (Exception $e) {
        $pdo->rollBack();
        return [
            'success' => false,
            'error' => $e->getMessage()
        ];
    }
}

/**
 * Beräkna savings för multi-rider order
 */
function calculateMultiRiderSavings(int $riderCount): array {
    $swishFeePerTransaction = 1.00; // kr

    $individualCost = $riderCount * $swishFeePerTransaction;
    $multiRiderCost = $swishFeePerTransaction; // Bara en avgift
    $savings = $individualCost - $multiRiderCost;

    return [
        'individual_fees' => $individualCost,
        'multi_rider_fee' => $multiRiderCost,
        'savings' => $savings,
        'savings_percent' => $riderCount > 1 ? round((1 - 1/$riderCount) * 100) : 0
    ];
}
