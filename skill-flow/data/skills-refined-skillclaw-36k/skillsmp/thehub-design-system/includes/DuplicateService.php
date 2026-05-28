<?php
/**
 * DuplicateService - Smart duplicate detection
 *
 * Features:
 * - Name normalization (Swedish characters, accents, etc.)
 * - Fingerprinting for fast candidate lookup
 * - Jaro-Winkler similarity scoring
 * - Configurable thresholds
 * - Merge tracking via rider_merge_map
 *
 * @package TheHUB
 * @version 1.0
 */

class DuplicateService
{
    private PDO $pdo;

    // Thresholds
    const SCORE_CERTAIN = 0.92;    // Nästan säkert dublett
    const SCORE_POSSIBLE = 0.80;   // Möjlig dublett
    const SCORE_IGNORE = 0.75;     // Ignorera under detta

    // Swedish character mappings
    private static array $charMap = [
        'å' => 'a', 'ä' => 'a', 'ö' => 'o',
        'Å' => 'a', 'Ä' => 'a', 'Ö' => 'o',
        'é' => 'e', 'è' => 'e', 'ê' => 'e', 'ë' => 'e',
        'á' => 'a', 'à' => 'a', 'â' => 'a',
        'ü' => 'u', 'ú' => 'u', 'ù' => 'u',
        'ï' => 'i', 'í' => 'i', 'ì' => 'i',
        'ñ' => 'n', 'ç' => 'c',
        'ø' => 'o', 'æ' => 'ae',
    ];

    public function __construct(PDO $pdo)
    {
        $this->pdo = $pdo;
    }

    /**
     * Normalize a name for comparison
     */
    public function normalizeName(string $name): string
    {
        // Lowercase
        $name = mb_strtolower(trim($name), 'UTF-8');

        // Replace Swedish/special characters
        $name = strtr($name, self::$charMap);

        // Remove hyphens, apostrophes, dots
        $name = str_replace(['-', "'", "\u{2019}", '.', ','], ' ', $name);

        // Collapse multiple spaces
        $name = preg_replace('/\s+/', ' ', $name);

        // Remove leading/trailing
        return trim($name);
    }

    /**
     * Create fingerprint for fast lookup
     * Format: first3(firstname) + first5(lastname) [+ birthyear if available]
     */
    public function fingerprint(string $firstName, string $lastName, ?int $birthYear = null): string
    {
        $normFirst = $this->normalizeName($firstName);
        $normLast = $this->normalizeName($lastName);

        $fp = substr($normFirst, 0, 3) . substr($normLast, 0, 5);

        if ($birthYear) {
            $fp .= '_' . $birthYear;
        }

        return $fp;
    }

    /**
     * Calculate Jaro similarity between two strings
     */
    private function jaroSimilarity(string $s1, string $s2): float
    {
        $len1 = mb_strlen($s1);
        $len2 = mb_strlen($s2);

        if ($len1 === 0 && $len2 === 0) return 1.0;
        if ($len1 === 0 || $len2 === 0) return 0.0;

        $matchDistance = max($len1, $len2) / 2 - 1;
        $matchDistance = max(0, (int)$matchDistance);

        $s1Matches = array_fill(0, $len1, false);
        $s2Matches = array_fill(0, $len2, false);

        $matches = 0;
        $transpositions = 0;

        // Find matches
        for ($i = 0; $i < $len1; $i++) {
            $start = max(0, $i - $matchDistance);
            $end = min($i + $matchDistance + 1, $len2);

            for ($j = $start; $j < $end; $j++) {
                if ($s2Matches[$j] || mb_substr($s1, $i, 1) !== mb_substr($s2, $j, 1)) {
                    continue;
                }
                $s1Matches[$i] = true;
                $s2Matches[$j] = true;
                $matches++;
                break;
            }
        }

        if ($matches === 0) return 0.0;

        // Count transpositions
        $k = 0;
        for ($i = 0; $i < $len1; $i++) {
            if (!$s1Matches[$i]) continue;

            while (!$s2Matches[$k]) $k++;

            if (mb_substr($s1, $i, 1) !== mb_substr($s2, $k, 1)) {
                $transpositions++;
            }
            $k++;
        }

        return (($matches / $len1) + ($matches / $len2) +
                (($matches - $transpositions / 2) / $matches)) / 3;
    }

    /**
     * Calculate Jaro-Winkler similarity (better for names)
     */
    public function jaroWinkler(string $s1, string $s2): float
    {
        $jaro = $this->jaroSimilarity($s1, $s2);

        // Find common prefix (max 4 chars)
        $prefixLen = 0;
        $maxPrefix = min(4, min(mb_strlen($s1), mb_strlen($s2)));

        for ($i = 0; $i < $maxPrefix; $i++) {
            if (mb_substr($s1, $i, 1) === mb_substr($s2, $i, 1)) {
                $prefixLen++;
            } else {
                break;
            }
        }

        // Winkler modification (prefix scaling factor 0.1)
        return $jaro + ($prefixLen * 0.1 * (1 - $jaro));
    }

    /**
     * Score a potential duplicate pair
     *
     * Returns array with:
     * - score: 0-1 overall similarity
     * - reasons: array of matching reasons
     * - certain: bool if score >= SCORE_CERTAIN
     */
    public function scorePair(array $a, array $b): array
    {
        $score = 0.0;
        $reasons = [];

        // Normalize names
        $nameA = $this->normalizeName($a['firstname'] . ' ' . $a['lastname']);
        $nameB = $this->normalizeName($b['firstname'] . ' ' . $b['lastname']);

        // Name similarity (Jaro-Winkler)
        $nameSim = $this->jaroWinkler($nameA, $nameB);
        $score = $nameSim;

        if ($nameSim >= 0.95) {
            $reasons[] = 'Mycket lika namn';
        } elseif ($nameSim >= 0.85) {
            $reasons[] = 'Liknande namn';
        }

        // UCI ID match = 100% certain
        $uciA = $this->extractUciId($a['license_number'] ?? '');
        $uciB = $this->extractUciId($b['license_number'] ?? '');

        if ($uciA && $uciB) {
            if ($uciA === $uciB) {
                $score = 1.0;
                $reasons = ['Samma UCI ID'];
            } else {
                // Different UCI IDs = definitely NOT same person
                return [
                    'score' => 0.0,
                    'reasons' => ['Olika UCI ID - ej dublett'],
                    'certain' => false,
                    'conflict' => 'uci_id'
                ];
            }
        }

        // Birth year bonus/penalty
        $byA = $a['birth_year'] ?? null;
        $byB = $b['birth_year'] ?? null;

        if ($byA && $byB) {
            if ($byA === $byB) {
                $score = min(1.0, $score + 0.1);
                $reasons[] = 'Samma födelseår';
            } else {
                // Different birth years = very unlikely same person
                $score = max(0, $score - 0.3);
                $reasons[] = "Olika födelseår ({$byA} vs {$byB})";

                return [
                    'score' => $score,
                    'reasons' => $reasons,
                    'certain' => false,
                    'conflict' => 'birth_year'
                ];
            }
        }

        // Club match bonus
        if (!empty($a['club_id']) && !empty($b['club_id']) && $a['club_id'] === $b['club_id']) {
            $score = min(1.0, $score + 0.05);
            $reasons[] = 'Samma klubb';
        }

        // One has data the other lacks = likely duplicate
        $aHasData = !empty($a['birth_year']) || !empty($uciA) || !empty($a['email']);
        $bHasData = !empty($b['birth_year']) || !empty($uciB) || !empty($b['email']);

        if ($aHasData xor $bHasData) {
            $reasons[] = 'En profil har mer data';
        }

        return [
            'score' => round($score, 3),
            'reasons' => $reasons,
            'certain' => $score >= self::SCORE_CERTAIN,
            'possible' => $score >= self::SCORE_POSSIBLE,
            'conflict' => null
        ];
    }

    /**
     * Extract real UCI ID (not SWE-generated)
     */
    private function extractUciId(?string $license): ?string
    {
        if (!$license) return null;
        $license = trim($license);

        // SWE-IDs are generated, not real UCI
        if (strpos($license, 'SWE') === 0) {
            return null;
        }

        return preg_replace('/\s+/', '', $license) ?: null;
    }

    /**
     * Find duplicate candidates for a rider
     */
    public function findCandidates(int $riderId, int $limit = 50): array
    {
        // Get the rider
        $stmt = $this->pdo->prepare("
            SELECT id, firstname, lastname, birth_year, license_number, club_id, email
            FROM riders WHERE id = ?
        ");
        $stmt->execute([$riderId]);
        $rider = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$rider) return [];

        $fp = $this->fingerprint($rider['firstname'], $rider['lastname']);
        $normName = $this->normalizeName($rider['firstname'] . ' ' . $rider['lastname']);

        // Find candidates with similar fingerprint or same normalized name start
        $stmt = $this->pdo->prepare("
            SELECT id, firstname, lastname, birth_year, license_number, club_id, email,
                   (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
            FROM riders r
            WHERE id != ?
              AND (
                -- Same fingerprint base (first 8 chars)
                LEFT(LOWER(CONCAT(
                    LEFT(firstname, 3),
                    LEFT(lastname, 5)
                )), 8) = LEFT(?, 8)
                -- Or same last name
                OR LOWER(lastname) = LOWER(?)
                -- Or very similar first few chars
                OR SOUNDEX(CONCAT(firstname, ' ', lastname)) = SOUNDEX(?)
              )
            ORDER BY
                CASE WHEN birth_year = ? THEN 0 ELSE 1 END,
                lastname, firstname
            LIMIT ?
        ");

        $stmt->execute([
            $riderId,
            $fp,
            $rider['lastname'],
            $rider['firstname'] . ' ' . $rider['lastname'],
            $rider['birth_year'],
            $limit
        ]);

        $candidates = [];
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $scoreData = $this->scorePair($rider, $row);

            if ($scoreData['score'] >= self::SCORE_IGNORE) {
                $candidates[] = [
                    'rider' => $row,
                    'score' => $scoreData['score'],
                    'reasons' => $scoreData['reasons'],
                    'certain' => $scoreData['certain'],
                    'conflict' => $scoreData['conflict'] ?? null
                ];
            }
        }

        // Sort by score descending
        usort($candidates, fn($a, $b) => $b['score'] <=> $a['score']);

        return $candidates;
    }

    /**
     * Find all duplicate groups
     */
    public function findAllDuplicates(int $limit = 200): array
    {
        $groups = [];
        $processed = [];

        // First: exact name matches (fastest, most reliable)
        $stmt = $this->pdo->query("
            SELECT
                LOWER(CONCAT(firstname, ' ', lastname)) as name_key,
                GROUP_CONCAT(id ORDER BY id) as ids,
                COUNT(*) as cnt
            FROM riders
            WHERE firstname IS NOT NULL AND lastname IS NOT NULL
              AND firstname != '' AND lastname != ''
            GROUP BY LOWER(CONCAT(firstname, ' ', lastname))
            HAVING cnt > 1
            ORDER BY cnt DESC
            LIMIT {$limit}
        ");

        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $ids = explode(',', $row['ids']);

            // Get full rider data
            $placeholders = implode(',', array_fill(0, count($ids), '?'));
            $riderStmt = $this->pdo->prepare("
                SELECT r.*, c.name as club_name,
                       (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE r.id IN ($placeholders)
                ORDER BY r.id
            ");
            $riderStmt->execute($ids);
            $riders = $riderStmt->fetchAll(PDO::FETCH_ASSOC);

            if (count($riders) < 2) continue;

            // Score pairs
            $pairs = [];
            for ($i = 0; $i < count($riders) - 1; $i++) {
                for ($j = $i + 1; $j < count($riders); $j++) {
                    $scoreData = $this->scorePair($riders[$i], $riders[$j]);
                    $pairs[] = [
                        'rider1' => $riders[$i],
                        'rider2' => $riders[$j],
                        'score' => $scoreData['score'],
                        'reasons' => $scoreData['reasons'],
                        'conflict' => $scoreData['conflict'] ?? null,
                        'certain' => $scoreData['certain'] ?? false
                    ];
                }
            }

            if (!empty($pairs)) {
                $groups[] = [
                    'name' => $riders[0]['firstname'] . ' ' . $riders[0]['lastname'],
                    'count' => count($riders),
                    'riders' => $riders,
                    'pairs' => $pairs,
                    'max_score' => max(array_column($pairs, 'score'))
                ];
            }

            foreach ($ids as $id) {
                $processed[$id] = true;
            }
        }

        // Sort groups by max score
        usort($groups, fn($a, $b) => $b['max_score'] <=> $a['max_score']);

        return $groups;
    }

    /**
     * Merge two riders (keep one, delete other)
     */
    public function merge(int $keepId, int $removeId, ?int $userId = null): array
    {
        $stats = ['results_moved' => 0, 'results_deleted' => 0, 'fields_updated' => []];

        try {
            $this->pdo->beginTransaction();

            // Get both riders
            $stmt = $this->pdo->prepare("SELECT * FROM riders WHERE id IN (?, ?)");
            $stmt->execute([$keepId, $removeId]);
            $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

            $keep = $remove = null;
            foreach ($riders as $r) {
                if ($r['id'] == $keepId) $keep = $r;
                if ($r['id'] == $removeId) $remove = $r;
            }

            if (!$keep || !$remove) {
                throw new Exception("Rider not found");
            }

            // Move results
            $stmt = $this->pdo->prepare("SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?");
            $stmt->execute([$removeId]);
            $resultsToMove = $stmt->fetchAll(PDO::FETCH_ASSOC);

            foreach ($resultsToMove as $result) {
                // Check for conflict
                $checkStmt = $this->pdo->prepare("
                    SELECT id FROM results
                    WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?
                ");
                $checkStmt->execute([$keepId, $result['event_id'], $result['class_id']]);

                if ($checkStmt->fetch()) {
                    // Delete duplicate result
                    $this->pdo->prepare("DELETE FROM results WHERE id = ?")->execute([$result['id']]);
                    $stats['results_deleted']++;
                } else {
                    // Move result
                    $this->pdo->prepare("UPDATE results SET cyclist_id = ? WHERE id = ?")
                        ->execute([$keepId, $result['id']]);
                    $stats['results_moved']++;
                }
            }

            // Move series_results
            $this->pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?")
                ->execute([$keepId, $removeId]);

            // Update keep rider with missing data from remove
            $updates = [];
            $fields = ['birth_year', 'email', 'phone', 'club_id', 'gender'];

            foreach ($fields as $field) {
                if (empty($keep[$field]) && !empty($remove[$field])) {
                    $updates[$field] = $remove[$field];
                    $stats['fields_updated'][] = $field;
                }
            }

            // Prefer real UCI ID
            if (!empty($remove['license_number'])) {
                $keepIsSwe = empty($keep['license_number']) || strpos($keep['license_number'], 'SWE') === 0;
                $removeIsUci = strpos($remove['license_number'], 'SWE') !== 0;

                if ($keepIsSwe && $removeIsUci) {
                    $updates['license_number'] = $remove['license_number'];
                    $stats['fields_updated'][] = 'license_number';
                }
            }

            if (!empty($updates)) {
                $setClauses = [];
                $params = [];
                foreach ($updates as $col => $val) {
                    $setClauses[] = "$col = ?";
                    $params[] = $val;
                }
                $params[] = $keepId;
                $this->pdo->prepare("UPDATE riders SET " . implode(', ', $setClauses) . " WHERE id = ?")
                    ->execute($params);
            }

            // Record merge
            try {
                $this->pdo->prepare("
                    INSERT INTO rider_merge_map
                    (canonical_rider_id, merged_rider_id, reason, confidence, status, merged_by)
                    VALUES (?, ?, 'duplicate_service', 100, 'approved', ?)
                    ON DUPLICATE KEY UPDATE
                        canonical_rider_id = VALUES(canonical_rider_id),
                        merged_at = CURRENT_TIMESTAMP
                ")->execute([$keepId, $removeId, $userId]);
            } catch (Exception $e) {
                // Table might not exist
            }

            // Delete the duplicate
            $this->pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$removeId]);

            $this->pdo->commit();

            $stats['success'] = true;
            $stats['keep'] = $keep;
            $stats['removed'] = $remove;

            return $stats;

        } catch (Exception $e) {
            $this->pdo->rollBack();
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Check if pair is already ignored
     */
    public function isIgnored(int $id1, int $id2): bool
    {
        try {
            $stmt = $this->pdo->prepare("
                SELECT 1 FROM rider_duplicate_ignores
                WHERE (rider1_id = ? AND rider2_id = ?)
                   OR (rider1_id = ? AND rider2_id = ?)
            ");
            $stmt->execute([min($id1, $id2), max($id1, $id2), min($id1, $id2), max($id1, $id2)]);
            return (bool)$stmt->fetch();
        } catch (Exception $e) {
            return false; // Table might not exist
        }
    }

    /**
     * Mark pair as not duplicates
     */
    public function ignorePair(int $id1, int $id2, ?int $userId = null): bool
    {
        try {
            $this->pdo->prepare("
                INSERT IGNORE INTO rider_duplicate_ignores
                (rider1_id, rider2_id, ignored_by)
                VALUES (?, ?, ?)
            ")->execute([min($id1, $id2), max($id1, $id2), $userId]);
            return true;
        } catch (Exception $e) {
            return false;
        }
    }
}
