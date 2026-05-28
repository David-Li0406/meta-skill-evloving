<?php
/**
 * Registration Rules Database Helpers
 *
 * Functions for managing registration rules, rule types, and class eligibility.
 * Supports both series-level and event-level rule configuration.
 */

/**
 * Get all registration rule types
 *
 * @param PDO $pdo Database connection
 * @param bool $activeOnly Only return active (non-deleted) types
 * @return array
 */
function getRuleTypes($pdo, $activeOnly = true) {
    $sql = "SELECT * FROM registration_rule_types ORDER BY is_system DESC, name ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get a single rule type by ID or code
 *
 * @param PDO $pdo Database connection
 * @param int|string $identifier Rule type ID or code
 * @return array|null
 */
function getRuleType($pdo, $identifier) {
    if (is_numeric($identifier)) {
        $sql = "SELECT * FROM registration_rule_types WHERE id = ?";
    } else {
        $sql = "SELECT * FROM registration_rule_types WHERE code = ?";
    }
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$identifier]);
    return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
}

/**
 * Get all license types
 *
 * @param PDO $pdo Database connection
 * @param bool $activeOnly Only return active types
 * @return array
 */
function getLicenseTypes($pdo, $activeOnly = true) {
    $sql = "SELECT * FROM license_types";
    if ($activeOnly) {
        $sql .= " WHERE is_active = 1";
    }
    $sql .= " ORDER BY priority DESC, name ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get rule type setting for a series
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @return array|null Rule type info or null if not set
 */
function getSeriesRuleType($pdo, $seriesId) {
    $sql = "SELECT rt.*
            FROM series s
            LEFT JOIN registration_rule_types rt ON s.registration_rule_type_id = rt.id
            WHERE s.id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$seriesId]);
    return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
}

/**
 * Set rule type for a series
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int|null $ruleTypeId Rule type ID (null to clear)
 * @return bool Success
 */
function setSeriesRuleType($pdo, $seriesId, $ruleTypeId) {
    $sql = "UPDATE series SET registration_rule_type_id = ? WHERE id = ?";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([$ruleTypeId, $seriesId]);
}

/**
 * Get rule type setting for an event
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array Event rule info including use_series_rules flag
 */
function getEventRuleType($pdo, $eventId) {
    $sql = "SELECT e.id, e.name, e.series_id, e.registration_rule_type_id, e.use_series_rules,
                   COALESCE(ert.name, srt.name) AS effective_rule_name,
                   COALESCE(ert.code, srt.code) AS effective_rule_code,
                   COALESCE(ert.id, srt.id) AS effective_rule_type_id,
                   srt.name AS series_rule_name,
                   srt.code AS series_rule_code
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN registration_rule_types ert ON e.registration_rule_type_id = ert.id
            LEFT JOIN registration_rule_types srt ON s.registration_rule_type_id = srt.id
            WHERE e.id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId]);
    return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
}

/**
 * Set rule type for an event
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int|null $ruleTypeId Rule type ID (null to use series setting)
 * @param bool $useSeriesRules Whether to use series rules
 * @return bool Success
 */
function setEventRuleType($pdo, $eventId, $ruleTypeId, $useSeriesRules = true) {
    $sql = "UPDATE events SET registration_rule_type_id = ?, use_series_rules = ? WHERE id = ?";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([$ruleTypeId, $useSeriesRules ? 1 : 0, $eventId]);
}

/**
 * Get effective rule type for an event (considering series inheritance)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array|null Effective rule type
 */
function getEffectiveRuleType($pdo, $eventId) {
    $sql = "SELECT rt.*,
                   CASE WHEN e.use_series_rules = 1 THEN 'series' ELSE 'event' END AS source
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN registration_rule_types rt ON
                CASE
                    WHEN e.use_series_rules = 1 THEN s.registration_rule_type_id
                    ELSE e.registration_rule_type_id
                END = rt.id
            WHERE e.id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId]);
    return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
}

/**
 * Get class rules for a series
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @return array Array of class rules
 */
function getSeriesClassRules($pdo, $seriesId) {
    $sql = "SELECT scr.*, c.name AS class_name, c.display_name AS class_display_name,
                   c.gender AS class_gender, c.min_age AS class_min_age, c.max_age AS class_max_age
            FROM series_class_rules scr
            JOIN classes c ON scr.class_id = c.id
            WHERE scr.series_id = ?
            ORDER BY c.name ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$seriesId]);
    $rules = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Decode JSON fields
    foreach ($rules as &$rule) {
        $rule['allowed_license_types'] = json_decode($rule['allowed_license_types'] ?? '[]', true);
        $rule['allowed_genders'] = json_decode($rule['allowed_genders'] ?? '[]', true);
    }

    return $rules;
}

/**
 * Get class rules for an event
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array Array of event-specific class rules
 */
function getEventClassRules($pdo, $eventId) {
    $sql = "SELECT ecr.*, c.name AS class_name, c.display_name AS class_display_name,
                   c.gender AS class_gender, c.min_age AS class_min_age, c.max_age AS class_max_age
            FROM event_class_rules ecr
            JOIN classes c ON ecr.class_id = c.id
            WHERE ecr.event_id = ?
            ORDER BY c.name ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId]);
    $rules = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Decode JSON fields
    foreach ($rules as &$rule) {
        $rule['allowed_license_types'] = json_decode($rule['allowed_license_types'] ?? '[]', true);
        $rule['allowed_genders'] = json_decode($rule['allowed_genders'] ?? '[]', true);
    }

    return $rules;
}

/**
 * Get effective class rules for an event (series or event-specific)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array Array of effective rules with source info
 */
function getEffectiveClassRules($pdo, $eventId) {
    // First, determine if we should use series or event rules
    $eventInfo = getEventRuleType($pdo, $eventId);

    if (!$eventInfo) {
        return [];
    }

    if ($eventInfo['use_series_rules'] && $eventInfo['series_id']) {
        $rules = getSeriesClassRules($pdo, $eventInfo['series_id']);
        foreach ($rules as &$rule) {
            $rule['source'] = 'series';
        }
        return $rules;
    } else {
        $rules = getEventClassRules($pdo, $eventId);
        foreach ($rules as &$rule) {
            $rule['source'] = 'event';
        }
        return $rules;
    }
}

/**
 * Save or update a series class rule
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int $classId Class ID
 * @param array $data Rule data
 * @return bool Success
 */
function saveSeriesClassRule($pdo, $seriesId, $classId, $data) {
    // Check if rule exists
    $sql = "SELECT id FROM series_class_rules WHERE series_id = ? AND class_id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$seriesId, $classId]);
    $existing = $stmt->fetch(PDO::FETCH_ASSOC);

    $allowedLicenseTypes = isset($data['allowed_license_types'])
        ? json_encode($data['allowed_license_types'])
        : null;
    $allowedGenders = isset($data['allowed_genders'])
        ? json_encode($data['allowed_genders'])
        : null;

    if ($existing) {
        $sql = "UPDATE series_class_rules SET
                    allowed_license_types = ?,
                    min_birth_year = ?,
                    max_birth_year = ?,
                    min_age = ?,
                    max_age = ?,
                    allowed_genders = ?,
                    requires_license = ?,
                    requires_club_membership = ?,
                    is_active = ?
                WHERE id = ?";
        $stmt = $pdo->prepare($sql);
        return $stmt->execute([
            $allowedLicenseTypes,
            $data['min_birth_year'] ?? null,
            $data['max_birth_year'] ?? null,
            $data['min_age'] ?? null,
            $data['max_age'] ?? null,
            $allowedGenders,
            $data['requires_license'] ?? 1,
            $data['requires_club_membership'] ?? 0,
            $data['is_active'] ?? 1,
            $existing['id']
        ]);
    } else {
        $sql = "INSERT INTO series_class_rules
                (series_id, class_id, allowed_license_types, min_birth_year, max_birth_year,
                 min_age, max_age, allowed_genders, requires_license, requires_club_membership, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        return $stmt->execute([
            $seriesId,
            $classId,
            $allowedLicenseTypes,
            $data['min_birth_year'] ?? null,
            $data['max_birth_year'] ?? null,
            $data['min_age'] ?? null,
            $data['max_age'] ?? null,
            $allowedGenders,
            $data['requires_license'] ?? 1,
            $data['requires_club_membership'] ?? 0,
            $data['is_active'] ?? 1
        ]);
    }
}

/**
 * Save or update an event class rule
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int $classId Class ID
 * @param array $data Rule data
 * @return bool Success
 */
function saveEventClassRule($pdo, $eventId, $classId, $data) {
    // Check if rule exists
    $sql = "SELECT id FROM event_class_rules WHERE event_id = ? AND class_id = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId, $classId]);
    $existing = $stmt->fetch(PDO::FETCH_ASSOC);

    $allowedLicenseTypes = isset($data['allowed_license_types'])
        ? json_encode($data['allowed_license_types'])
        : null;
    $allowedGenders = isset($data['allowed_genders'])
        ? json_encode($data['allowed_genders'])
        : null;

    if ($existing) {
        $sql = "UPDATE event_class_rules SET
                    allowed_license_types = ?,
                    min_birth_year = ?,
                    max_birth_year = ?,
                    min_age = ?,
                    max_age = ?,
                    allowed_genders = ?,
                    requires_license = ?,
                    requires_club_membership = ?,
                    is_active = ?
                WHERE id = ?";
        $stmt = $pdo->prepare($sql);
        return $stmt->execute([
            $allowedLicenseTypes,
            $data['min_birth_year'] ?? null,
            $data['max_birth_year'] ?? null,
            $data['min_age'] ?? null,
            $data['max_age'] ?? null,
            $allowedGenders,
            $data['requires_license'] ?? 1,
            $data['requires_club_membership'] ?? 0,
            $data['is_active'] ?? 1,
            $existing['id']
        ]);
    } else {
        $sql = "INSERT INTO event_class_rules
                (event_id, class_id, allowed_license_types, min_birth_year, max_birth_year,
                 min_age, max_age, allowed_genders, requires_license, requires_club_membership, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        return $stmt->execute([
            $eventId,
            $classId,
            $allowedLicenseTypes,
            $data['min_birth_year'] ?? null,
            $data['max_birth_year'] ?? null,
            $data['min_age'] ?? null,
            $data['max_age'] ?? null,
            $allowedGenders,
            $data['requires_license'] ?? 1,
            $data['requires_club_membership'] ?? 0,
            $data['is_active'] ?? 1
        ]);
    }
}

/**
 * Delete a series class rule
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int $classId Class ID
 * @return bool Success
 */
function deleteSeriesClassRule($pdo, $seriesId, $classId) {
    $sql = "DELETE FROM series_class_rules WHERE series_id = ? AND class_id = ?";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([$seriesId, $classId]);
}

/**
 * Delete an event class rule
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int $classId Class ID
 * @return bool Success
 */
function deleteEventClassRule($pdo, $eventId, $classId) {
    $sql = "DELETE FROM event_class_rules WHERE event_id = ? AND class_id = ?";
    $stmt = $pdo->prepare($sql);
    return $stmt->execute([$eventId, $classId]);
}

/**
 * Copy series class rules to event (for event-specific overrides)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param int $seriesId Series ID
 * @return bool Success
 */
function copySeriesRulesToEvent($pdo, $eventId, $seriesId) {
    $seriesRules = getSeriesClassRules($pdo, $seriesId);

    foreach ($seriesRules as $rule) {
        saveEventClassRule($pdo, $eventId, $rule['class_id'], $rule);
    }

    return true;
}

/**
 * Get all classes for selection in admin
 *
 * @param PDO $pdo Database connection
 * @param string|null $discipline Filter by discipline
 * @return array
 */
function getAllClasses($pdo, $discipline = null) {
    $sql = "SELECT * FROM classes WHERE 1=1";
    $params = [];

    if ($discipline) {
        $sql .= " AND discipline = ?";
        $params[] = $discipline;
    }

    $sql .= " ORDER BY name ASC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get series with their rule type for admin listing
 *
 * @param PDO $pdo Database connection
 * @param int|null $year Filter by year
 * @return array
 */
function getSeriesWithRuleTypes($pdo, $year = null) {
    $sql = "SELECT s.*, rt.name AS rule_type_name, rt.code AS rule_type_code
            FROM series s
            LEFT JOIN registration_rule_types rt ON s.registration_rule_type_id = rt.id
            WHERE 1=1";
    $params = [];

    if ($year) {
        $sql .= " AND s.year = ?";
        $params[] = $year;
    }

    $sql .= " ORDER BY s.year DESC, s.name ASC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get events with their effective rule type for admin listing
 *
 * @param PDO $pdo Database connection
 * @param int|null $seriesId Filter by series
 * @return array
 */
function getEventsWithRuleTypes($pdo, $seriesId = null) {
    $sql = "SELECT e.*, s.name AS series_name,
                   COALESCE(ert.name, srt.name) AS effective_rule_name,
                   COALESCE(ert.code, srt.code) AS effective_rule_code,
                   e.use_series_rules,
                   srt.name AS series_rule_name
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN registration_rule_types ert ON e.registration_rule_type_id = ert.id
            LEFT JOIN registration_rule_types srt ON s.registration_rule_type_id = srt.id
            WHERE 1=1";
    $params = [];

    if ($seriesId) {
        $sql .= " AND e.series_id = ?";
        $params[] = $seriesId;
    }

    $sql .= " ORDER BY e.date DESC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Apply default rules based on rule type
 *
 * @param PDO $pdo Database connection
 * @param int $seriesId Series ID
 * @param int $ruleTypeId Rule type ID
 * @return bool Success
 */
function applyDefaultRules($pdo, $seriesId, $ruleTypeId) {
    $ruleType = getRuleType($pdo, $ruleTypeId);
    if (!$ruleType) {
        return false;
    }

    // Get all classes
    $classes = getAllClasses($pdo);

    // Get existing rules for this series
    $existingRules = getSeriesClassRules($pdo, $seriesId);
    $existingClassIds = array_column($existingRules, 'class_id');

    // Apply default rules to classes that don't have rules yet
    foreach ($classes as $class) {
        if (in_array($class['id'], $existingClassIds)) {
            continue; // Skip if rule already exists
        }

        $data = [
            'requires_license' => $ruleType['default_requires_license'],
            'requires_club_membership' => 0,
            'is_active' => 1
        ];

        // Set gender restriction based on class
        if ($ruleType['default_strict_gender'] && $class['gender'] !== 'ALL') {
            $data['allowed_genders'] = [$class['gender']];
        }

        // Set age restrictions if strict
        if ($ruleType['default_strict_age']) {
            if ($class['min_age']) {
                $data['min_age'] = $class['min_age'];
            }
            if ($class['max_age']) {
                $data['max_age'] = $class['max_age'];
            }
        }

        saveSeriesClassRule($pdo, $seriesId, $class['id'], $data);
    }

    return true;
}
