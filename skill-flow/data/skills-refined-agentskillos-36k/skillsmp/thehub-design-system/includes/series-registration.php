<?php
/**
 * Series Registration System
 *
 * Handles series (season pass) registration including:
 * - Price calculation (sum of events - series discount)
 * - Rider eligibility validation (gender-based initially)
 * - Creating series registrations
 * - Auto-creating event registrations for all events in series
 *
 * @since 2026-01-11
 */

/**
 * Calculate the price for a series registration
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int $classId Class ID
 * @return array Price breakdown
 */
function calculateSeriesPrice($pdo, $seriesId, $classId) {
    // Get series info
    $stmt = $pdo->prepare("
        SELECT
            s.*,
            pt.early_bird_percent,
            pt.early_bird_days_before
        FROM series s
        LEFT JOIN pricing_templates pt ON s.pricing_template_id = pt.id
        WHERE s.id = ?
    ");
    $stmt->execute([$seriesId]);
    $series = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$series) {
        return ['error' => 'Serie hittades inte'];
    }

    // If series has fixed price, use that
    if ($series['series_price_type'] === 'fixed' && $series['full_series_price'] > 0) {
        return [
            'type' => 'fixed',
            'base_price' => $series['full_series_price'],
            'discount_percent' => 0,
            'discount_amount' => 0,
            'final_price' => $series['full_series_price'],
            'event_count' => getSeriesEventCount($pdo, $seriesId),
            'events' => getSeriesEventsWithPrices($pdo, $seriesId, $classId),
            'savings' => calculateSavingsVsIndividual($pdo, $seriesId, $classId, $series['full_series_price'])
        ];
    }

    // Calculate price from individual events
    $events = getSeriesEventsWithPrices($pdo, $seriesId, $classId);

    if (empty($events)) {
        return ['error' => 'Inga event i serien'];
    }

    $totalBasePrice = 0;
    foreach ($events as $event) {
        $totalBasePrice += $event['price'];
    }

    // Apply series discount
    $discountPercent = floatval($series['series_discount_percent'] ?? 15);
    $discountAmount = $totalBasePrice * ($discountPercent / 100);
    $finalPrice = $totalBasePrice - $discountAmount;

    return [
        'type' => 'calculated',
        'base_price' => $totalBasePrice,
        'discount_percent' => $discountPercent,
        'discount_amount' => round($discountAmount, 2),
        'final_price' => round($finalPrice, 2),
        'event_count' => count($events),
        'events' => $events,
        'savings' => round($discountAmount, 2)
    ];
}

/**
 * Get all events in a series with their prices for a specific class
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int $classId Class ID
 * @return array Events with pricing
 */
function getSeriesEventsWithPrices($pdo, $seriesId, $classId) {
    // Get events that are connected to this series via series_events table
    $stmt = $pdo->prepare("
        SELECT
            e.id,
            e.name,
            e.date,
            e.location,
            v.city,
            e.status,
            -- Get price: First check event_pricing_rules, then pricing_template_rules
            COALESCE(
                epr.base_price,
                ptr.base_price,
                0
            ) AS price,
            CASE
                WHEN epr.base_price IS NOT NULL THEN 'event_specific'
                WHEN ptr.base_price IS NOT NULL THEN 'template'
                ELSE 'default'
            END AS price_source
        FROM series_events se
        JOIN events e ON se.event_id = e.id
        LEFT JOIN venues v ON e.venue_id = v.id
        LEFT JOIN event_pricing_rules epr ON e.id = epr.event_id AND epr.class_id = ?
        LEFT JOIN pricing_templates pt ON e.pricing_template_id = pt.id
        LEFT JOIN pricing_template_rules ptr ON pt.id = ptr.template_id AND ptr.class_id = ?
        WHERE se.series_id = ?
        AND e.active = 1
        ORDER BY e.date ASC
    ");
    $stmt->execute([$classId, $classId, $seriesId]);

    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get count of events in a series
 */
function getSeriesEventCount($pdo, $seriesId) {
    $stmt = $pdo->prepare("
        SELECT COUNT(*) FROM series_events se
        JOIN events e ON se.event_id = e.id
        WHERE se.series_id = ? AND e.active = 1
    ");
    $stmt->execute([$seriesId]);
    return (int) $stmt->fetchColumn();
}

/**
 * Calculate how much rider saves vs buying individual tickets
 */
function calculateSavingsVsIndividual($pdo, $seriesId, $classId, $seriesPrice) {
    $events = getSeriesEventsWithPrices($pdo, $seriesId, $classId);
    $individualTotal = array_sum(array_column($events, 'price'));
    return max(0, $individualTotal - $seriesPrice);
}

/**
 * Validate if a rider can register for a series in a specific class
 *
 * For now, we only validate gender. License validation will be added
 * when 2026 licenses are imported.
 *
 * @param PDO $pdo Database connection
 * @param int $riderId Rider ID
 * @param int $seriesId Series ID
 * @param int $classId Class ID
 * @return array Validation result with 'allowed', 'errors', 'warnings'
 */
function validateSeriesRegistration($pdo, $riderId, $seriesId, $classId) {
    $errors = [];
    $warnings = [];

    // Get rider
    $stmt = $pdo->prepare("SELECT * FROM riders WHERE id = ?");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        return [
            'allowed' => false,
            'errors' => ['Cyklisten hittades inte'],
            'warnings' => []
        ];
    }

    // Get series
    $stmt = $pdo->prepare("SELECT * FROM series WHERE id = ?");
    $stmt->execute([$seriesId]);
    $series = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$series) {
        return [
            'allowed' => false,
            'errors' => ['Serien hittades inte'],
            'warnings' => []
        ];
    }

    // Get class
    $stmt = $pdo->prepare("SELECT * FROM classes WHERE id = ?");
    $stmt->execute([$classId]);
    $class = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$class) {
        return [
            'allowed' => false,
            'errors' => ['Klassen hittades inte'],
            'warnings' => []
        ];
    }

    // Check if series registration is allowed
    if (!$series['allow_series_registration']) {
        $errors[] = 'Serieanmälan är inte aktiverad för denna serie';
    }

    // Check if registration is open (date check)
    $now = new DateTime();
    if ($series['registration_opens']) {
        $opens = new DateTime($series['registration_opens']);
        if ($series['registration_opens_time']) {
            $opens = DateTime::createFromFormat('Y-m-d H:i:s', $series['registration_opens'] . ' ' . $series['registration_opens_time']);
        }
        if ($now < $opens) {
            $errors[] = 'Anmälan öppnar ' . $opens->format('Y-m-d H:i');
        }
    }

    if ($series['registration_closes']) {
        $closes = new DateTime($series['registration_closes']);
        if ($series['registration_closes_time']) {
            $closes = DateTime::createFromFormat('Y-m-d H:i:s', $series['registration_closes'] . ' ' . $series['registration_closes_time']);
        }
        if ($now > $closes) {
            $errors[] = 'Anmälan stängde ' . $closes->format('Y-m-d H:i');
        }
    }

    // Check if already registered for this series
    $stmt = $pdo->prepare("
        SELECT id FROM series_registrations
        WHERE rider_id = ? AND series_id = ? AND status != 'cancelled'
    ");
    $stmt->execute([$riderId, $seriesId]);
    if ($stmt->fetch()) {
        $errors[] = 'Du är redan anmäld till denna serie';
    }

    // GENDER VALIDATION (primary validation for now)
    if ($class['gender'] && $class['gender'] !== 'ALL') {
        $riderGender = strtoupper($rider['gender'] ?? '');
        $classGender = strtoupper($class['gender']);

        // Normalize Swedish K to F
        if ($riderGender === 'F') $riderGender = 'K';
        if ($classGender === 'F') $classGender = 'K';

        if ($riderGender !== $classGender) {
            $genderName = $riderGender === 'M' ? 'man' : 'kvinna';
            $classGenderName = $classGender === 'M' ? 'herrar' : 'damer';
            $errors[] = "Du kan inte anmäla dig som {$genderName} till en klass för {$classGenderName}";
        }
    }

    // AGE VALIDATION (if class has age limits)
    if ($class['min_age'] || $class['max_age']) {
        $birthYear = $rider['birth_year'];
        if ($birthYear) {
            $seriesYear = $series['year'] ?? date('Y');
            $age = $seriesYear - $birthYear;

            if ($class['min_age'] && $age < $class['min_age']) {
                $errors[] = "Du är {$age} år. Denna klass kräver minst {$class['min_age']} år";
            }
            if ($class['max_age'] && $age > $class['max_age']) {
                $errors[] = "Du är {$age} år. Denna klass kräver max {$class['max_age']} år";
            }
        } else {
            $warnings[] = 'Ditt födelseår saknas - vi kan inte verifiera ålderskraven';
        }
    }

    // LICENSE VALIDATION (placeholder - will be stricter when 2026 licenses are imported)
    // For now, just warn if no license
    if (empty($rider['license_number'])) {
        $warnings[] = 'Du har ingen registrerad licens. Vissa klasser kan kräva licens.';
    }

    return [
        'allowed' => empty($errors),
        'errors' => $errors,
        'warnings' => $warnings,
        'rider' => [
            'id' => $rider['id'],
            'name' => $rider['firstname'] . ' ' . $rider['lastname'],
            'email' => $rider['email'],
            'gender' => $rider['gender'],
            'license_type' => $rider['license_type'],
            'license_number' => $rider['license_number']
        ],
        'series' => [
            'id' => $series['id'],
            'name' => $series['name']
        ],
        'class' => [
            'id' => $class['id'],
            'name' => $class['display_name'] ?: $class['name']
        ]
    ];
}

/**
 * Create a series registration and all associated event registrations
 *
 * @param PDO $pdo Database connection
 * @param int $riderId Rider ID
 * @param int $seriesId Series ID
 * @param int $classId Class ID
 * @param string $source Registration source (web, admin, etc.)
 * @param int|null $adminId Admin ID if registered by admin
 * @return array Result with registration ID or error
 */
function createSeriesRegistration($pdo, $riderId, $seriesId, $classId, $source = 'web', $adminId = null) {
    // Validate first
    $validation = validateSeriesRegistration($pdo, $riderId, $seriesId, $classId);
    if (!$validation['allowed']) {
        return [
            'success' => false,
            'errors' => $validation['errors']
        ];
    }

    // Calculate price
    $pricing = calculateSeriesPrice($pdo, $seriesId, $classId);
    if (isset($pricing['error'])) {
        return [
            'success' => false,
            'errors' => [$pricing['error']]
        ];
    }

    // Get rider info for event registrations
    $stmt = $pdo->prepare("
        SELECT r.*, c.name AS club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    // Get class info
    $stmt = $pdo->prepare("SELECT * FROM classes WHERE id = ?");
    $stmt->execute([$classId]);
    $class = $stmt->fetch(PDO::FETCH_ASSOC);

    $pdo->beginTransaction();

    try {
        // 1. Create series registration
        $stmt = $pdo->prepare("
            INSERT INTO series_registrations (
                rider_id, series_id, class_id,
                base_price, discount_percent, discount_amount, final_price,
                payment_status, registration_source, registered_by_admin_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
        ");
        $stmt->execute([
            $riderId,
            $seriesId,
            $classId,
            $pricing['base_price'],
            $pricing['discount_percent'],
            $pricing['discount_amount'],
            $pricing['final_price'],
            $source,
            $adminId
        ]);

        $seriesRegId = $pdo->lastInsertId();

        // 2. Create event registrations for each event in series
        $eventsCreated = 0;
        foreach ($pricing['events'] as $event) {
            // Create entry in event_registrations
            $stmt = $pdo->prepare("
                INSERT INTO event_registrations (
                    event_id, rider_id, first_name, last_name, email,
                    birth_year, gender, club_name, license_number,
                    category, status, payment_status, registration_source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', 'paid', ?)
                ON DUPLICATE KEY UPDATE
                    status = 'confirmed',
                    payment_status = 'paid',
                    updated_at = CURRENT_TIMESTAMP
            ");
            $stmt->execute([
                $event['id'],
                $riderId,
                $rider['firstname'],
                $rider['lastname'],
                $rider['email'],
                $rider['birth_year'],
                $rider['gender'],
                $rider['club_name'],
                $rider['license_number'],
                $class['display_name'] ?: $class['name'],
                'series_' . $source
            ]);

            $eventRegId = $pdo->lastInsertId();

            // Create series_registration_events entry
            $stmt = $pdo->prepare("
                INSERT INTO series_registration_events (
                    series_registration_id, event_id, event_registration_id, status
                ) VALUES (?, ?, ?, 'registered')
            ");
            $stmt->execute([$seriesRegId, $event['id'], $eventRegId ?: null]);

            $eventsCreated++;
        }

        $pdo->commit();

        return [
            'success' => true,
            'registration_id' => $seriesRegId,
            'events_created' => $eventsCreated,
            'pricing' => $pricing,
            'warnings' => $validation['warnings']
        ];

    } catch (Exception $e) {
        $pdo->rollBack();
        return [
            'success' => false,
            'errors' => ['Databasfel: ' . $e->getMessage()]
        ];
    }
}

/**
 * Get eligible classes for a rider in a series
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int $riderId Rider ID
 * @return array Classes with eligibility and pricing
 */
function getEligibleSeriesClasses($pdo, $seriesId, $riderId) {
    // Get rider info
    $stmt = $pdo->prepare("SELECT * FROM riders WHERE id = ?");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        return [];
    }

    // Get all active classes for this series
    // First check if series has specific class rules, otherwise get all active classes
    $stmt = $pdo->prepare("
        SELECT DISTINCT c.*
        FROM classes c
        WHERE c.active = 1
        ORDER BY c.sort_order ASC, c.name ASC
    ");
    $stmt->execute();
    $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $result = [];
    foreach ($classes as $class) {
        $validation = validateSeriesRegistration($pdo, $riderId, $seriesId, $class['id']);
        $pricing = calculateSeriesPrice($pdo, $seriesId, $class['id']);

        $result[] = [
            'id' => $class['id'],
            'name' => $class['display_name'] ?: $class['name'],
            'gender' => $class['gender'],
            'min_age' => $class['min_age'],
            'max_age' => $class['max_age'],
            'eligible' => $validation['allowed'],
            'errors' => $validation['errors'],
            'warnings' => $validation['warnings'],
            'price' => $pricing['final_price'] ?? 0,
            'original_price' => $pricing['base_price'] ?? 0,
            'discount' => $pricing['discount_amount'] ?? 0
        ];
    }

    return $result;
}

/**
 * Get a rider's series registrations
 *
 * @param PDO $pdo Database connection
 * @param int $riderId Rider ID
 * @return array List of series registrations
 */
function getRiderSeriesRegistrations($pdo, $riderId) {
    $stmt = $pdo->prepare("
        SELECT
            sr.*,
            s.name AS series_name,
            s.year AS series_year,
            s.logo AS series_logo,
            c.name AS class_name,
            c.display_name AS class_display_name,
            (SELECT COUNT(*) FROM series_registration_events WHERE series_registration_id = sr.id) AS event_count,
            (SELECT COUNT(*) FROM series_registration_events WHERE series_registration_id = sr.id AND status = 'attended') AS events_attended,
            (SELECT MIN(e.date) FROM series_registration_events sre JOIN events e ON sre.event_id = e.id WHERE sre.series_registration_id = sr.id) AS first_event_date,
            (SELECT MAX(e.date) FROM series_registration_events sre JOIN events e ON sre.event_id = e.id WHERE sre.series_registration_id = sr.id) AS last_event_date
        FROM series_registrations sr
        JOIN series s ON sr.series_id = s.id
        JOIN classes c ON sr.class_id = c.id
        WHERE sr.rider_id = ?
        ORDER BY sr.created_at DESC
    ");
    $stmt->execute([$riderId]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get events for a specific series registration
 *
 * @param PDO $pdo Database connection
 * @param int $seriesRegistrationId Series registration ID
 * @return array List of events with status
 */
function getSeriesRegistrationEvents($pdo, $seriesRegistrationId) {
    $stmt = $pdo->prepare("
        SELECT
            sre.*,
            e.name AS event_name,
            e.date AS event_date,
            e.location AS event_location,
            v.city AS event_city,
            e.status AS event_status
        FROM series_registration_events sre
        JOIN events e ON sre.event_id = e.id
        LEFT JOIN venues v ON e.venue_id = v.id
        WHERE sre.series_registration_id = ?
        ORDER BY e.date ASC
    ");
    $stmt->execute([$seriesRegistrationId]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Check if a rider has a series registration that covers a specific event
 *
 * @param PDO $pdo Database connection
 * @param int $riderId Rider ID
 * @param int $eventId Event ID
 * @return array|false Series registration info or false
 */
function getRiderSeriesRegistrationForEvent($pdo, $riderId, $eventId) {
    $stmt = $pdo->prepare("
        SELECT sr.*, sre.status AS event_status, sre.checked_in
        FROM series_registrations sr
        JOIN series_registration_events sre ON sr.id = sre.series_registration_id
        WHERE sr.rider_id = ?
        AND sre.event_id = ?
        AND sr.status = 'active'
        AND sr.payment_status = 'paid'
    ");
    $stmt->execute([$riderId, $eventId]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

/**
 * Mark series registration as paid (called by payment callback)
 *
 * @param PDO $pdo Database connection
 * @param int $seriesRegistrationId Series registration ID
 * @param string $paymentMethod Payment method used
 * @param string $paymentReference Payment reference
 * @param int|null $orderId Order ID if using order system
 * @return bool Success
 */
function markSeriesRegistrationPaid($pdo, $seriesRegistrationId, $paymentMethod, $paymentReference = null, $orderId = null) {
    $stmt = $pdo->prepare("
        UPDATE series_registrations
        SET payment_status = 'paid',
            payment_method = ?,
            payment_reference = ?,
            order_id = ?,
            paid_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ");

    return $stmt->execute([$paymentMethod, $paymentReference, $orderId, $seriesRegistrationId]);
}

/**
 * Cancel a series registration
 *
 * @param PDO $pdo Database connection
 * @param int $seriesRegistrationId Series registration ID
 * @param string $reason Cancellation reason
 * @return bool Success
 */
function cancelSeriesRegistration($pdo, $seriesRegistrationId, $reason = null) {
    $pdo->beginTransaction();

    try {
        // Update series registration
        $stmt = $pdo->prepare("
            UPDATE series_registrations
            SET status = 'cancelled',
                cancelled_at = CURRENT_TIMESTAMP,
                cancelled_reason = ?
            WHERE id = ?
        ");
        $stmt->execute([$reason, $seriesRegistrationId]);

        // Cancel all event registrations
        $stmt = $pdo->prepare("
            UPDATE series_registration_events
            SET status = 'cancelled'
            WHERE series_registration_id = ?
        ");
        $stmt->execute([$seriesRegistrationId]);

        // Also update the event_registrations table
        $stmt = $pdo->prepare("
            UPDATE event_registrations er
            JOIN series_registration_events sre ON er.id = sre.event_registration_id
            SET er.status = 'cancelled'
            WHERE sre.series_registration_id = ?
        ");
        $stmt->execute([$seriesRegistrationId]);

        $pdo->commit();
        return true;

    } catch (Exception $e) {
        $pdo->rollBack();
        return false;
    }
}
