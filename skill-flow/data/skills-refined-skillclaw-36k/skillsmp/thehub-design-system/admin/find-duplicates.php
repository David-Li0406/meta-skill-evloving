<?php
/**
 * Smart Duplicate Finder
 * Find potential duplicate riders - only when one profile is missing data
 */
ini_set('display_errors', '1');
error_reporting(E_ALL);

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// File to store ignored duplicate pairs
$ignoredFile = __DIR__ . '/../uploads/ignored_rider_duplicates.json';

// Load ignored duplicates
function loadIgnoredRiderDuplicates($file) {
    if (file_exists($file)) {
        $data = json_decode(file_get_contents($file), true);
        return is_array($data) ? $data : [];
    }
    return [];
}

// Save ignored duplicates
function saveIgnoredRiderDuplicates($file, $data) {
    $dir = dirname($file);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
    file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));
}

// Generate unique key for a rider pair (sorted so order doesn't matter)
function getRiderPairKey($id1, $id2) {
    return min($id1, $id2) . '-' . max($id1, $id2);
}

$ignoredDuplicates = loadIgnoredRiderDuplicates($ignoredFile);

// Handle ignore action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ignore_pair'])) {
    checkCsrf();
    $pairKey = $_POST['ignore_pair'];
    if (!in_array($pairKey, $ignoredDuplicates)) {
        $ignoredDuplicates[] = $pairKey;
        saveIgnoredRiderDuplicates($ignoredFile, $ignoredDuplicates);
        $_SESSION['dup_message'] = 'Paret markerat som "inte dubbletter" och kommer inte visas igen';
        $_SESSION['dup_message_type'] = 'success';
    }
    header('Location: /admin/find-duplicates.php');
    exit;
}

// Handle reset ignored action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['reset_ignored'])) {
    checkCsrf();
    $ignoredDuplicates = [];
    saveIgnoredRiderDuplicates($ignoredFile, $ignoredDuplicates);
    $_SESSION['dup_message'] = 'Alla ignorerade par återställda';
    $_SESSION['dup_message_type'] = 'info';
    header('Location: /admin/find-duplicates.php');
    exit;
}

// Handle MERGE action - merge two riders
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge_pair'])) {
    checkCsrf();
    $keepId = (int)$_POST['keep_id'];
    $removeId = (int)$_POST['remove_id'];

    if ($keepId > 0 && $removeId > 0 && $keepId !== $removeId) {
        try {
            $pdo = $db->getPdo();
            $pdo->beginTransaction();

            // Move results
            $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
            $stmt->execute([$keepId, $removeId]);
            $resultsMoved = $stmt->rowCount();

            // Move series_results
            $stmt = $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?");
            $stmt->execute([$keepId, $removeId]);
            $seriesResultsMoved = $stmt->rowCount();

            // Get rider info before delete
            $removedRider = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$removeId]);
            $keptRider = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$keepId]);

            // Delete the duplicate
            $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$removeId]);

            $pdo->commit();

            // Remove from ignored list if it was there
            $pairKey = getRiderPairKey($keepId, $removeId);
            $ignoredDuplicates = array_filter($ignoredDuplicates, fn($k) => $k !== $pairKey);
            saveIgnoredRiderDuplicates($ignoredFile, $ignoredDuplicates);

            $_SESSION['dup_message'] = "Sammanslagen! {$removedRider['firstname']} {$removedRider['lastname']} (ID {$removeId}) → {$keptRider['firstname']} {$keptRider['lastname']} (ID {$keepId}). Flyttade {$resultsMoved} resultat.";
            $_SESSION['dup_message_type'] = 'success';
        } catch (Exception $e) {
            if (isset($pdo)) $pdo->rollBack();
            $_SESSION['dup_message'] = 'Fel vid sammanslagning: ' . $e->getMessage();
            $_SESSION['dup_message_type'] = 'error';
        }
    }
    header('Location: /admin/find-duplicates.php');
    exit;
}

// Check for message from redirect
if (isset($_SESSION['dup_message'])) {
 $message = $_SESSION['dup_message'];
 $messageType = $_SESSION['dup_message_type'] ?? 'info';
 unset($_SESSION['dup_message'], $_SESSION['dup_message_type']);
}

// Helper functions - defined first
function normalizeUci($uci) {
 if (empty($uci)) return null;
 return preg_replace('/\s+/', '', $uci);
}

function isRealUci($license) {
 if (empty($license)) return false;
 return strpos($license, 'SWE') !== 0;
}

function nameSimilarity($name1, $name2) {
 $name1 = mb_strtolower(trim($name1), 'UTF-8');
 $name2 = mb_strtolower(trim($name2), 'UTF-8');
 if ($name1 === $name2) return 100;
 if (strlen($name1) < 2 || strlen($name2) < 2) return 0;
 if (strpos($name1, $name2) !== false || strpos($name2, $name1) !== false) {
 return 90;
 }
 $name1 = substr($name1, 0, 255);
 $name2 = substr($name2, 0, 255);
 $maxLen = max(strlen($name1), strlen($name2));
 if ($maxLen === 0) return 0;
 $distance = levenshtein($name1, $name2);
 return round((1 - $distance / $maxLen) * 100);
}

function areNamesSimilar($fn1, $ln1, $fn2, $ln2) {
 $fn1 = trim($fn1); $ln1 = trim($ln1);
 $fn2 = trim($fn2); $ln2 = trim($ln2);

 if (empty($fn1) || empty($ln1) || empty($fn2) || empty($ln2)) {
 return ['match' => false, 'reason' => null];
 }

 if (strtolower($fn1) === strtolower($fn2) && strtolower($ln1) === strtolower($ln2)) {
 return ['match' => true, 'reason' => 'Exakt samma namn'];
 }
 if (strtolower($ln1) === strtolower($ln2)) {
 $fnSim = nameSimilarity($fn1, $fn2);
 if ($fnSim >= 80) {
  return ['match' => true, 'reason' =>"Samma efternamn, liknande förnamn ({$fnSim}%)"];
 }
 }
 $lnSim = nameSimilarity($ln1, $ln2);
 if ($lnSim >= 80 && strtolower($fn1) === strtolower($fn2)) {
 return ['match' => true, 'reason' =>"Samma förnamn, liknande efternamn ({$lnSim}%)"];
 }
 $ln1Lower = strtolower($ln1);
 $ln2Lower = strtolower($ln2);
 if (strlen($ln1Lower) > 3 && strlen($ln2Lower) > 3) {
 if ((strpos($ln1Lower, $ln2Lower) !== false || strpos($ln2Lower, $ln1Lower) !== false) &&
  strtolower($fn1) === strtolower($fn2)) {
  return ['match' => true, 'reason' => 'Samma förnamn, dubbelt efternamn'];
 }
 }
 return ['match' => false, 'reason' => null];
}

function checkDuplicatePair($r1, $r2, $nameReason) {
 $uci1 = normalizeUci($r1['license_number']);
 $uci2 = normalizeUci($r2['license_number']);
 $isRealUci1 = isRealUci($r1['license_number']);
 $isRealUci2 = isRealUci($r2['license_number']);
 $isSweId1 = !empty($r1['license_number']) && strpos($r1['license_number'], 'SWE') === 0;
 $isSweId2 = !empty($r2['license_number']) && strpos($r2['license_number'], 'SWE') === 0;

 // Only exclude if BOTH have real UCI IDs (not SWE) and they're different
 if ($isRealUci1 && $isRealUci2 && $uci1 !== $uci2) {
 return null;
 }

 // If one has SWE-ID and the other has UCI-ID, they're likely duplicates - don't exclude based on birth year
 $oneHasSweOneHasUci = ($isSweId1 && $isRealUci2) || ($isSweId2 && $isRealUci1);

 // Only exclude based on birth year if NEITHER has a SWE-ID (both have real data)
 if (!$oneHasSweOneHasUci && !empty($r1['birth_year']) && !empty($r2['birth_year']) && $r1['birth_year'] !== $r2['birth_year']) {
 return null;
 }

 $r1Missing = [];
 $r2Missing = [];

 if (empty($r1['birth_year']) && !empty($r2['birth_year'])) $r1Missing[] = 'födelseår';
 if (empty($r2['birth_year']) && !empty($r1['birth_year'])) $r2Missing[] = 'födelseår';
 // Mark SWE-ID as "missing UCI ID" when comparing to a real UCI ID
 if ($isSweId1 && $isRealUci2) $r1Missing[] = 'UCI ID (har SWE-ID)';
 elseif (!$isRealUci1 && $isRealUci2) $r1Missing[] = 'UCI ID';
 if ($isSweId2 && $isRealUci1) $r2Missing[] = 'UCI ID (har SWE-ID)';
 elseif (!$isRealUci2 && $isRealUci1) $r2Missing[] = 'UCI ID';
 if (empty($r1['email']) && !empty($r2['email'])) $r1Missing[] = 'e-post';
 if (empty($r2['email']) && !empty($r1['email'])) $r2Missing[] = 'e-post';
 if (empty($r1['club_id']) && !empty($r2['club_id'])) $r1Missing[] = 'klubb';
 if (empty($r2['club_id']) && !empty($r1['club_id'])) $r2Missing[] = 'klubb';

 $sameUci = $isRealUci1 && $isRealUci2 && $uci1 === $uci2;
 $hasMissingData = !empty($r1Missing) || !empty($r2Missing);

 if (!$sameUci && !$hasMissingData) {
 return null;
 }

 return [
 'reason' => $sameUci ? 'Samma UCI ID' : $nameReason,
 'rider1' => [
  'id' => $r1['id'],
  'name' => $r1['firstname'] . ' ' . $r1['lastname'],
  'birth_year' => $r1['birth_year'],
  'license' => $r1['license_number'],
  'email' => $r1['email'],
  'club' => $r1['club_name'],
  'results' => $r1['result_count'],
  'missing' => $r1Missing
 ],
 'rider2' => [
  'id' => $r2['id'],
  'name' => $r2['firstname'] . ' ' . $r2['lastname'],
  'birth_year' => $r2['birth_year'],
  'license' => $r2['license_number'],
  'email' => $r2['email'],
  'club' => $r2['club_name'],
  'results' => $r2['result_count'],
  'missing' => $r2Missing
 ]
 ];
}

// Handle merge action (supports both AJAX and regular requests)
if (isset($_GET['action']) && $_GET['action'] === 'merge') {
    $keepId = (int)($_GET['keep'] ?? 0);
    $removeId = (int)($_GET['remove'] ?? 0);
    $isAjax = !empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';

    if ($keepId && $removeId && $keepId !== $removeId) {
        $transactionStarted = false;
        $resultMessage = '';
        $resultSuccess = false;

        try {
            $db->beginTransaction();
            $transactionStarted = true;

            $keepRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$keepId]);
            $removeRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$removeId]);

            if (empty($keepRider) || empty($removeRider)) {
                throw new Exception("En av ryttarna hittades inte");
            }

            // Move results from remove to keep (include class_id for multi-class support)
            $resultsToMove = $db->getAll("SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?", [$removeId]);
            $moved = 0;
            $deleted = 0;

            foreach ($resultsToMove as $result) {
                // Check if kept rider already has result for this event AND class
                $existing = $db->getRow(
                    "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?",
                    [$keepId, $result['event_id'], $result['class_id']]
                );

                if (!empty($existing)) {
                    $db->delete('results', 'id = ?', [$result['id']]);
                    $deleted++;
                } else {
                    $db->update('results', ['cyclist_id' => $keepId], 'id = ?', [$result['id']]);
                    $moved++;
                }
            }

            // Update keep rider with missing data from remove rider
            $updates = [];
            if (empty($keepRider['birth_year']) && !empty($removeRider['birth_year'])) {
                $updates['birth_year'] = $removeRider['birth_year'];
            }
            if (empty($keepRider['email']) && !empty($removeRider['email'])) {
                $updates['email'] = $removeRider['email'];
            }
            if (empty($keepRider['phone']) && !empty($removeRider['phone'])) {
                $updates['phone'] = $removeRider['phone'];
            }
            if (empty($keepRider['club_id']) && !empty($removeRider['club_id'])) {
                $updates['club_id'] = $removeRider['club_id'];
            }
            if (empty($keepRider['gender']) && !empty($removeRider['gender'])) {
                $updates['gender'] = $removeRider['gender'];
            }
            // Prefer UCI ID over SWE ID
            if (!empty($removeRider['license_number'])) {
                $keepIsSweid = empty($keepRider['license_number']) || strpos($keepRider['license_number'], 'SWE') === 0;
                $removeIsUci = strpos($removeRider['license_number'], 'SWE') !== 0;
                if ($keepIsSweid && $removeIsUci) {
                    $updates['license_number'] = $removeRider['license_number'];
                } elseif (empty($keepRider['license_number'])) {
                    $updates['license_number'] = $removeRider['license_number'];
                }
            }
            if (empty($keepRider['license_type']) && !empty($removeRider['license_type'])) {
                $updates['license_type'] = $removeRider['license_type'];
            }

            if (!empty($updates)) {
                $db->update('riders', $updates, 'id = ?', [$keepId]);
            }

            // Delete the duplicate rider
            $db->delete('riders', 'id = ?', [$removeId]);

            $db->commit();

            $resultMessage = "Sammanfogade {$removeRider['firstname']} {$removeRider['lastname']} → {$keepRider['firstname']} {$keepRider['lastname']} ({$moved} resultat flyttade" . ($deleted > 0 ? ", {$deleted} dubbletter borttagna" : "") . ")";
            $resultSuccess = true;

        } catch (Exception $e) {
            if ($transactionStarted) {
                try {
                    $db->rollback();
                } catch (Exception $rollbackError) {
                    // Ignore rollback errors
                }
            }
            $resultMessage = "Fel: " . $e->getMessage();
            $resultSuccess = false;
        }

        // Return JSON for AJAX requests
        if ($isAjax) {
            header('Content-Type: application/json');
            echo json_encode([
                'success' => $resultSuccess,
                'message' => $resultMessage,
                'keepId' => $keepId,
                'removeId' => $removeId
            ]);
            exit;
        }

        // Regular redirect for non-AJAX
        $_SESSION['dup_message'] = $resultMessage;
        $_SESSION['dup_message_type'] = $resultSuccess ? 'success' : 'error';
        header('Location: /admin/find-duplicates.php');
        exit;
    }
}

// Handle MERGE ALL action - merge all duplicates automatically
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge_all'])) {
    checkCsrf();

    $mergeCount = 0;
    $errorCount = 0;
    $totalResultsMoved = 0;

    // Get all duplicate groups
    $duplicateGroups = $db->getAll("
        SELECT firstname, lastname, COUNT(*) as cnt
        FROM riders
        WHERE firstname IS NOT NULL AND lastname IS NOT NULL
        GROUP BY LOWER(firstname), LOWER(lastname)
        HAVING cnt > 1
        LIMIT 100
    ");

    foreach ($duplicateGroups as $group) {
        // Get all riders in this group
        $riders = $db->getAll("
            SELECT r.*,
                   c.name as club_name,
                   (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE LOWER(r.firstname) = LOWER(?) AND LOWER(r.lastname) = LOWER(?)
            ORDER BY r.id
        ", [$group['firstname'], $group['lastname']]);

        if (count($riders) < 2) continue;

        // Score each rider: higher = more complete data + more results
        foreach ($riders as &$r) {
            $score = $r['result_count'] * 10; // Results are very important
            if (!empty($r['license_number']) && strpos($r['license_number'], 'SWE') !== 0) $score += 100; // Real UCI ID
            if (!empty($r['license_number'])) $score += 10;
            if (!empty($r['birth_year'])) $score += 5;
            if (!empty($r['email'])) $score += 5;
            if (!empty($r['club_id'])) $score += 5;
            if (!empty($r['gender'])) $score += 2;
            $r['score'] = $score;
        }
        unset($r);

        // Sort by score descending
        usort($riders, fn($a, $b) => $b['score'] - $a['score']);

        // Keep the best one, merge others into it
        $keep = array_shift($riders);
        $keepId = $keep['id'];

        // Check if any pair is in the ignored list - skip if so
        $skipGroup = false;
        foreach ($riders as $remove) {
            $pairKey = getRiderPairKey($keepId, $remove['id']);
            if (in_array($pairKey, $ignoredDuplicates)) {
                $skipGroup = true;
                break;
            }
        }
        if ($skipGroup) continue;

        // Check if riders have conflicting UCI IDs (only real UCI IDs, not SWE-IDs)
        $keepLicense = $keep['license_number'] ?? '';
        $keepIsRealUci = !empty($keepLicense) && strpos($keepLicense, 'SWE') !== 0;
        $hasConflict = false;
        foreach ($riders as $remove) {
            $removeLicense = $remove['license_number'] ?? '';
            $removeIsRealUci = !empty($removeLicense) && strpos($removeLicense, 'SWE') !== 0;
            // Only conflict if BOTH have real UCI IDs (not SWE-IDs) and they're different
            if ($keepIsRealUci && $removeIsRealUci) {
                $keepUci = preg_replace('/\s+/', '', $keepLicense);
                $removeUci = preg_replace('/\s+/', '', $removeLicense);
                if ($keepUci !== $removeUci) {
                    $hasConflict = true;
                    break;
                }
            }
        }
        if ($hasConflict) continue;

        // IMPORTANT: Check for conflicting birth years - don't auto-merge different people!
        $keepBirthYear = $keep['birth_year'] ?? null;
        $hasBirthYearConflict = false;
        foreach ($riders as $remove) {
            $removeBirthYear = $remove['birth_year'] ?? null;
            // If BOTH have birth years and they're different, skip this merge
            if (!empty($keepBirthYear) && !empty($removeBirthYear) && $keepBirthYear !== $removeBirthYear) {
                $hasBirthYearConflict = true;
                break;
            }
        }
        if ($hasBirthYearConflict) continue;

        // Merge all others into keep
        foreach ($riders as $remove) {
            $removeId = $remove['id'];

            try {
                $db->beginTransaction();

                // Move results
                $resultsToMove = $db->getAll("SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?", [$removeId]);
                foreach ($resultsToMove as $result) {
                    $existing = $db->getRow(
                        "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?",
                        [$keepId, $result['event_id'], $result['class_id']]
                    );
                    if (!empty($existing)) {
                        $db->delete('results', 'id = ?', [$result['id']]);
                    } else {
                        $db->update('results', ['cyclist_id' => $keepId], 'id = ?', [$result['id']]);
                        $totalResultsMoved++;
                    }
                }

                // Move series_results
                $db->query("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?", [$keepId, $removeId]);

                // Update keep rider with missing data from remove rider
                $updates = [];
                if (empty($keep['birth_year']) && !empty($remove['birth_year'])) {
                    $updates['birth_year'] = $remove['birth_year'];
                    $keep['birth_year'] = $remove['birth_year'];
                }
                if (empty($keep['email']) && !empty($remove['email'])) {
                    $updates['email'] = $remove['email'];
                    $keep['email'] = $remove['email'];
                }
                if (empty($keep['club_id']) && !empty($remove['club_id'])) {
                    $updates['club_id'] = $remove['club_id'];
                    $keep['club_id'] = $remove['club_id'];
                }
                $keepIsSweid = empty($keep['license_number']) || strpos($keep['license_number'], 'SWE') === 0;
                $removeIsUci = !empty($remove['license_number']) && strpos($remove['license_number'], 'SWE') !== 0;
                if ($keepIsSweid && $removeIsUci) {
                    $updates['license_number'] = $remove['license_number'];
                    $keep['license_number'] = $remove['license_number'];
                }
                if (!empty($updates)) {
                    $db->update('riders', $updates, 'id = ?', [$keepId]);
                }

                // Delete the duplicate
                $db->delete('riders', 'id = ?', [$removeId]);

                $db->commit();
                $mergeCount++;
            } catch (Exception $e) {
                try { $db->rollback(); } catch (Exception $re) {}
                $errorCount++;
            }
        }
    }

    $_SESSION['dup_message'] = "Klart! Slog ihop {$mergeCount} dubletter, flyttade {$totalResultsMoved} resultat." . ($errorCount > 0 ? " ({$errorCount} fel)" : "");
    $_SESSION['dup_message_type'] = $errorCount > 0 ? 'warning' : 'success';
    header('Location: /admin/find-duplicates.php');
    exit;
}

// Find potential duplicates - simple approach: same firstname+lastname
$potentialDuplicates = [];

$duplicateGroups = $db->getAll("
 SELECT firstname, lastname, COUNT(*) as cnt
 FROM riders
 WHERE firstname IS NOT NULL AND lastname IS NOT NULL
 GROUP BY LOWER(firstname), LOWER(lastname)
 HAVING cnt > 1
 ORDER BY cnt DESC
 LIMIT 100
");

// Batch load classes for multiple riders (called ONCE at the end)
function batchLoadRiderClasses($db, $riderIds) {
    if (empty($riderIds)) return [];

    $placeholders = implode(',', array_fill(0, count($riderIds), '?'));
    $classes = $db->getAll("
        SELECT res.cyclist_id, cl.name, cl.display_name
        FROM results res
        JOIN classes cl ON res.class_id = cl.id
        WHERE res.cyclist_id IN ($placeholders)
        GROUP BY res.cyclist_id, cl.id
        ORDER BY cl.sort_order
    ", $riderIds);

    $result = [];
    foreach ($classes as $c) {
        $riderId = $c['cyclist_id'];
        if (!isset($result[$riderId])) {
            $result[$riderId] = [];
        }
        if (count($result[$riderId]) < 5) {
            $result[$riderId][] = $c['display_name'] ?: $c['name'];
        }
    }
    return $result;
}

foreach ($duplicateGroups as $group) {
 // Get ALL riders with this name (increased limit to 20)
 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.birth_year, r.license_number,
  r.email, r.club_id, c.name as club_name,
  (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.firstname) = LOWER(?) AND LOWER(r.lastname) = LOWER(?)
 ORDER BY r.id
 LIMIT 20
", [$group['firstname'], $group['lastname']]);

 // Compare ALL pairs of riders in this group
 for ($i = 0; $i < count($riders); $i++) {
  for ($j = $i + 1; $j < count($riders); $j++) {
   $r1 = $riders[$i];
   $r2 = $riders[$j];

   // Check license types
   $uci1 = isRealUci($r1['license_number']) ? normalizeUci($r1['license_number']) : null;
   $uci2 = isRealUci($r2['license_number']) ? normalizeUci($r2['license_number']) : null;
   $isSwe1 = !empty($r1['license_number']) && strpos($r1['license_number'], 'SWE') === 0;
   $isSwe2 = !empty($r2['license_number']) && strpos($r2['license_number'], 'SWE') === 0;

   // Only skip if BOTH have real (non-SWE) UCI IDs and they're different
   if ($uci1 && $uci2 && $uci1 !== $uci2) {
     continue;
   }

   // Skip if this pair is marked as "not duplicates"
   $pairKey = getRiderPairKey($r1['id'], $r2['id']);
   if (in_array($pairKey, $ignoredDuplicates)) continue;

   // NOTE: We NO LONGER skip based on different birth years - show them all and let user decide

   // Check missing data
   $r1Missing = [];
   $r2Missing = [];
   if (!$r1['birth_year'] && $r2['birth_year']) $r1Missing[] = 'födelseår';
   if (!$r2['birth_year'] && $r1['birth_year']) $r2Missing[] = 'födelseår';
   // Mark SWE-ID as missing real UCI when comparing to UCI profile
   if ($isSwe1 && $uci2) $r1Missing[] = 'UCI ID (har SWE-ID)';
   elseif (!$uci1 && $uci2) $r1Missing[] = 'UCI ID';
   if ($isSwe2 && $uci1) $r2Missing[] = 'UCI ID (har SWE-ID)';
   elseif (!$uci2 && $uci1) $r2Missing[] = 'UCI ID';
   if (!$r1['email'] && $r2['email']) $r1Missing[] = 'e-post';
   if (!$r2['email'] && $r1['email']) $r2Missing[] = 'e-post';

   $sameUci = $uci1 && $uci2 && $uci1 === $uci2;

   // Determine reason for showing as duplicates
   $reason = 'Exakt samma namn';
   if ($sameUci) {
    $reason = 'Samma UCI ID';
   } elseif ($r1['birth_year'] && $r2['birth_year'] && $r1['birth_year'] !== $r2['birth_year']) {
    $reason = 'Samma namn, olika födelseår (' . $r1['birth_year'] . ' vs ' . $r2['birth_year'] . ')';
   }

   // Always show duplicates with same name (classes loaded later in batch)
   $potentialDuplicates[] = [
    'pair_key' => $pairKey,
    'reason' => $reason,
    'rider1' => ['id' => $r1['id'], 'name' => $r1['firstname'].' '.$r1['lastname'],
     'birth_year' => $r1['birth_year'], 'license' => $r1['license_number'],
     'email' => $r1['email'], 'club' => $r1['club_name'], 'missing' => $r1Missing,
     'results' => $r1['result_count'] ?? 0],
    'rider2' => ['id' => $r2['id'], 'name' => $r2['firstname'].' '.$r2['lastname'],
     'birth_year' => $r2['birth_year'], 'license' => $r2['license_number'],
     'email' => $r2['email'], 'club' => $r2['club_name'], 'missing' => $r2Missing,
     'results' => $r2['result_count'] ?? 0]
   ];
  }
 }
}

// Find fuzzy duplicates - similar first names with same last name (e.g. Lucas/Lukas Wibäck)
$seenPairs = []; // Track pairs we've already added
foreach ($potentialDuplicates as $dup) {
    $seenPairs[$dup['rider1']['id'] . '-' . $dup['rider2']['id']] = true;
    $seenPairs[$dup['rider2']['id'] . '-' . $dup['rider1']['id']] = true;
}

// === NEW: Find double last name duplicates ===
// E.g. "Anna Andersson" vs "Anna Andersson Berg"
// Get riders with potential double names (space/hyphen in name, or long lastname)
$doubleNameRiders = $db->getAll("
    SELECT r.id, r.firstname, r.lastname, r.birth_year, r.license_number,
        r.email, r.club_id, c.name as club_name,
        (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.firstname IS NOT NULL AND r.lastname IS NOT NULL
      AND (
        r.lastname LIKE '% %' OR r.lastname LIKE '%-%'
        OR r.firstname LIKE '% %' OR r.firstname LIKE '%-%'
      )
    ORDER BY r.lastname, r.firstname
    LIMIT 500
");

// For each double-name rider, find potential matches with similar names
$checkedPairs = [];
foreach ($doubleNameRiders as $r1) {
    $fn1 = mb_strtolower(trim($r1['firstname']), 'UTF-8');
    $ln1 = mb_strtolower(trim($r1['lastname']), 'UTF-8');
    $fn1Norm = str_replace('-', ' ', $fn1);
    $fn1Compact = str_replace(['-', ' '], '', $fn1);

    // Extract lastname parts for matching
    $ln1Parts = preg_split('/[\s-]+/', $ln1);
    $ln1First = $ln1Parts[0] ?? '';

    // Find riders with matching first name and partial lastname match
    $potentialMatches = $db->getAll("
        SELECT r.id, r.firstname, r.lastname, r.birth_year, r.license_number,
            r.email, r.club_id, c.name as club_name,
            (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id != ?
          AND (
            LOWER(r.firstname) = ? OR LOWER(r.firstname) = ?
            OR REPLACE(REPLACE(LOWER(r.firstname), '-', ''), ' ', '') = ?
          )
          AND (
            LOWER(r.lastname) LIKE ? OR ? LIKE CONCAT('%', LOWER(r.lastname), '%')
          )
        LIMIT 20
    ", [$r1['id'], $fn1, $fn1Norm, $fn1Compact, '%' . $ln1First . '%', $ln1]);

    foreach ($potentialMatches as $r2) {
        $pairKey = getRiderPairKey($r1['id'], $r2['id']);
        if (isset($checkedPairs[$pairKey])) continue;
        if (isset($seenPairs[$pairKey])) continue;
        if (in_array($pairKey, $ignoredDuplicates)) continue;
        $checkedPairs[$pairKey] = true;

        $fn2 = mb_strtolower(trim($r2['firstname']), 'UTF-8');
        $ln2 = mb_strtolower(trim($r2['lastname']), 'UTF-8');
        $fn2Norm = str_replace('-', ' ', $fn2);

        $isDuplicate = false;
        $reason = '';

        // Check 1: Same firstname, one lastname contains the other (double name)
        // E.g. "Anna Andersson" vs "Anna Andersson Berg"
        if ($fn1Norm === $fn2Norm || $fn1 === $fn2) {
            if (mb_strlen($ln1, 'UTF-8') >= 3 && mb_strlen($ln2, 'UTF-8') >= 3) {
                if ($ln1 !== $ln2 && (mb_strpos($ln1, $ln2) !== false || mb_strpos($ln2, $ln1) !== false)) {
                    $isDuplicate = true;
                    $reason = 'Dubbelnamn? (' . $r1['lastname'] . ' / ' . $r2['lastname'] . ')';
                }
            }
        }

        // Check 2: Similar firstname (hyphen vs space), same lastname
        // E.g. "Anna-Maria Svensson" vs "Anna Maria Svensson"
        if (!$isDuplicate && $ln1 === $ln2) {
            $fn1Clean = str_replace(['-', ' '], '', $fn1);
            $fn2Clean = str_replace(['-', ' '], '', $fn2);
            if ($fn1Clean === $fn2Clean && $fn1 !== $fn2) {
                $isDuplicate = true;
                $reason = 'Samma namn, olika stavning (' . $r1['firstname'] . ' / ' . $r2['firstname'] . ')';
            }
        }

        // Check 3: One firstname contains the other, same lastname
        // E.g. "Anna Svensson" vs "Anna-Maria Svensson"
        if (!$isDuplicate && $ln1 === $ln2) {
            if (mb_strlen($fn1, 'UTF-8') >= 3 && mb_strlen($fn2, 'UTF-8') >= 3) {
                if ($fn1 !== $fn2 && (mb_strpos($fn1, $fn2) !== false || mb_strpos($fn2, $fn1) !== false)) {
                    $isDuplicate = true;
                    $reason = 'Förnamn innehåller varandra (' . $r1['firstname'] . ' / ' . $r2['firstname'] . ')';
                }
            }
        }

        // Check 4: Same firstname, similar lastnames (one word difference)
        // E.g. "Erik von Ansen" vs "Erik Ansen"
        if (!$isDuplicate && ($fn1 === $fn2 || $fn1Norm === $fn2Norm)) {
            $ln1Parts = preg_split('/[\s-]+/', $ln1);
            $ln2Parts = preg_split('/[\s-]+/', $ln2);
            // Check if one is subset of other (ignoring noble prefixes)
            $noblePrefixes = ['von', 'af', 'de', 'van', 'der', 'la'];
            $ln1Core = array_diff($ln1Parts, $noblePrefixes);
            $ln2Core = array_diff($ln2Parts, $noblePrefixes);
            if (!empty($ln1Core) && !empty($ln2Core) && $ln1Core != $ln2Core) {
                $intersection = array_intersect($ln1Core, $ln2Core);
                if (!empty($intersection) && (count($intersection) >= count($ln1Core) - 1 || count($intersection) >= count($ln2Core) - 1)) {
                    $isDuplicate = true;
                    $reason = 'Liknande efternamn (' . $r1['lastname'] . ' / ' . $r2['lastname'] . ')';
                }
            }
        }

        if (!$isDuplicate) continue;

        // Skip if different UCI IDs
        $uci1 = isRealUci($r1['license_number']) ? normalizeUci($r1['license_number']) : null;
        $uci2 = isRealUci($r2['license_number']) ? normalizeUci($r2['license_number']) : null;
        if ($uci1 && $uci2 && $uci1 !== $uci2) continue;

        $r1Missing = [];
        $r2Missing = [];
        $isSwe1 = !empty($r1['license_number']) && strpos($r1['license_number'], 'SWE') === 0;
        $isSwe2 = !empty($r2['license_number']) && strpos($r2['license_number'], 'SWE') === 0;

        if (!$r1['birth_year'] && $r2['birth_year']) $r1Missing[] = 'födelseår';
        if (!$r2['birth_year'] && $r1['birth_year']) $r2Missing[] = 'födelseår';
        if ($isSwe1 && $uci2) $r1Missing[] = 'UCI ID (har SWE-ID)';
        elseif (!$uci1 && $uci2) $r1Missing[] = 'UCI ID';
        if ($isSwe2 && $uci1) $r2Missing[] = 'UCI ID (har SWE-ID)';
        elseif (!$uci2 && $uci1) $r2Missing[] = 'UCI ID';

        $seenPairs[$pairKey] = true;
        $potentialDuplicates[] = [
            'pair_key' => $pairKey,
            'reason' => $reason,
            'rider1' => ['id' => $r1['id'], 'name' => $r1['firstname'].' '.$r1['lastname'],
                'birth_year' => $r1['birth_year'], 'license' => $r1['license_number'],
                'email' => $r1['email'], 'club' => $r1['club_name'], 'missing' => $r1Missing,
                'results' => $r1['result_count'] ?? 0],
            'rider2' => ['id' => $r2['id'], 'name' => $r2['firstname'].' '.$r2['lastname'],
                'birth_year' => $r2['birth_year'], 'license' => $r2['license_number'],
                'email' => $r2['email'], 'club' => $r2['club_name'], 'missing' => $r2Missing,
                'results' => $r2['result_count'] ?? 0]
        ];
    }
}

// Also find SOUNDEX fuzzy matches
$fuzzyGroups = $db->getAll("
    SELECT lastname, SOUNDEX(firstname) as fname_sound, COUNT(*) as cnt,
           GROUP_CONCAT(DISTINCT firstname SEPARATOR '|') as firstnames
    FROM riders
    WHERE firstname IS NOT NULL AND lastname IS NOT NULL
    GROUP BY LOWER(lastname), SOUNDEX(firstname)
    HAVING cnt > 1 AND COUNT(DISTINCT LOWER(firstname)) > 1
    ORDER BY cnt DESC
    LIMIT 100
");

foreach ($fuzzyGroups as $group) {
    $riders = $db->getAll("
        SELECT r.id, r.firstname, r.lastname, r.birth_year, r.license_number,
            r.email, r.club_id, c.name as club_name,
            (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE LOWER(r.lastname) = LOWER(?) AND SOUNDEX(r.firstname) = ?
        ORDER BY r.firstname
        LIMIT 10
    ", [$group['lastname'], $group['fname_sound']]);

    // Group riders by firstname and pick one from each unique firstname
    $byFirstname = [];
    foreach ($riders as $rider) {
        $fnLower = strtolower($rider['firstname']);
        if (!isset($byFirstname[$fnLower])) {
            $byFirstname[$fnLower] = $rider;
        }
    }

    $uniqueRiders = array_values($byFirstname);
    if (count($uniqueRiders) >= 2) {
        // Compare pairs of riders with different first names
        for ($i = 0; $i < count($uniqueRiders) - 1; $i++) {
            for ($j = $i + 1; $j < count($uniqueRiders); $j++) {
                $r1 = $uniqueRiders[$i];
                $r2 = $uniqueRiders[$j];

                // Skip if already in list
                $pairKey = getRiderPairKey($r1['id'], $r2['id']);
                if (isset($seenPairs[$pairKey])) continue;
                $seenPairs[$pairKey] = true;

                // Skip if this pair is marked as "not duplicates"
                if (in_array($pairKey, $ignoredDuplicates)) continue;

                // Skip if different birth year (when both have one)
                if ($r1['birth_year'] && $r2['birth_year'] && $r1['birth_year'] !== $r2['birth_year']) continue;

                $uci1 = isRealUci($r1['license_number']) ? normalizeUci($r1['license_number']) : null;
                $uci2 = isRealUci($r2['license_number']) ? normalizeUci($r2['license_number']) : null;

                // Skip if different UCI
                if ($uci1 && $uci2 && $uci1 !== $uci2) continue;

                $r1Missing = [];
                $r2Missing = [];
                if (!$r1['birth_year'] && $r2['birth_year']) $r1Missing[] = 'födelseår';
                if (!$r2['birth_year'] && $r1['birth_year']) $r2Missing[] = 'födelseår';
                if (!$uci1 && $uci2) $r1Missing[] = 'UCI ID';
                if (!$uci2 && $uci1) $r2Missing[] = 'UCI ID';

                $potentialDuplicates[] = [
                    'pair_key' => $pairKey,
                    'reason' => 'Liknande namn (' . $r1['firstname'] . '/' . $r2['firstname'] . ')',
                    'rider1' => ['id' => $r1['id'], 'name' => $r1['firstname'].' '.$r1['lastname'],
                        'birth_year' => $r1['birth_year'], 'license' => $r1['license_number'],
                        'email' => $r1['email'], 'club' => $r1['club_name'], 'missing' => $r1Missing,
                        'results' => $r1['result_count'] ?? 0],
                    'rider2' => ['id' => $r2['id'], 'name' => $r2['firstname'].' '.$r2['lastname'],
                        'birth_year' => $r2['birth_year'], 'license' => $r2['license_number'],
                        'email' => $r2['email'], 'club' => $r2['club_name'], 'missing' => $r2Missing,
                        'results' => $r2['result_count'] ?? 0]
                ];
            }
        }
    }
}

// === NEW: Find nickname/similar first name duplicates ===
// Catches cases like "Oliver Barton" vs "Ollie Barton" that SOUNDEX misses
$allLastnames = $db->getAll("
    SELECT LOWER(lastname) as ln, COUNT(*) as cnt
    FROM riders
    WHERE firstname IS NOT NULL AND lastname IS NOT NULL
    GROUP BY LOWER(lastname)
    HAVING cnt >= 2 AND cnt <= 20
    ORDER BY cnt DESC
    LIMIT 200
");

foreach ($allLastnames as $lnGroup) {
    $ridersWithSameLn = $db->getAll("
        SELECT r.id, r.firstname, r.lastname, r.birth_year, r.license_number,
            r.email, r.club_id, c.name as club_name,
            (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE LOWER(r.lastname) = ?
        ORDER BY r.firstname
    ", [$lnGroup['ln']]);

    // Compare all pairs for Levenshtein similarity in first names
    for ($i = 0; $i < count($ridersWithSameLn) - 1; $i++) {
        for ($j = $i + 1; $j < count($ridersWithSameLn); $j++) {
            $r1 = $ridersWithSameLn[$i];
            $r2 = $ridersWithSameLn[$j];

            $fn1 = mb_strtolower(trim($r1['firstname']), 'UTF-8');
            $fn2 = mb_strtolower(trim($r2['firstname']), 'UTF-8');

            // Skip if same firstname (already caught by exact match)
            if ($fn1 === $fn2) continue;

            $pairKey = getRiderPairKey($r1['id'], $r2['id']);
            if (isset($seenPairs[$pairKey])) continue;
            if (in_array($pairKey, $ignoredDuplicates)) continue;

            // Check if one name starts with the other (Oliver/Ollie, Alexander/Alex)
            $isNickname = false;
            $shorterName = strlen($fn1) < strlen($fn2) ? $fn1 : $fn2;
            $longerName = strlen($fn1) < strlen($fn2) ? $fn2 : $fn1;

            // One name starts with the other (min 3 chars)
            if (strlen($shorterName) >= 3 && strpos($longerName, $shorterName) === 0) {
                $isNickname = true;
            }

            // Check Levenshtein distance (for names like Olle/Ollie, Erik/Eric)
            if (!$isNickname && strlen($fn1) >= 3 && strlen($fn2) >= 3) {
                $distance = levenshtein($fn1, $fn2);
                $maxLen = max(strlen($fn1), strlen($fn2));
                // Allow up to 2 edits for short names, or 30% difference for longer names
                if ($distance <= 2 || ($distance / $maxLen) <= 0.3) {
                    $isNickname = true;
                }
            }

            if (!$isNickname) continue;

            // Skip if different UCI IDs (both real)
            $uci1 = isRealUci($r1['license_number']) ? normalizeUci($r1['license_number']) : null;
            $uci2 = isRealUci($r2['license_number']) ? normalizeUci($r2['license_number']) : null;
            if ($uci1 && $uci2 && $uci1 !== $uci2) continue;

            $seenPairs[$pairKey] = true;

            $r1Missing = [];
            $r2Missing = [];
            $isSwe1 = !empty($r1['license_number']) && strpos($r1['license_number'], 'SWE') === 0;
            $isSwe2 = !empty($r2['license_number']) && strpos($r2['license_number'], 'SWE') === 0;

            if (!$r1['birth_year'] && $r2['birth_year']) $r1Missing[] = 'födelseår';
            if (!$r2['birth_year'] && $r1['birth_year']) $r2Missing[] = 'födelseår';
            if ($isSwe1 && $uci2) $r1Missing[] = 'UCI ID (har SWE-ID)';
            elseif (!$uci1 && $uci2) $r1Missing[] = 'UCI ID';
            if ($isSwe2 && $uci1) $r2Missing[] = 'UCI ID (har SWE-ID)';
            elseif (!$uci2 && $uci1) $r2Missing[] = 'UCI ID';

            // Determine reason
            $reason = 'Smeknamn? (' . $r1['firstname'] . '/' . $r2['firstname'] . ')';
            if ($r1['birth_year'] && $r2['birth_year'] && $r1['birth_year'] !== $r2['birth_year']) {
                $reason = 'Liknande namn, OLIKA födelseår (' . $r1['birth_year'] . '/' . $r2['birth_year'] . ')';
            }

            $potentialDuplicates[] = [
                'pair_key' => $pairKey,
                'reason' => $reason,
                'rider1' => ['id' => $r1['id'], 'name' => $r1['firstname'].' '.$r1['lastname'],
                    'birth_year' => $r1['birth_year'], 'license' => $r1['license_number'],
                    'email' => $r1['email'], 'club' => $r1['club_name'], 'missing' => $r1Missing,
                    'results' => $r1['result_count'] ?? 0],
                'rider2' => ['id' => $r2['id'], 'name' => $r2['firstname'].' '.$r2['lastname'],
                    'birth_year' => $r2['birth_year'], 'license' => $r2['license_number'],
                    'email' => $r2['email'], 'club' => $r2['club_name'], 'missing' => $r2Missing,
                    'results' => $r2['result_count'] ?? 0]
            ];
        }
    }
}

// BATCH LOAD all rider classes in ONE query (performance optimization)
$allRiderIds = [];
foreach ($potentialDuplicates as $dup) {
    $allRiderIds[] = $dup['rider1']['id'];
    $allRiderIds[] = $dup['rider2']['id'];
}
$allRiderIds = array_unique($allRiderIds);
$riderClassesMap = batchLoadRiderClasses($db, $allRiderIds);

// Add classes to duplicates
foreach ($potentialDuplicates as &$dup) {
    $dup['rider1']['classes'] = $riderClassesMap[$dup['rider1']['id']] ?? [];
    $dup['rider2']['classes'] = $riderClassesMap[$dup['rider2']['id']] ?? [];
}
unset($dup);

// Page config for unified layout
$page_title = 'Hitta Dubbletter';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Hitta Dubbletter']
];

include __DIR__ . '/components/unified-layout.php';
?>

 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>


 <?php $ignoredCount = count($ignoredDuplicates); ?>
 <?php if ($ignoredCount > 0): ?>
  <!-- Ignored pairs info -->
  <div class="card mb-lg" style="background: var(--color-bg-sunken, #f5f5f5);">
   <div class="card-body flex items-center justify-between">
    <div>
     <strong class="text-secondary"><i data-lucide="eye-off" class="icon-sm"></i> <?= $ignoredCount ?> par dolda</strong>
     <p class="text-sm text-secondary gs-mb-0">Par markerade som "inte dubbletter"</p>
    </div>
    <form method="POST">
     <?= csrf_field() ?>
     <button type="submit" name="reset_ignored" value="1" class="btn btn--secondary btn--sm"
      onclick="return confirm('Återställa alla dolda par?')">
      <i data-lucide="refresh-cw"></i>
      Visa alla igen
     </button>
    </form>
   </div>
  </div>
 <?php endif; ?>

 <div class="card">
  <div class="card-header flex justify-between items-center">
  <h2 class="">
   <i data-lucide="users"></i>
   Potentiella dubbletter (<?= count($potentialDuplicates) ?>)
  </h2>
  <?php if (!empty($potentialDuplicates)): ?>
  <form method="POST" style="display: inline;">
   <?= csrf_field() ?>
   <button type="submit" name="merge_all" class="btn btn-danger"
           onclick="return confirm('Slå ihop dubbletter automatiskt?\n\nDen bästa profilen (flest resultat/data) behålls.\n\nHOPPAS ÖVER:\n- Par med olika UCI-ID\n- Par med olika födelseår\n- Ignorerade par')">
    <i data-lucide="git-merge"></i>
    Slå ihop säkra
   </button>
  </form>
  <?php endif; ?>
  </div>
  <div class="card-body">
  <?php if (empty($potentialDuplicates)): ?>
   <div class="text-center py-lg">
   <i data-lucide="check-circle" class="text-success" style="width: 48px; height: 48px;"></i>
   <p class="text-success mt-md">Inga potentiella dubbletter hittades!</p>
   </div>
  <?php else: ?>
   <?php foreach ($potentialDuplicates as $idx => $dup):
   // Check if this pair has different birth years
   $hasDifferentBirthYears = !empty($dup['rider1']['birth_year']) && !empty($dup['rider2']['birth_year'])
                             && $dup['rider1']['birth_year'] !== $dup['rider2']['birth_year'];
   $borderColor = $hasDifferentBirthYears ? '#dc3545' : '#ffc107';
   $bgColor = $hasDifferentBirthYears ? 'rgba(220,53,69,0.15)' : 'rgba(255,193,7,0.15)';
   ?>
   <div id="dup-pair-<?= $idx ?>" data-pair-key="<?= h($dup['pair_key']) ?>" style="border: 2px solid <?= $borderColor ?>; border-radius: 8px; margin-bottom: 1rem; overflow: hidden;">
   <?php if ($hasDifferentBirthYears): ?>
   <div style="background: #dc3545; color: white; padding: 0.5rem 1rem; font-weight: bold;">
    <i data-lucide="alert-triangle" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle;"></i>
    VARNING: Olika födelseår (<?= $dup['rider1']['birth_year'] ?> vs <?= $dup['rider2']['birth_year'] ?>) - Kan vara olika personer!
   </div>
   <?php endif; ?>
   <div class="flex justify-between items-center" style="background: <?= $bgColor ?>; padding: 0.5rem 1rem;">
    <span class="badge <?= $dup['reason'] === 'Samma UCI ID' ? 'badge-danger' : ($hasDifferentBirthYears ? 'badge-danger' : 'badge-warning') ?>">
    <?= h($dup['reason']) ?>
    </span>
    <span class="text-secondary text-sm">#<?= $idx + 1 ?></span>
   </div>
   <div class="flex gap-md flex-wrap" style="padding: 1rem;">
    <?php foreach (['rider1', 'rider2'] as $key):
    $rider = $dup[$key];
    $isComplete = empty($rider['missing']);
    $borderColor = $isComplete ? '#28a745' : '#dc3545';
    $bgColor = $isComplete ? 'rgba(40,167,69,0.08)' : 'rgba(220,53,69,0.08)';
    ?>
    <div class="flex-1" style="min-width: 280px; padding: 1rem; background: <?= $bgColor ?>; border: 2px solid <?= $borderColor ?>; border-radius: 8px;">
    <div class="flex justify-between mb-sm">
     <div>
     <strong style="font-size: 1.1rem;"><?= h($rider['name']) ?></strong>
     <div class="text-xs text-secondary">ID: <?= $rider['id'] ?></div>
     </div>
     <span class="badge badge-secondary"><?= $rider['results'] ?> resultat</span>
    </div>

    <?php if (!empty($rider['missing'])): ?>
    <div class="mb-sm text-sm" style="background: rgba(255,193,7,0.2); padding: 0.5rem; border-radius: 4px;">
     <strong>Saknar:</strong> <?= implode(', ', $rider['missing']) ?>
    </div>
    <?php endif; ?>

    <table class="w-full text-sm">
     <tr>
     <td class="text-secondary" style="width: 80px;">Födelseår:</td>
     <td><?= $rider['birth_year'] ?: '<span class="text-error">-</span>' ?></td>
     </tr>
     <tr>
     <td class="text-secondary">License:</td>
     <td><code><?= h($rider['license'] ?: '-') ?></code></td>
     </tr>
     <tr>
     <td class="text-secondary">Klubb:</td>
     <td><?= h($rider['club'] ?: '-') ?></td>
     </tr>
     <tr>
     <td class="text-secondary">E-post:</td>
     <td><?= h($rider['email'] ?: '-') ?></td>
     </tr>
     <tr>
     <td class="text-secondary">Klasser:</td>
     <td><?php if (!empty($rider['classes'])): ?>
      <?php foreach ($rider['classes'] as $cls): ?>
       <span class="badge badge-secondary" style="font-size: 0.7rem; margin-right: 2px;"><?= h($cls) ?></span>
      <?php endforeach; ?>
     <?php else: ?>
      <span style="color: #999;">-</span>
     <?php endif; ?></td>
     </tr>
    </table>

    <div class="flex gap-sm mt-md">
     <a href="/rider/<?= $rider['id'] ?>" target="_blank" class="btn btn--sm btn--secondary" title="Visa profil">
     <i data-lucide="external-link"></i>
     </a>
     <?php
     $otherId = $key === 'rider1' ? $dup['rider2']['id'] : $dup['rider1']['id'];
     $otherBirthYear = $key === 'rider1' ? $dup['rider2']['birth_year'] : $dup['rider1']['birth_year'];
     $confirmMsg = 'Behåll denna profil och ta bort den andra?\\n\\nResultat flyttas och data slås ihop.';
     if ($hasDifferentBirthYears) {
         $confirmMsg = 'VARNING: Olika födelseår!\\n\\n' . $rider['birth_year'] . ' vs ' . $otherBirthYear . '\\n\\nÄr du SÄKER på att detta är samma person?\\n\\nResultat flyttas och den andra profilen raderas permanent.';
     }
     ?>
     <button type="button"
     class="btn btn--sm <?= $hasDifferentBirthYears ? 'btn-warning' : 'btn-success' ?> flex-1 merge-btn"
     data-keep="<?= $rider['id'] ?>"
     data-remove="<?= $otherId ?>"
     data-pair-idx="<?= $idx ?>"
     data-confirm="<?= $confirmMsg ?>">
     <i data-lucide="check"></i> Behåll denna
     </button>
    </div>
    </div>
    <?php endforeach; ?>
   </div>
   <!-- Not duplicates button -->
   <div style="padding: 0 1rem 1rem; text-align: right;">
    <form method="POST" style="display: inline;">
     <?= csrf_field() ?>
     <button type="submit" name="ignore_pair" value="<?= h($dup['pair_key']) ?>" class="btn btn--secondary btn--sm">
      <i data-lucide="eye-off"></i>
      Inte dubbletter
     </button>
    </form>
   </div>
   </div>
   <?php endforeach; ?>
  <?php endif; ?>
  </div>
 </div>

<script>
// AJAX merge handling - no page reload
document.querySelectorAll('.merge-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const keepId = this.dataset.keep;
        const removeId = this.dataset.remove;
        const pairIdx = this.dataset.pairIdx;
        const confirmMsg = this.dataset.confirm;

        if (!confirm(confirmMsg.replace(/\\n/g, '\n'))) {
            return;
        }

        // Disable button and show loading
        this.disabled = true;
        const originalText = this.innerHTML;
        this.innerHTML = '<i data-lucide="loader-2" class="animate-spin"></i> Slår ihop...';

        try {
            const response = await fetch(`?action=merge&keep=${keepId}&remove=${removeId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                // Remove the card with animation
                const card = document.getElementById('dup-pair-' + pairIdx);
                if (card) {
                    card.style.transition = 'opacity 0.3s, transform 0.3s';
                    card.style.opacity = '0';
                    card.style.transform = 'translateX(-20px)';
                    setTimeout(() => {
                        card.remove();
                        // Update counter
                        const counter = document.querySelector('.card-header h2');
                        if (counter) {
                            const match = counter.textContent.match(/\((\d+)\)/);
                            if (match) {
                                const newCount = parseInt(match[1]) - 1;
                                counter.innerHTML = counter.innerHTML.replace(/\(\d+\)/, '(' + newCount + ')');
                            }
                        }
                    }, 300);
                }
                // Show toast message
                showToast(data.message, 'success');
            } else {
                showToast(data.message || 'Ett fel uppstod', 'error');
                this.disabled = false;
                this.innerHTML = originalText;
            }
        } catch (error) {
            showToast('Nätverksfel: ' + error.message, 'error');
            this.disabled = false;
            this.innerHTML = originalText;
        }
    });
});

// Simple toast notification
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
    .animate-spin { animation: spin 1s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
`;
document.head.appendChild(style);

// Re-init lucide icons after any DOM changes
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
