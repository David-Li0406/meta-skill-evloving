<?php
/**
 * Sponsor Management Functions
 * TheHUB V3 - Media & Sponsor System
 */

/**
 * Ensure sponsor logo columns exist
 * Simplified structure: banner (1200x150) and logo (600x150, auto-scales)
 */
function ensure_sponsor_logo_columns() {
    global $pdo;

    $columns = [
        'logo_banner_id' => 'INT DEFAULT NULL COMMENT "Media ID for banner logo (1200x150)"',
        'logo_media_id' => 'INT DEFAULT NULL COMMENT "Media ID for main logo (600x150, auto-scales to 300x75, 240x60, 160x40)"',
        // Legacy columns kept for backwards compatibility
        'logo_standard_id' => 'INT DEFAULT NULL COMMENT "Legacy: Media ID for standard logo"',
        'logo_small_id' => 'INT DEFAULT NULL COMMENT "Legacy: Media ID for small logo"'
    ];

    try {
        foreach ($columns as $column => $definition) {
            $check = $pdo->query("SHOW COLUMNS FROM sponsors LIKE '{$column}'")->fetch();
            if (!$check) {
                $pdo->exec("ALTER TABLE sponsors ADD COLUMN {$column} {$definition}");
            }
        }
    } catch (Exception $e) {
        error_log("ensure_sponsor_logo_columns error: " . $e->getMessage());
    }
}

// Run migration on load
ensure_sponsor_logo_columns();

/**
 * Get all sponsors with optional filters
 */
function get_sponsors($activeOnly = true, $tier = null) {
    global $pdo;

    try {
        // Check which logo columns exist
        $hasLogoMediaId = false;
        $hasLogoField = false;
        try {
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'logo_media_id'")->fetch();
            $hasLogoMediaId = $cols !== false;
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'logo'")->fetch();
            $hasLogoField = $cols !== false;
        } catch (Exception $e) {}

        // Build SELECT based on available columns
        if ($hasLogoMediaId) {
            $sql = "SELECT s.*, m.filepath as media_logo_url,
                    COALESCE(m.filepath, s.logo) as logo_url
                    FROM sponsors s
                    LEFT JOIN media m ON s.logo_media_id = m.id";
        } else {
            $sql = "SELECT s.*, s.logo as logo_url FROM sponsors s";
        }

        $conditions = [];
        $params = [];

        if ($activeOnly) {
            $conditions[] = "s.active = 1";
        }

        if ($tier) {
            $conditions[] = "s.tier = ?";
            $params[] = $tier;
        }

        if (!empty($conditions)) {
            $sql .= " WHERE " . implode(' AND ', $conditions);
        }

        // Check if display_order column exists
        $hasDisplayOrder = false;
        try {
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'display_order'")->fetch();
            $hasDisplayOrder = $cols !== false;
        } catch (Exception $e) {}

        if ($hasDisplayOrder) {
            $sql .= " ORDER BY s.display_order ASC, s.name ASC";
        } else {
            $sql .= " ORDER BY s.name ASC";
        }

        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);

        $sponsors = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Format logo URLs
        foreach ($sponsors as &$sponsor) {
            if (!empty($sponsor['logo_url'])) {
                $sponsor['logo_url'] = '/' . ltrim($sponsor['logo_url'], '/');
            }
        }

        return $sponsors;
    } catch (PDOException $e) {
        error_log("get_sponsors error: " . $e->getMessage());
        return [];
    }
}

/**
 * Search sponsors
 */
function search_sponsors($query, $limit = 50) {
    global $pdo;

    try {
        $searchTerm = "%{$query}%";

        // Check which columns exist
        $hasLogoMediaId = false;
        $hasContactName = false;
        $hasDisplayOrder = false;
        try {
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'logo_media_id'")->fetch();
            $hasLogoMediaId = $cols !== false;
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'contact_name'")->fetch();
            $hasContactName = $cols !== false;
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'display_order'")->fetch();
            $hasDisplayOrder = $cols !== false;
        } catch (Exception $e) {}

        // Build query based on available columns
        if ($hasLogoMediaId) {
            $sql = "SELECT s.*, COALESCE(m.filepath, s.logo) as logo_url
                    FROM sponsors s
                    LEFT JOIN media m ON s.logo_media_id = m.id
                    WHERE s.name LIKE ? OR s.description LIKE ?";
        } else {
            $sql = "SELECT s.*, s.logo as logo_url FROM sponsors s
                    WHERE s.name LIKE ? OR s.description LIKE ?";
        }

        $params = [$searchTerm, $searchTerm];

        if ($hasContactName) {
            $sql .= " OR s.contact_name LIKE ?";
            $params[] = $searchTerm;
        }

        if ($hasDisplayOrder) {
            $sql .= " ORDER BY s.display_order ASC, s.name ASC";
        } else {
            $sql .= " ORDER BY s.name ASC";
        }
        $sql .= " LIMIT " . (int)$limit;

        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);

        $sponsors = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Format logo URLs
        foreach ($sponsors as &$sponsor) {
            if (!empty($sponsor['logo_url'])) {
                $sponsor['logo_url'] = '/' . ltrim($sponsor['logo_url'], '/');
            }
        }

        return $sponsors;
    } catch (PDOException $e) {
        error_log("search_sponsors error: " . $e->getMessage());
        return [];
    }
}

/**
 * Get single sponsor by ID
 */
function get_sponsor($id) {
    global $pdo;

    try {
        // Check if logo_media_id column exists
        $hasLogoMediaId = false;
        try {
            $cols = $pdo->query("SHOW COLUMNS FROM sponsors LIKE 'logo_media_id'")->fetch();
            $hasLogoMediaId = $cols !== false;
        } catch (Exception $e) {}

        if ($hasLogoMediaId) {
            $stmt = $pdo->prepare("
                SELECT s.*, COALESCE(m.filepath, s.logo) as logo_url
                FROM sponsors s
                LEFT JOIN media m ON s.logo_media_id = m.id
                WHERE s.id = ?
            ");
        } else {
            $stmt = $pdo->prepare("
                SELECT s.*, s.logo as logo_url
                FROM sponsors s
                WHERE s.id = ?
            ");
        }

        $stmt->execute([$id]);
        $sponsor = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($sponsor && !empty($sponsor['logo_url'])) {
            $sponsor['logo_url'] = '/' . ltrim($sponsor['logo_url'], '/');
        }

        // Get series associations
        if ($sponsor) {
            try {
                $seriesStmt = $pdo->prepare("SELECT series_id FROM series_sponsors WHERE sponsor_id = ?");
                $seriesStmt->execute([$id]);
                $sponsor['series_ids'] = $seriesStmt->fetchAll(PDO::FETCH_COLUMN);
            } catch (Exception $e) {
                $sponsor['series_ids'] = [];
            }
        }

        return $sponsor;
    } catch (PDOException $e) {
        error_log("get_sponsor error: " . $e->getMessage());
        return null;
    }
}

/**
 * Get sponsor statistics by tier
 */
function get_sponsor_stats() {
    global $pdo;
    
    try {
        $stmt = $pdo->query("
            SELECT 
                tier,
                COUNT(*) as count,
                SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) as active_count
            FROM sponsors
            GROUP BY tier
        ");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("get_sponsor_stats error: " . $e->getMessage());
        return [];
    }
}

/**
 * Create new sponsor
 */
function create_sponsor($data) {
    global $pdo;

    try {
        // Get available columns
        $availableColumns = [];
        $cols = $pdo->query("SHOW COLUMNS FROM sponsors")->fetchAll(PDO::FETCH_COLUMN);
        $availableColumns = array_flip($cols);

        // Generate slug from name if not provided
        $slug = $data['slug'] ?? null;
        if (empty($slug) && !empty($data['name'])) {
            $slug = generate_sponsor_slug($data['name']);
        }

        // Base fields that always exist
        $fields = ['name', 'tier', 'website', 'description', 'active'];
        $values = [
            $data['name'] ?? '',
            $data['tier'] ?? 'bronze',
            $data['website'] ?? null,
            $data['description'] ?? null,
            isset($data['active']) ? ($data['active'] ? 1 : 0) : 1
        ];

        // Add slug if column exists
        if (isset($availableColumns['slug']) && $slug) {
            $fields[] = 'slug';
            $values[] = $slug;
        }

        // Optional fields - only include if column exists
        $optionalFields = [
            'logo' => $data['logo'] ?? null,
            'logo_media_id' => $data['logo_media_id'] ?? null,
            'logo_banner_id' => $data['logo_banner_id'] ?? null,
            'logo_standard_id' => $data['logo_standard_id'] ?? null,
            'logo_small_id' => $data['logo_small_id'] ?? null,
            'contact_name' => $data['contact_name'] ?? null,
            'contact_email' => $data['contact_email'] ?? null,
            'contact_phone' => $data['contact_phone'] ?? null,
            'display_order' => $data['display_order'] ?? 0,
        ];

        foreach ($optionalFields as $field => $value) {
            if (isset($availableColumns[$field])) {
                $fields[] = $field;
                $values[] = $value;
            }
        }

        $placeholders = array_fill(0, count($fields), '?');
        $sql = "INSERT INTO sponsors (" . implode(', ', $fields) . ") VALUES (" . implode(', ', $placeholders) . ")";

        $stmt = $pdo->prepare($sql);
        $stmt->execute($values);

        $sponsorId = $pdo->lastInsertId();

        // Handle series associations
        if (!empty($data['series_ids']) && is_array($data['series_ids'])) {
            $seriesStmt = $pdo->prepare("INSERT INTO series_sponsors (series_id, sponsor_id) VALUES (?, ?)");
            foreach ($data['series_ids'] as $seriesId) {
                try {
                    $seriesStmt->execute([$seriesId, $sponsorId]);
                } catch (Exception $e) {
                    // Ignore duplicates
                }
            }
        }

        return [
            'success' => true,
            'id' => $sponsorId
        ];
    } catch (PDOException $e) {
        error_log("create_sponsor error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte skapa sponsor: ' . $e->getMessage()];
    }
}

/**
 * Generate unique slug from name
 */
function generate_sponsor_slug($name) {
    global $pdo;

    // Convert to lowercase, replace spaces/special chars with hyphens
    $slug = strtolower(trim($name));
    $slug = preg_replace('/[åä]/u', 'a', $slug);
    $slug = preg_replace('/[ö]/u', 'o', $slug);
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug);
    $slug = trim($slug, '-');

    // Check if slug exists, append number if needed
    $baseSlug = $slug;
    $counter = 1;

    while (true) {
        $stmt = $pdo->prepare("SELECT id FROM sponsors WHERE slug = ?");
        $stmt->execute([$slug]);
        if (!$stmt->fetch()) {
            break; // Slug is unique
        }
        $slug = $baseSlug . '-' . $counter;
        $counter++;
    }

    return $slug;
}

/**
 * Update sponsor
 */
function update_sponsor($id, $data) {
    global $pdo;

    try {
        // Get available columns
        $cols = $pdo->query("SHOW COLUMNS FROM sponsors")->fetchAll(PDO::FETCH_COLUMN);
        $availableColumns = array_flip($cols);

        // DEBUG: Log what we're trying to save
        error_log("UPDATE_SPONSOR: ID=$id, available_cols=" . implode(',', $cols));
        error_log("UPDATE_SPONSOR: data=" . json_encode($data));

        // All possible fields we might want to update
        $allFields = ['name', 'tier', 'website', 'description', 'logo', 'logo_media_id',
                      'logo_banner_id', 'logo_standard_id', 'logo_small_id',
                      'contact_name', 'contact_email', 'contact_phone', 'display_order', 'active'];

        $updates = [];
        $params = [];

        foreach ($allFields as $field) {
            // Only include if field exists in data AND column exists in database
            if (array_key_exists($field, $data) && isset($availableColumns[$field])) {
                $updates[] = "{$field} = ?";

                // Handle boolean for active
                if ($field === 'active') {
                    $params[] = $data[$field] ? 1 : 0;
                } else {
                    $params[] = $data[$field];
                }
            }
        }

        // DEBUG: Log what will be updated
        error_log("UPDATE_SPONSOR: updates=" . implode(', ', $updates));

        if (empty($updates)) {
            return ['success' => false, 'error' => 'Inget att uppdatera'];
        }

        // Add updated_at if column exists
        if (isset($availableColumns['updated_at'])) {
            $updates[] = "updated_at = NOW()";
        }

        $params[] = $id;
        $sql = "UPDATE sponsors SET " . implode(', ', $updates) . " WHERE id = ?";

        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);

        // Handle series associations if provided
        if (array_key_exists('series_ids', $data)) {
            // Remove existing associations
            $pdo->prepare("DELETE FROM series_sponsors WHERE sponsor_id = ?")->execute([$id]);

            // Add new associations
            if (!empty($data['series_ids']) && is_array($data['series_ids'])) {
                $seriesStmt = $pdo->prepare("INSERT INTO series_sponsors (series_id, sponsor_id) VALUES (?, ?)");
                foreach ($data['series_ids'] as $seriesId) {
                    try {
                        $seriesStmt->execute([$seriesId, $id]);
                    } catch (Exception $e) {
                        // Ignore duplicates
                    }
                }
            }
        }

        return ['success' => true];
    } catch (PDOException $e) {
        error_log("update_sponsor error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte uppdatera sponsor: ' . $e->getMessage()];
    }
}

/**
 * Delete sponsor
 */
function delete_sponsor($id) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("DELETE FROM sponsors WHERE id = ?");
        $stmt->execute([$id]);
        
        return ['success' => true];
    } catch (PDOException $e) {
        error_log("delete_sponsor error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte radera sponsor'];
    }
}

/**
 * Get sponsors by tier
 */
function get_sponsors_by_tier($tier) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("
            SELECT s.*, m.filepath as logo_url 
            FROM sponsors s 
            LEFT JOIN media m ON s.logo_media_id = m.id
            WHERE s.tier = ? AND s.active = 1
            ORDER BY s.display_order ASC, s.name ASC
        ");
        $stmt->execute([$tier]);
        
        $sponsors = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        foreach ($sponsors as &$sponsor) {
            if ($sponsor['logo_url']) {
                $sponsor['logo_url'] = '/' . ltrim($sponsor['logo_url'], '/');
            }
        }
        
        return $sponsors;
    } catch (PDOException $e) {
        error_log("get_sponsors_by_tier error: " . $e->getMessage());
        return [];
    }
}

/**
 * Get sponsors for a specific series
 */
function get_series_sponsors($seriesId) {
    global $pdo;

    try {
        // Get sponsors for this series
        $stmt = $pdo->prepare("
            SELECT s.*, m.filepath as logo_url, ss.display_order as series_display_order
            FROM sponsors s
            INNER JOIN series_sponsors ss ON s.id = ss.sponsor_id
            LEFT JOIN media m ON s.logo_media_id = m.id
            WHERE ss.series_id = ? AND s.active = 1
            ORDER BY ss.display_order ASC, s.display_order ASC
        ");
        $stmt->execute([$seriesId]);
        
        $sponsors = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        foreach ($sponsors as &$sponsor) {
            if ($sponsor['logo_url']) {
                $sponsor['logo_url'] = '/' . ltrim($sponsor['logo_url'], '/');
            }
        }
        
        return $sponsors;
    } catch (PDOException $e) {
        // Table might not exist, return empty
        error_log("get_series_sponsors error: " . $e->getMessage());
        return [];
    }
}

/**
 * Assign sponsor to series
 */
function assign_sponsor_to_series($sponsorId, $seriesId, $displayOrder = 0) {
    global $pdo;

    try {
        $stmt = $pdo->prepare("
            INSERT INTO series_sponsors (sponsor_id, series_id, display_order)
            VALUES (?, ?, ?)
            ON DUPLICATE KEY UPDATE display_order = ?
        ");
        $stmt->execute([$sponsorId, $seriesId, $displayOrder, $displayOrder]);
        
        return ['success' => true];
    } catch (PDOException $e) {
        error_log("assign_sponsor_to_series error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte tilldela sponsor'];
    }
}

/**
 * Remove sponsor from series
 */
function remove_sponsor_from_series($sponsorId, $seriesId) {
    global $pdo;

    try {
        $stmt = $pdo->prepare("DELETE FROM series_sponsors WHERE sponsor_id = ? AND series_id = ?");
        $stmt->execute([$sponsorId, $seriesId]);

        return ['success' => true];
    } catch (PDOException $e) {
        error_log("remove_sponsor_from_series error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte ta bort sponsor'];
    }
}

/**
 * Get sponsor with all logo URLs for different placements
 * Simplified structure: banner (1200x150) and logo (600x150, auto-scales)
 * Returns logo_url for main logo and banner_logo_url for banner
 */
function get_sponsor_with_logos($id) {
    global $pdo;

    try {
        $stmt = $pdo->prepare("
            SELECT s.*,
                   m_logo.filepath as logo_url,
                   m_banner.filepath as banner_logo_url,
                   m_standard.filepath as standard_logo_url,
                   m_small.filepath as small_logo_url
            FROM sponsors s
            LEFT JOIN media m_logo ON s.logo_media_id = m_logo.id
            LEFT JOIN media m_banner ON s.logo_banner_id = m_banner.id
            LEFT JOIN media m_standard ON s.logo_standard_id = m_standard.id
            LEFT JOIN media m_small ON s.logo_small_id = m_small.id
            WHERE s.id = ?
        ");
        $stmt->execute([$id]);
        $sponsor = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($sponsor) {
            // Main logo URL (from logo_media_id, with fallbacks to legacy fields)
            $mainLogo = $sponsor['logo_url']
                ?? $sponsor['standard_logo_url']
                ?? $sponsor['small_logo_url']
                ?? ($sponsor['logo'] ? '/uploads/sponsors/' . $sponsor['logo'] : null);

            // Banner logo URL (from logo_banner_id, with fallback to main logo)
            $bannerLogo = $sponsor['banner_logo_url'] ?? $mainLogo;

            // Build logo URLs structure for backwards compatibility
            $sponsor['logo_urls'] = [
                'banner' => $bannerLogo,
                'standard' => $mainLogo,
                'small' => $mainLogo,
            ];

            // Set primary logo_url
            $sponsor['logo_url'] = $mainLogo;

            // Normalize paths
            foreach ($sponsor['logo_urls'] as $key => $url) {
                if ($url) {
                    $sponsor['logo_urls'][$key] = '/' . ltrim($url, '/');
                }
            }
            if ($sponsor['logo_url']) {
                $sponsor['logo_url'] = '/' . ltrim($sponsor['logo_url'], '/');
            }
            if ($sponsor['banner_logo_url']) {
                $sponsor['banner_logo_url'] = '/' . ltrim($sponsor['banner_logo_url'], '/');
            }
        }

        // Get series associations
        if ($sponsor) {
            try {
                $seriesStmt = $pdo->prepare("SELECT series_id FROM series_sponsors WHERE sponsor_id = ?");
                $seriesStmt->execute([$id]);
                $sponsor['series_ids'] = $seriesStmt->fetchAll(PDO::FETCH_COLUMN);
            } catch (Exception $e) {
                $sponsor['series_ids'] = [];
            }
        }

        return $sponsor;
    } catch (PDOException $e) {
        error_log("get_sponsor_with_logos error: " . $e->getMessage());
        return null;
    }
}

/**
 * Get the appropriate logo URL for a sponsor based on placement
 * @param array $sponsor Sponsor data (must include logo fields)
 * @param string $placement 'header'/'banner', 'content'/'standard', 'sidebar'/'small'
 * @return string|null Logo URL or null
 */
function get_sponsor_logo_for_placement($sponsor, $placement) {
    // Map placement to logo field
    $placementMap = [
        'header' => 'banner',
        'banner' => 'banner',
        'content' => 'standard',
        'standard' => 'standard',
        'sidebar' => 'small',
        'small' => 'small',
        'footer' => 'standard'
    ];

    $logoType = $placementMap[$placement] ?? 'standard';

    // Try specific logo first, then fallback
    $fieldMap = [
        'banner' => ['logo_banner_id', 'banner_logo_url'],
        'standard' => ['logo_standard_id', 'standard_logo_url'],
        'small' => ['logo_small_id', 'small_logo_url']
    ];

    // Check if logo_urls array exists (from get_sponsor_with_logos)
    if (isset($sponsor['logo_urls'][$logoType])) {
        return $sponsor['logo_urls'][$logoType];
    }

    // Check specific URL field
    $urlField = $fieldMap[$logoType][1] ?? null;
    if ($urlField && !empty($sponsor[$urlField])) {
        return '/' . ltrim($sponsor[$urlField], '/');
    }

    // Try other sizes as fallback for this placement
    foreach (['standard', 'small', 'banner'] as $fallbackType) {
        if ($fallbackType === $logoType) continue;
        $fallbackField = $fieldMap[$fallbackType][1] ?? null;
        if ($fallbackField && !empty($sponsor[$fallbackField])) {
            return '/' . ltrim($sponsor[$fallbackField], '/');
        }
    }

    // Fallback to legacy_logo_url (from logo_media_id join)
    if (!empty($sponsor['legacy_logo_url'])) {
        return '/' . ltrim($sponsor['legacy_logo_url'], '/');
    }

    // Fallback to logo_url or logo field
    if (!empty($sponsor['logo_url'])) {
        return '/' . ltrim($sponsor['logo_url'], '/');
    }

    if (!empty($sponsor['logo'])) {
        return '/uploads/sponsors/' . $sponsor['logo'];
    }

    return null;
}
