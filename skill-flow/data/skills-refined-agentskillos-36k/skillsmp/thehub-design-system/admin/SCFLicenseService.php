<?php
/**
 * SCF License Portal API Service
 *
 * Integrates with Svenska Cykelförbundet's License Portal API
 * to verify and sync rider license information.
 *
 * @package TheHUB
 * @version 1.0
 */

class SCFLicenseService {
    /**
     * Default API base URL
     */
    const API_BASE_URL = 'https://licens.scf.se/api/1.0';

    /**
     * Maximum UCI IDs per batch request
     */
    const MAX_BATCH_SIZE = 25;

    /**
     * Delay between API requests (milliseconds)
     */
    const REQUEST_DELAY_MS = 600;

    /**
     * Available disciplines in SCF system
     */
    const DISCIPLINES = [
        'uci_road',
        'uci_mtb',
        'uci_cross',
        'uci_track',
        'uci_bmx',
        'uci_ecycling',
        'uci_gravel'
    ];

    /**
     * @var string API key
     */
    private $apiKey;

    /**
     * @var string API base URL (can be overridden via env SCF_API_URL)
     */
    private $apiBaseUrl;

    /**
     * @var DatabaseWrapper Database connection
     */
    private $db;

    /**
     * @var bool Debug mode
     */
    private $debug = false;

    /**
     * @var int Current sync log ID
     */
    private $currentSyncId = null;

    /**
     * Try to resolve a club ID from a club name (SCF string)
     *
     * @param string $clubName
     * @return array|null ['id' => int, 'scf_district' => ?string]
     */
    private function resolveClubByName(string $clubName): ?array {
        $clubName = trim($clubName);
        if ($clubName === '') return null;

        // 1) Exact match
        $row = $this->db->getRow(
            "SELECT id, scf_district FROM clubs WHERE name = ? LIMIT 1",
            [$clubName]
        );
        if ($row) return $row;

        // 2) Case-insensitive exact match
        $row = $this->db->getRow(
            "SELECT id, scf_district FROM clubs WHERE LOWER(name) = LOWER(?) LIMIT 1",
            [$clubName]
        );
        if ($row) return $row;

        // 3) Soft match: starts with / contains
        $like = '%' . str_replace(['%', '_'], ['\\%', '\\_'], $clubName) . '%';
        $row = $this->db->getRow(
            "SELECT id, scf_district FROM clubs WHERE name LIKE ? ORDER BY (name = ?) DESC, CHAR_LENGTH(name) ASC LIMIT 1",
            [$like, $clubName]
        );
        return $row ?: null;
    }

    /**
     * Constructor
     *
     * @param string $apiKey SCF API key
     * @param DatabaseWrapper $db Database wrapper instance
     */
    public function __construct(string $apiKey, $db) {
        $this->apiKey = $apiKey;
        $this->db = $db;

        // Allow overriding API URL via .env
        // (config.php defines env())
        $this->apiBaseUrl = self::API_BASE_URL;
        if (function_exists('env')) {
            $override = env('SCF_API_URL', '');
            if (!empty($override)) {
                $this->apiBaseUrl = rtrim($override, '/');
            }
        }
    }

    /**
     * Enable/disable debug output
     *
     * @param bool $debug
     * @return self
     */
    public function setDebug(bool $debug): self {
        $this->debug = $debug;
        return $this;
    }

    /**
     * Log debug message
     *
     * @param string $message
     */
    private function log(string $message): void {
        if ($this->debug) {
            echo "[" . date('H:i:s') . "] $message\n";
        }
    }

    /**
     * Make API request to SCF License Portal
     *
     * @param string $endpoint API endpoint (without base URL)
     * @param array $params Query parameters
     * @return array|null Response data or null on error
     */
    private function apiRequest(string $endpoint, array $params = []): ?array {
        $url = $this->apiBaseUrl . $endpoint;
        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }

        $this->log("API Request: $url");

        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $this->apiKey,
                'Accept: application/json',
                'Content-Type: application/json'
            ],
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_FOLLOWLOCATION => true
        ]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);

        if ($error) {
            $this->log("CURL Error: $error");
            return null;
        }

        if ($httpCode !== 200) {
            $this->log("HTTP Error: $httpCode - Response: $response");
            return null;
        }

        $data = json_decode($response, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->log("JSON Parse Error: " . json_last_error_msg());
            return null;
        }

        return $data;
    }

    /**
     * Normalize UCI ID to standard format (digits only, no spaces)
     *
     * @param string $uciId
     * @return string
     */
    public function normalizeUciId(string $uciId): string {
        return preg_replace('/[^0-9]/', '', $uciId);
    }

    /**
     * Format UCI ID for display (XXX XXX XXX XX)
     *
     * @param string $uciId
     * @return string
     */
    public function formatUciIdDisplay(string $uciId): string {
        $digits = $this->normalizeUciId($uciId);
        if (strlen($digits) !== 11) {
            return $digits;
        }
        return substr($digits, 0, 3) . ' ' .
               substr($digits, 3, 3) . ' ' .
               substr($digits, 6, 3) . ' ' .
               substr($digits, 9, 2);
    }

    /**
     * Lookup licenses by UCI IDs (batch)
     *
     * @param array $uciIds Array of UCI IDs (max 25)
     * @param int $year License year
     * @return array Array of license data indexed by UCI ID
     */
    public function lookupByUciIds(array $uciIds, int $year): array {
        if (empty($uciIds)) {
            return [];
        }

        // Normalize and limit
        $uciIds = array_slice($uciIds, 0, self::MAX_BATCH_SIZE);
        $normalizedIds = array_map([$this, 'normalizeUciId'], $uciIds);

        $response = $this->apiRequest('/ucilicenselookup', [
            'year' => $year,
            'uciids' => implode(',', $normalizedIds)
        ]);

        if (!$response || !isset($response['licenses'])) {
            return [];
        }

        $results = [];
        foreach ($response['licenses'] as $license) {
            $id = $this->normalizeUciId($license['uci_id'] ?? '');
            if ($id) {
                $results[$id] = $this->parseLicenseData($license);
            }
        }

        return $results;
    }

    /**
     * Lookup license by name
     *
     * @param string $firstname
     * @param string $lastname
     * @param string $gender M or F
     * @param string|null $birthdate YYYY-MM-DD format
     * @param int $year License year
     * @return array|null License data or null if not found
     */
    public function lookupByName(string $firstname, string $lastname, string $gender, ?string $birthdate, int $year): ?array {
        $params = [
            'year' => $year,
            'firstname' => $firstname,
            'lastname' => $lastname,
            'gender' => strtoupper($gender)
        ];

        if ($birthdate) {
            $params['birthdate'] = $birthdate;
        }

        $response = $this->apiRequest('/licenselookup', $params);

        if (!$response || empty($response['licenses'])) {
            return null;
        }

        // Return first match (API may return multiple for ambiguous queries)
        return $this->parseLicenseData($response['licenses'][0]);
    }

    /**
     * Parse license data from API response
     *
     * @param array $data Raw API response data
     * @return array Normalized license data
     */
    private function parseLicenseData(array $data): array {
        $disciplines = [];
        foreach (self::DISCIPLINES as $disc) {
            if (!empty($data[$disc])) {
                $disciplines[] = $disc;
            }
        }

        // Extract birth year from birthdate
        $birthYear = null;
        if (!empty($data['birthdate'])) {
            $birthYear = (int)substr($data['birthdate'], 0, 4);
        }

        return [
            'uci_id' => $this->normalizeUciId($data['uci_id'] ?? ''),
            'firstname' => $data['firstname'] ?? null,
            'lastname' => $data['lastname'] ?? null,
            'gender' => $data['gender'] ?? null,
            'birthdate' => $data['birthdate'] ?? null,
            'birth_year' => $birthYear,
            'nationality' => $data['nationality'] ?? null,
            'club_name' => $data['club_name'] ?? $data['club'] ?? null,
            'district' => $data['district'] ?? null,
            'license_type' => $data['license_type'] ?? $data['type'] ?? null,
            'disciplines' => $disciplines,
            'expires_at' => $data['expires_at'] ?? $data['valid_until'] ?? null,
            'raw_data' => $data
        ];
    }

    /**
     * Cache license data in database
     *
     * @param array $licenseData Parsed license data
     * @param int $year License year
     * @return bool Success
     */
    public function cacheLicense(array $licenseData, int $year): bool {
        if (empty($licenseData['uci_id'])) {
            return false;
        }

        $sql = "INSERT INTO scf_license_cache
                (uci_id, year, firstname, lastname, gender, birthdate, nationality,
                 club_name, license_type, disciplines, raw_data, expires_at, verified_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
                ON DUPLICATE KEY UPDATE
                    firstname = VALUES(firstname),
                    lastname = VALUES(lastname),
                    gender = VALUES(gender),
                    birthdate = VALUES(birthdate),
                    nationality = VALUES(nationality),
                    club_name = VALUES(club_name),
                    license_type = VALUES(license_type),
                    disciplines = VALUES(disciplines),
                    raw_data = VALUES(raw_data),
                    expires_at = VALUES(expires_at),
                    verified_at = NOW()";

        $stmt = $this->db->query($sql, [
            $licenseData['uci_id'],
            $year,
            $licenseData['firstname'],
            $licenseData['lastname'],
            $licenseData['gender'],
            $licenseData['birthdate'],
            $licenseData['nationality'],
            $licenseData['club_name'],
            $licenseData['license_type'],
            json_encode($licenseData['disciplines']),
            json_encode($licenseData['raw_data']),
            $licenseData['expires_at']
        ]);

        return $stmt !== false;
    }

    /**
     * Update rider with SCF license data
     *
     * Updates rider profile with verified data from SCF:
     * - License verification fields (scf_license_year, etc.)
     * - Birth year, gender, nationality (if missing)
     * - District from SCF
     * - Correctly spelled name from SCF
     *
     * @param int $riderId
     * @param array $licenseData
     * @param int $year
     * @return bool Success
     */
    public function updateRiderLicense(int $riderId, array $licenseData, int $year): bool {
        // Get current rider data to check what needs updating
        $rider = $this->db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);
        if (!$rider) {
            return false;
        }

        // Build update array with SCF verified fields
        $updates = [
            'scf_license_verified_at' => date('Y-m-d H:i:s'),
            'scf_license_year' => $year,
            'scf_license_type' => $licenseData['license_type'],
            'scf_disciplines' => json_encode($licenseData['disciplines']),
            'scf_club_name' => $licenseData['club_name']
        ];

        // Update birth year if we have it from SCF
        if (!empty($licenseData['birth_year']) && $licenseData['birth_year'] > 1900) {
            $updates['birth_year'] = $licenseData['birth_year'];
        }

        // Update gender if we have it from SCF
        if (!empty($licenseData['gender'])) {
            $updates['gender'] = strtoupper($licenseData['gender']);
        }

        // Update nationality if missing
        if (!empty($licenseData['nationality']) && empty($rider['nationality'])) {
            $updates['nationality'] = $licenseData['nationality'];
        }

        // Club + district handling
        // API payload may not contain district. We derive district from matched club if possible.
        if (!empty($licenseData['club_name'])) {
            $resolvedClub = $this->resolveClubByName($licenseData['club_name']);

            // Only overwrite club_id if rider currently has no club, or is a placeholder.
            // (Many solostartare will have club_id NULL/0. Some installs use a dedicated "Solostartare" club.)
            $shouldUpdateClubId = empty($rider['club_id']);
            if (!$shouldUpdateClubId && !empty($rider['club_id'])) {
                try {
                    $currentClubName = (string)$this->db->getValue("SELECT name FROM clubs WHERE id = ?", [$rider['club_id']]);
                    if ($currentClubName && mb_strtolower(trim($currentClubName)) === 'solostartare') {
                        $shouldUpdateClubId = true;
                    }
                } catch (Exception $e) {
                    // Ignore lookup errors; do not block sync
                }
            }

            if ($resolvedClub && $shouldUpdateClubId) {
                $updates['club_id'] = (int)$resolvedClub['id'];
            }

            // District: prefer explicit district from API (if present), otherwise from club.
            if (!empty($licenseData['district'])) {
                $updates['district'] = $licenseData['district'];
            } elseif (!empty($resolvedClub['scf_district'])) {
                $updates['district'] = $resolvedClub['scf_district'];
            }
        } else {
            // Update district from SCF if present even without club
            if (!empty($licenseData['district'])) {
                $updates['district'] = $licenseData['district'];
            }
        }

        // Update name with correctly spelled version from SCF
        if (!empty($licenseData['firstname'])) {
            $updates['firstname'] = $licenseData['firstname'];
        }
        if (!empty($licenseData['lastname'])) {
            $updates['lastname'] = $licenseData['lastname'];
        }

        // Perform update
        $result = $this->db->update('riders', $updates, 'id = ?', [$riderId]);

        if ($result === false) {
            return false;
        }

        // Record in history
        $this->recordLicenseHistory($riderId, $licenseData, $year);

        return true;
    }

    /**
     * Record license history entry
     *
     * @param int $riderId
     * @param array $licenseData
     * @param int $year
     */
    private function recordLicenseHistory(int $riderId, array $licenseData, int $year): void {
        $sql = "INSERT INTO scf_license_history
                (rider_id, uci_id, year, license_type, disciplines, club_name, nationality)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE
                    license_type = VALUES(license_type),
                    disciplines = VALUES(disciplines),
                    club_name = VALUES(club_name),
                    nationality = VALUES(nationality),
                    recorded_at = NOW()";

        $this->db->query($sql, [
            $riderId,
            $licenseData['uci_id'],
            $year,
            $licenseData['license_type'],
            json_encode($licenseData['disciplines']),
            $licenseData['club_name'],
            $licenseData['nationality']
        ]);
    }

    /**
     * Start a sync operation (creates log entry)
     *
     * @param string $type full|incremental|manual|match_search
     * @param int $year
     * @param int $totalRiders
     * @param array $options
     * @return int Sync log ID
     */
    public function startSync(string $type, int $year, int $totalRiders = 0, array $options = []): int {
        $this->db->query(
            "INSERT INTO scf_sync_log (sync_type, year, started_at, total_riders, options)
             VALUES (?, ?, NOW(), ?, ?)",
            [$type, $year, $totalRiders, json_encode($options)]
        );

        $this->currentSyncId = $this->db->getPdo()->lastInsertId();
        return $this->currentSyncId;
    }

    /**
     * Update sync progress
     *
     * @param int $processed
     * @param int $found
     * @param int $updated
     * @param int $errors
     */
    public function updateSyncProgress(int $processed, int $found, int $updated, int $errors): void {
        if (!$this->currentSyncId) return;

        $this->db->query(
            "UPDATE scf_sync_log SET processed = ?, found = ?, updated = ?, errors = ? WHERE id = ?",
            [$processed, $found, $updated, $errors, $this->currentSyncId]
        );
    }

    /**
     * Complete sync operation
     *
     * @param string $status completed|failed|cancelled
     * @param string|null $errorMessage
     */
    public function completeSync(string $status = 'completed', ?string $errorMessage = null): void {
        if (!$this->currentSyncId) return;

        $this->db->query(
            "UPDATE scf_sync_log SET status = ?, completed_at = NOW(), error_message = ? WHERE id = ?",
            [$status, $errorMessage, $this->currentSyncId]
        );

        $this->currentSyncId = null;
    }

    /**
     * Get riders with UCI ID (license_number) that need license verification
     *
     * @param int $year
     * @param int $limit
     * @param int $offset
     * @param bool $onlyUnverified Only get riders not yet verified this year
     * @return array
     */
    public function getRidersToSync(int $year, int $limit = 100, int $offset = 0, bool $onlyUnverified = true): array {
        // license_number contains either real UCI ID (NOT starting with SWE) or generated SWE-ID
        // Real UCI IDs can be formatted with spaces like "XXX XXX XXX XX"
        $sql = "SELECT id, firstname, lastname, license_number, gender, birth_year, nationality
                FROM riders
                WHERE license_number IS NOT NULL
                  AND license_number != ''
                  AND license_number NOT LIKE 'SWE%'";

        if ($onlyUnverified) {
            $sql .= " AND (scf_license_year IS NULL OR scf_license_year != ?)";
        }

        $sql .= " ORDER BY id LIMIT ? OFFSET ?";

        $params = $onlyUnverified ? [$year, $limit, $offset] : [$limit, $offset];

        return $this->db->getAll($sql, $params);
    }

    /**
     * Get count of riders that need syncing
     *
     * @param int $year
     * @param bool $onlyUnverified
     * @return int
     */
    public function countRidersToSync(int $year, bool $onlyUnverified = true): int {
        // license_number contains either real UCI ID (NOT starting with SWE) or generated SWE-ID
        $sql = "SELECT COUNT(*) FROM riders
                WHERE license_number IS NOT NULL
                  AND license_number != ''
                  AND license_number NOT LIKE 'SWE%'";

        if ($onlyUnverified) {
            $sql .= " AND (scf_license_year IS NULL OR scf_license_year != ?)";
            return (int)$this->db->getValue($sql, [$year]);
        }

        return (int)$this->db->getValue($sql);
    }

    /**
     * Sync licenses for a batch of riders
     *
     * @param array $riders Array of rider records
     * @param int $year
     * @return array Stats [processed, found, updated, errors]
     */
    public function syncRiderBatch(array $riders, int $year): array {
        $stats = ['processed' => 0, 'found' => 0, 'updated' => 0, 'errors' => 0];

        if (empty($riders)) {
            return $stats;
        }

        // Collect UCI IDs from license_number field
        $uciIdMap = [];
        foreach ($riders as $rider) {
            $normalizedId = $this->normalizeUciId($rider['license_number'] ?? '');
            if (strlen($normalizedId) === 11) {
                $uciIdMap[$normalizedId] = $rider;
            }
        }

        if (empty($uciIdMap)) {
            return $stats;
        }

        // Batch lookup
        $licenses = $this->lookupByUciIds(array_keys($uciIdMap), $year);

        // Process results
        foreach ($uciIdMap as $uciId => $rider) {
            $stats['processed']++;

            if (isset($licenses[$uciId])) {
                $stats['found']++;
                $licenseData = $licenses[$uciId];

                // Cache the license data
                $this->cacheLicense($licenseData, $year);

                // Update rider
                if ($this->updateRiderLicense($rider['id'], $licenseData, $year)) {
                    $stats['updated']++;
                    $this->log("Updated rider #{$rider['id']}: {$rider['firstname']} {$rider['lastname']}");
                } else {
                    $stats['errors']++;
                    $this->log("Error updating rider #{$rider['id']}");
                }
            } else {
                $this->log("Not found in SCF: {$rider['firstname']} {$rider['lastname']} (UCI: $uciId)");
            }
        }

        return $stats;
    }

    /**
     * Get riders without UCI ID (license_number) for potential matching
     *
     * @param int $limit
     * @param int $offset
     * @return array
     */
    public function getRidersWithoutUciId(int $limit = 100, int $offset = 0): array {
        // license_number contains either real UCI ID (NOT starting with SWE) or generated SWE-ID
        return $this->db->getAll(
            "SELECT r.id, r.firstname, r.lastname, r.gender, r.birth_year, r.nationality, c.name as club_name
             FROM riders r
             LEFT JOIN clubs c ON r.club_id = c.id
             WHERE (r.license_number IS NULL OR r.license_number = '' OR r.license_number LIKE 'SWE%')
               AND r.id NOT IN (SELECT rider_id FROM scf_match_candidates WHERE status = 'pending')
             ORDER BY r.id
             LIMIT ? OFFSET ?",
            [$limit, $offset]
        );
    }

    /**
     * Search for potential license matches for a rider
     *
     * @param array $rider Rider data
     * @param int $year
     * @return array Array of potential matches with scores
     */
    public function findPotentialMatches(array $rider, int $year): array {
        $matches = [];

        // Build birthdate from birth_year if available
        $birthdate = null;
        if (!empty($rider['birth_year'])) {
            $birthdate = $rider['birth_year'] . '-01-01';
        }

        // Try name lookup
        $gender = strtoupper(substr($rider['gender'] ?? 'M', 0, 1));
        $result = $this->lookupByName(
            $rider['firstname'],
            $rider['lastname'],
            $gender,
            $birthdate,
            $year
        );

        if ($result) {
            $score = $this->calculateMatchScore($rider, $result);
            $matches[] = [
                'license' => $result,
                'score' => $score,
                'reason' => $this->getMatchReason($rider, $result, $score)
            ];
        }

        // Also try without birthdate for fuzzy match
        if ($birthdate) {
            usleep(self::REQUEST_DELAY_MS * 1000);
            $result2 = $this->lookupByName(
                $rider['firstname'],
                $rider['lastname'],
                $gender,
                null,
                $year
            );

            if ($result2 && (!$result || $result2['uci_id'] !== $result['uci_id'])) {
                $score = $this->calculateMatchScore($rider, $result2);
                $matches[] = [
                    'license' => $result2,
                    'score' => $score,
                    'reason' => $this->getMatchReason($rider, $result2, $score)
                ];
            }
        }

        // Sort by score descending
        usort($matches, function($a, $b) {
            return $b['score'] <=> $a['score'];
        });

        return $matches;
    }

    /**
     * Calculate match confidence score
     *
     * @param array $rider TheHUB rider data
     * @param array $license SCF license data
     * @return float Score 0-100
     */
    private function calculateMatchScore(array $rider, array $license): float {
        $score = 0;

        // Name match (40 points)
        $fnSim = $this->stringSimilarity(
            mb_strtolower($rider['firstname']),
            mb_strtolower($license['firstname'] ?? '')
        );
        $lnSim = $this->stringSimilarity(
            mb_strtolower($rider['lastname']),
            mb_strtolower($license['lastname'] ?? '')
        );
        $score += ($fnSim * 20) + ($lnSim * 20);

        // Gender match (15 points)
        $riderGender = strtoupper(substr($rider['gender'] ?? '', 0, 1));
        $licenseGender = strtoupper(substr($license['gender'] ?? '', 0, 1));
        if ($riderGender && $licenseGender && $riderGender === $licenseGender) {
            $score += 15;
        }

        // Birth year match (25 points)
        if (!empty($rider['birth_year']) && !empty($license['birthdate'])) {
            $licenseYear = (int)substr($license['birthdate'], 0, 4);
            if ((int)$rider['birth_year'] === $licenseYear) {
                $score += 25;
            } elseif (abs((int)$rider['birth_year'] - $licenseYear) <= 1) {
                $score += 15;
            }
        }

        // Nationality match (10 points)
        if (!empty($rider['nationality']) && !empty($license['nationality'])) {
            if (strtoupper($rider['nationality']) === strtoupper($license['nationality'])) {
                $score += 10;
            }
        }

        // Club similarity (10 points)
        if (!empty($rider['club_name']) && !empty($license['club_name'])) {
            $clubSim = $this->stringSimilarity(
                mb_strtolower($rider['club_name']),
                mb_strtolower($license['club_name'])
            );
            $score += $clubSim * 10;
        }

        return min(100, $score);
    }

    /**
     * Calculate string similarity (0-1)
     *
     * @param string $a
     * @param string $b
     * @return float
     */
    private function stringSimilarity(string $a, string $b): float {
        if ($a === $b) return 1.0;
        if (empty($a) || empty($b)) return 0.0;

        similar_text($a, $b, $percent);
        return $percent / 100;
    }

    /**
     * Generate human-readable match reason
     *
     * @param array $rider
     * @param array $license
     * @param float $score
     * @return string
     */
    private function getMatchReason(array $rider, array $license, float $score): string {
        $reasons = [];

        if ($score >= 90) {
            $reasons[] = 'Stark matchning';
        } elseif ($score >= 75) {
            $reasons[] = 'God matchning';
        } else {
            $reasons[] = 'Svag matchning';
        }

        // Name comparison
        $fnMatch = mb_strtolower($rider['firstname']) === mb_strtolower($license['firstname'] ?? '');
        $lnMatch = mb_strtolower($rider['lastname']) === mb_strtolower($license['lastname'] ?? '');
        if ($fnMatch && $lnMatch) {
            $reasons[] = 'Exakt namnmatchning';
        } elseif ($lnMatch) {
            $reasons[] = 'Efternamn matchar';
        }

        // Birth year
        if (!empty($rider['birth_year']) && !empty($license['birthdate'])) {
            $licenseYear = (int)substr($license['birthdate'], 0, 4);
            if ((int)$rider['birth_year'] === $licenseYear) {
                $reasons[] = 'Födelseår matchar';
            }
        }

        return implode('. ', $reasons) . '.';
    }

    /**
     * Save a match candidate for review
     *
     * @param int $riderId
     * @param array $rider
     * @param array $match
     * @return bool
     */
    public function saveMatchCandidate(int $riderId, array $rider, array $match): bool {
        $license = $match['license'];

        // Build birthdate for hub rider
        $hubBirthdate = null;
        if (!empty($rider['birth_year'])) {
            $hubBirthdate = $rider['birth_year'] . '-01-01';
        }

        $sql = "INSERT INTO scf_match_candidates
                (rider_id, hub_firstname, hub_lastname, hub_gender, hub_birthdate, hub_birth_year,
                 scf_uci_id, scf_firstname, scf_lastname, scf_club, scf_nationality,
                 match_score, match_reason, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                ON DUPLICATE KEY UPDATE
                    scf_uci_id = VALUES(scf_uci_id),
                    scf_firstname = VALUES(scf_firstname),
                    scf_lastname = VALUES(scf_lastname),
                    scf_club = VALUES(scf_club),
                    scf_nationality = VALUES(scf_nationality),
                    match_score = VALUES(match_score),
                    match_reason = VALUES(match_reason),
                    status = 'pending',
                    created_at = NOW()";

        $stmt = $this->db->query($sql, [
            $riderId,
            $rider['firstname'],
            $rider['lastname'],
            $rider['gender'],
            $hubBirthdate,
            $rider['birth_year'],
            $license['uci_id'],
            $license['firstname'],
            $license['lastname'],
            $license['club_name'],
            $license['nationality'],
            $match['score'],
            $match['reason']
        ]);

        return $stmt !== false;
    }

    /**
     * Get pending match candidates
     *
     * @param int $limit
     * @param float $minScore
     * @return array
     */
    public function getPendingMatches(int $limit = 50, float $minScore = 0): array {
        return $this->db->getAll(
            "SELECT mc.*, r.id as current_rider_id
             FROM scf_match_candidates mc
             JOIN riders r ON mc.rider_id = r.id
             WHERE mc.status = 'pending'
               AND mc.match_score >= ?
             ORDER BY mc.match_score DESC, mc.created_at DESC
             LIMIT ?",
            [$minScore, $limit]
        );
    }

    /**
     * Confirm a match candidate (assigns UCI ID to rider's license_number field)
     *
     * @param int $matchId
     * @param int $adminUserId
     * @return bool
     */
    public function confirmMatch(int $matchId, int $adminUserId): bool {
        $match = $this->db->getRow(
            "SELECT * FROM scf_match_candidates WHERE id = ?",
            [$matchId]
        );

        if (!$match || $match['status'] !== 'pending') {
            return false;
        }

        $this->db->beginTransaction();
        try {
            // Update rider with UCI ID in license_number field
            $this->db->update('riders', [
                'license_number' => $this->normalizeUciId($match['scf_uci_id'])
            ], 'id = ?', [$match['rider_id']]);

            // Mark match as confirmed
            $this->db->update('scf_match_candidates', [
                'status' => 'confirmed',
                'reviewed_by' => $adminUserId,
                'reviewed_at' => date('Y-m-d H:i:s')
            ], 'id = ?', [$matchId]);

            $this->db->commit();
            return true;
        } catch (Exception $e) {
            $this->db->rollback();
            return false;
        }
    }

    /**
     * Reject a match candidate
     *
     * @param int $matchId
     * @param int $adminUserId
     * @return bool
     */
    public function rejectMatch(int $matchId, int $adminUserId): bool {
        return $this->db->update('scf_match_candidates', [
            'status' => 'rejected',
            'reviewed_by' => $adminUserId,
            'reviewed_at' => date('Y-m-d H:i:s')
        ], 'id = ?', [$matchId]) > 0;
    }

    /**
     * Get sync statistics
     *
     * @param int|null $year Filter by year
     * @return array
     */
    public function getSyncStats(?int $year = null): array {
        $whereClause = $year ? "WHERE year = ?" : "";
        $params = $year ? [$year] : [];

        return [
            'total_syncs' => (int)$this->db->getValue(
                "SELECT COUNT(*) FROM scf_sync_log $whereClause",
                $params
            ),
            'last_sync' => $this->db->getRow(
                "SELECT * FROM scf_sync_log $whereClause ORDER BY started_at DESC LIMIT 1",
                $params
            ),
            'total_verified' => (int)$this->db->getValue(
                $year
                    ? "SELECT COUNT(*) FROM riders WHERE scf_license_year = ?"
                    : "SELECT COUNT(*) FROM riders WHERE scf_license_year IS NOT NULL",
                $params
            ),
            'pending_matches' => (int)$this->db->getValue(
                "SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'pending'"
            ),
            // license_number contains either real UCI ID (NOT starting with "SWE")
            // or generated SWE-ID (starting with "SWE") for riders without real UCI
            'riders_with_uci' => (int)$this->db->getValue(
                "SELECT COUNT(*) FROM riders WHERE license_number IS NOT NULL AND license_number != '' AND license_number NOT LIKE 'SWE%'"
            ),
            'riders_without_uci' => (int)$this->db->getValue(
                "SELECT COUNT(*) FROM riders WHERE license_number IS NULL OR license_number = '' OR license_number LIKE 'SWE%'"
            )
        ];
    }

    /**
     * Get recent sync logs
     *
     * @param int $limit
     * @return array
     */
    public function getRecentSyncs(int $limit = 10): array {
        return $this->db->getAll(
            "SELECT * FROM scf_sync_log ORDER BY started_at DESC LIMIT ?",
            [$limit]
        );
    }

    /**
     * Sleep between API requests (rate limiting)
     */
    public function rateLimit(): void {
        usleep(self::REQUEST_DELAY_MS * 1000);
    }
}
