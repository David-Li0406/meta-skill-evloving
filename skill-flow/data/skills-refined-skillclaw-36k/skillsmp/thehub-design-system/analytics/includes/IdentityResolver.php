<?php
/**
 * IdentityResolver
 *
 * ALLA analytics-queries ska anvanda denna klass for att
 * sakerstalla att vi alltid raknar pa canonical rider.
 *
 * Denna klass hanterar:
 * - Lookup av canonical rider_id (huvudprofil)
 * - Registrering av merges (sammanslagning av dubbletter)
 * - Klubbhistorik (vilken klubb en rider tillhorde vid en viss tid)
 * - Hitta potentiella dubbletter for manuell granskning
 * - v3.0.1: Queue recalc efter merge (Merge→Recalc policy)
 *
 * KRITISKT: AnalyticsEngine far ALDRIG skriva original rider_id till
 * analytics-tabeller. ALLA writes maste ga via getCanonicalId().
 *
 * @package TheHUB Analytics
 * @version 3.0.1
 */

class IdentityResolver {
    private PDO $pdo;
    private array $cache = [];
    private int $cacheHits = 0;
    private int $cacheMisses = 0;

    /**
     * Constructor
     *
     * @param PDO $pdo Databasanslutning (INTE global!)
     */
    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }

    /**
     * Hamta canonical rider_id for en given rider
     * Om ingen merge finns, returneras original id
     *
     * Denna metod anvander en intern cache for att minimera databasanrop.
     *
     * @param int $riderId Original rider_id
     * @return int Canonical rider_id
     */
    public function getCanonicalId(int $riderId): int {
        if (isset($this->cache[$riderId])) {
            $this->cacheHits++;
            return $this->cache[$riderId];
        }

        $this->cacheMisses++;

        $stmt = $this->pdo->prepare("
            SELECT canonical_rider_id
            FROM rider_merge_map
            WHERE merged_rider_id = ? AND status = 'approved'
        ");
        $stmt->execute([$riderId]);
        $result = $stmt->fetchColumn();

        $canonical = $result ? (int)$result : $riderId;
        $this->cache[$riderId] = $canonical;

        return $canonical;
    }

    /**
     * Hamta alla merged rider_ids for en canonical rider
     *
     * @param int $canonicalRiderId Canonical rider_id
     * @return array Array av merged rider_ids
     */
    public function getMergedIds(int $canonicalRiderId): array {
        $stmt = $this->pdo->prepare("
            SELECT merged_rider_id
            FROM rider_merge_map
            WHERE canonical_rider_id = ? AND status = 'approved'
        ");
        $stmt->execute([$canonicalRiderId]);
        return $stmt->fetchAll(PDO::FETCH_COLUMN);
    }

    /**
     * Kontrollera om en rider ar en dubblett (har mergats till annan)
     *
     * @param int $riderId Rider att kontrollera
     * @return bool True om rider ar en dubblett
     */
    public function isMerged(int $riderId): bool {
        return $this->getCanonicalId($riderId) !== $riderId;
    }

    /**
     * Registrera en merge
     *
     * @param int $canonicalId Canonical (huvud) rider_id
     * @param int $mergedId Dubblett rider_id
     * @param string $reason Anledning (t.ex. 'same_uci_id', 'manual', 'name_match')
     * @param float $confidence Konfidens 0-100
     * @param string|null $by Anvandare som skapade merge
     * @return bool True om merge lyckades
     * @throws Exception Vid databasfel
     */
    public function merge(int $canonicalId, int $mergedId, string $reason, float $confidence = 100.0, ?string $by = null): bool {
        // Validering
        if ($canonicalId === $mergedId) {
            throw new InvalidArgumentException("Kan inte merga en rider med sig sjalv");
        }

        // Kolla att canonical inte sjalv ar mergad
        $existingMerge = $this->getCanonicalId($canonicalId);
        if ($existingMerge !== $canonicalId) {
            throw new InvalidArgumentException("Canonical rider {$canonicalId} ar redan mergad till {$existingMerge}");
        }

        try {
            $this->pdo->beginTransaction();

            // Satt in merge
            $stmt = $this->pdo->prepare("
                INSERT INTO rider_merge_map
                (canonical_rider_id, merged_rider_id, reason, confidence, merged_by, status)
                VALUES (?, ?, ?, ?, ?, 'approved')
                ON DUPLICATE KEY UPDATE
                    canonical_rider_id = VALUES(canonical_rider_id),
                    reason = VALUES(reason),
                    confidence = VALUES(confidence),
                    merged_by = VALUES(merged_by),
                    merged_at = CURRENT_TIMESTAMP
            ");
            $stmt->execute([$canonicalId, $mergedId, $reason, $confidence, $by]);

            // Logga i audit
            $stmt = $this->pdo->prepare("
                INSERT INTO rider_identity_audit (rider_id, action, details, created_by)
                VALUES (?, 'merge', ?, ?)
            ");
            $stmt->execute([
                $mergedId,
                json_encode([
                    'canonical' => $canonicalId,
                    'reason' => $reason,
                    'confidence' => $confidence
                ], JSON_UNESCAPED_UNICODE),
                $by
            ]);

            $this->pdo->commit();

            // Rensa cache
            unset($this->cache[$mergedId]);

            // v3.0.1: Queue recalc for affected riders
            $this->queueRecalc(
                'merge',
                'rider',
                $mergedId,
                [$canonicalId, $mergedId],
                $by
            );

            return true;
        } catch (Exception $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    /**
     * Ta bort en merge (aterstall rider som separat)
     *
     * @param int $mergedId Rider som ska aterstaallas
     * @param string|null $by Anvandare som tog bort merge
     * @return bool True om unmerge lyckades
     */
    public function unmerge(int $mergedId, ?string $by = null): bool {
        try {
            $this->pdo->beginTransaction();

            // Hitta befintlig merge
            $stmt = $this->pdo->prepare("
                SELECT canonical_rider_id FROM rider_merge_map
                WHERE merged_rider_id = ? AND status = 'approved'
            ");
            $stmt->execute([$mergedId]);
            $canonical = $stmt->fetchColumn();

            if (!$canonical) {
                $this->pdo->rollBack();
                return false; // Ingen merge att ta bort
            }

            // Ta bort merge
            $stmt = $this->pdo->prepare("
                DELETE FROM rider_merge_map WHERE merged_rider_id = ?
            ");
            $stmt->execute([$mergedId]);

            // Logga i audit
            $stmt = $this->pdo->prepare("
                INSERT INTO rider_identity_audit (rider_id, action, details, created_by)
                VALUES (?, 'unmerge', ?, ?)
            ");
            $stmt->execute([
                $mergedId,
                json_encode(['previous_canonical' => $canonical], JSON_UNESCAPED_UNICODE),
                $by
            ]);

            $this->pdo->commit();

            // Rensa cache
            unset($this->cache[$mergedId]);

            // v3.0.1: Queue recalc for unmerged riders
            $this->queueRecalc(
                'merge',
                'rider',
                $mergedId,
                [$canonical, $mergedId],
                $by
            );

            return true;
        } catch (Exception $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    /**
     * Hamta klubb for en rider vid ett givet datum
     * Anvander rider_affiliations om tillgangligt, annars riders.club_id
     *
     * @param int $riderId Rider (original eller canonical)
     * @param string $date Datum (YYYY-MM-DD)
     * @return int|null Club ID eller null om ingen klubb
     */
    public function getClubAtDate(int $riderId, string $date): ?int {
        $canonicalId = $this->getCanonicalId($riderId);

        // Forsok med affiliations forst
        $stmt = $this->pdo->prepare("
            SELECT club_id FROM rider_affiliations
            WHERE rider_id = ?
              AND (valid_from IS NULL OR valid_from <= ?)
              AND (valid_to IS NULL OR valid_to >= ?)
            ORDER BY valid_from DESC
            LIMIT 1
        ");
        $stmt->execute([$canonicalId, $date, $date]);
        $result = $stmt->fetchColumn();

        if ($result) {
            return (int)$result;
        }

        // Fallback till riders.club_id
        $stmt = $this->pdo->prepare("SELECT club_id FROM riders WHERE id = ?");
        $stmt->execute([$canonicalId]);
        $result = $stmt->fetchColumn();

        return $result ? (int)$result : null;
    }

    /**
     * Registrera klubbhistorik for en rider
     *
     * @param int $riderId Canonical rider_id
     * @param int $clubId Klubb
     * @param string|null $validFrom Startdatum (YYYY-MM-DD)
     * @param string|null $validTo Slutdatum (YYYY-MM-DD)
     * @param string $source Kalla (manual, derived, import, scf)
     * @return int Inserted ID
     */
    public function addAffiliation(int $riderId, int $clubId, ?string $validFrom = null, ?string $validTo = null, string $source = 'derived'): int {
        $canonicalId = $this->getCanonicalId($riderId);

        $stmt = $this->pdo->prepare("
            INSERT INTO rider_affiliations (rider_id, club_id, valid_from, valid_to, source)
            VALUES (?, ?, ?, ?, ?)
        ");
        $stmt->execute([$canonicalId, $clubId, $validFrom, $validTo, $source]);

        return (int)$this->pdo->lastInsertId();
    }

    /**
     * Hamta alla affiliations for en rider
     *
     * @param int $riderId Rider
     * @return array Array av affiliations
     */
    public function getAffiliations(int $riderId): array {
        $canonicalId = $this->getCanonicalId($riderId);

        $stmt = $this->pdo->prepare("
            SELECT ra.*, c.name as club_name
            FROM rider_affiliations ra
            LEFT JOIN clubs c ON ra.club_id = c.id
            WHERE ra.rider_id = ?
            ORDER BY ra.valid_from DESC
        ");
        $stmt->execute([$canonicalId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hitta potentiella dubbletter for manuell granskning
     *
     * Hittar riders som matchar pa:
     * - Samma UCI ID
     * - Samma licensnummer
     * - Exakt samma namn + fodelsear
     *
     * @param int $limit Max antal att returnera
     * @return array Array av potentiella dubbletter
     */
    public function findPotentialDuplicates(int $limit = 100): array {
        return $this->pdo->query("
            SELECT
                r1.id AS rider1_id,
                CONCAT(r1.firstname, ' ', r1.lastname) AS rider1_name,
                r1.club_id AS rider1_club,
                r1.uci_id AS rider1_uci,
                r1.license_number AS rider1_license,
                r2.id AS rider2_id,
                CONCAT(r2.firstname, ' ', r2.lastname) AS rider2_name,
                r2.club_id AS rider2_club,
                r2.uci_id AS rider2_uci,
                r2.license_number AS rider2_license,
                CASE
                    WHEN r1.uci_id = r2.uci_id AND r1.uci_id IS NOT NULL AND r1.uci_id != '' THEN 'uci_match'
                    WHEN r1.license_number = r2.license_number AND r1.license_number IS NOT NULL AND r1.license_number != '' THEN 'license_match'
                    ELSE 'name_match'
                END AS match_type
            FROM riders r1
            JOIN riders r2 ON r1.id < r2.id
            WHERE
                (r1.uci_id = r2.uci_id AND r1.uci_id IS NOT NULL AND r1.uci_id != '')
                OR (r1.license_number = r2.license_number AND r1.license_number IS NOT NULL AND r1.license_number != '')
                OR (
                    LOWER(r1.firstname) = LOWER(r2.firstname)
                    AND LOWER(r1.lastname) = LOWER(r2.lastname)
                    AND r1.birth_year = r2.birth_year
                    AND r1.birth_year IS NOT NULL
                )
            AND r1.id NOT IN (SELECT merged_rider_id FROM rider_merge_map WHERE status = 'approved')
            AND r2.id NOT IN (SELECT merged_rider_id FROM rider_merge_map WHERE status = 'approved')
            LIMIT $limit
        ")->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Bygg eller uppdatera rider_affiliations fran results-tabellen
     * Harddar klubbhistorik baserat pa vilken klubb en rider hade
     * nar de deltog i olika events.
     *
     * @param int|null $riderId Specifik rider, eller null for alla
     * @return int Antal affiliations skapade
     */
    public function deriveAffiliationsFromResults(?int $riderId = null): int {
        $count = 0;

        // Hamta alla unika kombinationer av rider + klubb + datum fran results
        $sql = "
            SELECT DISTINCT
                v.canonical_rider_id as rider_id,
                res.club_id,
                MIN(e.date) as first_seen,
                MAX(e.date) as last_seen
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE res.club_id IS NOT NULL
        ";

        if ($riderId !== null) {
            $sql .= " AND v.canonical_rider_id = ?";
        }

        $sql .= " GROUP BY v.canonical_rider_id, res.club_id ORDER BY rider_id, first_seen";

        $stmt = $this->pdo->prepare($sql);

        if ($riderId !== null) {
            $stmt->execute([$riderId]);
        } else {
            $stmt->execute();
        }

        $affiliations = $stmt->fetchAll(PDO::FETCH_ASSOC);

        foreach ($affiliations as $aff) {
            // Kolla om affiliering redan finns
            $existsStmt = $this->pdo->prepare("
                SELECT id FROM rider_affiliations
                WHERE rider_id = ? AND club_id = ? AND source = 'derived'
            ");
            $existsStmt->execute([$aff['rider_id'], $aff['club_id']]);

            if (!$existsStmt->fetch()) {
                $this->addAffiliation(
                    $aff['rider_id'],
                    $aff['club_id'],
                    $aff['first_seen'],
                    $aff['last_seen'],
                    'derived'
                );
                $count++;
            }
        }

        return $count;
    }

    /**
     * Hamta cache-statistik (for debugging/monitoring)
     *
     * @return array Cache stats
     */
    public function getCacheStats(): array {
        return [
            'size' => count($this->cache),
            'hits' => $this->cacheHits,
            'misses' => $this->cacheMisses,
            'hit_rate' => $this->cacheHits + $this->cacheMisses > 0
                ? round($this->cacheHits / ($this->cacheHits + $this->cacheMisses) * 100, 2)
                : 0
        ];
    }

    /**
     * Rensa cache (anvand efter bulk-operationer)
     */
    public function clearCache(): void {
        $this->cache = [];
    }

    // =========================================================================
    // v3.0.1: Recalc Queue Methods (Merge→Recalc Policy)
    // =========================================================================

    /**
     * Queue en recalculation for analytics-tabeller
     *
     * v3.0.2: Deterministisk och idempotent
     * - Checksum for deduplication
     * - Spårar years_source (stats/results/manual)
     * - Prioritet baserad på trigger_type
     *
     * @param string $triggerType Vad som triggade (merge, import, manual, correction)
     * @param string $triggerEntity Entitetstyp (rider, event, result)
     * @param int $triggerEntityId Entitetens ID
     * @param array $affectedRiderIds Lista med paverkade rider IDs
     * @param string|null $createdBy Anvandare som skapade
     * @return int Queue entry ID (-1 om redan i kö)
     */
    public function queueRecalc(
        string $triggerType,
        string $triggerEntity,
        int $triggerEntityId,
        array $affectedRiderIds,
        ?string $createdBy = null
    ): int {
        // v3.0.2: Hitta ar med source-spårning
        $yearsResult = $this->findAffectedYearsWithSource($affectedRiderIds);
        $affectedYears = $yearsResult['years'];
        $yearsSource = $yearsResult['source'];

        // Skapa DETERMINISTISK checksum for deduplication
        // Sortera rider IDs för konsekvent hash
        sort($affectedRiderIds, SORT_NUMERIC);
        $checksum = hash('sha256', json_encode([
            'type' => $triggerType,
            'entity' => $triggerEntity,
            'entity_id' => $triggerEntityId,
            'riders' => $affectedRiderIds,
        ], JSON_NUMERIC_CHECK));

        // Kolla om samma recalc redan finns i kon (pending)
        $existsStmt = $this->pdo->prepare("
            SELECT id FROM analytics_recalc_queue
            WHERE checksum = ? AND status = 'pending'
        ");
        $existsStmt->execute([$checksum]);

        if ($existsStmt->fetch()) {
            // Redan i kon - IDEMPOTENT beteende
            return -1;
        }

        // v3.0.2: Inkludera years_source i INSERT
        $stmt = $this->pdo->prepare("
            INSERT INTO analytics_recalc_queue (
                trigger_type, trigger_entity, trigger_entity_id,
                affected_rider_ids, affected_years, years_source,
                priority, status, created_by, checksum
            ) VALUES (
                ?, ?, ?,
                ?, ?, ?,
                ?, 'pending', ?, ?
            )
        ");

        // Prioritet: merge = 3 (hög), correction = 4, import/manual = 5
        $priority = match($triggerType) {
            'merge' => 3,
            'correction' => 4,
            default => 5,
        };

        $stmt->execute([
            $triggerType,
            $triggerEntity,
            $triggerEntityId,
            json_encode($affectedRiderIds),
            json_encode($affectedYears),
            $yearsSource,
            $priority,
            $createdBy,
            $checksum,
        ]);

        return (int)$this->pdo->lastInsertId();
    }

    /**
     * Hitta alla ar som paverkas av andringar for givna riders
     *
     * v3.0.2: Deterministisk logik med fallback
     * 1. Forsoker hamta fran rider_yearly_stats (snabbt)
     * 2. Fallback till raw results om stats saknas
     * 3. Returnerar ocksa source-info for spårbarhet
     *
     * @param array $riderIds Lista med rider IDs
     * @return array Lista med ar (t.ex. [2024, 2025])
     */
    private function findAffectedYears(array $riderIds): array {
        if (empty($riderIds)) {
            return [];
        }

        $result = $this->findAffectedYearsWithSource($riderIds);
        return $result['years'];
    }

    /**
     * Hitta affected years med source-information
     *
     * @param array $riderIds Lista med rider IDs
     * @return array ['years' => [...], 'source' => 'stats'|'results'|'manual']
     */
    public function findAffectedYearsWithSource(array $riderIds): array {
        if (empty($riderIds)) {
            return ['years' => [], 'source' => 'manual'];
        }

        $placeholders = implode(',', array_fill(0, count($riderIds), '?'));

        // Forst: Forsoker hamta fran rider_yearly_stats (primär källa)
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT season_year
            FROM rider_yearly_stats
            WHERE rider_id IN ($placeholders)
            ORDER BY season_year DESC
        ");
        $stmt->execute($riderIds);
        $years = $stmt->fetchAll(PDO::FETCH_COLUMN);

        if (!empty($years)) {
            return [
                'years' => array_map('intval', $years),
                'source' => 'stats',
            ];
        }

        // Fallback: Hamta fran raw results om stats saknas
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT YEAR(e.date) as year
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id IN ($placeholders)
               OR res.cyclist_id IN ($placeholders)
            ORDER BY year DESC
        ");
        // Dubbla parameters for bade canonical och original
        $params = array_merge($riderIds, $riderIds);
        $stmt->execute($params);
        $years = $stmt->fetchAll(PDO::FETCH_COLUMN);

        if (!empty($years)) {
            return [
                'years' => array_map('intval', array_filter($years)),
                'source' => 'results',
            ];
        }

        // Inget hittat - returnera tomt
        return ['years' => [], 'source' => 'manual'];
    }

    /**
     * Hamta pending recalc jobs
     *
     * @param int $limit Max antal
     * @return array Lista med jobs
     */
    public function getPendingRecalcJobs(int $limit = 10): array {
        $stmt = $this->pdo->prepare("
            SELECT *
            FROM analytics_recalc_queue
            WHERE status = 'pending'
            ORDER BY priority ASC, created_at ASC
            LIMIT ?
        ");
        $stmt->execute([$limit]);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Markera ett recalc job som processing
     *
     * @param int $jobId Job ID
     * @return bool Success
     */
    public function markRecalcStarted(int $jobId): bool {
        $stmt = $this->pdo->prepare("
            UPDATE analytics_recalc_queue
            SET status = 'processing', started_at = NOW()
            WHERE id = ? AND status = 'pending'
        ");
        $stmt->execute([$jobId]);

        return $stmt->rowCount() > 0;
    }

    /**
     * Markera ett recalc job som completed
     *
     * @param int $jobId Job ID
     * @param int $rowsAffected Antal rader som paverkades
     * @param int $executionTimeMs Kortid i millisekunder
     * @return bool Success
     */
    public function markRecalcCompleted(int $jobId, int $rowsAffected, int $executionTimeMs): bool {
        $stmt = $this->pdo->prepare("
            UPDATE analytics_recalc_queue
            SET status = 'completed',
                completed_at = NOW(),
                rows_affected = ?,
                execution_time_ms = ?
            WHERE id = ?
        ");
        $stmt->execute([$rowsAffected, $executionTimeMs, $jobId]);

        return $stmt->rowCount() > 0;
    }

    /**
     * Markera ett recalc job som failed
     *
     * @param int $jobId Job ID
     * @param string $errorMessage Felmeddelande
     * @return bool Success
     */
    public function markRecalcFailed(int $jobId, string $errorMessage): bool {
        $stmt = $this->pdo->prepare("
            UPDATE analytics_recalc_queue
            SET status = 'failed',
                completed_at = NOW(),
                error_message = ?
            WHERE id = ?
        ");
        $stmt->execute([$errorMessage, $jobId]);

        return $stmt->rowCount() > 0;
    }

    /**
     * Hamta recalc queue statistik
     *
     * @return array Statistik
     */
    public function getRecalcQueueStats(): array {
        $stmt = $this->pdo->query("
            SELECT
                status,
                COUNT(*) as count,
                AVG(execution_time_ms) as avg_time_ms,
                SUM(rows_affected) as total_rows
            FROM analytics_recalc_queue
            GROUP BY status
        ");

        $stats = [
            'pending' => 0,
            'processing' => 0,
            'completed' => 0,
            'failed' => 0,
            'total_processed_rows' => 0,
            'avg_execution_time_ms' => 0,
        ];

        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $stats[$row['status']] = (int)$row['count'];
            if ($row['status'] === 'completed') {
                $stats['total_processed_rows'] = (int)$row['total_rows'];
                $stats['avg_execution_time_ms'] = round((float)$row['avg_time_ms'], 2);
            }
        }

        return $stats;
    }
}
