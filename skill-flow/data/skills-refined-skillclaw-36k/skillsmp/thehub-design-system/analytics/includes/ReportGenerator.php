<?php
/**
 * ReportGenerator - Samlar analytics-data för rapporter
 *
 * Genererar strukturerad data för 2-3 sidors säsongsrapport.
 *
 * @package TheHUB Analytics
 */

class ReportGenerator {
    private PDO $pdo;
    private KPICalculator $kpi;

    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
        $this->kpi = new KPICalculator($pdo);
    }

    /**
     * Generera komplett rapport för ett år
     */
    public function generateSeasonReport(int $year): array {
        return [
            'meta' => $this->getReportMeta($year),
            'overview' => $this->getOverviewSection($year),
            'journey' => $this->getJourneySection($year),
            'insights' => $this->getInsightsSection($year),
        ];
    }

    /**
     * Rapport-metadata
     */
    private function getReportMeta(int $year): array {
        return [
            'title' => "Säsongsrapport $year",
            'generated_at' => date('Y-m-d H:i'),
            'year' => $year,
            'previous_year' => $year - 1,
        ];
    }

    /**
     * SIDA 1: Säsongsöversikt
     */
    private function getOverviewSection(int $year): array {
        $prevYear = $year - 1;

        // Nyckeltal
        $totalRiders = $this->kpi->getTotalActiveRiders($year);
        $totalRidersPrev = $this->kpi->getTotalActiveRiders($prevYear);
        $newRiders = $this->kpi->getNewRidersCount($year);
        $newRidersPrev = $this->kpi->getNewRidersCount($prevYear);
        $retentionRate = $this->kpi->getRetentionRate($year);
        $retentionRatePrev = $this->kpi->getRetentionRate($prevYear);

        // Events
        $eventCount = $this->getEventCount($year);
        $eventCountPrev = $this->getEventCount($prevYear);

        // Top events
        $topEvents = $this->getTopEventsByParticipants($year, 5);

        // 5-års trend
        $trend = $this->kpi->getGrowthTrend(5);

        return [
            'kpis' => [
                'total_riders' => [
                    'value' => $totalRiders,
                    'previous' => $totalRidersPrev,
                    'change' => $this->calcChange($totalRiders, $totalRidersPrev),
                    'label' => 'Aktiva deltagare',
                ],
                'new_riders' => [
                    'value' => $newRiders,
                    'previous' => $newRidersPrev,
                    'change' => $this->calcChange($newRiders, $newRidersPrev),
                    'label' => 'Nya deltagare (rookies)',
                ],
                'retention_rate' => [
                    'value' => round($retentionRate * 100, 1),
                    'previous' => round($retentionRatePrev * 100, 1),
                    'change' => round(($retentionRate - $retentionRatePrev) * 100, 1),
                    'label' => 'Retention (%)',
                    'suffix' => '%',
                ],
                'events' => [
                    'value' => $eventCount,
                    'previous' => $eventCountPrev,
                    'change' => $this->calcChange($eventCount, $eventCountPrev),
                    'label' => 'Antal event',
                ],
            ],
            'top_events' => $topEvents,
            'trend' => $trend,
        ];
    }

    /**
     * SIDA 2: Rider Journey & Retention
     */
    private function getJourneySection(int $year): array {
        // Kohort från 2 år sedan (för att ha data på år 2+)
        $cohortYear = $year - 2;

        // Kohort-funnel
        $funnel = $this->getCohortFunnel($cohortYear);

        // Retention by starts
        $retentionByStarts = [];
        try {
            $retentionByStarts = $this->kpi->getRetentionByStartCount($cohortYear);
        } catch (Exception $e) {}

        // Klubbar med bäst retention
        $topClubsRetention = $this->getClubsByRetention($year, 5);

        // Journey patterns
        $journeyPatterns = [];
        try {
            $journeyPatterns = $this->kpi->getJourneyTypeDistribution($cohortYear);
        } catch (Exception $e) {}

        return [
            'cohort_year' => $cohortYear,
            'funnel' => $funnel,
            'retention_by_starts' => $retentionByStarts,
            'top_clubs_retention' => $topClubsRetention,
            'journey_patterns' => $journeyPatterns,
        ];
    }

    /**
     * SIDA 3: Insikter & Rekommendationer
     */
    private function getInsightsSection(int $year): array {
        // Var tappar vi folk?
        $churnAnalysis = [];
        try {
            $churnAnalysis = $this->kpi->getChurnBySegment($year);
        } catch (Exception $e) {}

        // Events som lockar rookies
        $rookieEvents = [];
        try {
            $rookieEvents = $this->kpi->getEventsWithMostRookies($year, 5);
        } catch (Exception $e) {}

        // Klubbar med flest rookies
        $rookieClubs = [];
        try {
            $rookieClubs = $this->kpi->getClubsWithMostRookies($year, 5);
        } catch (Exception $e) {}

        // Generera rekommendationer baserat på data
        $recommendations = $this->generateRecommendations($year);

        return [
            'churn_analysis' => $churnAnalysis,
            'rookie_events' => $rookieEvents,
            'rookie_clubs' => $rookieClubs,
            'recommendations' => $recommendations,
        ];
    }

    /**
     * Hämta kohort-funnel (år 1 → år 2 → år 3 → år 4)
     */
    private function getCohortFunnel(int $cohortYear): array {
        $funnel = [];

        try {
            $cohortSize = $this->kpi->getCohortSize($cohortYear);

            for ($offset = 1; $offset <= 4; $offset++) {
                $targetYear = $cohortYear + $offset - 1;
                $retention = $this->kpi->getCohortRetention($cohortYear, $targetYear);

                $activeCount = 0;
                if (!empty($retention['years'])) {
                    foreach ($retention['years'] as $yr) {
                        if ($yr['year'] == $targetYear) {
                            $activeCount = $yr['active_riders'];
                            break;
                        }
                    }
                }

                $funnel[] = [
                    'year_offset' => $offset,
                    'calendar_year' => $targetYear,
                    'active' => $activeCount,
                    'retention_pct' => $cohortSize > 0 ? round(($activeCount / $cohortSize) * 100, 1) : 0,
                ];
            }
        } catch (Exception $e) {
            // Returnera tom funnel vid fel
        }

        return $funnel;
    }

    /**
     * Hämta antal event för ett år
     */
    private function getEventCount(int $year): int {
        try {
            $stmt = $this->pdo->prepare("
                SELECT COUNT(*) FROM events
                WHERE YEAR(date) = ? AND active = 1
            ");
            $stmt->execute([$year]);
            return (int)$stmt->fetchColumn();
        } catch (Exception $e) {
            return 0;
        }
    }

    /**
     * Hämta top events efter deltagare
     */
    private function getTopEventsByParticipants(int $year, int $limit = 5): array {
        try {
            $stmt = $this->pdo->prepare("
                SELECT
                    e.id,
                    e.name,
                    e.date,
                    e.location,
                    COUNT(DISTINCT r.cyclist_id) as participants
                FROM events e
                JOIN results r ON r.event_id = e.id
                WHERE YEAR(e.date) = ?
                GROUP BY e.id
                ORDER BY participants DESC
                LIMIT ?
            ");
            $stmt->execute([$year, $limit]);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            return [];
        }
    }

    /**
     * Hämta klubbar sorterade på retention
     */
    private function getClubsByRetention(int $year, int $limit = 5): array {
        try {
            $prevYear = $year - 1;
            $stmt = $this->pdo->prepare("
                SELECT
                    c.id,
                    c.name,
                    COUNT(DISTINCT CASE WHEN rys_prev.rider_id IS NOT NULL THEN rys.rider_id END) as retained,
                    COUNT(DISTINCT rys_prev.rider_id) as prev_total,
                    ROUND(COUNT(DISTINCT CASE WHEN rys.rider_id IS NOT NULL THEN rys_prev.rider_id END) /
                          NULLIF(COUNT(DISTINCT rys_prev.rider_id), 0) * 100, 1) as retention_pct
                FROM clubs c
                JOIN rider_yearly_stats rys_prev ON rys_prev.club_id = c.id AND rys_prev.season_year = ?
                LEFT JOIN rider_yearly_stats rys ON rys.rider_id = rys_prev.rider_id AND rys.season_year = ?
                GROUP BY c.id
                HAVING prev_total >= 10
                ORDER BY retention_pct DESC
                LIMIT ?
            ");
            $stmt->execute([$prevYear, $year, $limit]);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            return [];
        }
    }

    /**
     * Generera rekommendationer baserat på data
     */
    private function generateRecommendations(int $year): array {
        $recommendations = [];

        try {
            // Kolla retention
            $retention = $this->kpi->getRetentionRate($year);
            if ($retention < 0.5) {
                $recommendations[] = [
                    'priority' => 'high',
                    'area' => 'Retention',
                    'insight' => 'Endast ' . round($retention * 100) . '% av förra årets deltagare kom tillbaka.',
                    'action' => 'Fokusera på att kontakta inaktiva deltagare tidigt på säsongen.',
                ];
            }

            // Kolla rookie-rate
            $rookieRate = $this->kpi->getRookieRate($year);
            if ($rookieRate > 0.4) {
                $recommendations[] = [
                    'priority' => 'medium',
                    'area' => 'Nyrekrytering',
                    'insight' => round($rookieRate * 100) . '% av deltagarna är nya - bra inflöde!',
                    'action' => 'Säkerställ att rookies får en bra första upplevelse.',
                ];
            }

            // Kolla churn
            $churnRate = $this->kpi->getChurnRate($year);
            if ($churnRate > 0.5) {
                $recommendations[] = [
                    'priority' => 'high',
                    'area' => 'Churn',
                    'insight' => round($churnRate * 100) . '% av förra årets deltagare försvann.',
                    'action' => 'Analysera varför deltagare slutar - skicka enkät till inaktiva.',
                ];
            }

        } catch (Exception $e) {
            // Ignorera fel, returnera det vi har
        }

        // Lägg alltid till en generell rekommendation
        if (empty($recommendations)) {
            $recommendations[] = [
                'priority' => 'info',
                'area' => 'Allmänt',
                'insight' => 'Data ser stabil ut.',
                'action' => 'Fortsätt övervaka nyckeltal regelbundet.',
            ];
        }

        return $recommendations;
    }

    /**
     * Beräkna procentuell förändring
     */
    private function calcChange($current, $previous): float {
        if ($previous == 0) return 0;
        return round((($current - $previous) / $previous) * 100, 1);
    }
}
