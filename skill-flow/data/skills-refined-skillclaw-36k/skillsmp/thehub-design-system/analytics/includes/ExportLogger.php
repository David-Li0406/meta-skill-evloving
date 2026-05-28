<?php
/**
 * ExportLogger
 *
 * Hanterar loggning av alla analytics-exporter for GDPR och reproducerbarhet.
 * Skapar manifest med fingerprint for varje export.
 *
 * v3.0.2: DB-baserade rate limits, mandatory snapshot_id, deterministic fingerprint
 *
 * @package TheHUB Analytics
 * @version 3.0.2
 */

require_once __DIR__ . '/AnalyticsConfig.php';

class ExportLogger {
    private PDO $pdo;

    /** @var bool Om snapshot_id ar obligatoriskt (ALLTID true i v3.0.2) */
    private bool $requireSnapshotId = true;

    /** @var array|null Cachade rate limits fran DB */
    private ?array $rateLimitsCache = null;

    /** @var string Rate limit source: 'database' eller 'config' */
    private string $rateLimitSource = 'database';

    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
        $this->loadRateLimitsFromDb();
    }

    /**
     * Ladda rate limits fran databas
     */
    private function loadRateLimitsFromDb(): void {
        try {
            $stmt = $this->pdo->query("
                SELECT scope, scope_value, max_exports, window_seconds, max_rows_per_export
                FROM export_rate_limits
                WHERE enabled = 1
                ORDER BY
                    CASE scope
                        WHEN 'user' THEN 1
                        WHEN 'role' THEN 2
                        WHEN 'ip' THEN 3
                        WHEN 'global' THEN 4
                    END
            ");
            $this->rateLimitsCache = $stmt->fetchAll(PDO::FETCH_ASSOC);
            $this->rateLimitSource = 'database';
        } catch (PDOException $e) {
            // Fallback till default om tabellen inte finns
            $this->rateLimitsCache = null;
            $this->rateLimitSource = 'config';
            error_log('ExportLogger: Could not load rate limits from DB: ' . $e->getMessage());
        }
    }

    /**
     * Hamta applicerbar rate limit for en anvandare
     *
     * @param int|null $userId
     * @param string|null $role
     * @return array Rate limit config
     */
    private function getApplicableRateLimit(?int $userId, ?string $role = null): array {
        // Default fallback
        $default = ['max_exports' => 50, 'window_seconds' => 3600];

        if ($this->rateLimitsCache === null) {
            return $default;
        }

        // Prioritetsordning: user > role > global
        foreach ($this->rateLimitsCache as $limit) {
            // User-specific
            if ($limit['scope'] === 'user' && $userId !== null && $limit['scope_value'] == $userId) {
                return $limit;
            }
            // Role-specific
            if ($limit['scope'] === 'role' && $role !== null && $limit['scope_value'] === $role) {
                return $limit;
            }
        }

        // Global fallback
        foreach ($this->rateLimitsCache as $limit) {
            if ($limit['scope'] === 'global' && $limit['scope_value'] === null) {
                return $limit;
            }
        }

        return $default;
    }

    /**
     * Logga en export (v3.0.1 med mandatory snapshot_id)
     *
     * @param string $exportType Typ av export (riders_at_risk, cohort, winback, etc.)
     * @param array $data Exporterad data
     * @param array $options Export-optioner (snapshot_id REQUIRED)
     * @return int Export ID
     * @throws InvalidArgumentException Om snapshot_id saknas
     * @throws RuntimeException Om rate limit overskrids
     */
    public function logExport(string $exportType, array $data, array $options = []): int {
        // v3.0.1: Validera mandatory snapshot_id
        if ($this->requireSnapshotId && empty($options['snapshot_id'])) {
            throw new InvalidArgumentException(
                'snapshot_id is required for all exports in v3.0.1+. ' .
                'Create a snapshot first using AnalyticsEngine::createSnapshot()'
            );
        }

        // Rate limiting check
        $userId = $options['user_id'] ?? null;
        $ipAddress = $options['ip_address'] ?? $this->getClientIP();

        if (!$this->checkRateLimit($userId, $ipAddress)) {
            throw new RuntimeException(
                'Export rate limit exceeded. Please wait before exporting again.'
            );
        }

        // Generate unique export ID
        $exportUid = $this->generateExportUid();

        $manifest = $this->createManifest($exportType, $data, $options);
        $manifest['export_uid'] = $exportUid;

        $stmt = $this->pdo->prepare("
            INSERT INTO analytics_exports (
                export_uid, export_type, export_format, filename,
                exported_by, ip_address,
                season_year, series_id, filters, filters_json,
                row_count, contains_pii,
                snapshot_id, data_fingerprint, source_query_hash,
                manifest, status
            ) VALUES (
                ?, ?, ?, ?,
                ?, ?,
                ?, ?, ?, ?,
                ?, ?,
                ?, ?, ?,
                ?, 'completed'
            )
        ");

        $filters = $options['filters'] ?? [];
        $stmt->execute([
            $exportUid,
            $exportType,
            $options['format'] ?? 'csv',
            $options['filename'] ?? null,
            $userId,
            $ipAddress,
            $options['year'] ?? null,
            $options['series_id'] ?? null,
            json_encode($filters),       // Legacy filters column
            json_encode($filters),       // New JSON column
            count($data),
            $this->containsPII($data) ? 1 : 0,
            $options['snapshot_id'],
            $manifest['data_fingerprint'],
            $manifest['query_hash'] ?? null,
            json_encode($manifest),
        ]);

        return (int)$this->pdo->lastInsertId();
    }

    /**
     * Logga export utan snapshot (for bakåtkompatibilitet, loggar varning)
     *
     * @deprecated Anvand logExport() med snapshot_id istallet
     */
    public function logExportLegacy(string $exportType, array $data, array $options = []): int {
        error_log('WARNING: logExportLegacy() used without snapshot_id. Export will not be reproducible.');

        $this->requireSnapshotId = false;
        $result = $this->logExport($exportType, $data, $options);
        $this->requireSnapshotId = true;

        return $result;
    }

    /**
     * Generera unik export-UID
     *
     * @return string UUID v4
     */
    private function generateExportUid(): string {
        // UUID v4 implementation
        $data = random_bytes(16);
        $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
        $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

        return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
    }

    /**
     * Kontrollera rate limit for anvandare/IP
     *
     * v3.0.2: Anvander DB-baserade rate limits
     *
     * @param int|null $userId
     * @param string|null $ipAddress
     * @param string|null $role Anvandarens roll (for roll-baserade limits)
     * @return bool True om under limit
     */
    public function checkRateLimit(?int $userId, ?string $ipAddress, ?string $role = null): bool {
        $limit = $this->getApplicableRateLimit($userId, $role);
        $windowSeconds = (int)($limit['window_seconds'] ?? 3600);
        $maxExports = (int)($limit['max_exports'] ?? 50);

        // Kolla inom window
        $count = $this->getExportCountInWindow($userId, $ipAddress, $windowSeconds);

        return $count < $maxExports;
    }

    /**
     * Hamta antal exporter inom ett tidsfönster
     *
     * @param int|null $userId
     * @param string|null $ipAddress
     * @param int $windowSeconds Fönsterstorlek i sekunder
     * @return int Antal exporter
     */
    private function getExportCountInWindow(?int $userId, ?string $ipAddress, int $windowSeconds): int {
        $conditions = [];
        $params = [];

        if ($userId) {
            $conditions[] = 'exported_by = ?';
            $params[] = $userId;
        }
        if ($ipAddress) {
            $conditions[] = 'ip_address = ?';
            $params[] = $ipAddress;
        }

        if (empty($conditions)) {
            return 0;
        }

        $whereClause = implode(' OR ', $conditions);

        $stmt = $this->pdo->prepare("
            SELECT COUNT(*) FROM analytics_exports
            WHERE ($whereClause)
            AND exported_at >= DATE_SUB(NOW(), INTERVAL ? SECOND)
        ");
        $params[] = $windowSeconds;
        $stmt->execute($params);

        return (int)$stmt->fetchColumn();
    }

    /**
     * Hamta antal exporter for period (legacy wrapper)
     *
     * @deprecated Anvand getExportCountInWindow() istallet
     * @param int|null $userId
     * @param string|null $ipAddress
     * @param string $period 'hour' eller 'day'
     * @return int Antal exporter
     */
    private function getExportCount(?int $userId, ?string $ipAddress, string $period): int {
        $windowSeconds = $period === 'hour' ? 3600 : 86400;
        return $this->getExportCountInWindow($userId, $ipAddress, $windowSeconds);
    }

    /**
     * Hamta rate limit status for en anvandare
     *
     * v3.0.2: Stodjer DB-baserade rate limits med olika tidsfönster
     *
     * @param int|null $userId
     * @param string|null $ipAddress
     * @param string|null $role Anvandarens roll
     * @return array Status med counts och limits
     */
    public function getRateLimitStatus(?int $userId, ?string $ipAddress = null, ?string $role = null): array {
        $ipAddress = $ipAddress ?? $this->getClientIP();
        $limit = $this->getApplicableRateLimit($userId, $role);

        $windowSeconds = (int)($limit['window_seconds'] ?? 3600);
        $maxExports = (int)($limit['max_exports'] ?? 50);
        $currentCount = $this->getExportCountInWindow($userId, $ipAddress, $windowSeconds);

        // Formattera window for display
        $windowDisplay = $this->formatWindow($windowSeconds);

        // Hamta även daily för bakåtkompatibilitet
        $dailyCount = $this->getExportCountInWindow($userId, $ipAddress, 86400);
        $dailyLimit = $this->getDailyLimit($userId, $role);

        return [
            // Primary limit (from DB config)
            'primary' => [
                'current' => $currentCount,
                'limit' => $maxExports,
                'window_seconds' => $windowSeconds,
                'window_display' => $windowDisplay,
                'source' => $this->rateLimitSource,
            ],
            // Legacy format for backward compatibility
            'hourly' => [
                'current' => $windowSeconds <= 3600 ? $currentCount : $this->getExportCountInWindow($userId, $ipAddress, 3600),
                'limit' => $windowSeconds <= 3600 ? $maxExports : 50,
            ],
            'daily' => [
                'current' => $dailyCount,
                'limit' => $dailyLimit,
            ],
            'can_export' => $this->checkRateLimit($userId, $ipAddress, $role),
        ];
    }

    /**
     * Formattera window seconds to display string
     *
     * @param int $seconds
     * @return string
     */
    private function formatWindow(int $seconds): string {
        if ($seconds < 60) return $seconds . ' sekunder';
        if ($seconds < 3600) return round($seconds / 60) . ' minuter';
        if ($seconds < 86400) return round($seconds / 3600) . ' timmar';
        return round($seconds / 86400) . ' dagar';
    }

    /**
     * Hamta daily limit (for backwards compatibility)
     *
     * @param int|null $userId
     * @param string|null $role
     * @return int
     */
    private function getDailyLimit(?int $userId, ?string $role): int {
        if ($this->rateLimitsCache === null) {
            return 200; // Default
        }

        foreach ($this->rateLimitsCache as $limit) {
            if ($limit['window_seconds'] == 86400) {
                if ($limit['scope'] === 'user' && $userId && $limit['scope_value'] == $userId) {
                    return (int)$limit['max_exports'];
                }
                if ($limit['scope'] === 'global') {
                    return (int)$limit['max_exports'];
                }
            }
        }

        return 200; // Default
    }

    /**
     * Skapa komplett manifest for en export
     *
     * v3.0.2: Mandatory fields for revision-grade compliance:
     * - snapshot_id
     * - generated_at
     * - season_year
     * - source_max_updated_at
     * - platform_version
     * - calculation_version
     * - data_fingerprint (deterministic)
     *
     * @param string $exportType Typ
     * @param array $data Data
     * @param array $options Optioner
     * @return array Manifest
     */
    public function createManifest(string $exportType, array $data, array $options = []): array {
        $snapshotId = $options['snapshot_id'] ?? null;
        $seasonYear = $options['year'] ?? null;

        // v3.0.2: Deterministic fingerprint (sorterad JSON + stabil encoding)
        $dataFingerprint = $this->calculateDeterministicFingerprint($data);

        // Hamta snapshot-info for source_max_updated_at
        $sourceMaxUpdatedAt = $options['source_max_updated'] ?? null;
        if ($snapshotId && !$sourceMaxUpdatedAt) {
            $sourceMaxUpdatedAt = $this->getSnapshotSourceTimestamp($snapshotId);
        }

        return [
            // ===== MANDATORY FIELDS (v3.0.2 Revision Grade) =====
            'snapshot_id' => $snapshotId,
            'generated_at' => gmdate('Y-m-d\TH:i:s\Z'),
            'season_year' => $seasonYear,
            'source_max_updated_at' => $sourceMaxUpdatedAt,
            'platform_version' => AnalyticsConfig::PLATFORM_VERSION,
            'calculation_version' => AnalyticsConfig::CALCULATION_VERSION,
            'data_fingerprint' => $dataFingerprint,

            // ===== EXPORT METADATA =====
            'export_type' => $exportType,
            'exported_at_local' => date('Y-m-d H:i:s'),
            'timezone' => date_default_timezone_get(),

            // ===== DATA SUMMARY =====
            'row_count' => count($data),
            'columns' => $this->extractColumns($data),

            // ===== FILTERS & PARAMETERS =====
            'series_id' => $options['series_id'] ?? null,
            'filters' => $options['filters'] ?? [],
            'query_hash' => $options['query_hash'] ?? null,

            // ===== REPRODUCIBILITY =====
            'can_reproduce' => !empty($snapshotId),
            'reproducibility_note' => empty($snapshotId)
                ? 'ERROR: No snapshot_id. Export cannot be reproduced.'
                : 'Export kan reproduceras från snapshot #' . $snapshotId .
                  ' så länge pre-aggregaten inte har omräknats.',

            // ===== GDPR & COMPLIANCE =====
            'contains_pii' => $this->containsPII($data),
            'pii_fields' => $this->identifyPIIFields($data),
            'data_retention_days' => 365,
            'gdpr_compliant' => true,

            // ===== VALIDATION =====
            'checksum_algorithm' => 'sha256',
            'encoding' => 'JSON_UNESCAPED_UNICODE | JSON_NUMERIC_CHECK',
            'manifest_version' => '3.0.2',
        ];
    }

    /**
     * Hamta source_max_updated_at fran snapshot
     *
     * @param int $snapshotId
     * @return string|null
     */
    private function getSnapshotSourceTimestamp(int $snapshotId): ?string {
        try {
            $stmt = $this->pdo->prepare("
                SELECT source_max_updated_at FROM analytics_snapshots WHERE id = ?
            ");
            $stmt->execute([$snapshotId]);
            return $stmt->fetchColumn() ?: null;
        } catch (PDOException $e) {
            return null;
        }
    }

    /**
     * Berakna DETERMINISTISK fingerprint for data
     *
     * v3.0.2: Garanterar samma hash for samma data oavsett PHP-version
     * - Sorterar nycklar rekursivt
     * - Anvander stabil JSON encoding
     * - Hanterar floats konsekvent
     *
     * @param array $data Data
     * @return string SHA256 hash
     */
    public function calculateDeterministicFingerprint(array $data): string {
        // Sortera data rekursivt
        $normalized = $this->normalizeForFingerprint($data);

        // Stabil JSON encoding
        $json = json_encode(
            $normalized,
            JSON_UNESCAPED_UNICODE | JSON_NUMERIC_CHECK | JSON_PRESERVE_ZERO_FRACTION
        );

        return hash('sha256', $json);
    }

    /**
     * Normalisera data for fingerprint-berakning
     *
     * @param mixed $data
     * @return mixed
     */
    private function normalizeForFingerprint($data) {
        if (is_array($data)) {
            // Sortera associativa arrayer efter nyckel
            if ($this->isAssociativeArray($data)) {
                ksort($data, SORT_STRING);
            }

            // Rekursivt normalisera alla element
            foreach ($data as $key => $value) {
                $data[$key] = $this->normalizeForFingerprint($value);
            }
        } elseif (is_float($data)) {
            // Avrunda floats for konsekvent precision
            $data = round($data, 10);
        }

        return $data;
    }

    /**
     * Kolla om array ar associativ
     *
     * @param array $arr
     * @return bool
     */
    private function isAssociativeArray(array $arr): bool {
        if (empty($arr)) return false;
        return array_keys($arr) !== range(0, count($arr) - 1);
    }

    /**
     * Berakna fingerprint for data
     *
     * @deprecated Anvand calculateDeterministicFingerprint() for revision-grade
     * @param array $data Data
     * @return string SHA256 hash
     */
    public function calculateFingerprint(array $data): string {
        // v3.0.2: Redirect to deterministic method
        return $this->calculateDeterministicFingerprint($data);
    }

    /**
     * Kolla om data innehaller persondata (PII)
     *
     * @param array $data Data
     * @return bool
     */
    public function containsPII(array $data): bool {
        if (empty($data)) return false;

        $piiFields = AnalyticsConfig::PII_FIELDS ?? [
            'firstname', 'lastname', 'email', 'phone',
            'birth_year', 'birth_date', 'address', 'license_number'
        ];

        $firstRow = is_array($data[0] ?? null) ? $data[0] : [];

        foreach ($piiFields as $field) {
            if (array_key_exists($field, $firstRow)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Identifiera vilka PII-falt som finns i data
     *
     * @param array $data Data
     * @return array Lista over PII-falt
     */
    private function identifyPIIFields(array $data): array {
        if (empty($data)) return [];

        $piiFields = AnalyticsConfig::PII_FIELDS ?? [
            'firstname', 'lastname', 'email', 'phone',
            'birth_year', 'birth_date', 'rider_id', 'name',
            'address', 'license_number'
        ];

        $firstRow = is_array($data[0] ?? null) ? $data[0] : [];
        $found = [];

        foreach ($piiFields as $field) {
            if (array_key_exists($field, $firstRow)) {
                $found[] = $field;
            }
        }

        return $found;
    }

    /**
     * Extrahera kolumnnamn fran data
     *
     * @param array $data Data
     * @return array Kolumnnamn
     */
    private function extractColumns(array $data): array {
        if (empty($data)) return [];
        $firstRow = is_array($data[0] ?? null) ? $data[0] : [];
        return array_keys($firstRow);
    }

    /**
     * Hamta klient-IP
     *
     * @return string|null IP-adress
     */
    private function getClientIP(): ?string {
        // Kolla proxy-headers forst
        $headers = [
            'HTTP_CF_CONNECTING_IP',     // Cloudflare
            'HTTP_X_FORWARDED_FOR',
            'HTTP_X_REAL_IP',
            'REMOTE_ADDR',
        ];

        foreach ($headers as $header) {
            if (!empty($_SERVER[$header])) {
                $ip = $_SERVER[$header];
                // Om flera IPs (proxy chain), ta forsta
                if (strpos($ip, ',') !== false) {
                    $ip = trim(explode(',', $ip)[0]);
                }
                return $ip;
            }
        }

        return null;
    }

    /**
     * Hamta tidigare exporter for en anvandare
     *
     * @param int $userId Anvandar-ID
     * @param int $limit Max antal
     * @return array Exporter
     */
    public function getUserExports(int $userId, int $limit = 50): array {
        $stmt = $this->pdo->prepare("
            SELECT
                id, export_uid, export_type, export_format, filename,
                exported_at, season_year, row_count, contains_pii,
                snapshot_id, status
            FROM analytics_exports
            WHERE exported_by = ?
            ORDER BY exported_at DESC
            LIMIT ?
        ");
        $stmt->execute([$userId, $limit]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta export by UID
     *
     * @param string $exportUid Export UID
     * @return array|null Export data
     */
    public function getExportByUid(string $exportUid): ?array {
        $stmt = $this->pdo->prepare("
            SELECT * FROM analytics_exports WHERE export_uid = ?
        ");
        $stmt->execute([$exportUid]);
        $export = $stmt->fetch(PDO::FETCH_ASSOC);

        return $export ?: null;
    }

    /**
     * Hamta exportstatistik
     *
     * @param string|null $period 'day', 'week', 'month', 'year'
     * @return array Statistik
     */
    public function getExportStats(?string $period = 'month'): array {
        $dateFilter = match($period) {
            'day' => 'DATE(exported_at) = CURDATE()',
            'week' => 'exported_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)',
            'month' => 'exported_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)',
            'year' => 'exported_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)',
            default => '1=1',
        };

        $stmt = $this->pdo->query("
            SELECT
                COUNT(*) as total_exports,
                COUNT(DISTINCT exported_by) as unique_users,
                SUM(row_count) as total_rows,
                SUM(contains_pii) as pii_exports,
                COUNT(DISTINCT export_type) as export_types,
                SUM(CASE WHEN snapshot_id IS NOT NULL THEN 1 ELSE 0 END) as reproducible_exports
            FROM analytics_exports
            WHERE $dateFilter
        ");

        $stats = $stmt->fetch(PDO::FETCH_ASSOC);

        // Reproducibility rate
        $stats['reproducibility_rate'] = $stats['total_exports'] > 0
            ? round(($stats['reproducible_exports'] / $stats['total_exports']) * 100, 1)
            : 0;

        // Top export types
        $stmt = $this->pdo->query("
            SELECT export_type, COUNT(*) as count
            FROM analytics_exports
            WHERE $dateFilter
            GROUP BY export_type
            ORDER BY count DESC
            LIMIT 5
        ");
        $stats['top_types'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

        return $stats;
    }

    /**
     * Verifiera en export mot dess fingerprint
     *
     * @param int $exportId Export-ID
     * @param array $data Data att verifiera
     * @return bool Matchar fingerprint
     */
    public function verifyExport(int $exportId, array $data): bool {
        $stmt = $this->pdo->prepare("
            SELECT data_fingerprint FROM analytics_exports WHERE id = ?
        ");
        $stmt->execute([$exportId]);
        $storedFingerprint = $stmt->fetchColumn();

        if (!$storedFingerprint) {
            return false;
        }

        return $this->calculateFingerprint($data) === $storedFingerprint;
    }

    /**
     * Verifiera export by UID
     *
     * @param string $exportUid Export UID
     * @param array $data Data att verifiera
     * @return array Verification result
     */
    public function verifyExportByUid(string $exportUid, array $data): array {
        $export = $this->getExportByUid($exportUid);

        if (!$export) {
            return [
                'valid' => false,
                'error' => 'Export not found',
            ];
        }

        $currentFingerprint = $this->calculateFingerprint($data);
        $matches = $currentFingerprint === $export['data_fingerprint'];

        return [
            'valid' => $matches,
            'export_uid' => $exportUid,
            'original_fingerprint' => $export['data_fingerprint'],
            'current_fingerprint' => $currentFingerprint,
            'exported_at' => $export['exported_at'],
            'snapshot_id' => $export['snapshot_id'],
            'can_reproduce' => !empty($export['snapshot_id']),
        ];
    }

    /**
     * Hamta manifest for en export
     *
     * @param int $exportId Export-ID
     * @return array|null Manifest eller null
     */
    public function getManifest(int $exportId): ?array {
        $stmt = $this->pdo->prepare("
            SELECT manifest FROM analytics_exports WHERE id = ?
        ");
        $stmt->execute([$exportId]);
        $manifest = $stmt->fetchColumn();

        return $manifest ? json_decode($manifest, true) : null;
    }

    /**
     * Hamta manifest by UID
     *
     * @param string $exportUid Export UID
     * @return array|null Manifest
     */
    public function getManifestByUid(string $exportUid): ?array {
        $stmt = $this->pdo->prepare("
            SELECT manifest FROM analytics_exports WHERE export_uid = ?
        ");
        $stmt->execute([$exportUid]);
        $manifest = $stmt->fetchColumn();

        return $manifest ? json_decode($manifest, true) : null;
    }

    /**
     * Satt rate limits (for admin/testing)
     *
     * v3.0.2: Uppdaterar databas-baserade rate limits
     *
     * @param int $hourly Max per timme
     * @param int $daily Max per dag
     * @param string $scope 'global', 'user', 'ip', 'role'
     * @param string|null $scopeValue Scope-varde (user_id, roll, etc)
     */
    public function setRateLimits(int $hourly, int $daily, string $scope = 'global', ?string $scopeValue = null): void {
        try {
            // Uppdatera hourly
            $stmt = $this->pdo->prepare("
                INSERT INTO export_rate_limits (scope, scope_value, max_exports, window_seconds, description)
                VALUES (?, ?, ?, 3600, 'Set via setRateLimits()')
                ON DUPLICATE KEY UPDATE max_exports = VALUES(max_exports), updated_at = NOW()
            ");
            $stmt->execute([$scope, $scopeValue, $hourly]);

            // Uppdatera daily
            $stmt = $this->pdo->prepare("
                INSERT INTO export_rate_limits (scope, scope_value, max_exports, window_seconds, description)
                VALUES (?, ?, ?, 86400, 'Set via setRateLimits()')
                ON DUPLICATE KEY UPDATE max_exports = VALUES(max_exports), updated_at = NOW()
            ");
            $stmt->execute([$scope, $scopeValue === null ? 'daily' : $scopeValue . '_daily', $daily]);

            // Reload cache
            $this->loadRateLimitsFromDb();
        } catch (PDOException $e) {
            error_log('ExportLogger::setRateLimits failed: ' . $e->getMessage());
        }
    }

    /**
     * Inaktivera snapshot requirement
     *
     * @deprecated I v3.0.2 ar snapshot_id ALLTID obligatoriskt. Denna metod loggar varning.
     * @param bool $require
     */
    public function setRequireSnapshotId(bool $require): void {
        if (!$require) {
            error_log('WARNING: setRequireSnapshotId(false) called. In v3.0.2, snapshot_id is ALWAYS required.');
        }
        // I v3.0.2 ar detta ignorerat - snapshot_id ar alltid obligatoriskt
        $this->requireSnapshotId = true;
    }

    /**
     * Hamta rate limit source (for diagnostik)
     *
     * @return string 'database' eller 'config'
     */
    public function getRateLimitSource(): string {
        return $this->rateLimitSource;
    }

    /**
     * Reload rate limits fran databas
     */
    public function reloadRateLimits(): void {
        $this->loadRateLimitsFromDb();
    }
}
