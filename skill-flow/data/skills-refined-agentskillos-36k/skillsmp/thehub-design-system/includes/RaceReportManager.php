<?php
/**
 * Race Report Manager
 * Hanterar race reports/blogginlägg från deltagare
 *
 * @package TheHUB
 * @subpackage RaceReports
 */

class RaceReportManager {

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
     * Kolla om race reports är aktiverade för publika sidor
     */
    public function isPublicEnabled() {
        try {
            $stmt = $this->pdo->query("SELECT setting_value FROM sponsor_settings WHERE setting_key = 'race_reports_public'");
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            return ($row && $row['setting_value'] == '1');
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Skapa ett nytt race report
     * @param array $data
     * @return int|false
     */
    public function createReport($data) {
        try {
            $rider_id = $data['rider_id'] ?? null;
            $admin_user_id = $data['admin_user_id'] ?? null;
            $title = $data['title'];
            $content = $data['content'];
            $event_id = $data['event_id'] ?? null;
            $instagram_url = $data['instagram_url'] ?? null;
            $youtube_url = $data['youtube_url'] ?? null;
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

            // Kolla om YouTube-import
            $is_from_youtube = !empty($youtube_url) ? 1 : 0;
            $youtube_video_id = $is_from_youtube ? $this->getYoutubeVideoId($youtube_url) : null;

            // Set featured image from YouTube thumbnail if not set
            if ($is_from_youtube && !$featured_image && $youtube_video_id) {
                $featured_image = "https://img.youtube.com/vi/{$youtube_video_id}/maxresdefault.jpg";
            }

            $published_at = ($status === 'published') ? date('Y-m-d H:i:s') : null;

            $stmt = $this->pdo->prepare("
                INSERT INTO race_reports
                (rider_id, admin_user_id, event_id, title, slug, content, excerpt,
                 featured_image, status, instagram_url, instagram_embed_code,
                 is_from_instagram, youtube_url, youtube_video_id, is_from_youtube,
                 reading_time_minutes, published_at)
                VALUES (:rider_id, :admin_user_id, :event_id, :title, :slug, :content, :excerpt,
                        :featured_image, :status, :instagram_url, :instagram_embed_code,
                        :is_from_instagram, :youtube_url, :youtube_video_id, :is_from_youtube,
                        :reading_time_minutes, :published_at)
            ");

            $stmt->execute([
                ':rider_id' => $rider_id,
                ':admin_user_id' => $admin_user_id,
                ':event_id' => $event_id,
                ':title' => $title,
                ':slug' => $slug,
                ':content' => $content,
                ':excerpt' => $excerpt,
                ':featured_image' => $featured_image,
                ':status' => $status,
                ':instagram_url' => $instagram_url,
                ':instagram_embed_code' => $instagram_embed,
                ':is_from_instagram' => $is_from_instagram,
                ':youtube_url' => $youtube_url,
                ':youtube_video_id' => $youtube_video_id,
                ':is_from_youtube' => $is_from_youtube,
                ':reading_time_minutes' => $reading_time,
                ':published_at' => $published_at
            ]);

            $report_id = (int)$this->pdo->lastInsertId();

            // Lägg till tags om de finns
            if (!empty($data['tags'])) {
                $this->addTags($report_id, $data['tags']);
            }

            return $report_id;
        } catch (PDOException $e) {
            error_log("createReport error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Uppdatera befintligt race report
     */
    public function updateReport($report_id, $data) {
        try {
            // Bygg dynamisk UPDATE-query baserat på vad som finns i $data
            $allowed_fields = [
                'title', 'content', 'excerpt', 'featured_image', 'status',
                'event_id', 'instagram_url', 'youtube_url', 'is_featured', 'allow_comments'
            ];

            $updates = [];
            $params = [':id' => $report_id];

            foreach ($allowed_fields as $field) {
                if (array_key_exists($field, $data)) {
                    $updates[] = "{$field} = :{$field}";
                    $params[":{$field}"] = $data[$field];
                }
            }

            // Om status ändras till published, sätt published_at
            if (isset($data['status']) && $data['status'] === 'published') {
                $updates[] = "published_at = NOW()";
            }

            // Om title ändras, uppdatera slug
            if (isset($data['title'])) {
                $new_slug = $this->generateSlug($data['title'], $report_id);
                $updates[] = "slug = :new_slug";
                $params[':new_slug'] = $new_slug;
            }

            // Om content ändras, uppdatera reading_time
            if (isset($data['content'])) {
                $reading_time = $this->calculateReadingTime($data['content']);
                $updates[] = "reading_time_minutes = :reading_time";
                $params[':reading_time'] = $reading_time;
            }

            if (empty($updates)) {
                return false;
            }

            $sql = "UPDATE race_reports SET " . implode(', ', $updates) . " WHERE id = :id";

            $stmt = $this->pdo->prepare($sql);
            return $stmt->execute($params);
        } catch (PDOException $e) {
            error_log("updateReport error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Hämta race report
     * @param string|int $id_or_slug
     * @param bool $published_only
     * @return array|null
     */
    public function getReport($id_or_slug, $published_only = true) {
        try {
            $is_numeric = is_numeric($id_or_slug);

            $sql = "SELECT
                        rr.*,
                        r.firstname,
                        r.lastname,
                        r.uci_id,
                        r.club_id,
                        c.name as club_name,
                        e.name as event_name,
                        e.date as event_date
                    FROM race_reports rr
                    LEFT JOIN riders r ON rr.rider_id = r.id
                    LEFT JOIN clubs c ON r.club_id = c.id
                    LEFT JOIN events e ON rr.event_id = e.id
                    WHERE rr." . ($is_numeric ? "id" : "slug") . " = :identifier";

            if ($published_only) {
                $sql .= " AND rr.status = 'published'";
            }

            $stmt = $this->pdo->prepare($sql);
            $stmt->execute([':identifier' => $id_or_slug]);
            $report = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($report) {
                // Hämta tags
                $report['tags'] = $this->getReportTags($report['id']);

                // Uppdatera view-räknare (endast för publicerade)
                if ($report['status'] === 'published') {
                    $this->incrementViews($report['id']);
                }
            }

            return $report ?: null;
        } catch (PDOException $e) {
            error_log("getReport error: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Lista race reports med paginering och filtrering
     */
    public function listReports($filters = array()) {
        try {
            $page = $filters['page'] ?? 1;
            $per_page = $filters['per_page'] ?? 12;
            $offset = ($page - 1) * $per_page;

            $where = [];
            $params = [];

            // Default: endast publicerade (kan överskridas för admin)
            if (!isset($filters['include_drafts']) || !$filters['include_drafts']) {
                $where[] = "rr.status = 'published'";
            }

            // Filtrering
            if (!empty($filters['rider_id'])) {
                $where[] = "rr.rider_id = :rider_id";
                $params[':rider_id'] = $filters['rider_id'];
            }

            // Admin user filter - with optional linked_rider_id for OR query
            if (!empty($filters['admin_user_id'])) {
                if (!empty($filters['linked_rider_id'])) {
                    // Admin has a linked rider account - check both with OR
                    $where[] = "(rr.admin_user_id = :admin_user_id OR rr.rider_id = :linked_rider_id)";
                    $params[':admin_user_id'] = $filters['admin_user_id'];
                    $params[':linked_rider_id'] = $filters['linked_rider_id'];
                } else {
                    $where[] = "rr.admin_user_id = :admin_user_id";
                    $params[':admin_user_id'] = $filters['admin_user_id'];
                }
            }

            if (!empty($filters['event_id'])) {
                $where[] = "rr.event_id = :event_id";
                $params[':event_id'] = $filters['event_id'];
            }

            if (!empty($filters['status'])) {
                $where[] = "rr.status = :status";
                $params[':status'] = $filters['status'];
            }

            if (!empty($filters['tag'])) {
                $where[] = "EXISTS (
                    SELECT 1 FROM race_report_tag_relations rrtr
                    INNER JOIN race_report_tags rrt ON rrtr.tag_id = rrt.id
                    WHERE rrtr.report_id = rr.id
                    AND rrt.slug = :tag
                )";
                $params[':tag'] = $filters['tag'];
            }

            if (!empty($filters['search'])) {
                $where[] = "(rr.title LIKE :search OR rr.content LIKE :search2 OR rr.excerpt LIKE :search3)";
                $searchTerm = '%' . $filters['search'] . '%';
                $params[':search'] = $searchTerm;
                $params[':search2'] = $searchTerm;
                $params[':search3'] = $searchTerm;
            }

            if (isset($filters['featured']) && $filters['featured']) {
                $where[] = "rr.is_featured = 1";
            }

            $where_clause = !empty($where) ? 'WHERE ' . implode(' AND ', $where) : '';

            // Sortering
            $orderMap = [
                'popular' => 'rr.views DESC',
                'liked' => 'rr.likes DESC',
                'oldest' => 'rr.published_at ASC',
                'recent' => 'rr.published_at DESC'
            ];
            $orderBy = $filters['order_by'] ?? 'recent';
            $order = $orderMap[$orderBy] ?? 'rr.published_at DESC';

            $sql = "SELECT
                        rr.*,
                        r.firstname,
                        r.lastname,
                        r.club_id,
                        c.name as club_name,
                        e.name as event_name
                    FROM race_reports rr
                    LEFT JOIN riders r ON rr.rider_id = r.id
                    LEFT JOIN clubs c ON r.club_id = c.id
                    LEFT JOIN events e ON rr.event_id = e.id
                    {$where_clause}
                    ORDER BY {$order}
                    LIMIT :limit OFFSET :offset";

            $stmt = $this->pdo->prepare($sql);
            foreach ($params as $key => $value) {
                $stmt->bindValue($key, $value);
            }
            $stmt->bindValue(':limit', $per_page, PDO::PARAM_INT);
            $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
            $stmt->execute();

            $reports = [];
            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $row['tags'] = $this->getReportTags($row['id']);
                $reports[] = $row;
            }

            // Räkna total
            $count_sql = "SELECT COUNT(*) as total FROM race_reports rr {$where_clause}";
            $count_stmt = $this->pdo->prepare($count_sql);
            foreach ($params as $key => $value) {
                $count_stmt->bindValue($key, $value);
            }
            $count_stmt->execute();
            $total = $count_stmt->fetch(PDO::FETCH_ASSOC)['total'];

            return [
                'reports' => $reports,
                'total' => (int)$total,
                'page' => (int)$page,
                'per_page' => (int)$per_page,
                'total_pages' => (int)ceil($total / $per_page)
            ];
        } catch (PDOException $e) {
            error_log("listReports error: " . $e->getMessage());
            return ['reports' => [], 'total' => 0, 'page' => 1, 'per_page' => 12, 'total_pages' => 0];
        }
    }

    /**
     * Ta bort report
     */
    public function deleteReport($report_id) {
        try {
            $stmt = $this->pdo->prepare("DELETE FROM race_reports WHERE id = :id");
            return $stmt->execute([':id' => $report_id]);
        } catch (PDOException $e) {
            error_log("deleteReport error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Lägg till kommentar
     * @param int $report_id
     * @param int|null $rider_id
     * @param string $comment_text
     * @param int|null $parent_id
     * @return int|false
     */
    public function addComment($report_id, $rider_id, $comment_text, $parent_id = null) {
        try {
            $stmt = $this->pdo->prepare("
                INSERT INTO race_report_comments
                (report_id, rider_id, comment_text, parent_comment_id)
                VALUES (:report_id, :rider_id, :comment_text, :parent_id)
            ");

            $stmt->execute([
                ':report_id' => $report_id,
                ':rider_id' => $rider_id,
                ':comment_text' => $comment_text,
                ':parent_id' => $parent_id
            ]);

            return (int)$this->pdo->lastInsertId();
        } catch (PDOException $e) {
            error_log("addComment error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Hämta kommentarer för report
     */
    public function getComments($report_id) {
        try {
            $stmt = $this->pdo->prepare("
                SELECT
                    rc.*,
                    r.firstname,
                    r.lastname,
                    r.club_id
                FROM race_report_comments rc
                LEFT JOIN riders r ON rc.rider_id = r.id
                WHERE rc.report_id = :report_id
                AND rc.is_approved = 1
                ORDER BY rc.created_at ASC
            ");
            $stmt->execute([':report_id' => $report_id]);
            $comments = $stmt->fetchAll(PDO::FETCH_ASSOC);

            // Bygg träd-struktur för svar
            return $this->buildCommentTree($comments);
        } catch (PDOException $e) {
            error_log("getComments error: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Like/Unlike report
     */
    public function toggleLike($report_id, $rider_id) {
        try {
            // Kolla om redan likat
            $stmt = $this->pdo->prepare("
                SELECT 1 FROM race_report_likes
                WHERE report_id = :report_id AND rider_id = :rider_id
            ");
            $stmt->execute([':report_id' => $report_id, ':rider_id' => $rider_id]);
            $already_liked = $stmt->fetch() !== false;

            if ($already_liked) {
                // Ta bort like
                $stmt = $this->pdo->prepare("
                    DELETE FROM race_report_likes
                    WHERE report_id = :report_id AND rider_id = :rider_id
                ");
                $stmt->execute([':report_id' => $report_id, ':rider_id' => $rider_id]);

                // Minska räknare
                $stmt = $this->pdo->prepare("
                    UPDATE race_reports
                    SET likes = GREATEST(0, likes - 1)
                    WHERE id = :id
                ");
                $stmt->execute([':id' => $report_id]);

                return false; // Unliked
            } else {
                // Lägg till like
                $stmt = $this->pdo->prepare("
                    INSERT INTO race_report_likes (report_id, rider_id)
                    VALUES (:report_id, :rider_id)
                ");
                $stmt->execute([':report_id' => $report_id, ':rider_id' => $rider_id]);

                // Öka räknare
                $stmt = $this->pdo->prepare("
                    UPDATE race_reports
                    SET likes = likes + 1
                    WHERE id = :id
                ");
                $stmt->execute([':id' => $report_id]);

                return true; // Liked
            }
        } catch (PDOException $e) {
            error_log("toggleLike error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Kolla om rider har likat ett report
     */
    public function hasLiked($report_id, $rider_id) {
        try {
            $stmt = $this->pdo->prepare("
                SELECT 1 FROM race_report_likes
                WHERE report_id = :report_id AND rider_id = :rider_id
            ");
            $stmt->execute([':report_id' => $report_id, ':rider_id' => $rider_id]);
            return $stmt->fetch() !== false;
        } catch (PDOException $e) {
            return false;
        }
    }

    /**
     * Hämta alla tags
     */
    public function getAllTags() {
        try {
            $stmt = $this->pdo->query("
                SELECT * FROM race_report_tags
                ORDER BY usage_count DESC, name ASC
            ");
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            return [];
        }
    }

    /**
     * Hjälpfunktioner
     */

    private function generateSlug($title, $exclude_id = null) {
        $slug = strtolower(trim($title));
        // Ersätt svenska tecken
        $slug = str_replace(['å', 'ä', 'ö', 'Å', 'Ä', 'Ö'], ['a', 'a', 'o', 'a', 'a', 'o'], $slug);
        $slug = preg_replace('/[^a-z0-9-]/', '-', $slug);
        $slug = preg_replace('/-+/', '-', $slug);
        $slug = trim($slug, '-');

        // Kolla om slug redan finns
        $original_slug = $slug;
        $counter = 1;

        while (true) {
            $sql = "SELECT id FROM race_reports WHERE slug = :slug";
            $params = [':slug' => $slug];

            if ($exclude_id) {
                $sql .= " AND id != :exclude_id";
                $params[':exclude_id'] = $exclude_id;
            }

            $stmt = $this->pdo->prepare($sql);
            $stmt->execute($params);

            if (!$stmt->fetch()) {
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

    /**
     * Extrahera YouTube video ID från URL
     */
    private function getYoutubeVideoId($url) {
        // Stöder olika YouTube URL-format:
        // https://www.youtube.com/watch?v=VIDEO_ID
        // https://youtu.be/VIDEO_ID
        // https://www.youtube.com/embed/VIDEO_ID
        // https://www.youtube.com/shorts/VIDEO_ID

        $patterns = [
            '/youtube\.com\/watch\?v=([^&\s]+)/',
            '/youtu\.be\/([^?\s]+)/',
            '/youtube\.com\/embed\/([^?\s]+)/',
            '/youtube\.com\/shorts\/([^?\s]+)/',
        ];

        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $url, $matches)) {
                return $matches[1];
            }
        }

        return null;
    }

    /**
     * Hämta YouTube thumbnail URL
     */
    public function getYoutubeThumbnail($videoId, $quality = 'maxresdefault') {
        // Kvaliteter: default, mqdefault, hqdefault, sddefault, maxresdefault
        return "https://img.youtube.com/vi/{$videoId}/{$quality}.jpg";
    }

    private function incrementViews($report_id) {
        try {
            $stmt = $this->pdo->prepare("UPDATE race_reports SET views = views + 1 WHERE id = :id");
            $stmt->execute([':id' => $report_id]);
        } catch (PDOException $e) {
            // Ignorera fel
        }
    }

    private function addTags($report_id, $tags) {
        foreach ($tags as $tag_name) {
            try {
                // Skapa tag slug
                $tag_slug = strtolower(trim($tag_name));
                $tag_slug = str_replace(['å', 'ä', 'ö'], ['a', 'a', 'o'], $tag_slug);
                $tag_slug = preg_replace('/[^a-z0-9-]/', '-', $tag_slug);
                $tag_slug = preg_replace('/-+/', '-', $tag_slug);
                $tag_slug = trim($tag_slug, '-');

                // Skapa eller uppdatera tag
                $stmt = $this->pdo->prepare("
                    INSERT INTO race_report_tags (name, slug, usage_count)
                    VALUES (:name, :slug, 1)
                    ON DUPLICATE KEY UPDATE usage_count = usage_count + 1
                ");
                $stmt->execute([':name' => $tag_name, ':slug' => $tag_slug]);

                // Hämta tag_id
                $stmt = $this->pdo->prepare("SELECT id FROM race_report_tags WHERE slug = :slug");
                $stmt->execute([':slug' => $tag_slug]);
                $tag = $stmt->fetch(PDO::FETCH_ASSOC);

                if ($tag) {
                    // Koppla tag till report
                    $stmt = $this->pdo->prepare("
                        INSERT IGNORE INTO race_report_tag_relations (report_id, tag_id)
                        VALUES (:report_id, :tag_id)
                    ");
                    $stmt->execute([':report_id' => $report_id, ':tag_id' => $tag['id']]);
                }
            } catch (PDOException $e) {
                error_log("addTags error: " . $e->getMessage());
            }
        }
    }

    private function getReportTags($report_id) {
        try {
            $stmt = $this->pdo->prepare("
                SELECT rrt.*
                FROM race_report_tags rrt
                INNER JOIN race_report_tag_relations rrtr ON rrt.id = rrtr.tag_id
                WHERE rrtr.report_id = :report_id
                ORDER BY rrt.name
            ");
            $stmt->execute([':report_id' => $report_id]);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            return [];
        }
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
                $parent_id = $comment['parent_comment_id'];
                if (isset($lookup[$parent_id])) {
                    $lookup[$parent_id]['replies'][] = &$lookup[$id];
                }
            }
        }

        return $tree;
    }

    /**
     * Hämta report-statistik för admin
     */
    public function getStats() {
        try {
            $stmt = $this->pdo->query("
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) as published,
                    SUM(CASE WHEN status = 'draft' THEN 1 ELSE 0 END) as drafts,
                    SUM(views) as total_views,
                    SUM(likes) as total_likes
                FROM race_reports
            ");
            return $stmt->fetch(PDO::FETCH_ASSOC) ?: [];
        } catch (PDOException $e) {
            return [];
        }
    }
}
