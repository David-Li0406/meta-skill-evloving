<?php
/**
 * AnalyticsConfig
 *
 * Gemensamma definitioner och konfiguration for analytics-plattformen.
 * Denna fil innehaller konstanter och helpers som anvands over hela systemet.
 *
 * KRITISKT: Alla analytics-komponenter ska anvanda dessa definitioner
 * for att sakerstalla konsekvent datahantering.
 *
 * ========================= KPI-DEFINITIONER =========================
 *
 * ACTIVE (Aktiv):
 *   Definition: En rider ar "aktiv ar Y" om rider har minst 1 registrerad
 *   start (unik event_id) under season_year=Y, oavsett serie.
 *   Metod: COUNT(DISTINCT event_id) >= ACTIVE_MIN_EVENTS
 *
 * EVENT_COUNT (Antal events):
 *   Definition: Antal unika event_id dar rider startat under aret.
 *   INTE antal heat, starter eller resultatrader.
 *
 * RETENTION_FROM_PREV (Retention fran forriga aret):
 *   Definition: Andel av riders_year_(N-1) som ocksa finns i riders_year_N.
 *   Formel: (riders i bade N och N-1) / (riders i N-1) * 100
 *   Svarar pa: "Hur manga av forra arets riders kom tillbaka?"
 *
 * RETURNING_SHARE_OF_CURRENT (Aterkommande andel av aktuellt ar):
 *   Definition: Andel av riders_year_N som ocksa fanns i riders_year_(N-1).
 *   Formel: (riders i bade N och N-1) / (riders i N) * 100
 *   Svarar pa: "Hur stor del av arets riders ar aterkommande?"
 *
 * CHURN_RATE (Churn fran forriga aret):
 *   Definition: Andel av riders_year_(N-1) som INTE finns i riders_year_N.
 *   Formel: 100 - RETENTION_FROM_PREV
 *   Svarar pa: "Hur manga av forra arets riders forsvann?"
 *
 * ROOKIE (Nyborjare):
 *   Definition: Rider vars MIN(season_year) = aktuellt ar.
 *   Rider har aldrig deltagit fore detta ar.
 *
 * @package TheHUB Analytics
 * @version 3.0
 */

class AnalyticsConfig {
    // =========================================================================
    // PLATFORM VERSION - For snapshot reproducerbarhet
    // =========================================================================

    /**
     * Aktuell plattformsversion
     * Andras vid stora andringar i berakningslogik
     */
    public const PLATFORM_VERSION = '3.0.0';

    /**
     * Aktuell berakningsversion (for backwards compat)
     */
    public const CALCULATION_VERSION = 'v3';

    // =========================================================================
    // ACTIVE DEFINITION
    // =========================================================================

    /**
     * Definition: "Active ar Y" = rider har minst N registrerade events
     * (unika event_id) under season_year=Y (oavsett serie)
     *
     * OBS: Detta ar EVENTS, inte starter/heat/resultatrader.
     */
    public const ACTIVE_MIN_EVENTS = 1;

    // =========================================================================
    // EVENT COUNT DEFINITION
    // =========================================================================

    /**
     * Definition: event_count = antal unika event_id dar rider startat
     * under aret (INTE antal heat/starter/resultatrader)
     *
     * Metod: COUNT(DISTINCT event_id)
     */
    public const EVENT_COUNT_METHOD = 'unique_events';

    // =========================================================================
    // RETENTION/CHURN DEFINITIONS - Tydligt dokumenterade
    // =========================================================================

    /**
     * RETENTION_FROM_PREV - "Classic retention"
     *
     * Numerator: riders som finns i BADE ar N och ar N-1
     * Denominator: riders som finns i ar N-1
     * Formel: (retained / prev_total) * 100
     *
     * Svarar pa: "Hur manga procent av forra arets riders kom tillbaka?"
     *
     * Implementerad i: KPICalculator::getRetentionRate()
     */
    public const RETENTION_TYPE_FROM_PREV = 'retention_from_prev';

    /**
     * RETURNING_SHARE_OF_CURRENT - "Andel aterkommande"
     *
     * Numerator: riders som finns i BADE ar N och ar N-1
     * Denominator: riders som finns i ar N
     * Formel: (retained / current_total) * 100
     *
     * Svarar pa: "Hur stor andel av arets deltagare ar aterkommande?"
     *
     * Implementerad i: KPICalculator::getReturningShareOfCurrent()
     */
    public const RETENTION_TYPE_RETURNING_SHARE = 'returning_share_of_current';

    // =========================================================================
    // CHURN DEFINITIONS
    // =========================================================================

    /**
     * Soft churn: 1 ar inaktiv
     * Medium churn: 2 ar inaktiv
     * Hard churn: 3+ ar inaktiv
     */
    public const SOFT_CHURN_YEARS = 1;
    public const MEDIUM_CHURN_YEARS = 2;
    public const HARD_CHURN_YEARS = 3;

    // =========================================================================
    // CLASS RANKING - Konfigurerbar klass-hierarki
    // =========================================================================

    /**
     * Klass-ranking per sasong for att avgora upgrade/downgrade
     * Hogre rank = hogre niva (Elite ar hogst)
     *
     * OBS: SCF kan andra klasser mellan ar, sa detta maste justeras arligen
     *
     * @var array<int, array<string, int>>
     */
    public const CLASS_RANKING_BY_YEAR = [
        // Default ranking (anvands om specifikt ar saknas)
        'default' => [
            // Elite/Pro
            'Elite' => 100,
            'Elite Herr' => 100,
            'Elite Dam' => 100,
            'Pro' => 95,

            // Senior
            'Senior' => 80,
            'Senior Herr' => 80,
            'Senior Dam' => 80,
            'Open' => 75,

            // Master
            'Master 40+' => 70,
            'Master 50+' => 70,
            'Master' => 70,
            'Veteran' => 65,

            // Junior/U-klasser
            'Junior' => 60,
            'U21' => 55,
            'U19' => 50,
            'U17' => 45,
            'U15' => 40,

            // Sport/Motion
            'Sport' => 30,
            'Motion' => 25,
            'Hobby' => 20,
            'Nybörjare' => 15,

            // Fun/Kids
            'Fun' => 10,
            'Kids' => 5,
        ],

        // Specifika ar kan ha andra definitioner
        2025 => [
            // Inherit from default, override as needed
        ],
        2026 => [
            // Inherit from default, override as needed
        ],
    ];

    /**
     * Hamta klass-ranking for ett specifikt ar
     *
     * @param int $year Sasong
     * @return array<string, int> Klass => Rank mapping
     */
    public static function getClassRanking(int $year): array {
        if (isset(self::CLASS_RANKING_BY_YEAR[$year])) {
            return array_merge(
                self::CLASS_RANKING_BY_YEAR['default'],
                self::CLASS_RANKING_BY_YEAR[$year]
            );
        }
        return self::CLASS_RANKING_BY_YEAR['default'];
    }

    /**
     * Hamta rank for en specifik klass
     *
     * FALLBACK-LOGIK (for okanda klasser):
     * - Om klass inte finns i ranking, returnera null
     * - At-Risk berakningar IGNORERAR class_downgrade for okanda klasser
     * - Detta forhindrar falska "downgrades" nar SCF andrar klasser
     *
     * @param string $className Klassnamn
     * @param int $year Sasong
     * @return int|null Rank eller null om okand klass
     */
    public static function getClassRank(string $className, int $year): ?int {
        $ranking = self::getClassRanking($year);

        // Exakt match
        if (isset($ranking[$className])) {
            return $ranking[$className];
        }

        // Fuzzy match (case-insensitive)
        $classNameLower = strtolower(trim($className));
        foreach ($ranking as $name => $rank) {
            if (strtolower($name) === $classNameLower) {
                return $rank;
            }
        }

        // VIKTIGT: Returnera null for okanda klasser
        // At-Risk berakningar ska ignorera class_downgrade for dessa
        return null;
    }

    /**
     * Kolla om en klassandring ar en "downgrade"
     *
     * Returnerar false om nagon av klasserna ar okand (null rank)
     * Detta forhindrar falska downgrades nar SCF andrar klassnamn.
     *
     * @param string $fromClass Ursprungsklass
     * @param string $toClass Ny klass
     * @param int $fromYear Ursprungsar
     * @param int $toYear Nytt ar
     * @return bool|null True=downgrade, False=upgrade/same, Null=okand
     */
    public static function isClassDowngrade(
        string $fromClass,
        string $toClass,
        int $fromYear,
        int $toYear
    ): ?bool {
        $fromRank = self::getClassRank($fromClass, $fromYear);
        $toRank = self::getClassRank($toClass, $toYear);

        // Om nagon klass ar okand, ignorera (returnera null)
        if ($fromRank === null || $toRank === null) {
            return null;
        }

        // Lagre rank = downgrade
        return $toRank < $fromRank;
    }

    // =========================================================================
    // RISK FACTORS - Konfigurerbara vikter for At-Risk
    // =========================================================================

    /**
     * Riskfaktorer med vikter for churn-prediktion
     * Totalt = 100 poang max
     */
    public const RISK_FACTORS = [
        'declining_events' => [
            'weight' => 30,
            'description' => 'Minskande antal starter jamfort med tidigare ar',
            'enabled' => true,
        ],
        'no_recent_activity' => [
            'weight' => 25,
            'description' => 'Ingen aktivitet efter sasongens cutoff-datum',
            'enabled' => true,
        ],
        'class_downgrade' => [
            'weight' => 15,
            'description' => 'Har gatt ner i klass',
            'enabled' => true,
        ],
        'single_series' => [
            'weight' => 10,
            'description' => 'Deltar endast i en serie',
            'enabled' => true,
        ],
        'low_tenure' => [
            'weight' => 10,
            'description' => 'Kort karriar (1-2 sasonger)',
            'enabled' => true,
        ],
        'high_age_in_class' => [
            'weight' => 10,
            'description' => 'Hog alder i sin klass',
            'enabled' => true, // Kan disables om birth_year saknas
        ],
    ];

    /**
     * Hamta aktiva riskfaktorer
     *
     * @return array<string, array> Aktiva faktorer
     */
    public static function getActiveRiskFactors(): array {
        return array_filter(self::RISK_FACTORS, fn($f) => $f['enabled']);
    }

    /**
     * Hamta total vikt for aktiva faktorer
     *
     * @return int Total vikt
     */
    public static function getTotalRiskWeight(): int {
        $total = 0;
        foreach (self::getActiveRiskFactors() as $factor) {
            $total += $factor['weight'];
        }
        return $total;
    }

    // =========================================================================
    // SEASON ACTIVITY CUTOFF - For "ingen aktivitet" berakning
    // =========================================================================

    /**
     * Default cutoff-datum for "ingen aktivitet" berakning
     * Efter detta datum raknas rider som potentiellt inaktiv for aret
     */
    public const DEFAULT_SEASON_CUTOFF_MONTH = 7;  // Juli
    public const DEFAULT_SEASON_CUTOFF_DAY = 1;

    /**
     * Serie-specifika cutoff-datum (om serien slutar tidigare/senare)
     * Overrider default cutoff for specifika serier
     */
    public const SERIES_CUTOFF_OVERRIDES = [
        // Format: series_id => ['month' => X, 'day' => Y]
        // Lagg till serier som har annorlunda sasongslut
    ];

    /**
     * Anvand dynamisk cutoff baserat pa seriens last_event_date?
     * Om true, anvands MAX(last_event_date) fran series_participation
     * istallet for statiskt cutoff-datum.
     */
    public const USE_DYNAMIC_SERIES_CUTOFF = true;

    /**
     * Cache for dynamiska cutoff-datum
     * @var array<string, string>
     */
    private static array $dynamicCutoffCache = [];

    /**
     * Hamta cutoff-datum for aktivitetsberakning
     *
     * Prioritetsordning:
     * 1. Serie-specifik override (SERIES_CUTOFF_OVERRIDES)
     * 2. Dynamiskt fran last_event_date (om USE_DYNAMIC_SERIES_CUTOFF)
     * 3. Default cutoff
     *
     * @param int $year Sasong
     * @param int|null $seriesId Serie (optional)
     * @param PDO|null $pdo Databasanslutning (for dynamisk cutoff)
     * @return string Datum (Y-m-d format)
     */
    public static function getSeasonActivityCutoffDate(
        int $year,
        ?int $seriesId = null,
        ?PDO $pdo = null
    ): string {
        // 1. Kolla serie-specifik override forst
        if ($seriesId && isset(self::SERIES_CUTOFF_OVERRIDES[$seriesId])) {
            $override = self::SERIES_CUTOFF_OVERRIDES[$seriesId];
            return sprintf('%d-%02d-%02d', $year, $override['month'], $override['day']);
        }

        // 2. Dynamisk cutoff baserat pa seriens faktiska last_event_date
        if (self::USE_DYNAMIC_SERIES_CUTOFF && $seriesId && $pdo) {
            $cacheKey = "{$year}_{$seriesId}";
            if (!isset(self::$dynamicCutoffCache[$cacheKey])) {
                $stmt = $pdo->prepare("
                    SELECT MAX(last_event_date) as cutoff
                    FROM series_participation
                    WHERE series_id = ? AND season_year = ?
                ");
                $stmt->execute([$seriesId, $year]);
                $result = $stmt->fetchColumn();

                if ($result) {
                    // Lagg till 14 dagar efter sista event som cutoff
                    $cutoffDate = date('Y-m-d', strtotime($result . ' +14 days'));
                    self::$dynamicCutoffCache[$cacheKey] = $cutoffDate;
                }
            }

            if (isset(self::$dynamicCutoffCache[$cacheKey])) {
                return self::$dynamicCutoffCache[$cacheKey];
            }
        }

        // 3. Default cutoff
        return sprintf('%d-%02d-%02d', $year, self::DEFAULT_SEASON_CUTOFF_MONTH, self::DEFAULT_SEASON_CUTOFF_DAY);
    }

    /**
     * Rensa dynamisk cutoff-cache
     */
    public static function clearCutoffCache(): void {
        self::$dynamicCutoffCache = [];
    }

    // =========================================================================
    // COHORT DEFINITIONS
    // =========================================================================

    /**
     * Cohort year = MIN(season_year) per canonical rider
     * Detta ar aret da en rider forst deltog i tavlingar
     */
    public const COHORT_MIN_SIZE = 10; // Minsta antal riders for att visa kohort
    public const COHORT_MAX_DISPLAY_YEARS = 10; // Max antal ar att visa i trend

    // =========================================================================
    // GEOGRAPHIC DEFINITIONS
    // =========================================================================

    /**
     * Region mapping for Sverige (lan)
     * Anvands for geografisk analys
     */
    public const SWEDISH_REGIONS = [
        'Stockholm' => ['code' => 'AB', 'population' => 2415139],
        'Uppsala' => ['code' => 'C', 'population' => 395026],
        'Sodermanland' => ['code' => 'D', 'population' => 301542],
        'Ostergotland' => ['code' => 'E', 'population' => 468339],
        'Jonkoping' => ['code' => 'F', 'population' => 366479],
        'Kronoberg' => ['code' => 'G', 'population' => 203527],
        'Kalmar' => ['code' => 'H', 'population' => 246641],
        'Gotland' => ['code' => 'I', 'population' => 60124],
        'Blekinge' => ['code' => 'K', 'population' => 159606],
        'Skane' => ['code' => 'M', 'population' => 1402425],
        'Halland' => ['code' => 'N', 'population' => 340243],
        'Vastra Gotaland' => ['code' => 'O', 'population' => 1751166],
        'Varmland' => ['code' => 'S', 'population' => 282414],
        'Orebro' => ['code' => 'T', 'population' => 305792],
        'Vastmanland' => ['code' => 'U', 'population' => 277052],
        'Dalarna' => ['code' => 'W', 'population' => 286547],
        'Gavleborg' => ['code' => 'X', 'population' => 286547],
        'Vasternorrland' => ['code' => 'Y', 'population' => 245572],
        'Jamtland' => ['code' => 'Z', 'population' => 131830],
        'Vasterbotten' => ['code' => 'AC', 'population' => 274153],
        'Norrbotten' => ['code' => 'BD', 'population' => 250497],
    ];

    /**
     * Hamta region fran ortnamn (enkel matching)
     *
     * @param string $city Ortnamn
     * @return string|null Region eller null om okand
     */
    public static function getRegionFromCity(string $city): ?string {
        // Enkel mapping baserad pa stad
        $cityRegionMap = [
            // Stockholm-regionen
            'stockholm' => 'Stockholm',
            'solna' => 'Stockholm',
            'nacka' => 'Stockholm',
            'taby' => 'Stockholm',
            'sollentuna' => 'Stockholm',

            // Goteborg-regionen
            'goteborg' => 'Vastra Gotaland',
            'molndal' => 'Vastra Gotaland',
            'partille' => 'Vastra Gotaland',

            // Malmo-regionen
            'malmo' => 'Skane',
            'lund' => 'Skane',
            'helsingborg' => 'Skane',

            // Add more as needed...
        ];

        $cityLower = strtolower(trim($city));
        return $cityRegionMap[$cityLower] ?? null;
    }

    // =========================================================================
    // SIMILAR RIDERS HEURISTICS
    // =========================================================================

    /**
     * Konfiguration for "Similar Riders" matchning
     */
    public const SIMILAR_RIDERS_CONFIG = [
        'tenure_buckets' => [
            [1, 2, 'new'],       // 1-2 sasonger = new
            [3, 5, 'established'], // 3-5 sasonger = established
            [6, 99, 'veteran'],  // 6+ sasonger = veteran
        ],
        'event_count_buckets' => [
            [1, 3, 'casual'],    // 1-3 events = casual
            [4, 10, 'regular'],  // 4-10 events = regular
            [11, 99, 'active'],  // 11+ events = active
        ],
        'match_weights' => [
            'start_year' => 20,      // Samma startår
            'discipline' => 25,       // Samma primary discipline
            'tenure_bucket' => 20,    // Samma tenure bucket
            'event_bucket' => 15,     // Samma event count bucket
            'series_overlap' => 20,   // Samma serier
        ],
    ];

    // =========================================================================
    // FEATURE FLAGS
    // =========================================================================

    /**
     * Feature flags for att sla av/pa funktionalitet
     * Anvands nar data saknas eller ar otillracklig
     */
    private static array $featureFlags = [
        'high_age_in_class' => true,
        'no_recent_activity' => true,
        'geographic_analysis' => true,
    ];

    /**
     * Satt feature flag
     *
     * @param string $flag Flag-namn
     * @param bool $enabled Aktiverad
     */
    public static function setFeatureFlag(string $flag, bool $enabled): void {
        self::$featureFlags[$flag] = $enabled;
    }

    /**
     * Kolla om feature ar aktiverad
     *
     * @param string $flag Flag-namn
     * @return bool
     */
    public static function isFeatureEnabled(string $flag): bool {
        return self::$featureFlags[$flag] ?? false;
    }

    /**
     * Hamta alla feature flags
     *
     * @return array<string, bool>
     */
    public static function getFeatureFlags(): array {
        return self::$featureFlags;
    }

    // =========================================================================
    // DATA QUALITY THRESHOLDS
    // =========================================================================

    /**
     * Troskel for datakvalitet - under dessa varanden disables features
     */
    public const DATA_QUALITY_THRESHOLDS = [
        'birth_year_coverage' => 0.5,  // 50% av riders maste ha birth_year
        'club_coverage' => 0.3,        // 30% av riders maste ha club
        'event_date_coverage' => 0.9,  // 90% av events maste ha datum
        'class_coverage' => 0.7,       // 70% av results maste ha klass
        'region_coverage' => 0.3,      // 30% av riders maste ha region
    ];

    // =========================================================================
    // BRAND/SERIES GROUP DEFINITIONS
    // =========================================================================

    /**
     * Varumarkes-mappning for cohort-filtrering
     * Mappar brand_id till series_ids
     *
     * OBS: Utoka denna med faktiska brand-serie mappningar
     */
    public const BRAND_SERIES_MAP = [
        // Format: brand_id => [series_id1, series_id2, ...]
        // Exempel:
        // 1 => [1, 2, 3], // GES brand -> GES series
        // 2 => [4, 5],    // Swedish Enduro Series
    ];

    /**
     * Hamta series_ids for ett brand
     */
    public static function getSeriesForBrand(int $brandId): array {
        return self::BRAND_SERIES_MAP[$brandId] ?? [];
    }
}
