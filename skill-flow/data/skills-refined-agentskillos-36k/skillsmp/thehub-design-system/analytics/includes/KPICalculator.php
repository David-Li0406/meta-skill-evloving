<?php
/**
 * KPICalculator
 *
 * Beraknar alla KPI:er baserat pa pre-beraknad data i analytics-tabellerna.
 * Anvands av dashboard och rapportgeneratorn.
 *
 * Huvudkategorier:
 * - Retention & Growth (retention rate, churn rate, growth)
 * - Demographics (alder, kon, disciplin)
 * - Series Flow (feeder conversion, cross-participation, loyalty)
 * - Club (top klubbar, tillvaxt)
 * - Geographic (regioner)
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

class KPICalculator {
    private PDO $pdo;

    /**
     * Constructor
     *
     * @param PDO $pdo Databasanslutning
     */
    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }

    // =========================================================================
    // UTILITY METHODS
    // =========================================================================

    /**
     * Hamta senaste sasong med data (avslutad sasong)
     *
     * Returnerar det senaste aret som har rider_yearly_stats data.
     * Anvands for att undvika att rakna pagaende sasong som "inaktiv".
     *
     * @return int Senaste ar med data, eller foregaende ar om inget hittas
     */
    public function getLatestSeasonYear(): int {
        $stmt = $this->pdo->query("
            SELECT MAX(season_year) FROM rider_yearly_stats
        ");
        $result = $stmt->fetchColumn();

        if ($result) {
            return (int)$result;
        }

        // Fallback till foregaende ar om ingen data finns
        return (int)date('Y') - 1;
    }

    /**
     * Hamta senaste sasong med tillracklig data
     *
     * Returnerar det senaste aret som har minst X antal riders.
     * Anvands for att sakerstalla att vi har meningsfull data.
     *
     * @param int $minRiders Minimum antal riders for att raknas
     * @return int Senaste ar med tillracklig data
     */
    public function getLatestCompleteSeasonYear(int $minRiders = 100): int {
        $stmt = $this->pdo->prepare("
            SELECT season_year
            FROM rider_yearly_stats
            GROUP BY season_year
            HAVING COUNT(*) >= ?
            ORDER BY season_year DESC
            LIMIT 1
        ");
        $stmt->execute([$minRiders]);
        $result = $stmt->fetchColumn();

        return $result ? (int)$result : $this->getLatestSeasonYear();
    }

    // =========================================================================
    // RETENTION & GROWTH
    // =========================================================================

    /**
     * Berakna retention rate (andel som aterkom fran forra aret)
     *
     * När brandId anges: beräknar baserat på faktisk deltagande i varumärkets events,
     * inte primary_series_id. Detta ger konsistenta siffror med Event Participation.
     *
     * @param int $year Ar att berakna for
     * @param int|null $brandId Filtrera pa varumarke
     * @return float Retention rate i procent (0-100)
     */
    public function getRetentionRate(int $year, ?int $brandId = null): float {
        if ($brandId !== null) {
            // Använd faktiskt deltagande i varumärkets events
            $prevYear = $year - 1;
            $totalPrev = $this->getTotalActiveRiders($prevYear, $brandId);
            if ($totalPrev == 0) return 0;

            $retained = $this->getRetainedRidersCount($year, $brandId);
            return round(($retained / $totalPrev) * 100, 1);
        }

        // Utan brand: använd aggregerad data
        $stmt = $this->pdo->prepare("
            SELECT
                ROUND(
                    COUNT(DISTINCT CASE WHEN curr.rider_id IS NOT NULL THEN prev.rider_id END) * 100.0 /
                    NULLIF(COUNT(DISTINCT prev.rider_id), 0), 1
                ) as retention_rate
            FROM rider_yearly_stats prev
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = prev.season_year + 1
            WHERE prev.season_year = ?
        ");
        $stmt->execute([$year - 1]);
        return (float)($stmt->fetchColumn() ?: 0);
    }

    /**
     * Berakna churn rate (andel som forsvann fran forra aret)
     *
     * @param int $year Ar att berakna for
     * @param int|null $brandId Filtrera pa varumarke
     * @return float Churn rate i procent (0-100)
     */
    public function getChurnRate(int $year, ?int $brandId = null): float {
        return 100 - $this->getRetentionRate($year, $brandId);
    }

    /**
     * Hamta antal nya riders (rookies)
     *
     * När brandId anges: räknar riders som deltog i varumärkets events detta år
     * men INTE i något tidigare år (nya till varumärket).
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return int Antal nya riders
     */
    public function getNewRidersCount(int $year, ?int $brandId = null): int {
        if ($brandId !== null) {
            // Räkna riders som deltog i varumärket detta år men inte tidigare
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT current_riders.cyclist_id)
                FROM (
                    SELECT DISTINCT r.cyclist_id
                    FROM results r
                    JOIN events e ON e.id = r.event_id
                    JOIN series_events se ON se.event_id = e.id
                    JOIN series s ON s.id = se.series_id
                    WHERE YEAR(e.date) = ?
                    AND s.brand_id = ?
                ) current_riders
                WHERE current_riders.cyclist_id NOT IN (
                    SELECT DISTINCT r2.cyclist_id
                    FROM results r2
                    JOIN events e2 ON e2.id = r2.event_id
                    JOIN series_events se2 ON se2.event_id = e2.id
                    JOIN series s2 ON s2.id = se2.series_id
                    WHERE YEAR(e2.date) < ?
                    AND s2.brand_id = ?
                )
            ");
            $stmt->execute([$year, $brandId, $year, $brandId]);
            return (int)$stmt->fetchColumn();
        }

        // Utan brand: använd aggregerad data (globala rookies)
        $stmt = $this->pdo->prepare("
            SELECT COUNT(*) FROM rider_yearly_stats rys
            WHERE rys.season_year = ? AND rys.is_rookie = 1
        ");
        $stmt->execute([$year]);
        return (int)$stmt->fetchColumn();
    }

    /**
     * Hämta feeder-serie-breakdown för ett varumärke
     * Visar varifrån nya riders kommer (vilken serie de tävlade i innan)
     *
     * @param int $year År
     * @param int $brandId Varumärkes-ID
     * @return array ['true_rookies' => int, 'crossover' => int, 'feeder_series' => [...]]
     */
    public function getFeederSeriesBreakdown(int $year, int $brandId): array {
        // Hitta alla riders som deltog i detta varumärke detta år
        // och vars första deltagande i varumärket var detta år
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT sp.rider_id
            FROM series_participation sp
            JOIN series s ON sp.series_id = s.id
            WHERE s.brand_id = ?
            AND sp.season_year = ?
            AND sp.rider_id IN (
                -- Riders vars första år i detta varumärke var detta år
                SELECT sp2.rider_id
                FROM series_participation sp2
                JOIN series s2 ON sp2.series_id = s2.id
                WHERE s2.brand_id = ?
                GROUP BY sp2.rider_id
                HAVING MIN(sp2.season_year) = ?
            )
        ");
        $stmt->execute([$brandId, $year, $brandId, $year]);
        $newToBrandRiders = $stmt->fetchAll(PDO::FETCH_COLUMN);

        if (empty($newToBrandRiders)) {
            return [
                'total_new' => 0,
                'true_rookies' => 0,
                'crossover' => 0,
                'feeder_series' => []
            ];
        }

        // Hitta vilka av dessa som är true rookies (aldrig tävlat någonstans innan)
        $placeholders = implode(',', array_fill(0, count($newToBrandRiders), '?'));
        $stmt = $this->pdo->prepare("
            SELECT rider_id
            FROM rider_yearly_stats
            WHERE rider_id IN ($placeholders)
            GROUP BY rider_id
            HAVING MIN(season_year) = ?
        ");
        $params = array_merge($newToBrandRiders, [$year]);
        $stmt->execute($params);
        $trueRookies = $stmt->fetchAll(PDO::FETCH_COLUMN);

        // Crossover riders = nya i varumärket men inte true rookies
        $crossoverRiders = array_diff($newToBrandRiders, $trueRookies);

        // Hitta feeder-serier för crossover riders (endast aktiva varumärken)
        $feederSeries = [];
        if (!empty($crossoverRiders)) {
            $placeholders = implode(',', array_fill(0, count($crossoverRiders), '?'));
            $stmt = $this->pdo->prepare("
                SELECT
                    b.id as brand_id,
                    b.name as brand_name,
                    COUNT(DISTINCT sp.rider_id) as rider_count
                FROM series_participation sp
                JOIN series s ON sp.series_id = s.id
                JOIN series_brands b ON s.brand_id = b.id
                WHERE sp.rider_id IN ($placeholders)
                AND sp.season_year < ?
                AND s.brand_id != ?
                AND b.active = 1
                GROUP BY b.id, b.name
                ORDER BY rider_count DESC
            ");
            $params = array_merge(array_values($crossoverRiders), [$year, $brandId]);
            $stmt->execute($params);
            $feederSeries = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }

        return [
            'total_new' => count($newToBrandRiders),
            'true_rookies' => count($trueRookies),
            'crossover' => count($crossoverRiders),
            'feeder_series' => $feederSeries
        ];
    }

    /**
     * Hämta exit-analys för ett varumärke
     * Visar vart riders går när de slutar (fortsätter de i andra serier?)
     *
     * @param int $year År då de slutade
     * @param int $brandId Varumärkes-ID
     * @return array ['total_churned' => int, 'quit_completely' => int, 'continued_elsewhere' => int, 'destination_series' => [...]]
     */
    public function getExitDestinationAnalysis(int $year, int $brandId): array {
        // Hitta riders som var aktiva i varumärket året innan men INTE detta år
        $prevYear = $year - 1;

        // Riders aktiva i brand förra året
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT sp.rider_id
            FROM series_participation sp
            JOIN series s ON sp.series_id = s.id
            WHERE s.brand_id = ?
            AND sp.season_year = ?
        ");
        $stmt->execute([$brandId, $prevYear]);
        $prevYearRiders = $stmt->fetchAll(PDO::FETCH_COLUMN);

        if (empty($prevYearRiders)) {
            return [
                'total_churned' => 0,
                'quit_completely' => 0,
                'continued_elsewhere' => 0,
                'destination_series' => []
            ];
        }

        // Riders som fortfarande är i samma brand detta år
        $placeholders = implode(',', array_fill(0, count($prevYearRiders), '?'));
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT sp.rider_id
            FROM series_participation sp
            JOIN series s ON sp.series_id = s.id
            WHERE s.brand_id = ?
            AND sp.season_year = ?
            AND sp.rider_id IN ($placeholders)
        ");
        $params = array_merge([$brandId, $year], $prevYearRiders);
        $stmt->execute($params);
        $stillActiveRiders = $stmt->fetchAll(PDO::FETCH_COLUMN);

        // Churned riders = var med förra året men inte detta år i samma brand
        $churnedRiders = array_diff($prevYearRiders, $stillActiveRiders);

        if (empty($churnedRiders)) {
            return [
                'total_churned' => 0,
                'quit_completely' => 0,
                'continued_elsewhere' => 0,
                'destination_series' => []
            ];
        }

        // Kolla vilka av churned riders som fortsatte i NÅGON serie detta år
        $placeholders = implode(',', array_fill(0, count($churnedRiders), '?'));
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT rider_id
            FROM rider_yearly_stats
            WHERE rider_id IN ($placeholders)
            AND season_year = ?
        ");
        $params = array_merge(array_values($churnedRiders), [$year]);
        $stmt->execute($params);
        $continuedAnywhere = $stmt->fetchAll(PDO::FETCH_COLUMN);

        // Riders som slutade helt
        $quitCompletely = array_diff($churnedRiders, $continuedAnywhere);

        // Hitta destination-serier för de som fortsatte i andra brands (endast aktiva varumärken)
        $destinationSeries = [];
        if (!empty($continuedAnywhere)) {
            $placeholders = implode(',', array_fill(0, count($continuedAnywhere), '?'));
            $stmt = $this->pdo->prepare("
                SELECT
                    b.id as brand_id,
                    b.name as brand_name,
                    COUNT(DISTINCT sp.rider_id) as rider_count
                FROM series_participation sp
                JOIN series s ON sp.series_id = s.id
                JOIN series_brands b ON s.brand_id = b.id
                WHERE sp.rider_id IN ($placeholders)
                AND sp.season_year = ?
                AND s.brand_id != ?
                AND b.active = 1
                GROUP BY b.id, b.name
                ORDER BY rider_count DESC
            ");
            $params = array_merge(array_values($continuedAnywhere), [$year, $brandId]);
            $stmt->execute($params);
            $destinationSeries = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }

        return [
            'total_churned' => count($churnedRiders),
            'quit_completely' => count($quitCompletely),
            'continued_elsewhere' => count($continuedAnywhere),
            'destination_series' => $destinationSeries
        ];
    }

    /**
     * Hämta totalt antal aktiva riders
     *
     * När brandId anges: räknar alla unika riders som deltog i minst ett
     * event för varumärket (samma logik som Event Participation).
     * Utan brandId: räknar från rider_yearly_stats.
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return int Antal aktiva riders
     */
    public function getTotalActiveRiders(int $year, ?int $brandId = null): int {
        if ($brandId !== null) {
            // Räkna alla unika deltagare i events för varumärket
            // Samma logik som Event Participation för att få konsistenta siffror
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT r.cyclist_id)
                FROM results r
                JOIN events e ON e.id = r.event_id
                JOIN series_events se ON se.event_id = e.id
                JOIN series s ON s.id = se.series_id
                WHERE YEAR(e.date) = ?
                AND s.brand_id = ?
            ");
            $stmt->execute([$year, $brandId]);
            return (int)$stmt->fetchColumn();
        }

        // Utan brand: använd aggregerad data
        $stmt = $this->pdo->prepare("
            SELECT COUNT(*) FROM rider_yearly_stats rys
            WHERE rys.season_year = ?
        ");
        $stmt->execute([$year]);
        return (int)$stmt->fetchColumn();
    }

    /**
     * Hämta antal deltagare för en specifik serie
     *
     * @param int $year År
     * @param int $seriesId Serie-ID
     * @return int Antal unika deltagare
     */
    public function getSeriesParticipants(int $year, int $seriesId): int {
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT r.cyclist_id)
            FROM results r
            JOIN events e ON e.id = r.event_id
            JOIN series_events se ON se.event_id = e.id
            WHERE se.series_id = ?
            AND YEAR(e.date) = ?
        ");
        $stmt->execute([$seriesId, $year]);
        return (int)$stmt->fetchColumn();
    }

    /**
     * Berakna tillvaxtrate jamfort med forriga aret
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return float Tillvaxt i procent (kan vara negativ)
     */
    public function getGrowthRate(int $year, ?int $brandId = null): float {
        $current = $this->getTotalActiveRiders($year, $brandId);
        $previous = $this->getTotalActiveRiders($year - 1, $brandId);

        if ($previous == 0) return 0;

        return round(($current - $previous) / $previous * 100, 1);
    }

    /**
     * Hamta retained riders count
     *
     * När brandId anges: räknar riders som deltog i varumärkets events
     * både i år och förra året (återkommande till varumärket).
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return int Antal
     */
    public function getRetainedRidersCount(int $year, ?int $brandId = null): int {
        if ($brandId !== null) {
            // Riders som deltog i varumärket både i år och förra året
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT current_year.cyclist_id)
                FROM (
                    SELECT DISTINCT r.cyclist_id
                    FROM results r
                    JOIN events e ON e.id = r.event_id
                    JOIN series_events se ON se.event_id = e.id
                    JOIN series s ON s.id = se.series_id
                    WHERE YEAR(e.date) = ?
                    AND s.brand_id = ?
                ) current_year
                INNER JOIN (
                    SELECT DISTINCT r.cyclist_id
                    FROM results r
                    JOIN events e ON e.id = r.event_id
                    JOIN series_events se ON se.event_id = e.id
                    JOIN series s ON s.id = se.series_id
                    WHERE YEAR(e.date) = ?
                    AND s.brand_id = ?
                ) previous_year ON current_year.cyclist_id = previous_year.cyclist_id
            ");
            $stmt->execute([$year, $brandId, $year - 1, $brandId]);
            return (int)$stmt->fetchColumn();
        }

        // Utan brand: använd aggregerad data
        $stmt = $this->pdo->prepare("
            SELECT COUNT(*) FROM rider_yearly_stats rys
            WHERE rys.season_year = ? AND rys.is_retained = 1
        ");
        $stmt->execute([$year]);
        return (int)$stmt->fetchColumn();
    }

    /**
     * Berakna "Returning Share of Current Year"
     *
     * DEFINITION: Andel av ARETS riders som OCKSA deltog forra aret.
     * Formel: (riders i bade N och N-1) / (riders i N) * 100
     *
     * Svarar pa: "Hur stor andel av arets deltagare ar aterkommande?"
     *
     * SKILLNAD MOT getRetentionRate():
     * - getRetentionRate() har denominator = forra arets riders
     * - getReturningShareOfCurrent() har denominator = arets riders
     *
     * @param int $year Ar att berakna for
     * @return float Procent (0-100)
     */
    public function getReturningShareOfCurrent(int $year): float {
        $stmt = $this->pdo->prepare("
            SELECT
                ROUND(
                    COUNT(DISTINCT CASE WHEN prev.rider_id IS NOT NULL THEN curr.rider_id END) * 100.0 /
                    NULLIF(COUNT(DISTINCT curr.rider_id), 0), 1
                ) as returning_share
            FROM rider_yearly_stats curr
            LEFT JOIN rider_yearly_stats prev
                ON curr.rider_id = prev.rider_id
                AND prev.season_year = curr.season_year - 1
            WHERE curr.season_year = ?
        ");
        $stmt->execute([$year]);
        return (float)($stmt->fetchColumn() ?: 0);
    }

    /**
     * Berakna rookie rate (andel nya deltagare)
     *
     * DEFINITION: Andel av arets riders som ar nya (forsta aret).
     * Formel: (riders med is_rookie=1) / (alla riders ar N) * 100
     *
     * @param int $year Ar
     * @return float Procent (0-100)
     */
    public function getRookieRate(int $year): float {
        $total = $this->getTotalActiveRiders($year);
        if ($total == 0) return 0;

        $rookies = $this->getNewRidersCount($year);
        return round($rookies / $total * 100, 1);
    }

    /**
     * Hamta kompletta retention-nyckeltal for ett ar
     *
     * Returnerar alla retention-relaterade KPIs pa ett stalle
     * for tydlighet och dokumentation.
     *
     * @param int $year Ar
     * @return array Alla retention-KPIs
     */
    public function getRetentionMetrics(int $year): array {
        $totalCurrent = $this->getTotalActiveRiders($year);
        $totalPrev = $this->getTotalActiveRiders($year - 1);
        $retained = $this->getRetainedRidersCount($year);
        $rookies = $this->getNewRidersCount($year);

        return [
            // Grunddata
            'year' => $year,
            'total_riders_current' => $totalCurrent,
            'total_riders_previous' => $totalPrev,
            'retained_count' => $retained,
            'rookie_count' => $rookies,
            'churned_count' => $totalPrev - $retained,

            // KPIs med tydliga namn och definitioner
            'retention_from_prev' => [
                'value' => $this->getRetentionRate($year),
                'definition' => 'Andel av forra arets riders som aterkommer',
                'formula' => 'retained / prev_total * 100',
            ],
            'returning_share_of_current' => [
                'value' => $this->getReturningShareOfCurrent($year),
                'definition' => 'Andel av arets riders som ocksa deltog forra aret',
                'formula' => 'retained / current_total * 100',
            ],
            'churn_rate' => [
                'value' => $this->getChurnRate($year),
                'definition' => 'Andel av forra arets riders som INTE aterkommer',
                'formula' => '100 - retention_from_prev',
            ],
            'rookie_rate' => [
                'value' => $this->getRookieRate($year),
                'definition' => 'Andel av arets riders som ar nya',
                'formula' => 'rookies / current_total * 100',
            ],
            'growth_rate' => [
                'value' => $this->getGrowthRate($year),
                'definition' => 'Procentuell forandring i antal riders',
                'formula' => '(current - prev) / prev * 100',
            ],
        ];
    }

    // =========================================================================
    // DATA QUALITY METRICS
    // =========================================================================

    /**
     * Berakna datakvalitetsmatningar for ett ar
     *
     * Returnerar procentuell tackning for varje viktigt falt
     * samt absoluta tal for saknade varden.
     *
     * @param int $year Sasong att mata
     * @return array Datakvalitetsdata
     */
    public function getDataQualityMetrics(int $year): array {
        // Total antal riders for aret
        $totalRiders = $this->getTotalActiveRiders($year);

        if ($totalRiders == 0) {
            return [
                'year' => $year,
                'total_riders' => 0,
                'error' => 'Ingen data for aret',
            ];
        }

        // Birth year coverage
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rys.rider_id) as with_birth_year
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
        ");
        $stmt->execute([$year]);
        $withBirthYear = (int)$stmt->fetchColumn();

        // Club coverage
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rys.rider_id) as with_club
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND r.club_id IS NOT NULL
        ");
        $stmt->execute([$year]);
        $withClub = (int)$stmt->fetchColumn();

        // Gender coverage
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rys.rider_id) as with_gender
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND r.gender IS NOT NULL
              AND r.gender != ''
        ");
        $stmt->execute([$year]);
        $withGender = (int)$stmt->fetchColumn();

        // Results with class
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(*) as total_results,
                SUM(CASE WHEN class_id IS NOT NULL THEN 1 ELSE 0 END) as with_class
            FROM results res
            JOIN events e ON res.event_id = e.id
            WHERE YEAR(e.date) = ?
        ");
        $stmt->execute([$year]);
        $resultsData = $stmt->fetch();
        $totalResults = (int)$resultsData['total_results'];
        $withClass = (int)$resultsData['with_class'];

        // Events with date
        $stmt = $this->pdo->prepare("
            SELECT
                COUNT(*) as total_events,
                SUM(CASE WHEN date IS NOT NULL THEN 1 ELSE 0 END) as with_date
            FROM events
            WHERE YEAR(date) = ? OR date IS NULL
        ");
        $stmt->execute([$year]);
        $eventsData = $stmt->fetch();
        $totalEvents = (int)$eventsData['total_events'];
        $eventsWithDate = (int)$eventsData['with_date'];

        // Potential duplicates (simplified check)
        $stmt = $this->pdo->prepare("
            SELECT COUNT(*) as potential_dupes
            FROM (
                SELECT firstname, lastname, birth_year
                FROM riders r
                JOIN rider_yearly_stats rys ON r.id = rys.rider_id
                WHERE rys.season_year = ?
                  AND r.firstname IS NOT NULL
                  AND r.lastname IS NOT NULL
                GROUP BY LOWER(firstname), LOWER(lastname), birth_year
                HAVING COUNT(*) > 1
            ) dupes
        ");
        $stmt->execute([$year]);
        $potentialDupes = (int)$stmt->fetchColumn();

        // Merged riders
        $stmt = $this->pdo->query("SELECT COUNT(*) FROM rider_merge_map");
        $mergedRiders = (int)$stmt->fetchColumn();

        return [
            'year' => $year,
            'measured_at' => date('Y-m-d H:i:s'),
            'total_riders' => $totalRiders,

            // Procentuell tackning
            'birth_year_coverage' => round($withBirthYear / $totalRiders * 100, 1),
            'club_coverage' => round($withClub / $totalRiders * 100, 1),
            'gender_coverage' => round($withGender / $totalRiders * 100, 1),
            'class_coverage' => $totalResults > 0 ? round($withClass / $totalResults * 100, 1) : 0,
            'event_date_coverage' => $totalEvents > 0 ? round($eventsWithDate / $totalEvents * 100, 1) : 0,

            // Absoluta tal (saknade)
            'riders_missing_birth_year' => $totalRiders - $withBirthYear,
            'riders_missing_club' => $totalRiders - $withClub,
            'riders_missing_gender' => $totalRiders - $withGender,
            'results_missing_class' => $totalResults - $withClass,

            // Identitetsproblem
            'potential_duplicates' => $potentialDupes,
            'merged_riders' => $mergedRiders,

            // Status
            'quality_status' => $this->assessQualityStatus(
                $withBirthYear / $totalRiders,
                $withClub / $totalRiders,
                $totalResults > 0 ? $withClass / $totalResults : 0
            ),
        ];
    }

    /**
     * Bedom datakvalitetsstatus
     *
     * @param float $birthYearCov Birth year coverage (0-1)
     * @param float $clubCov Club coverage (0-1)
     * @param float $classCov Class coverage (0-1)
     * @return string Status: good, warning, critical
     */
    private function assessQualityStatus(float $birthYearCov, float $clubCov, float $classCov): string {
        // Ladda thresholds fran config
        require_once __DIR__ . '/AnalyticsConfig.php';
        $thresholds = AnalyticsConfig::DATA_QUALITY_THRESHOLDS;

        $issues = 0;
        if ($birthYearCov < $thresholds['birth_year_coverage']) $issues++;
        if ($clubCov < $thresholds['club_coverage']) $issues++;
        if ($classCov < ($thresholds['class_coverage'] ?? 0.7)) $issues++;

        if ($issues >= 2) return 'critical';
        if ($issues >= 1) return 'warning';
        return 'good';
    }

    /**
     * Spara datakvalitetsmatning till databas
     *
     * @param int $year Sasong
     * @return bool Lyckades
     */
    public function saveDataQualityMetrics(int $year): bool {
        $metrics = $this->getDataQualityMetrics($year);

        if (isset($metrics['error'])) {
            return false;
        }

        require_once __DIR__ . '/AnalyticsConfig.php';

        $stmt = $this->pdo->prepare("
            INSERT INTO data_quality_metrics (
                season_year, measured_at,
                birth_year_coverage, club_coverage, gender_coverage,
                class_coverage, event_date_coverage,
                total_riders, riders_missing_birth_year, riders_missing_club,
                riders_missing_gender, results_missing_class,
                potential_duplicates, merged_riders,
                calculation_version
            ) VALUES (?, NOW(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                birth_year_coverage = VALUES(birth_year_coverage),
                club_coverage = VALUES(club_coverage),
                gender_coverage = VALUES(gender_coverage),
                class_coverage = VALUES(class_coverage),
                event_date_coverage = VALUES(event_date_coverage),
                total_riders = VALUES(total_riders),
                riders_missing_birth_year = VALUES(riders_missing_birth_year),
                riders_missing_club = VALUES(riders_missing_club),
                riders_missing_gender = VALUES(riders_missing_gender),
                results_missing_class = VALUES(results_missing_class),
                potential_duplicates = VALUES(potential_duplicates),
                merged_riders = VALUES(merged_riders),
                calculation_version = VALUES(calculation_version),
                measured_at = NOW()
        ");

        return $stmt->execute([
            $year,
            $metrics['birth_year_coverage'],
            $metrics['club_coverage'],
            $metrics['gender_coverage'],
            $metrics['class_coverage'],
            $metrics['event_date_coverage'],
            $metrics['total_riders'],
            $metrics['riders_missing_birth_year'],
            $metrics['riders_missing_club'],
            $metrics['riders_missing_gender'],
            $metrics['results_missing_class'],
            $metrics['potential_duplicates'],
            $metrics['merged_riders'],
            AnalyticsConfig::CALCULATION_VERSION,
        ]);
    }

    // =========================================================================
    // DEMOGRAPHICS
    // =========================================================================

    /**
     * Berakna genomsnittsalder
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return float Genomsnittsalder
     */
    public function getAverageAge(int $year, ?int $brandId = null): float {
        if ($brandId !== null) {
            // Använd faktiskt deltagande i varumärkets events
            $stmt = $this->pdo->prepare("
                SELECT AVG($year - r.birth_year) as avg_age
                FROM riders r
                WHERE r.id IN (
                    SELECT DISTINCT res.cyclist_id
                    FROM results res
                    JOIN events e ON e.id = res.event_id
                    JOIN series_events se ON se.event_id = e.id
                    JOIN series s ON s.id = se.series_id
                    WHERE YEAR(e.date) = ?
                    AND s.brand_id = ?
                )
                AND r.birth_year IS NOT NULL
                AND r.birth_year > 1900
            ");
            $stmt->execute([$year, $brandId]);
            return round((float)($stmt->fetchColumn() ?: 0), 1);
        }

        // Utan brand: använd aggregerad data
        $stmt = $this->pdo->prepare("
            SELECT AVG($year - r.birth_year) as avg_age
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
        ");
        $stmt->execute([$year]);
        return round((float)($stmt->fetchColumn() ?: 0), 1);
    }

    /**
     * Hamta konsfordelning
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array ['M' => X, 'F' => Y, 'unknown' => Z]
     */
    public function getGenderDistribution(int $year, ?int $brandId = null): array {
        if ($brandId !== null) {
            // Använd faktiskt deltagande i varumärkets events
            $stmt = $this->pdo->prepare("
                SELECT
                    COALESCE(r.gender, 'unknown') as gender,
                    COUNT(DISTINCT r.id) as count
                FROM riders r
                JOIN results res ON res.cyclist_id = r.id
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                JOIN series s ON s.id = se.series_id
                WHERE YEAR(e.date) = ?
                AND s.brand_id = ?
                GROUP BY COALESCE(r.gender, 'unknown')
            ");
            $stmt->execute([$year, $brandId]);
        } else {
            // Utan brand: använd aggregerad data
            $stmt = $this->pdo->prepare("
                SELECT
                    COALESCE(r.gender, 'unknown') as gender,
                    COUNT(*) as count
                FROM rider_yearly_stats rys
                JOIN riders r ON rys.rider_id = r.id
                WHERE rys.season_year = ?
                GROUP BY COALESCE(r.gender, 'unknown')
            ");
            $stmt->execute([$year]);
        }

        $result = ['M' => 0, 'F' => 0, 'unknown' => 0];
        while ($row = $stmt->fetch()) {
            $g = $row['gender'];
            if ($g === 'M' || $g === 'male' || $g === 'man') {
                $result['M'] += $row['count'];
            } elseif ($g === 'F' || $g === 'female' || $g === 'kvinna' || $g === 'woman') {
                $result['F'] += $row['count'];
            } else {
                $result['unknown'] += $row['count'];
            }
        }
        return $result;
    }

    /**
     * Hamta aldersfordelning i grupper
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Aldersgrupper med antal
     */
    public function getAgeDistribution(int $year, ?int $brandId = null): array {
        $ageCase = "
            CASE
                WHEN $year - r.birth_year <= 9 THEN '5-9'
                WHEN $year - r.birth_year BETWEEN 10 AND 12 THEN '10-12'
                WHEN $year - r.birth_year BETWEEN 13 AND 14 THEN '13-14'
                WHEN $year - r.birth_year BETWEEN 15 AND 16 THEN '15-16'
                WHEN $year - r.birth_year BETWEEN 17 AND 18 THEN '17-18'
                WHEN $year - r.birth_year BETWEEN 19 AND 30 THEN '19-30'
                WHEN $year - r.birth_year BETWEEN 31 AND 35 THEN '31-35'
                WHEN $year - r.birth_year BETWEEN 36 AND 45 THEN '36-45'
                WHEN $year - r.birth_year BETWEEN 46 AND 50 THEN '46-50'
                WHEN $year - r.birth_year > 50 THEN '50+'
                ELSE 'Okand'
            END
        ";

        $orderCase = "
            CASE age_group
                WHEN '5-9' THEN 1
                WHEN '10-12' THEN 2
                WHEN '13-14' THEN 3
                WHEN '15-16' THEN 4
                WHEN '17-18' THEN 5
                WHEN '19-30' THEN 6
                WHEN '31-35' THEN 7
                WHEN '36-45' THEN 8
                WHEN '46-50' THEN 9
                WHEN '50+' THEN 10
                ELSE 11
            END
        ";

        if ($brandId !== null) {
            // Använd faktiskt deltagande i varumärkets events
            $stmt = $this->pdo->prepare("
                SELECT
                    $ageCase as age_group,
                    COUNT(DISTINCT r.id) as count
                FROM riders r
                JOIN results res ON res.cyclist_id = r.id
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                JOIN series s ON s.id = se.series_id
                WHERE YEAR(e.date) = ?
                AND s.brand_id = ?
                AND r.birth_year IS NOT NULL
                AND r.birth_year > 1900
                GROUP BY age_group
                ORDER BY $orderCase
            ");
            $stmt->execute([$year, $brandId]);
        } else {
            // Utan brand: använd aggregerad data
            $stmt = $this->pdo->prepare("
                SELECT
                    $ageCase as age_group,
                    COUNT(*) as count
                FROM rider_yearly_stats rys
                JOIN riders r ON rys.rider_id = r.id
                WHERE rys.season_year = ?
                  AND r.birth_year IS NOT NULL
                  AND r.birth_year > 1900
                GROUP BY age_group
                ORDER BY $orderCase
            ");
            $stmt->execute([$year]);
        }
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta disciplinfordelning baserat pa primary_discipline
     * OBS: Detta visar EN disciplin per rider (den de deltagit i mest)
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Discipliner med antal
     */
    public function getDisciplineDistribution(int $year, ?int $brandId = null): array {
        if ($brandId !== null) {
            // Använd faktiskt deltagande - visa disciplin från events
            $stmt = $this->pdo->prepare("
                SELECT
                    COALESCE(e.discipline, 'Okand') as discipline,
                    COUNT(DISTINCT res.cyclist_id) as count
                FROM results res
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                JOIN series s ON s.id = se.series_id
                WHERE YEAR(e.date) = ?
                AND s.brand_id = ?
                GROUP BY e.discipline
                ORDER BY count DESC
            ");
            $stmt->execute([$year, $brandId]);
        } else {
            // Utan brand: använd aggregerad data
            $stmt = $this->pdo->prepare("
                SELECT
                    COALESCE(rys.primary_discipline, 'Okand') as discipline,
                    COUNT(*) as count
                FROM rider_yearly_stats rys
                WHERE rys.season_year = ?
                GROUP BY rys.primary_discipline
                ORDER BY count DESC
            ");
            $stmt->execute([$year]);
        }
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta faktiskt deltagande per disciplin
     * Visar hur manga unika deltagare som deltagit i varje disciplin,
     * baserat pa faktiska resultat (inte primary_discipline).
     * En person kan raknas i flera discipliner om de deltagit i flera.
     */
    public function getDisciplineParticipation(int $year): array {
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(e.discipline, 'Okand') as discipline,
                COUNT(DISTINCT res.cyclist_id) as unique_riders,
                COUNT(*) as total_starts
            FROM results res
            JOIN events e ON res.event_id = e.id
            WHERE YEAR(e.date) = ?
            GROUP BY e.discipline
            ORDER BY unique_riders DESC
        ");
        $stmt->execute([$year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // ROOKIE ANALYSIS
    // =========================================================================

    /**
     * Hamta aldersfordelning for rookies
     *
     * @param int $year Ar
     * @return array Aldersgrupper med antal
     */
    public function getRookieAgeDistribution(int $year, ?int $seriesId = null): array {
        $seriesFilter = $seriesId !== null ? "
            AND rys.rider_id IN (
                SELECT DISTINCT res.cyclist_id
                FROM results res
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                WHERE se.series_id = ?
                AND YEAR(e.date) = ?
            )
        " : "";
        $stmt = $this->pdo->prepare("
            SELECT
                CASE
                    WHEN $year - r.birth_year <= 9 THEN '5-9'
                    WHEN $year - r.birth_year BETWEEN 10 AND 12 THEN '10-12'
                    WHEN $year - r.birth_year BETWEEN 13 AND 14 THEN '13-14'
                    WHEN $year - r.birth_year BETWEEN 15 AND 16 THEN '15-16'
                    WHEN $year - r.birth_year BETWEEN 17 AND 18 THEN '17-18'
                    WHEN $year - r.birth_year BETWEEN 19 AND 30 THEN '19-30'
                    WHEN $year - r.birth_year BETWEEN 31 AND 35 THEN '31-35'
                    WHEN $year - r.birth_year BETWEEN 36 AND 45 THEN '36-45'
                    WHEN $year - r.birth_year BETWEEN 46 AND 50 THEN '46-50'
                    WHEN $year - r.birth_year > 50 THEN '50+'
                    ELSE 'Okand'
                END as age_group,
                COUNT(*) as count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
              $seriesFilter
            GROUP BY age_group
            ORDER BY
                CASE age_group
                    WHEN '5-9' THEN 1
                    WHEN '10-12' THEN 2
                    WHEN '13-14' THEN 3
                    WHEN '15-16' THEN 4
                    WHEN '17-18' THEN 5
                    WHEN '19-30' THEN 6
                    WHEN '31-35' THEN 7
                    WHEN '36-45' THEN 8
                    WHEN '46-50' THEN 9
                    WHEN '50+' THEN 10
                    ELSE 11
                END
        ");
        $params = [$year];
        if ($seriesId !== null) {
            $params[] = $seriesId;
            $params[] = $year;
        }
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta klassfordelning for rookies
     * Vilka klasser startar nya deltagare i?
     *
     * @param int $year Ar
     * @return array Klasser med antal
     */
    public function getRookieClassDistribution(int $year, ?int $seriesId = null): array {
        $seriesFilter = $seriesId !== null ? " AND e.series_id = ?" : "";
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(c.name, 'Okand klass') as class_name,
                COUNT(DISTINCT res.cyclist_id) as rookie_count
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN rider_yearly_stats rys ON res.cyclist_id = rys.rider_id AND rys.season_year = ?
            LEFT JOIN classes c ON res.class_id = c.id
            WHERE YEAR(e.date) = ?
              AND rys.is_rookie = 1
              $seriesFilter
            GROUP BY res.class_id, c.name
            ORDER BY rookie_count DESC
        ");
        $params = [$year, $year];
        if ($seriesId !== null) $params[] = $seriesId;
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta events med flest rookies
     *
     * @param int $year Ar
     * @param int $limit Max antal events
     * @return array Events med rookie-antal
     */
    public function getEventsWithMostRookies(int $year, int $limit = 20, ?int $seriesId = null): array {
        $seriesFilter = $seriesId !== null ? " AND e.series_id = ?" : "";
        $stmt = $this->pdo->prepare("
            SELECT
                e.id as event_id,
                e.name as event_name,
                e.date as event_date,
                s.name as series_name,
                COUNT(DISTINCT res.cyclist_id) as total_participants,
                COUNT(DISTINCT CASE WHEN rys.is_rookie = 1 THEN res.cyclist_id END) as rookie_count,
                ROUND(
                    COUNT(DISTINCT CASE WHEN rys.is_rookie = 1 THEN res.cyclist_id END) * 100.0 /
                    NULLIF(COUNT(DISTINCT res.cyclist_id), 0), 1
                ) as rookie_percentage
            FROM events e
            JOIN results res ON res.event_id = e.id
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN rider_yearly_stats rys ON res.cyclist_id = rys.rider_id AND rys.season_year = ?
            WHERE YEAR(e.date) = ?
            $seriesFilter
            GROUP BY e.id
            HAVING rookie_count > 0
            ORDER BY rookie_count DESC
            LIMIT ?
        ");
        $params = [$year, $year];
        if ($seriesId !== null) $params[] = $seriesId;
        $params[] = $limit;
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta komplett lista over alla rookies
     * Med detaljer for profillankningar
     *
     * @param int $year Ar
     * @param int|null $seriesId Filtrera pa serie (optional)
     * @return array Lista med rookies
     */
    public function getRookiesList(int $year, ?int $seriesId = null): array {
        if ($seriesId !== null) {
            // Med serie-filter: använd faktiskt deltagande via results-tabellen
            $sql = "
                SELECT DISTINCT
                    r.id as rider_id,
                    r.firstname,
                    r.lastname,
                    CASE
                        WHEN r.birth_year IS NOT NULL AND r.birth_year > 1900
                        THEN $year - r.birth_year
                        ELSE NULL
                    END as age,
                    r.birth_year,
                    r.gender,
                    c.id as club_id,
                    c.name as club_name,
                    rys.total_events,
                    rys.total_points,
                    rys.best_position,
                    rys.primary_discipline,
                    rys.primary_series_id,
                    s.name as series_name
                FROM rider_yearly_stats rys
                JOIN riders r ON rys.rider_id = r.id
                LEFT JOIN clubs c ON r.club_id = c.id
                LEFT JOIN series s ON rys.primary_series_id = s.id
                WHERE rys.season_year = ?
                  AND rys.is_rookie = 1
                  AND rys.rider_id IN (
                      -- Riders som faktiskt deltog i denna serie
                      SELECT DISTINCT res.cyclist_id
                      FROM results res
                      JOIN events e ON e.id = res.event_id
                      JOIN series_events se ON se.event_id = e.id
                      WHERE se.series_id = ?
                      AND YEAR(e.date) = ?
                  )
                ORDER BY r.lastname, r.firstname
            ";
            $params = [$year, $seriesId, $year];
        } else {
            // Utan serie-filter: hämta alla rookies
            $sql = "
                SELECT
                    r.id as rider_id,
                    r.firstname,
                    r.lastname,
                    CASE
                        WHEN r.birth_year IS NOT NULL AND r.birth_year > 1900
                        THEN $year - r.birth_year
                        ELSE NULL
                    END as age,
                    r.birth_year,
                    r.gender,
                    c.id as club_id,
                    c.name as club_name,
                    rys.total_events,
                    rys.total_points,
                    rys.best_position,
                    rys.primary_discipline,
                    rys.primary_series_id,
                    s.name as series_name
                FROM rider_yearly_stats rys
                JOIN riders r ON rys.rider_id = r.id
                LEFT JOIN clubs c ON r.club_id = c.id
                LEFT JOIN series s ON rys.primary_series_id = s.id
                WHERE rys.season_year = ?
                  AND rys.is_rookie = 1
                ORDER BY r.lastname, r.firstname
            ";
            $params = [$year];
        }

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hämta rookies för ett varumärke (brand)
     * Räknar alla som är is_rookie=1 OCH deltog i någon serie under varumärket
     */
    public function getRookiesListByBrand(int $year, int $brandId): array {
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT
                r.id as rider_id,
                r.firstname,
                r.lastname,
                CASE
                    WHEN r.birth_year IS NOT NULL AND r.birth_year > 1900
                    THEN ? - r.birth_year
                    ELSE NULL
                END as age,
                r.birth_year,
                r.gender,
                c.id as club_id,
                c.name as club_name,
                rys.total_events,
                rys.total_points,
                rys.best_position,
                rys.primary_discipline,
                rys.primary_series_id,
                ps.name as series_name
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            LEFT JOIN series ps ON rys.primary_series_id = ps.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND rys.rider_id IN (
                  SELECT DISTINCT res.cyclist_id
                  FROM results res
                  JOIN events e ON e.id = res.event_id
                  JOIN series_events se ON se.event_id = e.id
                  JOIN series s ON s.id = se.series_id
                  WHERE s.brand_id = ?
                  AND YEAR(e.date) = ?
              )
            ORDER BY r.lastname, r.firstname
        ");
        $stmt->execute([$year, $year, $brandId, $year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hämta genomsnittsålder för rookies i ett varumärke
     */
    public function getRookieAverageAgeByBrand(int $year, int $brandId): float {
        $stmt = $this->pdo->prepare("
            SELECT AVG(? - r.birth_year) as avg_age
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
              AND rys.rider_id IN (
                  SELECT DISTINCT res.cyclist_id
                  FROM results res
                  JOIN events e ON e.id = res.event_id
                  JOIN series_events se ON se.event_id = e.id
                  JOIN series s ON s.id = se.series_id
                  WHERE s.brand_id = ?
                  AND YEAR(e.date) = ?
              )
        ");
        $stmt->execute([$year, $year, $brandId, $year]);
        return round((float)($stmt->fetchColumn() ?: 0), 1);
    }

    /**
     * Hämta könsfördelning för rookies i ett varumärke
     */
    public function getRookieGenderDistributionByBrand(int $year, int $brandId): array {
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(r.gender, 'unknown') as gender,
                COUNT(*) as count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND rys.rider_id IN (
                  SELECT DISTINCT res.cyclist_id
                  FROM results res
                  JOIN events e ON e.id = res.event_id
                  JOIN series_events se ON se.event_id = e.id
                  JOIN series s ON s.id = se.series_id
                  WHERE s.brand_id = ?
                  AND YEAR(e.date) = ?
              )
            GROUP BY COALESCE(r.gender, 'unknown')
        ");
        $stmt->execute([$year, $brandId, $year]);

        $result = ['M' => 0, 'F' => 0, 'unknown' => 0];
        while ($row = $stmt->fetch()) {
            $g = $row['gender'];
            if ($g === 'M' || $g === 'male' || $g === 'man') {
                $result['M'] += $row['count'];
            } elseif ($g === 'F' || $g === 'female' || $g === 'kvinna' || $g === 'woman') {
                $result['F'] += $row['count'];
            } else {
                $result['unknown'] += $row['count'];
            }
        }
        return $result;
    }

    /**
     * Hämta åldersfördelning för rookies i ett varumärke
     */
    public function getRookieAgeDistributionByBrand(int $year, int $brandId): array {
        $stmt = $this->pdo->prepare("
            SELECT
                CASE
                    WHEN ? - r.birth_year <= 9 THEN '5-9'
                    WHEN ? - r.birth_year BETWEEN 10 AND 12 THEN '10-12'
                    WHEN ? - r.birth_year BETWEEN 13 AND 14 THEN '13-14'
                    WHEN ? - r.birth_year BETWEEN 15 AND 16 THEN '15-16'
                    WHEN ? - r.birth_year BETWEEN 17 AND 18 THEN '17-18'
                    WHEN ? - r.birth_year BETWEEN 19 AND 30 THEN '19-30'
                    WHEN ? - r.birth_year BETWEEN 31 AND 35 THEN '31-35'
                    WHEN ? - r.birth_year BETWEEN 36 AND 45 THEN '36-45'
                    WHEN ? - r.birth_year BETWEEN 46 AND 50 THEN '46-50'
                    WHEN ? - r.birth_year > 50 THEN '50+'
                    ELSE 'Okand'
                END as age_group,
                COUNT(*) as count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
              AND rys.rider_id IN (
                  SELECT DISTINCT res.cyclist_id
                  FROM results res
                  JOIN events e ON e.id = res.event_id
                  JOIN series_events se ON se.event_id = e.id
                  JOIN series s ON s.id = se.series_id
                  WHERE s.brand_id = ?
                  AND YEAR(e.date) = ?
              )
            GROUP BY age_group
            ORDER BY
                CASE age_group
                    WHEN '5-9' THEN 1 WHEN '10-12' THEN 2 WHEN '13-14' THEN 3
                    WHEN '15-16' THEN 4 WHEN '17-18' THEN 5 WHEN '19-30' THEN 6
                    WHEN '31-35' THEN 7 WHEN '36-45' THEN 8 WHEN '46-50' THEN 9
                    WHEN '50+' THEN 10 ELSE 11
                END
        ");
        $stmt->execute([$year, $year, $year, $year, $year, $year, $year, $year, $year, $year, $year, $brandId, $year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hämta klubbar med flest rookies för ett varumärke
     */
    public function getClubsWithMostRookiesByBrand(int $year, int $limit, int $brandId): array {
        $stmt = $this->pdo->prepare("
            SELECT
                c.id as club_id,
                c.name as club_name,
                c.city,
                COUNT(*) as rookie_count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            JOIN clubs c ON r.club_id = c.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND rys.rider_id IN (
                  SELECT DISTINCT res.cyclist_id
                  FROM results res
                  JOIN events e ON e.id = res.event_id
                  JOIN series_events se ON se.event_id = e.id
                  JOIN series s ON s.id = se.series_id
                  WHERE s.brand_id = ?
                  AND YEAR(e.date) = ?
              )
            GROUP BY c.id
            ORDER BY rookie_count DESC
            LIMIT ?
        ");
        $stmt->execute([$year, $brandId, $year, $limit]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta serier som har rookies for ett ar
     *
     * @param int $year Ar
     * @return array Serier med rookie-antal
     */
    public function getSeriesWithRookies(int $year): array {
        $stmt = $this->pdo->prepare("
            SELECT
                s.id,
                s.name,
                COUNT(*) as rookie_count
            FROM rider_yearly_stats rys
            JOIN series s ON rys.primary_series_id = s.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND rys.primary_series_id IS NOT NULL
            GROUP BY s.id, s.name
            ORDER BY rookie_count DESC
        ");
        $stmt->execute([$year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta rookie-deltagande per disciplin (baserat pa faktiska starter)
     * Till skillnad fran primary_discipline som bara visar EN disciplin per rider,
     * visar denna hur manga rookies som faktiskt deltagit i varje disciplin.
     *
     * @param int $year Ar
     * @return array Discipliner med antal rookies och starter
     */
    public function getRookieDisciplineParticipation(int $year, ?int $seriesId = null): array {
        $seriesFilter = $seriesId !== null ? " AND e.series_id = ?" : "";
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(e.discipline, 'Okand') as discipline,
                COUNT(DISTINCT res.cyclist_id) as rookie_count,
                COUNT(*) as total_starts
            FROM results res
            JOIN events e ON res.event_id = e.id
            JOIN rider_yearly_stats rys ON res.cyclist_id = rys.rider_id AND rys.season_year = ?
            WHERE YEAR(e.date) = ?
              AND rys.is_rookie = 1
              $seriesFilter
            GROUP BY e.discipline
            ORDER BY rookie_count DESC
        ");
        $params = [$year, $year];
        if ($seriesId !== null) $params[] = $seriesId;
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta rookie-trend over flera ar
     * Visar antal nya deltagare, totalt deltagare, och andel per ar
     *
     * @param int $years Antal ar att visa
     * @return array Trenddata per ar
     */
    public function getRookieTrend(int $years = 5): array {
        $currentYear = (int)date('Y');
        $startYear = $currentYear - $years + 1;

        $stmt = $this->pdo->prepare("
            SELECT
                rys.season_year as year,
                COUNT(*) as total_riders,
                SUM(CASE WHEN rys.is_rookie = 1 THEN 1 ELSE 0 END) as rookie_count,
                ROUND(
                    SUM(CASE WHEN rys.is_rookie = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0),
                    1
                ) as rookie_percentage
            FROM rider_yearly_stats rys
            WHERE rys.season_year >= ? AND rys.season_year <= ?
            GROUP BY rys.season_year
            ORDER BY rys.season_year ASC
        ");
        $stmt->execute([$startYear, $currentYear]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta genomsnittsalder for rookies per ar (trend)
     *
     * @param int $years Antal ar
     * @return array Snittålder per ar
     */
    public function getRookieAgeTrend(int $years = 5): array {
        $currentYear = (int)date('Y');
        $startYear = $currentYear - $years + 1;

        $stmt = $this->pdo->prepare("
            SELECT
                rys.season_year as year,
                ROUND(AVG(rys.season_year - r.birth_year), 1) as avg_age,
                COUNT(*) as rookie_count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year >= ? AND rys.season_year <= ?
              AND rys.is_rookie = 1
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
            GROUP BY rys.season_year
            ORDER BY rys.season_year ASC
        ");
        $stmt->execute([$startYear, $currentYear]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta genomsnittsalder for rookies
     *
     * @param int $year Ar
     * @return float Genomsnittsalder
     */
    public function getRookieAverageAge(int $year, ?int $seriesId = null): float {
        $seriesFilter = $seriesId !== null ? "
            AND rys.rider_id IN (
                SELECT DISTINCT res.cyclist_id
                FROM results res
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                WHERE se.series_id = ?
                AND YEAR(e.date) = ?
            )
        " : "";
        $stmt = $this->pdo->prepare("
            SELECT AVG($year - r.birth_year) as avg_age
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              AND r.birth_year IS NOT NULL
              AND r.birth_year > 1900
              $seriesFilter
        ");
        $params = [$year];
        if ($seriesId !== null) {
            $params[] = $seriesId;
            $params[] = $year;
        }
        $stmt->execute($params);
        return round((float)($stmt->fetchColumn() ?: 0), 1);
    }

    /**
     * Hamta konsfordelning for rookies
     *
     * @param int $year Ar
     * @return array ['M' => X, 'F' => Y, 'unknown' => Z]
     */
    public function getRookieGenderDistribution(int $year, ?int $seriesId = null): array {
        $seriesFilter = $seriesId !== null ? "
            AND rys.rider_id IN (
                SELECT DISTINCT res.cyclist_id
                FROM results res
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                WHERE se.series_id = ?
                AND YEAR(e.date) = ?
            )
        " : "";
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(r.gender, 'unknown') as gender,
                COUNT(*) as count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              $seriesFilter
            GROUP BY COALESCE(r.gender, 'unknown')
        ");
        $params = [$year];
        if ($seriesId !== null) {
            $params[] = $seriesId;
            $params[] = $year;
        }
        $stmt->execute($params);

        $result = ['M' => 0, 'F' => 0, 'unknown' => 0];
        while ($row = $stmt->fetch()) {
            $g = $row['gender'];
            if ($g === 'M' || $g === 'male' || $g === 'man') {
                $result['M'] += $row['count'];
            } elseif ($g === 'F' || $g === 'female' || $g === 'kvinna' || $g === 'woman') {
                $result['F'] += $row['count'];
            } else {
                $result['unknown'] += $row['count'];
            }
        }
        return $result;
    }

    /**
     * Hamta klubbar med flest rookies
     *
     * @param int $year Ar
     * @param int $limit Max antal
     * @return array Klubbar med rookie-antal
     */
    public function getClubsWithMostRookies(int $year, int $limit = 20, ?int $seriesId = null): array {
        $seriesFilter = $seriesId !== null ? "
            AND rys.rider_id IN (
                SELECT DISTINCT res.cyclist_id
                FROM results res
                JOIN events e ON e.id = res.event_id
                JOIN series_events se ON se.event_id = e.id
                WHERE se.series_id = ?
                AND YEAR(e.date) = ?
            )
        " : "";
        $stmt = $this->pdo->prepare("
            SELECT
                c.id as club_id,
                c.name as club_name,
                c.city,
                COUNT(*) as rookie_count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            JOIN clubs c ON r.club_id = c.id
            WHERE rys.season_year = ?
              AND rys.is_rookie = 1
              $seriesFilter
            GROUP BY c.id
            ORDER BY rookie_count DESC
            LIMIT ?
        ");
        $params = [$year];
        if ($seriesId !== null) {
            $params[] = $seriesId;
            $params[] = $year;
        }
        $params[] = $limit;
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // SERIES FLOW (NYCKELFUNKTIONER)
    // =========================================================================

    /**
     * Berakna feeder conversion rate
     * Hur stor andel av deltagare i en regional serie gar vidare till en nationell?
     *
     * @param int $fromSeriesId Ursprungsserie (t.ex. Capital Enduro)
     * @param int $toSeriesId Malserie (t.ex. ESS)
     * @param int $year Ar
     * @return float Conversion rate i procent
     */
    public function getFeederConversionRate(int $fromSeriesId, int $toSeriesId, int $year): float {
        // Antal i from-serie
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rider_id) FROM series_participation
            WHERE series_id = ? AND season_year = ?
        ");
        $stmt->execute([$fromSeriesId, $year]);
        $fromCount = (int)$stmt->fetchColumn();

        if ($fromCount == 0) return 0;

        // Antal som ocksa deltog i to-serie
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT sp1.rider_id)
            FROM series_participation sp1
            JOIN series_participation sp2
                ON sp1.rider_id = sp2.rider_id
                AND sp2.series_id = ?
                AND sp2.season_year = sp1.season_year
            WHERE sp1.series_id = ?
              AND sp1.season_year = ?
        ");
        $stmt->execute([$toSeriesId, $fromSeriesId, $year]);
        $convertedCount = (int)$stmt->fetchColumn();

        return round($convertedCount / $fromCount * 100, 1);
    }

    /**
     * Berakna cross-participation rate
     * Andel riders som deltar i mer an en serie
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return float Rate i procent
     */
    public function getCrossParticipationRate(int $year, ?int $brandId = null): float {
        // Total aktiva
        $total = $this->getTotalActiveRiders($year, $brandId);
        if ($total == 0) return 0;

        if ($brandId !== null) {
            // Med brand: räkna riders från DETTA varumärke som ÄVEN deltog i ANDRA varumärken
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT this_brand.cyclist_id)
                FROM (
                    -- Riders i det valda varumärket
                    SELECT DISTINCT r.cyclist_id
                    FROM results r
                    JOIN events e ON e.id = r.event_id
                    JOIN series_events se ON se.event_id = e.id
                    JOIN series s ON s.id = se.series_id
                    WHERE YEAR(e.date) = ?
                    AND s.brand_id = ?
                ) this_brand
                WHERE this_brand.cyclist_id IN (
                    -- Riders som också deltog i ett ANNAT varumärke (inkl serier utan brand)
                    SELECT DISTINCT r2.cyclist_id
                    FROM results r2
                    JOIN events e2 ON e2.id = r2.event_id
                    JOIN series_events se2 ON se2.event_id = e2.id
                    JOIN series s2 ON s2.id = se2.series_id
                    WHERE YEAR(e2.date) = ?
                    AND (s2.brand_id IS NULL OR s2.brand_id != ?)
                )
            ");
            $stmt->execute([$year, $brandId, $year, $brandId]);
            $crossCount = (int)$stmt->fetchColumn();
        } else {
            // Utan brand: riders med mer än 1 serie (original logik)
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT rider_id)
                FROM (
                    SELECT sp.rider_id, COUNT(DISTINCT sp.series_id) as series_count
                    FROM series_participation sp
                    WHERE sp.season_year = ?
                    GROUP BY sp.rider_id
                    HAVING series_count > 1
                ) as multi_series
            ");
            $stmt->execute([$year]);
            $crossCount = (int)$stmt->fetchColumn();
        }

        return round($crossCount / $total * 100, 1);
    }

    /**
     * Berakna serielojalitet
     * Andel som aterkom till samma serie fran forra aret
     *
     * @param int $seriesId Serie
     * @param int $year Ar
     * @return float Lojalitet i procent
     */
    public function getSeriesLoyaltyRate(int $seriesId, int $year): float {
        // Deltagare forra aret
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rider_id) FROM series_participation
            WHERE series_id = ? AND season_year = ?
        ");
        $stmt->execute([$seriesId, $year - 1]);
        $prevCount = (int)$stmt->fetchColumn();

        if ($prevCount == 0) return 0;

        // Som ocksa deltog detta ar
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT sp1.rider_id)
            FROM series_participation sp1
            JOIN series_participation sp2
                ON sp1.rider_id = sp2.rider_id
                AND sp2.series_id = sp1.series_id
                AND sp2.season_year = sp1.season_year + 1
            WHERE sp1.series_id = ?
              AND sp1.season_year = ?
        ");
        $stmt->execute([$seriesId, $year - 1]);
        $returnedCount = (int)$stmt->fetchColumn();

        return round($returnedCount / $prevCount * 100, 1);
    }

    /**
     * Berakna exklusivitet for en serie
     * Andel som ENDAST deltar i denna serie (ej andra serier)
     *
     * @param int $seriesId Serie
     * @param int $year Ar
     * @return float Exklusivitet i procent
     */
    public function getExclusivityRate(int $seriesId, int $year): float {
        // Total i serien
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rider_id) FROM series_participation
            WHERE series_id = ? AND season_year = ?
        ");
        $stmt->execute([$seriesId, $year]);
        $totalInSeries = (int)$stmt->fetchColumn();

        if ($totalInSeries == 0) return 0;

        // Endast denna serie
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT sp1.rider_id)
            FROM series_participation sp1
            WHERE sp1.series_id = ?
              AND sp1.season_year = ?
              AND NOT EXISTS (
                  SELECT 1 FROM series_participation sp2
                  WHERE sp2.rider_id = sp1.rider_id
                    AND sp2.season_year = sp1.season_year
                    AND sp2.series_id != sp1.series_id
              )
        ");
        $stmt->execute([$seriesId, $year]);
        $exclusiveCount = (int)$stmt->fetchColumn();

        return round($exclusiveCount / $totalInSeries * 100, 1);
    }

    /**
     * Hamta entry point distribution
     * Vilken serie borjar nya riders i?
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Serie-fordelning for rookies
     */
    public function getEntryPointDistribution(int $year, ?int $brandId = null): array {
        $brandFilter = $brandId !== null ? "AND s.brand_id = ?" : "";

        // Försök först med förberäknad is_entry_series data
        $stmt = $this->pdo->prepare("
            SELECT
                s.id as series_id,
                s.name as series_name,
                COALESCE(s.series_level, 'unknown') as series_level,
                COUNT(DISTINCT sp.rider_id) as rider_count
            FROM series_participation sp
            JOIN series s ON sp.series_id = s.id
            WHERE sp.is_entry_series = 1
              AND sp.season_year = ?
              $brandFilter
            GROUP BY s.id
            ORDER BY rider_count DESC
        ");

        $params = [$year];
        if ($brandId !== null) {
            $params[] = $brandId;
        }

        $stmt->execute($params);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Fallback: om ingen förberäknad data, hitta rookies via rider_yearly_stats
        if (empty($result)) {
            $stmt = $this->pdo->prepare("
                SELECT
                    s.id as series_id,
                    s.name as series_name,
                    COALESCE(s.series_level, 'unknown') as series_level,
                    COUNT(DISTINCT sp.rider_id) as rider_count
                FROM series_participation sp
                JOIN series s ON sp.series_id = s.id
                JOIN rider_yearly_stats rys ON sp.rider_id = rys.rider_id
                    AND rys.season_year = sp.season_year
                WHERE sp.season_year = ?
                  AND rys.is_rookie = 1
                  $brandFilter
                GROUP BY s.id
                ORDER BY rider_count DESC
            ");
            $params = [$year];
            if ($brandId !== null) {
                $params[] = $brandId;
            }
            $stmt->execute($params);
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }

        return $result;
    }

    /**
     * Berakna feeder matrix
     * Visar flodet mellan alla serier
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Matrix med from/to/count
     */
    public function calculateFeederMatrix(int $year, ?int $brandId = null): array {
        $brandFilter = $brandId !== null ? "AND (s_from.brand_id = ? OR s_to.brand_id = ?)" : "";

        // Försök först med förberäknad series_crossover data
        $stmt = $this->pdo->prepare("
            SELECT
                sc.from_series_id,
                s_from.name as from_name,
                COALESCE(s_from.series_level, 'unknown') as from_level,
                sc.to_series_id,
                s_to.name as to_name,
                COALESCE(s_to.series_level, 'unknown') as to_level,
                COUNT(DISTINCT sc.rider_id) as flow_count
            FROM series_crossover sc
            JOIN series s_from ON sc.from_series_id = s_from.id
            JOIN series s_to ON sc.to_series_id = s_to.id
            WHERE sc.from_year = ?
              AND sc.crossover_type = 'same_year'
              $brandFilter
            GROUP BY sc.from_series_id, sc.to_series_id
            ORDER BY flow_count DESC
        ");

        $params = [$year];
        if ($brandId !== null) {
            $params[] = $brandId;
            $params[] = $brandId;  // Used twice in the OR condition
        }

        $stmt->execute($params);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Fallback: om ingen förberäknad data, beräkna direkt från series_participation
        if (empty($result)) {
            $brandFilter2 = $brandId !== null ? "AND (s1.brand_id = ? OR s2.brand_id = ?)" : "";

            $stmt = $this->pdo->prepare("
                SELECT
                    sp1.series_id as from_series_id,
                    s1.name as from_name,
                    COALESCE(s1.series_level, 'unknown') as from_level,
                    sp2.series_id as to_series_id,
                    s2.name as to_name,
                    COALESCE(s2.series_level, 'unknown') as to_level,
                    COUNT(DISTINCT sp1.rider_id) as flow_count
                FROM series_participation sp1
                JOIN series_participation sp2 ON sp1.rider_id = sp2.rider_id
                    AND sp1.season_year = sp2.season_year
                    AND sp1.series_id < sp2.series_id
                JOIN series s1 ON sp1.series_id = s1.id
                JOIN series s2 ON sp2.series_id = s2.id
                WHERE sp1.season_year = ?
                $brandFilter2
                GROUP BY sp1.series_id, sp2.series_id
                HAVING flow_count > 0
                ORDER BY flow_count DESC
                LIMIT 50
            ");

            $params = [$year];
            if ($brandId !== null) {
                $params[] = $brandId;
                $params[] = $brandId;
            }

            $stmt->execute($params);
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }

        return $result;
    }

    /**
     * Hamta overlapp mellan tva serier
     *
     * @param int $series1 Forsta serie
     * @param int $series2 Andra serie
     * @param int $year Ar
     * @return array [both, only_1, only_2, overlap_pct]
     */
    public function getSeriesOverlap(int $series1, int $series2, int $year): array {
        // Deltagare i serie 1
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT rider_id FROM series_participation
            WHERE series_id = ? AND season_year = ?
        ");
        $stmt->execute([$series1, $year]);
        $set1 = $stmt->fetchAll(PDO::FETCH_COLUMN);

        // Deltagare i serie 2
        $stmt->execute([$series2, $year]);
        $set2 = $stmt->fetchAll(PDO::FETCH_COLUMN);

        $both = array_intersect($set1, $set2);
        $only1 = array_diff($set1, $set2);
        $only2 = array_diff($set2, $set1);

        $total = count(array_unique(array_merge($set1, $set2)));

        return [
            'both' => count($both),
            'only_series_1' => count($only1),
            'only_series_2' => count($only2),
            'overlap_percentage' => $total > 0 ? round(count($both) / $total * 100, 1) : 0
        ];
    }

    // =========================================================================
    // CLUB
    // =========================================================================

    /**
     * Hamta top klubbar efter aktiva riders
     *
     * @param int $year Ar
     * @param int $limit Max antal
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Top klubbar
     */
    public function getTopClubs(int $year, int $limit = 10, ?int $brandId = null): array {
        // When filtering by brand, count riders from rider_yearly_stats instead
        if ($brandId !== null) {
            $stmt = $this->pdo->prepare("
                SELECT
                    c.id as club_id,
                    c.name as club_name,
                    c.city,
                    COUNT(DISTINCT rys.rider_id) as active_riders,
                    SUM(rys.total_points) as total_points,
                    SUM(CASE WHEN rys.best_position = 1 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN rys.best_position <= 3 THEN 1 ELSE 0 END) as podiums
                FROM rider_yearly_stats rys
                JOIN riders r ON rys.rider_id = r.id
                JOIN clubs c ON r.club_id = c.id
                JOIN series s ON rys.primary_series_id = s.id
                WHERE rys.season_year = ?
                  AND s.brand_id = ?
                  AND c.id IS NOT NULL
                GROUP BY c.id
                ORDER BY active_riders DESC
                LIMIT ?
            ");
            $stmt->execute([$year, $brandId, $limit]);
        } else {
            $stmt = $this->pdo->prepare("
                SELECT
                    cys.club_id,
                    c.name as club_name,
                    c.city,
                    cys.active_riders,
                    cys.total_points,
                    cys.wins,
                    cys.podiums
                FROM club_yearly_stats cys
                JOIN clubs c ON cys.club_id = c.id
                WHERE cys.season_year = ?
                ORDER BY cys.active_riders DESC
                LIMIT ?
            ");
            $stmt->execute([$year, $limit]);
        }
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta klubbtillvaxt over tid
     *
     * @param int $clubId Klubb
     * @param int $years Antal ar bakot
     * @return array Arlig statistik
     */
    public function getClubGrowth(int $clubId, int $years = 5): array {
        $stmt = $this->pdo->prepare("
            SELECT
                season_year,
                active_riders,
                new_riders,
                retained_riders,
                churned_riders
            FROM club_yearly_stats
            WHERE club_id = ?
            ORDER BY season_year DESC
            LIMIT ?
        ");
        $stmt->execute([$clubId, $years]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // GEOGRAPHIC
    // =========================================================================

    /**
     * Hamta riders per region (baserat pa klubbens SCF-distrikt)
     *
     * @param int $year Ar
     * @return array Regioner med antal
     */
    public function getRidersByRegion(int $year): array {
        // Anvand klubbens SCF-distrikt (fran RF-registrering)
        // Fallback till 'Okand' om inget finns
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(NULLIF(c.scf_district, ''), 'Okand') as region,
                COUNT(DISTINCT rys.rider_id) as rider_count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE rys.season_year = ?
            GROUP BY COALESCE(NULLIF(c.scf_district, ''), 'Okand')
            ORDER BY rider_count DESC
        ");
        $stmt->execute([$year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // TREND-DATA
    // =========================================================================

    /**
     * Hamta tillvaxttrend over tid
     *
     * @param int $years Antal ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Arlig data
     */
    public function getGrowthTrend(int $years = 5, ?int $brandId = null): array {
        if ($brandId !== null) {
            // Hämta tillgängliga år för varumärket först
            $stmt = $this->pdo->prepare("
                SELECT DISTINCT YEAR(e.date) as season_year
                FROM events e
                JOIN series_events se ON se.event_id = e.id
                JOIN series s ON s.id = se.series_id
                WHERE s.brand_id = ?
                ORDER BY season_year DESC
                LIMIT ?
            ");
            $stmt->execute([$brandId, $years]);
            $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);

            // Beräkna metrics för varje år med faktisk deltagande
            $result = [];
            foreach ($availableYears as $year) {
                $total = $this->getTotalActiveRiders($year, $brandId);
                $newRiders = $this->getNewRidersCount($year, $brandId);
                $retained = $this->getRetainedRidersCount($year, $brandId);

                $result[] = [
                    'season_year' => $year,
                    'total_riders' => $total,
                    'new_riders' => $newRiders,
                    'retained_riders' => $retained
                ];
            }
            return array_reverse($result);
        }

        // Utan brand: använd aggregerad data
        $stmt = $this->pdo->prepare("
            SELECT
                rys.season_year,
                COUNT(*) as total_riders,
                SUM(rys.is_rookie) as new_riders,
                SUM(rys.is_retained) as retained_riders
            FROM rider_yearly_stats rys
            GROUP BY rys.season_year
            ORDER BY rys.season_year DESC
            LIMIT ?
        ");
        $stmt->execute([$years]);
        return array_reverse($stmt->fetchAll(PDO::FETCH_ASSOC));
    }

    /**
     * Hamta retention trend over tid
     *
     * @param int $years Antal ar
     * @return array Arlig retention rate
     */
    public function getRetentionTrend(int $years = 5): array {
        $currentYear = (int)date('Y');
        $result = [];

        for ($y = $currentYear - $years + 1; $y <= $currentYear; $y++) {
            $result[] = [
                'year' => $y,
                'retention_rate' => $this->getRetentionRate($y)
            ];
        }

        return $result;
    }

    // =========================================================================
    // SAMMANFATTNING
    // =========================================================================

    /**
     * Hamta alla nyckeltal for ett ar (for dashboard)
     *
     * @param int $year Ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Alla KPIs
     */
    public function getAllKPIs(int $year, ?int $brandId = null): array {
        return [
            'total_riders' => $this->getTotalActiveRiders($year, $brandId),
            'new_riders' => $this->getNewRidersCount($year, $brandId),
            'retained_riders' => $this->getRetainedRidersCount($year, $brandId),
            'retention_rate' => $this->getRetentionRate($year, $brandId),
            'churn_rate' => $this->getChurnRate($year, $brandId),
            'growth_rate' => $this->getGrowthRate($year, $brandId),
            'cross_participation_rate' => $this->getCrossParticipationRate($year, $brandId),
            'average_age' => $this->getAverageAge($year, $brandId),
            'gender_distribution' => $this->getGenderDistribution($year, $brandId)
        ];
    }

    /**
     * Jamfor tva ar
     *
     * @param int $year1 Forsta ar
     * @param int $year2 Andra ar
     * @param int|null $brandId Filtrera pa varumarke
     * @return array Jamforelsedata
     */
    public function compareYears(int $year1, int $year2, ?int $brandId = null): array {
        $kpi1 = $this->getAllKPIs($year1, $brandId);
        $kpi2 = $this->getAllKPIs($year2, $brandId);

        $result = [];
        foreach ($kpi1 as $key => $value1) {
            $value2 = $kpi2[$key] ?? null;

            if (is_numeric($value1) && is_numeric($value2)) {
                $diff = $value2 - $value1;
                $diffPct = $value1 != 0 ? round($diff / $value1 * 100, 1) : 0;
                $result[$key] = [
                    'year1' => $value1,
                    'year2' => $value2,
                    'difference' => $diff,
                    'difference_pct' => $diffPct,
                    'trend' => $diff > 0 ? 'up' : ($diff < 0 ? 'down' : 'stable')
                ];
            } else {
                $result[$key] = [
                    'year1' => $value1,
                    'year2' => $value2
                ];
            }
        }

        return $result;
    }

    // =========================================================================
    // CHURN & RETENTION DEEP ANALYSIS
    // =========================================================================

    /**
     * Hamta deltagare som slutat (churned) - deltog forra aret men inte i ar
     *
     * @param int $year Aktuellt ar
     * @param int $limit Max antal att hamta
     * @return array Lista med churned riders
     */
    public function getChurnedRiders(int $year, int $limit = 500): array {
        $stmt = $this->pdo->prepare("
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                r.birth_year,
                r.gender,
                c.name as club_name,
                prev.total_events as last_year_events,
                prev.total_points as last_year_points,
                prev.primary_discipline as last_discipline,
                :year1 - r.birth_year as age,
                (SELECT MIN(rys2.season_year) FROM rider_yearly_stats rys2 WHERE rys2.rider_id = r.id) as first_season,
                (SELECT MAX(rys2.season_year) FROM rider_yearly_stats rys2 WHERE rys2.rider_id = r.id) as last_season,
                (SELECT COUNT(DISTINCT rys2.season_year) FROM rider_yearly_stats rys2 WHERE rys2.rider_id = r.id) as total_seasons
            FROM rider_yearly_stats prev
            JOIN riders r ON prev.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = :year2
            WHERE prev.season_year = :prevyear
              AND curr.rider_id IS NULL
            ORDER BY prev.total_events DESC, prev.total_points DESC
            LIMIT :limit
        ");
        $stmt->bindValue(':year1', $year, PDO::PARAM_INT);
        $stmt->bindValue(':year2', $year, PDO::PARAM_INT);
        $stmt->bindValue(':prevyear', $year - 1, PDO::PARAM_INT);
        $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta "one-timers" - deltagare som bara startade 1-2 ggr totalt
     *
     * @param int $year Ar att analysera
     * @param int $maxStarts Max antal starter (default 2)
     * @return array Lista med one-time deltagare
     */
    public function getOneTimers(int $year, int $maxStarts = 2): array {
        $stmt = $this->pdo->prepare("
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                r.birth_year,
                r.gender,
                c.name as club_name,
                :year1 - r.birth_year as age,
                total.total_events,
                total.first_season,
                total.last_season,
                total.disciplines
            FROM (
                SELECT
                    rider_id,
                    SUM(total_events) as total_events,
                    MIN(season_year) as first_season,
                    MAX(season_year) as last_season,
                    GROUP_CONCAT(DISTINCT primary_discipline) as disciplines
                FROM rider_yearly_stats
                GROUP BY rider_id
                HAVING SUM(total_events) <= :maxstarts
            ) total
            JOIN riders r ON total.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE total.last_season <= :year2
            ORDER BY total.last_season DESC, total.total_events DESC
        ");
        $stmt->bindValue(':year1', $year, PDO::PARAM_INT);
        $stmt->bindValue(':year2', $year, PDO::PARAM_INT);
        $stmt->bindValue(':maxstarts', $maxStarts, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta comeback-riders - de som aterkom efter uppehall
     *
     * @param int $year Ar att analysera
     * @param int $minGapYears Minsta antal ars uppehall (default 1)
     * @return array Lista med comeback riders
     */
    public function getComebackRiders(int $year, int $minGapYears = 1): array {
        // Positional params - PDO tillater inte ateranvandning av named params
        $stmt = $this->pdo->prepare("
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                r.birth_year,
                r.gender,
                c.name as club_name,
                ? - r.birth_year as age,
                curr.total_events as current_events,
                curr.primary_discipline,
                prev_max.last_active_before as previous_last_season,
                ? - prev_max.last_active_before as years_away,
                (SELECT MIN(season_year) FROM rider_yearly_stats WHERE rider_id = r.id) as first_season_ever
            FROM rider_yearly_stats curr
            JOIN riders r ON curr.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            JOIN (
                SELECT
                    rider_id,
                    MAX(season_year) as last_active_before
                FROM rider_yearly_stats
                WHERE season_year < ?
                GROUP BY rider_id
                HAVING MAX(season_year) < ? - ?
            ) prev_max ON curr.rider_id = prev_max.rider_id
            WHERE curr.season_year = ?
            ORDER BY years_away DESC, curr.total_events DESC
        ");
        $stmt->execute([$year, $year, $year, $year, $minGapYears, $year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta inaktiva riders grupperade efter hur lange de varit borta
     *
     * @param int $year Aktuellt ar
     * @return array Gruppering per antal ar inaktiv
     */
    public function getInactiveByDuration(int $year): array {
        // Positional params - PDO tillater inte ateranvandning av named params
        $stmt = $this->pdo->prepare("
            SELECT
                ? - last_active.last_season as years_inactive,
                COUNT(*) as count,
                AVG(? - r.birth_year) as avg_age
            FROM (
                SELECT
                    rider_id,
                    MAX(season_year) as last_season
                FROM rider_yearly_stats
                WHERE season_year < ?
                GROUP BY rider_id
            ) last_active
            JOIN riders r ON last_active.rider_id = r.id
            LEFT JOIN rider_yearly_stats curr
                ON last_active.rider_id = curr.rider_id
                AND curr.season_year = ?
            WHERE curr.rider_id IS NULL
            GROUP BY years_inactive
            ORDER BY years_inactive ASC
        ");
        $stmt->execute([$year, $year, $year, $year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Analysera churn per segment (alder, disciplin, klubb)
     *
     * @param int $year Ar att analysera
     * @return array Segmenterad churn-data
     */
    public function getChurnBySegment(int $year): array {
        $prevYear = $year - 1;

        // Churn per aldersgrupp - positional params for PDO compatibility
        $ageStmt = $this->pdo->prepare("
            SELECT
                CASE
                    WHEN ? - r.birth_year <= 9 THEN '5-9'
                    WHEN ? - r.birth_year BETWEEN 10 AND 12 THEN '10-12'
                    WHEN ? - r.birth_year BETWEEN 13 AND 14 THEN '13-14'
                    WHEN ? - r.birth_year BETWEEN 15 AND 16 THEN '15-16'
                    WHEN ? - r.birth_year BETWEEN 17 AND 18 THEN '17-18'
                    WHEN ? - r.birth_year BETWEEN 19 AND 30 THEN '19-30'
                    WHEN ? - r.birth_year BETWEEN 31 AND 35 THEN '31-35'
                    WHEN ? - r.birth_year BETWEEN 36 AND 45 THEN '36-45'
                    WHEN ? - r.birth_year BETWEEN 46 AND 50 THEN '46-50'
                    WHEN ? - r.birth_year > 50 THEN '50+'
                    ELSE 'Okand'
                END as age_group,
                COUNT(*) as churned_count,
                (SELECT COUNT(*) FROM rider_yearly_stats rys2
                 JOIN riders r2 ON rys2.rider_id = r2.id
                 WHERE rys2.season_year = ?
                 AND CASE
                    WHEN ? - r2.birth_year <= 9 THEN '5-9'
                    WHEN ? - r2.birth_year BETWEEN 10 AND 12 THEN '10-12'
                    WHEN ? - r2.birth_year BETWEEN 13 AND 14 THEN '13-14'
                    WHEN ? - r2.birth_year BETWEEN 15 AND 16 THEN '15-16'
                    WHEN ? - r2.birth_year BETWEEN 17 AND 18 THEN '17-18'
                    WHEN ? - r2.birth_year BETWEEN 19 AND 30 THEN '19-30'
                    WHEN ? - r2.birth_year BETWEEN 31 AND 35 THEN '31-35'
                    WHEN ? - r2.birth_year BETWEEN 36 AND 45 THEN '36-45'
                    WHEN ? - r2.birth_year BETWEEN 46 AND 50 THEN '46-50'
                    WHEN ? - r2.birth_year > 50 THEN '50+'
                    ELSE 'Okand'
                 END = age_group
                ) as total_in_group
            FROM rider_yearly_stats prev
            JOIN riders r ON prev.rider_id = r.id
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = ?
            WHERE prev.season_year = ?
              AND curr.rider_id IS NULL
            GROUP BY age_group
            ORDER BY churned_count DESC
        ");
        $ageStmt->execute([
            $year, $year, $year, $year, $year, $year, $year, $year, $year, $year,  // outer CASE (10)
            $prevYear,                                                              // subquery year
            $year, $year, $year, $year, $year, $year, $year, $year, $year, $year,  // subquery CASE (10)
            $year,                                                                  // curr.season_year
            $prevYear                                                               // prev.season_year
        ]);
        $byAge = $ageStmt->fetchAll(PDO::FETCH_ASSOC);

        // Berakna churn rate per grupp
        foreach ($byAge as &$row) {
            $row['churn_rate'] = $row['total_in_group'] > 0
                ? round($row['churned_count'] / $row['total_in_group'] * 100, 1)
                : 0;
        }

        // Churn per disciplin
        $discStmt = $this->pdo->prepare("
            SELECT
                COALESCE(prev.primary_discipline, 'Okand') as discipline,
                COUNT(*) as churned_count
            FROM rider_yearly_stats prev
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = ?
            WHERE prev.season_year = ?
              AND curr.rider_id IS NULL
            GROUP BY prev.primary_discipline
            ORDER BY churned_count DESC
        ");
        $discStmt->execute([$year, $prevYear]);
        $byDiscipline = $discStmt->fetchAll(PDO::FETCH_ASSOC);

        // Top 10 klubbar med flest churned
        $clubStmt = $this->pdo->prepare("
            SELECT
                COALESCE(c.name, 'Ingen klubb') as club_name,
                COUNT(*) as churned_count
            FROM rider_yearly_stats prev
            JOIN riders r ON prev.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = ?
            WHERE prev.season_year = ?
              AND curr.rider_id IS NULL
            GROUP BY c.id, c.name
            ORDER BY churned_count DESC
            LIMIT 10
        ");
        $clubStmt->execute([$year, $prevYear]);
        $byClub = $clubStmt->fetchAll(PDO::FETCH_ASSOC);

        return [
            'by_age' => $byAge,
            'by_discipline' => $byDiscipline,
            'by_club' => $byClub
        ];
    }

    /**
     * Hamta sammanfattning av inaktiva/churned for att na ut till
     *
     * @param int $year Aktuellt ar
     * @return array Sammanfattande statistik
     */
    public function getChurnSummary(int $year): array {
        // Antal som slutat (forra aret men inte i ar)
        $churnedStmt = $this->pdo->prepare("
            SELECT COUNT(*)
            FROM rider_yearly_stats prev
            LEFT JOIN rider_yearly_stats curr
                ON prev.rider_id = curr.rider_id
                AND curr.season_year = :year
            WHERE prev.season_year = :prevyear
              AND curr.rider_id IS NULL
        ");
        $churnedStmt->bindValue(':year', $year, PDO::PARAM_INT);
        $churnedStmt->bindValue(':prevyear', $year - 1, PDO::PARAM_INT);
        $churnedStmt->execute();
        $churnedLastYear = (int)$churnedStmt->fetchColumn();

        // One-timers totalt
        $oneTimersStmt = $this->pdo->prepare("
            SELECT COUNT(*)
            FROM (
                SELECT rider_id
                FROM rider_yearly_stats
                GROUP BY rider_id
                HAVING SUM(total_events) <= 2
            ) t
        ");
        $oneTimersStmt->execute();
        $oneTimersTotal = (int)$oneTimersStmt->fetchColumn();

        // Comebacks i ar (positional params - PDO tillater inte ateranvandning av named params)
        $comebacksStmt = $this->pdo->prepare("
            SELECT COUNT(*)
            FROM rider_yearly_stats curr
            JOIN (
                SELECT rider_id, MAX(season_year) as last_active
                FROM rider_yearly_stats
                WHERE season_year < ?
                GROUP BY rider_id
                HAVING MAX(season_year) < ? - 1
            ) prev ON curr.rider_id = prev.rider_id
            WHERE curr.season_year = ?
        ");
        $comebacksStmt->execute([$year, $year, $year]);
        $comebacksThisYear = (int)$comebacksStmt->fetchColumn();

        // Inaktiva 2+ ar (ej i ar, senast aktiva for 2+ ar sedan)
        $longInactiveStmt = $this->pdo->prepare("
            SELECT COUNT(*)
            FROM (
                SELECT rider_id, MAX(season_year) as last_season
                FROM rider_yearly_stats
                GROUP BY rider_id
                HAVING MAX(season_year) < ? - 1
            ) inactive
            LEFT JOIN rider_yearly_stats curr
                ON inactive.rider_id = curr.rider_id
                AND curr.season_year = ?
            WHERE curr.rider_id IS NULL
        ");
        $longInactiveStmt->execute([$year, $year]);
        $longInactive = (int)$longInactiveStmt->fetchColumn();

        return [
            'churned_last_year' => $churnedLastYear,
            'one_timers_total' => $oneTimersTotal,
            'comebacks_this_year' => $comebacksThisYear,
            'inactive_2plus_years' => $longInactive,
            'retention_rate' => $this->getRetentionRate($year),
            'churn_rate' => $this->getChurnRate($year)
        ];
    }

    /**
     * Hamta riders att "vinna tillbaka" - sorterade efter potentiell varde
     *
     * @param int $year Aktuellt ar
     * @param int $limit Max antal
     * @return array Lista med riders att kontakta
     */
    public function getWinBackTargets(int $year, int $limit = 100): array {
        $stmt = $this->pdo->prepare("
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                r.birth_year,
                r.gender,
                c.name as club_name,
                :year1 - r.birth_year as age,
                stats.total_seasons,
                stats.total_events_all_time,
                stats.total_points_all_time,
                stats.last_season,
                :year2 - stats.last_season as years_inactive,
                stats.primary_disciplines,
                CASE
                    WHEN stats.total_seasons >= 3 AND stats.total_events_all_time >= 10 THEN 'Hog'
                    WHEN stats.total_seasons >= 2 OR stats.total_events_all_time >= 5 THEN 'Medium'
                    ELSE 'Lag'
                END as priority
            FROM (
                SELECT
                    rider_id,
                    COUNT(DISTINCT season_year) as total_seasons,
                    SUM(total_events) as total_events_all_time,
                    SUM(total_points) as total_points_all_time,
                    MAX(season_year) as last_season,
                    GROUP_CONCAT(DISTINCT primary_discipline) as primary_disciplines
                FROM rider_yearly_stats
                GROUP BY rider_id
            ) stats
            JOIN riders r ON stats.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            LEFT JOIN rider_yearly_stats curr
                ON stats.rider_id = curr.rider_id
                AND curr.season_year = :year3
            WHERE curr.rider_id IS NULL
              AND stats.last_season >= :year4 - 3
            ORDER BY
                CASE
                    WHEN stats.total_seasons >= 3 AND stats.total_events_all_time >= 10 THEN 1
                    WHEN stats.total_seasons >= 2 OR stats.total_events_all_time >= 5 THEN 2
                    ELSE 3
                END,
                stats.total_events_all_time DESC
            LIMIT :limit
        ");
        $stmt->bindValue(':year1', $year, PDO::PARAM_INT);
        $stmt->bindValue(':year2', $year, PDO::PARAM_INT);
        $stmt->bindValue(':year3', $year, PDO::PARAM_INT);
        $stmt->bindValue(':year4', $year, PDO::PARAM_INT);
        $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // COHORT ANALYSIS (Phase 2)
    // =========================================================================

    /**
     * Hamta cohort retention over tid
     * Foljer en kohort (riders som borjade ar X) och ser hur manga som ar kvar
     *
     * @param int $cohortYear Startaret for kohorten
     * @param int|null $endYear Slutar (default: current year)
     * @return array Retention per ar
     */
    public function getCohortRetention(int $cohortYear, ?int $endYear = null): array {
        $endYear = $endYear ?? (int)date('Y');

        // Hamta alla riders som hade sitt forsta ar = cohortYear
        $stmt = $this->pdo->prepare("
            SELECT rider_id
            FROM rider_yearly_stats
            WHERE rider_id IN (
                SELECT rider_id
                FROM rider_yearly_stats
                GROUP BY rider_id
                HAVING MIN(season_year) = ?
            )
            AND season_year = ?
        ");
        $stmt->execute([$cohortYear, $cohortYear]);
        $cohortRiders = $stmt->fetchAll(PDO::FETCH_COLUMN);

        $cohortSize = count($cohortRiders);
        if ($cohortSize === 0) {
            return [];
        }

        $result = [];

        // For varje ar, rakna hur manga fran kohorten som ar aktiva
        for ($year = $cohortYear; $year <= $endYear; $year++) {
            $yearsFromStart = $year - $cohortYear;

            if (empty($cohortRiders)) {
                $activeCount = 0;
            } else {
                $placeholders = implode(',', array_fill(0, count($cohortRiders), '?'));
                $stmt = $this->pdo->prepare("
                    SELECT COUNT(DISTINCT rider_id)
                    FROM rider_yearly_stats
                    WHERE season_year = ?
                    AND rider_id IN ($placeholders)
                ");
                $stmt->execute(array_merge([$year], $cohortRiders));
                $activeCount = (int)$stmt->fetchColumn();
            }

            $result[] = [
                'year' => $year,
                'years_from_start' => $yearsFromStart,
                'active_count' => $activeCount,
                'cohort_size' => $cohortSize,
                'retention_rate' => round($activeCount / $cohortSize * 100, 1),
            ];
        }

        return $result;
    }

    /**
     * Jamfor flera kohorter
     *
     * @param array $cohortYears Array av ar att jamfora
     * @param int $maxYears Max antal ar att folja varje kohort
     * @return array Jamforelsedata
     */
    public function compareCohorts(array $cohortYears, int $maxYears = 5): array {
        $result = [];

        foreach ($cohortYears as $cohortYear) {
            $endYear = min($cohortYear + $maxYears - 1, (int)date('Y'));
            $retention = $this->getCohortRetention($cohortYear, $endYear);

            if (!empty($retention)) {
                $result[$cohortYear] = [
                    'cohort_year' => $cohortYear,
                    'cohort_size' => $retention[0]['cohort_size'] ?? 0,
                    'retention_data' => $retention,
                ];
            }
        }

        return $result;
    }

    /**
     * Hamta riders i en kohort
     *
     * @param int $cohortYear Kohort-ar
     * @param string $status 'all', 'active', 'churned'
     * @param int|null $asOfYear Ar att kolla status for (default: current)
     * @return array Lista med riders
     */
    public function getCohortRiders(int $cohortYear, string $status = 'all', ?int $asOfYear = null): array {
        $asOfYear = $asOfYear ?? (int)date('Y');

        $sql = "
            SELECT
                r.id as rider_id,
                r.firstname,
                r.lastname,
                r.birth_year,
                r.gender,
                c.name as club_name,
                cohort.first_discipline,
                cohort.total_seasons,
                cohort.last_active_year,
                CASE
                    WHEN cohort.last_active_year >= ? THEN 'active'
                    WHEN ? - cohort.last_active_year = 1 THEN 'soft_churn'
                    WHEN ? - cohort.last_active_year = 2 THEN 'medium_churn'
                    ELSE 'hard_churn'
                END as current_status
            FROM (
                SELECT
                    rider_id,
                    MIN(season_year) as cohort_year,
                    MAX(season_year) as last_active_year,
                    COUNT(DISTINCT season_year) as total_seasons,
                    (SELECT primary_discipline FROM rider_yearly_stats rys2
                     WHERE rys2.rider_id = rys.rider_id
                     ORDER BY season_year ASC LIMIT 1) as first_discipline
                FROM rider_yearly_stats rys
                GROUP BY rider_id
                HAVING cohort_year = ?
            ) cohort
            JOIN riders r ON cohort.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
        ";

        $params = [$asOfYear, $asOfYear, $asOfYear, $cohortYear];

        if ($status === 'active') {
            $sql .= " WHERE cohort.last_active_year >= ?";
            $params[] = $asOfYear;
        } elseif ($status === 'churned') {
            $sql .= " WHERE cohort.last_active_year < ?";
            $params[] = $asOfYear;
        }

        $sql .= " ORDER BY r.lastname, r.firstname";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta kohort-storlek
     *
     * @param int $cohortYear Kohort-ar
     * @return int Antal riders
     */
    public function getCohortSize(int $cohortYear): int {
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT rider_id)
            FROM rider_yearly_stats
            WHERE rider_id IN (
                SELECT rider_id
                FROM rider_yearly_stats
                GROUP BY rider_id
                HAVING MIN(season_year) = ?
            )
            AND season_year = ?
        ");
        $stmt->execute([$cohortYear, $cohortYear]);
        return (int)$stmt->fetchColumn();
    }

    /**
     * Hamta genomsnittlig karriarlangd for en kohort
     *
     * @param int $cohortYear Kohort-ar
     * @return float Genomsnittlig antal sasonger
     */
    public function getCohortAverageLifespan(int $cohortYear): float {
        $stmt = $this->pdo->prepare("
            SELECT AVG(seasons) as avg_lifespan
            FROM (
                SELECT
                    rider_id,
                    COUNT(DISTINCT season_year) as seasons
                FROM rider_yearly_stats
                WHERE rider_id IN (
                    SELECT rider_id
                    FROM rider_yearly_stats
                    GROUP BY rider_id
                    HAVING MIN(season_year) = ?
                )
                GROUP BY rider_id
            ) career_lengths
        ");
        $stmt->execute([$cohortYear]);
        return round((float)($stmt->fetchColumn() ?: 0), 2);
    }

    /**
     * Hamta status-breakdown for en kohort
     *
     * @param int $cohortYear Kohort-ar
     * @param int|null $asOfYear Ar att kolla status for
     * @return array Status-fordelning
     */
    public function getCohortStatusBreakdown(int $cohortYear, ?int $asOfYear = null): array {
        $asOfYear = $asOfYear ?? (int)date('Y');

        $stmt = $this->pdo->prepare("
            SELECT
                CASE
                    WHEN last_year >= ? THEN 'active'
                    WHEN ? - last_year = 1 THEN 'soft_churn'
                    WHEN ? - last_year = 2 THEN 'medium_churn'
                    ELSE 'hard_churn'
                END as status,
                COUNT(*) as count
            FROM (
                SELECT
                    rider_id,
                    MAX(season_year) as last_year
                FROM rider_yearly_stats
                WHERE rider_id IN (
                    SELECT rider_id
                    FROM rider_yearly_stats
                    GROUP BY rider_id
                    HAVING MIN(season_year) = ?
                )
                GROUP BY rider_id
            ) rider_careers
            GROUP BY status
            ORDER BY
                CASE status
                    WHEN 'active' THEN 1
                    WHEN 'soft_churn' THEN 2
                    WHEN 'medium_churn' THEN 3
                    ELSE 4
                END
        ");
        $stmt->execute([$asOfYear, $asOfYear, $asOfYear, $cohortYear]);

        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Ensure all statuses are represented
        $statusMap = [
            'active' => 0,
            'soft_churn' => 0,
            'medium_churn' => 0,
            'hard_churn' => 0,
        ];

        foreach ($results as $row) {
            $statusMap[$row['status']] = (int)$row['count'];
        }

        $total = array_sum($statusMap);

        return [
            'cohort_year' => $cohortYear,
            'as_of_year' => $asOfYear,
            'total' => $total,
            'active' => $statusMap['active'],
            'active_pct' => $total > 0 ? round($statusMap['active'] / $total * 100, 1) : 0,
            'soft_churn' => $statusMap['soft_churn'],
            'soft_churn_pct' => $total > 0 ? round($statusMap['soft_churn'] / $total * 100, 1) : 0,
            'medium_churn' => $statusMap['medium_churn'],
            'medium_churn_pct' => $total > 0 ? round($statusMap['medium_churn'] / $total * 100, 1) : 0,
            'hard_churn' => $statusMap['hard_churn'],
            'hard_churn_pct' => $total > 0 ? round($statusMap['hard_churn'] / $total * 100, 1) : 0,
        ];
    }

    /**
     * Hamta tillgangliga kohort-ar
     *
     * @param int $minSize Minsta kohort-storlek att inkludera
     * @return array Lista med ar och storlekar
     */
    public function getAvailableCohorts(int $minSize = 10): array {
        $stmt = $this->pdo->prepare("
            SELECT
                cohort_year,
                COUNT(*) as cohort_size
            FROM (
                SELECT rider_id, MIN(season_year) as cohort_year
                FROM rider_yearly_stats
                GROUP BY rider_id
            ) cohorts
            GROUP BY cohort_year
            HAVING cohort_size >= ?
            ORDER BY cohort_year DESC
        ");
        $stmt->execute([$minSize]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // BRAND-FILTERED COHORT METHODS
    // =========================================================================

    /**
     * Hamta rider IDs for en kohort filtrerat pa varumarke
     *
     * Returnerar riders vars FORSTA serie-deltagande var i en serie
     * som tillhor det angivna varumarket.
     *
     * @param int $cohortYear Kohort-ar (forsta aktiva ar)
     * @param int|null $brandId Varumarkes-ID (null = alla)
     * @return array Lista med rider_ids
     */
    private function getCohortRiderIdsByBrand(int $cohortYear, ?int $brandId = null): array {
        if ($brandId === null) {
            // Ingen brand-filtrering - anvand standard-logik
            $stmt = $this->pdo->prepare("
                SELECT rider_id
                FROM rider_yearly_stats
                GROUP BY rider_id
                HAVING MIN(season_year) = ?
            ");
            $stmt->execute([$cohortYear]);
        } else {
            // Filtrera pa riders vars forsta serie-deltagande var i valt varumarke
            $stmt = $this->pdo->prepare("
                SELECT DISTINCT sp.rider_id
                FROM series_participation sp
                JOIN series s ON sp.series_id = s.id
                WHERE s.brand_id = ?
                AND sp.season_year = ?
                AND sp.rider_id IN (
                    -- Endast riders vars forsta ar overhuvudtaget var detta ar
                    SELECT rider_id
                    FROM rider_yearly_stats
                    GROUP BY rider_id
                    HAVING MIN(season_year) = ?
                )
                AND sp.rider_id IN (
                    -- Och vars forsta serie i detta varumarke var detta ar
                    SELECT sp2.rider_id
                    FROM series_participation sp2
                    JOIN series s2 ON sp2.series_id = s2.id
                    WHERE s2.brand_id = ?
                    GROUP BY sp2.rider_id
                    HAVING MIN(sp2.season_year) = ?
                )
            ");
            $stmt->execute([$brandId, $cohortYear, $cohortYear, $brandId, $cohortYear]);
        }
        return $stmt->fetchAll(PDO::FETCH_COLUMN);
    }

    /**
     * Hamta tillgangliga kohort-ar for ett specifikt varumarke
     *
     * @param int|null $brandId Varumarkes-ID (null = alla)
     * @param int $minSize Minsta kohort-storlek att inkludera
     * @return array Lista med ar och storlekar
     */
    public function getAvailableCohortsByBrand(?int $brandId = null, int $minSize = 10): array {
        if ($brandId === null) {
            return $this->getAvailableCohorts($minSize);
        }

        $stmt = $this->pdo->prepare("
            SELECT
                cohort_year,
                COUNT(*) as cohort_size
            FROM (
                SELECT sp.rider_id, MIN(sp.season_year) as cohort_year
                FROM series_participation sp
                JOIN series s ON sp.series_id = s.id
                WHERE s.brand_id = ?
                AND sp.rider_id IN (
                    SELECT rider_id
                    FROM rider_yearly_stats
                    GROUP BY rider_id
                    HAVING MIN(season_year) = (
                        SELECT MIN(sp2.season_year)
                        FROM series_participation sp2
                        JOIN series s2 ON sp2.series_id = s2.id
                        WHERE sp2.rider_id = sp.rider_id
                        AND s2.brand_id = ?
                    )
                )
                GROUP BY sp.rider_id
            ) cohorts
            GROUP BY cohort_year
            HAVING cohort_size >= ?
            ORDER BY cohort_year DESC
        ");
        $stmt->execute([$brandId, $brandId, $minSize]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta kohort-retention filtrerat pa varumarke
     *
     * @param int $cohortYear Kohort-ar
     * @param int|null $brandId Varumarkes-ID (null = alla)
     * @param int|null $endYear Slutar
     * @return array Retention per ar
     */
    public function getCohortRetentionByBrand(int $cohortYear, ?int $brandId = null, ?int $endYear = null): array {
        if ($brandId === null) {
            return $this->getCohortRetention($cohortYear, $endYear);
        }

        $endYear = $endYear ?? (int)date('Y');
        $cohortRiders = $this->getCohortRiderIdsByBrand($cohortYear, $brandId);
        $cohortSize = count($cohortRiders);

        if ($cohortSize === 0) {
            return [];
        }

        $result = [];

        for ($year = $cohortYear; $year <= $endYear; $year++) {
            $yearsFromStart = $year - $cohortYear;

            $placeholders = implode(',', array_fill(0, count($cohortRiders), '?'));
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT rider_id)
                FROM rider_yearly_stats
                WHERE season_year = ?
                AND rider_id IN ($placeholders)
            ");
            $stmt->execute(array_merge([$year], $cohortRiders));
            $activeCount = (int)$stmt->fetchColumn();

            $result[] = [
                'year' => $year,
                'years_from_start' => $yearsFromStart,
                'active_count' => $activeCount,
                'cohort_size' => $cohortSize,
                'retention_rate' => round($activeCount / $cohortSize * 100, 1),
            ];
        }

        return $result;
    }

    /**
     * Hamta kohort status-breakdown filtrerat pa varumarke
     *
     * @param int $cohortYear Kohort-ar
     * @param int|null $brandId Varumarkes-ID (null = alla)
     * @param int|null $asOfYear Ar att kolla status for
     * @return array Status-fordelning
     */
    public function getCohortStatusBreakdownByBrand(int $cohortYear, ?int $brandId = null, ?int $asOfYear = null): array {
        if ($brandId === null) {
            return $this->getCohortStatusBreakdown($cohortYear, $asOfYear);
        }

        $asOfYear = $asOfYear ?? (int)date('Y');
        $cohortRiders = $this->getCohortRiderIdsByBrand($cohortYear, $brandId);

        if (empty($cohortRiders)) {
            return [
                'cohort_year' => $cohortYear,
                'as_of_year' => $asOfYear,
                'total' => 0,
                'active' => 0, 'active_pct' => 0,
                'soft_churn' => 0, 'soft_churn_pct' => 0,
                'medium_churn' => 0, 'medium_churn_pct' => 0,
                'hard_churn' => 0, 'hard_churn_pct' => 0,
            ];
        }

        $placeholders = implode(',', array_fill(0, count($cohortRiders), '?'));
        $stmt = $this->pdo->prepare("
            SELECT
                CASE
                    WHEN last_year >= ? THEN 'active'
                    WHEN ? - last_year = 1 THEN 'soft_churn'
                    WHEN ? - last_year = 2 THEN 'medium_churn'
                    ELSE 'hard_churn'
                END as status,
                COUNT(*) as count
            FROM (
                SELECT rider_id, MAX(season_year) as last_year
                FROM rider_yearly_stats
                WHERE rider_id IN ($placeholders)
                GROUP BY rider_id
            ) rider_careers
            GROUP BY status
        ");
        $stmt->execute(array_merge([$asOfYear, $asOfYear, $asOfYear], $cohortRiders));

        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $statusMap = [
            'active' => 0,
            'soft_churn' => 0,
            'medium_churn' => 0,
            'hard_churn' => 0,
        ];

        foreach ($results as $row) {
            $statusMap[$row['status']] = (int)$row['count'];
        }

        $total = array_sum($statusMap);

        return [
            'cohort_year' => $cohortYear,
            'as_of_year' => $asOfYear,
            'total' => $total,
            'active' => $statusMap['active'],
            'active_pct' => $total > 0 ? round($statusMap['active'] / $total * 100, 1) : 0,
            'soft_churn' => $statusMap['soft_churn'],
            'soft_churn_pct' => $total > 0 ? round($statusMap['soft_churn'] / $total * 100, 1) : 0,
            'medium_churn' => $statusMap['medium_churn'],
            'medium_churn_pct' => $total > 0 ? round($statusMap['medium_churn'] / $total * 100, 1) : 0,
            'hard_churn' => $statusMap['hard_churn'],
            'hard_churn_pct' => $total > 0 ? round($statusMap['hard_churn'] / $total * 100, 1) : 0,
        ];
    }

    /**
     * Hamta kohort-riders filtrerat pa varumarke
     *
     * @param int $cohortYear Kohort-ar
     * @param int|null $brandId Varumarkes-ID (null = alla)
     * @param string $status 'all', 'active', 'churned'
     * @param int|null $asOfYear Ar att kolla status for
     * @return array Lista med riders
     */
    public function getCohortRidersByBrand(int $cohortYear, ?int $brandId = null, string $status = 'all', ?int $asOfYear = null): array {
        if ($brandId === null) {
            return $this->getCohortRiders($cohortYear, $status, $asOfYear);
        }

        $asOfYear = $asOfYear ?? (int)date('Y');
        $cohortRiderIds = $this->getCohortRiderIdsByBrand($cohortYear, $brandId);

        if (empty($cohortRiderIds)) {
            return [];
        }

        $placeholders = implode(',', array_fill(0, count($cohortRiderIds), '?'));

        $sql = "
            SELECT
                r.id as rider_id,
                r.firstname,
                r.lastname,
                r.birth_year,
                r.gender,
                c.name as club_name,
                cohort.first_discipline,
                cohort.total_seasons,
                cohort.last_active_year,
                CASE
                    WHEN cohort.last_active_year >= ? THEN 'active'
                    WHEN ? - cohort.last_active_year = 1 THEN 'soft_churn'
                    WHEN ? - cohort.last_active_year = 2 THEN 'medium_churn'
                    ELSE 'hard_churn'
                END as current_status
            FROM (
                SELECT
                    rider_id,
                    MAX(season_year) as last_active_year,
                    COUNT(DISTINCT season_year) as total_seasons,
                    (SELECT primary_discipline FROM rider_yearly_stats rys2
                     WHERE rys2.rider_id = rys.rider_id
                     ORDER BY season_year ASC LIMIT 1) as first_discipline
                FROM rider_yearly_stats rys
                WHERE rider_id IN ($placeholders)
                GROUP BY rider_id
            ) cohort
            JOIN riders r ON cohort.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
        ";

        $params = array_merge([$asOfYear, $asOfYear, $asOfYear], $cohortRiderIds);

        if ($status === 'active') {
            $sql .= " WHERE cohort.last_active_year >= ?";
            $params[] = $asOfYear;
        } elseif ($status === 'churned') {
            $sql .= " WHERE cohort.last_active_year < ?";
            $params[] = $asOfYear;
        }

        $sql .= " ORDER BY r.lastname, r.firstname";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta genomsnittlig livslangd for en kohort filtrerat pa varumarke
     *
     * @param int $cohortYear Kohort-ar
     * @param int|null $brandId Varumarkes-ID (null = alla)
     * @return float Genomsnittligt antal sasonger
     */
    public function getCohortAverageLifespanByBrand(int $cohortYear, ?int $brandId = null): float {
        if ($brandId === null) {
            return $this->getCohortAverageLifespan($cohortYear);
        }

        $cohortRiders = $this->getCohortRiderIdsByBrand($cohortYear, $brandId);

        if (empty($cohortRiders)) {
            return 0;
        }

        $placeholders = implode(',', array_fill(0, count($cohortRiders), '?'));
        $stmt = $this->pdo->prepare("
            SELECT AVG(seasons) as avg_lifespan
            FROM (
                SELECT rider_id, COUNT(DISTINCT season_year) as seasons
                FROM rider_yearly_stats
                WHERE rider_id IN ($placeholders)
                GROUP BY rider_id
            ) career_lengths
        ");
        $stmt->execute($cohortRiders);
        return round((float)($stmt->fetchColumn() ?: 0), 2);
    }

    /**
     * Hamta alla varumarken
     *
     * @return array Lista med varumarken
     */
    public function getAllBrands(): array {
        $stmt = $this->pdo->query("
            SELECT id, name, accent_color, active
            FROM series_brands
            ORDER BY display_order ASC, name ASC
        ");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // RIDER JOURNEY (Phase 2)
    // =========================================================================

    /**
     * Hamta en riders kompletta resa/historik
     *
     * @param int $riderId Rider ID
     * @return array Journey-data
     */
    public function getRiderJourney(int $riderId): array {
        // Hamta arlig statistik
        $stmt = $this->pdo->prepare("
            SELECT
                rys.season_year as year,
                rys.total_events,
                rys.total_series,
                rys.total_points,
                rys.best_position,
                rys.avg_position,
                rys.primary_discipline,
                rys.primary_series_id,
                s.name as primary_series_name,
                rys.is_rookie
            FROM rider_yearly_stats rys
            LEFT JOIN series s ON rys.primary_series_id = s.id
            WHERE rys.rider_id = ?
            ORDER BY rys.season_year ASC
        ");
        $stmt->execute([$riderId]);
        $yearlyStats = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($yearlyStats)) {
            return [];
        }

        // Hamta serier per ar
        $stmt = $this->pdo->prepare("
            SELECT
                sp.season_year as year,
                sp.series_id,
                s.name as series_name,
                sp.events_attended,
                sp.total_points
            FROM series_participation sp
            JOIN series s ON sp.series_id = s.id
            WHERE sp.rider_id = ?
            ORDER BY sp.season_year ASC, sp.events_attended DESC
        ");
        $stmt->execute([$riderId]);
        $seriesData = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Gruppera serier per ar
        $seriesByYear = [];
        foreach ($seriesData as $row) {
            $seriesByYear[$row['year']][] = [
                'series_id' => $row['series_id'],
                'series_name' => $row['series_name'],
                'events' => $row['events_attended'],
                'points' => $row['total_points'],
            ];
        }

        // Bygg journey
        $journey = [];
        $prevDiscipline = null;
        $prevSeriesIds = [];

        foreach ($yearlyStats as $stat) {
            $year = $stat['year'];
            $currentSeriesIds = array_column($seriesByYear[$year] ?? [], 'series_id');

            // Detektera andringar
            $changedDiscipline = $prevDiscipline !== null && $prevDiscipline !== $stat['primary_discipline'];
            $changedSeries = !empty($prevSeriesIds) &&
                             count(array_diff($currentSeriesIds, $prevSeriesIds)) > 0;

            $journey[] = [
                'year' => $year,
                'is_rookie' => (bool)$stat['is_rookie'],
                'total_events' => $stat['total_events'],
                'total_series' => $stat['total_series'],
                'total_points' => $stat['total_points'],
                'best_position' => $stat['best_position'],
                'avg_position' => $stat['avg_position'],
                'primary_discipline' => $stat['primary_discipline'],
                'primary_series' => $stat['primary_series_name'],
                'series' => $seriesByYear[$year] ?? [],
                'changed_discipline' => $changedDiscipline,
                'changed_series' => $changedSeries,
            ];

            $prevDiscipline = $stat['primary_discipline'];
            $prevSeriesIds = $currentSeriesIds;
        }

        return $journey;
    }

    /**
     * Hamta riders progression (hur de utvecklats over tid)
     *
     * @param int $riderId Rider ID
     * @return array Progression-data
     */
    public function getRiderProgression(int $riderId): array {
        $journey = $this->getRiderJourney($riderId);

        if (count($journey) < 2) {
            return [
                'has_progression' => false,
                'years_active' => count($journey),
            ];
        }

        $first = $journey[0];
        $last = $journey[count($journey) - 1];

        // Berakna progression
        $eventsChange = $last['total_events'] - $first['total_events'];
        $pointsChange = $last['total_points'] - $first['total_points'];
        $positionChange = null;

        if ($first['best_position'] && $last['best_position']) {
            $positionChange = $first['best_position'] - $last['best_position']; // Positiv = forbattring
        }

        // Hitta basta sasong
        $bestYear = null;
        $bestPoints = 0;
        foreach ($journey as $year) {
            if ($year['total_points'] > $bestPoints) {
                $bestPoints = $year['total_points'];
                $bestYear = $year['year'];
            }
        }

        return [
            'has_progression' => true,
            'first_year' => $first['year'],
            'last_year' => $last['year'],
            'years_active' => count($journey),
            'total_seasons' => count($journey),
            'first_discipline' => $first['primary_discipline'],
            'current_discipline' => $last['primary_discipline'],
            'discipline_changed' => $first['primary_discipline'] !== $last['primary_discipline'],
            'events_first_year' => $first['total_events'],
            'events_last_year' => $last['total_events'],
            'events_change' => $eventsChange,
            'points_change' => $pointsChange,
            'position_improvement' => $positionChange,
            'best_season_year' => $bestYear,
            'best_season_points' => $bestPoints,
        ];
    }

    /**
     * Hamta liknande riders baserat pa karriarmonster
     *
     * @param int $riderId Rider att hitta liknande for
     * @param int $limit Max antal att returnera
     * @return array Lista med liknande riders
     */
    public function getSimilarRiders(int $riderId, int $limit = 10): array {
        // Hamta basinformation om target rider
        $stmt = $this->pdo->prepare("
            SELECT
                MIN(season_year) as start_year,
                COUNT(DISTINCT season_year) as total_seasons,
                SUM(total_events) as total_events,
                (SELECT primary_discipline FROM rider_yearly_stats
                 WHERE rider_id = ? ORDER BY season_year DESC LIMIT 1) as current_discipline
            FROM rider_yearly_stats
            WHERE rider_id = ?
        ");
        $stmt->execute([$riderId, $riderId]);
        $target = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$target || !$target['start_year']) {
            return [];
        }

        // Hamta serier for target
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT series_id FROM series_participation WHERE rider_id = ?
        ");
        $stmt->execute([$riderId]);
        $targetSeries = $stmt->fetchAll(PDO::FETCH_COLUMN);

        // Definiera buckets
        $tenureBucket = $target['total_seasons'] <= 2 ? 'new' :
                       ($target['total_seasons'] <= 5 ? 'established' : 'veteran');
        $eventBucket = $target['total_events'] <= 10 ? 'casual' :
                      ($target['total_events'] <= 30 ? 'regular' : 'active');

        // Hitta liknande riders
        $stmt = $this->pdo->prepare("
            SELECT
                r.id as rider_id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                stats.start_year,
                stats.total_seasons,
                stats.total_events,
                stats.current_discipline,
                0 as similarity_score
            FROM (
                SELECT
                    rider_id,
                    MIN(season_year) as start_year,
                    COUNT(DISTINCT season_year) as total_seasons,
                    SUM(total_events) as total_events,
                    (SELECT primary_discipline FROM rider_yearly_stats rys2
                     WHERE rys2.rider_id = rys.rider_id
                     ORDER BY season_year DESC LIMIT 1) as current_discipline
                FROM rider_yearly_stats rys
                WHERE rider_id != ?
                GROUP BY rider_id
            ) stats
            JOIN riders r ON stats.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE
                ABS(stats.start_year - ?) <= 2
                OR stats.current_discipline = ?
                OR (stats.total_seasons BETWEEN ? AND ?)
            ORDER BY
                CASE WHEN stats.current_discipline = ? THEN 0 ELSE 1 END,
                ABS(stats.start_year - ?),
                ABS(stats.total_seasons - ?)
            LIMIT ?
        ");

        $tenureMin = max(1, $target['total_seasons'] - 2);
        $tenureMax = $target['total_seasons'] + 2;

        $stmt->execute([
            $riderId,
            $target['start_year'],
            $target['current_discipline'],
            $tenureMin,
            $tenureMax,
            $target['current_discipline'],
            $target['start_year'],
            $target['total_seasons'],
            $limit * 2 // Fetch more to filter
        ]);

        $candidates = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Score candidates
        foreach ($candidates as &$candidate) {
            $score = 0;

            // Start year similarity (max 20)
            $yearDiff = abs($candidate['start_year'] - $target['start_year']);
            $score += max(0, 20 - $yearDiff * 5);

            // Discipline match (25)
            if ($candidate['current_discipline'] === $target['current_discipline']) {
                $score += 25;
            }

            // Tenure bucket (20)
            $candTenure = $candidate['total_seasons'] <= 2 ? 'new' :
                         ($candidate['total_seasons'] <= 5 ? 'established' : 'veteran');
            if ($candTenure === $tenureBucket) {
                $score += 20;
            }

            // Event bucket (15)
            $candEvents = $candidate['total_events'] <= 10 ? 'casual' :
                         ($candidate['total_events'] <= 30 ? 'regular' : 'active');
            if ($candEvents === $eventBucket) {
                $score += 15;
            }

            $candidate['similarity_score'] = $score;
        }

        // Sort by score and limit
        usort($candidates, fn($a, $b) => $b['similarity_score'] - $a['similarity_score']);

        return array_slice($candidates, 0, $limit);
    }

    /**
     * Hamta senaste aktiva ar for en rider
     *
     * @param int $riderId Rider ID
     * @return int|null Senaste ar eller null
     */
    public function getRiderLastActiveYear(int $riderId): ?int {
        $stmt = $this->pdo->prepare("
            SELECT MAX(season_year) FROM rider_yearly_stats WHERE rider_id = ?
        ");
        $stmt->execute([$riderId]);
        $result = $stmt->fetchColumn();
        return $result ? (int)$result : null;
    }

    // =========================================================================
    // AT-RISK / CHURN PREDICTION (Phase 2)
    // =========================================================================

    /**
     * Hamta at-risk riders for ett ar
     *
     * @param int $year Ar
     * @param int $limit Max antal
     * @return array Lista med at-risk riders
     */
    public function getAtRiskRiders(int $year, int $limit = 100): array {
        // Forst, kolla om vi har cachad data
        $stmt = $this->pdo->prepare("
            SELECT
                rrs.rider_id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                rrs.risk_score,
                rrs.risk_level,
                rrs.factors,
                rrs.declining_events,
                rrs.no_recent_activity,
                rrs.class_downgrade,
                rrs.single_series,
                rrs.low_tenure,
                rrs.high_age_in_class,
                rys.total_events,
                rys.primary_discipline,
                rys.primary_series_id,
                s.name as series_name
            FROM rider_risk_scores rrs
            JOIN riders r ON rrs.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            LEFT JOIN rider_yearly_stats rys ON rrs.rider_id = rys.rider_id AND rys.season_year = ?
            LEFT JOIN series s ON rys.primary_series_id = s.id
            WHERE rrs.season_year = ?
            ORDER BY rrs.risk_score DESC
            LIMIT ?
        ");

        try {
            $stmt->execute([$year, $year, $limit]);
            $cached = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if (!empty($cached)) {
                // Decode JSON factors
                foreach ($cached as &$row) {
                    $row['factors'] = $row['factors'] ? json_decode($row['factors'], true) : [];
                }
                return $cached;
            }
        } catch (PDOException $e) {
            // Table might not exist yet
        }

        // Fallback: berakna on-the-fly (langsammare)
        return $this->calculateAtRiskRidersOnTheFly($year, $limit);
    }

    /**
     * Berakna risk on-the-fly (fallback om cache saknas)
     */
    private function calculateAtRiskRidersOnTheFly(int $year, int $limit): array {
        // Hamta riders som var aktiva forra aret
        $stmt = $this->pdo->prepare("
            SELECT
                rys.rider_id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                rys.total_events as current_events,
                prev.total_events as prev_events,
                rys.primary_discipline,
                rys.primary_series_id,
                s.name as series_name,
                (SELECT COUNT(DISTINCT season_year) FROM rider_yearly_stats WHERE rider_id = rys.rider_id) as total_seasons,
                (SELECT COUNT(DISTINCT series_id) FROM series_participation WHERE rider_id = rys.rider_id AND season_year = ?) as series_count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            LEFT JOIN rider_yearly_stats prev ON rys.rider_id = prev.rider_id AND prev.season_year = ? - 1
            LEFT JOIN series s ON rys.primary_series_id = s.id
            WHERE rys.season_year = ?
            ORDER BY rys.total_events ASC
            LIMIT ?
        ");
        $stmt->execute([$year, $year, $year, $limit * 2]);
        $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $results = [];
        foreach ($riders as $rider) {
            $risk = $this->calculateChurnRisk($rider['rider_id'], $year);
            if ($risk['risk_score'] >= 30) { // Only include medium+ risk
                $results[] = array_merge($rider, $risk);
            }
        }

        usort($results, fn($a, $b) => $b['risk_score'] - $a['risk_score']);
        return array_slice($results, 0, $limit);
    }

    /**
     * Berakna churn-risk for en specifik rider
     *
     * @param int $riderId Rider ID
     * @param int $year Ar
     * @return array Risk-data
     */
    public function calculateChurnRisk(int $riderId, int $year): array {
        $factors = [];
        $totalScore = 0;

        // Hamta rider-data
        $stmt = $this->pdo->prepare("
            SELECT
                rys.total_events,
                rys.primary_discipline,
                (SELECT total_events FROM rider_yearly_stats WHERE rider_id = ? AND season_year = ? - 1) as prev_events,
                (SELECT COUNT(DISTINCT season_year) FROM rider_yearly_stats WHERE rider_id = ?) as total_seasons,
                (SELECT COUNT(DISTINCT series_id) FROM series_participation WHERE rider_id = ? AND season_year = ?) as series_count
            FROM rider_yearly_stats rys
            WHERE rys.rider_id = ? AND rys.season_year = ?
        ");
        $stmt->execute([$riderId, $year, $riderId, $riderId, $year, $riderId, $year]);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$data) {
            return ['risk_score' => 0, 'risk_level' => 'unknown', 'factors' => []];
        }

        // Factor 1: Declining events (30 points)
        $decliningEvents = false;
        if ($data['prev_events'] && $data['total_events'] < $data['prev_events']) {
            $decline = ($data['prev_events'] - $data['total_events']) / $data['prev_events'];
            if ($decline >= 0.3) {
                $decliningEvents = true;
                $score = min(30, round($decline * 30));
                $totalScore += $score;
                $factors['declining_events'] = [
                    'score' => $score,
                    'detail' => "Minskade fran {$data['prev_events']} till {$data['total_events']} events",
                ];
            }
        }

        // Factor 2: Single series (10 points)
        $singleSeries = $data['series_count'] <= 1;
        if ($singleSeries) {
            $totalScore += 10;
            $factors['single_series'] = [
                'score' => 10,
                'detail' => 'Deltar endast i en serie',
            ];
        }

        // Factor 3: Low tenure (10 points)
        $lowTenure = $data['total_seasons'] <= 2;
        if ($lowTenure) {
            $totalScore += 10;
            $factors['low_tenure'] = [
                'score' => 10,
                'detail' => "Endast {$data['total_seasons']} sasonger",
            ];
        }

        // Determine risk level
        $riskLevel = 'low';
        if ($totalScore >= 70) {
            $riskLevel = 'critical';
        } elseif ($totalScore >= 50) {
            $riskLevel = 'high';
        } elseif ($totalScore >= 30) {
            $riskLevel = 'medium';
        }

        return [
            'risk_score' => $totalScore,
            'risk_level' => $riskLevel,
            'factors' => $factors,
            'declining_events' => $decliningEvents,
            'single_series' => $singleSeries,
            'low_tenure' => $lowTenure,
            'no_recent_activity' => false,
            'class_downgrade' => false,
            'high_age_in_class' => false,
        ];
    }

    /**
     * Hamta risk-distribution for ett ar
     *
     * @param int $year Ar
     * @return array Distribution per risk-niva
     */
    public function getRiskDistribution(int $year): array {
        // Forst kolla cache
        $stmt = $this->pdo->prepare("
            SELECT
                risk_level,
                COUNT(*) as count
            FROM rider_risk_scores
            WHERE season_year = ?
            GROUP BY risk_level
        ");

        try {
            $stmt->execute([$year]);
            $results = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);

            if (!empty($results)) {
                return [
                    'low' => $results['low'] ?? 0,
                    'medium' => $results['medium'] ?? 0,
                    'high' => $results['high'] ?? 0,
                    'critical' => $results['critical'] ?? 0,
                    'total' => array_sum($results),
                ];
            }
        } catch (PDOException $e) {
            // Table might not exist
        }

        // Return empty if no cache
        return [
            'low' => 0,
            'medium' => 0,
            'high' => 0,
            'critical' => 0,
            'total' => 0,
            'cache_missing' => true,
        ];
    }

    // =========================================================================
    // FEEDER TRENDS (Phase 2)
    // =========================================================================

    /**
     * Hamta feeder-trend over tid for ett specifikt flode
     *
     * @param int $fromSeriesId Ursprungsserie
     * @param int $toSeriesId Malserie
     * @param int $years Antal ar
     * @return array Trend-data
     */
    public function getFeederTrend(int $fromSeriesId, int $toSeriesId, int $years = 5): array {
        $currentYear = (int)date('Y');
        $startYear = $currentYear - $years + 1;

        $result = [];

        for ($year = $startYear; $year <= $currentYear; $year++) {
            // Antal i from-serie
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT rider_id) FROM series_participation
                WHERE series_id = ? AND season_year = ?
            ");
            $stmt->execute([$fromSeriesId, $year]);
            $fromCount = (int)$stmt->fetchColumn();

            // Antal som ocksa deltog i to-serie (same year)
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT sc.rider_id)
                FROM series_crossover sc
                WHERE sc.from_series_id = ? AND sc.to_series_id = ?
                AND sc.from_year = ? AND sc.crossover_type = 'same_year'
            ");
            $stmt->execute([$fromSeriesId, $toSeriesId, $year]);
            $flowCount = (int)$stmt->fetchColumn();

            $result[] = [
                'year' => $year,
                'from_count' => $fromCount,
                'flow_count' => $flowCount,
                'conversion_rate' => $fromCount > 0 ? round($flowCount / $fromCount * 100, 1) : 0,
            ];
        }

        // Berakna trend
        if (count($result) >= 2) {
            $first = $result[0]['conversion_rate'];
            $last = $result[count($result) - 1]['conversion_rate'];
            $trend = $last - $first;

            foreach ($result as &$r) {
                $r['overall_trend'] = $trend > 1 ? 'growing' : ($trend < -1 ? 'declining' : 'stable');
            }
        }

        return $result;
    }

    /**
     * Hamta oversikt av feeder-trends
     *
     * @param int $year Ar
     * @return array Alla floden med trend-indikatorer
     */
    public function getFeederTrendsOverview(int $year): array {
        $matrix = $this->calculateFeederMatrix($year);
        $prevMatrix = $this->calculateFeederMatrix($year - 1);

        // Skapa lookup for foregaende ar
        $prevLookup = [];
        foreach ($prevMatrix as $flow) {
            $key = $flow['from_series_id'] . '-' . $flow['to_series_id'];
            $prevLookup[$key] = $flow['flow_count'];
        }

        // Lagg till trend-info
        foreach ($matrix as &$flow) {
            $key = $flow['from_series_id'] . '-' . $flow['to_series_id'];
            $prevCount = $prevLookup[$key] ?? 0;

            $change = $flow['flow_count'] - $prevCount;
            $changePct = $prevCount > 0 ? round($change / $prevCount * 100, 1) : ($flow['flow_count'] > 0 ? 100 : 0);

            $flow['prev_count'] = $prevCount;
            $flow['change'] = $change;
            $flow['change_pct'] = $changePct;
            $flow['trend'] = $change > 2 ? 'growing' : ($change < -2 ? 'declining' : 'stable');
        }

        return $matrix;
    }

    /**
     * Hamta framvaxande floden (snabb tillvaxt)
     *
     * @param int $year Ar
     * @param float $minGrowth Minsta tillvaxt i procent
     * @return array Framvaxande floden
     */
    public function getEmergingFlows(int $year, float $minGrowth = 20.0): array {
        $trends = $this->getFeederTrendsOverview($year);

        $emerging = array_filter($trends, function($flow) use ($minGrowth) {
            return $flow['change_pct'] >= $minGrowth && $flow['flow_count'] >= 5;
        });

        usort($emerging, fn($a, $b) => $b['change_pct'] - $a['change_pct']);

        return $emerging;
    }

    // =========================================================================
    // GEOGRAPHIC ANALYSIS (Phase 2)
    // =========================================================================

    /**
     * Hamta regional tillvaxttend
     *
     * @param int $years Antal ar
     * @return array Trend per region
     */
    public function getRegionalGrowthTrend(int $years = 5): array {
        $currentYear = (int)date('Y');
        $startYear = $currentYear - $years + 1;

        $stmt = $this->pdo->prepare("
            SELECT
                rys.season_year as year,
                COALESCE(NULLIF(c.scf_district, ''), 'Okand') as region,
                COUNT(DISTINCT rys.rider_id) as rider_count
            FROM rider_yearly_stats rys
            JOIN riders r ON rys.rider_id = r.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE rys.season_year >= ? AND rys.season_year <= ?
            GROUP BY rys.season_year, COALESCE(NULLIF(c.scf_district, ''), 'Okand')
            ORDER BY rys.season_year ASC, rider_count DESC
        ");
        $stmt->execute([$startYear, $currentYear]);

        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Gruppera per region
        $byRegion = [];
        foreach ($results as $row) {
            $byRegion[$row['region']][] = [
                'year' => $row['year'],
                'count' => $row['rider_count'],
            ];
        }

        // Berakna tillvaxt
        $trends = [];
        foreach ($byRegion as $region => $years) {
            $firstYear = $years[0]['count'] ?? 0;
            $lastYear = $years[count($years) - 1]['count'] ?? 0;

            $growth = $firstYear > 0
                ? round(($lastYear - $firstYear) / $firstYear * 100, 1)
                : ($lastYear > 0 ? 100 : 0);

            $trends[$region] = [
                'region' => $region,
                'years' => $years,
                'first_year_count' => $firstYear,
                'last_year_count' => $lastYear,
                'growth_pct' => $growth,
                'trend' => $growth > 5 ? 'growing' : ($growth < -5 ? 'declining' : 'stable'),
            ];
        }

        // Sortera efter senaste antal
        uasort($trends, fn($a, $b) => $b['last_year_count'] - $a['last_year_count']);

        return $trends;
    }

    /**
     * Hamta underservade regioner (lag tackning per capita)
     *
     * @param int $year Ar
     * @return array Regioner sorterade efter tackning
     */
    public function getUnderservedRegions(int $year): array {
        // Hamta riders per region
        $regions = $this->getRidersByRegion($year);

        // Lagg till befolkningsdata fran config
        require_once __DIR__ . '/AnalyticsConfig.php';

        $result = [];
        foreach ($regions as $region) {
            $regionName = $region['region'];
            $population = AnalyticsConfig::SWEDISH_REGIONS[$regionName]['population'] ?? null;

            $ridersPerCapita = null;
            if ($population && $population > 0) {
                $ridersPerCapita = round($region['rider_count'] / $population * 100000, 2);
            }

            $result[] = [
                'region' => $regionName,
                'rider_count' => $region['rider_count'],
                'population' => $population,
                'riders_per_100k' => $ridersPerCapita,
            ];
        }

        // Sortera efter riders per capita (lagst forst)
        usort($result, function($a, $b) {
            if ($a['riders_per_100k'] === null) return 1;
            if ($b['riders_per_100k'] === null) return -1;
            return $a['riders_per_100k'] - $b['riders_per_100k'];
        });

        return $result;
    }

    /**
     * Hamta events per region (baserat pa destinationens region)
     *
     * Prioriterar venues.region (destinationens SCF-distrikt).
     * Om destination saknar region, anvands arrangorsklubbens distrikt som fallback.
     *
     * @param int $year Ar
     * @return array Events per region
     */
    public function getEventsByRegion(int $year): array {
        $stmt = $this->pdo->prepare("
            SELECT
                COALESCE(
                    NULLIF(v.region, ''),
                    NULLIF(c.scf_district, ''),
                    'Okand'
                ) as region,
                COUNT(DISTINCT e.id) as event_count,
                COUNT(DISTINCT res.cyclist_id) as participant_count,
                SUM(CASE WHEN e.discipline = 'Enduro' THEN 1 ELSE 0 END) as enduro_events,
                SUM(CASE WHEN e.discipline = 'DH' THEN 1 ELSE 0 END) as dh_events
            FROM events e
            LEFT JOIN venues v ON e.venue_id = v.id
            LEFT JOIN clubs c ON e.organizer_club_id = c.id
            LEFT JOIN results res ON e.id = res.event_id
            WHERE YEAR(e.date) = ?
            GROUP BY COALESCE(
                NULLIF(v.region, ''),
                NULLIF(c.scf_district, ''),
                'Okand'
            )
            ORDER BY event_count DESC
        ");
        $stmt->execute([$year]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // =========================================================================
    // CAREER PATH ANALYSIS - Feeder Pipeline & Series Level Transitions
    // =========================================================================

    /**
     * Hamta "feeder pipeline" - riders som startade regionalt och sen gick till nationellt
     *
     * Returnerar riders vars FORSTA tavling var i en regional serie,
     * och som sedan nagon gang deltog i en nationell serie.
     *
     * @param int|null $maxYear Senaste ar att inkludera (default: senaste data)
     * @return array Pipeline data uppdelat per feeder-serie
     */
    public function getFeederPipeline(?int $maxYear = null): array {
        $maxYear = $maxYear ?? $this->getLatestSeasonYear();

        $stmt = $this->pdo->prepare("
            SELECT
                first_series.series_id as feeder_series_id,
                s.name as feeder_series_name,
                s.region as feeder_region,
                COUNT(DISTINCT first_series.rider_id) as total_starters,
                COUNT(DISTINCT CASE WHEN nat.rider_id IS NOT NULL THEN first_series.rider_id END) as went_national,
                ROUND(
                    COUNT(DISTINCT CASE WHEN nat.rider_id IS NOT NULL THEN first_series.rider_id END) * 100.0 /
                    NULLIF(COUNT(DISTINCT first_series.rider_id), 0),
                1) as conversion_rate
            FROM (
                -- Hitta forsta serien for varje rider (maste vara regional)
                SELECT
                    sp.rider_id,
                    sp.series_id,
                    sp.season_year as first_year
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'regional'
                AND (sp.rider_id, sp.season_year) IN (
                    SELECT rider_id, MIN(season_year)
                    FROM series_participation
                    GROUP BY rider_id
                )
            ) first_series
            JOIN series s ON first_series.series_id = s.id
            LEFT JOIN (
                -- Riders som nagonsin deltog i en nationell serie
                SELECT DISTINCT sp.rider_id
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'national'
                AND sp.season_year <= ?
            ) nat ON first_series.rider_id = nat.rider_id
            WHERE first_series.first_year <= ?
            GROUP BY first_series.series_id, s.name, s.region
            ORDER BY went_national DESC
        ");
        $stmt->execute([$maxYear, $maxYear]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta riders som startade nationellt och sen provade regionalt
     *
     * Returnerar statistik for riders vars FORSTA tavling var i en nationell serie.
     *
     * @param int|null $maxYear Senaste ar att inkludera
     * @return array Flow data
     */
    public function getNationalToRegionalFlow(?int $maxYear = null): array {
        $maxYear = $maxYear ?? $this->getLatestSeasonYear();

        $stmt = $this->pdo->prepare("
            SELECT
                -- Totalt som startade nationellt
                COUNT(DISTINCT first_nat.rider_id) as started_national,

                -- Av dessa: provade regional
                COUNT(DISTINCT CASE WHEN reg.rider_id IS NOT NULL THEN first_nat.rider_id END) as tried_regional,

                -- Av dessa: slutade nationellt men fortsatte regionalt
                COUNT(DISTINCT CASE
                    WHEN reg.rider_id IS NOT NULL
                    AND last_nat.last_national_year < ?
                    AND last_reg.last_regional_year >= ?
                    THEN first_nat.rider_id
                END) as quit_national_kept_regional,

                -- Av dessa: fortsatter bade nationellt och regionalt
                COUNT(DISTINCT CASE
                    WHEN reg.rider_id IS NOT NULL
                    AND last_nat.last_national_year >= ?
                    THEN first_nat.rider_id
                END) as still_both

            FROM (
                -- Riders vars forsta tavling var nationell
                SELECT sp.rider_id, MIN(sp.season_year) as first_year
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'national'
                AND (sp.rider_id, sp.season_year) IN (
                    SELECT rider_id, MIN(season_year)
                    FROM series_participation
                    GROUP BY rider_id
                )
                GROUP BY sp.rider_id
            ) first_nat

            -- Vilka av dessa provade regional nagon gang?
            LEFT JOIN (
                SELECT DISTINCT sp.rider_id
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'regional'
            ) reg ON first_nat.rider_id = reg.rider_id

            -- Senaste ar de tavlade nationellt
            LEFT JOIN (
                SELECT sp.rider_id, MAX(sp.season_year) as last_national_year
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'national'
                GROUP BY sp.rider_id
            ) last_nat ON first_nat.rider_id = last_nat.rider_id

            -- Senaste ar de tavlade regionalt
            LEFT JOIN (
                SELECT sp.rider_id, MAX(sp.season_year) as last_regional_year
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'regional'
                GROUP BY sp.rider_id
            ) last_reg ON first_nat.rider_id = last_reg.rider_id

            WHERE first_nat.first_year <= ?
        ");
        // Anvand maxYear - 1 for "slutade nationellt" (maste ha minst 1 ar utan)
        $stmt->execute([$maxYear, $maxYear - 1, $maxYear - 1, $maxYear]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta detaljerad karriarvags-analys
     *
     * Kategoriserar alla riders baserat pa deras serie-niva-historia:
     * - regional_only: Bara regionalt
     * - national_only: Bara nationellt
     * - regional_to_national: Startade regionalt, gick till nationellt
     * - national_to_regional: Startade nationellt, provade regionalt
     * - mixed: Startade med bada samma ar
     *
     * @param int|null $maxYear Senaste ar
     * @return array Karriarvagar med antal
     */
    public function getCareerPathsAnalysis(?int $maxYear = null): array {
        $maxYear = $maxYear ?? $this->getLatestSeasonYear();

        $stmt = $this->pdo->prepare("
            SELECT
                CASE
                    WHEN first_regional IS NULL AND first_national IS NOT NULL THEN 'national_only'
                    WHEN first_national IS NULL AND first_regional IS NOT NULL THEN 'regional_only'
                    WHEN first_regional < first_national THEN 'regional_to_national'
                    WHEN first_national < first_regional THEN 'national_to_regional'
                    WHEN first_regional = first_national THEN 'started_both'
                    ELSE 'unknown'
                END as career_path,
                COUNT(*) as rider_count
            FROM (
                SELECT
                    r.id as rider_id,
                    reg.first_regional,
                    nat.first_national
                FROM riders r
                LEFT JOIN (
                    SELECT sp.rider_id, MIN(sp.season_year) as first_regional
                    FROM series_participation sp
                    JOIN series ser ON sp.series_id = ser.id
                    WHERE ser.series_level = 'regional'
                    GROUP BY sp.rider_id
                ) reg ON r.id = reg.rider_id
                LEFT JOIN (
                    SELECT sp.rider_id, MIN(sp.season_year) as first_national
                    FROM series_participation sp
                    JOIN series ser ON sp.series_id = ser.id
                    WHERE ser.series_level = 'national'
                    GROUP BY sp.rider_id
                ) nat ON r.id = nat.rider_id
                WHERE reg.first_regional IS NOT NULL OR nat.first_national IS NOT NULL
                AND COALESCE(reg.first_regional, nat.first_national) <= ?
            ) paths
            GROUP BY career_path
            ORDER BY rider_count DESC
        ");
        $stmt->execute([$maxYear]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta forsta-tavlings-statistik per serie (entry points for first-timers)
     *
     * Visar vilka serier som ar "gateway" serier dar riders har sin forsta tavling.
     *
     * @param int $year Ar att analysera
     * @return array Entry point data per serie
     */
    public function getFirstRaceEntryPoints(int $year): array {
        $stmt = $this->pdo->prepare("
            SELECT
                s.id as series_id,
                s.name as series_name,
                s.series_level,
                s.region,
                COUNT(DISTINCT first_race.rider_id) as first_timers,
                -- Av dessa: hur manga fortsatte nasta ar?
                COUNT(DISTINCT CASE WHEN next_year.rider_id IS NOT NULL THEN first_race.rider_id END) as returned_next_year,
                ROUND(
                    COUNT(DISTINCT CASE WHEN next_year.rider_id IS NOT NULL THEN first_race.rider_id END) * 100.0 /
                    NULLIF(COUNT(DISTINCT first_race.rider_id), 0),
                1) as first_year_retention
            FROM (
                -- Riders vars forsta tavlingsdeltagande var detta ar
                SELECT sp.rider_id, sp.series_id
                FROM series_participation sp
                WHERE sp.season_year = ?
                AND (sp.rider_id, sp.season_year) IN (
                    SELECT rider_id, MIN(season_year)
                    FROM series_participation
                    GROUP BY rider_id
                )
            ) first_race
            JOIN series s ON first_race.series_id = s.id
            LEFT JOIN (
                -- Deltog de nasta ar (i nagon serie)?
                SELECT DISTINCT rider_id
                FROM series_participation
                WHERE season_year = ?
            ) next_year ON first_race.rider_id = next_year.rider_id
            GROUP BY s.id, s.name, s.series_level, s.region
            ORDER BY first_timers DESC
        ");
        $stmt->execute([$year, $year + 1]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Hamta "graduation" statistik - riders som gick fran regional till national
     *
     * @param int $fromYear Startår
     * @param int $toYear Slutår
     * @return array Årlig graduation data
     */
    public function getGraduationTrend(int $fromYear, int $toYear): array {
        $result = [];

        for ($year = $fromYear; $year <= $toYear; $year++) {
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT sp.rider_id) as graduated
                FROM series_participation sp
                JOIN series ser ON sp.series_id = ser.id
                WHERE ser.series_level = 'national'
                AND sp.season_year = ?
                AND sp.rider_id IN (
                    -- Riders som tavlade regionalt foregaende ar men INTE nationellt
                    SELECT DISTINCT sp2.rider_id
                    FROM series_participation sp2
                    JOIN series ser2 ON sp2.series_id = ser2.id
                    WHERE ser2.series_level = 'regional'
                    AND sp2.season_year = ?
                    AND sp2.rider_id NOT IN (
                        SELECT DISTINCT sp3.rider_id
                        FROM series_participation sp3
                        JOIN series ser3 ON sp3.series_id = ser3.id
                        WHERE ser3.series_level = 'national'
                        AND sp3.season_year = ?
                    )
                )
            ");
            $stmt->execute([$year, $year - 1, $year - 1]);
            $graduated = (int)$stmt->fetchColumn();

            $result[] = [
                'year' => $year,
                'graduated' => $graduated
            ];
        }

        return $result;
    }

    // =========================================================================
    // FIRST SEASON JOURNEY ANALYSIS (v3.1)
    // =========================================================================

    /**
     * Build safe IN clause for brand filtering
     *
     * @param array|null $brandIds Brand IDs to filter (max 12)
     * @return array ['clause' => string, 'params' => array]
     */
    private function buildBrandFilter(?array $brandIds): array {
        if (empty($brandIds)) {
            return ['clause' => '', 'params' => []];
        }

        // Max 12 brands
        $brandIds = array_slice(array_filter($brandIds, 'is_numeric'), 0, 12);
        if (empty($brandIds)) {
            return ['clause' => '', 'params' => []];
        }

        $placeholders = implode(',', array_fill(0, count($brandIds), '?'));
        return [
            'clause' => "AND first_brand_id IN ($placeholders)",
            'params' => array_map('intval', $brandIds)
        ];
    }

    /**
     * Get First Season Journey summary statistics
     *
     * @param int $cohortYear Cohort year
     * @param array|null $brandIds Optional brand filter (max 12)
     * @return array Summary statistics
     */
    public function getFirstSeasonJourneySummary(int $cohortYear, ?array $brandIds = null): array {
        $brandFilter = $this->buildBrandFilter($brandIds);

        $sql = "
            SELECT
                COUNT(*) AS total_rookies,
                AVG(total_starts) AS avg_starts,
                AVG(total_events) AS avg_events,
                AVG(total_finishes) AS avg_finishes,
                AVG(CASE WHEN total_starts > 0 THEN (total_starts - total_finishes) / total_starts END) AS avg_dnf_rate,
                AVG(result_percentile) AS avg_percentile,
                AVG(engagement_score) AS avg_engagement,
                SUM(returned_year2) / COUNT(*) AS return_rate_y2,
                SUM(returned_year3) / COUNT(*) AS return_rate_y3,
                AVG(total_career_seasons) AS avg_career_length,
                SUM(CASE WHEN activity_pattern = 'high_engagement' THEN 1 ELSE 0 END) AS high_engagement_count,
                SUM(CASE WHEN activity_pattern = 'moderate' THEN 1 ELSE 0 END) AS moderate_count,
                SUM(CASE WHEN activity_pattern = 'low_engagement' THEN 1 ELSE 0 END) AS low_engagement_count
            FROM rider_first_season
            WHERE cohort_year = ?
            {$brandFilter['clause']}
        ";

        $params = array_merge([$cohortYear], $brandFilter['params']);

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        // Apply GDPR check
        if (!$data || $data['total_rookies'] < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)',
                'cohort_year' => $cohortYear
            ];
        }

        return [
            'cohort_year' => $cohortYear,
            'total_rookies' => (int)$data['total_rookies'],
            'avg_starts' => round((float)$data['avg_starts'], 2),
            'avg_events' => round((float)$data['avg_events'], 2),
            'avg_finishes' => round((float)$data['avg_finishes'], 2),
            'avg_dnf_rate' => round((float)$data['avg_dnf_rate'] * 100, 1),
            'avg_percentile' => round((float)$data['avg_percentile'], 1),
            'avg_engagement' => round((float)$data['avg_engagement'], 1),
            'return_rate_y2' => round((float)$data['return_rate_y2'] * 100, 1),
            'return_rate_y3' => round((float)$data['return_rate_y3'] * 100, 1),
            'avg_career_length' => round((float)$data['avg_career_length'], 2),
            'engagement_distribution' => [
                'high' => (int)$data['high_engagement_count'],
                'moderate' => (int)$data['moderate_count'],
                'low' => (int)$data['low_engagement_count']
            ],
            'suppressed' => false
        ];
    }

    /**
     * Get cohort longitudinal overview (retention funnel)
     *
     * @param int $cohortYear Cohort year
     * @param array|null $brandIds Optional brand filter
     * @return array Retention funnel data
     */
    public function getCohortLongitudinalOverview(int $cohortYear, ?array $brandIds = null): array {
        $brandFilter = $this->buildBrandFilter($brandIds);

        // Use brand filter on rider_first_season join
        $brandJoin = empty($brandFilter['clause']) ? '' :
            "JOIN rider_first_season rfs ON rjy.rider_id = rfs.rider_id AND rjy.cohort_year = rfs.cohort_year";

        $sql = "
            SELECT
                rjy.year_offset,
                COUNT(*) AS cohort_size,
                SUM(rjy.was_active) AS active_count,
                SUM(rjy.was_active) / COUNT(*) AS retention_rate,
                AVG(CASE WHEN rjy.was_active = 1 THEN rjy.total_starts END) AS avg_starts,
                AVG(CASE WHEN rjy.was_active = 1 THEN rjy.total_events END) AS avg_events,
                AVG(CASE WHEN rjy.was_active = 1 THEN rjy.result_percentile END) AS avg_percentile,
                SUM(CASE WHEN rjy.was_active = 1 AND rjy.percentile_delta > 0 THEN 1 ELSE 0 END) AS improved_count
            FROM rider_journey_years rjy
            " . (empty($brandFilter['clause']) ? '' : "
            JOIN rider_first_season rfs ON rjy.rider_id = rfs.rider_id AND rjy.cohort_year = rfs.cohort_year
            ") . "
            WHERE rjy.cohort_year = ?
            " . str_replace('first_brand_id', 'rfs.first_brand_id', $brandFilter['clause']) . "
            GROUP BY rjy.year_offset
            ORDER BY rjy.year_offset
        ";

        $params = array_merge([$cohortYear], $brandFilter['params']);

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // GDPR check on base cohort
        if (empty($results) || $results[0]['cohort_size'] < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)',
                'cohort_year' => $cohortYear
            ];
        }

        $funnel = [];
        foreach ($results as $row) {
            $funnel[] = [
                'year_offset' => (int)$row['year_offset'],
                'cohort_size' => (int)$row['cohort_size'],
                'active_count' => (int)$row['active_count'],
                'retention_rate' => round((float)$row['retention_rate'] * 100, 1),
                'avg_starts' => round((float)$row['avg_starts'], 2),
                'avg_events' => round((float)$row['avg_events'], 2),
                'avg_percentile' => round((float)$row['avg_percentile'], 1),
                'improved_count' => (int)$row['improved_count']
            ];
        }

        return [
            'cohort_year' => $cohortYear,
            'funnel' => $funnel,
            'suppressed' => false
        ];
    }

    /**
     * Get journey type distribution
     *
     * @param int $cohortYear Cohort year
     * @param array|null $brandIds Optional brand filter
     * @return array Journey pattern distribution
     */
    public function getJourneyTypeDistribution(int $cohortYear, ?array $brandIds = null): array {
        $brandFilter = $this->buildBrandFilter($brandIds);

        $sql = "
            SELECT
                rjs.journey_pattern,
                COUNT(*) AS rider_count,
                AVG(rjs.fs_engagement_score) AS avg_engagement,
                AVG(rjs.fs_result_percentile) AS avg_percentile
            FROM rider_journey_summary rjs
            " . (empty($brandFilter['clause']) ? '' : "
            JOIN rider_first_season rfs ON rjs.rider_id = rfs.rider_id AND rjs.cohort_year = rfs.cohort_year
            ") . "
            WHERE rjs.cohort_year = ?
            " . str_replace('first_brand_id', 'rfs.first_brand_id', $brandFilter['clause']) . "
            GROUP BY rjs.journey_pattern
            HAVING COUNT(*) >= 10
            ORDER BY rider_count DESC
        ";

        $params = array_merge([$cohortYear], $brandFilter['params']);

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $total = array_sum(array_column($results, 'rider_count'));

        if ($total < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)',
                'cohort_year' => $cohortYear
            ];
        }

        $distribution = [];
        foreach ($results as $row) {
            $distribution[] = [
                'pattern' => $row['journey_pattern'],
                'count' => (int)$row['rider_count'],
                'percentage' => round((int)$row['rider_count'] / $total * 100, 1),
                'avg_engagement' => round((float)$row['avg_engagement'], 1),
                'avg_percentile' => round((float)$row['avg_percentile'], 1)
            ];
        }

        return [
            'cohort_year' => $cohortYear,
            'total_classified' => $total,
            'distribution' => $distribution,
            'suppressed' => false
        ];
    }

    /**
     * Get retention by first season start count
     *
     * @param int $cohortYear Cohort year
     * @param array|null $brandIds Optional brand filter
     * @return array Retention data by start count
     */
    public function getRetentionByStartCount(int $cohortYear, ?array $brandIds = null): array {
        $brandFilter = $this->buildBrandFilter($brandIds);

        $sql = "
            SELECT
                CASE
                    WHEN total_starts = 1 THEN '1 start'
                    WHEN total_starts BETWEEN 2 AND 3 THEN '2-3 starts'
                    WHEN total_starts BETWEEN 4 AND 6 THEN '4-6 starts'
                    WHEN total_starts BETWEEN 7 AND 10 THEN '7-10 starts'
                    ELSE '11+ starts'
                END AS start_bucket,
                COUNT(*) AS rider_count,
                SUM(returned_year2) / COUNT(*) AS return_rate_y2,
                SUM(returned_year3) / COUNT(*) AS return_rate_y3,
                AVG(total_career_seasons) AS avg_career
            FROM rider_first_season
            WHERE cohort_year = ?
            {$brandFilter['clause']}
            GROUP BY
                CASE
                    WHEN total_starts = 1 THEN '1 start'
                    WHEN total_starts BETWEEN 2 AND 3 THEN '2-3 starts'
                    WHEN total_starts BETWEEN 4 AND 6 THEN '4-6 starts'
                    WHEN total_starts BETWEEN 7 AND 10 THEN '7-10 starts'
                    ELSE '11+ starts'
                END
            HAVING COUNT(*) >= 10
            ORDER BY MIN(total_starts)
        ";

        $params = array_merge([$cohortYear], $brandFilter['params']);

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($results)) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)',
                'cohort_year' => $cohortYear
            ];
        }

        $buckets = [];
        foreach ($results as $row) {
            $buckets[] = [
                'bucket' => $row['start_bucket'],
                'rider_count' => (int)$row['rider_count'],
                'return_rate_y2' => round((float)$row['return_rate_y2'] * 100, 1),
                'return_rate_y3' => round((float)$row['return_rate_y3'] * 100, 1),
                'avg_career' => round((float)$row['avg_career'], 2)
            ];
        }

        return [
            'cohort_year' => $cohortYear,
            'buckets' => $buckets,
            'suppressed' => false
        ];
    }

    // =========================================================================
    // BRAND COMPARISON (v3.1)
    // =========================================================================

    /**
     * Get multi-brand journey comparison
     *
     * @param int $cohortYear Cohort year
     * @param array $brandIds Brand IDs to compare (max 12)
     * @return array Brand comparison data
     */
    public function getBrandJourneyComparison(int $cohortYear, array $brandIds): array {
        if (empty($brandIds)) {
            return ['error' => 'No brands specified'];
        }

        // Max 12 brands
        $brandIds = array_slice(array_filter($brandIds, 'is_numeric'), 0, 12);
        $placeholders = implode(',', array_fill(0, count($brandIds), '?'));

        $sql = "
            SELECT
                b.id AS brand_id,
                b.name AS brand_name,
                b.short_code,
                b.color_primary,
                COUNT(*) AS rookie_count,
                AVG(rfs.total_starts) AS avg_starts,
                AVG(rfs.total_events) AS avg_events,
                AVG(rfs.result_percentile) AS avg_percentile,
                AVG(rfs.engagement_score) AS avg_engagement,
                SUM(rfs.returned_year2) / COUNT(*) AS return_rate_y2,
                SUM(rfs.returned_year3) / COUNT(*) AS return_rate_y3,
                AVG(rfs.total_career_seasons) AS avg_career_seasons
            FROM rider_first_season rfs
            JOIN series_brands b ON rfs.first_brand_id = b.id
            WHERE rfs.cohort_year = ?
            AND rfs.first_brand_id IN ($placeholders)
            GROUP BY b.id, b.name, b.short_code, b.color_primary
            HAVING COUNT(*) >= 10
            ORDER BY rookie_count DESC
        ";

        $params = array_merge([$cohortYear], array_map('intval', $brandIds));

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $brands = [];
        foreach ($results as $row) {
            $brands[] = [
                'brand_id' => (int)$row['brand_id'],
                'brand_name' => $row['brand_name'],
                'short_code' => $row['short_code'],
                'color' => $row['color_primary'],
                'rookie_count' => (int)$row['rookie_count'],
                'avg_starts' => round((float)$row['avg_starts'], 2),
                'avg_events' => round((float)$row['avg_events'], 2),
                'avg_percentile' => round((float)$row['avg_percentile'], 1),
                'avg_engagement' => round((float)$row['avg_engagement'], 1),
                'return_rate_y2' => round((float)$row['return_rate_y2'] * 100, 1),
                'return_rate_y3' => round((float)$row['return_rate_y3'] * 100, 1),
                'avg_career_seasons' => round((float)$row['avg_career_seasons'], 2)
            ];
        }

        return [
            'cohort_year' => $cohortYear,
            'brands' => $brands,
            'brand_count' => count($brands)
        ];
    }

    /**
     * Get brand-specific retention funnel
     *
     * @param int $brandId Brand ID
     * @param int $cohortYear Cohort year
     * @return array Retention funnel for brand
     */
    public function getBrandRetentionFunnel(int $brandId, int $cohortYear): array {
        $sql = "
            SELECT
                rjy.year_offset,
                COUNT(*) AS cohort_size,
                SUM(rjy.was_active) AS active_count,
                SUM(rjy.was_active) / COUNT(*) AS retention_rate,
                AVG(CASE WHEN rjy.was_active = 1 THEN rjy.total_starts END) AS avg_starts,
                AVG(CASE WHEN rjy.was_active = 1 THEN rjy.result_percentile END) AS avg_percentile
            FROM rider_journey_years rjy
            JOIN rider_first_season rfs ON rjy.rider_id = rfs.rider_id AND rjy.cohort_year = rfs.cohort_year
            WHERE rjy.cohort_year = ?
            AND rfs.first_brand_id = ?
            GROUP BY rjy.year_offset
            ORDER BY rjy.year_offset
        ";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([$cohortYear, $brandId]);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Get brand info
        $brandStmt = $this->pdo->prepare("SELECT name, short_code, color_primary FROM series_brands WHERE id = ?");
        $brandStmt->execute([$brandId]);
        $brand = $brandStmt->fetch(PDO::FETCH_ASSOC);

        if (empty($results) || $results[0]['cohort_size'] < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)',
                'brand_id' => $brandId,
                'cohort_year' => $cohortYear
            ];
        }

        $funnel = [];
        foreach ($results as $row) {
            $funnel[] = [
                'year_offset' => (int)$row['year_offset'],
                'cohort_size' => (int)$row['cohort_size'],
                'active_count' => (int)$row['active_count'],
                'retention_rate' => round((float)$row['retention_rate'] * 100, 1),
                'avg_starts' => round((float)$row['avg_starts'], 2),
                'avg_percentile' => round((float)$row['avg_percentile'], 1)
            ];
        }

        return [
            'brand_id' => $brandId,
            'brand_name' => $brand['name'] ?? 'Unknown',
            'short_code' => $brand['short_code'] ?? null,
            'color' => $brand['color_primary'] ?? null,
            'cohort_year' => $cohortYear,
            'funnel' => $funnel,
            'suppressed' => false
        ];
    }

    /**
     * Get journey patterns by brand
     *
     * @param int $cohortYear Cohort year
     * @param array $brandIds Brand IDs to analyze
     * @return array Journey patterns per brand
     */
    public function getJourneyPatternsByBrand(int $cohortYear, array $brandIds): array {
        if (empty($brandIds)) {
            return ['error' => 'No brands specified'];
        }

        $brandIds = array_slice(array_filter($brandIds, 'is_numeric'), 0, 12);
        $placeholders = implode(',', array_fill(0, count($brandIds), '?'));

        $sql = "
            SELECT
                b.id AS brand_id,
                b.name AS brand_name,
                b.short_code,
                rjs.journey_pattern,
                COUNT(*) AS rider_count
            FROM rider_journey_summary rjs
            JOIN rider_first_season rfs ON rjs.rider_id = rfs.rider_id AND rjs.cohort_year = rfs.cohort_year
            JOIN series_brands b ON rfs.first_brand_id = b.id
            WHERE rjs.cohort_year = ?
            AND rfs.first_brand_id IN ($placeholders)
            GROUP BY b.id, b.name, b.short_code, rjs.journey_pattern
            HAVING COUNT(*) >= 10
            ORDER BY b.name, rider_count DESC
        ";

        $params = array_merge([$cohortYear], array_map('intval', $brandIds));

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Organize by brand
        $byBrand = [];
        foreach ($results as $row) {
            $brandId = (int)$row['brand_id'];
            if (!isset($byBrand[$brandId])) {
                $byBrand[$brandId] = [
                    'brand_id' => $brandId,
                    'brand_name' => $row['brand_name'],
                    'short_code' => $row['short_code'],
                    'patterns' => [],
                    'total' => 0
                ];
            }
            $byBrand[$brandId]['patterns'][] = [
                'pattern' => $row['journey_pattern'],
                'count' => (int)$row['rider_count']
            ];
            $byBrand[$brandId]['total'] += (int)$row['rider_count'];
        }

        // Calculate percentages
        foreach ($byBrand as &$brand) {
            foreach ($brand['patterns'] as &$pattern) {
                $pattern['percentage'] = round($pattern['count'] / $brand['total'] * 100, 1);
            }
        }

        return [
            'cohort_year' => $cohortYear,
            'brands' => array_values($byBrand)
        ];
    }

    /**
     * Get available brands for journey filtering
     *
     * @param int|null $cohortYear Optional cohort year filter
     * @return array Available brands with rookie counts
     */
    public function getAvailableBrandsForJourney(?int $cohortYear = null): array {
        $whereClause = $cohortYear ? 'WHERE rfs.cohort_year = ?' : '';
        $params = $cohortYear ? [$cohortYear] : [];

        $sql = "
            SELECT
                b.id,
                b.name,
                b.short_code,
                b.color_primary,
                COUNT(DISTINCT rfs.rider_id) AS rookie_count
            FROM series_brands b
            JOIN rider_first_season rfs ON rfs.first_brand_id = b.id
            $whereClause
            GROUP BY b.id, b.name, b.short_code, b.color_primary
            HAVING COUNT(DISTINCT rfs.rider_id) >= 10
            ORDER BY rookie_count DESC
        ";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Get available cohort years with optional brand filter
     *
     * @param array|null $brandIds Optional brand filter
     * @return array Available cohort years
     */
    public function getAvailableCohortYears(?array $brandIds = null): array {
        $brandFilter = $this->buildBrandFilter($brandIds);

        $sql = "
            SELECT
                cohort_year,
                COUNT(*) AS rookie_count
            FROM rider_first_season
            WHERE 1=1
            {$brandFilter['clause']}
            GROUP BY cohort_year
            HAVING COUNT(*) >= 10
            ORDER BY cohort_year DESC
        ";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($brandFilter['params']);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Export journey data (respects GDPR)
     *
     * @param int $cohortYear Cohort year
     * @param array|null $brandIds Optional brand filter
     * @param string $format Export format ('csv' or 'json')
     * @return array Export data with metadata
     */
    public function exportJourneyData(int $cohortYear, ?array $brandIds = null, string $format = 'csv'): array {
        $summary = $this->getFirstSeasonJourneySummary($cohortYear, $brandIds);
        $longitudinal = $this->getCohortLongitudinalOverview($cohortYear, $brandIds);
        $patterns = $this->getJourneyTypeDistribution($cohortYear, $brandIds);
        $retention = $this->getRetentionByStartCount($cohortYear, $brandIds);

        // Build export data
        $exportData = [
            'metadata' => [
                'cohort_year' => $cohortYear,
                'brand_filter' => $brandIds,
                'exported_at' => date('Y-m-d H:i:s'),
                'gdpr_compliant' => true
            ],
            'summary' => $summary,
            'retention_funnel' => $longitudinal,
            'journey_patterns' => $patterns,
            'retention_by_starts' => $retention
        ];

        if ($format === 'csv') {
            return [
                'format' => 'csv',
                'data' => $this->convertToCSV($exportData),
                'filename' => "journey_cohort_{$cohortYear}_" . date('Ymd') . ".csv"
            ];
        }

        return [
            'format' => 'json',
            'data' => $exportData,
            'filename' => "journey_cohort_{$cohortYear}_" . date('Ymd') . ".json"
        ];
    }

    /**
     * Convert journey data to CSV format
     *
     * @param array $data Journey data
     * @return string CSV content
     */
    private function convertToCSV(array $data): string {
        $lines = [];

        // Summary section
        $lines[] = "# First Season Journey Summary";
        $lines[] = "Cohort Year," . $data['metadata']['cohort_year'];
        $lines[] = "";

        if (!empty($data['summary']) && empty($data['summary']['suppressed'])) {
            $lines[] = "Metric,Value";
            $lines[] = "Total Rookies," . $data['summary']['total_rookies'];
            $lines[] = "Avg Starts," . $data['summary']['avg_starts'];
            $lines[] = "Avg Events," . $data['summary']['avg_events'];
            $lines[] = "Avg DNF Rate (%)," . $data['summary']['avg_dnf_rate'];
            $lines[] = "Avg Percentile," . $data['summary']['avg_percentile'];
            $lines[] = "Year 2 Return Rate (%)," . $data['summary']['return_rate_y2'];
            $lines[] = "Year 3 Return Rate (%)," . $data['summary']['return_rate_y3'];
            $lines[] = "";
        }

        // Retention funnel section
        if (!empty($data['retention_funnel']) && empty($data['retention_funnel']['suppressed'])) {
            $lines[] = "# Retention Funnel";
            $lines[] = "Year Offset,Cohort Size,Active Count,Retention Rate (%),Avg Starts";
            foreach ($data['retention_funnel']['funnel'] as $row) {
                $lines[] = implode(',', [
                    $row['year_offset'],
                    $row['cohort_size'],
                    $row['active_count'],
                    $row['retention_rate'],
                    $row['avg_starts']
                ]);
            }
            $lines[] = "";
        }

        // Journey patterns section
        if (!empty($data['journey_patterns']) && empty($data['journey_patterns']['suppressed'])) {
            $lines[] = "# Journey Patterns";
            $lines[] = "Pattern,Count,Percentage (%)";
            foreach ($data['journey_patterns']['distribution'] as $row) {
                $lines[] = implode(',', [
                    $row['pattern'],
                    $row['count'],
                    $row['percentage']
                ]);
            }
            $lines[] = "";
        }

        return implode("\n", $lines);
    }

    // =========================================================================
    // EVENT PARTICIPATION ANALYSIS (v3.2)
    // =========================================================================

    /**
     * Build brand filter for series-based queries
     * Resolves brands via brand_series_map
     *
     * @param array|null $brandIds Brand IDs to filter
     * @return array ['clause' => string, 'params' => array, 'join' => string]
     */
    private function buildSeriesBrandFilter(?array $brandIds): array {
        if (empty($brandIds)) {
            return ['clause' => '', 'params' => [], 'join' => ''];
        }

        // Max 12 brands
        $brandIds = array_slice(array_filter($brandIds, 'is_numeric'), 0, 12);
        if (empty($brandIds)) {
            return ['clause' => '', 'params' => [], 'join' => ''];
        }

        $placeholders = implode(',', array_fill(0, count($brandIds), '?'));
        return [
            'join' => "JOIN brand_series_map bsm ON e.series_id = bsm.series_id
                       AND (bsm.relationship_type = 'owner' OR bsm.relationship_type IS NULL)",
            'clause' => "AND bsm.brand_id IN ($placeholders)",
            'params' => array_map('intval', $brandIds)
        ];
    }

    /**
     * Get participation distribution for a series
     * Shows how many participants attend 1, 2, 3... N events
     *
     * @param int $seriesId Series ID
     * @param int $year Season year
     * @param array|null $brandIds Optional brand filter
     * @return array Distribution data
     */
    public function getSeriesParticipationDistribution(int $seriesId, int $year, ?array $brandIds = null): array {
        $brandFilter = $this->buildSeriesBrandFilter($brandIds);

        // Get total events in series for this year
        $stmt = $this->pdo->prepare("
            SELECT COUNT(*) FROM events e
            {$brandFilter['join']}
            WHERE e.series_id = ? AND YEAR(e.date) = ?
            {$brandFilter['clause']}
        ");
        $params = array_merge([$seriesId, $year], $brandFilter['params']);
        $stmt->execute($params);
        $totalEvents = (int)$stmt->fetchColumn();

        if ($totalEvents === 0) {
            return [
                'suppressed' => true,
                'reason' => 'No events found for this series/year'
            ];
        }

        // Get participation distribution
        $sql = "
            SELECT
                events_attended,
                COUNT(*) AS participant_count
            FROM (
                SELECT
                    r.cyclist_id,
                    COUNT(DISTINCT r.event_id) AS events_attended
                FROM results r
                JOIN events e ON r.event_id = e.id
                {$brandFilter['join']}
                WHERE e.series_id = ? AND YEAR(e.date) = ?
                {$brandFilter['clause']}
                GROUP BY r.cyclist_id
            ) rider_counts
            GROUP BY events_attended
            ORDER BY events_attended
        ";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $rawDistribution = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Get total participants
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT r.cyclist_id)
            FROM results r
            JOIN events e ON r.event_id = e.id
            {$brandFilter['join']}
            WHERE e.series_id = ? AND YEAR(e.date) = ?
            {$brandFilter['clause']}
        ");
        $stmt->execute($params);
        $totalParticipants = (int)$stmt->fetchColumn();

        if ($totalParticipants < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)'
            ];
        }

        // Build distribution with percentages
        $distribution = [];
        $singleEventCount = 0;
        $fullSeriesCount = 0;
        $totalEventsAttended = 0;

        foreach ($rawDistribution as $row) {
            $count = (int)$row['events_attended'];
            $participants = (int)$row['participant_count'];
            $pct = round(100 * $participants / $totalParticipants, 1);

            $distribution[$count] = [
                'events' => $count,
                'count' => $participants,
                'percentage' => $pct
            ];

            $totalEventsAttended += $count * $participants;

            if ($count === 1) {
                $singleEventCount = $participants;
            }
            if ($count === $totalEvents) {
                $fullSeriesCount = $participants;
            }
        }

        return [
            'series_id' => $seriesId,
            'season_year' => $year,
            'total_events_in_series' => $totalEvents,
            'total_participants' => $totalParticipants,
            'distribution' => $distribution,
            'avg_events_per_rider' => round($totalEventsAttended / $totalParticipants, 2),
            'single_event_count' => $singleEventCount,
            'single_event_pct' => round(100 * $singleEventCount / $totalParticipants, 1),
            'full_series_count' => $fullSeriesCount,
            'full_series_pct' => round(100 * $fullSeriesCount / $totalParticipants, 1),
            'brand_filter' => $brandIds
        ];
    }

    /**
     * Get events with unique (single-event) participants
     * Shows which events attract participants who ONLY attend that event
     *
     * @param int $seriesId Series ID
     * @param int $year Season year
     * @param array|null $brandIds Optional brand filter
     * @return array Events ranked by unique participant percentage
     */
    public function getEventsWithUniqueParticipants(int $seriesId, int $year, ?array $brandIds = null): array {
        $brandFilter = $this->buildSeriesBrandFilter($brandIds);

        $sql = "
            SELECT
                e.id AS event_id,
                e.name AS event_name,
                e.date AS event_date,
                e.venue_id,
                v.name AS venue_name,
                v.city AS venue_city,
                total_stats.total_participants,
                unique_stats.unique_count,
                ROUND(100 * unique_stats.unique_count / total_stats.total_participants, 1) AS unique_pct
            FROM events e
            LEFT JOIN venues v ON e.venue_id = v.id
            {$brandFilter['join']}
            -- Total participants per event
            JOIN (
                SELECT event_id, COUNT(DISTINCT cyclist_id) AS total_participants
                FROM results
                GROUP BY event_id
            ) total_stats ON total_stats.event_id = e.id
            -- Unique participants (only this event in series)
            LEFT JOIN (
                SELECT
                    r.event_id,
                    COUNT(DISTINCT r.cyclist_id) AS unique_count
                FROM results r
                JOIN events e2 ON r.event_id = e2.id
                WHERE r.cyclist_id IN (
                    -- Riders who only attended 1 event in this series this year
                    SELECT cyclist_id
                    FROM results r3
                    JOIN events e3 ON r3.event_id = e3.id
                    WHERE e3.series_id = ? AND YEAR(e3.date) = ?
                    GROUP BY cyclist_id
                    HAVING COUNT(DISTINCT r3.event_id) = 1
                )
                AND e2.series_id = ? AND YEAR(e2.date) = ?
                GROUP BY r.event_id
            ) unique_stats ON unique_stats.event_id = e.id
            WHERE e.series_id = ? AND YEAR(e.date) = ?
            {$brandFilter['clause']}
            AND total_stats.total_participants >= 10
            ORDER BY unique_pct DESC
        ";

        $params = array_merge(
            [$seriesId, $year, $seriesId, $year, $seriesId, $year],
            $brandFilter['params']
        );

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($events)) {
            return [
                'suppressed' => true,
                'reason' => 'No events with sufficient data'
            ];
        }

        return [
            'series_id' => $seriesId,
            'season_year' => $year,
            'events' => $events,
            'brand_filter' => $brandIds
        ];
    }

    /**
     * Get event retention year-over-year
     * Shows how many participants return to the same event next year
     *
     * @param int $eventId Event ID (from year)
     * @param int $fromYear From year
     * @param int $toYear To year (usually fromYear + 1)
     * @return array Retention statistics
     */
    public function getEventRetention(int $eventId, int $fromYear, int $toYear): array {
        // Get event info
        $stmt = $this->pdo->prepare("
            SELECT e.*, s.name AS series_name, v.name AS venue_name, v.city AS venue_city
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN venues v ON e.venue_id = v.id
            WHERE e.id = ?
        ");
        $stmt->execute([$eventId]);
        $event = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$event) {
            return ['error' => 'Event not found'];
        }

        // Find matching event in to_year (same series, same venue or similar name)
        $stmt = $this->pdo->prepare("
            SELECT id FROM events
            WHERE series_id = ?
              AND YEAR(date) = ?
              AND (venue_id = ? OR name LIKE ?)
            ORDER BY
                CASE WHEN venue_id = ? THEN 0 ELSE 1 END,
                date ASC
            LIMIT 1
        ");
        $likeName = '%' . substr($event['name'], 0, 20) . '%';
        $stmt->execute([$event['series_id'], $toYear, $event['venue_id'], $likeName, $event['venue_id']]);
        $matchedEventId = $stmt->fetchColumn();

        // Get participants from from_year event
        $stmt = $this->pdo->prepare("
            SELECT DISTINCT cyclist_id FROM results WHERE event_id = ?
        ");
        $stmt->execute([$eventId]);
        $fromYearParticipants = $stmt->fetchAll(PDO::FETCH_COLUMN);

        $participantCount = count($fromYearParticipants);
        if ($participantCount < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)'
            ];
        }

        // Check how many returned to same event
        $returnedSameEvent = 0;
        if ($matchedEventId) {
            $placeholders = implode(',', array_fill(0, count($fromYearParticipants), '?'));
            $stmt = $this->pdo->prepare("
                SELECT COUNT(DISTINCT cyclist_id)
                FROM results
                WHERE event_id = ? AND cyclist_id IN ($placeholders)
            ");
            $stmt->execute(array_merge([$matchedEventId], $fromYearParticipants));
            $returnedSameEvent = (int)$stmt->fetchColumn();
        }

        // Check how many returned to series (any event)
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT r.cyclist_id)
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE e.series_id = ?
              AND YEAR(e.date) = ?
              AND r.cyclist_id IN ($placeholders)
        ");
        $stmt->execute(array_merge([$event['series_id'], $toYear], $fromYearParticipants));
        $returnedSeries = (int)$stmt->fetchColumn();

        // Check how many returned to ANY event
        $stmt = $this->pdo->prepare("
            SELECT COUNT(DISTINCT r.cyclist_id)
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE YEAR(e.date) = ?
              AND r.cyclist_id IN ($placeholders)
        ");
        $stmt->execute(array_merge([$toYear], $fromYearParticipants));
        $returnedAny = (int)$stmt->fetchColumn();

        return [
            'event_id' => $eventId,
            'event_name' => $event['name'],
            'series_name' => $event['series_name'],
            'venue_name' => $event['venue_name'],
            'from_year' => $fromYear,
            'to_year' => $toYear,
            'matched_event_id' => $matchedEventId,
            'participants_from_year' => $participantCount,
            'returned_same_event' => $returnedSameEvent,
            'returned_same_series' => $returnedSeries,
            'returned_any_event' => $returnedAny,
            'not_returned' => $participantCount - $returnedAny,
            'same_event_retention_rate' => round(100 * $returnedSameEvent / $participantCount, 1),
            'series_retention_rate' => round(100 * $returnedSeries / $participantCount, 1),
            'overall_retention_rate' => round(100 * $returnedAny / $participantCount, 1)
        ];
    }

    /**
     * Get multi-year loyal riders for an event/venue
     * Identifies riders who attend the same event year after year
     *
     * @param int $seriesId Series ID
     * @param int|null $venueId Optional venue filter
     * @param int $minYears Minimum consecutive years
     * @return array Loyalty statistics
     */
    public function getEventLoyalRiders(int $seriesId, ?int $venueId = null, int $minYears = 2): array {
        $venueClause = $venueId ? "AND e.venue_id = ?" : "";
        $params = $venueId ? [$seriesId, $venueId] : [$seriesId];

        // Find riders who attended events in this series/venue for multiple years
        $sql = "
            SELECT
                r.cyclist_id,
                GROUP_CONCAT(DISTINCT YEAR(e.date) ORDER BY YEAR(e.date)) AS years_attended,
                COUNT(DISTINCT YEAR(e.date)) AS total_years,
                MIN(YEAR(e.date)) AS first_year,
                MAX(YEAR(e.date)) AS last_year,
                COUNT(DISTINCT r.event_id) AS total_events_attended
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE e.series_id = ?
            $venueClause
            GROUP BY r.cyclist_id
            HAVING COUNT(DISTINCT YEAR(e.date)) >= ?
            ORDER BY total_years DESC, first_year ASC
        ";

        $params[] = $minYears;
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $loyalRiders = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (count($loyalRiders) < 10) {
            return [
                'suppressed' => true,
                'reason' => 'Insufficient data (GDPR minimum 10)'
            ];
        }

        // Calculate consecutive years for each rider
        foreach ($loyalRiders as &$rider) {
            $years = array_map('intval', explode(',', $rider['years_attended']));
            $rider['consecutive_years'] = $this->calculateConsecutiveYears($years);
        }

        // Aggregate statistics
        $totalLoyalRiders = count($loyalRiders);
        $avgConsecutive = array_sum(array_column($loyalRiders, 'consecutive_years')) / $totalLoyalRiders;
        $avgTotalYears = array_sum(array_column($loyalRiders, 'total_years')) / $totalLoyalRiders;
        $maxConsecutive = max(array_column($loyalRiders, 'consecutive_years'));

        // Check how many are "single-event loyalists" (only attend one event in series per year)
        $singleEventLoyalists = 0;
        foreach ($loyalRiders as $rider) {
            // Rider attends same number of events as years = single event per year
            if ($rider['total_events_attended'] == $rider['total_years']) {
                $singleEventLoyalists++;
            }
        }

        return [
            'series_id' => $seriesId,
            'venue_id' => $venueId,
            'min_years' => $minYears,
            'total_loyal_riders' => $totalLoyalRiders,
            'avg_consecutive_years' => round($avgConsecutive, 1),
            'avg_total_years' => round($avgTotalYears, 1),
            'max_consecutive_years' => $maxConsecutive,
            'single_event_loyalists' => $singleEventLoyalists,
            'single_event_loyalist_pct' => round(100 * $singleEventLoyalists / $totalLoyalRiders, 1),
            'riders' => array_slice($loyalRiders, 0, 100) // Limit for privacy
        ];
    }

    /**
     * Calculate maximum consecutive years from a list of years
     */
    private function calculateConsecutiveYears(array $years): int {
        if (empty($years)) return 0;

        sort($years);
        $maxConsecutive = 1;
        $currentConsecutive = 1;

        for ($i = 1; $i < count($years); $i++) {
            if ($years[$i] == $years[$i-1] + 1) {
                $currentConsecutive++;
                $maxConsecutive = max($maxConsecutive, $currentConsecutive);
            } else {
                $currentConsecutive = 1;
            }
        }

        return $maxConsecutive;
    }

    /**
     * Get available series for event participation analysis
     *
     * @param array|null $brandIds Optional brand filter
     * @return array Series with event counts
     */
    public function getAvailableSeriesForEventAnalysis(?array $brandIds = null): array {
        $brandFilter = $this->buildSeriesBrandFilter($brandIds);

        $sql = "
            SELECT
                s.id,
                s.name,
                COUNT(DISTINCT e.id) AS event_count,
                COUNT(DISTINCT YEAR(e.date)) AS year_count,
                MIN(YEAR(e.date)) AS first_year,
                MAX(YEAR(e.date)) AS last_year,
                COUNT(DISTINCT r.cyclist_id) AS total_participants
            FROM series s
            JOIN events e ON e.series_id = s.id
            {$brandFilter['join']}
            LEFT JOIN results r ON r.event_id = e.id
            WHERE e.date IS NOT NULL
            " . ($brandFilter['clause'] ? str_replace('AND bsm.', 'AND bsm.', $brandFilter['clause']) : "") . "
            GROUP BY s.id, s.name
            HAVING event_count >= 2 AND total_participants >= 10
            ORDER BY total_participants DESC
        ";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($brandFilter['params']);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Get available years for a series
     *
     * @param int $seriesId Series ID
     * @return array Years with event/participant counts
     */
    public function getAvailableYearsForSeries(int $seriesId): array {
        $stmt = $this->pdo->prepare("
            SELECT
                YEAR(e.date) AS year,
                COUNT(DISTINCT e.id) AS event_count,
                COUNT(DISTINCT r.cyclist_id) AS participant_count
            FROM events e
            LEFT JOIN results r ON r.event_id = e.id
            WHERE e.series_id = ? AND e.date IS NOT NULL
            GROUP BY YEAR(e.date)
            HAVING participant_count >= 10
            ORDER BY year DESC
        ");
        $stmt->execute([$seriesId]);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    /**
     * Get series-level retention overview
     * Compares retention across events in a series
     *
     * @param int $seriesId Series ID
     * @param int $fromYear From year
     * @param int $toYear To year
     * @param array|null $brandIds Optional brand filter
     * @return array Per-event retention comparison
     */
    public function getSeriesEventRetentionComparison(int $seriesId, int $fromYear, int $toYear, ?array $brandIds = null): array {
        $brandFilter = $this->buildSeriesBrandFilter($brandIds);

        // Get all events in from_year for this series
        $sql = "
            SELECT e.id, e.name, e.date, e.venue_id, v.name AS venue_name
            FROM events e
            LEFT JOIN venues v ON e.venue_id = v.id
            {$brandFilter['join']}
            WHERE e.series_id = ? AND YEAR(e.date) = ?
            {$brandFilter['clause']}
            ORDER BY e.date
        ";

        $params = array_merge([$seriesId, $fromYear], $brandFilter['params']);
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($events)) {
            return [
                'suppressed' => true,
                'reason' => 'No events found'
            ];
        }

        $results = [];
        foreach ($events as $event) {
            $retention = $this->getEventRetention($event['id'], $fromYear, $toYear);
            if (!isset($retention['suppressed'])) {
                $results[] = array_merge($event, [
                    'retention' => $retention
                ]);
            }
        }

        if (empty($results)) {
            return [
                'suppressed' => true,
                'reason' => 'No events with sufficient data'
            ];
        }

        // Sort by retention rate
        usort($results, function($a, $b) {
            return ($b['retention']['same_event_retention_rate'] ?? 0)
                 - ($a['retention']['same_event_retention_rate'] ?? 0);
        });

        return [
            'series_id' => $seriesId,
            'from_year' => $fromYear,
            'to_year' => $toYear,
            'events' => $results,
            'brand_filter' => $brandIds
        ];
    }
}
