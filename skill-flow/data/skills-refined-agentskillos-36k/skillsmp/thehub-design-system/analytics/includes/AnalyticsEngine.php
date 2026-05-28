<?php
/**
 * AnalyticsEngine
 *
 * Karnklass for all analytics-berakning i TheHUB.
 * Beraknar och lagrar statistik for riders, serier, klubbar och venues.
 *
 * KRITISKT:
 * - Anvander IdentityResolver for ALLA rider-lookups
 * - Skriver ALLTID canonical rider_id till analytics-tabeller
 * - Markerar alla berakningar med calculation_version
 * - Loggar alla korningar till analytics_cron_runs
 *
 * v3.0.1: Heartbeat, timeout handling, recalc queue processing
 * v3.1.0: First Season Journey + Longitudinal Journey analysis
 *
 * @package TheHUB Analytics
 * @version 3.1.0
 */

require_once __DIR__ . '/IdentityResolver.php';
require_once __DIR__ . '/sql-runner.php';

class AnalyticsEngine {
    private PDO $pdo;
    private IdentityResolver $identityResolver;
    private string $calculationVersion = 'v1';
    private ?string $currentJobName = null;
    private ?int $currentJobId = null;
    private bool $nonBlockingMode = false;
    private bool $forceRerun = false;

    /**
     * Constructor
     *
     * @param PDO $pdo Databasanslutning (INTE global!)
     */
    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
        $this->identityResolver = new IdentityResolver($pdo);
    }

    /**
     * Aktivera icke-blockerande lage
     *
     * Satter READ UNCOMMITTED isolation level sa att analytics-fragor
     * inte lasar tabeller och blockerar resten av sidan.
     * Dirty reads ar OK for analytics - vi behover inte exakt precision.
     */
    public function enableNonBlockingMode(): void {
        $this->pdo->exec("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED");
        $this->nonBlockingMode = true;
    }

    /**
     * Aterstall normal isolation level
     */
    public function disableNonBlockingMode(): void {
        $this->pdo->exec("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ");
        $this->nonBlockingMode = false;
    }

    /**
     * Satt force-rerun flagga
     * Om true, kors jobb om aven om de redan ar klara
     */
    public function setForceRerun(bool $force): void {
        $this->forceRerun = $force;
    }

    /**
     * Hamta force-rerun flagga
     */
    public function getForceRerun(): bool {
        return $this->forceRerun;
    }

    // =========================================================================
    // JOBB-HANTERING
    // =========================================================================

    /**
     * Starta ett analytics-jobb (for loggning och las)
     *
     * @param string $jobName Jobbnamn (t.ex. 'yearly-stats')
     * @param string $runKey Unik nyckel (t.ex. '2025')
     * @param bool $force Tvinga omkorning aven om redan klar
     * @return int|false Job ID eller false om redan kors/klar
     */
    public function startJob(string $jobName, string $runKey, bool $force = false): int|false {
        // Kolla om jobb redan kors eller ar klart
        $stmt = $this->pdo->prepare("
            SELECT id, status FROM analytics_cron_runs
            WHERE job_name = ? AND run_key = ?
        ");
        $stmt->execute([$jobName, $runKey]);
        $existing = $stmt->fetch();

        if ($existing) {
            // Om jobbet pagar, avbryt
            if ($existing['status'] === 'started') {
                return false;
            }

            // Om jobbet ar klart och vi inte tvingas om, hoppa over
            if ($existing['status'] === 'success' && !$force) {
                return false;
            }

            // Uppdatera befintligt jobb (force eller failed)
            $stmt = $this->pdo->prepare("
                UPDATE analytics_cron_runs
                SET status = 'started',
                    started_at = CURRENT_TIMESTAMP,
                    finished_at = NULL,
                    duration_ms = NULL,
                    rows_affected = 0,
                    log = NULL
                WHERE id = ?
            ");
            $stmt->execute([$existing['id']]);
            $this->currentJobId = (int)$existing['id'];
        } else {
            // Skapa nytt jobb
            $stmt = $this->pdo->prepare("
                INSERT INTO analytics_cron_runs (job_name, run_key, status)
                VALUES (?, ?, 'started')
            ");
            $stmt->execute([$jobName, $runKey]);
            $this->currentJobId = (int)$this->pdo->lastInsertId();
        }

        $this->currentJobName = $jobName;
        return $this->currentJobId;
    }

    /**
     * Avsluta ett analytics-jobb
     *
     * @param string $status 'success' eller 'failed'
     * @param int $rowsAffected Antal rader paverkade
     * @param array $log Extra loggdata
     */
    public function endJob(string $status, int $rowsAffected = 0, array $log = []): void {
        if (!$this->currentJobId) return;

        $stmt = $this->pdo->prepare("
            UPDATE analytics_cron_runs
            SET status = ?,
                finished_at = CURRENT_TIMESTAMP,
                duration_ms = TIMESTAMPDIFF(MICROSECOND, started_at, CURRENT_TIMESTAMP) / 1000,
                rows_affected = ?,
                log = ?
            WHERE id = ?
        ");
        $stmt->execute([
            $status,
            $rowsAffected,
            json_encode($log, JSON_UNESCAPED_UNICODE),
            $this->currentJobId
        ]);

        $this->currentJobName = null;
        $this->currentJobId = null;
    }

    // =========================================================================
    // ARLIG STATISTIK
    // =========================================================================

    /**
     * Berakna yearly stats for alla riders ett visst ar
     *
     * Fyller i rider_yearly_stats med:
     * - total_events, total_series, total_points
     * - best_position, avg_position
     * - primary_discipline, primary_series_id
     * - is_rookie, is_retained
     *
     * @param int $year Sasong att berakna
     * @param callable|null $progressCallback Callback for progress (int $current, int $total)
     * @return int Antal rader skapade/uppdaterade
     */
    public function calculateYearlyStats(int $year, ?callable $progressCallback = null): int {
        $jobId = $this->startJob('yearly-stats', (string)$year, $this->forceRerun);
        if ($jobId === false) {
            // Job already running or completed - skip
            return 0;
        }

        $count = 0;

        try {
            // Hamta alla unika riders som deltog detta ar
            $riders = $this->pdo->query("
                SELECT DISTINCT v.canonical_rider_id as rider_id
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE YEAR(e.date) = $year
            ")->fetchAll(PDO::FETCH_COLUMN);

            $total = count($riders);
            $processed = 0;

            foreach ($riders as $riderId) {
                $stats = $this->calculateSingleRiderYearlyStats($riderId, $year);

                if ($stats) {
                    $this->upsertRiderYearlyStats($riderId, $year, $stats);
                    $count++;
                }

                $processed++;

                // Report progress every 100 riders
                if ($progressCallback && ($processed % 100 === 0 || $processed === $total)) {
                    $progressCallback($processed, $total);
                }
            }

            $this->endJob('success', $count, [
                'year' => $year,
                'riders_processed' => count($riders)
            ]);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    /**
     * Berakna statistik for en enskild rider ett ar
     */
    private function calculateSingleRiderYearlyStats(int $riderId, int $year): ?array {
        // Total events och poang
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(DISTINCT res.event_id) as total_events,
                COUNT(DISTINCT e.series_id) as total_series,
                SUM(COALESCE(res.points, 0)) as total_points,
                MIN(res.position) as best_position,
                AVG(res.position) as avg_position
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND res.position > 0
        ");
        $stmt->execute([$riderId, $year]);
        $basic = $stmt->fetch();

        if (!$basic || $basic['total_events'] == 0) {
            return null;
        }

        // Primary discipline (mest deltaganden)
        $stmt = $this->pdo->prepare("
            SELECT e.discipline, COUNT(*) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND e.discipline IS NOT NULL
            GROUP BY e.discipline
            ORDER BY cnt DESC
            LIMIT 1
        ");
        $stmt->execute([$riderId, $year]);
        $discipline = $stmt->fetch();

        // Primary series (mest deltaganden)
        $stmt = $this->pdo->prepare("
            SELECT e.series_id, COUNT(*) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND e.series_id IS NOT NULL
            GROUP BY e.series_id
            ORDER BY cnt DESC
            LIMIT 1
        ");
        $stmt->execute([$riderId, $year]);
        $series = $stmt->fetch();

        // Is rookie? (forsta aret)
        $isRookie = $this->isRookie($riderId, $year) ? 1 : 0;

        // Is retained? (aterkom fran forra aret)
        $isRetained = $this->wasRetained($riderId, $year) ? 1 : 0;

        return [
            'total_events' => (int)$basic['total_events'],
            'total_series' => (int)$basic['total_series'],
            'total_points' => (float)$basic['total_points'],
            'best_position' => $basic['best_position'] ? (int)$basic['best_position'] : null,
            'avg_position' => $basic['avg_position'] ? round($basic['avg_position'], 2) : null,
            'primary_discipline' => $discipline ? $discipline['discipline'] : null,
            'primary_series_id' => $series ? (int)$series['series_id'] : null,
            'is_rookie' => $isRookie,
            'is_retained' => $isRetained
        ];
    }

    /**
     * Upsert rider yearly stats
     */
    private function upsertRiderYearlyStats(int $riderId, int $year, array $stats): void {
        $stmt = $this->pdo->prepare("
            INSERT INTO rider_yearly_stats (
                rider_id, season_year, total_events, total_series, total_points,
                best_position, avg_position, primary_discipline, primary_series_id,
                is_rookie, is_retained, calculation_version, calculated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
            )
            ON DUPLICATE KEY UPDATE
                total_events = VALUES(total_events),
                total_series = VALUES(total_series),
                total_points = VALUES(total_points),
                best_position = VALUES(best_position),
                avg_position = VALUES(avg_position),
                primary_discipline = VALUES(primary_discipline),
                primary_series_id = VALUES(primary_series_id),
                is_rookie = VALUES(is_rookie),
                is_retained = VALUES(is_retained),
                calculation_version = VALUES(calculation_version),
                calculated_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
        ");

        $stmt->execute([
            $riderId,
            $year,
            $stats['total_events'],
            $stats['total_series'],
            $stats['total_points'],
            $stats['best_position'],
            $stats['avg_position'],
            $stats['primary_discipline'],
            $stats['primary_series_id'],
            $stats['is_rookie'],
            $stats['is_retained'],
            $this->calculationVersion
        ]);
    }

    // =========================================================================
    // SERIEDELTAGANDE
    // =========================================================================

    /**
     * Berakna series participation for ett ar
     *
     * @param int $year Sasong
     * @param callable|null $progressCallback Callback for progress (int $current, int $total)
     * @return int Antal rader skapade
     */
    public function calculateSeriesParticipation(int $year, ?callable $progressCallback = null): int {
        $jobId = $this->startJob('series-participation', (string)$year, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;

        try {
            // Hamta alla rider-serie kombinationer for aret
            $participations = $this->pdo->query("
                SELECT
                    v.canonical_rider_id as rider_id,
                    e.series_id,
                    COUNT(DISTINCT res.event_id) as events_attended,
                    MIN(e.date) as first_event_date,
                    MAX(e.date) as last_event_date,
                    SUM(COALESCE(res.points, 0)) as total_points
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE YEAR(e.date) = $year
                  AND e.series_id IS NOT NULL
                GROUP BY v.canonical_rider_id, e.series_id
            ")->fetchAll();

            $total = count($participations);
            $processed = 0;

            foreach ($participations as $p) {
                // Ar detta riders forsta serie nagonsin?
                $isEntrySeries = $this->isFirstSeriesEver($p['rider_id'], $p['series_id'], $year) ? 1 : 0;

                $stmt = $this->pdo->prepare("
                    INSERT INTO series_participation (
                        rider_id, series_id, season_year, events_attended,
                        first_event_date, last_event_date, total_points,
                        is_entry_series, calculation_version, calculated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON DUPLICATE KEY UPDATE
                        events_attended = VALUES(events_attended),
                        first_event_date = VALUES(first_event_date),
                        last_event_date = VALUES(last_event_date),
                        total_points = VALUES(total_points),
                        is_entry_series = VALUES(is_entry_series),
                        calculation_version = VALUES(calculation_version),
                        calculated_at = CURRENT_TIMESTAMP
                ");

                $stmt->execute([
                    $p['rider_id'],
                    $p['series_id'],
                    $year,
                    $p['events_attended'],
                    $p['first_event_date'],
                    $p['last_event_date'],
                    $p['total_points'],
                    $isEntrySeries,
                    $this->calculationVersion
                ]);

                $count++;
                $processed++;

                // Report progress every 100 items
                if ($progressCallback && ($processed % 100 === 0 || $processed === $total)) {
                    $progressCallback($processed, $total);
                }
            }

            $this->endJob('success', $count);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    // =========================================================================
    // SERIEFLODE (CROSSOVER)
    // =========================================================================

    /**
     * Berakna series crossover for ett ar
     * Hittar riders som deltar i flera serier
     *
     * @param int $year Sasong
     * @return int Antal rader skapade
     */
    public function calculateSeriesCrossover(int $year): int {
        $jobId = $this->startJob('series-crossover', (string)$year, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;

        try {
            // Hitta riders som deltog i minst 2 serier samma ar
            $crossovers = $this->pdo->query("
                SELECT
                    sp1.rider_id,
                    sp1.series_id as from_series_id,
                    sp2.series_id as to_series_id,
                    $year as from_year,
                    $year as to_year,
                    'same_year' as crossover_type
                FROM series_participation sp1
                JOIN series_participation sp2
                    ON sp1.rider_id = sp2.rider_id
                    AND sp1.series_id < sp2.series_id
                    AND sp1.season_year = sp2.season_year
                WHERE sp1.season_year = $year
            ")->fetchAll();

            foreach ($crossovers as $c) {
                $stmt = $this->pdo->prepare("
                    INSERT INTO series_crossover (
                        rider_id, from_series_id, to_series_id,
                        from_year, to_year, crossover_type,
                        calculation_version, calculated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ");

                $stmt->execute([
                    $c['rider_id'],
                    $c['from_series_id'],
                    $c['to_series_id'],
                    $c['from_year'],
                    $c['to_year'],
                    $c['crossover_type'],
                    $this->calculationVersion
                ]);

                $count++;
            }

            // Hitta riders som bytte serie fran forriga aret
            $yearChanges = $this->pdo->query("
                SELECT
                    sp1.rider_id,
                    sp1.series_id as from_series_id,
                    sp2.series_id as to_series_id,
                    " . ($year - 1) . " as from_year,
                    $year as to_year,
                    'next_year' as crossover_type
                FROM series_participation sp1
                JOIN series_participation sp2
                    ON sp1.rider_id = sp2.rider_id
                    AND sp1.series_id != sp2.series_id
                WHERE sp1.season_year = " . ($year - 1) . "
                  AND sp2.season_year = $year
            ")->fetchAll();

            foreach ($yearChanges as $c) {
                $stmt = $this->pdo->prepare("
                    INSERT INTO series_crossover (
                        rider_id, from_series_id, to_series_id,
                        from_year, to_year, crossover_type,
                        calculation_version, calculated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ");

                $stmt->execute([
                    $c['rider_id'],
                    $c['from_series_id'],
                    $c['to_series_id'],
                    $c['from_year'],
                    $c['to_year'],
                    $c['crossover_type'],
                    $this->calculationVersion
                ]);

                $count++;
            }

            $this->endJob('success', $count);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    // =========================================================================
    // KLUBBSTATISTIK
    // =========================================================================

    /**
     * Berakna club yearly stats
     *
     * @param int $year Sasong
     * @param callable|null $progressCallback Callback for progress (int $current, int $total)
     * @return int Antal rader skapade
     */
    public function calculateClubStats(int $year, ?callable $progressCallback = null): int {
        $jobId = $this->startJob('club-stats', (string)$year, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;

        try {
            // Berakna per klubb
            $clubs = $this->pdo->query("
                SELECT DISTINCT r.club_id
                FROM riders r
                JOIN v_canonical_riders v ON r.id = v.original_rider_id
                JOIN results res ON res.cyclist_id = v.original_rider_id
                JOIN events e ON res.event_id = e.id
                WHERE r.club_id IS NOT NULL
                  AND YEAR(e.date) = $year
            ")->fetchAll(PDO::FETCH_COLUMN);

            $total = count($clubs);
            $processed = 0;

            foreach ($clubs as $clubId) {
                $stats = $this->calculateSingleClubYearlyStats($clubId, $year);

                if ($stats) {
                    $this->upsertClubYearlyStats($clubId, $year, $stats);
                    $count++;
                }

                $processed++;

                // Report progress every 10 clubs
                if ($progressCallback && ($processed % 10 === 0 || $processed === $total)) {
                    $progressCallback($processed, $total);
                }
            }

            $this->endJob('success', $count);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    /**
     * Berakna statistik for en enskild klubb ett ar
     */
    private function calculateSingleClubYearlyStats(int $clubId, int $year): ?array {
        // Aktiva riders i klubben detta ar
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(DISTINCT v.canonical_rider_id) as active_riders,
                COUNT(res.id) as total_events_participation,
                SUM(COALESCE(res.points, 0)) as total_points,
                SUM(CASE WHEN res.position <= 10 THEN 1 ELSE 0 END) as top_10_finishes,
                SUM(CASE WHEN res.position <= 3 THEN 1 ELSE 0 END) as podiums,
                SUM(CASE WHEN res.position = 1 THEN 1 ELSE 0 END) as wins
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            JOIN riders r ON v.canonical_rider_id = r.id
            WHERE r.club_id = ?
              AND YEAR(e.date) = ?
        ");
        $stmt->execute([$clubId, $year]);
        $basic = $stmt->fetch();

        if (!$basic || $basic['active_riders'] == 0) {
            return null;
        }

        // Nya riders (forsta aret i klubben)
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rys.rider_id) as new_riders
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE r.club_id = ?
              AND rys.season_year = ?
              AND rys.is_rookie = 1
        ");
        $stmt->execute([$clubId, $year]);
        $newRiders = $stmt->fetchColumn() ?: 0;

        // Retained riders
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rys.rider_id) as retained
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE r.club_id = ?
              AND rys.season_year = ?
              AND rys.is_retained = 1
        ");
        $stmt->execute([$clubId, $year]);
        $retained = $stmt->fetchColumn() ?: 0;

        // Churned (var med forra aret men inte detta)
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT prev.rider_id) as churned
            FROM rider_yearly_stats prev
            JOIN riders r ON prev.rider_id = r.id
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = ?
            WHERE r.club_id = ?
              AND prev.season_year = ?
              AND curr.id IS NULL
        ");
        $stmt->execute([$year, $clubId, $year - 1]);
        $churned = $stmt->fetchColumn() ?: 0;

        // Primary discipline
        $stmt = $this->pdo->prepare("
            SELECT e.discipline, COUNT(*) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            JOIN riders r ON v.canonical_rider_id = r.id
            WHERE r.club_id = ?
              AND YEAR(e.date) = ?
              AND e.discipline IS NOT NULL
            GROUP BY e.discipline
            ORDER BY cnt DESC
            LIMIT 1
        ");
        $stmt->execute([$clubId, $year]);
        $discipline = $stmt->fetch();

        return [
            'active_riders' => (int)$basic['active_riders'],
            'new_riders' => (int)$newRiders,
            'retained_riders' => (int)$retained,
            'churned_riders' => (int)$churned,
            'total_events_participation' => (int)$basic['total_events_participation'],
            'total_points' => (float)$basic['total_points'],
            'top_10_finishes' => (int)$basic['top_10_finishes'],
            'podiums' => (int)$basic['podiums'],
            'wins' => (int)$basic['wins'],
            'primary_discipline' => $discipline ? $discipline['discipline'] : null
        ];
    }

    /**
     * Upsert club yearly stats
     */
    private function upsertClubYearlyStats(int $clubId, int $year, array $stats): void {
        $stmt = $this->pdo->prepare("
            INSERT INTO club_yearly_stats (
                club_id, season_year, active_riders, new_riders, retained_riders,
                churned_riders, total_events_participation, total_points,
                top_10_finishes, podiums, wins, primary_discipline,
                calculation_version, calculated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE
                active_riders = VALUES(active_riders),
                new_riders = VALUES(new_riders),
                retained_riders = VALUES(retained_riders),
                churned_riders = VALUES(churned_riders),
                total_events_participation = VALUES(total_events_participation),
                total_points = VALUES(total_points),
                top_10_finishes = VALUES(top_10_finishes),
                podiums = VALUES(podiums),
                wins = VALUES(wins),
                primary_discipline = VALUES(primary_discipline),
                calculation_version = VALUES(calculation_version),
                calculated_at = CURRENT_TIMESTAMP
        ");

        $stmt->execute([
            $clubId,
            $year,
            $stats['active_riders'],
            $stats['new_riders'],
            $stats['retained_riders'],
            $stats['churned_riders'],
            $stats['total_events_participation'],
            $stats['total_points'],
            $stats['top_10_finishes'],
            $stats['podiums'],
            $stats['wins'],
            $stats['primary_discipline'],
            $this->calculationVersion
        ]);
    }

    // =========================================================================
    // VENUE-STATISTIK
    // =========================================================================

    /**
     * Berakna venue yearly stats
     *
     * @param int $year Sasong
     * @return int Antal rader skapade
     */
    public function calculateVenueStats(int $year): int {
        $jobId = $this->startJob('venue-stats', (string)$year, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;

        try {
            $venues = $this->pdo->query("
                SELECT
                    e.venue_id,
                    COUNT(DISTINCT e.id) as total_events,
                    COUNT(res.id) as total_participants,
                    COUNT(DISTINCT v.canonical_rider_id) as unique_riders
                FROM events e
                LEFT JOIN results res ON e.id = res.event_id
                LEFT JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE YEAR(e.date) = $year
                  AND e.venue_id IS NOT NULL
                GROUP BY e.venue_id
            ")->fetchAll();

            foreach ($venues as $v) {
                if (!$v['venue_id']) continue;

                // Disciplines pa detta venue
                $disciplines = $this->pdo->prepare("
                    SELECT e.discipline, COUNT(*) as cnt
                    FROM events e
                    WHERE e.venue_id = ?
                      AND YEAR(e.date) = ?
                      AND e.discipline IS NOT NULL
                    GROUP BY e.discipline
                ");
                $disciplines->execute([$v['venue_id'], $year]);
                $disciplineData = [];
                while ($d = $disciplines->fetch()) {
                    $disciplineData[$d['discipline']] = (int)$d['cnt'];
                }

                // Serier som haft event har
                $series = $this->pdo->prepare("
                    SELECT DISTINCT e.series_id
                    FROM events e
                    WHERE e.venue_id = ?
                      AND YEAR(e.date) = ?
                      AND e.series_id IS NOT NULL
                ");
                $series->execute([$v['venue_id'], $year]);
                $seriesHosted = $series->fetchAll(PDO::FETCH_COLUMN);

                $stmt = $this->pdo->prepare("
                    INSERT INTO venue_yearly_stats (
                        venue_id, season_year, total_events, total_participants,
                        unique_riders, avg_participants_per_event, disciplines,
                        series_hosted, calculation_version, calculated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON DUPLICATE KEY UPDATE
                        total_events = VALUES(total_events),
                        total_participants = VALUES(total_participants),
                        unique_riders = VALUES(unique_riders),
                        avg_participants_per_event = VALUES(avg_participants_per_event),
                        disciplines = VALUES(disciplines),
                        series_hosted = VALUES(series_hosted),
                        calculation_version = VALUES(calculation_version),
                        calculated_at = CURRENT_TIMESTAMP
                ");

                $avgPart = $v['total_events'] > 0
                    ? round($v['total_participants'] / $v['total_events'], 2)
                    : 0;

                $stmt->execute([
                    $v['venue_id'],
                    $year,
                    $v['total_events'],
                    $v['total_participants'],
                    $v['unique_riders'],
                    $avgPart,
                    json_encode($disciplineData),
                    json_encode($seriesHosted),
                    $this->calculationVersion
                ]);

                $count++;
            }

            $this->endJob('success', $count);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    // =========================================================================
    // HJALPMETODER
    // =========================================================================

    /**
     * Ar detta riders forsta ar?
     */
    private function isRookie(int $riderId, int $year): bool {
        $stmt = $this->pdo->prepare("
            SELECT MIN(YEAR(e.date)) as first_year
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
        ");
        $stmt->execute([$riderId]);
        $firstYear = $stmt->fetchColumn();

        return $firstYear && (int)$firstYear === $year;
    }

    /**
     * Aterkom fran forriga aret?
     */
    private function wasRetained(int $riderId, int $year): bool {
        $stmt = $this->pdo->prepare("
            SELECT 1
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
            LIMIT 1
        ");
        $stmt->execute([$riderId, $year - 1]);
        return (bool)$stmt->fetch();
    }

    /**
     * Ar detta riders forsta serie nagonsin?
     */
    private function isFirstSeriesEver(int $riderId, int $seriesId, int $year): bool {
        $stmt = $this->pdo->prepare("
            SELECT MIN(sp.season_year) as first_year
            FROM series_participation sp
            WHERE sp.rider_id = ?
        ");
        $stmt->execute([$riderId]);
        $firstYear = $stmt->fetchColumn();

        // Om ingen tidigare participation, kolla i results
        if (!$firstYear) {
            $stmt = $this->pdo->prepare("
                SELECT MIN(YEAR(e.date)) as first_year, e.series_id as first_series
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id = ?
                  AND e.series_id IS NOT NULL
                ORDER BY e.date ASC
                LIMIT 1
            ");
            $stmt->execute([$riderId]);
            $first = $stmt->fetch();

            if ($first && $first['first_year']) {
                return (int)$first['first_year'] === $year && (int)$first['first_series'] === $seriesId;
            }
        }

        return false;
    }

    // =========================================================================
    // BULK-METODER (SNABBA)
    // =========================================================================

    /**
     * Berakna yearly stats med EN stor query istallet for per-rider
     * Mycket snabbare for stora datamangder
     *
     * @param int $year Sasong
     * @return int Antal rader
     */
    public function calculateYearlyStatsBulk(int $year): int {
        $jobId = $this->startJob('yearly-stats', (string)$year, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        try {
            // Rensa befintlig data for detta ar (for att undvika dubbletter)
            $this->pdo->prepare("DELETE FROM rider_yearly_stats WHERE season_year = ?")->execute([$year]);

            // En stor INSERT...SELECT som beraknar allt pa en gang
            $sql = "
                INSERT INTO rider_yearly_stats (
                    rider_id, season_year, total_events, total_series, total_points,
                    best_position, avg_position, primary_discipline, primary_series_id,
                    is_rookie, is_retained, calculation_version, calculated_at
                )
                SELECT
                    stats.rider_id,
                    $year as season_year,
                    stats.total_events,
                    stats.total_series,
                    stats.total_points,
                    stats.best_position,
                    stats.avg_position,
                    disc.discipline as primary_discipline,
                    ser.series_id as primary_series_id,
                    CASE WHEN first_year.first_year = $year THEN 1 ELSE 0 END as is_rookie,
                    CASE WHEN prev_year.rider_id IS NOT NULL THEN 1 ELSE 0 END as is_retained,
                    '{$this->calculationVersion}' as calculation_version,
                    NOW() as calculated_at
                FROM (
                    -- Grundstatistik per rider
                    SELECT
                        v.canonical_rider_id as rider_id,
                        COUNT(DISTINCT res.event_id) as total_events,
                        COUNT(DISTINCT e.series_id) as total_series,
                        SUM(COALESCE(res.points, 0)) as total_points,
                        MIN(CASE WHEN res.position > 0 THEN res.position END) as best_position,
                        AVG(CASE WHEN res.position > 0 THEN res.position END) as avg_position
                    FROM results res
                    JOIN events e ON res.event_id = e.id
                    JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                    WHERE YEAR(e.date) = $year
                    GROUP BY v.canonical_rider_id
                ) stats
                -- Primary discipline (mest deltaganden)
                LEFT JOIN (
                    SELECT rider_id, discipline FROM (
                        SELECT
                            v.canonical_rider_id as rider_id,
                            e.discipline,
                            COUNT(*) as cnt,
                            ROW_NUMBER() OVER (PARTITION BY v.canonical_rider_id ORDER BY COUNT(*) DESC) as rn
                        FROM results res
                        JOIN events e ON res.event_id = e.id
                        JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                        WHERE YEAR(e.date) = $year AND e.discipline IS NOT NULL
                        GROUP BY v.canonical_rider_id, e.discipline
                    ) ranked WHERE rn = 1
                ) disc ON stats.rider_id = disc.rider_id
                -- Primary series (mest deltaganden)
                LEFT JOIN (
                    SELECT rider_id, series_id FROM (
                        SELECT
                            v.canonical_rider_id as rider_id,
                            e.series_id,
                            COUNT(*) as cnt,
                            ROW_NUMBER() OVER (PARTITION BY v.canonical_rider_id ORDER BY COUNT(*) DESC) as rn
                        FROM results res
                        JOIN events e ON res.event_id = e.id
                        JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                        WHERE YEAR(e.date) = $year AND e.series_id IS NOT NULL
                        GROUP BY v.canonical_rider_id, e.series_id
                    ) ranked WHERE rn = 1
                ) ser ON stats.rider_id = ser.rider_id
                -- First year (for is_rookie)
                LEFT JOIN (
                    SELECT
                        v.canonical_rider_id as rider_id,
                        MIN(YEAR(e.date)) as first_year
                    FROM results res
                    JOIN events e ON res.event_id = e.id
                    JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                    GROUP BY v.canonical_rider_id
                ) first_year ON stats.rider_id = first_year.rider_id
                -- Previous year participation (for is_retained)
                LEFT JOIN (
                    SELECT DISTINCT v.canonical_rider_id as rider_id
                    FROM results res
                    JOIN events e ON res.event_id = e.id
                    JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                    WHERE YEAR(e.date) = " . ($year - 1) . "
                ) prev_year ON stats.rider_id = prev_year.rider_id
            ";

            $this->pdo->exec($sql);
            $count = $this->pdo->query("SELECT COUNT(*) FROM rider_yearly_stats WHERE season_year = $year")->fetchColumn();

            $this->endJob('success', $count, ['year' => $year]);
            return (int)$count;

        } catch (Exception $e) {
            $this->endJob('failed', 0, ['error' => $e->getMessage()]);
            throw $e;
        }
    }

    /**
     * Snabb version av refreshAllStats som anvander bulk-metoder
     * Rensar forst alla cron-runs for aret sa att allt kors om
     */
    public function refreshAllStatsFast(int $year): array {
        // Rensa ALLA cron-runs for detta ar sa att inget hoppas over
        $this->pdo->prepare("DELETE FROM analytics_cron_runs WHERE run_key = ?")->execute([(string)$year]);

        $results = [];
        $results['yearly_stats'] = $this->calculateYearlyStatsBulk($year);
        $results['series_participation'] = $this->calculateSeriesParticipation($year);
        $results['series_crossover'] = $this->calculateSeriesCrossover($year);
        $results['club_stats'] = $this->calculateClubStats($year);
        $results['venue_stats'] = $this->calculateVenueStats($year);
        return $results;
    }

    // =========================================================================
    // REFRESH-METODER
    // =========================================================================

    /**
     * Kor alla berakningar for ett ar
     *
     * @param int $year Sasong
     * @return array Resultat per berakning
     */
    public function refreshAllStats(int $year): array {
        $results = [];

        $results['yearly_stats'] = $this->calculateYearlyStats($year);
        $results['series_participation'] = $this->calculateSeriesParticipation($year);
        $results['series_crossover'] = $this->calculateSeriesCrossover($year);
        $results['club_stats'] = $this->calculateClubStats($year);
        $results['venue_stats'] = $this->calculateVenueStats($year);

        return $results;
    }

    /**
     * Hamta lista over tillgangliga ar
     */
    public function getAvailableYears(): array {
        return $this->pdo->query("
            SELECT DISTINCT YEAR(date) as year
            FROM events
            WHERE date IS NOT NULL
            ORDER BY year DESC
        ")->fetchAll(PDO::FETCH_COLUMN);
    }

    /**
     * Hamta IdentityResolver
     */
    public function getIdentityResolver(): IdentityResolver {
        return $this->identityResolver;
    }

    // =========================================================================
    // v3.0.1: HEARTBEAT & TIMEOUT HANDLING
    // =========================================================================

    /**
     * Skicka heartbeat for pagaende jobb
     *
     * Anropas regelbundet under langa jobb for att visa att de lever.
     * checkTimeout() kan anvandas for att hitta jobb som slutat skicka heartbeat.
     */
    public function heartbeat(): void {
        if (!$this->currentJobId) return;

        $stmt = $this->pdo->prepare("
            UPDATE analytics_cron_runs
            SET heartbeat_at = NOW()
            WHERE id = ?
        ");
        $stmt->execute([$this->currentJobId]);
    }

    /**
     * Kontrollera om ett jobb har timeout
     *
     * @param string $jobName Jobbnamn
     * @param int $timeoutSeconds Timeout i sekunder (default 1 timme)
     * @return array|null Jobb-info om timeout, annars null
     */
    public function checkTimeout(string $jobName, int $timeoutSeconds = 3600): ?array {
        $stmt = $this->pdo->prepare("
            SELECT id, job_name, run_key, started_at, heartbeat_at
            FROM analytics_cron_runs
            WHERE job_name = ?
              AND status = 'started'
              AND (
                  -- Om vi har heartbeat, kolla mot det
                  (heartbeat_at IS NOT NULL AND heartbeat_at < DATE_SUB(NOW(), INTERVAL ? SECOND))
                  OR
                  -- Om ingen heartbeat, kolla mot started_at
                  (heartbeat_at IS NULL AND started_at < DATE_SUB(NOW(), INTERVAL ? SECOND))
              )
            LIMIT 1
        ");
        $stmt->execute([$jobName, $timeoutSeconds, $timeoutSeconds]);
        $timedOut = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($timedOut) {
            // Markera som timeout
            $this->markJobTimedOut($timedOut['id']);
            return $timedOut;
        }

        return null;
    }

    /**
     * Markera ett jobb som timeout
     *
     * @param int $jobId Job ID
     */
    private function markJobTimedOut(int $jobId): void {
        $stmt = $this->pdo->prepare("
            UPDATE analytics_cron_runs
            SET status = 'failed',
                finished_at = NOW(),
                timeout_detected = 1,
                error_text = 'Job timed out (no heartbeat received)'
            WHERE id = ?
        ");
        $stmt->execute([$jobId]);
    }

    /**
     * Hamta alla timed out jobs for en period
     *
     * @param int $days Antal dagar bakåt
     * @return array Lista med timed out jobs
     */
    public function getTimedOutJobs(int $days = 7): array {
        $stmt = $this->pdo->prepare("
            SELECT *
            FROM analytics_cron_runs
            WHERE timeout_detected = 1
              AND finished_at >= DATE_SUB(NOW(), INTERVAL ? DAY)
            ORDER BY finished_at DESC
        ");
        $stmt->execute([$days]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // v3.0.1: RECALC QUEUE PROCESSING (Merge→Recalc Policy)
    // =========================================================================

    /**
     * Processa recalc-kon
     *
     * Hamtar jobb fran analytics_recalc_queue och kor om berakningar
     * for de paverkade riders och aren.
     *
     * @param int $maxJobs Max antal jobb att processa
     * @return array Resultat per jobb
     */
    public function processRecalcQueue(int $maxJobs = 10): array {
        $results = [];
        $pendingJobs = $this->identityResolver->getPendingRecalcJobs($maxJobs);

        foreach ($pendingJobs as $job) {
            $jobId = (int)$job['id'];
            $startTime = microtime(true);

            // Markera som processing
            if (!$this->identityResolver->markRecalcStarted($jobId)) {
                continue; // Already taken by another process
            }

            try {
                $affectedRiders = json_decode($job['affected_rider_ids'], true) ?? [];
                $affectedYears = json_decode($job['affected_years'], true) ?? [];

                $rowsAffected = 0;

                foreach ($affectedYears as $year) {
                    // Recalculate yearly stats for affected riders
                    foreach ($affectedRiders as $riderId) {
                        $stats = $this->calculateSingleRiderYearlyStats($riderId, $year);
                        if ($stats) {
                            $this->upsertRiderYearlyStats($riderId, $year, $stats);
                            $rowsAffected++;
                        }
                    }
                }

                $executionTimeMs = (int)((microtime(true) - $startTime) * 1000);

                $this->identityResolver->markRecalcCompleted($jobId, $rowsAffected, $executionTimeMs);

                $results[] = [
                    'job_id' => $jobId,
                    'status' => 'completed',
                    'rows_affected' => $rowsAffected,
                    'execution_time_ms' => $executionTimeMs,
                ];

            } catch (Exception $e) {
                $this->identityResolver->markRecalcFailed($jobId, $e->getMessage());

                $results[] = [
                    'job_id' => $jobId,
                    'status' => 'failed',
                    'error' => $e->getMessage(),
                ];
            }
        }

        return $results;
    }

    /**
     * Hamta recalc queue status
     *
     * @return array Queue statistik
     */
    public function getRecalcQueueStatus(): array {
        return $this->identityResolver->getRecalcQueueStats();
    }

    // =========================================================================
    // v3.0.1: SNAPSHOT CREATION
    // =========================================================================

    /**
     * Skapa en snapshot av nuvarande analytics-data
     *
     * @param string $description Beskrivning av snapshot
     * @param string|null $createdBy Anvandare som skapade
     * @return int Snapshot ID
     */
    public function createSnapshot(string $description = '', ?string $createdBy = null): int {
        // Hamta max updated_at fran sources
        $sourceMaxUpdated = $this->pdo->query("
            SELECT MAX(updated_at) FROM (
                SELECT MAX(updated_at) as updated_at FROM rider_yearly_stats
                UNION ALL
                SELECT MAX(updated_at) FROM results
                UNION ALL
                SELECT MAX(updated_at) FROM events
            ) sources
        ")->fetchColumn();

        // Berakna fingerprint
        $fingerprint = hash('sha256', json_encode([
            'rider_yearly_stats' => $this->getTableChecksum('rider_yearly_stats'),
            'series_participation' => $this->getTableChecksum('series_participation'),
            'club_yearly_stats' => $this->getTableChecksum('club_yearly_stats'),
            'timestamp' => $sourceMaxUpdated,
        ]));

        $stmt = $this->pdo->prepare("
            INSERT INTO analytics_snapshots (
                snapshot_type, description, source_max_updated_at,
                fingerprint, created_by
            ) VALUES (
                'full', ?, ?, ?, ?
            )
        ");

        $stmt->execute([
            $description ?: 'Auto-generated snapshot',
            $sourceMaxUpdated,
            $fingerprint,
            $createdBy,
        ]);

        return (int)$this->pdo->lastInsertId();
    }

    /**
     * Hamta checksum for en tabell (for fingerprint)
     *
     * @param string $table Tabellnamn
     * @return string Checksum
     */
    private function getTableChecksum(string $table): string {
        // Sanitize table name
        $table = preg_replace('/[^a-z_]/', '', $table);

        $result = $this->pdo->query("CHECKSUM TABLE $table")->fetch();
        return (string)($result['Checksum'] ?? '0');
    }

    /**
     * Hamta senaste snapshot
     *
     * @return array|null Snapshot data eller null
     */
    public function getLatestSnapshot(): ?array {
        $stmt = $this->pdo->query("
            SELECT * FROM analytics_snapshots
            ORDER BY created_at DESC
            LIMIT 1
        ");
        $snapshot = $stmt->fetch(PDO::FETCH_ASSOC);

        return $snapshot ?: null;
    }

    /**
     * Hamta eller skapa snapshot
     *
     * Returnerar senaste snapshot om den ar tillrackligt ny (inom intervall),
     * annars skapas en ny.
     *
     * @param int $maxAgeMinutes Max alder i minuter
     * @param string|null $createdBy Anvandare
     * @return int Snapshot ID
     */
    public function getOrCreateSnapshot(int $maxAgeMinutes = 60, ?string $createdBy = null): int {
        $latest = $this->getLatestSnapshot();

        if ($latest) {
            $createdAt = strtotime($latest['created_at']);
            $ageMinutes = (time() - $createdAt) / 60;

            if ($ageMinutes <= $maxAgeMinutes) {
                return (int)$latest['id'];
            }
        }

        return $this->createSnapshot('Auto-generated for export', $createdBy);
    }

    // =========================================================================
    // v3.1.1: BRAND RESOLUTION FOR JOURNEY ANALYSIS
    // =========================================================================

    /**
     * Resolve brand ID for a series in a given year
     *
     * Uses brand_series_map with priority:
     * 1. relationship_type = 'owner'
     * 2. Valid date range (valid_from/valid_until)
     * 3. Any mapping if no owner found
     *
     * @param int $seriesId Series ID
     * @param int $year Year for date validation
     * @return int|null Brand ID or null if not found
     */
    private function resolveBrandIdForSeries(int $seriesId, int $year): ?int {
        // First try to find owner relationship with valid dates
        $stmt = $this->pdo->prepare("
            SELECT brand_id
            FROM brand_series_map
            WHERE series_id = ?
              AND (valid_from IS NULL OR valid_from <= ?)
              AND (valid_until IS NULL OR valid_until >= ?)
            ORDER BY
                CASE WHEN relationship_type = 'owner' THEN 0 ELSE 1 END,
                valid_from DESC
            LIMIT 1
        ");
        $stmt->execute([$seriesId, $year, $year]);
        $brandId = $stmt->fetchColumn();

        return $brandId ? (int)$brandId : null;
    }

    /**
     * Resolve brand ID for a rider's first event
     *
     * @param int $riderId Rider ID
     * @param int $cohortYear Cohort year
     * @return array ['brand_id' => int|null, 'series_id' => int|null]
     */
    private function resolveFirstBrandForRider(int $riderId, int $cohortYear): array {
        // Get first event series
        $stmt = $this->pdo->prepare("
            SELECT e.series_id, e.date
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
            ORDER BY e.date ASC
            LIMIT 1
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$row || !$row['series_id']) {
            return ['brand_id' => null, 'series_id' => null];
        }

        $brandId = $this->resolveBrandIdForSeries((int)$row['series_id'], $cohortYear);

        return [
            'brand_id' => $brandId,
            'series_id' => (int)$row['series_id']
        ];
    }

    /**
     * Resolve primary brand for a rider in a specific year
     *
     * Uses the series with most starts in that year
     *
     * @param int $riderId Rider ID
     * @param int $year Calendar year
     * @return array ['brand_id' => int|null, 'series_id' => int|null]
     */
    private function resolvePrimaryBrandForYear(int $riderId, int $year): array {
        // Get series with most starts
        $stmt = $this->pdo->prepare("
            SELECT e.series_id, COUNT(*) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND e.series_id IS NOT NULL
            GROUP BY e.series_id
            ORDER BY cnt DESC
            LIMIT 1
        ");
        $stmt->execute([$riderId, $year]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$row || !$row['series_id']) {
            return ['brand_id' => null, 'series_id' => null];
        }

        $brandId = $this->resolveBrandIdForSeries((int)$row['series_id'], $year);

        return [
            'brand_id' => $brandId,
            'series_id' => (int)$row['series_id']
        ];
    }

    /**
     * Calculate brand journey aggregates for a cohort
     *
     * @param int $cohortYear Cohort year
     * @param int|null $snapshotId Snapshot ID
     * @return int Number of aggregates created
     */
    public function calculateBrandJourneyAggregates(int $cohortYear, ?int $snapshotId = null): int {
        $minSize = 10;
        $count = 0;

        // Get all brands with riders in this cohort
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT first_brand_id
            FROM rider_first_season
            WHERE cohort_year = ?
              AND first_brand_id IS NOT NULL
        ");
        $stmt->execute([$cohortYear]);
        $brandIds = $stmt->fetchAll(PDO::FETCH_COLUMN);

        // Clear existing aggregates for this cohort
        $this->pdo->prepare("
            DELETE FROM brand_journey_aggregates
            WHERE cohort_year = ?
        ")->execute([$cohortYear]);

        foreach ($brandIds as $brandId) {
            // For each year offset 1-4
            for ($offset = 1; $offset <= 4; $offset++) {
                $calendarYear = $cohortYear + $offset - 1;
                if ($calendarYear > (int)date('Y')) continue;

                $stmt = $this->pdo->prepare("
                    SELECT
                        COUNT(*) as total_riders,
                        SUM(rjy.was_active) as active_riders,
                        AVG(CASE WHEN rjy.was_active = 1 THEN rjy.total_starts END) as avg_starts,
                        AVG(CASE WHEN rjy.was_active = 1 THEN rjy.total_events END) as avg_events,
                        AVG(CASE WHEN rjy.was_active = 1 THEN rjy.dnf_rate END) as avg_dnf,
                        AVG(CASE WHEN rjy.was_active = 1 THEN rjy.result_percentile END) as avg_perc,
                        SUM(CASE WHEN rjy.was_active = 1 AND rjy.podium_count > 0 THEN 1 ELSE 0 END) /
                            NULLIF(SUM(rjy.was_active), 0) as pct_podium
                    FROM rider_journey_years rjy
                    JOIN rider_first_season rfs ON rjy.rider_id = rfs.rider_id AND rjy.cohort_year = rfs.cohort_year
                    WHERE rfs.cohort_year = ?
                      AND rfs.first_brand_id = ?
                      AND rjy.year_offset = ?
                ");
                $stmt->execute([$cohortYear, $brandId, $offset]);
                $data = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$data || (int)$data['total_riders'] < $minSize) continue;

                $retention = (int)$data['total_riders'] > 0
                    ? (int)$data['active_riders'] / (int)$data['total_riders']
                    : null;

                // Journey patterns (only for max offset with data)
                $pctContinuous = null;
                $pctOneAndDone = null;
                $pctGapReturner = null;

                if ($offset === 4 || $calendarYear >= (int)date('Y')) {
                    $stmt = $this->pdo->prepare("
                        SELECT
                            SUM(CASE WHEN rjs.journey_pattern = 'continuous_4yr' THEN 1 ELSE 0 END) / COUNT(*) as pct_cont,
                            SUM(CASE WHEN rjs.journey_pattern = 'one_and_done' THEN 1 ELSE 0 END) / COUNT(*) as pct_oad,
                            SUM(CASE WHEN rjs.journey_pattern = 'gap_returner' THEN 1 ELSE 0 END) / COUNT(*) as pct_gap
                        FROM rider_journey_summary rjs
                        JOIN rider_first_season rfs ON rjs.rider_id = rfs.rider_id AND rjs.cohort_year = rfs.cohort_year
                        WHERE rfs.cohort_year = ? AND rfs.first_brand_id = ?
                    ");
                    $stmt->execute([$cohortYear, $brandId]);
                    $patterns = $stmt->fetch(PDO::FETCH_ASSOC);
                    if ($patterns) {
                        $pctContinuous = $patterns['pct_cont'] ? round($patterns['pct_cont'], 4) : null;
                        $pctOneAndDone = $patterns['pct_oad'] ? round($patterns['pct_oad'], 4) : null;
                        $pctGapReturner = $patterns['pct_gap'] ? round($patterns['pct_gap'], 4) : null;
                    }
                }

                $insert = $this->pdo->prepare("
                    INSERT INTO brand_journey_aggregates (
                        brand_id, cohort_year, year_offset,
                        total_riders, active_riders, retention_rate,
                        avg_starts, avg_events, avg_dnf_rate, avg_percentile, pct_with_podium,
                        pct_continuous_4yr, pct_one_and_done, pct_gap_returner,
                        calculated_at, snapshot_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?)
                    ON DUPLICATE KEY UPDATE
                        total_riders = VALUES(total_riders),
                        active_riders = VALUES(active_riders),
                        retention_rate = VALUES(retention_rate),
                        avg_starts = VALUES(avg_starts),
                        avg_events = VALUES(avg_events),
                        avg_dnf_rate = VALUES(avg_dnf_rate),
                        avg_percentile = VALUES(avg_percentile),
                        pct_with_podium = VALUES(pct_with_podium),
                        pct_continuous_4yr = VALUES(pct_continuous_4yr),
                        pct_one_and_done = VALUES(pct_one_and_done),
                        pct_gap_returner = VALUES(pct_gap_returner),
                        calculated_at = NOW(),
                        snapshot_id = VALUES(snapshot_id)
                ");

                $insert->execute([
                    $brandId,
                    $cohortYear,
                    $offset,
                    $data['total_riders'],
                    $data['active_riders'],
                    $retention ? round($retention, 4) : null,
                    $data['avg_starts'] ? round($data['avg_starts'], 2) : null,
                    $data['avg_events'] ? round($data['avg_events'], 2) : null,
                    $data['avg_dnf'] ? round($data['avg_dnf'], 4) : null,
                    $data['avg_perc'] ? round($data['avg_perc'], 2) : null,
                    $data['pct_podium'] ? round($data['pct_podium'], 4) : null,
                    $pctContinuous,
                    $pctOneAndDone,
                    $pctGapReturner,
                    $snapshotId
                ]);

                $count++;
            }
        }

        return $count;
    }

    // =========================================================================
    // v3.1.0: FIRST SEASON JOURNEY ANALYSIS
    // =========================================================================

    /**
     * Berakna First Season Journey for en kohort
     *
     * Analyserar rookies forsta sasong och beraknar metrics som:
     * - Aktivitet (starter, events, finishes)
     * - Resultat (percentil, podier, DNF)
     * - Timing (dagar i sasongen, gap mellan starter)
     * - Social kontext (klubbkamrater)
     * - Outcome (aterkom ar 2-3)
     *
     * GDPR: All data aggregeras - inga individuella prognoser.
     *
     * @param int $cohortYear Kohortar (forsta sasongen)
     * @param int|null $snapshotId Snapshot for reproducerbarhet
     * @param callable|null $progressCallback Progress callback
     * @return int Antal riders processade
     */
    public function calculateFirstSeasonJourney(
        int $cohortYear,
        ?int $snapshotId = null,
        ?callable $progressCallback = null
    ): int {
        $jobId = $this->startJob('first-season-journey', (string)$cohortYear, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;

        try {
            // Hitta alla rookies for detta ar (forsta gang de hade resultat)
            // LEFT JOIN med clubs for att validera att club_id finns (FK constraint)
            $rookies = $this->pdo->prepare("
                SELECT
                    v.canonical_rider_id as rider_id,
                    CASE WHEN c.id IS NOT NULL THEN r.club_id ELSE NULL END as club_id,
                    r.gender,
                    r.birth_year
                FROM v_canonical_riders v
                JOIN riders r ON v.canonical_rider_id = r.id
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE v.canonical_rider_id IN (
                    SELECT v2.canonical_rider_id
                    FROM results res
                    JOIN events e ON res.event_id = e.id
                    JOIN v_canonical_riders v2 ON res.cyclist_id = v2.original_rider_id
                    GROUP BY v2.canonical_rider_id
                    HAVING MIN(YEAR(e.date)) = ?
                )
            ");
            $rookies->execute([$cohortYear]);
            $rookieList = $rookies->fetchAll(PDO::FETCH_ASSOC);

            $total = count($rookieList);
            $processed = 0;

            if ($total === 0) {
                $this->endJob('success', 0, ['cohort_year' => $cohortYear, 'rookies_found' => 0]);
                return 0;
            }

            // === BATCH PRE-COMPUTE ALL DATA ===
            $riderIds = array_column($rookieList, 'rider_id');
            $placeholders = implode(',', array_fill(0, count($riderIds), '?'));

            // 1. Batch: Activity in year+1 and year+2 (retention)
            $activityMap = [];
            $activityStmt = $this->pdo->prepare("
                SELECT
                    v.canonical_rider_id as rider_id,
                    GROUP_CONCAT(DISTINCT YEAR(e.date)) as active_years
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id IN ($placeholders)
                  AND YEAR(e.date) IN (?, ?)
                GROUP BY v.canonical_rider_id
            ");
            $activityStmt->execute(array_merge($riderIds, [$cohortYear + 1, $cohortYear + 2]));
            while ($row = $activityStmt->fetch(PDO::FETCH_ASSOC)) {
                $years = explode(',', $row['active_years']);
                $activityMap[$row['rider_id']] = [
                    'year2' => in_array((string)($cohortYear + 1), $years),
                    'year3' => in_array((string)($cohortYear + 2), $years)
                ];
            }

            // 2. Batch: First brand/series for each rider
            $brandMap = [];
            $brandStmt = $this->pdo->prepare("
                SELECT
                    v.canonical_rider_id as rider_id,
                    (
                        SELECT s.brand_id
                        FROM results r2
                        JOIN events e2 ON r2.event_id = e2.id
                        JOIN series_events se2 ON se2.event_id = e2.id
                        JOIN series s ON s.id = se2.series_id
                        JOIN v_canonical_riders v2 ON r2.cyclist_id = v2.original_rider_id
                        WHERE v2.canonical_rider_id = v.canonical_rider_id
                          AND YEAR(e2.date) = ?
                        ORDER BY e2.date ASC
                        LIMIT 1
                    ) as first_brand_id,
                    (
                        SELECT se3.series_id
                        FROM results r3
                        JOIN events e3 ON r3.event_id = e3.id
                        JOIN series_events se3 ON se3.event_id = e3.id
                        JOIN v_canonical_riders v3 ON r3.cyclist_id = v3.original_rider_id
                        WHERE v3.canonical_rider_id = v.canonical_rider_id
                          AND YEAR(e3.date) = ?
                        ORDER BY e3.date ASC
                        LIMIT 1
                    ) as first_series_id
                FROM v_canonical_riders v
                WHERE v.canonical_rider_id IN ($placeholders)
                GROUP BY v.canonical_rider_id
            ");
            $brandStmt->execute(array_merge([$cohortYear, $cohortYear], $riderIds));
            while ($row = $brandStmt->fetch(PDO::FETCH_ASSOC)) {
                $brandMap[$row['rider_id']] = [
                    'brand_id' => $row['first_brand_id'] ? (int)$row['first_brand_id'] : null,
                    'series_id' => $row['first_series_id'] ? (int)$row['first_series_id'] : null
                ];
            }

            // 3. Batch: Career seasons and last active year
            $careerMap = [];
            $careerStmt = $this->pdo->prepare("
                SELECT
                    v.canonical_rider_id as rider_id,
                    COUNT(DISTINCT YEAR(e.date)) as total_seasons,
                    MAX(YEAR(e.date)) as last_active_year
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id IN ($placeholders)
                GROUP BY v.canonical_rider_id
            ");
            $careerStmt->execute($riderIds);
            while ($row = $careerStmt->fetch(PDO::FETCH_ASSOC)) {
                $careerMap[$row['rider_id']] = [
                    'total_seasons' => (int)$row['total_seasons'],
                    'last_active_year' => $row['last_active_year'] ? (int)$row['last_active_year'] : null
                ];
            }

            // 4. Batch: First season metrics for ALL rookies at once
            $metricsMap = [];
            $metricsStmt = $this->pdo->prepare("
                SELECT
                    v.canonical_rider_id as rider_id,
                    COUNT(*) as total_starts,
                    COUNT(DISTINCT res.event_id) as total_events,
                    SUM(CASE WHEN res.status = 'finished' OR res.position IS NOT NULL THEN 1 ELSE 0 END) as total_finishes,
                    SUM(CASE WHEN res.status = 'DNF' THEN 1 ELSE 0 END) as total_dnf,
                    MIN(CASE WHEN res.position > 0 THEN res.position END) as best_position,
                    AVG(CASE WHEN res.position > 0 THEN res.position END) as avg_position,
                    SUM(CASE WHEN res.position <= 3 THEN 1 ELSE 0 END) as podium_count,
                    SUM(CASE WHEN res.position <= 10 THEN 1 ELSE 0 END) as top10_count,
                    MIN(e.date) as first_event_date,
                    MAX(e.date) as last_event_date
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id IN ($placeholders)
                  AND YEAR(e.date) = ?
                GROUP BY v.canonical_rider_id
            ");
            $metricsStmt->execute(array_merge($riderIds, [$cohortYear]));
            while ($row = $metricsStmt->fetch(PDO::FETCH_ASSOC)) {
                $metricsMap[$row['rider_id']] = $row;
            }

            // === NOW LOOP WITH LOOKUPS ONLY (no queries!) ===
            foreach ($rookieList as $rookie) {
                $riderId = (int)$rookie['rider_id'];

                // Lookup pre-computed metrics
                $rawMetrics = $metricsMap[$riderId] ?? null;
                if (!$rawMetrics || $rawMetrics['total_starts'] == 0) {
                    $processed++;
                    continue;
                }

                // Build metrics from pre-computed data
                $metrics = [
                    'total_starts' => (int)$rawMetrics['total_starts'],
                    'total_events' => (int)$rawMetrics['total_events'],
                    'total_finishes' => (int)$rawMetrics['total_finishes'],
                    'total_dnf' => (int)$rawMetrics['total_dnf'],
                    'best_position' => $rawMetrics['best_position'] ? (int)$rawMetrics['best_position'] : null,
                    'avg_position' => $rawMetrics['avg_position'] ? round((float)$rawMetrics['avg_position'], 2) : null,
                    'podium_count' => (int)$rawMetrics['podium_count'],
                    'top10_count' => (int)$rawMetrics['top10_count'],
                    'first_event_date' => $rawMetrics['first_event_date'],
                    'last_event_date' => $rawMetrics['last_event_date'],
                ];

                // Calculate derived metrics
                $metrics['dnf_rate'] = $metrics['total_starts'] > 0
                    ? round($metrics['total_dnf'] / $metrics['total_starts'], 4)
                    : 0;

                if ($metrics['first_event_date'] && $metrics['last_event_date']) {
                    $first = new DateTime($metrics['first_event_date']);
                    $last = new DateTime($metrics['last_event_date']);
                    $metrics['season_span_days'] = $first->diff($last)->days;
                } else {
                    $metrics['season_span_days'] = 0;
                }

                // Add rider-specific data
                $metrics['club_id'] = $rookie['club_id'];
                $metrics['gender'] = $rookie['gender'] ?? 'U';
                $metrics['age_at_first_start'] = $rookie['birth_year']
                    ? $cohortYear - (int)$rookie['birth_year']
                    : null;

                // Lookup pre-computed activity (no query!)
                $activity = $activityMap[$riderId] ?? ['year2' => false, 'year3' => false];
                $metrics['returned_year2'] = $activity['year2'] ? 1 : 0;
                $metrics['returned_year3'] = $activity['year3'] ? 1 : 0;

                // Lookup pre-computed brand (no query!)
                $brand = $brandMap[$riderId] ?? ['brand_id' => null, 'series_id' => null];
                $metrics['first_brand_id'] = $brand['brand_id'];
                $metrics['first_series_id'] = $brand['series_id'];

                // Lookup pre-computed career stats (no query!)
                $career = $careerMap[$riderId] ?? ['total_seasons' => 1, 'last_active_year' => $cohortYear];
                $metrics['total_career_seasons'] = $career['total_seasons'];
                $metrics['last_active_year'] = $career['last_active_year'];

                // Calculate engagement score and pattern
                $metrics['engagement_score'] = $this->calculateEngagementScore($metrics);
                $metrics['activity_pattern'] = $this->classifyActivityPattern($metrics['engagement_score']);

                // Spara till databas
                $this->upsertRiderFirstSeason($riderId, $cohortYear, $metrics, $snapshotId);
                $count++;

                $processed++;
                if ($progressCallback && ($processed % 50 === 0 || $processed === $total)) {
                    $progressCallback($processed, $total);
                }

                // Heartbeat var 100:e rider
                if ($processed % 100 === 0) {
                    $this->heartbeat();
                }
            }

            // Berakna klubb-kontext (hur manga andra rookies i samma klubb)
            $this->updateClubRookieContext($cohortYear);

            $this->endJob('success', $count, [
                'cohort_year' => $cohortYear,
                'rookies_found' => $total,
                'processed' => $count
            ]);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    /**
     * Berakna first season metrics for en enskild rider
     */
    private function calculateSingleRiderFirstSeason(int $riderId, int $cohortYear): ?array {
        // Grundlaggande aktivitetsdata
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(*) as total_starts,
                COUNT(DISTINCT res.event_id) as total_events,
                SUM(CASE WHEN res.status = 'finished' OR res.position IS NOT NULL THEN 1 ELSE 0 END) as total_finishes,
                SUM(CASE WHEN res.status = 'DNF' THEN 1 ELSE 0 END) as total_dnf,
                MIN(CASE WHEN res.position > 0 THEN res.position END) as best_position,
                AVG(CASE WHEN res.position > 0 THEN res.position END) as avg_position,
                SUM(CASE WHEN res.position <= 3 THEN 1 ELSE 0 END) as podium_count,
                SUM(CASE WHEN res.position <= 10 THEN 1 ELSE 0 END) as top10_count,
                MIN(e.date) as first_event_date,
                MAX(e.date) as last_event_date
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $basic = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$basic || $basic['total_starts'] == 0) {
            return null;
        }

        // Berakna percentil inom klass (genomsnitt)
        $stmt = $this->pdo->prepare("
            SELECT AVG(
                (class_count - position + 1) / class_count * 100
            ) as avg_percentile
            FROM (
                SELECT
                    res.position,
                    (SELECT COUNT(*) FROM results r2 WHERE r2.event_id = res.event_id AND r2.class_id = res.class_id) as class_count
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id = ?
                  AND YEAR(e.date) = ?
                  AND res.position IS NOT NULL
                  AND res.position > 0
            ) percentiles
            WHERE class_count > 1
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $percentile = $stmt->fetchColumn();

        // Berakna timing-metrics
        $stmt = $this->pdo->prepare("
            SELECT e.date
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
            ORDER BY e.date
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $dates = $stmt->fetchAll(PDO::FETCH_COLUMN);

        $avgGap = null;
        $maxGap = 0;
        if (count($dates) > 1) {
            $gaps = [];
            for ($i = 1; $i < count($dates); $i++) {
                $gap = (strtotime($dates[$i]) - strtotime($dates[$i-1])) / 86400;
                $gaps[] = $gap;
                if ($gap > $maxGap) $maxGap = (int)$gap;
            }
            $avgGap = count($gaps) > 0 ? array_sum($gaps) / count($gaps) : null;
        }

        // Berakna sasongsspridning (early/mid/late)
        $spreadData = $this->calculateSeasonSpread($dates, $cohortYear);

        // Hamta primar klass och disciplin
        $stmt = $this->pdo->prepare("
            SELECT res.class_id, COUNT(*) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND res.class_id IS NOT NULL
            GROUP BY res.class_id
            ORDER BY cnt DESC
            LIMIT 1
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $classRow = $stmt->fetch();

        $stmt = $this->pdo->prepare("
            SELECT e.discipline, COUNT(*) as cnt
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND e.discipline IS NOT NULL
            GROUP BY e.discipline
            ORDER BY cnt DESC
            LIMIT 1
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $discRow = $stmt->fetch();

        // Antal olika discipliner
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT e.discipline) as disc_count
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
              AND e.discipline IS NOT NULL
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $discCount = $stmt->fetchColumn() ?: 1;

        return [
            'total_starts' => (int)$basic['total_starts'],
            'total_events' => (int)$basic['total_events'],
            'total_finishes' => (int)$basic['total_finishes'],
            'total_dnf' => (int)$basic['total_dnf'],
            'dnf_rate' => $basic['total_starts'] > 0
                ? round($basic['total_dnf'] / $basic['total_starts'], 4)
                : null,
            'best_position' => $basic['best_position'] ? (int)$basic['best_position'] : null,
            'avg_position' => $basic['avg_position'] ? round($basic['avg_position'], 2) : null,
            'result_percentile' => $percentile ? round($percentile, 2) : null,
            'podium_count' => (int)$basic['podium_count'],
            'top10_count' => (int)$basic['top10_count'],
            'first_event_date' => $basic['first_event_date'],
            'last_event_date' => $basic['last_event_date'],
            'days_in_season' => $basic['first_event_date'] && $basic['last_event_date']
                ? (strtotime($basic['last_event_date']) - strtotime($basic['first_event_date'])) / 86400
                : 0,
            'avg_days_between_starts' => $avgGap ? round($avgGap, 2) : null,
            'max_gap_days' => $maxGap ?: null,
            'early_season_starts' => $spreadData['early'],
            'mid_season_starts' => $spreadData['mid'],
            'late_season_starts' => $spreadData['late'],
            'season_spread_score' => $spreadData['spread_score'],
            'class_id' => $classRow ? (int)$classRow['class_id'] : null,
            'primary_discipline' => $discRow ? $discRow['discipline'] : null,
            'discipline_count' => (int)$discCount,
        ];
    }

    /**
     * Berakna sasongsspridning (hur jamt fordelat over sasongen)
     */
    private function calculateSeasonSpread(array $dates, int $year): array {
        $early = 0;  // Apr-May
        $mid = 0;    // Jun-Jul
        $late = 0;   // Aug-Oct

        foreach ($dates as $date) {
            $month = (int)date('n', strtotime($date));
            if ($month <= 5) {
                $early++;
            } elseif ($month <= 7) {
                $mid++;
            } else {
                $late++;
            }
        }

        $total = count($dates);
        if ($total === 0) {
            return ['early' => 0, 'mid' => 0, 'late' => 0, 'spread_score' => 0];
        }

        // Berakna entropy-baserad spread score (0-1, hoger = mer jamt)
        $proportions = [$early/$total, $mid/$total, $late/$total];
        $entropy = 0;
        foreach ($proportions as $p) {
            if ($p > 0) {
                $entropy -= $p * log($p);
            }
        }
        // Normalisera till 0-1 (max entropy for 3 kategorier = ln(3))
        $maxEntropy = log(3);
        $spreadScore = $maxEntropy > 0 ? $entropy / $maxEntropy : 0;

        return [
            'early' => $early,
            'mid' => $mid,
            'late' => $late,
            'spread_score' => round($spreadScore, 4)
        ];
    }

    /**
     * Kontrollera om rider hade aktivitet ett visst ar
     */
    private function hadActivityInYear(int $riderId, int $year): bool {
        $stmt = $this->pdo->prepare("
            SELECT 1
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
            LIMIT 1
        ");
        $stmt->execute([$riderId, $year]);
        return (bool)$stmt->fetch();
    }

    /**
     * Hamta totalt antal sasonger for en rider
     */
    private function getTotalCareerSeasons(int $riderId): int {
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT YEAR(e.date)) as seasons
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
        ");
        $stmt->execute([$riderId]);
        return (int)$stmt->fetchColumn();
    }

    /**
     * Hamta senaste aktiva ar for en rider
     */
    private function getLastActiveYear(int $riderId): ?int {
        $stmt = $this->pdo->prepare("
            SELECT MAX(YEAR(e.date)) as last_year
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
        ");
        $stmt->execute([$riderId]);
        $year = $stmt->fetchColumn();
        return $year ? (int)$year : null;
    }

    /**
     * Berakna engagement score (sammansatt metric)
     *
     * Kombinerar flera faktorer till ett 0-100 score:
     * - Antal starter (30%)
     * - Antal events (20%)
     * - Sasongsspridning (20%)
     * - Resultatpercentil (30%)
     */
    private function calculateEngagementScore(array $metrics): float {
        $score = 0;

        // Starter: 1 start = 10, 5+ = 30
        $startsScore = min(30, ($metrics['total_starts'] ?? 0) * 6);
        $score += $startsScore;

        // Events: 1 event = 5, 5+ = 20
        $eventsScore = min(20, ($metrics['total_events'] ?? 0) * 4);
        $score += $eventsScore;

        // Spread: 0-1 * 20
        $spreadScore = ($metrics['season_spread_score'] ?? 0) * 20;
        $score += $spreadScore;

        // Percentil: 0-100 * 0.3
        $percentileScore = ($metrics['result_percentile'] ?? 50) * 0.3;
        $score += $percentileScore;

        return round($score, 2);
    }

    /**
     * Klassificera activity pattern baserat pa engagement score
     */
    private function classifyActivityPattern(float $engagementScore): string {
        if ($engagementScore >= 70) {
            return 'high_engagement';
        } elseif ($engagementScore >= 40) {
            return 'moderate';
        } else {
            return 'low_engagement';
        }
    }

    /**
     * Uppdatera klubb-kontext (antal rookies i samma klubb)
     */
    private function updateClubRookieContext(int $cohortYear): void {
        // Berakna antal rookies per klubb
        $this->pdo->prepare("
            UPDATE rider_first_season rfs
            JOIN (
                SELECT club_id, COUNT(*) as rookie_count
                FROM rider_first_season
                WHERE cohort_year = ?
                  AND club_id IS NOT NULL
                GROUP BY club_id
            ) counts ON rfs.club_id = counts.club_id
            SET
                rfs.club_rookie_count = counts.rookie_count,
                rfs.club_had_other_rookies = CASE WHEN counts.rookie_count > 1 THEN 1 ELSE 0 END
            WHERE rfs.cohort_year = ?
        ")->execute([$cohortYear, $cohortYear]);
    }

    /**
     * Spara rider first season data
     */
    private function upsertRiderFirstSeason(int $riderId, int $cohortYear, array $metrics, ?int $snapshotId): void {
        $stmt = $this->pdo->prepare("
            INSERT INTO rider_first_season (
                rider_id, cohort_year,
                total_starts, total_events, total_finishes, total_dnf, dnf_rate,
                best_position, avg_position, result_percentile, podium_count, top10_count,
                first_event_date, last_event_date, days_in_season,
                avg_days_between_starts, max_gap_days,
                early_season_starts, mid_season_starts, late_season_starts, season_spread_score,
                club_id, first_brand_id, first_series_id,
                gender, age_at_first_start, class_id, primary_discipline, discipline_count,
                returned_year2, returned_year3, total_career_seasons, last_active_year,
                engagement_score, activity_pattern,
                calculated_at, snapshot_id
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?
            )
            ON DUPLICATE KEY UPDATE
                total_starts = VALUES(total_starts),
                total_events = VALUES(total_events),
                total_finishes = VALUES(total_finishes),
                total_dnf = VALUES(total_dnf),
                dnf_rate = VALUES(dnf_rate),
                best_position = VALUES(best_position),
                avg_position = VALUES(avg_position),
                result_percentile = VALUES(result_percentile),
                podium_count = VALUES(podium_count),
                top10_count = VALUES(top10_count),
                first_event_date = VALUES(first_event_date),
                last_event_date = VALUES(last_event_date),
                days_in_season = VALUES(days_in_season),
                avg_days_between_starts = VALUES(avg_days_between_starts),
                max_gap_days = VALUES(max_gap_days),
                early_season_starts = VALUES(early_season_starts),
                mid_season_starts = VALUES(mid_season_starts),
                late_season_starts = VALUES(late_season_starts),
                season_spread_score = VALUES(season_spread_score),
                club_id = VALUES(club_id),
                first_brand_id = VALUES(first_brand_id),
                first_series_id = VALUES(first_series_id),
                gender = VALUES(gender),
                age_at_first_start = VALUES(age_at_first_start),
                class_id = VALUES(class_id),
                primary_discipline = VALUES(primary_discipline),
                discipline_count = VALUES(discipline_count),
                returned_year2 = VALUES(returned_year2),
                returned_year3 = VALUES(returned_year3),
                total_career_seasons = VALUES(total_career_seasons),
                last_active_year = VALUES(last_active_year),
                engagement_score = VALUES(engagement_score),
                activity_pattern = VALUES(activity_pattern),
                calculated_at = NOW(),
                snapshot_id = VALUES(snapshot_id)
        ");

        $stmt->execute([
            $riderId,
            $cohortYear,
            $metrics['total_starts'],
            $metrics['total_events'],
            $metrics['total_finishes'],
            $metrics['total_dnf'],
            $metrics['dnf_rate'],
            $metrics['best_position'],
            $metrics['avg_position'],
            $metrics['result_percentile'],
            $metrics['podium_count'],
            $metrics['top10_count'],
            $metrics['first_event_date'],
            $metrics['last_event_date'],
            $metrics['days_in_season'],
            $metrics['avg_days_between_starts'],
            $metrics['max_gap_days'],
            $metrics['early_season_starts'],
            $metrics['mid_season_starts'],
            $metrics['late_season_starts'],
            $metrics['season_spread_score'],
            $metrics['club_id'],
            $metrics['first_brand_id'] ?? null,
            $metrics['first_series_id'] ?? null,
            $metrics['gender'],
            $metrics['age_at_first_start'],
            $metrics['class_id'],
            $metrics['primary_discipline'],
            $metrics['discipline_count'],
            $metrics['returned_year2'],
            $metrics['returned_year3'],
            $metrics['total_career_seasons'],
            $metrics['last_active_year'],
            $metrics['engagement_score'],
            $metrics['activity_pattern'],
            $snapshotId,
        ]);
    }

    /**
     * Berakna First Season Aggregates for en kohort
     *
     * Aggregerar data fran rider_first_season till first_season_aggregates.
     * Endast segment med >= 10 riders inkluderas (GDPR).
     *
     * @param int $cohortYear Kohortar
     * @param int|null $snapshotId Snapshot ID
     * @return int Antal aggregat skapade
     */
    public function calculateFirstSeasonAggregates(int $cohortYear, ?int $snapshotId = null): int {
        $jobId = $this->startJob('first-season-aggregates', (string)$cohortYear, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;
        $minSegmentSize = 10; // GDPR minimum

        try {
            // Rensa gamla aggregat for denna kohort
            $this->pdo->prepare("
                DELETE FROM first_season_aggregates
                WHERE cohort_year = ? AND (snapshot_id = ? OR snapshot_id IS NULL)
            ")->execute([$cohortYear, $snapshotId]);

            // Overall aggregates
            $count += $this->insertFirstSeasonAggregate($cohortYear, 'overall', null, $snapshotId, $minSegmentSize);

            // Gender aggregates
            foreach (['M', 'F'] as $gender) {
                $count += $this->insertFirstSeasonAggregate($cohortYear, 'gender', $gender, $snapshotId, $minSegmentSize);
            }

            // Engagement level aggregates
            foreach (['high_engagement', 'moderate', 'low_engagement'] as $pattern) {
                $count += $this->insertFirstSeasonAggregate($cohortYear, 'engagement_level', $pattern, $snapshotId, $minSegmentSize);
            }

            // Discipline aggregates
            $disciplines = $this->pdo->prepare("
                SELECT DISTINCT primary_discipline
                FROM rider_first_season
                WHERE cohort_year = ? AND primary_discipline IS NOT NULL
            ");
            $disciplines->execute([$cohortYear]);
            foreach ($disciplines->fetchAll(PDO::FETCH_COLUMN) as $disc) {
                $count += $this->insertFirstSeasonAggregate($cohortYear, 'discipline', $disc, $snapshotId, $minSegmentSize);
            }

            $this->endJob('success', $count, [
                'cohort_year' => $cohortYear,
                'aggregates_created' => $count
            ]);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    /**
     * Skapa ett aggregat for ett segment
     */
    private function insertFirstSeasonAggregate(
        int $cohortYear,
        string $segmentType,
        ?string $segmentValue,
        ?int $snapshotId,
        int $minSize
    ): int {
        // Bygg WHERE-klausul
        $where = "cohort_year = ?";
        $params = [$cohortYear];

        if ($segmentType === 'gender' && $segmentValue) {
            $where .= " AND gender = ?";
            $params[] = $segmentValue;
        } elseif ($segmentType === 'engagement_level' && $segmentValue) {
            $where .= " AND activity_pattern = ?";
            $params[] = $segmentValue;
        } elseif ($segmentType === 'discipline' && $segmentValue) {
            $where .= " AND primary_discipline = ?";
            $params[] = $segmentValue;
        }

        // Hamta aggregat
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(*) as total_riders,
                AVG(total_starts) as avg_total_starts,
                AVG(total_events) as avg_total_events,
                AVG(dnf_rate) as avg_dnf_rate,
                AVG(result_percentile) as avg_result_percentile,
                SUM(CASE WHEN podium_count > 0 THEN 1 ELSE 0 END) / COUNT(*) as pct_with_podium,
                SUM(CASE WHEN top10_count > 0 THEN 1 ELSE 0 END) / COUNT(*) as pct_with_top10,
                AVG(days_in_season) as avg_days_in_season,
                AVG(season_spread_score) as avg_season_spread,
                AVG(returned_year2) as pct_returned_year2,
                AVG(returned_year3) as pct_returned_year3,
                AVG(total_career_seasons) as avg_career_seasons
            FROM rider_first_season
            WHERE $where
        ");
        $stmt->execute($params);
        $agg = $stmt->fetch(PDO::FETCH_ASSOC);

        // Skip if below minimum size
        if (!$agg || (int)$agg['total_riders'] < $minSize) {
            return 0;
        }

        // Berakna startfordelning
        $stmt = $this->pdo->prepare("
            SELECT
                SUM(CASE WHEN total_starts = 1 THEN 1 ELSE 0 END) as s1,
                SUM(CASE WHEN total_starts BETWEEN 2 AND 3 THEN 1 ELSE 0 END) as s2_3,
                SUM(CASE WHEN total_starts BETWEEN 4 AND 5 THEN 1 ELSE 0 END) as s4_5,
                SUM(CASE WHEN total_starts >= 6 THEN 1 ELSE 0 END) as s6plus
            FROM rider_first_season
            WHERE $where
        ");
        $stmt->execute($params);
        $dist = $stmt->fetch(PDO::FETCH_ASSOC);

        $startsDistribution = json_encode([
            '1' => (int)$dist['s1'],
            '2-3' => (int)$dist['s2_3'],
            '4-5' => (int)$dist['s4_5'],
            '6+' => (int)$dist['s6plus']
        ]);

        // Insert aggregat
        $stmt = $this->pdo->prepare("
            INSERT INTO first_season_aggregates (
                cohort_year, segment_type, segment_value, total_riders,
                avg_total_starts, avg_total_events, avg_dnf_rate,
                avg_result_percentile, pct_with_podium, pct_with_top10,
                avg_days_in_season, avg_season_spread,
                pct_returned_year2, pct_returned_year3, avg_career_seasons,
                starts_distribution, calculated_at, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?)
            ON DUPLICATE KEY UPDATE
                total_riders = VALUES(total_riders),
                avg_total_starts = VALUES(avg_total_starts),
                avg_total_events = VALUES(avg_total_events),
                avg_dnf_rate = VALUES(avg_dnf_rate),
                avg_result_percentile = VALUES(avg_result_percentile),
                pct_with_podium = VALUES(pct_with_podium),
                pct_with_top10 = VALUES(pct_with_top10),
                avg_days_in_season = VALUES(avg_days_in_season),
                avg_season_spread = VALUES(avg_season_spread),
                pct_returned_year2 = VALUES(pct_returned_year2),
                pct_returned_year3 = VALUES(pct_returned_year3),
                avg_career_seasons = VALUES(avg_career_seasons),
                starts_distribution = VALUES(starts_distribution),
                calculated_at = NOW(),
                snapshot_id = VALUES(snapshot_id)
        ");

        $stmt->execute([
            $cohortYear,
            $segmentType,
            $segmentValue,
            $agg['total_riders'],
            round($agg['avg_total_starts'], 2),
            round($agg['avg_total_events'], 2),
            $agg['avg_dnf_rate'] ? round($agg['avg_dnf_rate'], 4) : null,
            $agg['avg_result_percentile'] ? round($agg['avg_result_percentile'], 2) : null,
            $agg['pct_with_podium'] ? round($agg['pct_with_podium'], 4) : null,
            $agg['pct_with_top10'] ? round($agg['pct_with_top10'], 4) : null,
            $agg['avg_days_in_season'] ? round($agg['avg_days_in_season'], 2) : null,
            $agg['avg_season_spread'] ? round($agg['avg_season_spread'], 4) : null,
            $agg['pct_returned_year2'] ? round($agg['pct_returned_year2'], 4) : null,
            $agg['pct_returned_year3'] ? round($agg['pct_returned_year3'], 4) : null,
            $agg['avg_career_seasons'] ? round($agg['avg_career_seasons'], 2) : null,
            $startsDistribution,
            $snapshotId
        ]);

        return 1;
    }

    // =========================================================================
    // v3.1.0: LONGITUDINAL JOURNEY ANALYSIS (Years 2-4)
    // =========================================================================

    /**
     * Berakna Longitudinal Journey for en kohort
     *
     * Foljer rookies genom ar 2-4 och beraknar:
     * - Aktivitet per ar
     * - Progression/regression
     * - Retention/churn
     * - Journey patterns
     *
     * @param int $cohortYear Kohortar (forsta sasongen)
     * @param int|null $snapshotId Snapshot
     * @param callable|null $progressCallback Progress
     * @return int Antal records
     */
    public function calculateLongitudinalJourney(
        int $cohortYear,
        ?int $snapshotId = null,
        ?callable $progressCallback = null
    ): int {
        $jobId = $this->startJob('longitudinal-journey', (string)$cohortYear, $this->forceRerun);
        if ($jobId === false) {
            return 0;
        }

        $count = 0;

        try {
            // Hamta alla riders fran kohorten
            $stmt = $this->pdo->prepare("
                SELECT rider_id, cohort_year
                FROM rider_first_season
                WHERE cohort_year = ?
            ");
            $stmt->execute([$cohortYear]);
            $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

            $total = count($riders);
            $processed = 0;
            $currentYear = (int)date('Y');

            foreach ($riders as $rider) {
                $riderId = (int)$rider['rider_id'];

                // Berakna metrics for ar 1-4
                for ($yearOffset = 1; $yearOffset <= 4; $yearOffset++) {
                    $calendarYear = $cohortYear + $yearOffset - 1;

                    // Hoppa over framtida ar
                    if ($calendarYear > $currentYear) {
                        continue;
                    }

                    $yearMetrics = $this->calculateRiderYearMetrics($riderId, $calendarYear);
                    $this->upsertRiderJourneyYear($riderId, $cohortYear, $yearOffset, $calendarYear, $yearMetrics, $snapshotId);
                    $count++;
                }

                // Berakna journey summary
                $this->updateRiderJourneySummary($riderId, $cohortYear, $snapshotId);

                $processed++;
                if ($progressCallback && ($processed % 50 === 0 || $processed === $total)) {
                    $progressCallback($processed, $total);
                }

                if ($processed % 100 === 0) {
                    $this->heartbeat();
                }
            }

            // Berakna longitudinal aggregates
            $this->calculateCohortLongitudinalAggregates($cohortYear, $snapshotId);

            $this->endJob('success', $count, [
                'cohort_year' => $cohortYear,
                'riders' => $total,
                'year_records' => $count
            ]);

        } catch (Exception $e) {
            $this->endJob('failed', $count, ['error' => $e->getMessage()]);
            throw $e;
        }

        return $count;
    }

    /**
     * Berakna ar-metrics for en rider
     */
    private function calculateRiderYearMetrics(int $riderId, int $year): array {
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(*) as total_starts,
                COUNT(DISTINCT res.event_id) as total_events,
                SUM(CASE WHEN res.status = 'finished' OR res.position IS NOT NULL THEN 1 ELSE 0 END) as total_finishes,
                SUM(CASE WHEN res.status = 'DNF' THEN 1 ELSE 0 END) as total_dnf,
                MIN(CASE WHEN res.position > 0 THEN res.position END) as best_position,
                AVG(CASE WHEN res.position > 0 THEN res.position END) as avg_position,
                SUM(CASE WHEN res.position <= 3 THEN 1 ELSE 0 END) as podium_count,
                SUM(CASE WHEN res.position <= 10 THEN 1 ELSE 0 END) as top10_count,
                SUM(COALESCE(res.points, 0)) as total_points,
                MIN(e.date) as first_event_date,
                MAX(e.date) as last_event_date
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
            WHERE v.canonical_rider_id = ?
              AND YEAR(e.date) = ?
        ");
        $stmt->execute([$riderId, $year]);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        $wasActive = $data && (int)$data['total_starts'] > 0;

        // Berakna percentil
        $percentile = null;
        if ($wasActive) {
            $stmt = $this->pdo->prepare("
                SELECT AVG(
                    (class_count - position + 1) / class_count * 100
                ) as avg_percentile
                FROM (
                    SELECT
                        res.position,
                        (SELECT COUNT(*) FROM results r2 WHERE r2.event_id = res.event_id AND r2.class_id = res.class_id) as class_count
                    FROM results res
                    JOIN events e ON res.event_id = e.id
                    JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                    WHERE v.canonical_rider_id = ?
                      AND YEAR(e.date) = ?
                      AND res.position IS NOT NULL AND res.position > 0
                ) p WHERE class_count > 1
            ");
            $stmt->execute([$riderId, $year]);
            $percentile = $stmt->fetchColumn();
        }

        // Hamta klubb och klass
        $clubId = null;
        $classId = null;
        $discipline = null;

        if ($wasActive) {
            // Validera att club_id finns i clubs-tabellen (FK constraint)
            $stmt = $this->pdo->prepare("
                SELECT CASE WHEN c.id IS NOT NULL THEN r.club_id ELSE NULL END as club_id
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE r.id = ?
            ");
            $stmt->execute([$riderId]);
            $clubId = $stmt->fetchColumn() ?: null;

            $stmt = $this->pdo->prepare("
                SELECT res.class_id, COUNT(*) as cnt
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id = ? AND YEAR(e.date) = ? AND res.class_id IS NOT NULL
                GROUP BY res.class_id ORDER BY cnt DESC LIMIT 1
            ");
            $stmt->execute([$riderId, $year]);
            $row = $stmt->fetch();
            $classId = $row ? (int)$row['class_id'] : null;

            $stmt = $this->pdo->prepare("
                SELECT e.discipline, COUNT(*) as cnt
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                WHERE v.canonical_rider_id = ? AND YEAR(e.date) = ? AND e.discipline IS NOT NULL
                GROUP BY e.discipline ORDER BY cnt DESC LIMIT 1
            ");
            $stmt->execute([$riderId, $year]);
            $row = $stmt->fetch();
            $discipline = $row ? $row['discipline'] : null;
        }

        // Resolve primary brand for this year (v3.1.1)
        $brandData = $wasActive ? $this->resolvePrimaryBrandForYear($riderId, $year) : ['brand_id' => null, 'series_id' => null];

        return [
            'total_starts' => $wasActive ? (int)$data['total_starts'] : 0,
            'total_events' => $wasActive ? (int)$data['total_events'] : 0,
            'total_finishes' => $wasActive ? (int)$data['total_finishes'] : 0,
            'total_dnf' => $wasActive ? (int)$data['total_dnf'] : 0,
            'dnf_rate' => $wasActive && $data['total_starts'] > 0
                ? round($data['total_dnf'] / $data['total_starts'], 4)
                : null,
            'best_position' => $wasActive && $data['best_position'] ? (int)$data['best_position'] : null,
            'avg_position' => $wasActive && $data['avg_position'] ? round($data['avg_position'], 2) : null,
            'result_percentile' => $percentile ? round($percentile, 2) : null,
            'podium_count' => $wasActive ? (int)$data['podium_count'] : 0,
            'top10_count' => $wasActive ? (int)$data['top10_count'] : 0,
            'total_points' => $wasActive ? (int)$data['total_points'] : 0,
            'was_active' => $wasActive ? 1 : 0,
            'first_event_date' => $wasActive ? $data['first_event_date'] : null,
            'last_event_date' => $wasActive ? $data['last_event_date'] : null,
            'days_active' => $wasActive && $data['first_event_date'] && $data['last_event_date']
                ? (int)((strtotime($data['last_event_date']) - strtotime($data['first_event_date'])) / 86400)
                : null,
            'club_id' => $clubId,
            'class_id' => $classId,
            'primary_discipline' => $discipline,
            'primary_brand_id' => $brandData['brand_id'],
            'primary_series_id' => $brandData['series_id'],
        ];
    }

    /**
     * Spara rider journey year data
     */
    private function upsertRiderJourneyYear(
        int $riderId,
        int $cohortYear,
        int $yearOffset,
        int $calendarYear,
        array $metrics,
        ?int $snapshotId
    ): void {
        $stmt = $this->pdo->prepare("
            INSERT INTO rider_journey_years (
                rider_id, cohort_year, year_offset, calendar_year,
                total_starts, total_events, total_finishes, total_dnf, dnf_rate,
                best_position, avg_position, result_percentile,
                podium_count, top10_count, total_points,
                was_active, first_event_date, last_event_date, days_active,
                club_id, class_id, primary_discipline,
                primary_brand_id, primary_series_id,
                calculated_at, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?)
            ON DUPLICATE KEY UPDATE
                total_starts = VALUES(total_starts),
                total_events = VALUES(total_events),
                total_finishes = VALUES(total_finishes),
                total_dnf = VALUES(total_dnf),
                dnf_rate = VALUES(dnf_rate),
                best_position = VALUES(best_position),
                avg_position = VALUES(avg_position),
                result_percentile = VALUES(result_percentile),
                podium_count = VALUES(podium_count),
                top10_count = VALUES(top10_count),
                total_points = VALUES(total_points),
                was_active = VALUES(was_active),
                first_event_date = VALUES(first_event_date),
                last_event_date = VALUES(last_event_date),
                days_active = VALUES(days_active),
                club_id = VALUES(club_id),
                class_id = VALUES(class_id),
                primary_discipline = VALUES(primary_discipline),
                primary_brand_id = VALUES(primary_brand_id),
                primary_series_id = VALUES(primary_series_id),
                calculated_at = NOW(),
                snapshot_id = VALUES(snapshot_id)
        ");

        $stmt->execute([
            $riderId,
            $cohortYear,
            $yearOffset,
            $calendarYear,
            $metrics['total_starts'],
            $metrics['total_events'],
            $metrics['total_finishes'],
            $metrics['total_dnf'],
            $metrics['dnf_rate'],
            $metrics['best_position'],
            $metrics['avg_position'],
            $metrics['result_percentile'],
            $metrics['podium_count'],
            $metrics['top10_count'],
            $metrics['total_points'],
            $metrics['was_active'],
            $metrics['first_event_date'],
            $metrics['last_event_date'],
            $metrics['days_active'],
            $metrics['club_id'],
            $metrics['class_id'],
            $metrics['primary_discipline'],
            $metrics['primary_brand_id'] ?? null,
            $metrics['primary_series_id'] ?? null,
            $snapshotId
        ]);
    }

    /**
     * Uppdatera rider journey summary
     */
    private function updateRiderJourneySummary(int $riderId, int $cohortYear, ?int $snapshotId): void {
        // Hamta alla ar-data
        $stmt = $this->pdo->prepare("
            SELECT year_offset, was_active, total_starts, result_percentile
            FROM rider_journey_years
            WHERE rider_id = ? AND cohort_year = ?
            ORDER BY year_offset
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $years = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($years)) return;

        // Berakna pattern
        $y = [1 => 0, 2 => 0, 3 => 0, 4 => 0];
        $totalSeasons = 0;
        $lastActiveOffset = 0;

        foreach ($years as $yr) {
            $offset = (int)$yr['year_offset'];
            $y[$offset] = (int)$yr['was_active'];
            if ($y[$offset]) {
                $totalSeasons++;
                $lastActiveOffset = $offset;
            }
        }

        // Klassificera pattern
        $pattern = 'one_and_done';
        if ($y[1] && $y[2] && $y[3] && $y[4]) {
            $pattern = 'continuous_4yr';
        } elseif ($y[1] && $y[2] && $y[3]) {
            $pattern = 'continuous_3yr';
        } elseif ($y[1] && $y[2] && !$y[3] && !$y[4]) {
            $pattern = 'continuous_2yr';
        } elseif ($y[1] && !$y[2] && !$y[3] && !$y[4]) {
            $pattern = 'one_and_done';
        } elseif (($y[1] && !$y[2] && $y[3]) || ($y[1] && !$y[2] && $y[4]) || ($y[2] && !$y[3] && $y[4])) {
            $pattern = 'gap_returner';
        } elseif ($totalSeasons >= 2 && $lastActiveOffset < 4) {
            $pattern = 'late_dropout';
        }

        // Hamta aggregerade karriardata
        $stmt = $this->pdo->prepare("
            SELECT
                SUM(total_starts) as career_starts,
                SUM(total_events) as career_events,
                SUM(total_finishes) as career_finishes,
                MIN(best_position) as career_best,
                AVG(CASE WHEN result_percentile IS NOT NULL THEN result_percentile END) as career_percentile,
                SUM(podium_count) as career_podiums,
                SUM(total_points) as career_points
            FROM rider_journey_years
            WHERE rider_id = ? AND cohort_year = ?
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $career = $stmt->fetch(PDO::FETCH_ASSOC);

        // Hamta first season data
        $stmt = $this->pdo->prepare("
            SELECT total_starts, result_percentile, engagement_score, activity_pattern
            FROM rider_first_season
            WHERE rider_id = ? AND cohort_year = ?
        ");
        $stmt->execute([$riderId, $cohortYear]);
        $fs = $stmt->fetch(PDO::FETCH_ASSOC);

        // Berakna trajektorier
        $percTrajectory = 'insufficient_data';
        $actTrajectory = 'sporadic';

        if ($totalSeasons >= 2) {
            // Percentil trajectory
            $firstPerc = null;
            $lastPerc = null;
            foreach ($years as $yr) {
                if ($yr['result_percentile'] !== null) {
                    if ($firstPerc === null) $firstPerc = (float)$yr['result_percentile'];
                    $lastPerc = (float)$yr['result_percentile'];
                }
            }
            if ($firstPerc !== null && $lastPerc !== null) {
                $percDiff = $lastPerc - $firstPerc;
                if ($percDiff > 5) $percTrajectory = 'improving';
                elseif ($percDiff < -5) $percTrajectory = 'declining';
                else $percTrajectory = 'stable';
            }

            // Activity trajectory
            $y1Starts = 0;
            $laterStarts = 0;
            $laterCount = 0;
            foreach ($years as $yr) {
                if ((int)$yr['year_offset'] === 1) {
                    $y1Starts = (int)$yr['total_starts'];
                } elseif ((int)$yr['was_active']) {
                    $laterStarts += (int)$yr['total_starts'];
                    $laterCount++;
                }
            }
            if ($laterCount > 0) {
                $avgLater = $laterStarts / $laterCount;
                if ($avgLater > $y1Starts + 1) $actTrajectory = 'increasing';
                elseif ($avgLater < $y1Starts - 1) $actTrajectory = 'decreasing';
                else $actTrajectory = 'stable';
            }
        }

        // Upsert summary
        $stmt = $this->pdo->prepare("
            INSERT INTO rider_journey_summary (
                rider_id, cohort_year,
                total_seasons_active, last_active_year_offset,
                journey_pattern,
                total_career_starts, total_career_events, total_career_finishes,
                career_dnf_rate, career_best_position, career_avg_percentile,
                career_podium_count,
                percentile_trajectory, activity_trajectory,
                fs_total_starts, fs_result_percentile, fs_engagement_score, fs_activity_pattern,
                calculated_at, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?)
            ON DUPLICATE KEY UPDATE
                total_seasons_active = VALUES(total_seasons_active),
                last_active_year_offset = VALUES(last_active_year_offset),
                journey_pattern = VALUES(journey_pattern),
                total_career_starts = VALUES(total_career_starts),
                total_career_events = VALUES(total_career_events),
                total_career_finishes = VALUES(total_career_finishes),
                career_dnf_rate = VALUES(career_dnf_rate),
                career_best_position = VALUES(career_best_position),
                career_avg_percentile = VALUES(career_avg_percentile),
                career_podium_count = VALUES(career_podium_count),
                percentile_trajectory = VALUES(percentile_trajectory),
                activity_trajectory = VALUES(activity_trajectory),
                fs_total_starts = VALUES(fs_total_starts),
                fs_result_percentile = VALUES(fs_result_percentile),
                fs_engagement_score = VALUES(fs_engagement_score),
                fs_activity_pattern = VALUES(fs_activity_pattern),
                calculated_at = NOW(),
                snapshot_id = VALUES(snapshot_id)
        ");

        $careerDnfRate = $career['career_starts'] > 0
            ? round(($career['career_starts'] - $career['career_finishes']) / $career['career_starts'], 4)
            : null;

        $stmt->execute([
            $riderId,
            $cohortYear,
            $totalSeasons,
            $lastActiveOffset,
            $pattern,
            $career['career_starts'] ?: 0,
            $career['career_events'] ?: 0,
            $career['career_finishes'] ?: 0,
            $careerDnfRate,
            $career['career_best'],
            $career['career_percentile'] ? round($career['career_percentile'], 2) : null,
            $career['career_podiums'] ?: 0,
            $percTrajectory,
            $actTrajectory,
            $fs['total_starts'] ?? null,
            $fs['result_percentile'] ?? null,
            $fs['engagement_score'] ?? null,
            $fs['activity_pattern'] ?? null,
            $snapshotId
        ]);
    }

    /**
     * Berakna cohort longitudinal aggregates
     */
    private function calculateCohortLongitudinalAggregates(int $cohortYear, ?int $snapshotId): void {
        $minSize = 10;

        // Hamta kohort-storlek
        $cohortSize = $this->pdo->prepare("
            SELECT COUNT(*) FROM rider_first_season WHERE cohort_year = ?
        ");
        $cohortSize->execute([$cohortYear]);
        $totalCohort = (int)$cohortSize->fetchColumn();

        if ($totalCohort < $minSize) return;

        // Rensa gamla aggregat
        $this->pdo->prepare("
            DELETE FROM cohort_longitudinal_aggregates WHERE cohort_year = ?
        ")->execute([$cohortYear]);

        // For varje year_offset (1-4)
        for ($offset = 1; $offset <= 4; $offset++) {
            $calendarYear = $cohortYear + $offset - 1;
            if ($calendarYear > (int)date('Y')) continue;

            $stmt = $this->pdo->prepare("
                SELECT
                    SUM(was_active) as active_count,
                    AVG(CASE WHEN was_active = 1 THEN total_starts END) as avg_starts,
                    AVG(CASE WHEN was_active = 1 THEN total_events END) as avg_events,
                    AVG(CASE WHEN was_active = 1 THEN dnf_rate END) as avg_dnf,
                    AVG(CASE WHEN was_active = 1 THEN result_percentile END) as avg_perc
                FROM rider_journey_years
                WHERE cohort_year = ? AND year_offset = ?
            ");
            $stmt->execute([$cohortYear, $offset]);
            $data = $stmt->fetch(PDO::FETCH_ASSOC);

            $activeCount = (int)($data['active_count'] ?? 0);
            $retention = $totalCohort > 0 ? $activeCount / $totalCohort : 0;

            $insert = $this->pdo->prepare("
                INSERT INTO cohort_longitudinal_aggregates (
                    cohort_year, year_offset, segment_type, segment_value,
                    total_riders_in_cohort, active_riders_this_year,
                    retention_rate, churn_rate,
                    avg_starts, avg_events, avg_dnf_rate, avg_percentile,
                    calculated_at, snapshot_id
                ) VALUES (?, ?, 'overall', NULL, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), ?)
                ON DUPLICATE KEY UPDATE
                    total_riders_in_cohort = VALUES(total_riders_in_cohort),
                    active_riders_this_year = VALUES(active_riders_this_year),
                    retention_rate = VALUES(retention_rate),
                    churn_rate = VALUES(churn_rate),
                    avg_starts = VALUES(avg_starts),
                    avg_events = VALUES(avg_events),
                    avg_dnf_rate = VALUES(avg_dnf_rate),
                    avg_percentile = VALUES(avg_percentile),
                    calculated_at = NOW(),
                    snapshot_id = VALUES(snapshot_id)
            ");

            $insert->execute([
                $cohortYear,
                $offset,
                $totalCohort,
                $activeCount,
                round($retention, 4),
                round(1 - $retention, 4),
                $data['avg_starts'] ? round($data['avg_starts'], 2) : null,
                $data['avg_events'] ? round($data['avg_events'], 2) : null,
                $data['avg_dnf'] ? round($data['avg_dnf'], 4) : null,
                $data['avg_perc'] ? round($data['avg_perc'], 2) : null,
                $snapshotId
            ]);
        }
    }

    /**
     * Kor alla journey-berakningar for en kohort
     *
     * @param int $cohortYear
     * @param int|null $snapshotId
     * @return array Resultat
     */
    public function calculateFullJourneyAnalysis(int $cohortYear, ?int $snapshotId = null): array {
        $results = [];

        $results['first_season'] = $this->calculateFirstSeasonJourney($cohortYear, $snapshotId);
        $results['first_season_aggregates'] = $this->calculateFirstSeasonAggregates($cohortYear, $snapshotId);
        $results['longitudinal'] = $this->calculateLongitudinalJourney($cohortYear, $snapshotId);
        $results['brand_aggregates'] = $this->calculateBrandJourneyAggregates($cohortYear, $snapshotId);

        return $results;
    }

    /**
     * Hamta tillgangliga kohortar
     *
     * @return array Lista med kohortar (year => count)
     */
    public function getAvailableCohorts(): array {
        $stmt = $this->pdo->query("
            SELECT
                cohort_year,
                COUNT(*) as rookie_count
            FROM (
                SELECT
                    v.canonical_rider_id,
                    MIN(YEAR(e.date)) as cohort_year
                FROM results res
                JOIN events e ON res.event_id = e.id
                JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
                GROUP BY v.canonical_rider_id
            ) cohorts
            GROUP BY cohort_year
            ORDER BY cohort_year DESC
        ");
        return $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
    }
}
