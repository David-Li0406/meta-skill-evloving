<?php
/**
 * Admin Elimination Manage - Hantera kvalificering och brackets för ett event
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

$eventId = isset($_GET['event_id']) ? intval($_GET['event_id']) : 0;
if (!$eventId) {
    header('Location: /admin/elimination.php');
    exit;
}

// Get event info
$event = $db->getRow("SELECT e.*, s.name as series_name FROM events e LEFT JOIN series s ON e.series_id = s.id WHERE e.id = ?", [$eventId]);
if (!$event) {
    $_SESSION['error'] = 'Event hittades inte';
    header('Location: /admin/elimination.php');
    exit;
}

// Get classes that have elimination qualifying data for this event
$classes = $db->getAll("
    SELECT DISTINCT c.id, c.name, c.display_name, COUNT(eq.id) as rider_count
    FROM classes c
    INNER JOIN elimination_qualifying eq ON eq.class_id = c.id AND eq.event_id = ?
    WHERE c.active = 1
    GROUP BY c.id, c.name, c.display_name
    ORDER BY c.sort_order, c.name
", [$eventId]);

// If no classes with qualifying data, show all active classes as fallback
if (empty($classes)) {
    $classes = $db->getAll("
        SELECT DISTINCT c.id, c.name, c.display_name, 0 as rider_count
        FROM classes c
        WHERE c.active = 1
        ORDER BY c.sort_order, c.name
    ");
}

$selectedClassId = isset($_GET['class_id']) ? intval($_GET['class_id']) : ($classes[0]['id'] ?? 0);

// Check if elimination tables exist
$tablesExist = true;
try {
    $pdo->query("SELECT 1 FROM elimination_qualifying LIMIT 1");
} catch (Exception $e) {
    $tablesExist = false;
}

// Get qualifying results for selected class (for backwards compat)
$qualifyingResults = [];
$brackets = [];
$finalResults = [];

// Get ALL qualifying results grouped by class
$allQualifyingByClass = [];
$allBracketsByClass = [];
$allFinalResultsByClass = [];

if ($tablesExist) {
    // Get all qualifying results for ALL classes
    $allQualRaw = $db->getAll("
        SELECT eq.*, r.firstname, r.lastname, cl.name as club_name, c.display_name as class_display_name, c.name as class_name
        FROM elimination_qualifying eq
        JOIN riders r ON eq.rider_id = r.id
        LEFT JOIN clubs cl ON r.club_id = cl.id
        JOIN classes c ON eq.class_id = c.id
        WHERE eq.event_id = ?
        ORDER BY c.sort_order, c.name, eq.seed_position ASC, eq.best_time ASC
    ", [$eventId]);

    foreach ($allQualRaw as $q) {
        $allQualifyingByClass[$q['class_id']]['name'] = $q['class_display_name'] ?? $q['class_name'];
        $allQualifyingByClass[$q['class_id']]['results'][] = $q;
    }

    // Get all brackets for ALL classes
    $allBracketsRaw = $db->getAll("
        SELECT eb.*, c.display_name as class_display_name, c.name as class_name,
            r1.firstname as rider1_firstname, r1.lastname as rider1_lastname,
            r2.firstname as rider2_firstname, r2.lastname as rider2_lastname,
            w.firstname as winner_firstname, w.lastname as winner_lastname
        FROM elimination_brackets eb
        LEFT JOIN riders r1 ON eb.rider_1_id = r1.id
        LEFT JOIN riders r2 ON eb.rider_2_id = r2.id
        LEFT JOIN riders w ON eb.winner_id = w.id
        JOIN classes c ON eb.class_id = c.id
        WHERE eb.event_id = ?
        ORDER BY c.sort_order, c.name, eb.round_number ASC, eb.heat_number ASC
    ", [$eventId]);

    foreach ($allBracketsRaw as $b) {
        $allBracketsByClass[$b['class_id']]['name'] = $b['class_display_name'] ?? $b['class_name'];
        $allBracketsByClass[$b['class_id']]['rounds'][$b['round_name']][] = $b;
    }

    // Get all final results for ALL classes
    $allFinalRaw = $db->getAll("
        SELECT er.*, r.firstname, r.lastname, cl.name as club_name, c.display_name as class_display_name, c.name as class_name
        FROM elimination_results er
        JOIN riders r ON er.rider_id = r.id
        LEFT JOIN clubs cl ON r.club_id = cl.id
        JOIN classes c ON er.class_id = c.id
        WHERE er.event_id = ?
        ORDER BY c.sort_order, c.name, er.final_position ASC
    ", [$eventId]);

    foreach ($allFinalRaw as $f) {
        $allFinalResultsByClass[$f['class_id']]['name'] = $f['class_display_name'] ?? $f['class_name'];
        $allFinalResultsByClass[$f['class_id']]['results'][] = $f;
    }

    // Also keep selected class data for backwards compat
    if ($selectedClassId && isset($allQualifyingByClass[$selectedClassId])) {
        $qualifyingResults = $allQualifyingByClass[$selectedClassId]['results'] ?? [];
    }
    if ($selectedClassId && isset($allBracketsByClass[$selectedClassId])) {
        $brackets = $allBracketsByClass[$selectedClassId]['rounds'] ?? [];
    }
    if ($selectedClassId && isset($allFinalResultsByClass[$selectedClassId])) {
        $finalResults = $allFinalResultsByClass[$selectedClassId]['results'] ?? [];
    }

    // AUTO-REPAIR: Check for missing bronze matches and create them
    // This fixes events created before the bronze match logic was added
    $repairCount = 0;
    foreach ($classes as $classInfo) {
        $cid = $classInfo['id'];

        // Check if both semifinals are complete but no bronze match exists
        $semiFinals = $db->getAll("
            SELECT * FROM elimination_brackets
            WHERE event_id = ? AND class_id = ? AND round_name = 'semifinal'
            AND loser_id IS NOT NULL
            ORDER BY heat_number ASC
        ", [$eventId, $cid]);

        if (count($semiFinals) >= 2) {
            // Check if bronze match already exists
            $bronzeExists = $db->getRow("
                SELECT id FROM elimination_brackets
                WHERE event_id = ? AND class_id = ? AND round_name = 'third_place'
            ", [$eventId, $cid]);

            if (!$bronzeExists) {
                // Create bronze match with both semifinal losers
                $loser1 = $semiFinals[0];
                $loser2 = $semiFinals[1];

                $loser1Seed = ($loser1['loser_id'] == $loser1['rider_1_id']) ? $loser1['rider_1_seed'] : $loser1['rider_2_seed'];
                $loser2Seed = ($loser2['loser_id'] == $loser2['rider_1_id']) ? $loser2['rider_1_seed'] : $loser2['rider_2_seed'];

                $stmt = $pdo->prepare("
                    INSERT INTO elimination_brackets
                    (event_id, class_id, bracket_type, round_name, round_number, heat_number,
                     rider_1_id, rider_2_id, rider_1_seed, rider_2_seed, status, bracket_position)
                    VALUES (?, ?, 'main', 'third_place', 5, 1, ?, ?, ?, ?, 'pending', 1)
                ");
                $stmt->execute([
                    $eventId, $cid,
                    $loser1['loser_id'], $loser2['loser_id'],
                    $loser1Seed, $loser2Seed
                ]);
                $repairCount++;

                // Also update the allBracketsByClass data so UI shows the new bronze match
                $allBracketsByClass[$cid]['rounds']['third_place'][] = [
                    'id' => $pdo->lastInsertId(),
                    'event_id' => $eventId,
                    'class_id' => $cid,
                    'class_display_name' => $classInfo['display_name'] ?? $classInfo['name'],
                    'class_name' => $classInfo['name'],
                    'bracket_type' => 'main',
                    'round_name' => 'third_place',
                    'round_number' => 5,
                    'heat_number' => 1,
                    'rider_1_id' => $loser1['loser_id'],
                    'rider_2_id' => $loser2['loser_id'],
                    'rider_1_seed' => $loser1Seed,
                    'rider_2_seed' => $loser2Seed,
                    'rider1_firstname' => null, // Will be fetched separately if needed
                    'rider1_lastname' => null,
                    'rider2_firstname' => null,
                    'rider2_lastname' => null,
                    'status' => 'pending',
                    'winner_id' => null,
                    'loser_id' => null,
                    'bracket_position' => 1
                ];
            }
        }
    }

    if ($repairCount > 0) {
        $_SESSION['success'] = "Automatisk reparation: Skapade $repairCount bronsmatch(er) som saknades.";
    }
}

/**
 * Generate all subsequent rounds for an elimination bracket
 * Automatically advances BYE winners to next round
 * Also creates bronze match (3rd/4th place) after semifinals
 */
function generateNextRounds($pdo, $eventId, $classId) {
    $roundOrder = ['round_of_32', 'round_of_16', 'quarterfinal', 'semifinal', 'final'];
    $roundNames = [
        'round_of_32' => 'round_of_16',
        'round_of_16' => 'quarterfinal',
        'quarterfinal' => 'semifinal',
        'semifinal' => 'final'
    ];

    // Process each round in order
    foreach ($roundOrder as $roundIdx => $currentRound) {
        // Get heats from current round
        $stmt = $pdo->prepare("
            SELECT * FROM elimination_brackets
            WHERE event_id = ? AND class_id = ? AND round_name = ?
            ORDER BY heat_number ASC
        ");
        $stmt->execute([$eventId, $classId, $currentRound]);
        $currentHeats = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($currentHeats)) continue;

        $nextRound = $roundNames[$currentRound] ?? null;
        if (!$nextRound) continue; // Final has no next round

        $nextRoundNumber = $roundIdx + 2;

        // Check if next round already exists
        $checkStmt = $pdo->prepare("SELECT COUNT(*) FROM elimination_brackets WHERE event_id = ? AND class_id = ? AND round_name = ?");
        $checkStmt->execute([$eventId, $classId, $nextRound]);
        if ($checkStmt->fetchColumn() > 0) continue; // Already created

        // Collect winners from current round (including BYEs)
        $winners = [];
        foreach ($currentHeats as $heat) {
            if ($heat['winner_id']) {
                $seed = ($heat['winner_id'] == $heat['rider_1_id'])
                    ? $heat['rider_1_seed']
                    : $heat['rider_2_seed'];
                $winners[] = [
                    'rider_id' => $heat['winner_id'],
                    'seed' => $seed
                ];
            }
        }

        // Create next round heats
        $nextHeatNum = 1;
        for ($i = 0; $i < count($winners); $i += 2) {
            $rider1 = $winners[$i] ?? null;
            $rider2 = $winners[$i + 1] ?? null;

            $status = ($rider1 && $rider2) ? 'pending' : 'bye';
            $winnerId = null;

            if ($status === 'bye' && $rider1) {
                $winnerId = $rider1['rider_id'];
            }

            $stmt = $pdo->prepare("
                INSERT INTO elimination_brackets
                (event_id, class_id, bracket_type, round_name, round_number, heat_number,
                 rider_1_id, rider_2_id, rider_1_seed, rider_2_seed, winner_id, status, bracket_position)
                VALUES (?, ?, 'main', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ");
            $stmt->execute([
                $eventId, $classId, $nextRound, $nextRoundNumber, $nextHeatNum,
                $rider1 ? $rider1['rider_id'] : null,
                $rider2 ? $rider2['rider_id'] : null,
                $rider1 ? $rider1['seed'] : null,
                $rider2 ? $rider2['seed'] : null,
                $winnerId, $status, $nextHeatNum
            ]);
            $nextHeatNum++;
        }

        // After creating the final, also create the bronze match (3rd/4th place)
        if ($currentRound === 'semifinal' && count($currentHeats) >= 2) {
            // Check if bronze match already exists
            $bronzeCheck = $pdo->prepare("SELECT COUNT(*) FROM elimination_brackets WHERE event_id = ? AND class_id = ? AND round_name = 'third_place'");
            $bronzeCheck->execute([$eventId, $classId]);
            if ($bronzeCheck->fetchColumn() == 0) {
                // Collect losers from semifinals for bronze match
                $losers = [];
                foreach ($currentHeats as $heat) {
                    if ($heat['loser_id']) {
                        $seed = ($heat['loser_id'] == $heat['rider_1_id'])
                            ? $heat['rider_1_seed']
                            : $heat['rider_2_seed'];
                        $losers[] = [
                            'rider_id' => $heat['loser_id'],
                            'seed' => $seed
                        ];
                    }
                }

                // Create bronze match if we have 2 losers
                if (count($losers) >= 2) {
                    $stmt = $pdo->prepare("
                        INSERT INTO elimination_brackets
                        (event_id, class_id, bracket_type, round_name, round_number, heat_number,
                         rider_1_id, rider_2_id, rider_1_seed, rider_2_seed, status, bracket_position)
                        VALUES (?, ?, 'main', 'third_place', ?, 1, ?, ?, ?, ?, 'pending', 1)
                    ");
                    $stmt->execute([
                        $eventId, $classId, $nextRoundNumber,
                        $losers[0]['rider_id'], $losers[1]['rider_id'],
                        $losers[0]['seed'], $losers[1]['seed']
                    ]);
                }
            }
        }
    }
}

/**
 * Generate final results when both final and bronze matches are complete
 */
function generateFinalResults($pdo, $db, $eventId, $classId) {
    // Check if final and bronze matches are both completed
    $final = $db->getRow("
        SELECT * FROM elimination_brackets
        WHERE event_id = ? AND class_id = ? AND round_name = 'final' AND status = 'completed'
    ", [$eventId, $classId]);

    $bronze = $db->getRow("
        SELECT * FROM elimination_brackets
        WHERE event_id = ? AND class_id = ? AND round_name = 'third_place' AND status = 'completed'
    ", [$eventId, $classId]);

    if (!$final) return; // Final not completed yet

    // Clear existing results for this class
    $pdo->prepare("DELETE FROM elimination_results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

    // 1st place - final winner
    if ($final['winner_id']) {
        $pdo->prepare("
            INSERT INTO elimination_results (event_id, class_id, rider_id, final_position, qualifying_position, bracket_type)
            SELECT ?, ?, ?, 1, eq.seed_position, 'main'
            FROM elimination_qualifying eq
            WHERE eq.event_id = ? AND eq.class_id = ? AND eq.rider_id = ?
        ")->execute([$eventId, $classId, $final['winner_id'], $eventId, $classId, $final['winner_id']]);
    }

    // 2nd place - final loser
    if ($final['loser_id']) {
        $pdo->prepare("
            INSERT INTO elimination_results (event_id, class_id, rider_id, final_position, qualifying_position, bracket_type)
            SELECT ?, ?, ?, 2, eq.seed_position, 'main'
            FROM elimination_qualifying eq
            WHERE eq.event_id = ? AND eq.class_id = ? AND eq.rider_id = ?
        ")->execute([$eventId, $classId, $final['loser_id'], $eventId, $classId, $final['loser_id']]);
    }

    // 3rd and 4th place from bronze match
    if ($bronze) {
        if ($bronze['winner_id']) {
            $pdo->prepare("
                INSERT INTO elimination_results (event_id, class_id, rider_id, final_position, qualifying_position, bracket_type)
                SELECT ?, ?, ?, 3, eq.seed_position, 'main'
                FROM elimination_qualifying eq
                WHERE eq.event_id = ? AND eq.class_id = ? AND eq.rider_id = ?
            ")->execute([$eventId, $classId, $bronze['winner_id'], $eventId, $classId, $bronze['winner_id']]);
        }
        if ($bronze['loser_id']) {
            $pdo->prepare("
                INSERT INTO elimination_results (event_id, class_id, rider_id, final_position, qualifying_position, bracket_type)
                SELECT ?, ?, ?, 4, eq.seed_position, 'main'
                FROM elimination_qualifying eq
                WHERE eq.event_id = ? AND eq.class_id = ? AND eq.rider_id = ?
            ")->execute([$eventId, $classId, $bronze['loser_id'], $eventId, $classId, $bronze['loser_id']]);
        }
    }

    // Add remaining riders based on elimination round
    $eliminatedRiders = $db->getAll("
        SELECT eb.loser_id, eb.round_name, eq.seed_position
        FROM elimination_brackets eb
        JOIN elimination_qualifying eq ON eq.rider_id = eb.loser_id AND eq.event_id = eb.event_id AND eq.class_id = eb.class_id
        WHERE eb.event_id = ? AND eb.class_id = ?
        AND eb.round_name NOT IN ('final', 'third_place')
        AND eb.loser_id IS NOT NULL
        ORDER BY
            CASE eb.round_name
                WHEN 'semifinal' THEN 1
                WHEN 'quarterfinal' THEN 2
                WHEN 'round_of_16' THEN 3
                WHEN 'round_of_32' THEN 4
            END,
            eq.seed_position ASC
    ", [$eventId, $classId]);

    $position = 5;
    foreach ($eliminatedRiders as $rider) {
        // Skip if already in results (semifinal losers are in bronze)
        if ($rider['round_name'] === 'semifinal') continue;

        $pdo->prepare("
            INSERT INTO elimination_results (event_id, class_id, rider_id, final_position, qualifying_position, eliminated_in_round, bracket_type)
            VALUES (?, ?, ?, ?, ?, ?, 'main')
            ON DUPLICATE KEY UPDATE final_position = VALUES(final_position)
        ")->execute([$eventId, $classId, $rider['loser_id'], $position, $rider['seed_position'], $rider['round_name']]);
        $position++;
    }

    // Sync final results to main results table for series points
    syncEliminationResultsToMainTable($pdo, $db, $eventId, $classId);
}

/**
 * Sync elimination results to main results table
 * Uses series_class_id if set, otherwise uses the elimination class_id
 */
function syncEliminationResultsToMainTable($pdo, $db, $eventId, $classId) {
    // Get all elimination results with their series class mapping
    $eliminationResults = $db->getAll("
        SELECT er.rider_id, er.final_position, eq.series_class_id, eq.best_time, eq.bib_number
        FROM elimination_results er
        JOIN elimination_qualifying eq ON eq.event_id = er.event_id AND eq.rider_id = er.rider_id
        WHERE er.event_id = ? AND er.class_id = ?
        ORDER BY er.final_position ASC
    ", [$eventId, $classId]);

    foreach ($eliminationResults as $result) {
        // Use series_class_id if set, otherwise use the elimination class_id
        $targetClass = $result['series_class_id'] ?: $classId;

        // Delete any old results for this rider in different classes (class change cleanup)
        $pdo->prepare("DELETE FROM results WHERE event_id = ? AND cyclist_id = ? AND class_id != ?")->execute([
            $eventId, $result['rider_id'], $targetClass
        ]);

        // Insert/update result with final bracket position
        $pdo->prepare("
            INSERT INTO results (event_id, class_id, cyclist_id, position, finish_time, bib_number, status)
            VALUES (?, ?, ?, ?, ?, ?, 'finished')
            ON DUPLICATE KEY UPDATE
            position = VALUES(position),
            finish_time = VALUES(finish_time)
        ")->execute([
            $eventId,
            $targetClass,
            $result['rider_id'],
            $result['final_position'],
            $result['best_time'],
            $result['bib_number']
        ]);
    }
}

/**
 * Advance a winner to the next round
 * Places winner in the correct slot based on their heat number
 */
function advanceWinnerToNextRound($pdo, $db, $eventId, $completedHeat) {
    $roundNames = [
        'round_of_32' => 'round_of_16',
        'round_of_16' => 'quarterfinal',
        'quarterfinal' => 'semifinal',
        'semifinal' => 'final'
    ];

    $currentRound = $completedHeat['round_name'];
    $nextRound = $roundNames[$currentRound] ?? null;

    if (!$nextRound || !$completedHeat['winner_id']) {
        return; // No next round or no winner
    }

    // Calculate which heat and slot in next round
    // Heat 1,2 -> next heat 1; Heat 3,4 -> next heat 2; etc.
    $currentHeat = $completedHeat['heat_number'];
    $nextHeatNum = ceil($currentHeat / 2);
    $isFirstSlot = ($currentHeat % 2) === 1; // Odd heats go to rider_1, even to rider_2

    // Get the winner's seed
    $winnerSeed = ($completedHeat['winner_id'] == $completedHeat['rider_1_id'])
        ? $completedHeat['rider_1_seed']
        : $completedHeat['rider_2_seed'];

    // Check if next round heat exists
    $nextHeat = $db->getRow("
        SELECT * FROM elimination_brackets
        WHERE event_id = ? AND class_id = ? AND round_name = ? AND heat_number = ?
    ", [$eventId, $completedHeat['class_id'], $nextRound, $nextHeatNum]);

    if ($nextHeat) {
        // Update existing heat
        if ($isFirstSlot) {
            $stmt = $pdo->prepare("UPDATE elimination_brackets SET rider_1_id = ?, rider_1_seed = ? WHERE id = ?");
            $stmt->execute([$completedHeat['winner_id'], $winnerSeed, $nextHeat['id']]);
        } else {
            $stmt = $pdo->prepare("UPDATE elimination_brackets SET rider_2_id = ?, rider_2_seed = ? WHERE id = ?");
            $stmt->execute([$completedHeat['winner_id'], $winnerSeed, $nextHeat['id']]);
        }

        // Check if both riders are now assigned - if so and one of them is null, it's a BYE
        $updatedHeat = $db->getRow("SELECT * FROM elimination_brackets WHERE id = ?", [$nextHeat['id']]);
        if ($updatedHeat['rider_1_id'] && !$updatedHeat['rider_2_id']) {
            $stmt = $pdo->prepare("UPDATE elimination_brackets SET status = 'bye', winner_id = ? WHERE id = ?");
            $stmt->execute([$updatedHeat['rider_1_id'], $nextHeat['id']]);
        } elseif (!$updatedHeat['rider_1_id'] && $updatedHeat['rider_2_id']) {
            $stmt = $pdo->prepare("UPDATE elimination_brackets SET status = 'bye', winner_id = ? WHERE id = ?");
            $stmt->execute([$updatedHeat['rider_2_id'], $nextHeat['id']]);
        }
    } else {
        // Create new heat in next round
        $roundNumbers = ['round_of_16' => 2, 'quarterfinal' => 3, 'semifinal' => 4, 'final' => 5];
        $roundNum = $roundNumbers[$nextRound] ?? 2;

        $stmt = $pdo->prepare("
            INSERT INTO elimination_brackets
            (event_id, class_id, bracket_type, round_name, round_number, heat_number,
             rider_1_id, rider_2_id, rider_1_seed, rider_2_seed, status, bracket_position)
            VALUES (?, ?, 'main', ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        ");

        if ($isFirstSlot) {
            $stmt->execute([
                $eventId, $completedHeat['class_id'], $nextRound, $roundNum, $nextHeatNum,
                $completedHeat['winner_id'], null, $winnerSeed, null, $nextHeatNum
            ]);
        } else {
            $stmt->execute([
                $eventId, $completedHeat['class_id'], $nextRound, $roundNum, $nextHeatNum,
                null, $completedHeat['winner_id'], null, $winnerSeed, $nextHeatNum
            ]);
        }
    }

    // If this was a semifinal, check if we should create the bronze match
    if ($currentRound === 'semifinal' && $completedHeat['loser_id']) {
        // Check if bronze match already exists
        $bronzeExists = $db->getRow("
            SELECT id FROM elimination_brackets
            WHERE event_id = ? AND class_id = ? AND round_name = 'third_place'
        ", [$eventId, $completedHeat['class_id']]);

        if (!$bronzeExists) {
            // Check if both semifinals are completed (have losers)
            $semiFinals = $db->getAll("
                SELECT * FROM elimination_brackets
                WHERE event_id = ? AND class_id = ? AND round_name = 'semifinal'
                AND loser_id IS NOT NULL
                ORDER BY heat_number ASC
            ", [$eventId, $completedHeat['class_id']]);

            if (count($semiFinals) >= 2) {
                // Create bronze match with both semifinal losers
                $loser1 = $semiFinals[0];
                $loser2 = $semiFinals[1];

                $loser1Seed = ($loser1['loser_id'] == $loser1['rider_1_id']) ? $loser1['rider_1_seed'] : $loser1['rider_2_seed'];
                $loser2Seed = ($loser2['loser_id'] == $loser2['rider_1_id']) ? $loser2['rider_1_seed'] : $loser2['rider_2_seed'];

                $stmt = $pdo->prepare("
                    INSERT INTO elimination_brackets
                    (event_id, class_id, bracket_type, round_name, round_number, heat_number,
                     rider_1_id, rider_2_id, rider_1_seed, rider_2_seed, status, bracket_position)
                    VALUES (?, ?, 'main', 'third_place', 5, 1, ?, ?, ?, ?, 'pending', 1)
                ");
                $stmt->execute([
                    $eventId, $completedHeat['class_id'],
                    $loser1['loser_id'], $loser2['loser_id'],
                    $loser1Seed, $loser2Seed
                ]);
            }
        }
    }
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'import_qualifying') {
        // Handle CSV import of qualifying results
        // TODO: Implement CSV import
    }

    if ($action === 'generate_brackets') {
        // Generate brackets for ALL classes with qualifying data
        try {
            // Get all classes with qualifying data for this event
            $allClasses = $db->getAll("
                SELECT DISTINCT class_id FROM elimination_qualifying
                WHERE event_id = ? AND status = 'finished'
            ", [$eventId]);

            $generatedCount = 0;
            $totalRiders = 0;
            $classResults = [];

            foreach ($allClasses as $classRow) {
                $classId = $classRow['class_id'];

                // Get ALL qualifiers with finished status for this class
                $qualifiers = $db->getAll("
                    SELECT * FROM elimination_qualifying
                    WHERE event_id = ? AND class_id = ? AND status = 'finished'
                    ORDER BY best_time ASC
                ", [$eventId, $classId]);

                $numQualifiers = count($qualifiers);

                if ($numQualifiers >= 2) {
                    // Auto-determine bracket size: smallest power of 2 >= numQualifiers
                    if ($numQualifiers <= 4) {
                        $bracketSize = 4;
                    } elseif ($numQualifiers <= 8) {
                        $bracketSize = 8;
                    } elseif ($numQualifiers <= 16) {
                        $bracketSize = 16;
                    } else {
                        $bracketSize = 32;
                    }

                    // Clear existing brackets for this class
                    $pdo->prepare("DELETE FROM elimination_brackets WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);
                    $pdo->prepare("DELETE FROM elimination_results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                    // Update seed positions
                    $seedPos = 1;
                    foreach ($qualifiers as $q) {
                        $pdo->prepare("UPDATE elimination_qualifying SET seed_position = ?, advances_to_bracket = 1 WHERE id = ?")
                            ->execute([$seedPos, $q['id']]);
                        $seedPos++;
                    }

                    // Standard bracket seeding - ORDER IS CRITICAL!
                    // Heats 1,2 -> next round Heat 1; Heats 3,4 -> next round Heat 2; etc.
                    // This ensures proper advancement through the bracket
                    if ($bracketSize == 4) {
                        // Semifinal: Heat 1,2 -> Final
                        $seedPairs = [[1,4], [2,3]];
                        $roundName = 'semifinal';
                        $roundNumber = 1;
                    } elseif ($bracketSize == 8) {
                        // Quarterfinal: Seed 2 i Heat 4 (längst ner visuellt)
                        // Heat 1,2 → SF1; Heat 3,4 → SF2
                        $seedPairs = [[1,8], [4,5], [3,6], [2,7]];
                        $roundName = 'quarterfinal';
                        $roundNumber = 1;
                    } elseif ($bracketSize == 16) {
                        // Round of 16: Korrekt seeding för att 1 vs 2 möts i final
                        // ÖVRE HALVAN (Semifinal 1):
                        // Heat 1,2 -> Kvartsfinal 1; Heat 3,4 -> Kvartsfinal 2
                        // NEDRE HALVAN (Semifinal 2):
                        // Heat 5,6 -> Kvartsfinal 3; Heat 7,8 -> Kvartsfinal 4
                        $seedPairs = [
                            [1,16], [8,9],   // Heat 1,2 -> Kvartsfinal 1
                            [5,12], [4,13],  // Heat 3,4 -> Kvartsfinal 2
                            [3,14], [6,11],  // Heat 5,6 -> Kvartsfinal 3
                            [7,10], [2,15]   // Heat 7,8 -> Kvartsfinal 4
                        ];
                        $roundName = 'round_of_16';
                        $roundNumber = 1;
                    } else {
                        // Round of 32: Korrekt seeding för att 1 vs 2 möts i final
                        // ÖVRE HALVAN (Semifinal 1):
                        // R32 Heats 1-4 → R16 Heats 1,2 → Kvartsfinal 1
                        // R32 Heats 5-8 → R16 Heats 3,4 → Kvartsfinal 2
                        // NEDRE HALVAN (Semifinal 2):
                        // R32 Heats 9-12 → R16 Heats 5,6 → Kvartsfinal 3
                        // R32 Heats 13-16 → R16 Heats 7,8 → Kvartsfinal 4
                        $seedPairs = [
                            // ÖVRE HALVAN (SF1):
                            [1,32], [16,17], [8,25], [9,24],   // R32 H1-4 → R16 H1,2 → QF1
                            [5,28], [12,21], [4,29], [13,20],  // R32 H5-8 → R16 H3,4 → QF2
                            // NEDRE HALVAN (SF2):
                            [3,30], [14,19], [6,27], [11,22],  // R32 H9-12 → R16 H5,6 → QF3
                            [7,26], [10,23], [2,31], [15,18]   // R32 H13-16 → R16 H7,8 → QF4
                        ];
                        $roundName = 'round_of_32';
                        $roundNumber = 1;
                    }

                    $heatNum = 1;

                    foreach ($seedPairs as $pair) {
                        $rider1 = ($pair[0] <= $numQualifiers) ? $qualifiers[$pair[0] - 1] : null;
                        $rider2 = ($pair[1] <= $numQualifiers) ? $qualifiers[$pair[1] - 1] : null;

                        $status = ($rider1 && $rider2) ? 'pending' : 'bye';
                        $winnerId = null;

                        if ($status === 'bye') {
                            $winnerId = $rider1 ? $rider1['rider_id'] : ($rider2 ? $rider2['rider_id'] : null);
                        }

                        if ($rider1 || $rider2) {
                            $stmt = $pdo->prepare("
                                INSERT INTO elimination_brackets
                                (event_id, class_id, bracket_type, round_name, round_number, heat_number,
                                 rider_1_id, rider_2_id, rider_1_seed, rider_2_seed, winner_id, status, bracket_position)
                                VALUES (?, ?, 'main', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ");
                            $stmt->execute([
                                $eventId, $classId, $roundName, $roundNumber, $heatNum,
                                $rider1 ? $rider1['rider_id'] : null,
                                $rider2 ? $rider2['rider_id'] : null,
                                $pair[0], $pair[1],
                                $winnerId, $status, $heatNum
                            ]);
                            $heatNum++;
                        }
                    }

                    // NOTE: Generera INTE nästa runda här!
                    // Nästa runda skapas automatiskt när alla heats i nuvarande runda har vinnare.
                    // Om alla heats är BYEs, kör generateNextRounds direkt
                    $pendingCount = $db->getRow("
                        SELECT COUNT(*) as cnt FROM elimination_brackets
                        WHERE event_id = ? AND class_id = ? AND status = 'pending'
                    ", [$eventId, $classId]);

                    if ($pendingCount['cnt'] == 0) {
                        // Alla heats är BYEs, generera nästa runda direkt
                        generateNextRounds($pdo, $eventId, $classId);
                    }

                    $generatedCount++;
                    $totalRiders += $numQualifiers;

                    // Get class name for message
                    $className = $db->getRow("SELECT display_name, name FROM classes WHERE id = ?", [$classId]);
                    $classResults[] = ($className['display_name'] ?? $className['name']) . " ({$numQualifiers} åkare, {$bracketSize}-bracket)";
                }
            }

            if ($generatedCount > 0) {
                // Verify what was actually inserted
                $debugInfo = [];
                foreach ($allClasses as $classRow) {
                    $cid = $classRow['class_id'];
                    $firstHeats = $db->getAll("
                        SELECT heat_number, rider_1_seed, rider_2_seed
                        FROM elimination_brackets
                        WHERE event_id = ? AND class_id = ?
                        ORDER BY round_number, heat_number
                        LIMIT 4
                    ", [$eventId, $cid]);
                    if (!empty($firstHeats)) {
                        $heatsInfo = [];
                        foreach ($firstHeats as $h) {
                            $heatsInfo[] = "H{$h['heat_number']}:[{$h['rider_1_seed']}v{$h['rider_2_seed']}]";
                        }
                        $debugInfo[] = implode(' ', $heatsInfo);
                    }
                }
                $debugStr = !empty($debugInfo) ? " | Seeds: " . implode('; ', $debugInfo) : '';
                $_SESSION['success'] = "Bracket genererade för {$generatedCount} klasser, totalt {$totalRiders} åkare: " . implode(', ', $classResults) . $debugStr;
            } else {
                $_SESSION['error'] = "Inga klasser med tillräckligt med kvalificerade åkare (minst 2 krävs).";
            }
        } catch (Exception $e) {
            $_SESSION['error'] = "Fel vid generering: " . $e->getMessage();
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$selectedClassId}");
        exit;
    }

    if ($action === 'clear_all_results') {
        // Clear ALL results for this event (all classes)
        try {
            // Delete all brackets for this event
            $pdo->prepare("DELETE FROM elimination_brackets WHERE event_id = ?")->execute([$eventId]);

            // Delete all qualifying results for this event
            $pdo->prepare("DELETE FROM elimination_qualifying WHERE event_id = ?")->execute([$eventId]);

            // Delete all final results from elimination_results
            $pdo->prepare("DELETE FROM elimination_results WHERE event_id = ?")->execute([$eventId]);

            // Delete from main results table (only for classes that had elimination data)
            $pdo->prepare("DELETE FROM results WHERE event_id = ?")->execute([$eventId]);

            // Delete class mappings too
            try {
                $pdo->prepare("DELETE FROM elimination_class_mapping WHERE event_id = ?")->execute([$eventId]);
            } catch (Exception $e) {
                // Table might not exist
            }

            $_SESSION['success'] = "Alla resultat för detta event har rensats (alla klasser).";
        } catch (Exception $e) {
            $_SESSION['error'] = "Fel vid rensning: " . $e->getMessage();
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}");
        exit;
    }

    if ($action === 'clear_qualifying') {
        // Clear qualifying results for this class (and any brackets)
        $classId = intval($_POST['class_id'] ?? 0);

        if ($classId) {
            try {
                // Delete brackets first (they depend on qualifying)
                $pdo->prepare("DELETE FROM elimination_brackets WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                // Delete qualifying results
                $pdo->prepare("DELETE FROM elimination_qualifying WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                // Delete final results from elimination_results
                $pdo->prepare("DELETE FROM elimination_results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                // Also delete from main results table
                $pdo->prepare("DELETE FROM results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                $_SESSION['success'] = "Alla resultat rensade för denna klass (kvalificering, bracket och tävlingsresultat).";
            } catch (Exception $e) {
                $_SESSION['error'] = "Fel vid rensning: " . $e->getMessage();
            }
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$classId}");
        exit;
    }

    if ($action === 'clear_brackets') {
        // Clear only brackets (keep qualifying)
        $classId = intval($_POST['class_id'] ?? 0);

        if ($classId) {
            try {
                $pdo->prepare("DELETE FROM elimination_brackets WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);
                $pdo->prepare("DELETE FROM elimination_results WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                // Reset advances_to_bracket flag
                $pdo->prepare("UPDATE elimination_qualifying SET advances_to_bracket = 0 WHERE event_id = ? AND class_id = ?")->execute([$eventId, $classId]);

                $_SESSION['success'] = "Bracket rensat. Kvalificeringsresultat behålls.";
            } catch (Exception $e) {
                $_SESSION['error'] = "Fel vid rensning: " . $e->getMessage();
            }
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$classId}");
        exit;
    }

    if ($action === 'resync_results') {
        // Re-sync elimination results to main results table
        $classId = intval($_POST['class_id'] ?? 0);

        if ($classId) {
            try {
                // First regenerate elimination_results from brackets
                generateFinalResults($pdo, $db, $eventId, $classId);

                $_SESSION['success'] = "Resultat synkade om från bracket-placeringar!";
            } catch (Exception $e) {
                $_SESSION['error'] = "Fel vid synkning: " . $e->getMessage();
            }
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$classId}");
        exit;
    }

    if ($action === 'save_heat') {
        // Save heat result
        $heatId = intval($_POST['heat_id'] ?? 0);
        $isBye = isset($_POST['is_bye']) && $_POST['is_bye'] === '1';
        $skipBye = isset($_POST['skip_bye']) && $_POST['skip_bye'] === '1';

        // Handle both comma and dot as decimal separator
        $rider1Run1 = floatval(str_replace(',', '.', $_POST['rider1_run1'] ?? '0'));
        $rider1Run2 = floatval(str_replace(',', '.', $_POST['rider1_run2'] ?? '0'));
        $rider2Run1 = floatval(str_replace(',', '.', $_POST['rider2_run1'] ?? '0'));
        $rider2Run2 = floatval(str_replace(',', '.', $_POST['rider2_run2'] ?? '0'));

        if ($heatId) {
            $rider1Total = $rider1Run1 + $rider1Run2;
            $rider2Total = $rider2Run1 + $rider2Run2;

            // Get current heat data
            $heat = $db->getRow("SELECT * FROM elimination_brackets WHERE id = ?", [$heatId]);
            $winnerId = $heat['winner_id']; // Keep existing winner for BYE
            $loserId = $heat['loser_id'];

            if ($skipBye && $isBye) {
                // Just mark BYE as completed without times - winner is already set
                $stmt = $pdo->prepare("UPDATE elimination_brackets SET status = 'completed' WHERE id = ?");
                $stmt->execute([$heatId]);
                $_SESSION['success'] = "BYE-runda markerad som klar!";

                // Advance winner to next round
                advanceWinnerToNextRound($pdo, $db, $eventId, $heat);

                // Check if this completes final or bronze match
                if (in_array($heat['round_name'], ['final', 'third_place'])) {
                    generateFinalResults($pdo, $db, $eventId, $heat['class_id']);
                }

                header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$selectedClassId}");
                exit;
            } elseif ($isBye) {
                // For BYE heats with times, save times and mark completed
                $stmt = $pdo->prepare("
                    UPDATE elimination_brackets SET
                        rider_1_run1 = ?, rider_1_run2 = ?, rider_1_total = ?,
                        rider_2_run1 = ?, rider_2_run2 = ?, rider_2_total = ?,
                        status = 'completed'
                    WHERE id = ?
                ");
                $stmt->execute([
                    $rider1Run1 ?: null, $rider1Run2 ?: null, $rider1Total ?: null,
                    $rider2Run1 ?: null, $rider2Run2 ?: null, $rider2Total ?: null,
                    $heatId
                ]);

                // Advance winner to next round
                advanceWinnerToNextRound($pdo, $db, $eventId, $heat);

                // Check if this completes final or bronze match
                if (in_array($heat['round_name'], ['final', 'third_place'])) {
                    generateFinalResults($pdo, $db, $eventId, $heat['class_id']);
                }
            } else {
                // Normal heat - determine winner (lower total time wins)
                if ($rider1Total > 0 && $rider2Total > 0) {
                    if ($rider1Total < $rider2Total) {
                        $winnerId = $heat['rider_1_id'];
                        $loserId = $heat['rider_2_id'];
                    } else {
                        $winnerId = $heat['rider_2_id'];
                        $loserId = $heat['rider_1_id'];
                    }
                }

                $stmt = $pdo->prepare("
                    UPDATE elimination_brackets SET
                        rider_1_run1 = ?, rider_1_run2 = ?, rider_1_total = ?,
                        rider_2_run1 = ?, rider_2_run2 = ?, rider_2_total = ?,
                        winner_id = ?, loser_id = ?, status = 'completed'
                    WHERE id = ?
                ");
                $stmt->execute([
                    $rider1Run1, $rider1Run2, $rider1Total,
                    $rider2Run1, $rider2Run2, $rider2Total,
                    $winnerId, $loserId, $heatId
                ]);

                // Advance winner to next round if we have a winner
                if ($winnerId) {
                    // Reload heat with winner_id to pass to function
                    $completedHeat = $db->getRow("SELECT * FROM elimination_brackets WHERE id = ?", [$heatId]);
                    advanceWinnerToNextRound($pdo, $db, $eventId, $completedHeat);

                    // Check if this completes final or bronze match - generate final results
                    if (in_array($completedHeat['round_name'], ['final', 'third_place'])) {
                        generateFinalResults($pdo, $db, $eventId, $completedHeat['class_id']);
                    }
                }
            }

            $_SESSION['success'] = "Heat sparat!";
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}&class_id={$selectedClassId}");
        exit;
    }

    if ($action === 'save_series_classes') {
        // Save series class for each rider
        $seriesClasses = $_POST['series_class'] ?? [];

        try {
            // First check if series_class_id column exists
            try {
                $pdo->query("SELECT series_class_id FROM elimination_qualifying LIMIT 1");
            } catch (Exception $e) {
                // Column doesn't exist, add it
                $pdo->exec("ALTER TABLE elimination_qualifying ADD COLUMN series_class_id INT NULL AFTER class_id");
            }

            $updated = 0;
            foreach ($seriesClasses as $qualId => $seriesClassId) {
                $qualId = intval($qualId);
                $seriesClassId = !empty($seriesClassId) ? intval($seriesClassId) : null;

                $stmt = $pdo->prepare("UPDATE elimination_qualifying SET series_class_id = ? WHERE id = ?");
                $stmt->execute([$seriesClassId, $qualId]);
                $updated++;

                // Also sync to main results table with the new series class
                $qual = $db->getRow("SELECT * FROM elimination_qualifying WHERE id = ?", [$qualId]);
                if ($qual) {
                    $targetClass = $seriesClassId ?: $qual['class_id'];

                    // Check if rider has a final bracket result - use that position instead of qualifying
                    $finalResult = $db->getRow("
                        SELECT final_position FROM elimination_results
                        WHERE event_id = ? AND rider_id = ?
                    ", [$qual['event_id'], $qual['rider_id']]);

                    // Use final bracket position if available, otherwise qualifying position
                    $position = $finalResult ? $finalResult['final_position'] : $qual['seed_position'];

                    // Delete old result first (to handle class change)
                    $pdo->prepare("DELETE FROM results WHERE event_id = ? AND cyclist_id = ? AND class_id != ?")->execute([
                        $qual['event_id'], $qual['rider_id'], $targetClass
                    ]);

                    $syncStmt = $pdo->prepare("
                        INSERT INTO results (event_id, class_id, cyclist_id, position, finish_time, bib_number, status)
                        VALUES (?, ?, ?, ?, ?, ?, 'finished')
                        ON DUPLICATE KEY UPDATE
                        position = VALUES(position),
                        finish_time = VALUES(finish_time)
                    ");
                    $syncStmt->execute([
                        $qual['event_id'],
                        $targetClass,
                        $qual['rider_id'],
                        $position,
                        $qual['best_time'],
                        $qual['bib_number']
                    ]);
                }
            }

            $_SESSION['success'] = "Seriepoängklasser sparade för {$updated} deltagare!";
        } catch (Exception $e) {
            $_SESSION['error'] = "Fel vid sparande: " . $e->getMessage();
        }

        header("Location: /admin/elimination-manage.php?event_id={$eventId}");
        exit;
    }
}

// Get class mappings for this event
$classMappings = [];
try {
    $mappingsRaw = $db->getAll("
        SELECT ds_class_id, series_class_id FROM elimination_class_mapping
        WHERE event_id = ?
    ", [$eventId]);
    foreach ($mappingsRaw as $m) {
        $classMappings[$m['ds_class_id']] = $m['series_class_id'];
    }
} catch (Exception $e) {
    // Table might not exist yet
}

// Get all series classes for dropdown
$allSeriesClasses = $db->getAll("
    SELECT id, name, display_name, discipline
    FROM classes
    WHERE active = 1
    ORDER BY sort_order, name
");

// Page config
$page_title = 'Hantera Elimination - ' . $event['name'];
$breadcrumbs = [
    ['label' => 'Tävlingar', 'url' => '/admin/events.php'],
    ['label' => 'Elimination', 'url' => '/admin/elimination.php'],
    ['label' => $event['name']]
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if (isset($_SESSION['success'])): ?>
    <div class="alert alert-success mb-lg">
        <i data-lucide="check-circle"></i>
        <?= h($_SESSION['success']) ?>
    </div>
    <?php unset($_SESSION['success']); ?>
<?php endif; ?>

<?php if (isset($_SESSION['error'])): ?>
    <div class="alert alert-danger mb-lg">
        <i data-lucide="alert-circle"></i>
        <?= h($_SESSION['error']) ?>
    </div>
    <?php unset($_SESSION['error']); ?>
<?php endif; ?>

<?php if (!$tablesExist): ?>
    <div class="admin-card">
        <div class="admin-card-body">
            <div class="alert alert-warning">
                <i data-lucide="database"></i>
                <strong>Databastabeller saknas!</strong>
                <p>Elimination-tabellerna har inte skapats än. Kör migrationen först:</p>
                <a href="/admin/run-migrations.php" class="btn-admin btn-admin-primary mt-md">Kör Migrationer</a>
            </div>
        </div>
    </div>
<?php else: ?>

<!-- Event Info Header -->
<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <div class="flex items-center justify-between flex-wrap gap-md">
            <div>
                <h2 style="margin: 0;"><?= h($event['name']) ?></h2>
                <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                    <?= date('Y-m-d', strtotime($event['date'])) ?> &middot; <?= h($event['location'] ?? 'Okänd plats') ?>
                    <?php if ($event['series_name']): ?>
                        &middot; <?= h($event['series_name']) ?>
                    <?php endif; ?>
                </p>
            </div>
            <div class="flex gap-sm">
                <a href="/admin/elimination-live.php?event_id=<?= $eventId ?>&class_id=<?= $selectedClassId ?>" class="btn-admin btn-admin-primary">
                    <i data-lucide="radio"></i> Live Entry
                </a>
                <a href="/event/<?= $eventId ?>?tab=elimination" class="btn-admin btn-admin-secondary">
                    <i data-lucide="eye"></i> Visa publikt
                </a>
            </div>
        </div>
    </div>
</div>

<!-- Global Actions: Import & Generate Brackets -->
<?php
$totalQualifiers = 0;
$classesWithData = [];
if ($tablesExist) {
    $qualStats = $db->getAll("
        SELECT c.id, c.display_name, c.name, COUNT(eq.id) as count
        FROM elimination_qualifying eq
        JOIN classes c ON eq.class_id = c.id
        WHERE eq.event_id = ? AND eq.status = 'finished'
        GROUP BY c.id, c.display_name, c.name
    ", [$eventId]);
    foreach ($qualStats as $qs) {
        $totalQualifiers += $qs['count'];
        $classesWithData[] = ($qs['display_name'] ?? $qs['name']) . " ({$qs['count']})";
    }
}
$hasBrackets = !empty($brackets);
?>
<div class="admin-card mb-lg" style="background: linear-gradient(135deg, var(--color-bg) 0%, rgba(97,206,112,0.1) 100%); border: 2px solid var(--color-accent);">
    <div class="admin-card-body">
        <div class="flex items-center justify-between flex-wrap gap-md">
            <div>
                <h3 style="margin: 0; display: flex; align-items: center; gap: var(--space-sm);">
                    <i data-lucide="git-branch" style="color: var(--color-accent);"></i>
                    Bracket-generering
                </h3>
                <?php if ($totalQualifiers > 0): ?>
                    <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                        <?= $totalQualifiers ?> åkare i <?= count($classesWithData) ?> klasser: <?= implode(', ', $classesWithData) ?>
                    </p>
                <?php else: ?>
                    <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                        Ladda först upp kvalificeringsresultat
                    </p>
                <?php endif; ?>
            </div>
            <div class="flex gap-sm flex-wrap">
                <a href="/admin/elimination-import-qualifying.php?event_id=<?= $eventId ?>" class="btn-admin btn-admin-secondary">
                    <i data-lucide="upload"></i> Importera kvalresultat
                </a>
                <?php if ($totalQualifiers >= 2): ?>
                    <form method="POST" style="display: inline;" id="generate-brackets-form">
                        <input type="hidden" name="action" value="generate_brackets">
                        <button type="button" onclick="confirmGenerateBrackets()" class="btn-admin btn-admin-primary" style="background: var(--color-accent);">
                            <i data-lucide="play"></i> Generera bracket för alla klasser
                        </button>
                    </form>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<script>
function confirmGenerateBrackets() {
    const classInfo = <?= json_encode($classesWithData) ?>;
    const message = `Vill du generera bracket för alla klasser?\n\n${classInfo.join('\n')}\n\nBefintliga brackets kommer att ersättas.`;

    if (confirm(message)) {
        document.getElementById('generate-brackets-form').submit();
    }
}

function confirmClearAll() {
    const message = 'Vill du rensa ALLA resultat för detta event?\n\nDetta tar bort:\n- Alla kvalificeringsresultat\n- Alla brackets\n- Alla slutresultat\n\nDenna åtgärd kan inte ångras!';

    if (confirm(message)) {
        document.getElementById('clear-all-form').submit();
    }
}
</script>


<!-- Clear All Results -->
<?php if ($totalQualifiers > 0): ?>
<div class="admin-card mb-lg" style="border-color: var(--color-error);">
    <div class="admin-card-body">
        <div class="flex items-center justify-between flex-wrap gap-md">
            <div>
                <h4 style="margin: 0; color: var(--color-error);">
                    <i data-lucide="trash-2"></i> Rensa alla resultat
                </h4>
                <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                    Tar bort alla kvalificeringar, brackets och resultat för detta event.
                </p>
            </div>
            <form method="POST" style="display: inline;" id="clear-all-form">
                <input type="hidden" name="action" value="clear_all_results">
                <button type="button" onclick="confirmClearAll()" class="btn-admin btn-admin-danger">
                    <i data-lucide="trash-2"></i> Rensa allt
                </button>
            </form>
        </div>
    </div>
</div>
<?php endif; ?>

<?php
$totalQualCount = 0;
foreach ($allQualifyingByClass as $cdata) {
    $totalQualCount += count($cdata['results'] ?? []);
}
$totalBracketCount = 0;
foreach ($allBracketsByClass as $cdata) {
    foreach ($cdata['rounds'] ?? [] as $heats) {
        $totalBracketCount += count($heats);
    }
}
$totalResultCount = 0;
foreach ($allFinalResultsByClass as $cdata) {
    $totalResultCount += count($cdata['results'] ?? []);
}
?>

<!-- Clear Brackets Only (keep qualifying) -->
<?php if ($totalBracketCount > 0): ?>
<div class="admin-card mb-lg" style="border-color: var(--color-warning);">
    <div class="admin-card-body">
        <div class="flex items-center justify-between flex-wrap gap-md">
            <div>
                <h4 style="margin: 0; color: var(--color-warning);">
                    <i data-lucide="refresh-cw"></i> Rensa bracket
                </h4>
                <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                    Tar bort brackets och slutresultat. Kvalificeringsresultat behålls.
                </p>
            </div>
            <div class="flex gap-sm">
                <?php foreach ($allBracketsByClass as $classId => $classData): ?>
                    <form method="POST" style="display: inline;" class="clear-bracket-form">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="clear_brackets">
                        <input type="hidden" name="class_id" value="<?= $classId ?>">
                        <button type="submit" class="btn-admin btn-admin-warning" onclick="return confirm('Rensa bracket för <?= h($classData['name'] ?? 'denna klass') ?>?\n\nKvalificeringsresultat behålls.')">
                            <i data-lucide="trash"></i> <?= h($classData['name'] ?? 'Klass ' . $classId) ?>
                        </button>
                    </form>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Tabs for different sections -->
<div class="tabs mb-lg">
    <nav class="tabs-nav">
        <button class="tab-btn active" data-tab="qualifying">
            <i data-lucide="timer"></i> Kvalificering
            <span class="admin-badge admin-badge-<?= $totalQualCount > 0 ? 'success' : 'secondary' ?> ml-sm"><?= $totalQualCount ?></span>
        </button>
        <button class="tab-btn" data-tab="brackets">
            <i data-lucide="git-branch"></i> Bracket
            <span class="admin-badge admin-badge-<?= $totalBracketCount > 0 ? 'success' : 'secondary' ?> ml-sm"><?= $totalBracketCount ?></span>
        </button>
        <button class="tab-btn" data-tab="results">
            <i data-lucide="trophy"></i> Resultat
            <span class="admin-badge admin-badge-<?= $totalResultCount > 0 ? 'success' : 'secondary' ?> ml-sm"><?= $totalResultCount ?></span>
        </button>
    </nav>

    <!-- QUALIFYING TAB - Shows ALL classes -->
    <div class="tab-content active" id="qualifying">
        <?php if (empty($allQualifyingByClass)): ?>
            <div class="admin-card">
                <div class="admin-card-body">
                    <div class="admin-empty-state">
                        <i data-lucide="timer"></i>
                        <h3>Inga kvalresultat</h3>
                        <p>Importera kvalificeringsresultat för att komma igång.</p>
                        <a href="/admin/elimination-import-qualifying.php?event_id=<?= $eventId ?>" class="btn-admin btn-admin-primary mt-md">
                            <i data-lucide="upload"></i> Importera kvalresultat
                        </a>
                    </div>
                </div>
            </div>
        <?php else: ?>
            <form method="POST" id="series-class-form">
                <input type="hidden" name="action" value="save_series_classes">
                <div class="mb-md flex justify-end">
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <i data-lucide="save"></i> Spara seriepoängklasser
                    </button>
                </div>
            <?php foreach ($allQualifyingByClass as $classId => $classData): ?>
                <div class="admin-card mb-lg">
                    <div class="admin-card-header">
                        <h3><?= h($classData['name']) ?></h3>
                        <span class="admin-badge admin-badge-success"><?= count($classData['results']) ?> åkare</span>
                    </div>
                    <div class="admin-card-body" style="padding: 0;">
                        <div class="admin-table-container">
                            <table class="admin-table">
                                <thead>
                                    <tr>
                                        <th>Seed</th>
                                        <th>Nr</th>
                                        <th>Namn</th>
                                        <th>Klubb</th>
                                        <th class="text-right">Bäst</th>
                                        <th>Seriepoängklass</th>
                                        <th class="text-center">Bracket</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($classData['results'] as $qr): ?>
                                        <tr class="<?= $qr['advances_to_bracket'] ? 'row-highlight' : '' ?>">
                                            <td><strong><?= $qr['seed_position'] ?? '-' ?></strong></td>
                                            <td><?= h($qr['bib_number'] ?? '-') ?></td>
                                            <td><?= h($qr['firstname'] . ' ' . $qr['lastname']) ?></td>
                                            <td><?= h($qr['club_name'] ?? '-') ?></td>
                                            <td class="text-right"><strong><?= $qr['best_time'] ? number_format($qr['best_time'], 3) : '-' ?></strong></td>
                                            <td>
                                                <select name="series_class[<?= $qr['id'] ?>]" class="admin-form-select" style="min-width: 150px; font-size: var(--text-sm);">
                                                    <option value="">-- DS-klass --</option>
                                                    <?php foreach ($allSeriesClasses as $sc): ?>
                                                        <option value="<?= $sc['id'] ?>" <?= ($qr['series_class_id'] ?? '') == $sc['id'] ? 'selected' : '' ?>>
                                                            <?= h($sc['display_name'] ?? $sc['name']) ?>
                                                        </option>
                                                    <?php endforeach; ?>
                                                </select>
                                            </td>
                                            <td class="text-center">
                                            <?php if ($qr['advances_to_bracket']): ?>
                                                <span class="admin-badge admin-badge-success">Ja</span>
                                            <?php else: ?>
                                                <span class="admin-badge admin-badge-secondary">Nej</span>
                                            <?php endif; ?>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
            </form>
        <?php endif; ?>
    </div>

    <!-- BRACKETS TAB - Shows ALL classes -->
    <div class="tab-content" id="brackets">
        <?php if (empty($allBracketsByClass)): ?>
            <div class="admin-card">
                <div class="admin-card-body">
                    <div class="admin-empty-state">
                        <i data-lucide="git-branch"></i>
                        <h3>Ingen bracket genererad</h3>
                        <p>Generera bracket från kvalificeringsresultaten.</p>
                    </div>
                </div>
            </div>
        <?php else: ?>
            <?php
            $roundNames = [
                'round_of_32' => '32-delsfinal',
                'round_of_16' => '16-delsfinal',
                'quarterfinal' => 'Kvartsfinal',
                'semifinal' => 'Semifinal',
                'third_place' => 'Brons',
                'final' => 'Final'
            ];
            ?>
            <?php foreach ($allBracketsByClass as $classId => $classData): ?>
                <div class="admin-card mb-lg">
                    <div class="admin-card-header">
                        <h3><?= h($classData['name']) ?></h3>
                    </div>
                    <div class="admin-card-body">
                        <?php foreach ($classData['rounds'] as $roundName => $heats): ?>
                        <div class="bracket-round mb-lg">
                            <h4 class="mb-md"><?= $roundNames[$roundName] ?? ucfirst($roundName) ?></h4>
                            <div class="bracket-heats">
                                <?php foreach ($heats as $heat): ?>
                                    <div class="bracket-heat admin-card mb-sm" style="background: var(--color-bg-secondary);">
                                        <div class="admin-card-body" style="padding: var(--space-sm);">
                                            <div class="flex justify-between items-center mb-sm">
                                                <span class="text-sm text-secondary">Heat <?= $heat['heat_number'] ?></span>
                                                <span class="admin-badge admin-badge-<?= $heat['status'] === 'completed' ? 'success' : ($heat['status'] === 'bye' ? 'warning' : 'secondary') ?>">
                                                    <?= $heat['status'] === 'completed' ? 'Klar' : ($heat['status'] === 'bye' ? 'BYE' : 'Väntar') ?>
                                                </span>
                                            </div>

                                            <?php if ($heat['status'] === 'bye'): ?>
                                                <form method="POST" class="bracket-matchup-form">
                                                    <input type="hidden" name="action" value="save_heat">
                                                    <input type="hidden" name="heat_id" value="<?= $heat['id'] ?>">
                                                    <input type="hidden" name="is_bye" value="1">

                                                    <div class="bracket-rider winner">
                                                        <span class="seed"><?= $heat['rider_1_seed'] ?: $heat['rider_2_seed'] ?></span>
                                                        <span class="name">
                                                            <?php if ($heat['rider_1_id']): ?>
                                                                <?= h($heat['rider1_firstname'] . ' ' . $heat['rider1_lastname']) ?>
                                                            <?php else: ?>
                                                                <?= h($heat['rider2_firstname'] . ' ' . $heat['rider2_lastname']) ?>
                                                            <?php endif; ?>
                                                        </span>
                                                        <div class="times">
                                                            <?php if ($heat['rider_1_id']): ?>
                                                                <input type="text" inputmode="decimal" name="rider1_run1" value="<?= $heat['rider_1_run1'] ? number_format($heat['rider_1_run1'], 3) : '' ?>" placeholder="Åk1" class="time-input">
                                                                <input type="text" inputmode="decimal" name="rider1_run2" value="<?= $heat['rider_1_run2'] ? number_format($heat['rider_1_run2'], 3) : '' ?>" placeholder="Åk2" class="time-input">
                                                                <span class="total"><?= $heat['rider_1_total'] ? number_format($heat['rider_1_total'], 3) : '-' ?></span>
                                                            <?php else: ?>
                                                                <input type="text" inputmode="decimal" name="rider2_run1" value="<?= $heat['rider_2_run1'] ? number_format($heat['rider_2_run1'], 3) : '' ?>" placeholder="Åk1" class="time-input">
                                                                <input type="text" inputmode="decimal" name="rider2_run2" value="<?= $heat['rider_2_run2'] ? number_format($heat['rider_2_run2'], 3) : '' ?>" placeholder="Åk2" class="time-input">
                                                                <span class="total"><?= $heat['rider_2_total'] ? number_format($heat['rider_2_total'], 3) : '-' ?></span>
                                                            <?php endif; ?>
                                                        </div>
                                                    </div>

                                                    <div class="bracket-rider bye-slot">
                                                        <span class="seed">-</span>
                                                        <span class="name"><em>BYE</em></span>
                                                    </div>

                                                    <div class="flex gap-sm mt-sm">
                                                        <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm">
                                                            <i data-lucide="save"></i> Spara tider
                                                        </button>
                                                        <button type="submit" name="skip_bye" value="1" class="btn-admin btn-admin-secondary btn-admin-sm">
                                                            <i data-lucide="skip-forward"></i> Gå vidare
                                                        </button>
                                                    </div>
                                                </form>
                                            <?php else: ?>
                                                <form method="POST" class="bracket-matchup-form">
                                                    <input type="hidden" name="action" value="save_heat">
                                                    <input type="hidden" name="heat_id" value="<?= $heat['id'] ?>">

                                                    <!-- Rider 1 -->
                                                    <div class="bracket-rider <?= $heat['winner_id'] == $heat['rider_1_id'] ? 'winner' : '' ?>">
                                                        <span class="seed"><?= $heat['rider_1_seed'] ?></span>
                                                        <span class="name"><?= h($heat['rider1_firstname'] . ' ' . $heat['rider1_lastname']) ?></span>
                                                        <div class="times">
                                                            <input type="text" inputmode="decimal" name="rider1_run1" value="<?= $heat['rider_1_run1'] ? number_format($heat['rider_1_run1'], 3) : '' ?>" placeholder="Åk1" class="time-input">
                                                            <input type="text" inputmode="decimal" name="rider1_run2" value="<?= $heat['rider_1_run2'] ? number_format($heat['rider_1_run2'], 3) : '' ?>" placeholder="Åk2" class="time-input">
                                                            <span class="total"><?= $heat['rider_1_total'] ? number_format($heat['rider_1_total'], 3) : '-' ?></span>
                                                        </div>
                                                    </div>

                                                    <div class="vs">vs</div>

                                                    <!-- Rider 2 -->
                                                    <div class="bracket-rider <?= $heat['winner_id'] == $heat['rider_2_id'] ? 'winner' : '' ?>">
                                                        <span class="seed"><?= $heat['rider_2_seed'] ?></span>
                                                        <span class="name"><?= h($heat['rider2_firstname'] . ' ' . $heat['rider2_lastname']) ?></span>
                                                        <div class="times">
                                                            <input type="text" inputmode="decimal" name="rider2_run1" value="<?= $heat['rider_2_run1'] ? number_format($heat['rider_2_run1'], 3) : '' ?>" placeholder="Åk1" class="time-input">
                                                            <input type="text" inputmode="decimal" name="rider2_run2" value="<?= $heat['rider_2_run2'] ? number_format($heat['rider_2_run2'], 3) : '' ?>" placeholder="Åk2" class="time-input">
                                                            <span class="total"><?= $heat['rider_2_total'] ? number_format($heat['rider_2_total'], 3) : '-' ?></span>
                                                        </div>
                                                    </div>

                                                    <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm mt-sm">
                                                        <i data-lucide="save"></i> Spara
                                                    </button>
                                                </form>
                                            <?php endif; ?>
                                        </div>
                                    </div>
                                <?php endforeach; ?>
                            </div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>

    <!-- RESULTS TAB - Shows ALL classes -->
    <div class="tab-content" id="results">
        <?php if (empty($allFinalResultsByClass)): ?>
            <div class="admin-card">
                <div class="admin-card-body">
                    <div class="admin-empty-state">
                        <i data-lucide="trophy"></i>
                        <h3>Inga slutresultat</h3>
                        <p>Slutresultat genereras automatiskt när alla heats är klara.</p>
                    </div>
                </div>
            </div>
        <?php else: ?>
            <?php foreach ($allFinalResultsByClass as $classId => $classData): ?>
                <div class="admin-card mb-lg">
                    <div class="admin-card-header" style="display: flex; justify-content: space-between; align-items: center;">
                        <h3><?= h($classData['name']) ?></h3>
                        <form method="POST" style="display: inline;">
                            <?= csrf_field() ?>
                            <input type="hidden" name="action" value="resync_results">
                            <input type="hidden" name="class_id" value="<?= $classId ?>">
                            <button type="submit" class="btn-admin btn-admin-sm btn-admin-secondary" title="Synka om resultat från brackets till resultattabellen">
                                <i data-lucide="refresh-cw"></i> Synka om
                            </button>
                        </form>
                    </div>
                    <div class="admin-card-body" style="padding: 0;">
                        <div class="admin-table-container">
                            <table class="admin-table">
                                <thead>
                                    <tr>
                                        <th>Plac</th>
                                        <th>Namn</th>
                                        <th>Klubb</th>
                                        <th>Kval</th>
                                        <th>Bracket</th>
                                        <th class="text-right">Poäng</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($classData['results'] as $result): ?>
                                        <tr>
                                            <td>
                                                <?php if ($result['final_position'] <= 3): ?>
                                                    <span class="position-badge position-<?= $result['final_position'] ?>"><?= $result['final_position'] ?></span>
                                                <?php else: ?>
                                                    <?= $result['final_position'] ?>
                                                <?php endif; ?>
                                            </td>
                                            <td><?= h($result['firstname'] . ' ' . $result['lastname']) ?></td>
                                            <td><?= h($result['club_name'] ?? '-') ?></td>
                                            <td><?= $result['qualifying_position'] ?? '-' ?></td>
                                            <td>
                                                <?php if ($result['bracket_type'] === 'consolation'): ?>
                                                    <span class="admin-badge admin-badge-warning">B</span>
                                                <?php else: ?>
                                                    <span class="admin-badge admin-badge-success">A</span>
                                                <?php endif; ?>
                                            </td>
                                            <td class="text-right"><?= $result['points'] ?></td>
                                        </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>
</div>

<style>
/* Bracket styling */
.bracket-heats {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--space-md);
}

.bracket-rider {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) var(--space-sm);
    background: var(--color-bg);
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-xs);
}

.bracket-rider.winner {
    background: var(--color-success);
    color: white;
}

.bracket-rider .seed {
    font-weight: 600;
    min-width: 24px;
    text-align: center;
}

.bracket-rider .name {
    flex: 1;
}

.bracket-rider .times {
    display: flex;
    gap: var(--space-xs);
    align-items: center;
}

.time-input {
    width: 70px;
    padding: var(--space-xs);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    text-align: right;
}

.bracket-rider .total {
    font-weight: 600;
    min-width: 60px;
    text-align: right;
}

.vs {
    text-align: center;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    margin: var(--space-xs) 0;
}

.row-highlight {
    background: rgba(97, 206, 112, 0.1);
}

.position-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-weight: 600;
    color: white;
}

.position-1 { background: gold; color: #333; }
.position-2 { background: silver; color: #333; }
.position-3 { background: #cd7f32; }

/* Tabs */
.tabs-nav {
    display: flex;
    gap: var(--space-xs);
    border-bottom: 2px solid var(--color-border);
    margin-bottom: var(--space-lg);
}

.tab-btn {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    border: none;
    background: none;
    cursor: pointer;
    color: var(--color-text-secondary);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
}

.tab-btn:hover {
    color: var(--color-text);
}

.tab-btn.active {
    color: var(--color-accent);
    border-bottom-color: var(--color-accent);
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}
</style>

<script>
// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.dataset.tab;
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});
</script>

<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
