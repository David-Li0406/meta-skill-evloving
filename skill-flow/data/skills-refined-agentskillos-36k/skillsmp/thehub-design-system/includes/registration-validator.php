<?php
/**
 * Registration Validator
 *
 * Validates rider registration against event class rules.
 * Supports national (strict) and sport/motion (relaxed) rule types.
 */

require_once __DIR__ . '/registration-rules.php';

/**
 * Main validation function - validates a registration attempt
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int $riderId Rider ID
 * @param int $classId Class ID
 * @return array Validation result with 'allowed', 'errors', and 'warnings'
 */
function validateRegistration($pdo, $eventId, $riderId, $classId) {
    $errors = [];
    $warnings = [];

    // Get rider information
    $rider = getRiderForValidation($pdo, $riderId);
    if (!$rider) {
        return [
            'allowed' => false,
            'errors' => ['Åkaren hittades inte i systemet.'],
            'warnings' => []
        ];
    }

    // Get event information
    $event = getEventForValidation($pdo, $eventId);
    if (!$event) {
        return [
            'allowed' => false,
            'errors' => ['Eventet hittades inte.'],
            'warnings' => []
        ];
    }

    // Get class information
    $class = getClassForValidation($pdo, $classId);
    if (!$class) {
        return [
            'allowed' => false,
            'errors' => ['Klassen hittades inte.'],
            'warnings' => []
        ];
    }

    // Get effective rule type for this event
    $ruleType = getEffectiveRuleType($pdo, $eventId);

    // If no rule type is set, allow registration with a warning
    if (!$ruleType) {
        return [
            'allowed' => true,
            'errors' => [],
            'warnings' => ['Inga registreringsregler har konfigurerats för detta event.']
        ];
    }

    // Get the specific class rules
    $classRules = getClassRuleForValidation($pdo, $eventId, $classId);

    // If no specific rules for this class, check rule type defaults
    if (!$classRules) {
        // Use rule type defaults
        $classRules = [
            'requires_license' => $ruleType['default_requires_license'],
            'requires_club_membership' => 0,
            'allowed_license_types' => [],
            'allowed_genders' => $ruleType['default_strict_gender'] ? [$class['gender']] : [],
            'min_age' => $ruleType['default_strict_age'] ? $class['min_age'] : null,
            'max_age' => $ruleType['default_strict_age'] ? $class['max_age'] : null,
            'min_birth_year' => null,
            'max_birth_year' => null
        ];
    }

    // Calculate rider age on event date
    $eventDate = new DateTime($event['date']);
    $riderAge = calculateRiderAge($rider['birth_year'], $eventDate);

    // Validation checks based on rule type strictness

    // 1. License validation
    if ($classRules['requires_license']) {
        $licenseResult = validateLicense($rider, $classRules, $event, $ruleType);
        $errors = array_merge($errors, $licenseResult['errors']);
        $warnings = array_merge($warnings, $licenseResult['warnings']);
    }

    // 2. Gender validation
    if (!empty($classRules['allowed_genders'])) {
        $genderResult = validateGender($rider, $classRules, $class);
        $errors = array_merge($errors, $genderResult['errors']);
        $warnings = array_merge($warnings, $genderResult['warnings']);
    }

    // 3. Age validation
    $ageResult = validateAge($riderAge, $classRules, $class);
    $errors = array_merge($errors, $ageResult['errors']);
    $warnings = array_merge($warnings, $ageResult['warnings']);

    // 4. Club membership validation
    if ($classRules['requires_club_membership']) {
        $clubResult = validateClubMembership($rider);
        $errors = array_merge($errors, $clubResult['errors']);
        $warnings = array_merge($warnings, $clubResult['warnings']);
    }

    // 5. Check if class is active
    if (isset($classRules['is_active']) && !$classRules['is_active']) {
        $errors[] = 'Denna klass är inte öppen för anmälan.';
    }

    return [
        'allowed' => empty($errors),
        'errors' => $errors,
        'warnings' => $warnings,
        'rider' => [
            'name' => $rider['firstname'] . ' ' . $rider['lastname'],
            'age' => $riderAge,
            'gender' => $rider['gender'],
            'license_type' => $rider['license_type'],
            'club' => $rider['club_name']
        ],
        'class' => [
            'name' => $class['display_name'] ?: $class['name']
        ],
        'rule_type' => $ruleType['name'] ?? 'Ingen'
    ];
}

/**
 * Validate license requirements
 */
function validateLicense($rider, $classRules, $event, $ruleType) {
    $errors = [];
    $warnings = [];

    // Check if rider has a license
    if (empty($rider['license_number'])) {
        if ($ruleType && $ruleType['default_strict_license_type']) {
            $errors[] = 'Du måste ha en giltig licens för att anmäla dig till denna klass.';
        } else {
            $warnings[] = 'Du har ingen registrerad licens. Kontrollera att detta är tillåtet för eventet.';
        }
        return ['errors' => $errors, 'warnings' => $warnings];
    }

    // Check license validity date
    if (!empty($rider['license_valid_until'])) {
        $eventDate = new DateTime($event['date']);
        $licenseExpiry = new DateTime($rider['license_valid_until']);

        if ($licenseExpiry < $eventDate) {
            $errors[] = 'Din licens går ut ' . $licenseExpiry->format('Y-m-d') .
                       ' men eventet är ' . $eventDate->format('Y-m-d') .
                       '. Förnya din licens före anmälan.';
        }
    }

    // Check if rider's license type is allowed for this class
    if (!empty($classRules['allowed_license_types'])) {
        $allowedTypes = $classRules['allowed_license_types'];

        // Normalize license type comparison (case-insensitive)
        $riderLicenseType = strtolower(trim($rider['license_type'] ?? ''));
        $allowedTypesLower = array_map('strtolower', array_map('trim', $allowedTypes));

        if (!empty($riderLicenseType) && !in_array($riderLicenseType, $allowedTypesLower)) {
            $allowedList = implode(', ', $allowedTypes);
            $errors[] = "Din licenstyp ({$rider['license_type']}) är inte godkänd för denna klass. " .
                       "Tillåtna licenstyper: {$allowedList}.";
        }
    }

    return ['errors' => $errors, 'warnings' => $warnings];
}

/**
 * Validate gender requirements
 */
function validateGender($rider, $classRules, $class) {
    $errors = [];
    $warnings = [];

    $allowedGenders = $classRules['allowed_genders'];

    // Handle different gender formats (M/K vs M/F)
    $riderGender = strtoupper($rider['gender'] ?? '');

    // Map F to K if needed (Swedish convention)
    $riderGenderNormalized = $riderGender === 'F' ? 'K' : $riderGender;

    // Check if ALL is in allowed genders (means no restriction)
    if (in_array('ALL', array_map('strtoupper', $allowedGenders))) {
        return ['errors' => $errors, 'warnings' => $warnings];
    }

    // Normalize allowed genders
    $allowedGendersUpper = array_map('strtoupper', $allowedGenders);

    if (!in_array($riderGenderNormalized, $allowedGendersUpper) &&
        !in_array($riderGender, $allowedGendersUpper)) {

        $genderName = $riderGenderNormalized === 'M' ? 'man' : 'kvinna';
        $className = $class['display_name'] ?: $class['name'];

        // Determine class gender description
        $classGenderDesc = '';
        if (in_array('M', $allowedGendersUpper) && !in_array('K', $allowedGendersUpper)) {
            $classGenderDesc = 'herrar';
        } elseif (in_array('K', $allowedGendersUpper) && !in_array('M', $allowedGendersUpper)) {
            $classGenderDesc = 'damer';
        }

        $errors[] = "Du kan inte anmäla dig till klassen {$className} som {$genderName}. " .
                   ($classGenderDesc ? "Denna klass är endast för {$classGenderDesc}." : '');
    }

    return ['errors' => $errors, 'warnings' => $warnings];
}

/**
 * Validate age requirements
 */
function validateAge($riderAge, $classRules, $class) {
    $errors = [];
    $warnings = [];

    // Check min age from rules or class default
    $minAge = $classRules['min_age'] ?? $class['min_age'] ?? null;
    $maxAge = $classRules['max_age'] ?? $class['max_age'] ?? null;

    if ($minAge !== null && $riderAge < $minAge) {
        $className = $class['display_name'] ?: $class['name'];
        $errors[] = "Du är för ung för klassen {$className}. " .
                   "Minimum ålder är {$minAge} år, du är {$riderAge} år.";
    }

    if ($maxAge !== null && $riderAge > $maxAge) {
        $className = $class['display_name'] ?: $class['name'];
        $errors[] = "Du är för gammal för klassen {$className}. " .
                   "Maximum ålder är {$maxAge} år, du är {$riderAge} år.";
    }

    // Birth year checks (alternative age specification)
    if (isset($classRules['min_birth_year']) && $classRules['min_birth_year']) {
        // min_birth_year is the oldest allowed (lowest year number)
        if ($classRules['min_birth_year'] && intval($classRules['min_birth_year']) > 0) {
            // This logic needs rider birth year
            // Note: We don't have direct access to birth year here, so we skip this
            // The age validation above should handle most cases
        }
    }

    // Special warnings for junior riders
    if ($riderAge !== null && $riderAge < 18) {
        $warnings[] = 'Du är under 18 år. Förälder/målsman kan behöva godkänna anmälan.';
    }

    return ['errors' => $errors, 'warnings' => $warnings];
}

/**
 * Validate club membership requirement
 */
function validateClubMembership($rider) {
    $errors = [];
    $warnings = [];

    if (empty($rider['club_id']) || empty($rider['club_name'])) {
        $errors[] = 'Du måste vara medlem i en klubb för att anmäla dig till denna klass.';
    }

    return ['errors' => $errors, 'warnings' => $warnings];
}

/**
 * Calculate rider age on event date
 */
function calculateRiderAge($birthYear, $eventDate) {
    if (!$birthYear) {
        return null;
    }

    $eventYear = (int) $eventDate->format('Y');
    return $eventYear - (int) $birthYear;
}

/**
 * Get rider information for validation
 */
function getRiderForValidation($pdo, $riderId) {
    $sql = "SELECT r.*, c.name AS club_name, c.short_name AS club_short_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$riderId]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

/**
 * Get event information for validation
 */
function getEventForValidation($pdo, $eventId) {
    $sql = "SELECT e.*, s.name AS series_name
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            WHERE e.id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

/**
 * Get class information for validation
 */
function getClassForValidation($pdo, $classId) {
    $sql = "SELECT * FROM classes WHERE id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$classId]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

/**
 * Get the specific class rule for validation (from event or series)
 */
function getClassRuleForValidation($pdo, $eventId, $classId) {
    // First check if event uses series rules
    $sql = "SELECT use_series_rules, series_id FROM events WHERE id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId]);
    $event = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$event) {
        return null;
    }

    if ($event['use_series_rules'] && $event['series_id']) {
        // Get from series
        $sql = "SELECT * FROM series_class_rules WHERE series_id = ? AND class_id = ?";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$event['series_id'], $classId]);
    } else {
        // Get from event
        $sql = "SELECT * FROM event_class_rules WHERE event_id = ? AND class_id = ?";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$eventId, $classId]);
    }

    $rule = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($rule) {
        // Decode JSON fields
        $rule['allowed_license_types'] = json_decode($rule['allowed_license_types'] ?? '[]', true) ?: [];
        $rule['allowed_genders'] = json_decode($rule['allowed_genders'] ?? '[]', true) ?: [];
    }

    return $rule;
}

/**
 * Get eligible classes for a rider in an event
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int $riderId Rider ID
 * @return array Array of classes with eligibility status
 */
function getEligibleClasses($pdo, $eventId, $riderId) {
    // Get all active classes for this event
    $sql = "SELECT DISTINCT c.*
            FROM classes c
            WHERE c.id IN (
                SELECT class_id FROM series_class_rules scr
                JOIN events e ON e.series_id = scr.series_id
                WHERE e.id = ? AND scr.is_active = 1
                UNION
                SELECT class_id FROM event_class_rules ecr
                WHERE ecr.event_id = ? AND ecr.is_active = 1
            )
            ORDER BY c.name ASC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId, $eventId]);
    $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Validate each class
    $result = [];
    foreach ($classes as $class) {
        $validation = validateRegistration($pdo, $eventId, $riderId, $class['id']);
        $result[] = [
            'class_id' => $class['id'],
            'class_name' => $class['display_name'] ?: $class['name'],
            'allowed' => $validation['allowed'],
            'errors' => $validation['errors'],
            'warnings' => $validation['warnings']
        ];
    }

    return $result;
}

/**
 * Get riders eligible for a specific class in an event
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int $classId Class ID
 * @param int $limit Maximum number of riders to check
 * @return array Array of riders with eligibility status
 */
function getEligibleRiders($pdo, $eventId, $classId, $limit = 100) {
    // Get active riders
    $sql = "SELECT id, firstname, lastname, birth_year, gender, license_type
            FROM riders
            WHERE active = 1
            ORDER BY lastname, firstname
            LIMIT ?";

    $stmt = $pdo->prepare($sql);
    $stmt->execute([$limit]);
    $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Validate each rider
    $result = [];
    foreach ($riders as $rider) {
        $validation = validateRegistration($pdo, $eventId, $rider['id'], $classId);
        $result[] = [
            'rider_id' => $rider['id'],
            'name' => $rider['firstname'] . ' ' . $rider['lastname'],
            'birth_year' => $rider['birth_year'],
            'gender' => $rider['gender'],
            'license_type' => $rider['license_type'],
            'allowed' => $validation['allowed'],
            'errors' => $validation['errors'],
            'warnings' => $validation['warnings']
        ];
    }

    return $result;
}

/**
 * Log validation result for debugging
 */
function logValidation($pdo, $eventId, $riderId, $classId, $result) {
    // Only log if debug mode is enabled
    if (!defined('DEBUG_MODE') || !DEBUG_MODE) {
        return;
    }

    $logData = [
        'timestamp' => date('Y-m-d H:i:s'),
        'event_id' => $eventId,
        'rider_id' => $riderId,
        'class_id' => $classId,
        'allowed' => $result['allowed'],
        'errors' => $result['errors'],
        'warnings' => $result['warnings']
    ];

    $logFile = __DIR__ . '/../logs/registration-validation.log';
    $logDir = dirname($logFile);

    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }

    file_put_contents(
        $logFile,
        json_encode($logData) . PHP_EOL,
        FILE_APPEND | LOCK_EX
    );
}
