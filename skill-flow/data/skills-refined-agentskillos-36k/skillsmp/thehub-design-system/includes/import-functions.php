<?php
/**
 * Import functions for CSV processing
 * Shared between import-results.php and import-results-preview.php
 */

// Include smart club matching
require_once __DIR__ . '/club-matching.php';

/**
 * Extract possible birth years from age class name
 * Examples: "Pojkar 13-14" in 2024 → [2010, 2011]
 *           "Herrar 19-29" → [1995-2005]
 *           "U17" → born 2007-2008 in 2024
 *
 * @param string $className The class name (e.g., "Pojkar 13-14", "U17", "Junior")
 * @param int|null $eventYear The year of the event (defaults to current year)
 * @return array Array of possible birth years, empty if can't determine
 */
function getBirthYearsFromClassName($className, $eventYear = null) {
    if (empty($className)) return [];

    $eventYear = $eventYear ?: (int)date('Y');
    $birthYears = [];

    // Pattern 1: Age range like "13-14", "19-29"
    if (preg_match('/(\d{1,2})\s*[-–]\s*(\d{1,2})/', $className, $matches)) {
        $minAge = (int)$matches[1];
        $maxAge = (int)$matches[2];

        // Calculate birth years (someone who is 13 in 2024 was born in 2011)
        for ($age = $minAge; $age <= $maxAge; $age++) {
            $birthYears[] = $eventYear - $age;
        }
    }
    // Pattern 2: U-categories like "U17", "U19"
    elseif (preg_match('/U\s*(\d{1,2})/i', $className, $matches)) {
        $maxAge = (int)$matches[1];
        // U17 means under 17, so ages 15-16 typically
        for ($age = $maxAge - 2; $age < $maxAge; $age++) {
            $birthYears[] = $eventYear - $age;
        }
    }
    // Pattern 3: Single age like "12 år"
    elseif (preg_match('/(\d{1,2})\s*år/i', $className, $matches)) {
        $birthYears[] = $eventYear - (int)$matches[1];
    }
    // Pattern 4: Junior (typically 17-18)
    elseif (preg_match('/junior/i', $className)) {
        $birthYears = [$eventYear - 17, $eventYear - 18];
    }

    return $birthYears;
}

/**
 * Check if a birth year is compatible with an age class
 */
function isBirthYearCompatibleWithClass($birthYear, $className, $eventYear = null) {
    if (empty($birthYear) || empty($className)) return true; // Can't verify, assume compatible

    $possibleYears = getBirthYearsFromClassName($className, $eventYear);
    if (empty($possibleYears)) return true; // Can't determine, assume compatible

    // Allow 1 year tolerance for edge cases (birthday timing)
    foreach ($possibleYears as $year) {
        if (abs($birthYear - $year) <= 1) {
            return true;
        }
    }

    return false;
}

/**
 * Check if a row appears to be a field mapping/description row
 * These rows contain field names like "class", "position", "club_name" instead of actual data
 */
function isFieldMappingRow($row) {
    if (!is_array($row)) return false;

    // Known field mapping keywords that appear in description rows
    $fieldKeywords = ['class', 'position', 'club_name', 'license_number', 'finish_time', 'status', 'firstname', 'lastname'];

    $matchCount = 0;
    foreach ($row as $value) {
        $cleanValue = strtolower(trim($value));
        if (in_array($cleanValue, $fieldKeywords)) {
            $matchCount++;
        }
    }

    // If 3 or more values match field keywords, it's likely a mapping row
    return $matchCount >= 3;
}

/**
 * Import results from CSV file with event mapping
 * Returns stage names mapping for automatic configuration
 */
function importResultsFromCSVWithMapping($filepath, $db, $importId, $eventMapping = [], $forceClassId = null, $forceClubUpdate = false) {
    $stats = [
        'total' => 0,
        'success' => 0,
        'updated' => 0,
        'skipped' => 0,
        'failed' => 0
    ];

    $matching_stats = [
        'events_found' => 0,
        'events_not_found' => 0,
        'events_created' => 0,
        'venues_created' => 0,
        'riders_found' => 0,
        'riders_not_found' => 0,
        'riders_created' => 0,
        'clubs_created' => 0,
        'categories_created' => 0,
        'classes_created' => 0
    ];

    $errors = [];
    $stageNamesMapping = []; // Will store original header names for split times
    $changelog = []; // Track what changed during updates

    // Set global event mapping for use in import
    global $IMPORT_EVENT_MAPPING;
    $IMPORT_EVENT_MAPPING = $eventMapping;

    if (($handle = fopen($filepath, 'r')) === false) {
        throw new Exception('Kunde inte öppna filen');
    }

    // Auto-detect delimiter (comma, semicolon, or tab)
    $firstLine = fgets($handle);
    rewind($handle);

    $commaCount = substr_count($firstLine, ',');
    $semicolonCount = substr_count($firstLine, ';');
    $tabCount = substr_count($firstLine, "\t");

    // Choose delimiter with highest count
    if ($tabCount > $commaCount && $tabCount > $semicolonCount) {
        $delimiter = "\t";
    } elseif ($semicolonCount > $commaCount) {
        $delimiter = ';';
    } else {
        $delimiter = ',';
    }

    // Read header row (0 = unlimited line length)
    $header = fgetcsv($handle, 0, $delimiter);

    if (!$header) {
        fclose($handle);
        throw new Exception('Tom fil eller ogiltigt format');
    }

    // Normalize header - accept multiple variants
    $originalHeaders = $header;

    // NEW APPROACH: Find columns BETWEEN "Club" and "NetTime" - these are all stage columns
    // This handles: varying column names, duplicate headers (SS3, SS3), empty columns, etc.
    $splitTimeColumns = [];
    $splitTimeIndex = 1;

    // First, find the positions of Club and NetTime/finish_time columns
    $clubIndex = -1;
    $netTimeIndex = -1;

    foreach ($header as $index => $col) {
        $normalizedCol = mb_strtolower(trim($col), 'UTF-8');
        $normalizedCol = str_replace([' ', '-', '_'], '', $normalizedCol);

        // Find Club column (matches: club, klubb, team, huvudförening)
        if (in_array($normalizedCol, ['club', 'klubb', 'team', 'huvudförening', 'huvudforening'])) {
            $clubIndex = $index;
        }

        // Find NetTime/finish_time column (matches: nettime, time, tid, finishtime, totaltid)
        if (in_array($normalizedCol, ['nettime', 'time', 'tid', 'finishtime', 'totaltid', 'totaltime', 'nettid'])) {
            $netTimeIndex = $index;
        }
    }

    // Helper function to generate proper stage name based on column header
    $generateStageName = function($originalCol, &$counters) {
        $normalized = mb_strtolower(trim($originalCol), 'UTF-8');
        $normalized = str_replace([' ', '-', '_'], '', $normalized);

        // Prostage → PS
        if (preg_match('/^(prostage|prolog|prologue)(\d*)$/', $normalized, $m)) {
            $num = !empty($m[2]) ? (int)$m[2] : ++$counters['ps'];
            return 'PS' . $num;
        }

        // Powerstage → PW
        if (preg_match('/^(powerstage|power)(\d*)$/', $normalized, $m)) {
            $num = !empty($m[2]) ? (int)$m[2] : ++$counters['pw'];
            return 'PW' . $num;
        }

        // SS/Stage → SS (extract number if present)
        if (preg_match('/^(ss|stage|sträcka|stracka|etapp|s)(\d+)$/', $normalized, $m)) {
            return 'SS' . (int)$m[2];
        }

        // Lap/Varv → LAP
        if (preg_match('/^(lap|varv|runda|round)(\d*)$/', $normalized, $m)) {
            $num = !empty($m[2]) ? (int)$m[2] : ++$counters['lap'];
            return 'LAP' . $num;
        }

        // Split/Mellantid → SPLIT
        if (preg_match('/^(split|mellantid|intermediate)(\d*)$/', $normalized, $m)) {
            $num = !empty($m[2]) ? (int)$m[2] : ++$counters['split'];
            return 'SPLIT' . $num;
        }

        // Just a number or unknown format - use SS with sequential number
        if (preg_match('/^\d+$/', $normalized)) {
            return 'SS' . (int)$normalized;
        }

        // Default: keep original but capitalize
        return strtoupper($originalCol);
    };

    // Counters for stages without numbers
    $stageCounters = ['ps' => 0, 'pw' => 0, 'ss' => 0, 'lap' => 0, 'split' => 0];

    // If we found both Club and NetTime, everything between them is stage columns
    if ($clubIndex >= 0 && $netTimeIndex > $clubIndex) {
        for ($i = $clubIndex + 1; $i < $netTimeIndex; $i++) {
            $originalCol = trim($header[$i]);

            // Skip completely empty columns or columns that are just whitespace
            if (empty($originalCol)) {
                continue;
            }

            // Skip non-stage columns that may appear between Club and NetTime
            // This includes: UCI-ID, birth year, age, DH run times, status columns
            $normalizedCheck = mb_strtolower($originalCol, 'UTF-8');
            $normalizedCheck = str_replace([' ', '-', '_'], '', $normalizedCheck);
            if (in_array($normalizedCheck, [
                'uciid', 'ucikod', 'licens', 'licensenumber',
                'birthyear', 'födelseår', 'fodelsear', 'ålder', 'alder', 'age',
                'run1', 'run2', 'run1time', 'run2time', 'åk1', 'åk2', 'ak1', 'ak2',
                'kval', 'qualifying', 'final',
                'land', 'nationality', 'nationalitet', 'country', 'nation',
                'status', 'fin', 'finished', 'dns', 'dnf', 'dq', 'dsq'
            ])) {
                continue;
            }

            // This is a stage column - map it sequentially to ss1, ss2, etc. in DB
            // But store the proper name (PS1, PW1, SS1) for display
            $properName = $generateStageName($originalCol, $stageCounters);
            $splitTimeColumns[$i] = [
                'original' => $originalCol,
                'mapped' => 'ss' . $splitTimeIndex
            ];
            $stageNamesMapping[$splitTimeIndex] = $properName;
            $splitTimeIndex++;
        }
    } else {
        // Fallback: Use pattern matching if we couldn't find Club/NetTime positions
        // This handles files with different column orders
        foreach ($header as $index => $col) {
            $originalCol = trim($col);
            if (empty($originalCol)) continue;

            $normalizedCol = mb_strtolower($originalCol, 'UTF-8');
            $normalizedCol = str_replace([' ', '-', '_'], '', $normalizedCol);

            // Check if this looks like a split/stage time column
            // Matches: ss1, ps1, s1, v1, stage1, sträcka1, varv1, lap1, split1, etc.
            // Also matches standalone names: prostage, powerstage, prolog, prologue (with or without number)
            $isSplitTimeCol = preg_match('/^(ss|ps|s|v|stage|sträcka|stracka|etapp|varv|lap|split|mellantid|intermediate)\d*/', $normalizedCol)
                           || preg_match('/^(prostage|powerstage|prolog|prologue|prologstage)\d*$/', $normalizedCol);

            if ($isSplitTimeCol) {
                $properName = $generateStageName($originalCol, $stageCounters);
                $splitTimeColumns[$index] = [
                    'original' => $originalCol,
                    'mapped' => 'ss' . $splitTimeIndex
                ];
                $stageNamesMapping[$splitTimeIndex] = $properName;
                $splitTimeIndex++;
            }
        }
    }

    $header = array_map(function($col) use ($splitTimeColumns, &$stageNamesMapping) {
        static $colIndex = 0;
        $currentIndex = $colIndex++;

        // Remove BOM from first column if present
        $col = preg_replace('/^\xEF\xBB\xBF/', '', $col);
        $col = mb_strtolower(trim($col), 'UTF-8');

        // Skip empty columns (give them unique names to avoid conflicts)
        if (empty($col)) {
            return 'empty_' . uniqid();
        }

        // Check if this is a split time column we already mapped
        if (isset($splitTimeColumns[$currentIndex])) {
            return $splitTimeColumns[$currentIndex]['mapped'];
        }

        // Remove spaces, hyphens, underscores for comparison
        $col = str_replace([' ', '-', '_'], '', $col);

        // Map Swedish and English column names
        $mappings = [
            // Event fields
            'eventname' => 'event_name',
            'tävling' => 'event_name',
            'tavling' => 'event_name',
            'event' => 'event_name',
            'eventdate' => 'event_date',
            'tävlingsdatum' => 'event_date',
            'tavlingsdatum' => 'event_date',
            'datum' => 'event_date',
            'date' => 'event_date',
            'eventlocation' => 'event_location',
            'location' => 'event_location',
            'plats' => 'event_location',
            'ort' => 'event_location',

            // Rider fields
            'firstname' => 'firstname',
            'förnamn' => 'firstname',
            'fornamn' => 'firstname',
            'fname' => 'firstname',
            'first_name' => 'firstname',
            'lastname' => 'lastname',
            'efternamn' => 'lastname',
            'lname' => 'lastname',
            'surname' => 'lastname',
            'last_name' => 'lastname',

            // License fields
            'licensenumber' => 'license_number',
            'uciid' => 'license_number',
            'ucikod' => 'license_number',
            'sweid' => 'license_number',
            'licens' => 'license_number',
            'uci_id' => 'license_number',
            'swe_id' => 'license_number',

            // Club/Team
            'club' => 'club_name',
            'clubname' => 'club_name',
            'team' => 'club_name',
            'klubb' => 'club_name',
            'club_name' => 'club_name',
            'huvudförening' => 'club_name',
            'huvudforening' => 'club_name',

            // Category is the racing class
            'category' => 'class_name',
            'class' => 'class_name',
            'klass' => 'class_name',
            'classname' => 'class_name',

            // PWR is used in some exports but we ignore it
            'pwr' => 'pwr',

            // Position
            'position' => 'position',
            'placering' => 'position',
            'placebycategory' => 'position',
            'place' => 'position',

            // Bib number
            'bibno' => 'bib_number',
            'bibnumber' => 'bib_number',
            'bib' => 'bib_number',
            'startnummer' => 'bib_number',
            'startnr' => 'bib_number',
            'nummerlapp' => 'bib_number',

            // Time fields
            'time' => 'finish_time',
            'tid' => 'finish_time',
            'finishtime' => 'finish_time',
            'nettime' => 'finish_time',
            'nettid' => 'finish_time',
            'finish_time' => 'finish_time',
            'totaltid' => 'finish_time',
            'totaltime' => 'finish_time',

            // Status (column header variants)
            'status' => 'status',
            'fin' => 'status',
            'finish' => 'status',
            'finished' => 'status',
            'finnish' => 'status',
            'finnised' => 'status',

            // Gender
            'gender' => 'gender',
            'kön' => 'gender',
            'kon' => 'gender',

            // Nationality
            'nationality' => 'nationality',
            'nation' => 'nationality',
            'land' => 'nationality',
            'country' => 'nationality',
            'nat' => 'nationality',

            // Birth year
            'birthyear' => 'birth_year',
            'födelseår' => 'birth_year',
            'fodelsear' => 'birth_year',

            // Stage times
            'ss1' => 'ss1', 'ss2' => 'ss2', 'ss3' => 'ss3', 'ss4' => 'ss4',
            'ss5' => 'ss5', 'ss6' => 'ss6', 'ss7' => 'ss7', 'ss8' => 'ss8',
            'ss9' => 'ss9', 'ss10' => 'ss10', 'ss11' => 'ss11', 'ss12' => 'ss12',
            'ss13' => 'ss13', 'ss14' => 'ss14', 'ss15' => 'ss15',

            // DH run times
            'run1time' => 'run_1_time',
            'run_1_time' => 'run_1_time',
            'run1' => 'run_1_time',
            'åk1' => 'run_1_time',
            'ak1' => 'run_1_time',
            'kval' => 'run_1_time',
            'qualifying' => 'run_1_time',
            'run2time' => 'run_2_time',
            'run_2_time' => 'run_2_time',
            'run2' => 'run_2_time',
            'åk2' => 'run_2_time',
            'ak2' => 'run_2_time',
            'final' => 'run_2_time',

            // DH split times for run 1 (stored in ss1-ss4)
            'run1split1' => 'ss1',
            'run1split2' => 'ss2',
            'run1split3' => 'ss3',
            'run1split4' => 'ss4',
            'split11' => 'ss1',
            'split12' => 'ss2',
            'split13' => 'ss3',
            'split14' => 'ss4',

            // DH split times for run 2 (stored in ss5-ss8)
            'run2split1' => 'ss5',
            'run2split2' => 'ss6',
            'run2split3' => 'ss7',
            'run2split4' => 'ss8',
            'split21' => 'ss5',
            'split22' => 'ss6',
            'split23' => 'ss7',
            'split24' => 'ss8',
        ];

        // Check static mappings
        return $mappings[$col] ?? $col;
    }, $header);

    // Cache for lookups
    $eventCache = [];
    $riderCache = [];
    $categoryCache = [];
    $clubCache = [];
    $classCache = [];

    $lineNumber = 1;

    while (($row = fgetcsv($handle, 0, $delimiter)) !== false) {
        $lineNumber++;

        // Skip empty rows (all columns empty or only whitespace)
        if (empty(array_filter($row, function($val) { return !empty(trim($val)); }))) {
            continue;
        }

        // Skip field mapping/description rows (contain field names like "class", "position", etc.)
        if (isFieldMappingRow($row)) {
            continue;
        }

        $stats['total']++;

        // Ensure row has same number of columns as header
        if (count($row) < count($header)) {
            $row = array_pad($row, count($header), '');
        } elseif (count($row) > count($header)) {
            $row = array_slice($row, 0, count($header));
        }

        // Map row to associative array
        $data = array_combine($header, $row);

        // Validate required fields
        $hasEventMapping = !empty($IMPORT_EVENT_MAPPING);

        if (empty($data['event_name']) && !$hasEventMapping) {
            $stats['skipped']++;
            $errors[] = "Rad {$lineNumber}: Saknar tävlingsnamn och ingen event vald";
            continue;
        }

        // If no event_name but we have a mapping, use the same key as preview
        if (empty($data['event_name']) && $hasEventMapping) {
            $data['event_name'] = 'Välj event för alla resultat';
        }

        if (empty($data['firstname']) || empty($data['lastname'])) {
            $stats['skipped']++;
            $errors[] = "Rad {$lineNumber}: Saknar namn på cyklist";
            continue;
        }

        try {
            // Find event - use mapping if available
            $eventKey = $data['event_name'];
            $eventId = null;

            if (isset($eventMapping[$eventKey])) {
                $eventId = $eventMapping[$eventKey];
            } else {
                // Try to find event by name
                if (!isset($eventCache[$eventKey])) {
                    $event = $db->getRow(
                        "SELECT id FROM events WHERE name LIKE ? ORDER BY date DESC LIMIT 1",
                        ['%' . $eventKey . '%']
                    );
                    $eventCache[$eventKey] = $event ? $event['id'] : null;
                }
                $eventId = $eventCache[$eventKey];
            }

            if (!$eventId) {
                $stats['skipped']++;
                $errors[] = "Rad {$lineNumber}: Event '{$eventKey}' hittades inte";
                continue;
            }

            // Get event format for DH scoring rules (cache it)
            static $eventFormatCache = [];
            if (!isset($eventFormatCache[$eventId])) {
                $eventInfo = $db->getRow("SELECT event_format FROM events WHERE id = ?", [$eventId]);
                $eventFormatCache[$eventId] = $eventInfo['event_format'] ?? 'ENDURO';
            }
            $eventFormat = $eventFormatCache[$eventId];

            // Find or create rider
            $riderName = trim($data['firstname']) . '|' . trim($data['lastname']);
            $rawLicenseNumber = $data['license_number'] ?? '';
            // Normalize UCI-ID to standard format: XXX XXX XXX XX
            $licenseNumber = normalizeUciId($rawLicenseNumber);
            // For database comparison, strip spaces
            $licenseNumberDigits = preg_replace('/[^0-9]/', '', $licenseNumber);

            // IMPORTANT: Use UCI-ID as PRIMARY cache key if available
            // This ensures same UCI = same rider, regardless of name variations
            $cacheKey = !empty($licenseNumberDigits) ? "UCI:{$licenseNumberDigits}" : "NAME:{$riderName}";

            if (!isset($riderCache[$cacheKey])) {
                // Try to find rider by license number first (normalized)
                $rider = null;
                if (!empty($licenseNumberDigits)) {
                    // Try exact match with normalized number (compare digits only)
                    $rider = $db->getRow(
                        "SELECT id, firstname, lastname FROM riders WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?",
                        [$licenseNumberDigits]
                    );
                    if ($rider) {
                        $matching_stats['riders_found']++;
                        error_log("IMPORT: UCI match found - UCI:{$licenseNumberDigits} → rider ID {$rider['id']} ({$rider['firstname']} {$rider['lastname']})");

                        // Update rider nationality if provided in CSV (always override if provided)
                        $importNationality = strtoupper(trim($data['nationality'] ?? ''));
                        if (!empty($importNationality) && strlen($importNationality) <= 3) {
                            $riderNat = $db->getRow("SELECT nationality FROM riders WHERE id = ?", [$rider['id']]);
                            if (empty($riderNat['nationality']) || $riderNat['nationality'] !== $importNationality) {
                                $db->update('riders', ['nationality' => $importNationality], 'id = ?', [$rider['id']]);
                                $matching_stats['riders_updated_with_nationality'] = ($matching_stats['riders_updated_with_nationality'] ?? 0) + 1;
                                error_log("IMPORT: Updated rider {$rider['id']} nationality to: {$importNationality}");
                            }
                        }

                        // Update rider birth_year if provided in CSV and rider doesn't have it
                        $importBirthYear = trim($data['birth_year'] ?? '');
                        if (!empty($importBirthYear) && is_numeric($importBirthYear)) {
                            $importBirthYear = (int)$importBirthYear;
                            if ($importBirthYear >= 1940 && $importBirthYear <= (int)date('Y')) {
                                $riderData = $db->getRow("SELECT birth_year FROM riders WHERE id = ?", [$rider['id']]);
                                if (empty($riderData['birth_year'])) {
                                    $db->update('riders', ['birth_year' => $importBirthYear], 'id = ?', [$rider['id']]);
                                    $matching_stats['riders_updated_with_birthyear'] = ($matching_stats['riders_updated_with_birthyear'] ?? 0) + 1;
                                    error_log("IMPORT: Updated rider {$rider['id']} birth_year to: {$importBirthYear}");
                                }
                            }
                        }
                    }
                }

                // Try by name if no license match - use UPPER() for case-insensitive matching
                if (!$rider) {
                    $firstName = trim($data['firstname']);
                    $lastName = trim($data['lastname']);
                    $importClubName = trim($data['club_name'] ?? '');

                    // SMART MATCHING: If we have club info, prioritize name+club match
                    // Same name + same club = almost certainly same person
                    if (!empty($importClubName)) {
                        // First try: name + club match (strongest signal)
                        $normalizedImportClub = normalizeClubName($importClubName);
                        $rider = $db->getRow(
                            "SELECT r.id, r.license_number FROM riders r
                             LEFT JOIN clubs c ON r.club_id = c.id
                             WHERE UPPER(r.firstname) = UPPER(?) AND UPPER(r.lastname) = UPPER(?)
                             AND c.id IS NOT NULL
                             ORDER BY
                                CASE WHEN UPPER(c.name) = UPPER(?) THEN 0
                                     WHEN UPPER(REPLACE(REPLACE(c.name, 'CK', 'Ck'), 'OK', 'Ok')) LIKE CONCAT('%', UPPER(?), '%') THEN 1
                                     ELSE 2 END,
                                r.id ASC
                             LIMIT 1",
                            [$firstName, $lastName, $importClubName, $normalizedImportClub]
                        );

                        if ($rider) {
                            error_log("IMPORT: Name+Club match - '{$firstName} {$lastName}' + club '{$importClubName}' → rider ID {$rider['id']}");
                        }
                    }

                    // Second try: exact name match (any club)
                    // If multiple riders have same name, prefer one with compatible birth year
                    if (!$rider) {
                        $className = $data['class_name'] ?? '';
                        $possibleBirthYears = getBirthYearsFromClassName($className);

                        // Get ALL riders with this name
                        $nameMatches = $db->getAll(
                            "SELECT id, license_number, birth_year FROM riders WHERE UPPER(firstname) = UPPER(?) AND UPPER(lastname) = UPPER(?)",
                            [$firstName, $lastName]
                        );

                        if (!empty($nameMatches)) {
                            if (count($nameMatches) === 1) {
                                // Only one match - use it
                                $rider = $nameMatches[0];
                            } elseif (!empty($possibleBirthYears)) {
                                // Multiple matches - prefer one with compatible birth year
                                foreach ($nameMatches as $match) {
                                    if (!empty($match['birth_year']) && in_array((int)$match['birth_year'], $possibleBirthYears)) {
                                        $rider = $match;
                                        error_log("IMPORT: Name match with birth year verification - class '{$className}' matches birth year {$match['birth_year']}");
                                        break;
                                    }
                                }
                                // If no birth year match, try one without birth year (can update it)
                                if (!$rider) {
                                    foreach ($nameMatches as $match) {
                                        if (empty($match['birth_year'])) {
                                            $rider = $match;
                                            error_log("IMPORT: Name match with empty birth year - will update from class '{$className}'");
                                            break;
                                        }
                                    }
                                }
                                // Last resort - use first match
                                if (!$rider) {
                                    $rider = $nameMatches[0];
                                }
                            } else {
                                // No age class info - use first match
                                $rider = $nameMatches[0];
                            }
                        }
                    }

                    // Third try: FUZZY matching for middle names
                    // "Lo Nyberg Zetterlund" should match existing "Lo Zetterlund"
                    // "Lo Zetterlund" should match existing "Lo Nyberg Zetterlund"
                    if (!$rider) {
                        $firstNamePart = explode(' ', $firstName)[0]; // Get first part of firstname

                        $rider = $db->getRow(
                            "SELECT id, license_number FROM riders
                             WHERE (UPPER(firstname) LIKE CONCAT(UPPER(?), '%') OR UPPER(firstname) = UPPER(?))
                             AND UPPER(lastname) = UPPER(?)",
                            [$firstNamePart, $firstNamePart, $lastName]
                        );

                        if ($rider) {
                            error_log("IMPORT: Fuzzy firstname match - '{$firstName} {$lastName}' matched first part '{$firstNamePart}' → rider ID {$rider['id']}");
                        }
                    }

                    if ($rider) {
                        $matching_stats['riders_found']++;
                        error_log("IMPORT: Name match found - '{$firstName} {$lastName}' → rider ID {$rider['id']}");

                        // If we found by name and import has UCI ID but rider doesn't - update rider
                        if (!empty($licenseNumber) && empty($rider['license_number'])) {
                            $db->update('riders', [
                                'license_number' => $licenseNumber
                            ], 'id = ?', [$rider['id']]);
                            $matching_stats['riders_updated_with_uci'] = ($matching_stats['riders_updated_with_uci'] ?? 0) + 1;
                            error_log("IMPORT: Updated rider {$rider['id']} with UCI: {$licenseNumber}");
                        }

                        // Update rider nationality if provided in CSV (always override if provided)
                        $importNationality = strtoupper(trim($data['nationality'] ?? ''));
                        if (!empty($importNationality) && strlen($importNationality) <= 3) {
                            $riderNat = $db->getRow("SELECT nationality FROM riders WHERE id = ?", [$rider['id']]);
                            if (empty($riderNat['nationality']) || $riderNat['nationality'] !== $importNationality) {
                                $db->update('riders', ['nationality' => $importNationality], 'id = ?', [$rider['id']]);
                                $matching_stats['riders_updated_with_nationality'] = ($matching_stats['riders_updated_with_nationality'] ?? 0) + 1;
                                error_log("IMPORT: Updated rider {$rider['id']} nationality to: {$importNationality}");
                            }
                        }

                        // Update rider birth_year if provided in CSV and rider doesn't have it
                        $importBirthYear = trim($data['birth_year'] ?? '');
                        $riderData = $db->getRow("SELECT birth_year FROM riders WHERE id = ?", [$rider['id']]);

                        if (!empty($importBirthYear) && is_numeric($importBirthYear)) {
                            $importBirthYear = (int)$importBirthYear;
                            if ($importBirthYear >= 1940 && $importBirthYear <= (int)date('Y')) {
                                if (empty($riderData['birth_year'])) {
                                    $db->update('riders', ['birth_year' => $importBirthYear], 'id = ?', [$rider['id']]);
                                    $matching_stats['riders_updated_with_birthyear'] = ($matching_stats['riders_updated_with_birthyear'] ?? 0) + 1;
                                    error_log("IMPORT: Updated rider {$rider['id']} birth_year to: {$importBirthYear}");
                                }
                            }
                        }
                        // NOTE: We do NOT infer birth year from class name - only use explicit data
                    } else {
                        error_log("IMPORT: No match found for '{$firstName} {$lastName}' UCI:{$licenseNumberDigits}");
                    }
                }

                // Create new rider if not found
                if (!$rider) {
                    $matching_stats['riders_not_found']++;
                    $matching_stats['riders_created']++;

                    // Determine gender from class name if available
                    $gender = 'M';
                    $className = $data['class_name'] ?? '';
                    if (preg_match('/(dam|women|female|flickor|girls)/i', $className)) {
                        $gender = 'F';
                    } elseif (preg_match('/(herr|men|male|pojkar|boys)/i', $className)) {
                        $gender = 'M';
                    }

                    // Generate SWE license number if no UCI ID provided
                    $finalLicenseNumber = $licenseNumber ?: generateSweLicenseNumber($db);

                    // Get nationality from import if available
                    $importNationality = strtoupper(trim($data['nationality'] ?? ''));
                    if (strlen($importNationality) > 3) $importNationality = '';

                    // Get birth year from import if available - NEVER infer/guess
                    $importBirthYear = trim($data['birth_year'] ?? '');
                    if (!empty($importBirthYear) && is_numeric($importBirthYear)) {
                        $importBirthYear = (int)$importBirthYear;
                        // Validate reasonable birth year range (1940-current year)
                        if ($importBirthYear < 1940 || $importBirthYear > (int)date('Y')) {
                            $importBirthYear = null;
                        }
                    } else {
                        $importBirthYear = null;
                    }

                    $riderId = $db->insert('riders', [
                        'firstname' => trim($data['firstname']),
                        'lastname' => trim($data['lastname']),
                        'license_number' => $finalLicenseNumber,
                        'gender' => $gender,
                        'nationality' => !empty($importNationality) ? $importNationality : null,
                        'birth_year' => $importBirthYear
                    ]);

                    // Track for rollback
                    if ($importId) {
                        trackImportRecord($db, $importId, 'rider', $riderId, 'created');
                    }

                    error_log("IMPORT: Created new rider ID {$riderId} for '{$data['firstname']} {$data['lastname']}' UCI:{$licenseNumberDigits}");
                    $riderCache[$cacheKey] = $riderId;
                } else {
                    $riderCache[$cacheKey] = $rider['id'];
                }
            }

            $riderId = $riderCache[$cacheKey];

            // Find or create club using smart matching
            $clubId = null;
            $clubName = trim($data['club_name'] ?? '');
            if (!empty($clubName)) {
                // Normalize the club name for cache key to catch variants
                $normalizedClubName = normalizeClubName($clubName);
                $clubCacheKey = !empty($normalizedClubName) ? $normalizedClubName : $clubName;

                if (!isset($clubCache[$clubCacheKey])) {
                    // Use smart matching (handles CK/Ck, OK/Ok variants, etc.)
                    $club = findClubByName($db, $clubName);

                    if (!$club) {
                        // Create club with the original name from CSV
                        $matching_stats['clubs_created']++;
                        $newClubId = $db->insert('clubs', [
                            'name' => $clubName,
                            'active' => 1
                        ]);
                        if ($importId) {
                            trackImportRecord($db, $importId, 'club', $newClubId, 'created');
                        }
                        $clubCache[$clubCacheKey] = $newClubId;
                    } else {
                        $clubCache[$clubCacheKey] = $club['id'];
                    }
                }
                $clubId = $clubCache[$clubCacheKey];
            }

            // Find or create class
            $classId = $forceClassId;
            $className = trim($data['class_name'] ?? '');
            if (!$classId && !empty($className)) {
                // IMPORTANT: Check user mapping FIRST, before any normalization
                // The mapping from preview page uses the original CSV class name
                global $IMPORT_CLASS_MAPPINGS;
                $originalClassName = $className;

                if (isset($IMPORT_CLASS_MAPPINGS[$originalClassName])) {
                    // User has explicitly mapped this class - use their choice
                    if (!isset($classCache[$originalClassName])) {
                        $classCache[$originalClassName] = $IMPORT_CLASS_MAPPINGS[$originalClassName];
                    }
                    $classId = $classCache[$originalClassName];
                } else {
                    // No user mapping - apply automatic normalization
                    // Maps common class name variants to canonical names
                    $classNameMappings = [
                        // Herrar Elit variants
                        'tävling herrar' => 'Herrar Elit',
                        'tavling herrar' => 'Herrar Elit',
                        'herrar tävling' => 'Herrar Elit',
                        'herrar tavling' => 'Herrar Elit',
                        'elit herrar' => 'Herrar Elit',
                        'herr elit' => 'Herrar Elit',
                        'elite men' => 'Herrar Elit',
                        'men elite' => 'Herrar Elit',
                        // Damer Elit variants
                        'tävling damer' => 'Damer Elit',
                        'tavling damer' => 'Damer Elit',
                        'damer tävling' => 'Damer Elit',
                        'damer tavling' => 'Damer Elit',
                        'elit damer' => 'Damer Elit',
                        'dam elit' => 'Damer Elit',
                        'elite women' => 'Damer Elit',
                        'women elite' => 'Damer Elit',
                    ];
                    $normalizedClassName = strtolower(trim($className));
                    if (isset($classNameMappings[$normalizedClassName])) {
                        $className = $classNameMappings[$normalizedClassName];
                    }

                    if (!isset($classCache[$className])) {
                        // Try alias match first (from class_aliases table)
                        $class = null;
                        try {
                            $aliasMatch = $db->getRow(
                                "SELECT class_id FROM class_aliases WHERE LOWER(alias) = LOWER(?)",
                                [$className]
                            );
                            if ($aliasMatch) {
                                $class = ['id' => $aliasMatch['class_id']];
                                error_log("IMPORT: Class alias match - '{$className}' → class_id {$aliasMatch['class_id']}");
                            }
                        } catch (Exception $e) {
                            // class_aliases table might not exist yet
                        }

                        // Try exact match (case-insensitive) - NO partial matching to avoid "Herrar" matching "Herrar Junior"
                        if (!$class) {
                            $class = $db->getRow(
                                "SELECT id FROM classes WHERE LOWER(display_name) = LOWER(?) OR LOWER(name) = LOWER(?)",
                                [$className, $className]
                            );
                        }

                        // NO partial match - it causes wrong matches like "Herrar" -> "Herrar Junior"
                        // If exact match fails, create new class - user can merge later with fix-event-classes.php

                        if (!$class) {
                            // Create class
                            $matching_stats['classes_created']++;
                            $newClassId = $db->insert('classes', [
                                'name' => strtolower(str_replace(' ', '_', $className)),
                                'display_name' => $className,
                                'active' => 1
                            ]);
                            if ($importId) {
                                trackImportRecord($db, $importId, 'class', $newClassId, 'created');
                            }
                            $classCache[$className] = $newClassId;
                        } else {
                            $classCache[$className] = $class['id'];
                        }
                        $classId = $classCache[$className];
                    } else {
                        $classId = $classCache[$className];
                    }
                }
            }

            // Validate class gender matches rider gender
            // TRUST THE CLASS NAME - if mismatch, update rider's gender (not the class)
            if ($classId) {
                $riderInfo = $db->getRow("SELECT gender, birth_year FROM riders WHERE id = ?", [$riderId]);
                if ($riderInfo) {
                    // Check what gender the class name suggests
                    $classIsFemale = preg_match('/(dam|women|female|flickor|girls|^[FK][\d\-])/i', $className);
                    $classIsMale = preg_match('/(herr|men|male|pojkar|boys|^[MP][\d\-])/i', $className);
                    $riderIsFemale = in_array($riderInfo['gender'], ['F', 'K']);

                    // Gender mismatch detected - trust the class and update rider's gender
                    if ($classIsFemale && !$riderIsFemale) {
                        // Class is female but rider is registered as male - fix rider
                        $db->update('riders', ['gender' => 'K'], 'id = ?', [$riderId]);
                        error_log("Import: Updated rider {$data['firstname']} {$data['lastname']} gender to K (was M, racing in '$className')");
                        $matching_stats['riders_gender_corrected'] = ($matching_stats['riders_gender_corrected'] ?? 0) + 1;
                    } elseif ($classIsMale && $riderIsFemale) {
                        // Class is male but rider is registered as female - fix rider
                        $db->update('riders', ['gender' => 'M'], 'id = ?', [$riderId]);
                        error_log("Import: Updated rider {$data['firstname']} {$data['lastname']} gender to M (was K, racing in '$className')");
                        $matching_stats['riders_gender_corrected'] = ($matching_stats['riders_gender_corrected'] ?? 0) + 1;
                    }
                }
            }

            // Parse time
            $finishTime = null;
            $timeStr = trim($data['finish_time'] ?? '');
            if (!empty($timeStr) && $timeStr !== 'DNF' && $timeStr !== 'DNS' && $timeStr !== 'DQ') {
                $finishTime = $timeStr;
            }

            // For DH: Calculate finish_time from Run1/Run2 if NetTime is empty
            // Auto-detect: If we have Run1/Run2 data but no finish_time, calculate it
            $run1 = trim($data['run_1_time'] ?? '');
            $run2 = trim($data['run_2_time'] ?? '');
            $hasRunData = !empty($run1) || !empty($run2);

            if (empty($finishTime) && $hasRunData) {
                // Helper function to convert time string to seconds for comparison
                $timeToSeconds = function($timeStr) {
                    if (empty($timeStr) || in_array(strtoupper($timeStr), ['DNF', 'DNS', 'DQ', 'DSQ'])) {
                        return PHP_FLOAT_MAX; // Invalid times are "slower" than any valid time
                    }
                    // Treat "0:00", "0:00:00", "0:00.00" etc as invalid (no time recorded)
                    if (preg_match('/^0+[:.]?0*[:.]?0*$/', $timeStr)) {
                        return PHP_FLOAT_MAX;
                    }
                    // Handle formats like "1:38.227" (m:ss.ms) or "98.227" (ss.ms)
                    if (preg_match('/^(\d+):(\d+)\.(\d+)$/', $timeStr, $m)) {
                        return ((int)$m[1] * 60) + (int)$m[2] + ((int)$m[3] / pow(10, strlen($m[3])));
                    } elseif (preg_match('/^(\d+)\.(\d+)$/', $timeStr, $m)) {
                        return (int)$m[1] + ((int)$m[2] / pow(10, strlen($m[2])));
                    } elseif (preg_match('/^(\d+):(\d+):(\d+)\.(\d+)$/', $timeStr, $m)) {
                        // h:mm:ss.ms format
                        return ((int)$m[1] * 3600) + ((int)$m[2] * 60) + (int)$m[3] + ((int)$m[4] / pow(10, strlen($m[4])));
                    }
                    return PHP_FLOAT_MAX;
                };

                if ($eventFormat === 'DH_SWECUP') {
                    // SweCUP: Only Run 2 (Final) counts for ranking/points
                    if (!empty($run2) && !in_array(strtoupper($run2), ['DNF', 'DNS', 'DQ', 'DSQ']) && !preg_match('/^0+[:.]?0*[:.]?0*$/', $run2)) {
                        $finishTime = $run2;
                    }
                } else {
                    // DH_STANDARD or auto-detect: Best (fastest) of both runs
                    $run1Seconds = $timeToSeconds($run1);
                    $run2Seconds = $timeToSeconds($run2);

                    if ($run1Seconds < PHP_FLOAT_MAX || $run2Seconds < PHP_FLOAT_MAX) {
                        if ($run1Seconds <= $run2Seconds && $run1Seconds < PHP_FLOAT_MAX) {
                            $finishTime = $run1;
                        } elseif ($run2Seconds < PHP_FLOAT_MAX) {
                            $finishTime = $run2;
                        }
                    }
                }

                if (!empty($finishTime)) {
                    error_log("IMPORT DH: Calculated finish_time '{$finishTime}' from Run1='{$run1}' Run2='{$run2}' for {$data['firstname']} {$data['lastname']}");
                }
            }

            // Determine status
            $status = strtolower(trim($data['status'] ?? 'finished'));
            if (in_array($status, ['fin', 'finish', 'finished', 'finnished', 'ok', ''])) {
                $status = 'finished';
            } elseif (in_array($status, ['dnf', 'did not finish'])) {
                $status = 'dnf';
            } elseif (in_array($status, ['dns', 'did not start'])) {
                $status = 'dns';
            } elseif (in_array($status, ['dq', 'disqualified'])) {
                $status = 'dq';
            }

            // Check if result already exists for this rider in this class
            // NOTE: We check class_id to allow riders to compete in multiple classes per event
            // Using <=> for NULL-safe comparison (rider can have one result per class per event)
            $existingResult = $db->getRow(
                "SELECT id FROM results WHERE event_id = ? AND cyclist_id = ? AND class_id <=> ?",
                [$eventId, $riderId, $classId]
            );

            // Calculate points based on position (only if class awards points)
            $positionRaw = trim($data['position'] ?? '');
            $isEBike = false;
            $position = null;
            $points = 0;

            // Check for E-BIKE in position field (case-insensitive)
            // E-BIKE participants are sorted by time but don't receive points or count in series
            if (stripos($positionRaw, 'e-bike') !== false || stripos($positionRaw, 'ebike') !== false) {
                $isEBike = true;
                $position = null; // No numeric position for E-BIKE
                $points = 0; // No points for E-BIKE
            } elseif (!empty($positionRaw) && is_numeric($positionRaw)) {
                $position = (int)$positionRaw;
            }

            // DNS/DNF/DQ riders should NOT have a position
            if (in_array($status, ['dns', 'dnf', 'dq'])) {
                $position = null;
            }

            // Check if class awards points
            $awardsPoints = true;
            if ($classId) {
                $classSettings = $db->getRow("SELECT awards_points FROM classes WHERE id = ?", [$classId]);
                if ($classSettings && isset($classSettings['awards_points'])) {
                    $awardsPoints = (bool)$classSettings['awards_points'];
                }
            }

            // Only calculate points if not E-BIKE and class awards points
            if (!$isEBike && $status === 'finished' && $position && $awardsPoints) {
                // Use the event's point scale from point_scales table
                // Pass class_id so calculatePoints can double-check class eligibility
                $points = calculatePoints($db, $eventId, $position, $status, $classId);
            }

            // Get club_id for this result (year-locked club membership)
            // Include club-membership.php if not already included
            if (!function_exists('getRiderClubForYear')) {
                require_once __DIR__ . '/club-membership.php';
            }

            // Get event date to determine the season year
            $eventDateInfo = $db->getRow("SELECT date FROM events WHERE id = ?", [$eventId]);
            $eventYear = $eventDateInfo ? (int)date('Y', strtotime($eventDateInfo['date'])) : (int)date('Y');

            // FIXED: First race of year should set the club, then lock it
            // Check if rider already has a LOCKED club for this year (has results)
            $existingSeasonClub = $db->getRow(
                "SELECT club_id, locked FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?",
                [$riderId, $eventYear]
            );

            $resultClubId = null;

            // Check if rider currently has a club set in their profile
            $riderProfile = $db->getRow("SELECT club_id FROM riders WHERE id = ?", [$riderId]);
            $riderHasNoClub = empty($riderProfile['club_id']);

            // Update rider's profile club_id if:
            // 1. Importing CURRENT year results (or future)
            // 2. OR rider has no club set yet (even for historical imports)
            $currentYear = (int)date('Y');
            $shouldUpdateProfileClub = ($eventYear >= $currentYear) || $riderHasNoClub;

            // If forceClubUpdate is true, always use the CSV club (ignore locked status)
            if ($clubId && $forceClubUpdate) {
                // Force update: use club from CSV regardless of locked status
                $resultClubId = $clubId;
                setRiderClubForYear($db, $riderId, $clubId, $eventYear, true);  // Pass true to force update locked entries
                lockRiderClubForYear($db, $riderId, $eventYear);
                // Update profile club
                if ($shouldUpdateProfileClub) {
                    $db->update('riders', ['club_id' => $clubId], 'id = ?', [$riderId]);
                }
            } elseif ($existingSeasonClub && $existingSeasonClub['locked'] && !$forceClubUpdate) {
                // Rider already has results this year - use their locked club
                $resultClubId = $existingSeasonClub['club_id'];
                // Still update profile if rider has no club
                if ($riderHasNoClub && $resultClubId) {
                    $db->update('riders', ['club_id' => $resultClubId], 'id = ?', [$riderId]);
                }
            } elseif ($clubId) {
                // First race of the year OR not locked: use club from CSV
                // This is the key fix: CSV club takes precedence for first race
                $resultClubId = $clubId;
                // Set/update this as the rider's club for the year
                setRiderClubForYear($db, $riderId, $clubId, $eventYear);
                lockRiderClubForYear($db, $riderId, $eventYear);
                // Update profile club if current year OR rider has no club
                if ($shouldUpdateProfileClub) {
                    $db->update('riders', ['club_id' => $clubId], 'id = ?', [$riderId]);
                }
            } else {
                // No club in CSV, use rider's profile club
                $resultClubId = getRiderClubForYear($db, $riderId, $eventYear, true);
            }

            $resultData = [
                'event_id' => $eventId,
                'cyclist_id' => $riderId,
                'club_id' => $resultClubId,
                'class_id' => $classId,
                'bib_number' => $data['bib_number'] ?? null,
                'position' => $position,
                'finish_time' => $finishTime,
                'status' => $status,
                'points' => $points,
                'is_ebike' => $isEBike ? 1 : 0,
                'run_1_time' => $data['run_1_time'] ?? null,
                'run_2_time' => $data['run_2_time'] ?? null,
                'ss1' => $data['ss1'] ?? null,
                'ss2' => $data['ss2'] ?? null,
                'ss3' => $data['ss3'] ?? null,
                'ss4' => $data['ss4'] ?? null,
                'ss5' => $data['ss5'] ?? null,
                'ss6' => $data['ss6'] ?? null,
                'ss7' => $data['ss7'] ?? null,
                'ss8' => $data['ss8'] ?? null,
                'ss9' => $data['ss9'] ?? null,
                'ss10' => $data['ss10'] ?? null,
                'ss11' => $data['ss11'] ?? null,
                'ss12' => $data['ss12'] ?? null,
                'ss13' => $data['ss13'] ?? null,
                'ss14' => $data['ss14'] ?? null,
                'ss15' => $data['ss15'] ?? null,
            ];

            if ($existingResult) {
                // Update existing
                $oldData = $db->getRow("SELECT * FROM results WHERE id = ?", [$existingResult['id']]);

                // Track what changed
                $changes = [];
                foreach ($resultData as $field => $newValue) {
                    $oldValue = $oldData[$field] ?? null;
                    // Normalize for comparison (treat empty string as null)
                    $oldNorm = ($oldValue === '' || $oldValue === null) ? null : $oldValue;
                    $newNorm = ($newValue === '' || $newValue === null) ? null : $newValue;
                    if ($oldNorm !== $newNorm) {
                        $changes[$field] = ['old' => $oldValue, 'new' => $newValue];
                    }
                }

                if (!empty($changes)) {
                    $db->update('results', $resultData, 'id = ?', [$existingResult['id']]);
                    $stats['updated']++;
                    $changelog[] = [
                        'rider' => $data['firstname'] . ' ' . $data['lastname'],
                        'changes' => $changes
                    ];
                    if ($importId) {
                        trackImportRecord($db, $importId, 'result', $existingResult['id'], 'updated', $oldData);
                    }
                } else {
                    // No changes, count as skipped
                    $stats['skipped']++;
                }
            } else {
                // Insert new
                $resultId = $db->insert('results', $resultData);
                $stats['success']++;

                // Lock the rider's club for this year (they now have results)
                lockRiderClubForYear($db, $riderId, $eventYear);

                if ($importId) {
                    trackImportRecord($db, $importId, 'result', $resultId, 'created');
                }
            }

        } catch (Exception $e) {
            $stats['failed']++;
            $errors[] = "Rad {$lineNumber}: " . $e->getMessage();
        }
    }

    fclose($handle);

    // Apply automatic stage bonus if series has it configured
    $stageBonusApplied = applySeriesStageBonusForEvent($db, $eventMapping['event_id'] ?? null);
    if ($stageBonusApplied > 0) {
        $matching_stats['stage_bonus_applied'] = $stageBonusApplied;
    }

    return [
        'stats' => $stats,
        'matching' => $matching_stats,
        'errors' => $errors,
        'stage_names' => $stageNamesMapping,
        'changelog' => $changelog
    ];
}

/**
 * Apply series stage bonus points for a specific event
 * Called automatically after import if series has stage_bonus_config
 *
 * @param Database $db
 * @param int $eventId
 * @return int Number of riders who got bonus points
 */
function applySeriesStageBonusForEvent($db, $eventId) {
    if (!$eventId) return 0;

    try {
        // Get series for this event (via series_events junction table or direct series_id)
        $seriesConfig = $db->getRow("
            SELECT s.stage_bonus_config
            FROM series s
            INNER JOIN series_events se ON s.id = se.series_id
            WHERE se.event_id = ?
            LIMIT 1
        ", [$eventId]);

        // Fallback: check direct series_id on event
        if (!$seriesConfig) {
            $seriesConfig = $db->getRow("
                SELECT s.stage_bonus_config
                FROM series s
                INNER JOIN events e ON s.id = e.series_id
                WHERE e.id = ?
            ", [$eventId]);
        }

        if (!$seriesConfig || empty($seriesConfig['stage_bonus_config'])) {
            return 0;
        }

        $config = json_decode($seriesConfig['stage_bonus_config'], true);
        if (!$config || !($config['enabled'] ?? false)) {
            return 0;
        }

        $stage = $config['stage'] ?? 'ss1';
        $pointValues = $config['points'] ?? [25, 20, 16];
        $classIds = $config['class_ids'] ?? null;

        // Validate stage column name
        $stageColumn = preg_replace('/[^a-z0-9_]/', '', $stage);
        if (!preg_match('/^ss\d+$/', $stageColumn)) {
            return 0;
        }

        // Get results for this event with stage times
        $sql = "
            SELECT r.id as result_id, r.class_id, r.{$stageColumn} as stage_time
            FROM results r
            WHERE r.event_id = ?
              AND r.{$stageColumn} IS NOT NULL
              AND r.{$stageColumn} != ''
              AND r.{$stageColumn} != '0'
        ";
        $params = [$eventId];

        if (!empty($classIds)) {
            $placeholders = implode(',', array_fill(0, count($classIds), '?'));
            $sql .= " AND r.class_id IN ({$placeholders})";
            $params = array_merge($params, $classIds);
        }

        $sql .= " ORDER BY r.class_id, r.{$stageColumn} ASC";

        $results = $db->getAll($sql, $params);

        if (empty($results)) {
            return 0;
        }

        // Group by class
        $byClass = [];
        foreach ($results as $result) {
            $cId = $result['class_id'] ?? 0;
            if (!isset($byClass[$cId])) {
                $byClass[$cId] = [];
            }
            $byClass[$cId][] = $result;
        }

        // Apply bonus points per class
        $updated = 0;
        foreach ($byClass as $cId => $classResults) {
            $rank = 1;
            foreach ($classResults as $result) {
                if ($rank <= count($pointValues)) {
                    $bonusPoints = $pointValues[$rank - 1];
                    $db->query(
                        "UPDATE results SET points = COALESCE(points, 0) + ? WHERE id = ?",
                        [$bonusPoints, $result['result_id']]
                    );
                    $updated++;
                }
                $rank++;
            }
        }

        if ($updated > 0) {
            error_log("Import: Applied stage bonus ({$stage}) to {$updated} riders for event {$eventId}");
        }

        return $updated;

    } catch (Exception $e) {
        error_log("Import: Failed to apply stage bonus: " . $e->getMessage());
        return 0;
    }
}
