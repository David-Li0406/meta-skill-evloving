<?php
/**
 * Club matching utilities
 * Smart matching for club names during import to reduce duplicates
 */

/**
 * Normalize club name for comparison
 * Handles variations like: CK Fix, Ck Fix, Cykelklubben Fix, Cykelklubb Fix
 */
function normalizeClubName($name) {
    $name = mb_strtolower(trim($name), 'UTF-8');

    // Handle compound names: "Team A / Club B" - extract parts for matching
    // Store both parts for potential matching
    $parts = preg_split('/\s*[\/&]\s*/', $name);
    if (count($parts) > 1) {
        // Use the most likely "club" part (contains ck, cykel, etc.)
        foreach ($parts as $part) {
            if (preg_match('/(ck|cykel|klubb|if|ik|sk|fk|ok)\b/u', $part)) {
                $name = trim($part);
                break;
            }
        }
        // If no club-like part found, use the last part
        if (count($parts) > 1 && $name === mb_strtolower(trim($parts[0] . ' / ' . $parts[1]), 'UTF-8')) {
            $name = trim(end($parts));
        }
    }

    // Remove common prefixes/suffixes (order matters - longer patterns first)
    $patterns = [
        // Long prefixes first
        '/^mountainbikeklubb\s+/u',      // "Mountainbikeklubb X" -> "x"
        '/^mountainbike\s+/u',           // "Mountainbike X" -> "x"
        '/^cykelklubben\s+/u',           // "Cykelklubben Fix" -> "fix"
        '/^cykelklubb\s+/u',             // "Cykelklubb Fix" -> "fix"
        '/^cykelföreningen\s+/u',        // "Cykelföreningen X" -> "x"
        '/^team\s+/u',                   // "Team Kungälv" -> "kungälv"
        '/^mtb\s+/u',                    // "MTB Täby" -> "täby"
        '/^ifk\s+/u',                    // "IFK Trampen" -> "trampen"
        '/^ok\s+/u',                     // "OK Tyr" -> "tyr"
        '/^ck\s+/u',                     // "CK Fix" -> "fix"
        '/^if\s+/u',                     // "IF Ceres" -> "ceres"
        '/^ik\s+/u',                     // "IK X" -> "x"
        '/^sk\s+/u',                     // "SK X" -> "x"
        '/^fk\s+/u',                     // "FK X" -> "x"
        '/^bk\s+/u',                     // "BK X" -> "x"
        // Long suffixes
        '/\s+mountainbikeklubb$/u',      // "X Mountainbikeklubb" -> "x"
        '/\s+mountainbike$/u',           // "X Mountainbike" -> "x"
        '/\s+idrottssällskap$/u',
        '/\s+idrottsällskap$/u',
        '/\s+idrottsförening$/u',
        '/\s+cykelklubb$/u',             // "Fix Cykelklubb" -> "fix"
        '/\s+cykelklubben$/u',           // "Fix Cykelklubben" -> "fix"
        // Short suffixes
        '/\s+enduro$/u',                 // "Fix Enduro" -> "fix"
        '/\s+mtb$/u',                    // "Fix MTB" -> "fix"
        '/\s+ck$/u',                     // "Fix CK" -> "fix"
        '/\s+ok$/u',                     // "Tyr OK" -> "tyr"
        '/\s+if$/u',                     // "Fix IF" -> "fix"
        '/\s+ifk$/u',                    // "X IFK" -> "x"
        '/\s+ik$/u',                     // "X IK" -> "X"
        '/\s+sk$/u',                     // "X SK" -> "X"
    ];

    foreach ($patterns as $pattern) {
        $name = preg_replace($pattern, '', $name);
    }

    // Replace Swedish chars for comparison
    $name = preg_replace('/[åä]/u', 'a', $name);
    $name = preg_replace('/[ö]/u', 'o', $name);
    $name = preg_replace('/[é]/u', 'e', $name);
    $name = preg_replace('/[ø]/u', 'o', $name);
    $name = preg_replace('/[æ]/u', 'ae', $name);

    // Remove non-alphanumeric (keeps only letters and numbers)
    $name = preg_replace('/[^a-z0-9]/u', '', $name);

    // Remove trailing 's' for possessive forms (e.g., "ulricehamns" vs "ulricehamn")
    // Only if it makes it match better - this is done in matching, not here
    // $name = preg_replace('/s$/u', '', $name);

    return $name;
}

/**
 * Find club by name with smart matching
 *
 * Tries matching in this order:
 * 1. Exact case-insensitive match
 * 2. Normalized name match (handles abbreviations like CK/Ck/Cykelklubben)
 * 3. Normalized with trailing 's' variations (possessive forms)
 * 4. Levenshtein distance for typos
 * 5. Partial match if no exact match found
 *
 * @param object $db Database connection
 * @param string $clubName Name to search for
 * @return array|null Matching club row or null
 */
function findClubByName($db, $clubName) {
    $clubName = trim($clubName);
    if (empty($clubName)) {
        return null;
    }

    // 1. Try exact case-insensitive match first (using UPPER - LOWER doesn't work with this MySQL)
    $club = $db->getRow(
        "SELECT id, name FROM clubs WHERE UPPER(name) = UPPER(?)",
        [$clubName]
    );
    if ($club) {
        return $club;
    }

    // 2. Try normalized matching (handles CK/Ck/Cykelklubben variants)
    $normalizedSearch = normalizeClubName($clubName);

    // Get all clubs and normalize them for comparison
    // Cache is refreshed if a new club was added (tracked via count)
    static $normalizedClubCache = null;
    static $normalizedClubCacheNoS = null; // Also cache without trailing 's'
    static $lastClubCount = -1;

    // Check if cache needs refresh (new clubs added)
    $currentCount = (int)$db->getRow("SELECT COUNT(*) as c FROM clubs")['c'];

    if ($normalizedClubCache === null || $currentCount !== $lastClubCount) {
        $allClubs = $db->getAll("SELECT id, name FROM clubs WHERE active = 1");
        $normalizedClubCache = [];
        $normalizedClubCacheNoS = [];
        foreach ($allClubs as $c) {
            $normalized = normalizeClubName($c['name']);
            if (!isset($normalizedClubCache[$normalized])) {
                $normalizedClubCache[$normalized] = $c;
            }
            // Also store without trailing 's' for possessive matching
            $withoutS = preg_replace('/s$/u', '', $normalized);
            if ($withoutS !== $normalized && !isset($normalizedClubCacheNoS[$withoutS])) {
                $normalizedClubCacheNoS[$withoutS] = $c;
            }
        }
        $lastClubCount = $currentCount;
    }

    // Check for normalized match
    if (isset($normalizedClubCache[$normalizedSearch])) {
        return $normalizedClubCache[$normalizedSearch];
    }

    // 3. Try variations with/without trailing 's' (possessive forms)
    // "Ulricehamns CK" -> "ulricehamn" should match "Ulricehamn CK"
    $searchWithoutS = preg_replace('/s$/u', '', $normalizedSearch);
    $searchWithS = $normalizedSearch . 's';

    if ($searchWithoutS !== $normalizedSearch && isset($normalizedClubCache[$searchWithoutS])) {
        return $normalizedClubCache[$searchWithoutS];
    }
    if (isset($normalizedClubCache[$searchWithS])) {
        return $normalizedClubCache[$searchWithS];
    }
    if (isset($normalizedClubCacheNoS[$normalizedSearch])) {
        return $normalizedClubCacheNoS[$normalizedSearch];
    }
    if (isset($normalizedClubCacheNoS[$searchWithoutS])) {
        return $normalizedClubCacheNoS[$searchWithoutS];
    }

    // 4. Try Levenshtein distance for very similar names (typos)
    // Only if the normalized name is long enough
    if (strlen($normalizedSearch) >= 4) {
        $bestMatch = null;
        $bestDistance = PHP_INT_MAX;

        // Calculate max allowed distance based on string length
        // Longer strings can have more typos: 4-6 chars=1, 7-10 chars=2, 11+ chars=3
        $maxDistance = strlen($normalizedSearch) <= 6 ? 1 : (strlen($normalizedSearch) <= 10 ? 2 : 3);

        foreach ($normalizedClubCache as $normalized => $c) {
            if (strlen($normalized) < 4) continue;

            // Also compare without trailing 's'
            $normalizedNoS = preg_replace('/s$/u', '', $normalized);
            $searchNoS = preg_replace('/s$/u', '', $normalizedSearch);

            $distance = min(
                levenshtein($normalizedSearch, $normalized),
                levenshtein($searchNoS, $normalizedNoS),
                levenshtein($searchNoS, $normalized),
                levenshtein($normalizedSearch, $normalizedNoS)
            );

            // Accept if distance is within threshold and better than previous
            if ($distance <= $maxDistance && $distance < $bestDistance) {
                $bestDistance = $distance;
                $bestMatch = $c;
            }
        }

        if ($bestMatch) {
            return $bestMatch;
        }
    }

    // 5. Fallback: try partial match (LIKE) - but be more careful
    // Only if the search term is long enough to be meaningful
    if (strlen($clubName) >= 5) {
        $club = $db->getRow(
            "SELECT id, name FROM clubs WHERE UPPER(name) LIKE UPPER(?)",
            ['%' . $clubName . '%']
        );
        if ($club) {
            return $club;
        }
    }

    return null;
}

/**
 * Check if a club name matches an existing club
 * Returns the matched club or null
 *
 * This is a simpler version for preview/stats that doesn't create clubs
 */
function checkClubMatch($db, $clubName) {
    return findClubByName($db, $clubName);
}
