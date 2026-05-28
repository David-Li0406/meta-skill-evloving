<?php
/**
 * Global Sponsor Manager
 * Hanterar globala sponsorplaceringar och rättigheter
 * 
 * @package TheHUB
 * @subpackage Sponsors
 */

class GlobalSponsorManager {
    
    private $db;
    
    public function __construct($db) {
        $this->db = $db;
    }
    
    /**
     * Hämta sponsorer för en specifik plats på en sida
     * 
     * @param string $page_type 'home', 'results', 'series_list', etc
     * @param string $position 'header_banner', 'sidebar_top', etc
     * @param int $limit Max antal sponsorer att visa
     * @return array Array av sponsorer
     */
    public function getSponsorsForPlacement($page_type, $position, $limit = 5) {
        $sql = "SELECT 
                    s.id,
                    s.name,
                    s.logo,
                    s.logo_dark,
                    s.website,
                    s.tier,
                    s.banner_image,
                    sp.position,
                    sp.display_order,
                    sp.clicks,
                    sp.impressions_current,
                    sp.impressions_target
                FROM sponsors s
                INNER JOIN sponsor_placements sp ON s.id = sp.sponsor_id
                WHERE sp.page_type IN (?, 'all')
                AND sp.position = ?
                AND sp.is_active = 1
                AND s.active = 1
                AND (sp.start_date IS NULL OR sp.start_date <= CURDATE())
                AND (sp.end_date IS NULL OR sp.end_date >= CURDATE())
                AND (sp.impressions_target IS NULL OR sp.impressions_current < sp.impressions_target)
                ORDER BY 
                    s.display_priority DESC,
                    sp.display_order ASC,
                    RAND()
                LIMIT ?";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('ssi', $page_type, $position, $limit);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $sponsors = [];
        while ($row = $result->fetch_assoc()) {
            $sponsors[] = $row;
        }
        
        return $sponsors;
    }
    
    /**
     * Hämta titelsponsor för GravitySeries
     */
    public function getTitleSponsor() {
        $sql = "SELECT * FROM sponsors 
                WHERE tier = 'title_gravityseries' 
                AND active = 1 
                AND is_global = 1
                ORDER BY display_priority DESC
                LIMIT 1";
        
        $result = $this->db->query($sql);
        return $result->fetch_assoc();
    }
    
    /**
     * Hämta titelsponsor för en specifik serie
     */
    public function getSeriesTitleSponsor($series_id) {
        $sql = "SELECT s.* 
                FROM sponsors s
                INNER JOIN series_sponsors ss ON s.id = ss.sponsor_id
                WHERE ss.series_id = ?
                AND s.tier = 'title_series'
                AND s.active = 1
                ORDER BY s.display_priority DESC
                LIMIT 1";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $series_id);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }
    
    /**
     * Registrera impression (visning) av sponsor
     */
    public function trackImpression($sponsor_id, $placement_id, $page_type, $page_id = null) {
        // Uppdatera räknare i sponsor_placements
        $sql = "UPDATE sponsor_placements 
                SET impressions_current = impressions_current + 1 
                WHERE id = ?";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $placement_id);
        $stmt->execute();
        
        // Logga i analytics om aktiverat
        if ($this->isAnalyticsEnabled()) {
            $this->logAnalytics($sponsor_id, $placement_id, 'impression', $page_type, $page_id);
        }
    }
    
    /**
     * Registrera klick på sponsor
     */
    public function trackClick($sponsor_id, $placement_id, $page_type, $page_id = null) {
        // Uppdatera klick-räknare
        $sql = "UPDATE sponsor_placements 
                SET clicks = clicks + 1 
                WHERE id = ?";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $placement_id);
        $stmt->execute();
        
        // Logga i analytics
        if ($this->isAnalyticsEnabled()) {
            $this->logAnalytics($sponsor_id, $placement_id, 'click', $page_type, $page_id);
        }
    }
    
    /**
     * Logga analytics-händelse
     */
    private function logAnalytics($sponsor_id, $placement_id, $action_type, $page_type, $page_id) {
        $ip_hash = hash('sha256', $_SERVER['REMOTE_ADDR'] ?? '');
        $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? '';
        $referer = $_SERVER['HTTP_REFERER'] ?? '';
        $session_id = session_id();
        $user_id = $_SESSION['rider_id'] ?? null;
        
        $sql = "INSERT INTO sponsor_analytics 
                (sponsor_id, placement_id, page_type, page_id, action_type, 
                 user_id, ip_hash, user_agent, referer, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param(
            'iisisssss',
            $sponsor_id,
            $placement_id,
            $page_type,
            $page_id,
            $action_type,
            $user_id,
            $ip_hash,
            $user_agent,
            $referer,
            $session_id
        );
        $stmt->execute();
    }
    
    /**
     * Kolla om analytics är aktiverat
     */
    private function isAnalyticsEnabled() {
        $sql = "SELECT setting_value FROM sponsor_settings 
                WHERE setting_key = 'enable_analytics'";
        $result = $this->db->query($sql);
        $row = $result->fetch_assoc();
        return ($row && $row['setting_value'] == '1');
    }
    
    /**
     * Rendera sponsor-HTML
     */
    public function renderSponsor($sponsor, $position = 'sidebar') {
        $classes = "sponsor-item sponsor-{$position} sponsor-tier-{$sponsor['tier']}";
        
        // Använd mörk logo om dark mode är aktivt
        $logo = $sponsor['logo'];
        if (isset($_COOKIE['theme']) && $_COOKIE['theme'] === 'dark' && !empty($sponsor['logo_dark'])) {
            $logo = $sponsor['logo_dark'];
        }
        
        $html = '<div class="' . $classes . '" data-sponsor-id="' . $sponsor['id'] . '">';
        
        if ($sponsor['website']) {
            $html .= '<a href="' . htmlspecialchars($sponsor['website']) . '" 
                         target="_blank" 
                         rel="noopener sponsored"
                         class="sponsor-link"
                         onclick="trackSponsorClick(' . $sponsor['id'] . ')">';
        }
        
        // Använd banner för header, annars logo
        if ($position === 'header_banner' && !empty($sponsor['banner_image'])) {
            $html .= '<img src="' . htmlspecialchars($sponsor['banner_image']) . '" 
                         alt="' . htmlspecialchars($sponsor['name']) . '" 
                         class="sponsor-banner">';
        } else {
            $html .= '<img src="' . htmlspecialchars($logo) . '" 
                         alt="' . htmlspecialchars($sponsor['name']) . '" 
                         class="sponsor-logo">';
        }
        
        if ($sponsor['website']) {
            $html .= '</a>';
        }
        
        $html .= '</div>';
        
        return $html;
    }
    
    /**
     * Rendera sponsor-sektion för en sida
     */
    public function renderSection($page_type, $position, $title = 'Våra partners') {
        $sponsors = $this->getSponsorsForPlacement($page_type, $position);
        
        if (empty($sponsors)) {
            return '';
        }
        
        $html = '<section class="sponsor-section sponsor-section-' . $position . '">';
        
        if ($title && $position !== 'header_banner') {
            $html .= '<h3 class="sponsor-section-title">' . htmlspecialchars($title) . '</h3>';
        }
        
        $html .= '<div class="sponsor-grid sponsor-grid-' . $position . '">';
        
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
     * Hämta sponsorstatistik för en sponsor
     */
    public function getSponsorStats($sponsor_id, $days = 30) {
        $sql = "SELECT 
                    DATE(created_at) as date,
                    action_type,
                    COUNT(*) as count
                FROM sponsor_analytics
                WHERE sponsor_id = ?
                AND created_at >= DATE_SUB(NOW(), INTERVAL ? DAY)
                GROUP BY DATE(created_at), action_type
                ORDER BY date DESC";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('ii', $sponsor_id, $days);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $stats = [];
        while ($row = $result->fetch_assoc()) {
            $stats[] = $row;
        }
        
        return $stats;
    }
    
    /**
     * Generera sponsor-rapport för admin
     */
    public function generateReport($sponsor_id, $period = 'month') {
        $date_condition = match($period) {
            'week' => 'DATE_SUB(NOW(), INTERVAL 7 DAY)',
            'month' => 'DATE_SUB(NOW(), INTERVAL 30 DAY)',
            'quarter' => 'DATE_SUB(NOW(), INTERVAL 90 DAY)',
            'year' => 'DATE_SUB(NOW(), INTERVAL 365 DAY)',
            default => 'DATE_SUB(NOW(), INTERVAL 30 DAY)'
        };
        
        $sql = "SELECT 
                    COUNT(CASE WHEN action_type = 'impression' THEN 1 END) as total_impressions,
                    COUNT(CASE WHEN action_type = 'click' THEN 1 END) as total_clicks,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    COUNT(DISTINCT ip_hash) as unique_users,
                    (COUNT(CASE WHEN action_type = 'click' THEN 1 END) / 
                     NULLIF(COUNT(CASE WHEN action_type = 'impression' THEN 1 END), 0) * 100) as ctr
                FROM sponsor_analytics
                WHERE sponsor_id = ?
                AND created_at >= {$date_condition}";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $sponsor_id);
        $stmt->execute();
        $result = $stmt->get_result();
        
        return $result->fetch_assoc();
    }
}
