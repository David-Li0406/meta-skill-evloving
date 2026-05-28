<?php
/**
 * V3 Event Page - Complete port from V2
 * Includes: Results, Information, PM, Jury, Schedule, Start times, Map, Registered, Tickets, Registration
 */

$db = hub_db();
$eventId = intval($pageInfo['params']['id'] ?? 0);

if (!$eventId) {
    header('Location: /results');
    exit;
}

// Check if user can edit this event (admins + promotors assigned to this event)
$canEditEvent = function_exists('canAccessEvent') && canAccessEvent($eventId);

// Helper functions (only define if not already defined)
if (!function_exists('timeToSeconds')) {
    function timeToSeconds($time) {
        if (empty($time)) return PHP_INT_MAX;
        // Treat "0:00", "0:00:00" etc as invalid (no time recorded)
        if (preg_match('/^0+[:.]?0*[:.]?0*$/', $time)) return PHP_INT_MAX;
        // Treat status values as invalid (including 'finished' that may end up in time columns)
        if (in_array(strtolower(trim($time)), ['dns', 'dnf', 'dq', 'dsq', 'finished', 'fin', 'finish', 'finnished', 'ok'])) return PHP_INT_MAX;
        $decimal = 0;
        if (preg_match('/(\.\d+)$/', $time, $matches)) {
            $decimal = floatval($matches[1]);
            $time = preg_replace('/\.\d+$/', '', $time);
        }
        $parts = explode(':', $time);
        $seconds = 0;
        if (count($parts) === 3) {
            $seconds = (int)$parts[0] * 3600 + (int)$parts[1] * 60 + (int)$parts[2];
        } elseif (count($parts) === 2) {
            $seconds = (int)$parts[0] * 60 + (int)$parts[1];
        } elseif (count($parts) === 1) {
            $seconds = (int)$parts[0];
        }
        $total = $seconds + $decimal;
        // Return invalid for times under 1 second (impossible for DH)
        return $total < 1 ? PHP_INT_MAX : $total;
    }
}

if (!function_exists('formatDisplayTime')) {
    function formatDisplayTime($time) {
        if (empty($time)) return null;
        // Treat "0:00" etc as no time
        if (preg_match('/^0+[:.]?0*[:.]?0*$/', $time)) return null;
        // Treat status values as no time (including 'finished' that may end up in time columns)
        if (in_array(strtolower(trim($time)), ['dns', 'dnf', 'dq', 'dsq', 'finished', 'fin', 'finish', 'finnished', 'ok'])) return null;
        $decimal = '';
        if (preg_match('/(\.\d+)$/', $time, $matches)) {
            $decimal = $matches[1];
            $time = preg_replace('/\.\d+$/', '', $time);
        }
        $parts = explode(':', $time);
        if (count($parts) === 3) {
            $hours = (int)$parts[0];
            $minutes = (int)$parts[1];
            $seconds = (int)$parts[2];
            if ($hours > 0) {
                return $hours . ':' . sprintf('%02d', $minutes) . ':' . sprintf('%02d', $seconds) . $decimal;
            } else {
                return $minutes . ':' . sprintf('%02d', $seconds) . $decimal;
            }
        }
        return $time . $decimal;
    }
}

if (!function_exists('getEventContent')) {
    function getEventContent($event, $field, $useGlobalField, $globalTextMap, $hiddenField = null) {
        // Check if content is hidden
        if ($hiddenField && !empty($event[$hiddenField])) {
            return '';
        }
        if (!empty($event[$useGlobalField]) && !empty($globalTextMap[$field])) {
            return $globalTextMap[$field];
        }
        return $event[$field] ?? '';
    }
}

try {
    // Fetch event details with venue info
    // Note: Uses only core columns that exist in base schema
    // organizer_club_id might not exist if migration 053 not run
    $stmt = $db->prepare("
        SELECT
            e.*,
            s.id as series_id,
            s.name as series_name,
            s.logo as series_logo,
            s.gradient_start as series_gradient_start,
            s.gradient_end as series_gradient_end,
            s.organizer as series_organizer,
            v.name as venue_name,
            v.city as venue_city,
            v.address as venue_address
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        LEFT JOIN venues v ON e.venue_id = v.id
        WHERE e.id = ?
    ");
    $stmt->execute([$eventId]);
    $event = $stmt->fetch(PDO::FETCH_ASSOC);

    // Try to get organizer club info if the column exists
    if ($event && isset($event['organizer_club_id']) && $event['organizer_club_id']) {
        try {
            $clubStmt = $db->prepare("SELECT id, name FROM clubs WHERE id = ?");
            $clubStmt->execute([$event['organizer_club_id']]);
            $orgClub = $clubStmt->fetch(PDO::FETCH_ASSOC);
            if ($orgClub) {
                $event['organizer_club_name'] = $orgClub['name'];
                $event['organizer_club_id_ref'] = $orgClub['id'];
            }
        } catch (PDOException $e) {
            // Column or table doesn't exist
        }
    }

    if (!$event) {
        include HUB_ROOT . '/pages/404.php';
        return;
    }

    // Fetch global texts for use_global functionality
    $globalTextMap = [];
    try {
        $globalTexts = $db->query("SELECT field_key, content FROM global_texts WHERE is_active = 1")->fetchAll(PDO::FETCH_ASSOC);
        foreach ($globalTexts as $gt) {
            $globalTextMap[$gt['field_key']] = $gt['content'];
        }
    } catch (PDOException $e) {
        // Table might not exist yet
    }

    // Check for interactive map (GPX data)
    require_once INCLUDES_PATH . '/map_functions.php';
    $hasInteractiveMap = eventHasMap($db, $eventId);

    // Check for race reports/news linked to this event
    $eventReportsCount = 0;
    try {
        $reportsStmt = $db->prepare("SELECT COUNT(*) FROM race_reports WHERE event_id = ? AND status = 'published'");
        $reportsStmt->execute([$eventId]);
        $eventReportsCount = (int)$reportsStmt->fetchColumn();
    } catch (PDOException $e) {
        // Table might not exist yet
    }

    // Fetch sponsors - series sponsors take priority over event sponsors
    // Include all logo fields for placement-specific logos
    require_once INCLUDES_PATH . '/sponsor-functions.php';
    $eventSponsors = ['header' => [], 'content' => [], 'sidebar' => [], 'footer' => [], 'partner' => []];

    // First, try series sponsors (these override event sponsors)
    if (!empty($event['series_id'])) {
        try {
            $seriesSponsorStmt = $db->prepare("
                SELECT s.*, ss.placement, ss.display_order,
                       m_banner.filepath as banner_logo_url,
                       m_standard.filepath as standard_logo_url,
                       m_small.filepath as small_logo_url,
                       m_legacy.filepath as legacy_logo_url
                FROM sponsors s
                INNER JOIN series_sponsors ss ON s.id = ss.sponsor_id
                LEFT JOIN media m_banner ON s.logo_banner_id = m_banner.id
                LEFT JOIN media m_standard ON s.logo_standard_id = m_standard.id
                LEFT JOIN media m_small ON s.logo_small_id = m_small.id
                LEFT JOIN media m_legacy ON s.logo_media_id = m_legacy.id
                WHERE ss.series_id = ? AND s.active = 1
                ORDER BY ss.display_order ASC, s.tier ASC
            ");
            $seriesSponsorStmt->execute([$event['series_id']]);
            foreach ($seriesSponsorStmt->fetchAll(PDO::FETCH_ASSOC) as $sponsor) {
                $placement = $sponsor['placement'] ?? 'sidebar';
                $eventSponsors[$placement][] = $sponsor;
            }
        } catch (Exception $e) {
            // Table might not exist yet
        }
    }

    // Event-specific sponsors - these ADD to series sponsors (or replace per placement if specified)
    try {
        $sponsorStmt = $db->prepare("
            SELECT s.*, es.placement, es.display_order,
                   m_banner.filepath as banner_logo_url,
                   m_standard.filepath as standard_logo_url,
                   m_small.filepath as small_logo_url,
                   m_legacy.filepath as legacy_logo_url
            FROM sponsors s
            INNER JOIN event_sponsors es ON s.id = es.sponsor_id
            LEFT JOIN media m_banner ON s.logo_banner_id = m_banner.id
            LEFT JOIN media m_standard ON s.logo_standard_id = m_standard.id
            LEFT JOIN media m_small ON s.logo_small_id = m_small.id
            LEFT JOIN media m_legacy ON s.logo_media_id = m_legacy.id
            WHERE es.event_id = ? AND s.active = 1
            ORDER BY es.display_order ASC, s.tier ASC
        ");
        $sponsorStmt->execute([$eventId]);
        foreach ($sponsorStmt->fetchAll(PDO::FETCH_ASSOC) as $sponsor) {
            $placement = $sponsor['placement'] ?? 'sidebar';
            // Event sponsors override series sponsors for each placement
            if (empty($eventSponsors[$placement])) {
                $eventSponsors[$placement] = [];
            }
            // Add to beginning (event sponsors take priority)
            array_unshift($eventSponsors[$placement], $sponsor);
        }
    } catch (Exception $e) {
        // Table might not exist yet
        error_log("EVENT PAGE: event_sponsors load error: " . $e->getMessage());
    }

    // DEBUG: Log all sponsor placements
    error_log("EVENT PAGE: Sponsor placements - header:" . count($eventSponsors['header']) . ", content:" . count($eventSponsors['content']) . ", sidebar:" . count($eventSponsors['sidebar']));

    // Check event format for DH mode
    $eventFormat = $event['event_format'] ?? 'ENDURO';
    $isDH = in_array($eventFormat, ['DH_STANDARD', 'DH_SWECUP']);

    // Check if this is a Dual Slalom event (discipline = DS or has elimination data with series_class_id)
    $isDS = ($event['discipline'] ?? '') === 'DS';
    if (!$isDS) {
        // Also check if results have series_class_id set (indicating DS-style import)
        $dsCheck = $db->prepare("SELECT COUNT(*) as cnt FROM results WHERE event_id = ? AND series_class_id IS NOT NULL");
        $dsCheck->execute([$eventId]);
        $dsRow = $dsCheck->fetch(PDO::FETCH_ASSOC);
        $isDS = ($dsRow && (int)$dsRow['cnt'] > 0);
    }

    // DEBUG: Log DS detection
    error_log("EVENT {$eventId}: isDS=" . ($isDS ? 'true' : 'false') . ", discipline=" . ($event['discipline'] ?? 'null'));

    // For DH events, calculate run time stats for color coding
    $dhRunStats = [];
    if ($isDH) {
        // Will be populated per class later
    }

    // Fetch all results for this event
    // For DS events: sort by position (elimination result), NULL positions last
    // For other events: sort by finish_time
    $orderBy = $isDS
        ? "cls.sort_order ASC,
           COALESCE(cls.name, 'Oklassificerad'),
           CASE WHEN res.status = 'finished' THEN 0 ELSE 1 END,
           CASE WHEN res.position IS NULL OR res.position = 0 THEN 9999 ELSE res.position END ASC"
        : "cls.sort_order ASC,
           COALESCE(cls.name, 'Oklassificerad'),
           CASE WHEN res.status = 'finished' THEN 0 ELSE 1 END,
           res.finish_time ASC";

    $stmt = $db->prepare("
        SELECT
            res.*,
            r.id as rider_id,
            r.firstname,
            r.lastname,
            r.gender,
            r.birth_year,
            r.license_number,
            c.name as club_name,
            c.id as club_id,
            cls.id as class_id,
            cls.name as class_name,
            cls.display_name as class_display_name,
            cls.sort_order as class_sort_order,
            cls.awards_points as class_awards_points,
            COALESCE(cls.ranking_type, 'time') as ranking_type
        FROM results res
        INNER JOIN riders r ON res.cyclist_id = r.id
        LEFT JOIN clubs c ON COALESCE(res.club_id, r.club_id) = c.id
        LEFT JOIN classes cls ON res.class_id = cls.id
        WHERE res.event_id = ?
        ORDER BY {$orderBy}
    ");
    $stmt->execute([$eventId]);
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Normalize status values (e.g., 'FIN' -> 'finished')
    // ALWAYS set normalized lowercase status to ensure sorting works correctly
    foreach ($results as &$result) {
        $status = strtolower(trim($result['status'] ?? ''));
        if (in_array($status, ['fin', 'finish', 'finished', 'finnished', 'ok', ''])) {
            $result['status'] = 'finished';
        } elseif (in_array($status, ['dnf', 'did not finish'])) {
            $result['status'] = 'dnf';
        } elseif (in_array($status, ['dns', 'did not start'])) {
            $result['status'] = 'dns';
        } elseif (in_array($status, ['dq', 'dsq', 'disqualified'])) {
            $result['status'] = 'dq';
        } else {
            // Unknown status - keep as-is but ensure lowercase
            $result['status'] = $status;
        }
    }
    unset($result); // Break reference

    // Status values that should NOT count as valid split times
    $invalidSplitValues = ['dns', 'dnf', 'dq', 'dsq', 'finished', 'fin', 'finish', 'ok', 'did not finish', 'did not start', 'disqualified', '0:00', '0:00.00', '00:00:00', ''];

    // Check if any results have split times (excluding status values in split columns)
    $hasSplitTimes = false;
    foreach ($results as $result) {
        for ($i = 1; $i <= 15; $i++) {
            $splitVal = $result['ss' . $i] ?? '';
            if (!empty($splitVal) && !in_array(strtolower(trim($splitVal)), $invalidSplitValues)) {
                $hasSplitTimes = true;
                break 2;
            }
        }
    }

    // Check if DH event has run 2 data (exclude status values that may have ended up in time columns)
    $hasRun2Data = false;
    if ($isDH) {
        foreach ($results as $result) {
            $run2Val = strtolower(trim($result['run_2_time'] ?? ''));
            if (!empty($run2Val) && !in_array($run2Val, $invalidSplitValues)) {
                $hasRun2Data = true;
                break;
            }
        }
    }

    // Parse stage names
    $stageNames = [];
    if (!empty($event['stage_names'])) {
        $stageNames = json_decode($event['stage_names'], true) ?: [];
    }

    // Group results by class
    $resultsByClass = [];
    $totalParticipants = count($results);
    $totalFinished = 0;

    foreach ($results as $result) {
        $classKey = $result['class_id'] ?? 'no_class';
        $className = $result['class_name'] ?? 'Oklassificerad';

        if (!isset($resultsByClass[$classKey])) {
            $resultsByClass[$classKey] = [
                'class_id' => $result['class_id'],
                'display_name' => $result['class_display_name'] ?? $className,
                'class_name' => $className,
                'sort_order' => $result['class_sort_order'] ?? 999,
                'awards_points' => (int)($result['class_awards_points'] ?? 1),
                'ranking_type' => $result['ranking_type'] ?? 'time',
                'results' => [],
                'split_stats' => []
            ];
        }

        $resultsByClass[$classKey]['results'][] = $result;

        if ($result['status'] === 'finished') {
            $totalFinished++;
        }
    }

    // Sort results within each class and calculate positions
    foreach ($resultsByClass as $classKey => &$classData) {
        $rankingType = $classData['ranking_type'] ?? 'time';

        // For DS events: sort by stored position (elimination result), don't re-sort by time
        if ($isDS) {
            usort($classData['results'], function($a, $b) {
                // Finished riders first
                if ($a['status'] === 'finished' && $b['status'] !== 'finished') return -1;
                if ($a['status'] !== 'finished' && $b['status'] === 'finished') return 1;

                // Sort by position (from database)
                $aPos = (int)($a['position'] ?? 9999);
                $bPos = (int)($b['position'] ?? 9999);
                if ($aPos === 0) $aPos = 9999;
                if ($bPos === 0) $bPos = 9999;
                return $aPos <=> $bPos;
            });
        } else {
            // Standard sorting for non-DS events
            usort($classData['results'], function($a, $b) use ($rankingType) {
                if ($rankingType !== 'time') {
                    $aName = ($a['lastname'] ?? '') . ' ' . ($a['firstname'] ?? '');
                    $bName = ($b['lastname'] ?? '') . ' ' . ($b['firstname'] ?? '');
                    return strcasecmp($aName, $bName);
                }

                if ($a['status'] === 'finished' && $b['status'] !== 'finished') return -1;
                if ($a['status'] !== 'finished' && $b['status'] === 'finished') return 1;

                if ($a['status'] === 'finished' && $b['status'] === 'finished') {
                    $aSeconds = timeToSeconds($a['finish_time']);
                    $bSeconds = timeToSeconds($b['finish_time']);
                    return $aSeconds <=> $bSeconds;
                }

                $statusPriority = ['dnf' => 1, 'dq' => 2, 'dns' => 3];
                $aPriority = $statusPriority[$a['status']] ?? 4;
                $bPriority = $statusPriority[$b['status']] ?? 4;
                return $aPriority <=> $bPriority;
            });
        }

        // Calculate positions and time behind
        $position = 0;
        $winnerSeconds = 0;
        foreach ($classData['results'] as &$result) {
            // For DS events: use the stored position directly
            if ($isDS) {
                $storedPos = (int)($result['position'] ?? 0);
                $result['class_position'] = ($storedPos > 0) ? $storedPos : null;
                $result['time_behind'] = null; // No time comparison for DS
                continue;
            }

            if ($rankingType !== 'time') {
                $result['class_position'] = null;
                $result['time_behind'] = null;
                continue;
            }

            // Check if rider is actually finished with a valid time
            // Some imports mark DNS riders as 'finished' but without a time
            // For DH events, also check run_1_time and run_2_time
            $hasValidTime = false;
            $invalidTimes = ['DNS', 'DNF', 'DQ', 'DSQ', '0:00', '0:00:00', '0:00.00', ''];

            if (!empty($result['finish_time']) && !in_array(strtoupper($result['finish_time']), $invalidTimes)) {
                $hasValidTime = true;
            } elseif (!empty($result['run_1_time']) && !in_array(strtoupper($result['run_1_time']), $invalidTimes)) {
                $hasValidTime = true;
            } elseif (!empty($result['run_2_time']) && !in_array(strtoupper($result['run_2_time']), $invalidTimes)) {
                $hasValidTime = true;
            } elseif (!empty($result['ss1']) && !in_array(strtoupper($result['ss1']), $invalidTimes)) {
                $hasValidTime = true;
            }

            if ($result['status'] === 'finished' && $hasValidTime) {
                $position++;
                $result['class_position'] = $position;

                if ($position === 1 && !empty($result['finish_time'])) {
                    $winnerSeconds = timeToSeconds($result['finish_time']);
                }

                if ($position > 1 && $winnerSeconds > 0 && !empty($result['finish_time'])) {
                    $riderSeconds = timeToSeconds($result['finish_time']);
                    $diffSeconds = $riderSeconds - $winnerSeconds;
                    if ($diffSeconds > 0) {
                        $hours = floor($diffSeconds / 3600);
                        $minutes = floor(($diffSeconds % 3600) / 60);
                        $wholeSeconds = floor($diffSeconds) % 60;
                        $decimals = $diffSeconds - floor($diffSeconds);
                        $decimalStr = $decimals > 0 ? sprintf('.%02d', round($decimals * 100)) : '';

                        if ($hours > 0) {
                            $result['time_behind'] = sprintf('+%d:%02d:%02d', $hours, $minutes, $wholeSeconds) . $decimalStr;
                        } else {
                            $result['time_behind'] = sprintf('+%d:%02d', $minutes, $wholeSeconds) . $decimalStr;
                        }
                    }
                }
            } else {
                $result['class_position'] = null;
            }
        }
        unset($result);

        // Check if this is a motion/kids class - skip split comparisons for these
        $rankingType = $classData['ranking_type'] ?? 'time';
        $className = strtolower($classData['class_name'] ?? '');
        $isMotionOrKids = ($rankingType !== 'time') ||
                          strpos($className, 'kids') !== false ||
                          strpos($className, 'barn') !== false ||
                          strpos($className, 'motion') !== false;

        $classData['is_motion_or_kids'] = $isMotionOrKids;

        // Calculate DH run time stats for color coding
        if ($isDH && !$isMotionOrKids) {
            foreach (['run_1_time', 'run_2_time'] as $runKey) {
                $times = [];
                foreach ($classData['results'] as $result) {
                    if (!empty($result[$runKey]) && $result['status'] === 'finished') {
                        $times[] = timeToSeconds($result[$runKey]);
                    }
                }
                if (count($times) >= 2) {
                    sort($times);
                    $min = $times[0];
                    $max = $times[count($times) - 1];
                    // Cap outliers at 90th percentile + 30%
                    if (count($times) >= 3) {
                        $p90Index = (int) floor(count($times) * 0.9);
                        $p90 = $times[$p90Index];
                        if ($max > $p90 * 1.3) {
                            $max = $p90;
                        }
                    }
                    $classData['dh_run_stats'][$runKey] = [
                        'min' => $min,
                        'max' => $max,
                        'range' => $max - $min
                    ];
                }
            }

            // Calculate run rankings and time behind for each rider
            foreach (['run_1_time', 'run_2_time'] as $runIdx => $runKey) {
                $runTimes = [];
                foreach ($classData['results'] as $idx => $result) {
                    if (!empty($result[$runKey]) && $result['status'] === 'finished') {
                        $seconds = timeToSeconds($result[$runKey]);
                        // Only include valid times (not 0:00 or empty)
                        if ($seconds < PHP_INT_MAX) {
                            $runTimes[] = [
                                'idx' => $idx,
                                'time' => $seconds
                            ];
                        }
                    }
                }

                if (count($runTimes) > 0) {
                    usort($runTimes, function($a, $b) {
                        return $a['time'] <=> $b['time'];
                    });

                    $bestTime = $runTimes[0]['time'];

                    foreach ($runTimes as $rank => $entry) {
                        $ridx = $entry['idx'];
                        $classData['results'][$ridx]['run_rank_' . ($runIdx + 1)] = $rank + 1;
                        $diff = $entry['time'] - $bestTime;
                        if ($diff > 0) {
                            $classData['results'][$ridx]['run_diff_' . ($runIdx + 1)] = '+' . number_format($diff, 2);
                        } else {
                            $classData['results'][$ridx]['run_diff_' . ($runIdx + 1)] = '';
                        }
                    }
                }
            }
        }

        // Only calculate split stats and rankings for competitive classes
        if (!$isMotionOrKids) {
            // Calculate split time statistics for color coding
            for ($ss = 1; $ss <= 15; $ss++) {
                $times = [];
                foreach ($classData['results'] as $result) {
                    if (!empty($result['ss' . $ss]) && $result['status'] === 'finished') {
                        $times[] = timeToSeconds($result['ss' . $ss]);
                    }
                }
                if (count($times) >= 2) {
                    sort($times);
                    $min = $times[0];
                    $max = $times[count($times) - 1];
                    if (count($times) >= 3) {
                        $p90Index = (int) floor(count($times) * 0.9);
                        $p90 = $times[$p90Index];
                        if ($max > $p90 * 1.3) {
                            $max = $p90;
                        }
                    }
                    $classData['split_stats'][$ss] = [
                        'min' => $min,
                        'max' => $max,
                        'range' => $max - $min
                    ];
                }
            }

            // Calculate split rankings and +time for each rider in this class
            for ($ss = 1; $ss <= 15; $ss++) {
                // Collect all valid split times with rider index
                $splitTimes = [];
                foreach ($classData['results'] as $idx => $result) {
                    if (!empty($result['ss' . $ss]) && $result['status'] === 'finished') {
                        $timeSeconds = timeToSeconds($result['ss' . $ss]);
                        // Only include valid times (not PHP_INT_MAX from invalid data)
                        if ($timeSeconds < PHP_INT_MAX) {
                            $splitTimes[] = [
                                'idx' => $idx,
                                'time' => $timeSeconds
                            ];
                        }
                    }
                }

                if (count($splitTimes) > 0) {
                    // Sort by time to calculate rankings
                    usort($splitTimes, function($a, $b) {
                        return $a['time'] <=> $b['time'];
                    });

                    $bestTime = $splitTimes[0]['time'];

                    // Assign rankings
                    foreach ($splitTimes as $rank => $entry) {
                        $ridx = $entry['idx'];
                        $classData['results'][$ridx]['split_rank_' . $ss] = $rank + 1;
                        $diff = $entry['time'] - $bestTime;
                        if ($diff > 0) {
                            $classData['results'][$ridx]['split_diff_' . $ss] = '+' . number_format($diff, 2);
                        } else {
                            $classData['results'][$ridx]['split_diff_' . $ss] = '';
                        }
                    }
                }
            }
        }
    }
    unset($classData);

    // Sort classes by sort_order
    uasort($resultsByClass, function($a, $b) {
        return $a['sort_order'] - $b['sort_order'];
    });

    // Calculate global split stats for "Sträcktider Total" view
    // Combines all time-ranked classes (excluding motion/kids)
    $globalSplitResults = [];
    $globalSplitStats = [];
    $globalSplits = [];

    if ($hasSplitTimes && !$isDH) {
        // Collect all results from time-ranked classes
        foreach ($resultsByClass as $classKey => $classData) {
            $rankingType = $classData['ranking_type'] ?? 'time';
            $className = strtolower($classData['class_name'] ?? '');

            // Skip motion classes and kids classes
            if ($rankingType !== 'time') continue;
            if (strpos($className, 'kids') !== false || strpos($className, 'barn') !== false) continue;

            foreach ($classData['results'] as $result) {
                if ($result['status'] === 'finished') {
                    $globalSplitResults[] = array_merge($result, [
                        'original_class' => $classData['display_name']
                    ]);
                }
            }
        }

        // Determine which splits exist globally
        for ($ss = 1; $ss <= 15; $ss++) {
            foreach ($globalSplitResults as $r) {
                if (!empty($r['ss' . $ss])) {
                    $globalSplits[] = $ss;
                    break;
                }
            }
        }

        // Calculate global split stats and rankings
        for ($ss = 1; $ss <= 15; $ss++) {
            $splitTimes = [];
            foreach ($globalSplitResults as $idx => $result) {
                if (!empty($result['ss' . $ss])) {
                    $timeSeconds = timeToSeconds($result['ss' . $ss]);
                    // Only include valid times (not PHP_INT_MAX from invalid data)
                    if ($timeSeconds < PHP_INT_MAX) {
                        $splitTimes[] = [
                            'idx' => $idx,
                            'time' => $timeSeconds
                        ];
                    }
                }
            }

            if (count($splitTimes) > 0) {
                usort($splitTimes, function($a, $b) {
                    return $a['time'] <=> $b['time'];
                });

                $bestTime = $splitTimes[0]['time'];
                $times = array_column($splitTimes, 'time');
                $min = min($times);
                $max = max($times);

                // Cap outliers at 90th percentile + 30%
                if (count($times) >= 3) {
                    $p90Index = (int) floor(count($times) * 0.9);
                    sort($times);
                    $p90 = $times[$p90Index];
                    if ($max > $p90 * 1.3) {
                        $max = $p90;
                    }
                }

                $globalSplitStats[$ss] = [
                    'min' => $min,
                    'max' => $max,
                    'range' => $max - $min
                ];

                // Assign global rankings
                foreach ($splitTimes as $rank => $entry) {
                    $ridx = $entry['idx'];
                    $globalSplitResults[$ridx]['global_split_rank_' . $ss] = $rank + 1;
                    $diff = $entry['time'] - $bestTime;
                    if ($diff > 0) {
                        $globalSplitResults[$ridx]['global_split_diff_' . $ss] = '+' . number_format($diff, 2);
                    } else {
                        $globalSplitResults[$ridx]['global_split_diff_' . $ss] = '';
                    }
                }
            }
        }

        // Sort global results by first split time by default
        if (count($globalSplits) > 0) {
            $firstSplit = $globalSplits[0];
            usort($globalSplitResults, function($a, $b) use ($firstSplit) {
                $aTime = !empty($a['ss' . $firstSplit]) ? timeToSeconds($a['ss' . $firstSplit]) : PHP_INT_MAX;
                $bTime = !empty($b['ss' . $firstSplit]) ? timeToSeconds($b['ss' . $firstSplit]) : PHP_INT_MAX;
                return $aTime <=> $bTime;
            });
        }
    }

    // Calculate global DH run stats for "Åktider Total" view (DH equivalent of Sträcktider Total)
    $globalDHResults = [];
    $globalDHStats = [];

    if ($isDH) {
        // Collect all results from competitive DH classes (excluding motion/kids)
        foreach ($resultsByClass as $classKey => $classData) {
            $rankingType = $classData['ranking_type'] ?? 'time';
            $className = strtolower($classData['class_name'] ?? '');

            // Skip motion classes and kids classes
            if ($rankingType !== 'time') continue;
            if (strpos($className, 'kids') !== false || strpos($className, 'barn') !== false) continue;
            if (strpos($className, 'motion') !== false) continue;

            foreach ($classData['results'] as $result) {
                if ($result['status'] === 'finished') {
                    $globalDHResults[] = array_merge($result, [
                        'original_class' => $classData['display_name']
                    ]);
                }
            }
        }

        // Calculate global run stats and rankings for run 1 and run 2
        foreach (['run_1_time' => 1, 'run_2_time' => 2] as $runKey => $runNum) {
            $runTimes = [];
            foreach ($globalDHResults as $idx => $result) {
                if (!empty($result[$runKey])) {
                    $seconds = timeToSeconds($result[$runKey]);
                    // Only include valid times (not 0:00 or empty)
                    if ($seconds < PHP_INT_MAX) {
                        $runTimes[] = [
                            'idx' => $idx,
                            'time' => $seconds
                        ];
                    }
                }
            }

            if (count($runTimes) > 0) {
                usort($runTimes, function($a, $b) {
                    return $a['time'] <=> $b['time'];
                });

                $bestTime = $runTimes[0]['time'];
                $times = array_column($runTimes, 'time');
                $min = min($times);
                $max = max($times);

                // Cap outliers at 90th percentile + 30%
                if (count($times) >= 3) {
                    $p90Index = (int) floor(count($times) * 0.9);
                    sort($times);
                    $p90 = $times[$p90Index];
                    if ($max > $p90 * 1.3) {
                        $max = $p90;
                    }
                }

                $globalDHStats[$runKey] = [
                    'min' => $min,
                    'max' => $max,
                    'range' => $max - $min
                ];

                // Assign global rankings
                foreach ($runTimes as $rank => $entry) {
                    $ridx = $entry['idx'];
                    $globalDHResults[$ridx]['global_run_rank_' . $runNum] = $rank + 1;
                    $diff = $entry['time'] - $bestTime;
                    if ($diff > 0) {
                        $globalDHResults[$ridx]['global_run_diff_' . $runNum] = '+' . number_format($diff, 2);
                    } else {
                        $globalDHResults[$ridx]['global_run_diff_' . $runNum] = '';
                    }
                }
            }
        }

        // Sort global DH results by run 1 time by default
        usort($globalDHResults, function($a, $b) {
            $aTime = !empty($a['run_1_time']) ? timeToSeconds($a['run_1_time']) : PHP_INT_MAX;
            $bTime = !empty($b['run_1_time']) ? timeToSeconds($b['run_1_time']) : PHP_INT_MAX;
            return $aTime <=> $bTime;
        });
    }

    // Fetch registrations with class info
    $registrations = $db->prepare("
        SELECT reg.*, r.firstname, r.lastname, c.name as club_name,
               COALESCE(cl.display_name, cl.name, reg.category) as class_name,
               cl.sort_order as class_sort_order
        FROM event_registrations reg
        LEFT JOIN riders r ON reg.rider_id = r.id
        LEFT JOIN clubs c ON r.club_id = c.id
        LEFT JOIN classes cl ON cl.name = reg.category
        WHERE reg.event_id = ? AND reg.status != 'cancelled'
        ORDER BY cl.sort_order ASC, cl.name ASC, reg.registration_date ASC
    ");
    $registrations->execute([$eventId]);
    $registrations = $registrations->fetchAll(PDO::FETCH_ASSOC);
    $totalRegistrations = count($registrations);

    // Group registrations by class
    $registrationsByClass = [];
    foreach ($registrations as $reg) {
        $className = $reg['class_name'] ?: $reg['category'] ?: 'Okänd klass';
        if (!isset($registrationsByClass[$className])) {
            $registrationsByClass[$className] = [];
        }
        $registrationsByClass[$className][] = $reg;
    }

    // Check if event is in the past
    $eventDate = strtotime($event['date']);
    $isPastEvent = $eventDate < strtotime('today');

    // Check registration status (with time support)
    $registrationDeadline = null;
    if (!empty($event['registration_deadline'])) {
        $deadlineDate = $event['registration_deadline'];
        $deadlineTime = !empty($event['registration_deadline_time']) ? $event['registration_deadline_time'] : '23:59:59';
        $registrationDeadline = strtotime($deadlineDate . ' ' . $deadlineTime);
    }

    // Registration is only "open" if deadline is set, hasn't passed, AND pricing is configured
    $hasPricingRules = false;
    try {
        $priceCheck = $db->prepare("SELECT COUNT(*) as cnt FROM event_pricing_rules WHERE event_id = ?");
        $priceCheck->execute([$eventId]);
        $priceRow = $priceCheck->fetch(PDO::FETCH_ASSOC);
        $hasPricingRules = ($priceRow && $priceRow['cnt'] > 0);
    } catch (Exception $e) {
        $hasPricingRules = false;
    }

    // Registration tab is shown if: has pricing rules AND either has valid deadline OR has external URL
    $registrationConfigured = $hasPricingRules || !empty($event['registration_url']);
    $registrationOpen = $registrationConfigured && ($registrationDeadline === null || $registrationDeadline >= time());

    // Check publish dates for starttider, karta and PM
    $starttiderPublished = empty($event['starttider_publish_at']) || strtotime($event['starttider_publish_at']) <= time();
    $kartaPublished = empty($event['karta_publish_at']) || strtotime($event['karta_publish_at']) <= time();
    $pmPublished = empty($event['pm_publish_at']) || strtotime($event['pm_publish_at']) <= time();

    // Check for elimination data
    $hasEliminationData = false;
    try {
        $elimCheck = $db->prepare("SELECT COUNT(*) as cnt FROM elimination_qualifying WHERE event_id = ?");
        $elimCheck->execute([$eventId]);
        $elimRow = $elimCheck->fetch(PDO::FETCH_ASSOC);
        $hasEliminationData = ($elimRow && $elimRow['cnt'] > 0);
    } catch (Exception $e) {
        // Table doesn't exist yet
        $hasEliminationData = false;
    }

    // Determine active tab based on event state
    // Priority: 1. Results (if exists) 2. Inbjudan (default for upcoming events)
    $hasResults = !empty($results);
    if ($hasResults) {
        $defaultTab = 'resultat';
    } else {
        $defaultTab = 'info'; // Inbjudan is default for upcoming events
    }
    $activeTab = isset($_GET['tab']) ? $_GET['tab'] : $defaultTab;

    // Ticketing info
    $ticketingEnabled = !empty($event['ticketing_enabled']);

    // Fetch other events in the same series for navigation
    $seriesEvents = [];
    if (!empty($event['series_id'])) {
        $seriesEventsStmt = $db->prepare("
            SELECT id, name, date
            FROM events
            WHERE series_id = ? AND active = 1
            ORDER BY date ASC
        ");
        $seriesEventsStmt->execute([$event['series_id']]);
        $seriesEvents = $seriesEventsStmt->fetchAll(PDO::FETCH_ASSOC);
    }

} catch (Exception $e) {
    $error = $e->getMessage();
    error_log("EVENT PAGE ERROR (ID: {$eventId}): " . $error);
    $event = null;
}

// Show database error if one occurred
if (isset($error) && $error): ?>
<div class="alert alert--error mb-lg">
    <p><strong>Databasfel:</strong> <?= htmlspecialchars($error) ?></p>
    <p class="text-muted text-sm">Event ID: <?= $eventId ?></p>
</div>
<?php
endif;

if (!$event) {
    // Only show 404 if there was no database error (event simply doesn't exist)
    if (!isset($error)) {
        include HUB_ROOT . '/pages/404.php';
    }
    return;
}
?>

<?php
// Event Header Banner (direct media upload on event) - hämta filepath
$eventHeaderBanner = null;
if (!empty($event['header_banner_media_id'])) {
    try {
        $bannerStmt = $db->prepare("SELECT filepath FROM media WHERE id = ?");
        $bannerStmt->execute([$event['header_banner_media_id']]);
        $bannerRow = $bannerStmt->fetch(PDO::FETCH_ASSOC);
        if ($bannerRow && !empty($bannerRow['filepath'])) {
            $eventHeaderBanner = '/' . ltrim($bannerRow['filepath'], '/');
        }
    } catch (Exception $e) {
        error_log("EVENT PAGE: Error loading header banner: " . $e->getMessage());
    }
}
// Fallback till header_banner_url om det finns
if (!$eventHeaderBanner && !empty($event['header_banner_url'])) {
    $eventHeaderBanner = '/' . ltrim($event['header_banner_url'], '/');
}

// Sponsor banner (från sponsor med placement=header)
$headerSponsorsWithLogos = array_filter($eventSponsors['header'] ?? [], function($s) {
    return get_sponsor_logo_for_placement($s, 'header') !== null;
});

// Visa event-banner ELLER sponsor-banner högst upp (full bredd)
if ($eventHeaderBanner): ?>
<section class="event-header-banner">
    <img src="<?= h($eventHeaderBanner) ?>" alt="<?= h($event['name']) ?>" class="event-header-banner-img">
</section>
<?php elseif (!empty($headerSponsorsWithLogos)): ?>
<section class="event-header-banner">
    <?php foreach ($headerSponsorsWithLogos as $sponsor):
        $bannerLogo = get_sponsor_logo_for_placement($sponsor, 'header');
    ?>
    <a href="<?= h($sponsor['website'] ?? '#') ?>" target="_blank" rel="noopener sponsored" style="display: block;">
        <img src="<?= h($bannerLogo) ?>" alt="<?= h($sponsor['name']) ?>" class="event-header-banner-img">
    </a>
    <?php endforeach; ?>
</section>
<?php endif; ?>

<!-- Event Header -->
<section class="event-header mb-sm">
    <div class="event-header-content">
        <?php if ($event['series_logo']): ?>
        <div class="event-logo">
            <img src="<?= h($event['series_logo']) ?>" alt="<?= h($event['series_name'] ?? 'Serie') ?>">
        </div>
        <?php endif; ?>

        <div class="event-info">
            <div class="event-title-row">
                <h1 class="event-title"><?= h($event['name']) ?></h1>
                <?php if ($canEditEvent): ?>
                <a href="/admin/event-edit.php?id=<?= $eventId ?>" class="btn-admin-edit" title="Redigera event">
                    <i data-lucide="pencil"></i>
                </a>
                <?php endif; ?>
            </div>

            <?php if (!empty($event['organizer_club_name']) || !empty($event['series_organizer'])): ?>
            <div class="event-organizer-club">
                <i data-lucide="users"></i>
                Arrangör:
                <?php if (!empty($event['organizer_club_name'])): ?>
                <a href="/club/<?= $event['organizer_club_id_ref'] ?>" class="organizer-club-link">
                    <?= h($event['organizer_club_name']) ?>
                </a>
                <?php elseif (!empty($event['series_organizer'])): ?>
                <span class="series-organizer"><?= h($event['series_organizer']) ?></span>
                <?php endif; ?>
            </div>
            <?php endif; ?>

            <div class="event-meta">
                <span class="event-meta-item">
                    <i data-lucide="calendar"></i>
                    <?= date('j F Y', strtotime($event['date'])) ?>
                </span>

                <?php if ($event['venue_name']): ?>
                <span class="event-meta-item">
                    <i data-lucide="map-pin"></i>
                    <?= h($event['venue_name']) ?><?php if ($event['venue_city']): ?>, <?= h($event['venue_city']) ?><?php endif; ?>
                </span>
                <?php elseif ($event['location']): ?>
                <span class="event-meta-item">
                    <i data-lucide="map-pin"></i>
                    <?= h($event['location']) ?>
                </span>
                <?php endif; ?>

                <?php if ($event['series_name']): ?>
                <a href="/series/<?= $event['series_id'] ?>" class="event-series-badge">
                    <i data-lucide="award"></i>
                    <?= h($event['series_name']) ?>
                </a>
                <?php endif; ?>

                <?php if (!empty($event['is_championship'])): ?>
                <span class="event-sm-badge" title="Svenska Mästerskap">
                    <i data-lucide="medal"></i>
                    SM
                </span>
                <?php endif; ?>
            </div>

            <?php if (!empty($event['organizer'])): ?>
            <div class="event-organizer">
                <span class="organizer-name">
                    <i data-lucide="building-2"></i>
                    <?= h($event['organizer']) ?>
                </span>
                <div class="organizer-links">
                    <?php if (!empty($event['website'])): ?>
                    <a href="<?= h($event['website']) ?>" target="_blank" rel="noopener">
                        <i data-lucide="globe"></i> Webb
                    </a>
                    <?php endif; ?>
                    <?php if (!empty($event['contact_email'])): ?>
                    <a href="mailto:<?= h($event['contact_email']) ?>">
                        <i data-lucide="mail"></i> E-post
                    </a>
                    <?php endif; ?>
                    <?php if (!empty($event['contact_phone'])): ?>
                    <a href="tel:<?= h($event['contact_phone']) ?>">
                        <i data-lucide="phone"></i> <?= h($event['contact_phone']) ?>
                    </a>
                    <?php endif; ?>
                </div>
            </div>
            <?php endif; ?>
        </div>

        <div class="event-stats">
            <?php if ($event['series_logo']): ?>
            <div class="event-stat event-stat--logo">
                <img src="<?= h($event['series_logo']) ?>" alt="<?= h($event['series_name'] ?? 'Serie') ?>">
            </div>
            <?php endif; ?>
            <?php if ($totalParticipants > 0): ?>
            <div class="event-stat">
                <span class="event-stat-value"><?= $totalParticipants ?></span>
                <span class="event-stat-label">deltagare</span>
            </div>
            <div class="event-stat">
                <span class="event-stat-value"><?= $totalFinished ?></span>
                <span class="event-stat-label">i mål</span>
            </div>
            <?php elseif ($totalRegistrations > 0): ?>
            <div class="event-stat">
                <span class="event-stat-value"><?= $totalRegistrations ?></span>
                <span class="event-stat-label">anmälda</span>
            </div>
            <?php endif; ?>
        </div>
    </div>
</section>

<?php
// Content sponsors (logo row) - show all, with or without logos
// DEBUG: Log content sponsors count
error_log("EVENT PAGE DEBUG: Content sponsors count = " . count($eventSponsors['content'] ?? []));
if (!empty($eventSponsors['content'])) {
    foreach ($eventSponsors['content'] as $sp) {
        error_log("EVENT PAGE DEBUG: Content sponsor: " . ($sp['name'] ?? 'N/A') . " (ID: " . ($sp['id'] ?? 'N/A') . ")");
    }
}
if (!empty($eventSponsors['content'])): ?>
<section class="event-sponsor-logos mb-sm">
    <div class="sponsor-logos-grid">
        <?php foreach ($eventSponsors['content'] as $sponsor):
            $standardLogo = get_sponsor_logo_for_placement($sponsor, 'content');
        ?>
        <a href="<?= h($sponsor['website'] ?? '#') ?>" target="_blank" rel="noopener sponsored" class="sponsor-logo-item" title="<?= h($sponsor['name']) ?>">
            <?php if ($standardLogo): ?>
            <img src="<?= h($standardLogo) ?>" alt="<?= h($sponsor['name']) ?>">
            <?php else: ?>
            <span><?= h($sponsor['name']) ?></span>
            <?php endif; ?>
        </a>
        <?php endforeach; ?>
    </div>
</section>
<?php endif; ?>

<!-- Tab Navigation -->
<div class="event-tabs-wrapper mb-sm">
    <div class="event-tabs">
        <?php
        // When results exist, we show fewer tabs (Resultat, Info, Karta only)
        $showAllTabs = !$hasResults;
        ?>

        <?php if ($hasResults): ?>
        <a href="?id=<?= $eventId ?>&tab=resultat" class="event-tab <?= $activeTab === 'resultat' ? 'active' : '' ?>">
            <i data-lucide="trophy"></i>
            Resultat
            <span class="tab-badge"><?= $totalParticipants ?></span>
        </a>
        <?php endif; ?>

        <?php if ($hasEliminationData): ?>
        <a href="?id=<?= $eventId ?>&tab=elimination" class="event-tab <?= $activeTab === 'elimination' ? 'active' : '' ?>">
            <i data-lucide="git-branch"></i>
            Elimination
        </a>
        <?php endif; ?>

        <?php if ($showAllTabs && $registrationOpen): ?>
        <a href="?id=<?= $eventId ?>&tab=anmalan" class="event-tab <?= $activeTab === 'anmalan' ? 'active' : '' ?>">
            <i data-lucide="edit-3"></i>
            Anmälan
        </a>
        <?php endif; ?>

        <a href="?id=<?= $eventId ?>&tab=info" class="event-tab <?= $activeTab === 'info' ? 'active' : '' ?>">
            <i data-lucide="file-text"></i>
            Inbjudan
        </a>

        <?php if ($showAllTabs && $pmPublished && empty($event['pm_hidden']) && (!empty($event['pm_content']) || !empty($event['pm_use_global']))): ?>
        <a href="?id=<?= $eventId ?>&tab=pm" class="event-tab <?= $activeTab === 'pm' ? 'active' : '' ?>">
            <i data-lucide="file-text"></i>
            PM
        </a>
        <?php endif; ?>

        <?php if ($showAllTabs && empty($event['jury_hidden']) && (!empty($event['jury_communication']) || !empty($event['jury_use_global']))): ?>
        <a href="?id=<?= $eventId ?>&tab=jury" class="event-tab <?= $activeTab === 'jury' ? 'active' : '' ?>">
            <i data-lucide="scale"></i>
            Jury
        </a>
        <?php endif; ?>

        <?php if ($showAllTabs && empty($event['schedule_hidden']) && (!empty($event['competition_schedule']) || !empty($event['schedule_use_global']))): ?>
        <a href="?id=<?= $eventId ?>&tab=schema" class="event-tab <?= $activeTab === 'schema' ? 'active' : '' ?>">
            <i data-lucide="calendar-clock"></i>
            Schema
        </a>
        <?php endif; ?>

        <?php if ($showAllTabs && $starttiderPublished && empty($event['start_times_hidden']) && (!empty($event['start_times']) || !empty($event['start_times_use_global']))): ?>
        <a href="?id=<?= $eventId ?>&tab=starttider" class="event-tab <?= $activeTab === 'starttider' ? 'active' : '' ?>">
            <i data-lucide="list-ordered"></i>
            Starttider
        </a>
        <?php endif; ?>

        <?php if ($hasInteractiveMap && $kartaPublished): ?>
        <a href="?id=<?= $eventId ?>&tab=karta" class="event-tab <?= $activeTab === 'karta' ? 'active' : '' ?>" onclick="if(window.innerWidth <= 768) { window.location.href='/map.php?id=<?= $eventId ?>'; return false; }">
            <i data-lucide="map-pin"></i>
            Karta
        </a>
        <?php endif; ?>

        <?php if ($eventReportsCount > 0): ?>
        <a href="?id=<?= $eventId ?>&tab=nyheter" class="event-tab <?= $activeTab === 'nyheter' ? 'active' : '' ?>">
            <i data-lucide="newspaper"></i>
            Media
            <span class="tab-badge tab-badge--accent"><?= $eventReportsCount ?></span>
        </a>
        <?php endif; ?>

        <?php if ($showAllTabs && !$isPastEvent && $totalRegistrations > 0): ?>
        <a href="?id=<?= $eventId ?>&tab=anmalda" class="event-tab <?= $activeTab === 'anmalda' ? 'active' : '' ?>">
            <i data-lucide="users"></i>
            Anmälda
            <span class="tab-badge tab-badge--secondary"><?= $totalRegistrations ?></span>
        </a>
        <?php endif; ?>

        <?php if ($showAllTabs && $ticketingEnabled): ?>
        <a href="?id=<?= $eventId ?>&tab=biljetter" class="event-tab <?= $activeTab === 'biljetter' ? 'active' : '' ?>">
            <i data-lucide="ticket"></i>
            Biljetter
        </a>
        <?php endif; ?>

        <?php if (count($seriesEvents) > 1): ?>
        <div class="series-jump-wrapper">
            <span class="series-jump-label"><?= h($event['series_name']) ?> <?= date('Y', strtotime($event['date'])) ?></span>
            <select onchange="if(this.value) window.location.href='/event/' + this.value" class="series-jump-select">
                <?php foreach ($seriesEvents as $sEvent): ?>
                    <option value="<?= $sEvent['id'] ?>" <?= $sEvent['id'] == $eventId ? 'selected' : '' ?>>
                        <?= date('j M', strtotime($sEvent['date'])) ?> – <?= h($sEvent['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <?php endif; ?>

        <?php if (!empty($event['series_id'])): ?>
        <a href="/series/<?= $event['series_id'] ?>" class="series-standings-btn">
            <i data-lucide="trophy"></i>
            Serietabeller
        </a>
        <?php endif; ?>
    </div>
</div>

<!-- Tab Content -->
<?php if ($activeTab === 'resultat'): ?>
<!-- RESULTS TAB -->
<?php if (empty($results)): ?>
<section class="card">
    <div class="empty-state">
        <i data-lucide="trophy" class="empty-state-icon"></i>
        <h3>Inga resultat ännu</h3>
        <p>Resultat har inte laddats upp för denna tävling.</p>
    </div>
</section>
<?php else: ?>

<!-- Filters -->
<div class="filter-row mb-lg">
    <div class="filter-field">
        <label class="filter-label">Klass</label>
        <select class="filter-select" id="classFilter" onchange="filterResults()">
            <option value="all">Alla klasser</option>
            <?php foreach ($resultsByClass as $classKey => $classData): ?>
            <option value="<?= $classKey ?>"><?= h($classData['display_name']) ?> (<?= count($classData['results']) ?>)</option>
            <?php endforeach; ?>
        </select>
    </div>
    <div class="filter-field">
        <label class="filter-label">Sök åkare</label>
        <input type="text" class="filter-input" id="searchFilter" placeholder="Namn eller klubb..." oninput="filterResults()">
    </div>
    <?php if ($hasSplitTimes || $isDH): ?>
    <div class="filter-toggles">
        <label class="toggle-label">
            <input type="checkbox" id="colorToggle" checked onchange="toggleSplitColors(this.checked)">
            <span class="toggle-text">Färgkodning</span>
            <span class="toggle-switch"></span>
        </label>
        <?php if (!$isDH && count($globalSplitResults) > 0): ?>
        <label class="toggle-label">
            <input type="checkbox" id="totalViewToggle" onchange="toggleTotalView(this.checked)">
            <span class="toggle-text">Sträcktider Total</span>
            <span class="toggle-switch"></span>
        </label>
        <?php endif; ?>
        <?php if ($isDH && count($globalDHResults) > 0): ?>
        <label class="toggle-label">
            <input type="checkbox" id="dhTotalViewToggle" onchange="toggleDHTotalView(this.checked)">
            <span class="toggle-text">Åktider Total</span>
            <span class="toggle-switch"></span>
        </label>
        <?php endif; ?>
    </div>
    <?php endif; ?>
</div>

<?php foreach ($resultsByClass as $classKey => $classData):
    $isTimeRanked = ($classData['ranking_type'] ?? 'time') === 'time';
    $isMotionOrKids = $classData['is_motion_or_kids'] ?? false;

    // Calculate which splits this class has (excluding status values in split columns)
    $classSplits = [];
    if ($hasSplitTimes && !$isDH) {
        for ($ss = 1; $ss <= 15; $ss++) {
            foreach ($classData['results'] as $r) {
                $splitVal = $r['ss' . $ss] ?? '';
                if (!empty($splitVal) && !in_array(strtolower(trim($splitVal)), $invalidSplitValues)) {
                    $classSplits[] = $ss;
                    break;
                }
            }
        }
    }
?>
<section class="card mb-lg class-section" id="class-<?= $classKey ?>" data-class="<?= $classKey ?>">
    <div class="card-header">
        <div>
            <h2 class="card-title"><?= h($classData['display_name']) ?></h2>
            <p class="card-subtitle"><?= count($classData['results']) ?> deltagare<?= !$isTimeRanked ? ' (motion)' : '' ?></p>
        </div>
        <?php
        // Only show sidebar sponsor if it has a logo
        $resultSponsor = $eventSponsors['sidebar'][0] ?? null;
        $smallLogo = $resultSponsor ? get_sponsor_logo_for_placement($resultSponsor, 'sidebar') : null;
        if ($resultSponsor && $smallLogo): ?>
        <a href="<?= h($resultSponsor['website'] ?? '#') ?>" target="_blank" rel="noopener sponsored" class="class-sponsor" title="Resultat sponsrat av <?= h($resultSponsor['name']) ?>">
            <span class="class-sponsor-label-desktop">Resultaten presenteras av</span>
            <span class="class-sponsor-label-mobile">Sponsor</span>
            <img src="<?= h($smallLogo) ?>" alt="<?= h($resultSponsor['name']) ?>" class="class-sponsor-logo">
        </a>
        <?php endif; ?>
    </div>

    <!-- Desktop Table -->
    <div class="table-wrapper">
        <table class="table table--striped table--hover results-table">
            <thead>
                <tr>
                    <th class="col-place"><?= $isTimeRanked ? '#' : '' ?></th>
                    <th class="col-rider">Åkare</th>
                    <th class="col-club table-col-hide-mobile">Klubb</th>
                    <?php if ($isDH): ?>
                    <?php if ($eventFormat === 'DH_SWECUP'): ?>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run1" onclick="sortDHByRun(this, '<?= $classKey ?>', 1)">Kval <span class="sort-icon"></span></th>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run2" onclick="sortDHByRun(this, '<?= $classKey ?>', 2)">Final <span class="sort-icon"></span></th>
                    <th class="col-time sortable-header" data-sort="time" onclick="sortByTime(this, '<?= $classKey ?>')">Tid <span class="sort-icon"></span></th>
                    <?php elseif ($hasRun2Data): ?>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run1" onclick="sortDHByRun(this, '<?= $classKey ?>', 1)">Åk 1 <span class="sort-icon"></span></th>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run2" onclick="sortDHByRun(this, '<?= $classKey ?>', 2)">Åk 2 <span class="sort-icon"></span></th>
                    <th class="col-time sortable-header" data-sort="best" onclick="sortByTime(this, '<?= $classKey ?>')">Bästa <span class="sort-icon"></span></th>
                    <?php else: ?>
                    <th class="col-time sortable-header" data-sort="time" onclick="sortByTime(this, '<?= $classKey ?>')">Tid <span class="sort-icon"></span></th>
                    <?php endif; ?>
                    <?php else: ?>
                    <th class="col-time sortable-header" data-sort="time" onclick="sortByTime(this, '<?= $classKey ?>')">Tid <span class="sort-icon"></span></th>
                    <?php foreach ($classSplits as $ss): ?>
                    <?php if ($isMotionOrKids): ?>
                    <th class="col-split split-time-col table-col-hide-mobile"><?= $stageNames[$ss] ?? 'SS' . $ss ?></th>
                    <?php else: ?>
                    <th class="col-split split-time-col table-col-hide-mobile sortable-header" data-sort="ss<?= $ss ?>" onclick="sortBySplit(this, '<?= $classKey ?>', <?= $ss ?>)"><?= $stageNames[$ss] ?? 'SS' . $ss ?> <span class="sort-icon"></span></th>
                    <?php endif; ?>
                    <?php endforeach; ?>
                    <?php endif; ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($classData['results'] as $result):
                    $searchData = strtolower($result['firstname'] . ' ' . $result['lastname'] . ' ' . ($result['club_name'] ?? ''));
                ?>
                <tr class="result-row" onclick="window.location='/rider/<?= $result['rider_id'] ?>'" data-search="<?= h($searchData) ?>">
                    <td class="col-place <?= $result['class_position'] && $result['class_position'] <= 3 ? 'col-place--' . $result['class_position'] : '' ?>">
                        <?php if (!$isTimeRanked): ?>
                            ✓
                        <?php elseif ($result['status'] !== 'finished'): ?>
                            <span class="status-badge status-<?= strtolower($result['status']) ?>"><?= strtoupper($result['status']) ?></span>
                        <?php elseif ($result['class_position'] == 1): ?>
                            <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                        <?php elseif ($result['class_position'] == 2): ?>
                            <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                        <?php elseif ($result['class_position'] == 3): ?>
                            <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                        <?php else: ?>
                            <?= $result['class_position'] ?>
                        <?php endif; ?>
                    </td>
                    <td class="col-rider">
                        <a href="/rider/<?= $result['rider_id'] ?>" class="rider-link">
                            <?= h($result['firstname'] . ' ' . $result['lastname']) ?>
                        </a>
                    </td>
                    <td class="col-club table-col-hide-mobile">
                        <?php if ($result['club_id']): ?>
                            <a href="/club/<?= $result['club_id'] ?>"><?= h($result['club_name'] ?? '-') ?></a>
                        <?php else: ?>
                            -
                        <?php endif; ?>
                    </td>
                    <?php if ($isDH && ($eventFormat === 'DH_SWECUP' || $hasRun2Data)):
                        // Calculate color classes for DH runs
                        $run1Class = '';
                        $run2Class = '';
                        $run1Seconds = !empty($result['run_1_time']) ? timeToSeconds($result['run_1_time']) : PHP_INT_MAX;
                        $run2Seconds = !empty($result['run_2_time']) ? timeToSeconds($result['run_2_time']) : PHP_INT_MAX;

                        if (!$isMotionOrKids && $result['status'] === 'finished') {
                            // Run 1 color
                            if (!empty($result['run_1_time']) && isset($classData['dh_run_stats']['run_1_time'])) {
                                $stats = $classData['dh_run_stats']['run_1_time'];
                                if ($stats['range'] > 0.5) {
                                    $position = ($run1Seconds - $stats['min']) / $stats['range'];
                                    $level = min(10, max(1, floor($position * 9) + 1));
                                    $run1Class = 'split-' . $level;
                                }
                            }
                            // Run 2 color
                            if (!empty($result['run_2_time']) && isset($classData['dh_run_stats']['run_2_time'])) {
                                $stats = $classData['dh_run_stats']['run_2_time'];
                                if ($stats['range'] > 0.5) {
                                    $position = ($run2Seconds - $stats['min']) / $stats['range'];
                                    $level = min(10, max(1, floor($position * 9) + 1));
                                    $run2Class = 'split-' . $level;
                                }
                            }
                        }

                        $run1Rank = $result['run_rank_1'] ?? null;
                        $run1Diff = $result['run_diff_1'] ?? '';
                        $run2Rank = $result['run_rank_2'] ?? null;
                        $run2Diff = $result['run_diff_2'] ?? '';
                    ?>
                    <td class="col-time col-dh-run table-col-hide-mobile <?= $run1Class ?>" data-sort-value="<?= $run1Seconds ?>">
                        <?php
                        $r1Display = formatDisplayTime($result['run_1_time'] ?? '');
                        if ($r1Display): ?>
                        <div class="split-time-main"><?= $r1Display ?></div>
                        <?php if (!$isMotionOrKids && ($run1Diff || $run1Rank)): ?>
                        <div class="split-time-details"><?= $run1Diff ?: '' ?><?= $run1Diff && $run1Rank ? ' ' : '' ?><?= $run1Rank ? '(' . $run1Rank . ')' : '' ?></div>
                        <?php endif; ?>
                        <?php else: ?>
                        <span class="text-secondary">DNS</span>
                        <?php endif; ?>
                    </td>
                    <td class="col-time col-dh-run table-col-hide-mobile <?= $run2Class ?>" data-sort-value="<?= $run2Seconds ?>">
                        <?php
                        $r2Display = formatDisplayTime($result['run_2_time'] ?? '');
                        if ($r2Display): ?>
                        <div class="split-time-main"><?= $r2Display ?></div>
                        <?php if (!$isMotionOrKids && ($run2Diff || $run2Rank)): ?>
                        <div class="split-time-details"><?= $run2Diff ?: '' ?><?= $run2Diff && $run2Rank ? ' ' : '' ?><?= $run2Rank ? '(' . $run2Rank . ')' : '' ?></div>
                        <?php endif; ?>
                        <?php else: ?>
                        <span class="text-secondary">DNS</span>
                        <?php endif; ?>
                    </td>
                    <?php
                    $bestTime = null;
                    $bestTimeSeconds = PHP_INT_MAX;
                    // Helper to check if time is valid (not empty, not 0:00)
                    $isValidDHTime = function($t) {
                        return !empty($t) && !preg_match('/^0+[:.]?0*[:.]?0*$/', $t);
                    };
                    if ($eventFormat === 'DH_SWECUP') {
                        $bestTime = $isValidDHTime($result['run_2_time']) ? $result['run_2_time'] : null;
                    } else {
                        $r1Valid = $isValidDHTime($result['run_1_time']);
                        $r2Valid = $isValidDHTime($result['run_2_time']);
                        if ($r1Valid && $r2Valid) {
                            $t1 = timeToSeconds($result['run_1_time']);
                            $t2 = timeToSeconds($result['run_2_time']);
                            $bestTime = $t1 < $t2 ? $result['run_1_time'] : $result['run_2_time'];
                        } elseif ($r1Valid) {
                            $bestTime = $result['run_1_time'];
                        } elseif ($r2Valid) {
                            $bestTime = $result['run_2_time'];
                        }
                    }
                    if ($bestTime) {
                        $bestTimeSeconds = timeToSeconds($bestTime);
                    }
                    ?>
                    <td class="col-time font-bold" data-sort-value="<?= $bestTimeSeconds ?>">
                        <?php if ($bestTime && $result['status'] === 'finished'): ?>
                        <div class="split-time-main"><?= formatDisplayTime($bestTime) ?></div>
                        <?php if (!empty($result['time_behind'])): ?>
                        <div class="split-time-details"><?= $result['time_behind'] ?></div>
                        <?php endif; ?>
                        <?php else: ?>
                        -
                        <?php endif; ?>
                    </td>
                    <?php else: ?>
                    <?php $finishTimeSeconds = !empty($result['finish_time']) ? timeToSeconds($result['finish_time']) : PHP_INT_MAX; ?>
                    <td class="col-time" data-sort-value="<?= $finishTimeSeconds ?>">
                        <?php if ($result['status'] === 'finished' && $result['finish_time']): ?>
                        <div class="split-time-main"><?= formatDisplayTime($result['finish_time']) ?></div>
                        <?php if ($isTimeRanked && !empty($result['time_behind']) && $result['time_behind'] !== '-'): ?>
                        <div class="split-time-details"><?= $result['time_behind'] ?></div>
                        <?php endif; ?>
                        <?php else: ?>
                        -
                        <?php endif; ?>
                    </td>
                    <?php foreach ($classSplits as $ss):
                        $splitTime = $result['ss' . $ss] ?? '';
                        $splitClass = '';
                        $splitRank = null;
                        $splitDiff = '';
                        $splitSeconds = !empty($splitTime) ? timeToSeconds($splitTime) : PHP_INT_MAX;

                        // Only show colors and rankings for competitive classes
                        if (!$isMotionOrKids) {
                            $splitRank = $result['split_rank_' . $ss] ?? null;
                            $splitDiff = $result['split_diff_' . $ss] ?? '';
                            if (!empty($splitTime) && isset($classData['split_stats'][$ss])) {
                                $stats = $classData['split_stats'][$ss];
                                $timeSeconds = timeToSeconds($splitTime);
                                if ($stats['range'] > 0.5) {
                                    $position = ($timeSeconds - $stats['min']) / $stats['range'];
                                    $level = min(10, max(1, floor($position * 9) + 1));
                                    $splitClass = 'split-' . $level;
                                }
                            }
                        }
                    ?>
                    <td class="col-split split-time-col table-col-hide-mobile <?= $splitClass ?>" data-sort-value="<?= $splitSeconds ?>">
                        <?php if (!empty($splitTime)): ?>
                        <div class="split-time-main"><?= formatDisplayTime($splitTime) ?></div>
                        <?php if (!$isMotionOrKids && ($splitDiff || $splitRank)): ?>
                        <div class="split-time-details"><?= $splitDiff ?: '' ?><?= $splitDiff && $splitRank ? ' ' : '' ?><?= $splitRank ? '(' . $splitRank . ')' : '' ?></div>
                        <?php endif; ?>
                        <?php else: ?>
                        -
                        <?php endif; ?>
                    </td>
                    <?php endforeach; ?>
                    <?php endif; ?>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <!-- Mobile Card View -->
    <div class="result-list">
        <?php foreach ($classData['results'] as $result):
            $searchData = strtolower($result['firstname'] . ' ' . $result['lastname'] . ' ' . ($result['club_name'] ?? ''));
        ?>
        <a href="/rider/<?= $result['rider_id'] ?>" class="result-item" data-search="<?= h($searchData) ?>">
            <div class="result-place <?= $result['class_position'] && $result['class_position'] <= 3 ? 'top-3' : '' ?>">
                <?php if (!$isTimeRanked): ?>
                    ✓
                <?php elseif ($result['status'] !== 'finished'): ?>
                    <span class="status-mini"><?= strtoupper(substr($result['status'], 0, 3)) ?></span>
                <?php elseif ($result['class_position'] == 1): ?>
                    <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon-mobile">
                <?php elseif ($result['class_position'] == 2): ?>
                    <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon-mobile">
                <?php elseif ($result['class_position'] == 3): ?>
                    <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon-mobile">
                <?php else: ?>
                    <?= $result['class_position'] ?>
                <?php endif; ?>
            </div>
            <div class="result-info">
                <div class="result-name"><?= h($result['firstname'] . ' ' . $result['lastname']) ?></div>
                <div class="result-club"><?= h($result['club_name'] ?? '-') ?></div>
            </div>
            <div class="result-time-col">
                <?php if ($result['status'] === 'finished' && $result['finish_time']): ?>
                    <div class="time-value"><?= formatDisplayTime($result['finish_time']) ?></div>
                    <?php if ($isTimeRanked && !empty($result['time_behind'])): ?>
                        <div class="time-behind-small"><?= $result['time_behind'] ?></div>
                    <?php endif; ?>
                <?php endif; ?>
            </div>
        </a>
        <?php endforeach; ?>
    </div>
</section>
<?php endforeach; ?>

<!-- Total Split Times Section (hidden by default, shown when toggle is active) -->
<?php if ($hasSplitTimes && !$isDH && count($globalSplitResults) > 0): ?>
<section class="card mb-lg total-split-section hidden" id="total-split-section">
    <div class="card-header">
        <div>
            <h2 class="card-title">Sträcktider Total</h2>
            <p class="card-subtitle"><?= count($globalSplitResults) ?> deltagare från alla klasser (exkl. Kids/Motion)</p>
        </div>
    </div>

    <!-- Desktop Table -->
    <div class="table-wrapper">
        <table class="table table--striped table--hover results-table" id="total-split-table">
            <thead>
                <tr>
                    <th class="col-place">#</th>
                    <th class="col-rider">Åkare</th>
                    <th class="col-club table-col-hide-mobile">Klubb</th>
                    <th class="col-class table-col-hide-mobile">Klass</th>
                    <?php foreach ($globalSplits as $ss): ?>
                    <th class="col-split split-time-col table-col-hide-mobile sortable-header" data-sort="ss<?= $ss ?>" onclick="sortTotalBySplit(this, <?= $ss ?>)"><?= $stageNames[$ss] ?? 'SS' . $ss ?> <span class="sort-icon"></span></th>
                    <?php endforeach; ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($globalSplitResults as $gIdx => $result):
                    $searchData = strtolower($result['firstname'] . ' ' . $result['lastname'] . ' ' . ($result['club_name'] ?? ''));
                ?>
                <tr class="result-row" onclick="window.location='/rider/<?= $result['rider_id'] ?>'" data-search="<?= h($searchData) ?>">
                    <td class="col-place total-position">
                        <?php if ($result['status'] !== 'finished'): ?>
                            <span class="status-badge status-<?= strtolower($result['status']) ?>"><?= strtoupper(substr($result['status'], 0, 3)) ?></span>
                        <?php else: ?>
                            <?= $gIdx + 1 ?>
                        <?php endif; ?>
                    </td>
                    <td class="col-rider">
                        <a href="/rider/<?= $result['rider_id'] ?>" class="rider-link">
                            <?= h($result['firstname'] . ' ' . $result['lastname']) ?>
                        </a>
                    </td>
                    <td class="col-club table-col-hide-mobile">
                        <?php if ($result['club_id']): ?>
                            <a href="/club/<?= $result['club_id'] ?>"><?= h($result['club_name'] ?? '-') ?></a>
                        <?php else: ?>
                            -
                        <?php endif; ?>
                    </td>
                    <td class="col-class table-col-hide-mobile">
                        <span class="class-badge"><?= h($result['original_class'] ?? '-') ?></span>
                    </td>
                    <?php foreach ($globalSplits as $ss):
                        $splitTime = $result['ss' . $ss] ?? '';
                        $splitClass = '';
                        $splitRank = $result['global_split_rank_' . $ss] ?? null;
                        $splitDiff = $result['global_split_diff_' . $ss] ?? '';
                        $splitSeconds = !empty($splitTime) ? timeToSeconds($splitTime) : PHP_INT_MAX;
                        if (!empty($splitTime) && isset($globalSplitStats[$ss])) {
                            $stats = $globalSplitStats[$ss];
                            $timeSeconds = timeToSeconds($splitTime);
                            if ($stats['range'] > 0.5) {
                                $position = ($timeSeconds - $stats['min']) / $stats['range'];
                                $level = min(10, max(1, floor($position * 9) + 1));
                                $splitClass = 'split-' . $level;
                            }
                        }
                    ?>
                    <td class="col-split split-time-col table-col-hide-mobile <?= $splitClass ?>" data-sort-value="<?= $splitSeconds ?>">
                        <?php if (!empty($splitTime)): ?>
                        <div class="split-time-main"><?= formatDisplayTime($splitTime) ?></div>
                        <div class="split-time-details"><?= $splitDiff ?: '' ?><?= $splitDiff && $splitRank ? ' ' : '' ?><?= $splitRank ? '(' . $splitRank . ')' : '' ?></div>
                        <?php else: ?>
                        -
                        <?php endif; ?>
                    </td>
                    <?php endforeach; ?>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <!-- Mobile Card View -->
    <div class="result-list">
        <?php foreach ($globalSplitResults as $gIdx => $result):
            $searchData = strtolower($result['firstname'] . ' ' . $result['lastname'] . ' ' . ($result['club_name'] ?? ''));
        ?>
        <a href="/rider/<?= $result['rider_id'] ?>" class="result-item result-item-splits" data-search="<?= h($searchData) ?>">
            <div class="result-place">
                <?php if ($result['status'] !== 'finished'): ?>
                    <span class="status-mini"><?= strtoupper(substr($result['status'], 0, 3)) ?></span>
                <?php else: ?>
                    <?= $gIdx + 1 ?>
                <?php endif; ?>
            </div>
            <div class="result-info">
                <div class="result-name"><?= h($result['firstname'] . ' ' . $result['lastname']) ?></div>
                <div class="result-club"><?= h($result['club_name'] ?? '-') ?> &middot; <?= h($result['original_class'] ?? '') ?></div>
                <div class="result-splits-row">
                    <?php foreach ($globalSplits as $ss):
                        $splitTime = $result['ss' . $ss] ?? '';
                        $splitRank = $result['global_split_rank_' . $ss] ?? null;
                    ?>
                    <div class="result-split-item">
                        <span class="split-label"><?= $stageNames[$ss] ?? 'SS' . $ss ?></span>
                        <span class="split-value"><?= !empty($splitTime) ? formatDisplayTime($splitTime) : '-' ?></span>
                        <?php if ($splitRank): ?><span class="split-rank">(<?= $splitRank ?>)</span><?php endif; ?>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </a>
        <?php endforeach; ?>
    </div>
</section>
<?php endif; ?>

<!-- Total DH Run Times Section (hidden by default, shown when toggle is active) -->
<?php if ($isDH && count($globalDHResults) > 0): ?>
<section class="card mb-lg total-dh-section hidden" id="total-dh-section">
    <div class="card-header">
        <div>
            <h2 class="card-title">Åktider Total</h2>
            <p class="card-subtitle"><?= count($globalDHResults) ?> deltagare från alla tävlingsklasser (exkl. Kids/Motion)</p>
        </div>
    </div>

    <!-- Desktop Table -->
    <div class="table-wrapper">
        <table class="table table--striped table--hover results-table" id="total-dh-table">
            <thead>
                <tr>
                    <th class="col-place">#</th>
                    <th class="col-rider">Åkare</th>
                    <th class="col-club table-col-hide-mobile">Klubb</th>
                    <th class="col-class table-col-hide-mobile">Klass</th>
                    <?php if ($eventFormat === 'DH_SWECUP'): ?>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run1" onclick="sortDHTotalByRun(this, 1)">Kval <span class="sort-icon"></span></th>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run2" onclick="sortDHTotalByRun(this, 2)">Final <span class="sort-icon"></span></th>
                    <?php elseif ($hasRun2Data): ?>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run1" onclick="sortDHTotalByRun(this, 1)">Åk 1 <span class="sort-icon"></span></th>
                    <th class="col-time col-dh-run table-col-hide-mobile sortable-header" data-sort="run2" onclick="sortDHTotalByRun(this, 2)">Åk 2 <span class="sort-icon"></span></th>
                    <?php else: ?>
                    <th class="col-time table-col-hide-mobile sortable-header" data-sort="run1" onclick="sortDHTotalByRun(this, 1)">Tid <span class="sort-icon"></span></th>
                    <?php endif; ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($globalDHResults as $gIdx => $result):
                    $searchData = strtolower($result['firstname'] . ' ' . $result['lastname'] . ' ' . ($result['club_name'] ?? ''));

                    // Calculate color classes for runs
                    $run1Time = $result['run_1_time'] ?? '';
                    $run2Time = $result['run_2_time'] ?? '';
                    $run1Class = '';
                    $run2Class = '';
                    $run1Rank = $result['global_run_rank_1'] ?? null;
                    $run2Rank = $result['global_run_rank_2'] ?? null;
                    $run1Diff = $result['global_run_diff_1'] ?? '';
                    $run2Diff = $result['global_run_diff_2'] ?? '';
                    $run1Seconds = !empty($run1Time) ? timeToSeconds($run1Time) : PHP_INT_MAX;
                    $run2Seconds = !empty($run2Time) ? timeToSeconds($run2Time) : PHP_INT_MAX;

                    if (!empty($run1Time) && isset($globalDHStats['run_1_time'])) {
                        $stats = $globalDHStats['run_1_time'];
                        $timeSeconds = timeToSeconds($run1Time);
                        if ($stats['range'] > 0.5) {
                            $position = ($timeSeconds - $stats['min']) / $stats['range'];
                            $level = min(10, max(1, floor($position * 9) + 1));
                            $run1Class = 'split-' . $level;
                        }
                    }
                    if (!empty($run2Time) && isset($globalDHStats['run_2_time'])) {
                        $stats = $globalDHStats['run_2_time'];
                        $timeSeconds = timeToSeconds($run2Time);
                        if ($stats['range'] > 0.5) {
                            $position = ($timeSeconds - $stats['min']) / $stats['range'];
                            $level = min(10, max(1, floor($position * 9) + 1));
                            $run2Class = 'split-' . $level;
                        }
                    }
                ?>
                <tr class="result-row" onclick="window.location='/rider/<?= $result['rider_id'] ?>'" data-search="<?= h($searchData) ?>">
                    <td class="col-place total-position">
                        <?php if ($result['status'] !== 'finished'): ?>
                            <span class="status-badge status-<?= strtolower($result['status']) ?>"><?= strtoupper(substr($result['status'], 0, 3)) ?></span>
                        <?php else: ?>
                            <?= $gIdx + 1 ?>
                        <?php endif; ?>
                    </td>
                    <td class="col-rider">
                        <a href="/rider/<?= $result['rider_id'] ?>" class="rider-link">
                            <?= h($result['firstname'] . ' ' . $result['lastname']) ?>
                        </a>
                    </td>
                    <td class="col-club table-col-hide-mobile">
                        <?php if ($result['club_id']): ?>
                            <a href="/club/<?= $result['club_id'] ?>"><?= h($result['club_name'] ?? '-') ?></a>
                        <?php else: ?>
                            -
                        <?php endif; ?>
                    </td>
                    <td class="col-class table-col-hide-mobile">
                        <span class="class-badge"><?= h($result['original_class'] ?? '-') ?></span>
                    </td>
                    <?php if ($eventFormat === 'DH_SWECUP' || $hasRun2Data): ?>
                    <td class="col-time col-dh-run table-col-hide-mobile <?= $run1Class ?>" data-sort-value="<?= $run1Seconds ?>">
                        <?php $r1Disp = formatDisplayTime($run1Time); if ($r1Disp): ?>
                        <div class="split-time-main"><?= $r1Disp ?></div>
                        <div class="split-time-details"><?= $run1Diff ?: '' ?><?= $run1Diff && $run1Rank ? ' ' : '' ?><?= $run1Rank ? '(' . $run1Rank . ')' : '' ?></div>
                        <?php else: ?><span class="text-secondary">DNS</span><?php endif; ?>
                    </td>
                    <td class="col-time col-dh-run table-col-hide-mobile <?= $run2Class ?>" data-sort-value="<?= $run2Seconds ?>">
                        <?php $r2Disp = formatDisplayTime($run2Time); if ($r2Disp): ?>
                        <div class="split-time-main"><?= $r2Disp ?></div>
                        <div class="split-time-details"><?= $run2Diff ?: '' ?><?= $run2Diff && $run2Rank ? ' ' : '' ?><?= $run2Rank ? '(' . $run2Rank . ')' : '' ?></div>
                        <?php else: ?><span class="text-secondary">DNS</span><?php endif; ?>
                    </td>
                    <?php else: ?>
                    <td class="col-time table-col-hide-mobile <?= $run1Class ?>" data-sort-value="<?= $run1Seconds ?>">
                        <?php $r1Disp = formatDisplayTime($run1Time); if ($r1Disp): ?>
                        <div class="split-time-main"><?= $r1Disp ?></div>
                        <?php else: ?><span class="text-secondary">DNS</span><?php endif; ?>
                    </td>
                    <?php endif; ?>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <!-- Mobile Card View -->
    <div class="result-list">
        <?php foreach ($globalDHResults as $gIdx => $result):
            $searchData = strtolower($result['firstname'] . ' ' . $result['lastname'] . ' ' . ($result['club_name'] ?? ''));
            $run1Time = $result['run_1_time'] ?? '';
            $run2Time = $result['run_2_time'] ?? '';
            $run1Rank = $result['global_run_rank_1'] ?? null;
            $run2Rank = $result['global_run_rank_2'] ?? null;
        ?>
        <a href="/rider/<?= $result['rider_id'] ?>" class="result-item result-item-splits" data-search="<?= h($searchData) ?>">
            <div class="result-place">
                <?php if ($result['status'] !== 'finished'): ?>
                    <span class="status-mini"><?= strtoupper(substr($result['status'], 0, 3)) ?></span>
                <?php else: ?>
                    <?= $gIdx + 1 ?>
                <?php endif; ?>
            </div>
            <div class="result-info">
                <div class="result-name"><?= h($result['firstname'] . ' ' . $result['lastname']) ?></div>
                <div class="result-club"><?= h($result['club_name'] ?? '-') ?> &middot; <?= h($result['original_class'] ?? '') ?></div>
                <div class="result-splits-row">
                    <?php if ($eventFormat === 'DH_SWECUP' || $hasRun2Data): ?>
                    <div class="result-split-item">
                        <span class="split-label"><?= $eventFormat === 'DH_SWECUP' ? 'Kval' : 'Åk 1' ?></span>
                        <span class="split-value"><?= formatDisplayTime($run1Time) ?: 'DNS' ?></span>
                        <?php if ($run1Rank): ?><span class="split-rank">(<?= $run1Rank ?>)</span><?php endif; ?>
                    </div>
                    <div class="result-split-item">
                        <span class="split-label"><?= $eventFormat === 'DH_SWECUP' ? 'Final' : 'Åk 2' ?></span>
                        <span class="split-value"><?= formatDisplayTime($run2Time) ?: 'DNS' ?></span>
                        <?php if ($run2Rank): ?><span class="split-rank">(<?= $run2Rank ?>)</span><?php endif; ?>
                    </div>
                    <?php else: ?>
                    <div class="result-split-item">
                        <span class="split-label">Tid</span>
                        <span class="split-value"><?= formatDisplayTime($run1Time) ?: 'DNS' ?></span>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </a>
        <?php endforeach; ?>
    </div>
</section>
<?php endif; ?>

<?php endif; ?>

<?php elseif ($activeTab === 'info'): ?>
<!-- INBJUDAN TAB - Invitation + Facilities & Logistics -->
<?php
// Get invitation content
$invitationText = getEventContent($event, 'invitation', 'invitation_use_global', $globalTextMap, 'invitation_hidden');

// Get all facility content
$hydrationInfo = getEventContent($event, 'hydration_stations', 'hydration_use_global', $globalTextMap, 'hydration_hidden');
$toiletsInfo = getEventContent($event, 'toilets_showers', 'toilets_use_global', $globalTextMap, 'toilets_hidden');
$bikeWashInfo = getEventContent($event, 'bike_wash', 'bike_wash_use_global', $globalTextMap, 'bike_wash_hidden');
$foodCafe = getEventContent($event, 'food_cafe', 'food_use_global', $globalTextMap, 'food_hidden');
$shopsInfo = getEventContent($event, 'shops_info', 'shops_use_global', $globalTextMap, 'shops_hidden');
$exhibitorsInfo = getEventContent($event, 'exhibitors', 'exhibitors_use_global', $globalTextMap, 'exhibitors_hidden');
$parkingInfo = !empty($event['parking_hidden']) ? '' : ($event['parking_detailed'] ?? '');
$hotelInfo = !empty($event['hotel_hidden']) ? '' : ($event['hotel_accommodation'] ?? '');
$localInfo = getEventContent($event, 'local_info', 'local_use_global', $globalTextMap, 'local_hidden');
$medicalInfo = getEventContent($event, 'medical_info', 'medical_use_global', $globalTextMap, 'medical_hidden');
$mediaInfo = getEventContent($event, 'media_production', 'media_use_global', $globalTextMap, 'media_hidden');
$contactsInfo = getEventContent($event, 'contacts_info', 'contacts_use_global', $globalTextMap, 'contacts_hidden');
$hasFacilities = $hydrationInfo || $toiletsInfo || $bikeWashInfo || $foodCafe || $shopsInfo || $exhibitorsInfo || $parkingInfo || $hotelInfo || $localInfo || $medicalInfo || $mediaInfo || $contactsInfo;
?>

<?php if (!empty($invitationText)): ?>
<section class="card mb-lg">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="mail-open"></i>
            Inbjudan
        </h2>
    </div>
    <div class="card-body">
        <div class="prose"><?= nl2br(h($invitationText)) ?></div>
    </div>
</section>
<?php endif; ?>

<section class="card">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="info"></i>
            Faciliteter & Logistik
        </h2>
    </div>
    <div class="card-body">
        <?php if ($hasFacilities): ?>
        <div class="info-grid">
            <?php if (!empty($hydrationInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="droplets"></i> Vätskekontroller</h3>
                <p><?= nl2br(h($hydrationInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($toiletsInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="bath"></i> Toaletter/Dusch</h3>
                <p><?= nl2br(h($toiletsInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($bikeWashInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="sparkles"></i> Cykeltvätt</h3>
                <p><?= nl2br(h($bikeWashInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($foodCafe)): ?>
            <div class="info-block">
                <h3><i data-lucide="utensils"></i> Mat/Café</h3>
                <p><?= nl2br(h($foodCafe)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($shopsInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="shopping-bag"></i> Affärer</h3>
                <p><?= nl2br(h($shopsInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($exhibitorsInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="store"></i> Utställare</h3>
                <p><?= nl2br(h($exhibitorsInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($parkingInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="car"></i> Parkering</h3>
                <p><?= nl2br(h($parkingInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($hotelInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="bed"></i> Hotell/Boende</h3>
                <p><?= nl2br(h($hotelInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($localInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="map-pin"></i> Lokal information</h3>
                <p><?= nl2br(h($localInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($medicalInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="heart-pulse"></i> Sjukvård</h3>
                <p><?= nl2br(h($medicalInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($mediaInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="camera"></i> Media</h3>
                <p><?= nl2br(h($mediaInfo)) ?></p>
            </div>
            <?php endif; ?>

            <?php if (!empty($contactsInfo)): ?>
            <div class="info-block">
                <h3><i data-lucide="phone"></i> Kontakter</h3>
                <p><?= nl2br(h($contactsInfo)) ?></p>
            </div>
            <?php endif; ?>
        </div>
        <?php else: ?>
        <p class="text-muted">Ingen information tillgänglig för detta event ännu.</p>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'pm'): ?>
<!-- PM TAB - With subcategories -->
<?php
// Check if PM is published yet
if (!$pmPublished):
?>
<section class="card">
    <div class="card-body">
        <p class="text-muted text-center">PM publiceras <?= date('Y-m-d H:i', strtotime($event['pm_publish_at'])) ?></p>
    </div>
</section>
<?php else:
// Get all PM-related content
$pmContent = getEventContent($event, 'pm_content', 'pm_use_global', $globalTextMap, 'pm_hidden');
$driverMeetingPM = getEventContent($event, 'driver_meeting', 'driver_meeting_use_global', $globalTextMap, 'driver_meeting_hidden');
$trainingPM = getEventContent($event, 'training_info', 'training_use_global', $globalTextMap, 'training_hidden');
$timingPM = getEventContent($event, 'timing_info', 'timing_use_global', $globalTextMap, 'timing_hidden');
$liftPM = getEventContent($event, 'lift_info', 'lift_use_global', $globalTextMap, 'lift_hidden');
$rulesPM = getEventContent($event, 'competition_rules', 'rules_use_global', $globalTextMap, 'rules_hidden');
$insurancePM = getEventContent($event, 'insurance_info', 'insurance_use_global', $globalTextMap, 'insurance_hidden');
$equipmentPM = getEventContent($event, 'equipment_info', 'equipment_use_global', $globalTextMap, 'equipment_hidden');
$scfPM = getEventContent($event, 'scf_representatives', 'scf_use_global', $globalTextMap, 'scf_hidden');
$medicalPM = getEventContent($event, 'medical_info', 'medical_use_global', $globalTextMap, 'medical_hidden');
$hasPMContent = $pmContent || $driverMeetingPM || $trainingPM || $timingPM || $liftPM || $rulesPM || $insurancePM || $equipmentPM || $scfPM || $medicalPM;
?>
<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="clipboard-list"></i> PM (Promemoria)</h2>
    </div>
    <div class="card-body">
        <?php if ($pmContent): ?>
        <div class="prose mb-lg"><?= nl2br(h($pmContent)) ?></div>
        <?php endif; ?>

        <?php if ($driverMeetingPM || $trainingPM || $timingPM || $liftPM || $rulesPM || $insurancePM || $equipmentPM || $scfPM || $medicalPM): ?>
        <div class="info-grid">
            <?php if ($driverMeetingPM): ?>
            <div class="info-block">
                <h3><i data-lucide="megaphone"></i> Förarmöte</h3>
                <p><?= nl2br(h($driverMeetingPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($trainingPM): ?>
            <div class="info-block">
                <h3><i data-lucide="bike"></i> Träning</h3>
                <p><?= nl2br(h($trainingPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($timingPM): ?>
            <div class="info-block">
                <h3><i data-lucide="timer"></i> Tidtagning</h3>
                <p><?= nl2br(h($timingPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($liftPM): ?>
            <div class="info-block">
                <h3><i data-lucide="cable-car"></i> Lift</h3>
                <p><?= nl2br(h($liftPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($rulesPM): ?>
            <div class="info-block">
                <h3><i data-lucide="book-open"></i> Tävlingsregler</h3>
                <p><?= nl2br(h($rulesPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($insurancePM): ?>
            <div class="info-block">
                <h3><i data-lucide="shield-check"></i> Försäkring</h3>
                <p><?= nl2br(h($insurancePM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($equipmentPM): ?>
            <div class="info-block">
                <h3><i data-lucide="hard-hat"></i> Utrustning</h3>
                <p><?= nl2br(h($equipmentPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($medicalPM): ?>
            <div class="info-block">
                <h3><i data-lucide="heart-pulse"></i> Sjukvård</h3>
                <p><?= nl2br(h($medicalPM)) ?></p>
            </div>
            <?php endif; ?>

            <?php if ($scfPM): ?>
            <div class="info-block">
                <h3><i data-lucide="badge-check"></i> SCF Representanter</h3>
                <p><?= nl2br(h($scfPM)) ?></p>
            </div>
            <?php endif; ?>
        </div>
        <?php endif; ?>

        <?php if (!$hasPMContent): ?>
        <p class="text-muted">Inget PM tillgängligt för detta event.</p>
        <?php endif; ?>
    </div>
</section>
<?php endif; // end pmPublished check ?>

<?php elseif ($activeTab === 'jury'): ?>
<!-- JURY TAB -->
<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="gavel"></i> Jurykommuniké</h2>
    </div>
    <div class="card-body">
        <?php $juryContent = getEventContent($event, 'jury_communication', 'jury_use_global', $globalTextMap, 'jury_hidden'); ?>
        <?php if ($juryContent): ?>
            <div class="prose"><?= nl2br(h($juryContent)) ?></div>
        <?php else: ?>
            <p class="text-muted">Ingen jurykommuniké tillgänglig.</p>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'schema'): ?>
<!-- SCHEDULE TAB -->
<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="calendar-clock"></i> Tävlingsschema</h2>
    </div>
    <div class="card-body">
        <?php $scheduleContent = getEventContent($event, 'competition_schedule', 'schedule_use_global', $globalTextMap, 'schedule_hidden'); ?>
        <?php if ($scheduleContent): ?>
            <div class="prose"><?= nl2br(h($scheduleContent)) ?></div>
        <?php else: ?>
            <p class="text-muted">Inget tävlingsschema tillgängligt.</p>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'starttider'): ?>
<!-- START TIMES TAB -->
<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="clock"></i> Starttider</h2>
    </div>
    <div class="card-body">
        <?php $startContent = getEventContent($event, 'start_times', 'start_times_use_global', $globalTextMap, 'start_times_hidden'); ?>
        <?php if ($startContent): ?>
            <div class="prose"><?= nl2br(h($startContent)) ?></div>
        <?php else: ?>
            <p class="text-muted">Inga starttider publicerade ännu.</p>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'karta'): ?>
<!-- MAP TAB - Full width interactive map -->
<?php if ($hasInteractiveMap): ?>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
<link rel="stylesheet" href="<?= hub_asset('css/map.css') ?>">
<?php
require_once ROOT_PATH . '/components/event-map.php';
render_event_map($eventId, $db, [
    'height' => 'min(calc(100vh - 250px), 600px)',
    'fullscreen' => false,
    'show_close' => false,
    'event_name' => $event['name'] ?? 'Event'
]);
?>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script>if (typeof lucide !== 'undefined') lucide.createIcons();</script>
<script src="<?= hub_asset('js/event-map.js') ?>"></script>
<?php else: ?>
<p class="text-muted">Ingen interaktiv karta tillgänglig.</p>
<?php endif; ?>

<?php elseif ($activeTab === 'nyheter'): ?>
<!-- NEWS/MEDIA TAB -->
<?php
// Fetch race reports for this event
$eventReports = [];
try {
    require_once HUB_ROOT . '/includes/RaceReportManager.php';
    $reportManager = new RaceReportManager($db);
    $reportsResult = $reportManager->listReports([
        'event_id' => $eventId,
        'per_page' => 20
    ]);
    $eventReports = $reportsResult['reports'];
} catch (Exception $e) {
    // Ignore
}
?>
<section class="card">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="newspaper"></i>
            Media och nyheter
            <span class="badge badge--primary ml-sm"><?= count($eventReports) ?></span>
        </h2>
        <a href="/news?event=<?= $eventId ?>" class="btn btn-sm btn-secondary">
            <i data-lucide="external-link"></i>
            Visa alla
        </a>
    </div>
    <div class="card-body">
        <?php if (empty($eventReports)): ?>
            <p class="text-muted">Inga nyheter eller media fran detta event an.</p>
        <?php else: ?>
        <div class="event-news-grid">
            <?php foreach ($eventReports as $report): ?>
            <a href="/news/<?= htmlspecialchars($report['slug']) ?>" class="event-news-card">
                <div class="event-news-card__image">
                    <?php if ($report['featured_image']): ?>
                    <img src="<?= htmlspecialchars($report['featured_image']) ?>" alt="" loading="lazy">
                    <?php elseif ($report['youtube_video_id']): ?>
                    <img src="https://img.youtube.com/vi/<?= htmlspecialchars($report['youtube_video_id']) ?>/hqdefault.jpg" alt="" loading="lazy">
                    <div class="event-news-card__play"><i data-lucide="play"></i></div>
                    <?php else: ?>
                    <div class="event-news-card__placeholder"><i data-lucide="image"></i></div>
                    <?php endif; ?>
                </div>
                <div class="event-news-card__content">
                    <h3 class="event-news-card__title"><?= htmlspecialchars($report['title']) ?></h3>
                    <div class="event-news-card__meta">
                        <span><?= htmlspecialchars($report['firstname'] . ' ' . $report['lastname']) ?></span>
                        <span><?= date('j M Y', strtotime($report['published_at'])) ?></span>
                    </div>
                    <div class="event-news-card__stats">
                        <span><i data-lucide="eye"></i> <?= number_format($report['views']) ?></span>
                        <span><i data-lucide="heart"></i> <?= number_format($report['likes']) ?></span>
                    </div>
                </div>
            </a>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>

        <?php if (function_exists('hub_current_user') && hub_current_user()): ?>
        <div class="event-news-cta">
            <p>Deltog du i denna tavling? Dela din upplevelse!</p>
            <a href="/profile/race-reports" class="btn btn-primary">
                <i data-lucide="pen-tool"></i>
                Skriv Race Report
            </a>
        </div>
        <?php endif; ?>
    </div>
</section>

<style>
.event-news-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.event-news-card {
    display: flex;
    flex-direction: column;
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
    text-decoration: none;
    transition: all 0.15s ease;
}

.event-news-card:hover {
    border-color: var(--color-accent);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.event-news-card__image {
    position: relative;
    aspect-ratio: 16 / 9;
    background: var(--color-bg-page);
    overflow: hidden;
}

.event-news-card__image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.event-news-card__placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-muted);
}

.event-news-card__placeholder i {
    width: 32px;
    height: 32px;
}

.event-news-card__play {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 40px;
    height: 40px;
    background: rgba(0,0,0,0.7);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.event-news-card__play i {
    width: 18px;
    height: 18px;
    margin-left: 2px;
}

.event-news-card__content {
    padding: var(--space-md);
}

.event-news-card__title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 var(--space-xs);
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.event-news-card__meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--color-text-muted);
    margin-bottom: var(--space-xs);
}

.event-news-card__stats {
    display: flex;
    gap: var(--space-md);
    font-size: 0.75rem;
    color: var(--color-text-muted);
}

.event-news-card__stats span {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
}

.event-news-card__stats i {
    width: 12px;
    height: 12px;
}

.event-news-cta {
    text-align: center;
    padding: var(--space-lg);
    background: var(--color-accent-light);
    border-radius: var(--radius-md);
}

.event-news-cta p {
    margin: 0 0 var(--space-md);
    color: var(--color-text-secondary);
}

@media (max-width: 767px) {
    .event-news-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<?php elseif ($activeTab === 'anmalda'): ?>
<!-- REGISTERED PARTICIPANTS TAB -->
<section class="card">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="users"></i>
            Anmälda deltagare
            <span class="badge badge--primary ml-sm"><?= $totalRegistrations ?></span>
        </h2>
    </div>
    <div class="card-body">
        <?php if (empty($registrationsByClass)): ?>
            <p class="text-muted">Inga anmälningar ännu.</p>
        <?php else: ?>
        <?php foreach ($registrationsByClass as $className => $classRegs): ?>
        <div class="reg-class-group mb-lg">
            <h3 class="reg-class-group__title">
                <?= h($className) ?>
                <span class="badge badge--neutral ml-sm"><?= count($classRegs) ?></span>
            </h3>
            <div class="table-wrapper">
                <table class="table table--striped table--compact">
                    <thead>
                        <tr>
                            <th style="width:40px">#</th>
                            <th>Namn</th>
                            <th>Klubb</th>
                            <th style="width:100px">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($classRegs as $index => $reg): ?>
                        <tr>
                            <td class="text-muted"><?= $index + 1 ?></td>
                            <td><strong><?= h(($reg['firstname'] ?? $reg['first_name'] ?? '') . ' ' . ($reg['lastname'] ?? $reg['last_name'] ?? '')) ?></strong></td>
                            <td class="text-secondary"><?= h($reg['club_name'] ?? '-') ?></td>
                            <td>
                                <?php
                                $statusClass = 'badge--secondary';
                                $statusText = ucfirst($reg['status'] ?? 'pending');
                                if ($reg['status'] === 'confirmed' || $reg['payment_status'] === 'paid') {
                                    $statusClass = 'badge--success';
                                    $statusText = 'Betald';
                                } elseif ($reg['status'] === 'pending') {
                                    $statusClass = 'badge--warning';
                                    $statusText = 'Väntande';
                                }
                                ?>
                                <span class="badge <?= $statusClass ?>"><?= $statusText ?></span>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
        <?php endforeach; ?>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'biljetter'): ?>
<!-- TICKETS TAB -->
<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="ticket"></i> Biljetter</h2>
    </div>
    <div class="card-body">
        <?php if (!$ticketingEnabled): ?>
            <p class="text-muted">Biljettförsäljning är inte aktiverad för detta event.</p>
        <?php else: ?>
            <p>Kontakta arrangören för biljettinformation.</p>
            <?php if (!empty($event['registration_url'])): ?>
            <a href="<?= h($event['registration_url']) ?>" target="_blank" class="btn btn--primary mt-md">
                <i data-lucide="external-link"></i>
                Extern anmälan
            </a>
            <?php endif; ?>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'anmalan'): ?>
<!-- REGISTRATION TAB -->
<?php
// Load registration-related data
$currentUser = hub_current_user();
$isLoggedIn = hub_is_logged_in();

// Get pricing info for this event
$eventPricing = [];
try {
    $pricingStmt = $db->prepare("
        SELECT epr.class_id, epr.base_price, epr.early_bird_price, epr.late_fee,
               c.name as class_name, c.display_name, c.gender, c.min_age, c.max_age
        FROM event_pricing_rules epr
        JOIN classes c ON epr.class_id = c.id
        WHERE epr.event_id = ?
        ORDER BY c.sort_order, c.name
    ");
    $pricingStmt->execute([$eventId]);
    $eventPricing = $pricingStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Pricing rules might not exist
}

// Check early bird / late fee status
$now = time();
$isEarlyBird = false;
$isLateFee = false;
$earlyBirdDeadline = null;
$lateFeeStart = null;

if (!empty($event['early_bird_deadline'])) {
    $earlyBirdDeadline = strtotime($event['early_bird_deadline']);
    $isEarlyBird = $now < $earlyBirdDeadline;
}
if (!empty($event['late_fee_start'])) {
    $lateFeeStart = strtotime($event['late_fee_start']);
    $isLateFee = $now >= $lateFeeStart;
}

// Check if user already registered
$existingRegistration = null;
if ($isLoggedIn && $currentUser) {
    try {
        // Note: event_registrations uses 'category' (VARCHAR) instead of class_id
        $checkStmt = $db->prepare("
            SELECT er.*, er.category as class_name
            FROM event_registrations er
            WHERE er.event_id = ? AND er.rider_id = ? AND er.status != 'cancelled'
        ");
        $checkStmt->execute([$eventId, $currentUser['id']]);
        $existingRegistration = $checkStmt->fetch(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {}
}

// Get eligible classes if user is logged in
$eligibleClasses = [];
if ($isLoggedIn && $currentUser && !$existingRegistration) {
    require_once HUB_ROOT . '/includes/registration-validator.php';
    $eligibleClasses = getEligibleClasses($db, $eventId, $currentUser['id']);
}

// Check if event is part of a series with series registration
$seriesPassAvailable = false;
$seriesInfo = null;
if (!empty($event['series_id'])) {
    try {
        $seriesStmt = $db->prepare("
            SELECT s.id, s.name, s.logo, s.allow_series_registration,
                   s.series_discount_percent, s.registration_opens, s.registration_closes
            FROM series s
            WHERE s.id = ? AND s.allow_series_registration = 1
        ");
        $seriesStmt->execute([$event['series_id']]);
        $seriesInfo = $seriesStmt->fetch(PDO::FETCH_ASSOC);
        if ($seriesInfo) {
            $seriesOpen = true;
            if ($seriesInfo['registration_opens'] && strtotime($seriesInfo['registration_opens']) > $now) {
                $seriesOpen = false;
            }
            if ($seriesInfo['registration_closes'] && strtotime($seriesInfo['registration_closes']) < $now) {
                $seriesOpen = false;
            }
            $seriesPassAvailable = $seriesOpen;
        }
    } catch (PDOException $e) {}
}
?>

<style>
/* Registration form styles - mobile first */
.reg-form {
    display: grid;
    gap: var(--space-md);
}

.reg-class-list {
    display: grid;
    gap: var(--space-sm);
}

.reg-class-item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
}

.reg-class-item:hover {
    border-color: var(--color-accent);
}

.reg-class-item.selected {
    border-color: var(--color-accent);
    background: var(--color-accent-light);
}

.reg-class-item.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.reg-class-radio {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.reg-class-info {
    flex: 1;
    min-width: 0;
}

.reg-class-name {
    font-weight: 600;
    color: var(--color-text-primary);
}

.reg-class-desc {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.reg-class-price {
    text-align: right;
    flex-shrink: 0;
}

.reg-class-price__current {
    font-weight: 700;
    font-size: 1.125rem;
    color: var(--color-accent);
}

.reg-class-price__original {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-decoration: line-through;
}

.reg-series-upsell {
    background: linear-gradient(135deg, var(--color-accent-light) 0%, var(--color-bg-surface) 100%);
    border: 1px solid var(--color-accent);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-top: var(--space-md);
}

.reg-series-upsell__header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-sm);
}

.reg-series-upsell__logo {
    width: 40px;
    height: 40px;
    object-fit: contain;
}

.reg-series-upsell__title {
    font-weight: 600;
    color: var(--color-text-primary);
}

.reg-series-upsell__savings {
    font-size: 0.875rem;
    color: var(--color-success);
    font-weight: 600;
}

.reg-summary {
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-top: var(--space-md);
}

.reg-summary__row {
    display: flex;
    justify-content: space-between;
    padding: var(--space-xs) 0;
}

.reg-summary__total {
    border-top: 1px solid var(--color-border);
    padding-top: var(--space-sm);
    margin-top: var(--space-sm);
    font-weight: 700;
    font-size: 1.25rem;
}

.reg-existing {
    padding: var(--space-lg);
    text-align: center;
}

.reg-existing__icon {
    width: 48px;
    height: 48px;
    color: var(--color-success);
    margin-bottom: var(--space-md);
}

@media (max-width: 767px) {
    .reg-class-item {
        flex-wrap: wrap;
    }
    .reg-class-price {
        width: 100%;
        text-align: left;
        margin-top: var(--space-xs);
        padding-left: 36px;
    }
}

/* Multi-rider cart styles */
.reg-cart {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-lg);
}

.reg-cart__header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.reg-cart__header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

.reg-cart__items {
    padding: var(--space-sm);
}

.reg-cart__item {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-card);
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-xs);
}

.reg-cart__item:last-child {
    margin-bottom: 0;
}

.reg-cart__item-info {
    flex: 1;
    min-width: 0;
}

.reg-cart__item-rider {
    font-weight: 600;
    color: var(--color-text-primary);
}

.reg-cart__item-class {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.reg-cart__item-price {
    font-weight: 600;
    color: var(--color-accent);
    white-space: nowrap;
}

.reg-cart__item-remove {
    background: none;
    border: none;
    color: var(--color-text-muted);
    cursor: pointer;
    padding: var(--space-xs);
    border-radius: var(--radius-sm);
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.reg-cart__item-remove:hover {
    color: var(--color-error);
    background: rgba(239, 68, 68, 0.1);
}

.reg-cart__summary {
    padding: var(--space-md);
    border-top: 1px solid var(--color-border);
    background: var(--color-bg-hover);
}

.reg-cart__savings {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
    border: 1px solid var(--color-success);
    border-radius: var(--radius-sm);
    padding: var(--space-sm) var(--space-md);
    margin-top: var(--space-sm);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    color: var(--color-success);
    font-weight: 500;
}

.reg-cart__actions {
    padding: var(--space-md);
    border-top: 1px solid var(--color-border);
}

/* Add rider section */
.reg-add-rider {
    background: var(--color-bg-surface);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
}

.reg-add-rider__header {
    margin-bottom: var(--space-md);
}

.reg-add-rider__header h4 {
    margin: 0 0 var(--space-xs) 0;
    font-weight: 600;
}

.reg-rider-select {
    display: grid;
    gap: var(--space-md);
}

.reg-rider-select .form-group {
    margin: 0;
}

/* Create rider inline form */
.reg-create-rider {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-top: var(--space-md);
}

.reg-create-rider__fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-md);
}

@media (max-width: 599px) {
    .reg-create-rider__fields {
        grid-template-columns: 1fr;
    }
}

/* Registered participants by class */
.reg-class-group {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.reg-class-group__title {
    background: var(--color-bg-surface);
    padding: var(--space-sm) var(--space-md);
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
}

.reg-class-group .table-wrapper {
    margin: 0;
}

.reg-class-group .table {
    margin: 0;
}

.table--compact th,
.table--compact td {
    padding: var(--space-xs) var(--space-sm);
}
</style>

<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="user-plus"></i> Anmälan</h2>
    </div>
    <div class="card-body">
        <?php if (!$registrationOpen): ?>
            <div class="alert alert--warning">
                <strong>Anmälan stängd</strong>
                <?php if (!empty($event['registration_deadline'])): ?>
                <p>Anmälan stängde <?= date('j F Y', strtotime($event['registration_deadline'])) ?>.</p>
                <?php endif; ?>
            </div>

        <?php elseif (!empty($event['registration_url'])): ?>
            <p>Anmälan sker via extern länk:</p>
            <a href="<?= h($event['registration_url']) ?>" target="_blank" class="btn btn--primary mt-md">
                <i data-lucide="external-link"></i>
                Gå till anmälan
            </a>

        <?php elseif (!$isLoggedIn): ?>
            <!-- Not logged in -->
            <div class="text-center py-lg">
                <i data-lucide="log-in" style="width:48px;height:48px;color:var(--color-text-muted);margin-bottom:var(--space-md);"></i>
                <h3 class="mb-sm">Logga in för att anmäla dig</h3>
                <p class="text-secondary mb-lg">Du måste vara inloggad för att kunna anmäla dig till eventet.</p>
                <a href="/login?redirect=<?= urlencode('/event/' . $eventId . '?tab=anmalan') ?>" class="btn btn--primary">
                    <i data-lucide="log-in"></i>
                    Logga in
                </a>
                <p class="text-sm text-muted mt-md">
                    Har du inget konto? <a href="/register?redirect=<?= urlencode('/event/' . $eventId . '?tab=anmalan') ?>">Registrera dig här</a>
                </p>
            </div>

        <?php elseif ($existingRegistration): ?>
            <!-- Already registered -->
            <div class="reg-existing">
                <i data-lucide="check-circle" class="reg-existing__icon"></i>
                <h3 class="mb-sm">Du är anmäld!</h3>
                <p class="text-secondary mb-md">
                    Du är anmäld i <strong><?= h($existingRegistration['class_name'] ?: $existingRegistration['category']) ?></strong>
                </p>
                <?php if ($existingRegistration['payment_status'] !== 'paid'): ?>
                    <div class="alert alert--warning mb-md">
                        <i data-lucide="credit-card"></i>
                        Betalning saknas. <a href="/checkout?registration=<?= $existingRegistration['id'] ?>">Betala nu</a>
                    </div>
                <?php else: ?>
                    <span class="badge badge-success">Betald</span>
                <?php endif; ?>
                <div class="mt-lg">
                    <a href="/profile/tickets" class="btn btn--ghost">
                        <i data-lucide="ticket"></i>
                        Mina biljetter
                    </a>
                </div>
            </div>

        <?php elseif (empty($eventPricing)): ?>
            <div class="alert alert--info">
                <i data-lucide="info"></i>
                Priserna för detta event är inte konfigurerade ännu. Kontakta arrangören.
            </div>

        <?php else: ?>
            <!-- Multi-Rider Registration Form -->
            <?php if ($isEarlyBird): ?>
                <div class="alert alert--success mb-md">
                    <i data-lucide="clock"></i>
                    <strong>Early Bird!</strong> Boka före <?= date('j M', $earlyBirdDeadline) ?> och spara pengar.
                </div>
            <?php elseif ($isLateFee): ?>
                <div class="alert alert--warning mb-md">
                    <i data-lucide="alert-triangle"></i>
                    <strong>Efteranmälan</strong> - extra avgift tillkommer.
                </div>
            <?php endif; ?>

            <!-- Cart (hidden until items added) -->
            <div id="registrationCart" class="reg-cart" style="display:none;">
                <div class="reg-cart__header">
                    <h3><i data-lucide="shopping-cart"></i> Anmälningar</h3>
                </div>
                <div id="cartItems" class="reg-cart__items"></div>
                <div class="reg-cart__summary">
                    <div class="reg-summary__row">
                        <span>Antal deltagare</span>
                        <span id="cartCount">0</span>
                    </div>
                    <div class="reg-summary__row reg-summary__total">
                        <span>Totalt</span>
                        <span id="cartTotal">0 kr</span>
                    </div>
                    <div id="cartSavings" class="reg-cart__savings" style="display:none;">
                        <i data-lucide="piggy-bank"></i>
                        <span>Du sparar <strong id="savingsAmount">0 kr</strong> i Swish-avgifter!</span>
                    </div>
                </div>
                <button type="button" id="checkoutBtn" class="btn btn--primary btn--lg btn--block">
                    <i data-lucide="credit-card"></i>
                    Gå till betalning
                </button>
            </div>

            <!-- Add Rider Section -->
            <div id="addRiderSection" class="reg-add-rider">
                <h3 class="mb-md">Lägg till deltagare</h3>

                <!-- Rider Selector -->
                <div class="form-group">
                    <label class="form-label">Välj vem som ska anmälas</label>
                    <select id="riderSelect" class="form-select">
                        <option value="">-- Välj deltagare --</option>
                        <option value="<?= $currentUser['id'] ?>">
                            <?= h($currentUser['firstname'] . ' ' . $currentUser['lastname']) ?> (du själv)
                        </option>
                        <!-- Family members loaded via JS -->
                    </select>
                </div>

                <!-- Class Selection (shown after rider selected) -->
                <div id="classSelection" style="display:none;">
                    <label class="form-label">Välj klass</label>
                    <div id="classList" class="reg-class-list"></div>

                    <button type="button" id="addToCartBtn" class="btn btn--secondary btn--block mt-md" disabled>
                        <i data-lucide="plus"></i>
                        Lägg till i anmälan
                    </button>
                </div>

                <div class="reg-add-more mt-md">
                    <button type="button" id="addAnotherBtn" class="btn btn--ghost btn--sm" style="display:none;">
                        <i data-lucide="user-plus"></i>
                        Lägg till fler deltagare
                    </button>
                </div>
            </div>

            <?php if ($seriesPassAvailable && $seriesInfo): ?>
            <div class="reg-series-upsell mt-lg">
                <div class="reg-series-upsell__header">
                    <?php if ($seriesInfo['logo']): ?>
                        <img src="<?= h($seriesInfo['logo']) ?>" alt="" class="reg-series-upsell__logo">
                    <?php endif; ?>
                    <div>
                        <div class="reg-series-upsell__title">Köp Serie-pass istället?</div>
                        <div class="reg-series-upsell__savings">
                            <i data-lucide="tag"></i>
                            Spara <?= $seriesInfo['series_discount_percent'] ?>% på alla event
                        </div>
                    </div>
                </div>
                <p class="text-sm text-secondary mb-sm">
                    Med ett serie-pass för <?= h($seriesInfo['name']) ?> får du tillgång till alla säsongens event till rabatterat pris.
                </p>
                <a href="/register/series?id=<?= $seriesInfo['id'] ?>" class="btn btn--outline btn--sm">
                    <i data-lucide="ticket"></i>
                    Se serie-pass
                </a>
            </div>
            <?php endif; ?>

            <script>
            (function() {
                const eventId = <?= $eventId ?>;
                const currentUserId = <?= $currentUser['id'] ?? 0 ?>;
                const isEarlyBird = <?= $isEarlyBird ? 'true' : 'false' ?>;
                const isLateFee = <?= $isLateFee ? 'true' : 'false' ?>;

                // Cart state
                let cart = [];
                let availableRiders = [];
                let selectedRiderId = null;
                let selectedClassId = null;
                let selectedClassData = null;

                // DOM elements
                const riderSelect = document.getElementById('riderSelect');
                const classSelection = document.getElementById('classSelection');
                const classList = document.getElementById('classList');
                const addToCartBtn = document.getElementById('addToCartBtn');
                const addAnotherBtn = document.getElementById('addAnotherBtn');
                const registrationCart = document.getElementById('registrationCart');
                const cartItems = document.getElementById('cartItems');
                const cartCount = document.getElementById('cartCount');
                const cartTotal = document.getElementById('cartTotal');
                const cartSavings = document.getElementById('cartSavings');
                const savingsAmount = document.getElementById('savingsAmount');
                const checkoutBtn = document.getElementById('checkoutBtn');

                // Load available riders
                async function loadRiders() {
                    try {
                        const response = await fetch('/api/orders.php?action=my_riders');
                        const data = await response.json();
                        if (data.success) {
                            availableRiders = data.riders;
                            updateRiderSelect();
                        }
                    } catch (e) {
                        console.error('Failed to load riders:', e);
                    }
                }

                function updateRiderSelect() {
                    // Clear and rebuild options
                    riderSelect.innerHTML = '<option value="">-- Välj deltagare --</option>';

                    availableRiders.forEach(rider => {
                        // Check if already in cart
                        const inCart = cart.some(item => item.rider_id === rider.id);
                        if (!inCart) {
                            const opt = document.createElement('option');
                            opt.value = rider.id;
                            opt.textContent = rider.firstname + ' ' + rider.lastname +
                                (rider.relation === 'self' ? ' (du själv)' : '');
                            riderSelect.appendChild(opt);
                        }
                    });
                }

                // Load classes for selected rider
                async function loadClasses(riderId) {
                    classList.innerHTML = '<p class="text-muted">Laddar klasser...</p>';
                    classSelection.style.display = 'block';

                    try {
                        const response = await fetch(`/api/orders.php?action=event_classes&event_id=${eventId}&rider_id=${riderId}`);
                        const data = await response.json();

                        if (data.success) {
                            renderClasses(data.classes);
                        } else {
                            classList.innerHTML = '<p class="text-error">Kunde inte ladda klasser</p>';
                        }
                    } catch (e) {
                        console.error('Failed to load classes:', e);
                        classList.innerHTML = '<p class="text-error">Ett fel uppstod</p>';
                    }
                }

                function renderClasses(classes) {
                    classList.innerHTML = '';

                    classes.forEach(cls => {
                        const div = document.createElement('label');
                        div.className = 'reg-class-item' + (!cls.eligible ? ' disabled' : '');
                        div.dataset.classId = cls.class_id;
                        div.dataset.price = cls.current_price;
                        div.dataset.name = cls.name;

                        div.innerHTML = `
                            <input type="radio" name="class_select" value="${cls.class_id}"
                                   class="reg-class-radio" ${!cls.eligible ? 'disabled' : ''}
                                   data-price="${cls.current_price}" data-name="${cls.name}">
                            <div class="reg-class-info">
                                <div class="reg-class-name">${cls.name}</div>
                                ${!cls.eligible ? `<div class="reg-class-desc text-warning">${cls.reason}</div>` : ''}
                            </div>
                            <div class="reg-class-price">
                                <div class="reg-class-price__current">${cls.current_price.toLocaleString('sv-SE')} kr</div>
                                ${cls.price_type === 'early_bird' ? `<div class="reg-class-price__original">${cls.base_price.toLocaleString('sv-SE')} kr</div>` : ''}
                            </div>
                        `;

                        if (cls.eligible) {
                            div.addEventListener('click', () => selectClass(cls));
                        }

                        classList.appendChild(div);
                    });
                }

                function selectClass(cls) {
                    // Update visual selection
                    document.querySelectorAll('.reg-class-item').forEach(item => {
                        item.classList.remove('selected');
                    });
                    event.currentTarget.classList.add('selected');

                    selectedClassId = cls.class_id;
                    selectedClassData = cls;
                    addToCartBtn.disabled = false;
                }

                function addToCart() {
                    if (!selectedRiderId || !selectedClassId) return;

                    const rider = availableRiders.find(r => r.id == selectedRiderId);
                    if (!rider) return;

                    cart.push({
                        type: 'event',
                        rider_id: rider.id,
                        rider_name: rider.firstname + ' ' + rider.lastname,
                        event_id: eventId,
                        class_id: selectedClassId,
                        class_name: selectedClassData.name,
                        price: selectedClassData.current_price
                    });

                    // Reset form
                    selectedRiderId = null;
                    selectedClassId = null;
                    selectedClassData = null;
                    riderSelect.value = '';
                    classSelection.style.display = 'none';
                    addToCartBtn.disabled = true;

                    updateCart();
                    updateRiderSelect();
                }

                function removeFromCart(index) {
                    cart.splice(index, 1);
                    updateCart();
                    updateRiderSelect();
                }

                function updateCart() {
                    if (cart.length === 0) {
                        registrationCart.style.display = 'none';
                        addAnotherBtn.style.display = 'none';
                        return;
                    }

                    registrationCart.style.display = 'block';
                    addAnotherBtn.style.display = 'inline-flex';

                    // Render cart items
                    cartItems.innerHTML = cart.map((item, index) => `
                        <div class="reg-cart__item">
                            <div class="reg-cart__item-info">
                                <strong>${item.rider_name}</strong>
                                <span class="text-muted">${item.class_name}</span>
                            </div>
                            <div class="reg-cart__item-price">${item.price.toLocaleString('sv-SE')} kr</div>
                            <button type="button" class="reg-cart__item-remove" onclick="window.removeCartItem(${index})">
                                <i data-lucide="x"></i>
                            </button>
                        </div>
                    `).join('');

                    // Update totals
                    const total = cart.reduce((sum, item) => sum + item.price, 0);
                    cartCount.textContent = cart.length;
                    cartTotal.textContent = total.toLocaleString('sv-SE') + ' kr';

                    // Show savings if multiple riders
                    if (cart.length > 1) {
                        const savings = (cart.length - 1) * 1; // 1 kr per extra Swish fee saved
                        savingsAmount.textContent = savings + ' kr';
                        cartSavings.style.display = 'flex';
                    } else {
                        cartSavings.style.display = 'none';
                    }

                    if (typeof lucide !== 'undefined') lucide.createIcons();
                }

                // Global function for remove button
                window.removeCartItem = removeFromCart;

                async function checkout() {
                    if (cart.length === 0) return;

                    checkoutBtn.disabled = true;
                    checkoutBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Bearbetar...';
                    if (typeof lucide !== 'undefined') lucide.createIcons();

                    try {
                        const response = await fetch('/api/orders.php', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                action: 'create',
                                buyer: {
                                    name: '<?= h($currentUser['firstname'] . ' ' . $currentUser['lastname']) ?>',
                                    email: '<?= h($currentUser['email'] ?? '') ?>'
                                },
                                items: cart
                            })
                        });

                        const data = await response.json();

                        if (data.success) {
                            window.location.href = data.order.checkout_url;
                        } else {
                            alert(data.error || 'Ett fel uppstod');
                            checkoutBtn.disabled = false;
                            checkoutBtn.innerHTML = '<i data-lucide="credit-card"></i> Gå till betalning';
                            if (typeof lucide !== 'undefined') lucide.createIcons();
                        }
                    } catch (error) {
                        console.error('Checkout error:', error);
                        alert('Ett fel uppstod. Försök igen.');
                        checkoutBtn.disabled = false;
                        checkoutBtn.innerHTML = '<i data-lucide="credit-card"></i> Gå till betalning';
                        if (typeof lucide !== 'undefined') lucide.createIcons();
                    }
                }

                // Event listeners
                riderSelect.addEventListener('change', function() {
                    selectedRiderId = this.value;
                    if (selectedRiderId) {
                        loadClasses(selectedRiderId);
                    } else {
                        classSelection.style.display = 'none';
                    }
                    selectedClassId = null;
                    addToCartBtn.disabled = true;
                });

                addToCartBtn.addEventListener('click', addToCart);
                checkoutBtn.addEventListener('click', checkout);
                addAnotherBtn.addEventListener('click', function() {
                    document.getElementById('addRiderSection').scrollIntoView({ behavior: 'smooth' });
                });

                // Initialize
                loadRiders();
            })();
            </script>
        <?php endif; ?>
    </div>
</section>

<?php elseif ($activeTab === 'elimination'): ?>
<!-- ELIMINATION TAB -->
<section class="card">
    <div class="card-header">
        <h2 class="card-title"><i data-lucide="git-branch"></i> Elimination / Dual Slalom</h2>
    </div>
    <div class="card-body">
        <?php
        // Include the elimination display component
        include INCLUDES_PATH . '/elimination-display.php';
        ?>
    </div>
</section>

<?php endif; ?>

<?php
// Partner sponsors (bottom of page - unlimited)
$partnerSponsorsWithLogos = array_filter($eventSponsors['partner'] ?? [], function($s) {
    return get_sponsor_logo_for_placement($s, 'content') !== null;
});
if (!empty($partnerSponsorsWithLogos)): ?>
<section class="event-partner-sponsors mt-xl mb-lg">
    <div class="partner-sponsors-header">
        <span class="partner-sponsors-label">Samarbetspartners</span>
    </div>
    <div class="partner-sponsors-grid">
        <?php foreach ($partnerSponsorsWithLogos as $sponsor):
            $partnerLogo = get_sponsor_logo_for_placement($sponsor, 'content');
        ?>
        <a href="<?= h($sponsor['website'] ?? '#') ?>" target="_blank" rel="noopener sponsored" class="partner-sponsor-item" title="<?= h($sponsor['name']) ?>">
            <img src="<?= h($partnerLogo) ?>" alt="<?= h($sponsor['name']) ?>">
        </a>
        <?php endforeach; ?>
    </div>
</section>
<?php endif; ?>

<script>
function filterResults() {
    const classFilter = document.getElementById('classFilter')?.value || 'all';
    const searchFilter = (document.getElementById('searchFilter')?.value || '').toLowerCase().trim();
    const totalViewEnabled = document.getElementById('totalViewToggle')?.checked || false;

    // If total view is enabled, only filter within total section
    if (totalViewEnabled) {
        const totalSection = document.getElementById('total-split-section');
        if (totalSection) {
            totalSection.querySelectorAll('.result-row, .result-item').forEach(row => {
                const searchData = row.dataset.search || '';
                const matchesSearch = !searchFilter || searchData.includes(searchFilter);
                row.style.display = matchesSearch ? '' : 'none';
            });
        }
        return;
    }

    document.querySelectorAll('.class-section').forEach(section => {
        const classId = section.dataset.class;
        const showClass = classFilter === 'all' || classFilter === classId;
        section.style.display = showClass ? '' : 'none';

        if (showClass) {
            section.querySelectorAll('.result-row, .result-item').forEach(row => {
                const searchData = row.dataset.search || '';
                const matchesSearch = !searchFilter || searchData.includes(searchFilter);
                row.style.display = matchesSearch ? '' : 'none';
            });
        }
    });
}

function toggleSplitColors(enabled) {
    // Toggle colors for split times (Enduro) and DH run times
    document.querySelectorAll('.col-split, .col-dh-run').forEach(cell => {
        if (enabled) {
            cell.classList.remove('no-color');
        } else {
            cell.classList.add('no-color');
        }
    });
}

function toggleTotalView(enabled) {
    const classSections = document.querySelectorAll('.class-section');
    const totalSection = document.getElementById('total-split-section');
    const classFilter = document.getElementById('classFilter');

    if (enabled) {
        // Hide class sections, show total section
        classSections.forEach(section => section.classList.add('hidden'));
        if (totalSection) totalSection.classList.remove('hidden');
        // Disable class filter when in total view
        if (classFilter) {
            classFilter.disabled = true;
            classFilter.style.opacity = '0.5';
        }
    } else {
        // Show class sections, hide total section
        classSections.forEach(section => section.classList.remove('hidden'));
        if (totalSection) totalSection.classList.add('hidden');
        // Re-enable class filter
        if (classFilter) {
            classFilter.disabled = false;
            classFilter.style.opacity = '1';
        }
        // Re-apply filters
        filterResults();
    }
}

// Sort class section by split time
function sortBySplit(headerEl, classKey, splitNum) {
    const section = document.getElementById('class-' + classKey);
    if (!section) return;

    const table = section.querySelector('.results-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr.result-row'));

    // Get the column index for this split
    const headers = table.querySelectorAll('thead th');
    let colIndex = -1;
    headers.forEach((th, idx) => {
        if (th.dataset.sort === 'ss' + splitNum) {
            colIndex = idx;
        }
    });

    if (colIndex === -1) return;

    // Determine sort direction
    const isAscending = !headerEl.classList.contains('sort-asc');

    // Remove sort classes from all headers in this table
    table.querySelectorAll('.sortable-header').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to clicked header
    headerEl.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aCell = a.cells[colIndex];
        const bCell = b.cells[colIndex];
        const aVal = parseFloat(aCell?.dataset.sortValue) || Infinity;
        const bVal = parseFloat(bCell?.dataset.sortValue) || Infinity;

        return isAscending ? aVal - bVal : bVal - aVal;
    });

    // Update position numbers and re-append rows
    rows.forEach((row, idx) => {
        const posCell = row.querySelector('.col-place');
        if (posCell && !posCell.querySelector('.status-badge') && !posCell.querySelector('.medal-icon') && posCell.textContent.trim() !== '✓') {
            // Only update numeric positions, not medals/status badges
            const pos = posCell.textContent.trim();
            if (!isNaN(parseInt(pos))) {
                // Keep original position, don't change
            }
        }
        tbody.appendChild(row);
    });
}

// Sort DH class section by run time
function sortDHByRun(headerEl, classKey, runNum) {
    const section = document.getElementById('class-' + classKey);
    if (!section) return;

    const table = section.querySelector('.results-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr.result-row'));

    // Get the column index for this run
    const headers = table.querySelectorAll('thead th');
    let colIndex = -1;
    headers.forEach((th, idx) => {
        if (th.dataset.sort === 'run' + runNum) {
            colIndex = idx;
        }
    });

    if (colIndex === -1) return;

    // Determine sort direction
    const isAscending = !headerEl.classList.contains('sort-asc');

    // Remove sort classes from all headers in this table
    table.querySelectorAll('.sortable-header').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to clicked header
    headerEl.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aCell = a.cells[colIndex];
        const bCell = b.cells[colIndex];
        const aVal = parseFloat(aCell?.dataset.sortValue) || Infinity;
        const bVal = parseFloat(bCell?.dataset.sortValue) || Infinity;

        return isAscending ? aVal - bVal : bVal - aVal;
    });

    // Re-append rows
    rows.forEach((row) => {
        tbody.appendChild(row);
    });
}

// Sort class section by time (Bästa/Tid column)
function sortByTime(headerEl, classKey) {
    const section = document.getElementById('class-' + classKey);
    if (!section) return;

    const table = section.querySelector('.results-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr.result-row'));

    // Get the column index for time/best column
    const headers = table.querySelectorAll('thead th');
    let colIndex = -1;
    headers.forEach((th, idx) => {
        if (th.dataset.sort === 'time' || th.dataset.sort === 'best') {
            colIndex = idx;
        }
    });

    if (colIndex === -1) return;

    // Determine sort direction
    const isAscending = !headerEl.classList.contains('sort-asc');

    // Remove sort classes from all headers in this table
    table.querySelectorAll('.sortable-header').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to clicked header
    headerEl.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aCell = a.cells[colIndex];
        const bCell = b.cells[colIndex];
        const aVal = parseFloat(aCell?.dataset.sortValue) || Infinity;
        const bVal = parseFloat(bCell?.dataset.sortValue) || Infinity;

        return isAscending ? aVal - bVal : bVal - aVal;
    });

    // Re-append rows
    rows.forEach((row) => {
        tbody.appendChild(row);
    });
}

// Sort total section by split time
function sortTotalBySplit(headerEl, splitNum) {
    const table = document.getElementById('total-split-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr.result-row'));

    // Get the column index for this split
    const headers = table.querySelectorAll('thead th');
    let colIndex = -1;
    headers.forEach((th, idx) => {
        if (th.dataset.sort === 'ss' + splitNum) {
            colIndex = idx;
        }
    });

    if (colIndex === -1) return;

    // Determine sort direction
    const isAscending = !headerEl.classList.contains('sort-asc');

    // Remove sort classes from all headers
    table.querySelectorAll('.sortable-header').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to clicked header
    headerEl.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aCell = a.cells[colIndex];
        const bCell = b.cells[colIndex];
        const aVal = parseFloat(aCell?.dataset.sortValue) || Infinity;
        const bVal = parseFloat(bCell?.dataset.sortValue) || Infinity;

        return isAscending ? aVal - bVal : bVal - aVal;
    });

    // Update position numbers and re-append rows
    rows.forEach((row, idx) => {
        const posCell = row.querySelector('.total-position');
        if (posCell) {
            posCell.textContent = idx + 1;
        }
        tbody.appendChild(row);
    });
}

// Toggle DH Total view (Åktider Total)
function toggleDHTotalView(enabled) {
    const classSections = document.querySelectorAll('.class-section');
    const totalSection = document.getElementById('total-dh-section');
    const classFilter = document.getElementById('classFilter');

    if (enabled) {
        // Hide class sections, show DH total section
        classSections.forEach(section => section.classList.add('hidden'));
        if (totalSection) totalSection.classList.remove('hidden');
        // Disable class filter when in total view
        if (classFilter) {
            classFilter.disabled = true;
            classFilter.style.opacity = '0.5';
        }
    } else {
        // Show class sections, hide DH total section
        classSections.forEach(section => section.classList.remove('hidden'));
        if (totalSection) totalSection.classList.add('hidden');
        // Re-enable class filter
        if (classFilter) {
            classFilter.disabled = false;
            classFilter.style.opacity = '1';
        }
        // Re-apply filters
        filterResults();
    }
}

// Sort DH total section by run time
function sortDHTotalByRun(headerEl, runNum) {
    const table = document.getElementById('total-dh-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr.result-row'));

    // Get the column index for this run
    const headers = table.querySelectorAll('thead th');
    let colIndex = -1;
    headers.forEach((th, idx) => {
        if (th.dataset.sort === 'run' + runNum) {
            colIndex = idx;
        }
    });

    if (colIndex === -1) return;

    // Determine sort direction
    const isAscending = !headerEl.classList.contains('sort-asc');

    // Remove sort classes from all headers
    table.querySelectorAll('.sortable-header').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to clicked header
    headerEl.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aCell = a.cells[colIndex];
        const bCell = b.cells[colIndex];
        const aVal = parseFloat(aCell?.dataset.sortValue) || Infinity;
        const bVal = parseFloat(bCell?.dataset.sortValue) || Infinity;

        return isAscending ? aVal - bVal : bVal - aVal;
    });

    // Update position numbers and re-append rows
    rows.forEach((row, idx) => {
        const posCell = row.querySelector('.total-position');
        if (posCell) {
            posCell.textContent = idx + 1;
        }
        tbody.appendChild(row);
    });
}

</script>

<style>
/* Series branding colors - dynamic per event */
:root {
    --series-gradient-start: <?= htmlspecialchars($event['series_gradient_start'] ?? '#004A98') ?>;
    --series-gradient-end: <?= htmlspecialchars($event['series_gradient_end'] ?? '#002a5c') ?>;
}
</style>
