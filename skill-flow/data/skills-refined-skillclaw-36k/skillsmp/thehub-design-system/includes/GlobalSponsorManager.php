<?php
/**
 * Global Sponsor Manager
 * Hanterar globala sponsorplaceringar och rättigheter
 *
 * @package TheHUB
 * @subpackage Sponsors
 */

class GlobalSponsorManager {

    private $pdo;

    public function __construct($pdo = null) {
        if ($pdo) {
            $this->pdo = $pdo;
        } else {
            global $pdo;
            $this->pdo = $pdo;
        }
    }

    /**
     * Kolla om globala sponsorer är aktiverade för publika sidor
     */
    public function isPublicEnabled(): bool {
        try {
            $stmt = $this->pdo->query("SELECT setting_value FROM sponsor_settings WHERE setting_key = 'public_enabled'");
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            return ($row && $row['setting_value'] == '1');
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Hämta sponsorer för en specifik plats på en sida
     *
     * @param string $page_type 'home', 'results', 'series_list', etc
     * @param string $position 'header_banner', 'sidebar_top', etc
     * @param int $limit Max antal sponsorer att visa
     * @return array Array av sponsorer
     */
    public function getSponsorsForPlacement(string $page_type, string $position, int $limit = 5): array {
        try {
            $sql = "SELECT
                        s.id,
                        s.name,
                        s.logo,
                        s.logo_dark,
                        s.website,
                        s.tier,
                        COALESCE(mb.filepath, s.banner_image) as banner_image,
                        sp.id as placement_id,
                        sp.position,
                        sp.display_order,
                        sp.clicks,
                        sp.impressions_current,
                        sp.impressions_target,
                        m.filepath as logo_url
                    FROM sponsors s
                    INNER JOIN sponsor_placements sp ON s.id = sp.sponsor_id
                    LEFT JOIN media m ON s.logo_media_id = m.id
                    LEFT JOIN media mb ON s.logo_banner_id = mb.id
                    WHERE sp.page_type IN (:page_type, 'all')
                    AND sp.position = :position
                    AND sp.is_active = 1
                    AND s.active = 1
                    AND (sp.start_date IS NULL OR sp.start_date <= CURDATE())
                    AND (sp.end_date IS NULL OR sp.end_date >= CURDATE())
                    AND (sp.impressions_target IS NULL OR sp.impressions_current < sp.impressions_target)
                    ORDER BY
                        s.display_priority DESC,
                        sp.display_order ASC,
                        RAND()
                    LIMIT :limit";

            $stmt = $this->pdo->prepare($sql);
            $stmt->bindValue(':page_type', $page_type, PDO::PARAM_STR);
            $stmt->bindValue(':position', $position, PDO::PARAM_STR);
            $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            error_log("getSponsorsForPlacement error: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Hämta titelsponsor för GravitySeries
     */
    public function getTitleSponsor(): ?array {
        try {
            $stmt = $this->pdo->prepare("
                SELECT s.*, m.filepath as logo_url
                FROM sponsors s
                LEFT JOIN media m ON s.logo_media_id = m.id
                WHERE s.tier = 'title_gravityseries'
                AND s.active = 1
                AND s.is_global = 1
                ORDER BY s.display_priority DESC
                LIMIT 1
            ");
            $stmt->execute();
            return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
        } catch (PDOException $e) {
            error_log("getTitleSponsor error: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Hämta titelsponsor för en specifik serie
     */
    public function getSeriesTitleSponsor(int $series_id): ?array {
        try {
            $stmt = $this->pdo->prepare("
                SELECT s.*, m.filepath as logo_url
                FROM sponsors s
                INNER JOIN series_sponsors ss ON s.id = ss.sponsor_id
                LEFT JOIN media m ON s.logo_media_id = m.id
                WHERE ss.series_id = :series_id
                AND s.tier = 'title_series'
                AND s.active = 1
                ORDER BY s.display_priority DESC
                LIMIT 1
            ");
            $stmt->execute([':series_id' => $series_id]);
            return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
        } catch (PDOException $e) {
            error_log("getSeriesTitleSponsor error: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Registrera impression (visning) av sponsor
     */
    public function trackImpression(int $sponsor_id, ?int $placement_id, string $page_type, ?int $page_id = null): void {
        try {
            // Uppdatera räknare i sponsor_placements
            if ($placement_id) {
                $stmt = $this->pdo->prepare("
                    UPDATE sponsor_placements
                    SET impressions_current = impressions_current + 1
                    WHERE id = :id
                ");
                $stmt->execute([':id' => $placement_id]);
            }

            // Logga i analytics om aktiverat
            if ($this->isAnalyticsEnabled()) {
                $this->logAnalytics($sponsor_id, $placement_id, 'impression', $page_type, $page_id);
            }
        } catch (PDOException $e) {
            error_log("trackImpression error: " . $e->getMessage());
        }
    }

    /**
     * Registrera klick på sponsor
     */
    public function trackClick(int $sponsor_id, ?int $placement_id, string $page_type, ?int $page_id = null): void {
        try {
            // Uppdatera klick-räknare
            if ($placement_id) {
                $stmt = $this->pdo->prepare("
                    UPDATE sponsor_placements
                    SET clicks = clicks + 1
                    WHERE id = :id
                ");
                $stmt->execute([':id' => $placement_id]);
            }

            // Logga i analytics
            if ($this->isAnalyticsEnabled()) {
                $this->logAnalytics($sponsor_id, $placement_id, 'click', $page_type, $page_id);
            }
        } catch (PDOException $e) {
            error_log("trackClick error: " . $e->getMessage());
        }
    }

    /**
     * Logga analytics-händelse
     */
    private function logAnalytics(int $sponsor_id, ?int $placement_id, string $action_type, string $page_type, ?int $page_id): void {
        try {
            $ip_hash = hash('sha256', $_SERVER['REMOTE_ADDR'] ?? '');
            $user_agent = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 500);
            $referer = substr($_SERVER['HTTP_REFERER'] ?? '', 0, 255);
            $session_id = session_id();
            $user_id = $_SESSION['rider_id'] ?? null;

            $stmt = $this->pdo->prepare("
                INSERT INTO sponsor_analytics
                (sponsor_id, placement_id, page_type, page_id, action_type,
                 user_id, ip_hash, user_agent, referer, session_id)
                VALUES (:sponsor_id, :placement_id, :page_type, :page_id, :action_type,
                        :user_id, :ip_hash, :user_agent, :referer, :session_id)
            ");

            $stmt->execute([
                ':sponsor_id' => $sponsor_id,
                ':placement_id' => $placement_id,
                ':page_type' => $page_type,
                ':page_id' => $page_id,
                ':action_type' => $action_type,
                ':user_id' => $user_id,
                ':ip_hash' => $ip_hash,
                ':user_agent' => $user_agent,
                ':referer' => $referer,
                ':session_id' => $session_id
            ]);
        } catch (PDOException $e) {
            error_log("logAnalytics error: " . $e->getMessage());
        }
    }

    /**
     * Kolla om analytics är aktiverat
     */
    private function isAnalyticsEnabled(): bool {
        try {
            $stmt = $this->pdo->query("SELECT setting_value FROM sponsor_settings WHERE setting_key = 'enable_analytics'");
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            return ($row && $row['setting_value'] == '1');
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Rendera sponsor-HTML
     */
    public function renderSponsor(array $sponsor, string $position = 'sidebar'): string {
        $tier = htmlspecialchars($sponsor['tier'] ?? 'silver');
        $classes = "sponsor-item sponsor-{$position} sponsor-tier-{$tier}";

        // Använd logo_url om den finns, annars logo
        $logo = $sponsor['logo_url'] ?? $sponsor['logo'] ?? '';
        if ($logo) {
            $logo = '/' . ltrim($logo, '/');
        }

        $html = '<div class="' . $classes . '" data-sponsor-id="' . intval($sponsor['id']) . '">';

        if (!empty($sponsor['website'])) {
            $html .= '<a href="' . htmlspecialchars($sponsor['website']) . '"
                         target="_blank"
                         rel="noopener sponsored"
                         class="sponsor-link"
                         onclick="trackSponsorClick(' . intval($sponsor['id']) . ', ' . intval($sponsor['placement_id'] ?? 0) . ')">';
        }

        // Använd banner för breda positioner (header_banner, header_inline, content_top, content_bottom)
        $useBanner = in_array($position, ['header_banner', 'header_inline', 'content_top', 'content_bottom', 'footer']);
        if ($useBanner && !empty($sponsor['banner_image'])) {
            $html .= '<img src="' . htmlspecialchars($sponsor['banner_image']) . '"
                         alt="' . htmlspecialchars($sponsor['name']) . '"
                         class="sponsor-banner">';
        } elseif ($logo) {
            $html .= '<img src="' . htmlspecialchars($logo) . '"
                         alt="' . htmlspecialchars($sponsor['name']) . '"
                         class="sponsor-logo">';
        } else {
            $html .= '<span class="sponsor-name">' . htmlspecialchars($sponsor['name']) . '</span>';
        }

        if (!empty($sponsor['website'])) {
            $html .= '</a>';
        }

        $html .= '</div>';

        return $html;
    }

    /**
     * Rendera sponsor-sektion för en sida
     */
    public function renderSection(string $page_type, string $position, string $title = 'Våra partners'): string {
        $sponsors = $this->getSponsorsForPlacement($page_type, $position);

        if (empty($sponsors)) {
            return '';
        }

        $html = '<section class="sponsor-section sponsor-section-' . htmlspecialchars($position) . '">';

        // Don't show title for inline header positions
        if ($title && !in_array($position, ['header_banner', 'header_inline'])) {
            $html .= '<h3 class="sponsor-section-title">' . htmlspecialchars($title) . '</h3>';
        }

        $html .= '<div class="sponsor-grid sponsor-grid-' . htmlspecialchars($position) . '">';

        foreach ($sponsors as $sponsor) {
            $html .= $this->renderSponsor($sponsor, $position);

            // Tracka impression
            if (isset($sponsor['placement_id'])) {
                $this->trackImpression(
                    $sponsor['id'],
                    $sponsor['placement_id'],
                    $page_type
                );
            }
        }

        $html .= '</div></section>';

        return $html;
    }

    /**
     * Hämta enskild placering
     */
    public function getPlacement(int $id): ?array {
        try {
            $stmt = $this->pdo->prepare("
                SELECT sp.*, s.name as sponsor_name, s.tier as sponsor_tier
                FROM sponsor_placements sp
                INNER JOIN sponsors s ON sp.sponsor_id = s.id
                WHERE sp.id = :id
            ");
            $stmt->execute([':id' => $id]);
            return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
        } catch (PDOException $e) {
            error_log("getPlacement error: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Hämta alla placeringar
     */
    public function getAllPlacements(): array {
        try {
            $stmt = $this->pdo->query("
                SELECT sp.*, s.name as sponsor_name, s.tier as sponsor_tier
                FROM sponsor_placements sp
                INNER JOIN sponsors s ON sp.sponsor_id = s.id
                ORDER BY sp.page_type, sp.position, sp.display_order
            ");
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            error_log("getAllPlacements error: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Skapa ny placering
     */
    public function createPlacement(array $data): array {
        try {
            $stmt = $this->pdo->prepare("
                INSERT INTO sponsor_placements
                (sponsor_id, page_type, position, display_order, is_active, start_date, end_date, impressions_target)
                VALUES (:sponsor_id, :page_type, :position, :display_order, :is_active, :start_date, :end_date, :impressions_target)
            ");

            $stmt->execute([
                ':sponsor_id' => $data['sponsor_id'],
                ':page_type' => $data['page_type'],
                ':position' => $data['position'],
                ':display_order' => $data['display_order'] ?? 0,
                ':is_active' => $data['is_active'] ?? 1,
                ':start_date' => $data['start_date'] ?: null,
                ':end_date' => $data['end_date'] ?: null,
                ':impressions_target' => $data['impressions_target'] ?: null
            ]);

            return ['success' => true, 'id' => $this->pdo->lastInsertId()];
        } catch (PDOException $e) {
            error_log("createPlacement error: " . $e->getMessage());
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }

    /**
     * Uppdatera placering
     */
    public function updatePlacement(int $id, array $data): array {
        try {
            $stmt = $this->pdo->prepare("
                UPDATE sponsor_placements SET
                    sponsor_id = :sponsor_id,
                    page_type = :page_type,
                    position = :position,
                    display_order = :display_order,
                    is_active = :is_active,
                    start_date = :start_date,
                    end_date = :end_date,
                    impressions_target = :impressions_target
                WHERE id = :id
            ");

            $stmt->execute([
                ':id' => $id,
                ':sponsor_id' => $data['sponsor_id'],
                ':page_type' => $data['page_type'],
                ':position' => $data['position'],
                ':display_order' => $data['display_order'] ?? 0,
                ':is_active' => $data['is_active'] ?? 1,
                ':start_date' => $data['start_date'] ?: null,
                ':end_date' => $data['end_date'] ?: null,
                ':impressions_target' => $data['impressions_target'] ?: null
            ]);

            return ['success' => true];
        } catch (PDOException $e) {
            error_log("updatePlacement error: " . $e->getMessage());
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }

    /**
     * Ta bort placering
     */
    public function deletePlacement(int $id): array {
        try {
            $stmt = $this->pdo->prepare("DELETE FROM sponsor_placements WHERE id = :id");
            $stmt->execute([':id' => $id]);
            return ['success' => true];
        } catch (PDOException $e) {
            error_log("deletePlacement error: " . $e->getMessage());
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }

    /**
     * Hämta sponsorstatistik för en sponsor
     */
    public function getSponsorStats(int $sponsor_id, int $days = 30): array {
        try {
            $stmt = $this->pdo->prepare("
                SELECT
                    DATE(created_at) as date,
                    action_type,
                    COUNT(*) as count
                FROM sponsor_analytics
                WHERE sponsor_id = :sponsor_id
                AND created_at >= DATE_SUB(NOW(), INTERVAL :days DAY)
                GROUP BY DATE(created_at), action_type
                ORDER BY date DESC
            ");
            $stmt->execute([':sponsor_id' => $sponsor_id, ':days' => $days]);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            error_log("getSponsorStats error: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Generera sponsor-rapport för admin
     */
    public function generateReport(int $sponsor_id, string $period = 'month'): ?array {
        $days = match($period) {
            'week' => 7,
            'month' => 30,
            'quarter' => 90,
            'year' => 365,
            default => 30
        };

        try {
            $stmt = $this->pdo->prepare("
                SELECT
                    COUNT(CASE WHEN action_type = 'impression' THEN 1 END) as total_impressions,
                    COUNT(CASE WHEN action_type = 'click' THEN 1 END) as total_clicks,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    COUNT(DISTINCT ip_hash) as unique_users
                FROM sponsor_analytics
                WHERE sponsor_id = :sponsor_id
                AND created_at >= DATE_SUB(NOW(), INTERVAL :days DAY)
            ");
            $stmt->execute([':sponsor_id' => $sponsor_id, ':days' => $days]);
            $result = $stmt->fetch(PDO::FETCH_ASSOC);

            // Beräkna CTR
            if ($result && $result['total_impressions'] > 0) {
                $result['ctr'] = round(($result['total_clicks'] / $result['total_impressions']) * 100, 2);
            } else {
                $result['ctr'] = 0;
            }

            return $result;
        } catch (PDOException $e) {
            error_log("generateReport error: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Hämta tier benefits
     */
    public function getTierBenefits(): array {
        try {
            $stmt = $this->pdo->query("
                SELECT * FROM sponsor_tier_benefits
                ORDER BY tier, display_order
            ");
            $benefits = $stmt->fetchAll(PDO::FETCH_ASSOC);

            // Gruppera per tier
            $grouped = [];
            foreach ($benefits as $benefit) {
                $tier = $benefit['tier'];
                if (!isset($grouped[$tier])) {
                    $grouped[$tier] = [];
                }
                $grouped[$tier][] = $benefit;
            }

            return $grouped;
        } catch (PDOException $e) {
            error_log("getTierBenefits error: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Uppdatera setting
     */
    public function updateSetting(string $key, string $value): bool {
        try {
            $stmt = $this->pdo->prepare("
                INSERT INTO sponsor_settings (setting_key, setting_value)
                VALUES (:key, :value)
                ON DUPLICATE KEY UPDATE setting_value = :value2
            ");
            $stmt->execute([':key' => $key, ':value' => $value, ':value2' => $value]);
            return true;
        } catch (PDOException $e) {
            error_log("updateSetting error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Hämta setting
     */
    public function getSetting(string $key, $default = null) {
        try {
            $stmt = $this->pdo->prepare("SELECT setting_value FROM sponsor_settings WHERE setting_key = :key");
            $stmt->execute([':key' => $key]);
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            return $row ? $row['setting_value'] : $default;
        } catch (PDOException $e) {
            return $default;
        }
    }

    /**
     * Hämta alla settings
     */
    public function getAllSettings(): array {
        try {
            $stmt = $this->pdo->query("SELECT setting_key, setting_value, description FROM sponsor_settings");
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            return [];
        }
    }
}
