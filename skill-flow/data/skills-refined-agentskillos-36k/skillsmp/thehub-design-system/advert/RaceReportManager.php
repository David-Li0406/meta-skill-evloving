<?php
/**
 * Race Report Manager
 * Hanterar race reports/blogginlägg från deltagare
 * 
 * @package TheHUB
 * @subpackage RaceReports
 */

class RaceReportManager {
    
    private $db;
    
    public function __construct($db) {
        $this->db = $db;
    }
    
    /**
     * Skapa ett nytt race report
     */
    public function createReport($data) {
        $rider_id = $data['rider_id'];
        $title = $data['title'];
        $content = $data['content'];
        $event_id = $data['event_id'] ?? null;
        $instagram_url = $data['instagram_url'] ?? null;
        $featured_image = $data['featured_image'] ?? null;
        $status = $data['status'] ?? 'draft';
        
        // Generera slug
        $slug = $this->generateSlug($title);
        
        // Generera excerpt från content
        $excerpt = $this->generateExcerpt($content);
        
        // Beräkna läs-tid
        $reading_time = $this->calculateReadingTime($content);
        
        // Kolla om Instagram-import
        $is_from_instagram = !empty($instagram_url) ? 1 : 0;
        $instagram_embed = $is_from_instagram ? $this->getInstagramEmbed($instagram_url) : null;
        
        $sql = "INSERT INTO race_reports 
                (rider_id, event_id, title, slug, content, excerpt, 
                 featured_image, status, instagram_url, instagram_embed_code, 
                 is_from_instagram, reading_time_minutes, published_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        $published_at = ($status === 'published') ? date('Y-m-d H:i:s') : null;
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param(
            'iissssssssiis',
            $rider_id,
            $event_id,
            $title,
            $slug,
            $content,
            $excerpt,
            $featured_image,
            $status,
            $instagram_url,
            $instagram_embed,
            $is_from_instagram,
            $reading_time,
            $published_at
        );
        
        if ($stmt->execute()) {
            $report_id = $stmt->insert_id;
            
            // Lägg till tags om de finns
            if (!empty($data['tags'])) {
                $this->addTags($report_id, $data['tags']);
            }
            
            return $report_id;
        }
        
        return false;
    }
    
    /**
     * Uppdatera befintligt race report
     */
    public function updateReport($report_id, $data) {
        $updates = [];
        $params = [];
        $types = '';
        
        // Bygg dynamisk UPDATE-query baserat på vad som finns i $data
        $allowed_fields = [
            'title' => 's',
            'content' => 's',
            'excerpt' => 's',
            'featured_image' => 's',
            'status' => 's',
            'event_id' => 'i',
            'instagram_url' => 's',
            'is_featured' => 'i',
            'allow_comments' => 'i'
        ];
        
        foreach ($allowed_fields as $field => $type) {
            if (isset($data[$field])) {
                $updates[] = "$field = ?";
                $params[] = $data[$field];
                $types .= $type;
            }
        }
        
        // Om status ändras till published, sätt published_at
        if (isset($data['status']) && $data['status'] === 'published') {
            $updates[] = "published_at = NOW()";
        }
        
        // Om title ändras, uppdatera slug
        if (isset($data['title'])) {
            $new_slug = $this->generateSlug($data['title'], $report_id);
            $updates[] = "slug = ?";
            $params[] = $new_slug;
            $types .= 's';
        }
        
        // Om content ändras, uppdatera reading_time
        if (isset($data['content'])) {
            $reading_time = $this->calculateReadingTime($data['content']);
            $updates[] = "reading_time_minutes = ?";
            $params[] = $reading_time;
            $types .= 'i';
        }
        
        if (empty($updates)) {
            return false;
        }
        
        $sql = "UPDATE race_reports SET " . implode(', ', $updates) . " WHERE id = ?";
        $params[] = $report_id;
        $types .= 'i';
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param($types, ...$params);
        
        return $stmt->execute();
    }
    
    /**
     * Hämta race report
     */
    public function getReport($id_or_slug) {
        $is_numeric = is_numeric($id_or_slug);
        
        $sql = "SELECT 
                    rr.*,
                    r.first_name,
                    r.last_name,
                    r.uci_id,
                    r.club_id,
                    c.name as club_name,
                    e.name as event_name,
                    e.date as event_date
                FROM race_reports rr
                INNER JOIN riders r ON rr.rider_id = r.id
                LEFT JOIN clubs c ON r.club_id = c.id
                LEFT JOIN events e ON rr.event_id = e.id
                WHERE rr." . ($is_numeric ? "id" : "slug") . " = ?
                AND rr.status = 'published'";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param($is_numeric ? 'i' : 's', $id_or_slug);
        $stmt->execute();
        $result = $stmt->get_result();
        $report = $result->fetch_assoc();
        
        if ($report) {
            // Hämta tags
            $report['tags'] = $this->getReportTags($report['id']);
            
            // Uppdatera view-räknare
            $this->incrementViews($report['id']);
        }
        
        return $report;
    }
    
    /**
     * Lista race reports med paginering och filtrering
     */
    public function listReports($filters = []) {
        $page = $filters['page'] ?? 1;
        $per_page = $filters['per_page'] ?? 12;
        $offset = ($page - 1) * $per_page;
        
        $where = ["rr.status = 'published'"];
        $params = [];
        $types = '';
        
        // Filtrering
        if (!empty($filters['rider_id'])) {
            $where[] = "rr.rider_id = ?";
            $params[] = $filters['rider_id'];
            $types .= 'i';
        }
        
        if (!empty($filters['event_id'])) {
            $where[] = "rr.event_id = ?";
            $params[] = $filters['event_id'];
            $types .= 'i';
        }
        
        if (!empty($filters['tag'])) {
            $where[] = "EXISTS (
                SELECT 1 FROM race_report_tag_relations rrtr
                INNER JOIN race_report_tags rrt ON rrtr.tag_id = rrt.id
                WHERE rrtr.report_id = rr.id
                AND rrt.slug = ?
            )";
            $params[] = $filters['tag'];
            $types .= 's';
        }
        
        if (!empty($filters['search'])) {
            $where[] = "MATCH(rr.title, rr.content, rr.excerpt) AGAINST(? IN NATURAL LANGUAGE MODE)";
            $params[] = $filters['search'];
            $types .= 's';
        }
        
        if (isset($filters['featured']) && $filters['featured']) {
            $where[] = "rr.is_featured = 1";
        }
        
        $where_clause = implode(' AND ', $where);
        
        // Sortering
        $order = match($filters['order_by'] ?? 'recent') {
            'popular' => 'rr.views DESC',
            'liked' => 'rr.likes DESC',
            'oldest' => 'rr.published_at ASC',
            default => 'rr.published_at DESC'
        };
        
        $sql = "SELECT 
                    rr.*,
                    r.first_name,
                    r.last_name,
                    r.club_id,
                    c.name as club_name,
                    e.name as event_name
                FROM race_reports rr
                INNER JOIN riders r ON rr.rider_id = r.id
                LEFT JOIN clubs c ON r.club_id = c.id
                LEFT JOIN events e ON rr.event_id = e.id
                WHERE {$where_clause}
                ORDER BY {$order}
                LIMIT ? OFFSET ?";
        
        $params[] = $per_page;
        $params[] = $offset;
        $types .= 'ii';
        
        $stmt = $this->db->prepare($sql);
        if (!empty($params)) {
            $stmt->bind_param($types, ...$params);
        }
        $stmt->execute();
        $result = $stmt->get_result();
        
        $reports = [];
        while ($row = $result->fetch_assoc()) {
            $row['tags'] = $this->getReportTags($row['id']);
            $reports[] = $row;
        }
        
        // Räkna total
        $count_sql = "SELECT COUNT(*) as total 
                      FROM race_reports rr 
                      WHERE {$where_clause}";
        $count_stmt = $this->db->prepare($count_sql);
        if (!empty($params)) {
            // Ta bort LIMIT och OFFSET parametrar
            array_pop($params);
            array_pop($params);
            $count_types = substr($types, 0, -2);
            $count_stmt->bind_param($count_types, ...$params);
        }
        $count_stmt->execute();
        $count_result = $count_stmt->get_result();
        $total = $count_result->fetch_assoc()['total'];
        
        return [
            'reports' => $reports,
            'total' => $total,
            'page' => $page,
            'per_page' => $per_page,
            'total_pages' => ceil($total / $per_page)
        ];
    }
    
    /**
     * Lägg till kommentar
     */
    public function addComment($report_id, $rider_id, $comment_text, $parent_id = null) {
        $sql = "INSERT INTO race_report_comments 
                (report_id, rider_id, comment_text, parent_comment_id)
                VALUES (?, ?, ?, ?)";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('iisi', $report_id, $rider_id, $comment_text, $parent_id);
        
        return $stmt->execute() ? $stmt->insert_id : false;
    }
    
    /**
     * Hämta kommentarer för report
     */
    public function getComments($report_id) {
        $sql = "SELECT 
                    rc.*,
                    r.first_name,
                    r.last_name,
                    r.club_id
                FROM race_report_comments rc
                LEFT JOIN riders r ON rc.rider_id = r.id
                WHERE rc.report_id = ?
                AND rc.is_approved = 1
                ORDER BY rc.created_at ASC";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $report_id);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $comments = [];
        while ($row = $result->fetch_assoc()) {
            $comments[] = $row;
        }
        
        // Bygg träd-struktur för svar
        return $this->buildCommentTree($comments);
    }
    
    /**
     * Like/Unlike report
     */
    public function toggleLike($report_id, $rider_id) {
        // Kolla om redan likat
        $check_sql = "SELECT 1 FROM race_report_likes 
                      WHERE report_id = ? AND rider_id = ?";
        $stmt = $this->db->prepare($check_sql);
        $stmt->bind_param('ii', $report_id, $rider_id);
        $stmt->execute();
        $result = $stmt->get_result();
        $already_liked = $result->num_rows > 0;
        
        if ($already_liked) {
            // Ta bort like
            $sql = "DELETE FROM race_report_likes 
                    WHERE report_id = ? AND rider_id = ?";
            $stmt = $this->db->prepare($sql);
            $stmt->bind_param('ii', $report_id, $rider_id);
            $stmt->execute();
            
            // Minska räknare
            $update_sql = "UPDATE race_reports 
                          SET likes = GREATEST(0, likes - 1) 
                          WHERE id = ?";
            $update_stmt = $this->db->prepare($update_sql);
            $update_stmt->bind_param('i', $report_id);
            $update_stmt->execute();
            
            return false; // Unliked
        } else {
            // Lägg till like
            $sql = "INSERT INTO race_report_likes (report_id, rider_id) 
                    VALUES (?, ?)";
            $stmt = $this->db->prepare($sql);
            $stmt->bind_param('ii', $report_id, $rider_id);
            $stmt->execute();
            
            // Öka räknare
            $update_sql = "UPDATE race_reports 
                          SET likes = likes + 1 
                          WHERE id = ?";
            $update_stmt = $this->db->prepare($update_sql);
            $update_stmt->bind_param('i', $report_id);
            $update_stmt->execute();
            
            return true; // Liked
        }
    }
    
    /**
     * Hjälpfunktioner
     */
    
    private function generateSlug($title, $exclude_id = null) {
        $slug = strtolower(trim($title));
        $slug = preg_replace('/[^a-z0-9-åäö]/', '-', $slug);
        $slug = preg_replace('/-+/', '-', $slug);
        $slug = trim($slug, '-');
        
        // Kolla om slug redan finns
        $original_slug = $slug;
        $counter = 1;
        
        while (true) {
            $check_sql = "SELECT id FROM race_reports WHERE slug = ?";
            if ($exclude_id) {
                $check_sql .= " AND id != ?";
            }
            
            $stmt = $this->db->prepare($check_sql);
            if ($exclude_id) {
                $stmt->bind_param('si', $slug, $exclude_id);
            } else {
                $stmt->bind_param('s', $slug);
            }
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows === 0) {
                break;
            }
            
            $slug = $original_slug . '-' . $counter;
            $counter++;
        }
        
        return $slug;
    }
    
    private function generateExcerpt($content, $length = 200) {
        $text = strip_tags($content);
        if (strlen($text) <= $length) {
            return $text;
        }
        
        return substr($text, 0, $length) . '...';
    }
    
    private function calculateReadingTime($content) {
        $words = str_word_count(strip_tags($content));
        $minutes = ceil($words / 200); // Genomsnitt 200 ord per minut
        return max(1, $minutes);
    }
    
    private function getInstagramEmbed($url) {
        // Här kan man integrera med Instagram oEmbed API
        // För nu returnerar vi bara URL:en
        return $url;
    }
    
    private function incrementViews($report_id) {
        $sql = "UPDATE race_reports SET views = views + 1 WHERE id = ?";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $report_id);
        $stmt->execute();
    }
    
    private function addTags($report_id, $tags) {
        foreach ($tags as $tag_name) {
            // Skapa tag om den inte finns
            $tag_slug = $this->generateSlug($tag_name);
            
            $sql = "INSERT INTO race_report_tags (name, slug) 
                    VALUES (?, ?) 
                    ON DUPLICATE KEY UPDATE usage_count = usage_count + 1";
            $stmt = $this->db->prepare($sql);
            $stmt->bind_param('ss', $tag_name, $tag_slug);
            $stmt->execute();
            
            $tag_id = $stmt->insert_id ?: $this->db->query(
                "SELECT id FROM race_report_tags WHERE slug = '{$tag_slug}'"
            )->fetch_assoc()['id'];
            
            // Koppla tag till report
            $rel_sql = "INSERT IGNORE INTO race_report_tag_relations (report_id, tag_id) 
                        VALUES (?, ?)";
            $rel_stmt = $this->db->prepare($rel_sql);
            $rel_stmt->bind_param('ii', $report_id, $tag_id);
            $rel_stmt->execute();
        }
    }
    
    private function getReportTags($report_id) {
        $sql = "SELECT rrt.* 
                FROM race_report_tags rrt
                INNER JOIN race_report_tag_relations rrtr ON rrt.id = rrtr.tag_id
                WHERE rrtr.report_id = ?
                ORDER BY rrt.name";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param('i', $report_id);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $tags = [];
        while ($row = $result->fetch_assoc()) {
            $tags[] = $row;
        }
        
        return $tags;
    }
    
    private function buildCommentTree($comments) {
        $tree = [];
        $lookup = [];
        
        // Bygg lookup-tabell
        foreach ($comments as $comment) {
            $comment['replies'] = [];
            $lookup[$comment['id']] = $comment;
        }
        
        // Bygg träd
        foreach ($lookup as $id => $comment) {
            if ($comment['parent_comment_id'] === null) {
                $tree[] = &$lookup[$id];
            } else {
                if (isset($lookup[$comment['parent_comment_id']])) {
                    $lookup[$comment['parent_comment_id']]['replies'][] = &$lookup[$id];
                }
            }
        }
        
        return $tree;
    }
}
