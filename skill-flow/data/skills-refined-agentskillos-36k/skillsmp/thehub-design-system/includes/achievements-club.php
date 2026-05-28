<?php
/**
 * TheHUB Achievements System - Club Badges
 * Hexagonal badge components for club achievements
 *
 * @version 2.0
 * @package TheHUB
 */

// Prevent direct access
if (!defined('DB_HOST') && !defined('THEHUB_LOADED')) {
    define('THEHUB_LOADED', true);
}

/**
 * Get club stats for achievements
 */
function getClubAchievementStats(PDO $pdo, int $club_id): array {
    $stats = [
        'total_starts' => 0,
        'active_members' => 0,
        'total_gold' => 0,
        'total_podiums' => 0,
        'series_wins' => 0,
        'sm_medals' => 0,
        'best_ranking' => null,
        'unique_champions' => 0,
        'champion_names' => [],
        'seasons_active' => 1,
        'first_season_year' => date('Y'),
        'total_members' => 0
    ];

    try {
        // Get total starts and podiums for active members (last 12 months)
        $stmt = $pdo->prepare("
            SELECT
                COUNT(*) as total_starts,
                COUNT(DISTINCT res.cyclist_id) as active_members,
                SUM(CASE WHEN res.position = 1 THEN 1 ELSE 0 END) as total_gold,
                SUM(CASE WHEN res.position <= 3 THEN 1 ELSE 0 END) as total_podiums
            FROM results res
            JOIN riders r ON res.cyclist_id = r.id
            JOIN events e ON res.event_id = e.id
            WHERE r.club_id = ?
            AND e.date > DATE_SUB(NOW(), INTERVAL 12 MONTH)
        ");
        $stmt->execute([$club_id]);
        $result = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($result) {
            $stats['total_starts'] = (int)$result['total_starts'];
            $stats['active_members'] = (int)$result['active_members'];
            $stats['total_gold'] = (int)$result['total_gold'];
            $stats['total_podiums'] = (int)$result['total_podiums'];
        }

        // Get total club members
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM riders WHERE club_id = ? AND active = 1");
        $stmt->execute([$club_id]);
        $stats['total_members'] = (int)$stmt->fetchColumn();

        // Get series wins (from rider_achievements)
        $stmt = $pdo->prepare("
            SELECT COUNT(*) as wins, r.firstname, r.lastname
            FROM rider_achievements ra
            JOIN riders r ON ra.rider_id = r.id
            WHERE r.club_id = ?
            AND ra.achievement_type = 'series_champion'
            GROUP BY r.id
        ");
        $stmt->execute([$club_id]);
        $champions = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $stats['series_wins'] = 0;
        $stats['champion_names'] = [];
        foreach ($champions as $champ) {
            $stats['series_wins'] += (int)$champ['wins'];
            $stats['champion_names'][] = $champ['firstname'] . ' ' . $champ['lastname'];
        }
        $stats['unique_champions'] = count($champions);

        // Get SM medals
        $stmt = $pdo->prepare("
            SELECT COUNT(*) as medals
            FROM rider_achievements ra
            JOIN riders r ON ra.rider_id = r.id
            WHERE r.club_id = ?
            AND ra.achievement_type = 'swedish_champion'
        ");
        $stmt->execute([$club_id]);
        $stats['sm_medals'] = (int)$stmt->fetchColumn();

        // Get club's first season (earliest rider registration)
        $stmt = $pdo->prepare("
            SELECT MIN(first_season) FROM riders WHERE club_id = ? AND first_season IS NOT NULL
        ");
        $stmt->execute([$club_id]);
        $firstSeason = $stmt->fetchColumn();
        if ($firstSeason) {
            $stats['first_season_year'] = (int)$firstSeason;
            $stats['seasons_active'] = (int)date('Y') - $stats['first_season_year'] + 1;
        }

        // Get best ranking (from latest series standings)
        $stmt = $pdo->prepare("
            SELECT MIN(ss.position) as best_position
            FROM series_standings ss
            JOIN riders r ON ss.rider_id = r.id
            WHERE r.club_id = ?
            AND ss.year = YEAR(NOW())
        ");
        $stmt->execute([$club_id]);
        $bestRanking = $stmt->fetchColumn();
        if ($bestRanking) {
            $stats['best_ranking'] = (int)$bestRanking;
        }

    } catch (PDOException $e) {
        // Silently fail, use defaults
    }

    return $stats;
}

/**
 * Get detailed club achievements with member names and event links
 * For showing in modal when clicking on achievements
 */
function getClubDetailedAchievements(PDO $pdo, int $club_id): array {
    $achievements = [];

    try {
        // Series Champions (members who won series)
        $stmt = $pdo->prepare("
            SELECT
                ra.id,
                ra.achievement_type,
                ra.achievement_value,
                ra.series_id,
                ra.season_year,
                r.id as rider_id,
                r.firstname,
                r.lastname,
                s.name as series_name
            FROM rider_achievements ra
            JOIN riders r ON ra.rider_id = r.id
            LEFT JOIN series s ON ra.series_id = s.id
            WHERE r.club_id = ?
            AND ra.achievement_type = 'series_champion'
            ORDER BY ra.season_year DESC, r.lastname ASC
        ");
        $stmt->execute([$club_id]);
        $seriesWins = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (!empty($seriesWins)) {
            $achievements['series_champion'] = [
                'label' => 'Seriesegrar',
                'count' => count($seriesWins),
                'items' => $seriesWins
            ];
        }

        // Swedish Champions (SM winners from club)
        $stmt = $pdo->prepare("
            SELECT
                ra.id,
                ra.achievement_type,
                ra.achievement_value,
                ra.season_year,
                ra.event_id,
                r.id as rider_id,
                r.firstname,
                r.lastname,
                e.name as event_name,
                e.date as event_date,
                e.discipline
            FROM rider_achievements ra
            JOIN riders r ON ra.rider_id = r.id
            LEFT JOIN events e ON ra.event_id = e.id
            WHERE r.club_id = ?
            AND ra.achievement_type = 'swedish_champion'
            ORDER BY ra.season_year DESC, r.lastname ASC
        ");
        $stmt->execute([$club_id]);
        $smWins = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (!empty($smWins)) {
            $achievements['swedish_champion'] = [
                'label' => 'SM-medaljer',
                'count' => count($smWins),
                'items' => $smWins
            ];
        }

        // Unique champions (for the "Mästare" badge) - removed from modal as it duplicates series_champion
        // The badge still shows count of unique champions, but clicking opens series_champion list instead

    } catch (PDOException $e) {
        // Silently fail
    }

    return $achievements;
}

/**
 * Get club experience level name
 */
function getClubExperienceLevelName(int $level): string {
    $levels = [
        1 => 'Ny Klubb',
        2 => 'Etablerad',
        3 => 'Växande',
        4 => 'Stark',
        5 => 'Elitsklubb',
        6 => 'Legendklubb'
    ];
    return $levels[$level] ?? 'Ny Klubb';
}

/**
 * Calculate club experience level (1-6)
 */
function calculateClubExperienceLevel(array $stats): int {
    // Level 6: 100+ members AND 25+ series wins (hidden until achieved)
    if ($stats['total_members'] >= 100 && $stats['series_wins'] >= 25) {
        return 6;
    }
    // Level 5: 50+ active members OR 10+ series wins
    if ($stats['active_members'] >= 50 || $stats['series_wins'] >= 10) {
        return 5;
    }
    // Level 4: 25+ active members
    if ($stats['active_members'] >= 25) {
        return 4;
    }
    // Level 3: 10+ active members
    if ($stats['active_members'] >= 10) {
        return 3;
    }
    // Level 2: 2+ seasons
    if ($stats['seasons_active'] >= 2) {
        return 2;
    }
    // Level 1: First season
    return 1;
}

/**
 * Get badge level based on thresholds
 */
function getBadgeLevel(int $value, array $thresholds): string {
    if ($value >= ($thresholds[3] ?? PHP_INT_MAX)) return 'diamond';
    if ($value >= ($thresholds[2] ?? PHP_INT_MAX)) return 'gold';
    if ($value >= ($thresholds[1] ?? PHP_INT_MAX)) return 'silver';
    if ($value >= ($thresholds[0] ?? 0)) return 'bronze';
    return '';
}

/**
 * Generate illustrated hexagonal badge base for club badges
 * 100x116 viewBox with gradient fills and shadows
 */
function getClubHexagonBase(string $gradientStart, string $gradientEnd, string $uniqueId): string {
    return <<<SVG
    <defs>
        <linearGradient id="clubGrad-{$uniqueId}" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="{$gradientStart}"/>
            <stop offset="100%" stop-color="{$gradientEnd}"/>
        </linearGradient>
        <linearGradient id="clubShine-{$uniqueId}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
            <stop offset="50%" stop-color="#ffffff" stop-opacity="0.1"/>
            <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
        </linearGradient>
        <filter id="clubShadow-{$uniqueId}">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.3"/>
        </filter>
    </defs>
    <!-- Hexagon background with gradient -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#clubGrad-{$uniqueId})" filter="url(#clubShadow-{$uniqueId})"/>
    <!-- Border highlight -->
    <path d="M50 6L92 30V86L50 110L8 86V30L50 6Z" fill="none" stroke="url(#clubShine-{$uniqueId})" stroke-width="2"/>
    <!-- Inner shine -->
    <path d="M50 10L88 32V84L50 106L12 84V32L50 10Z" fill="url(#clubShine-{$uniqueId})" opacity="0.3"/>
SVG;
}

/**
 * Render club starter badge SVG - Racing start gate with checkered flag
 */
function renderClubStarterBadge(): string {
    $base = getClubHexagonBase('#4CAF50', '#2E7D32', 'clubstarter');
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <!-- Starting gate posts -->
    <rect x="22" y="35" width="6" height="50" fill="#8B4513" rx="2"/>
    <rect x="72" y="35" width="6" height="50" fill="#8B4513" rx="2"/>

    <!-- Top bar -->
    <rect x="20" y="32" width="60" height="8" fill="#A0522D" rx="2"/>

    <!-- Checkered banner -->
    <g>
        <!-- Row 1 -->
        <rect x="28" y="42" width="6" height="6" fill="#ffffff"/>
        <rect x="34" y="42" width="6" height="6" fill="#1a1a1a"/>
        <rect x="40" y="42" width="6" height="6" fill="#ffffff"/>
        <rect x="46" y="42" width="6" height="6" fill="#1a1a1a"/>
        <rect x="52" y="42" width="6" height="6" fill="#ffffff"/>
        <rect x="58" y="42" width="6" height="6" fill="#1a1a1a"/>
        <rect x="64" y="42" width="6" height="6" fill="#ffffff"/>
        <!-- Row 2 -->
        <rect x="28" y="48" width="6" height="6" fill="#1a1a1a"/>
        <rect x="34" y="48" width="6" height="6" fill="#ffffff"/>
        <rect x="40" y="48" width="6" height="6" fill="#1a1a1a"/>
        <rect x="46" y="48" width="6" height="6" fill="#ffffff"/>
        <rect x="52" y="48" width="6" height="6" fill="#1a1a1a"/>
        <rect x="58" y="48" width="6" height="6" fill="#ffffff"/>
        <rect x="64" y="48" width="6" height="6" fill="#1a1a1a"/>
        <!-- Row 3 -->
        <rect x="28" y="54" width="6" height="6" fill="#ffffff"/>
        <rect x="34" y="54" width="6" height="6" fill="#1a1a1a"/>
        <rect x="40" y="54" width="6" height="6" fill="#ffffff"/>
        <rect x="46" y="54" width="6" height="6" fill="#1a1a1a"/>
        <rect x="52" y="54" width="6" height="6" fill="#ffffff"/>
        <rect x="58" y="54" width="6" height="6" fill="#1a1a1a"/>
        <rect x="64" y="54" width="6" height="6" fill="#ffffff"/>
    </g>

    <!-- GO text -->
    <text x="50" y="78" text-anchor="middle" fill="#ffffff" font-size="18" font-weight="bold" font-family="system-ui, sans-serif" filter="url(#clubShadow-clubstarter)">GO!</text>

    <!-- Ground/track -->
    <path d="M15 85 Q50 90 85 85" stroke="#5D4037" stroke-width="4" fill="none"/>
</svg>
SVG;
}

/**
 * Render club active members badge SVG - Group of cyclists
 */
function renderClubActiveBadge(): string {
    $base = getClubHexagonBase('#1565C0', '#0D47A1', 'clubactive');
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <!-- Back row cyclists (smaller, faded) -->
    <g opacity="0.5" transform="translate(25, 32) scale(0.7)">
        <!-- Cyclist 1 -->
        <circle cx="0" cy="0" r="8" fill="#ffffff"/>
        <ellipse cx="0" cy="18" rx="7" ry="10" fill="#ffffff"/>
    </g>
    <g opacity="0.5" transform="translate(75, 32) scale(0.7)">
        <!-- Cyclist 2 -->
        <circle cx="0" cy="0" r="8" fill="#ffffff"/>
        <ellipse cx="0" cy="18" rx="7" ry="10" fill="#ffffff"/>
    </g>

    <!-- Middle row cyclists -->
    <g opacity="0.75" transform="translate(35, 45) scale(0.85)">
        <!-- Cyclist 3 -->
        <circle cx="0" cy="0" r="8" fill="#E3F2FD"/>
        <ellipse cx="0" cy="18" rx="7" ry="10" fill="#E3F2FD"/>
    </g>
    <g opacity="0.75" transform="translate(65, 45) scale(0.85)">
        <!-- Cyclist 4 -->
        <circle cx="0" cy="0" r="8" fill="#E3F2FD"/>
        <ellipse cx="0" cy="18" rx="7" ry="10" fill="#E3F2FD"/>
    </g>

    <!-- Front row cyclist (leader) -->
    <g transform="translate(50, 55)">
        <!-- Head -->
        <circle cx="0" cy="0" r="10" fill="#ffffff"/>
        <!-- Helmet -->
        <path d="M-10 -2 Q-10 -12 0 -12 Q10 -12 10 -2" fill="#FFD700"/>
        <!-- Body -->
        <ellipse cx="0" cy="20" rx="9" ry="12" fill="#ffffff"/>
        <!-- Jersey detail -->
        <path d="M-6 15 L6 15 L4 25 L-4 25 Z" fill="#FFD700"/>
    </g>

    <!-- Connection lines (representing team unity) -->
    <path d="M30 50 Q50 45 70 50" stroke="#ffffff" stroke-width="1" fill="none" opacity="0.3"/>
    <path d="M35 65 Q50 60 65 65" stroke="#FFD700" stroke-width="1.5" fill="none" opacity="0.5"/>
</svg>
SVG;
}

/**
 * Render club gold badge SVG - Stack of gold medals with ribbon
 */
function renderClubGoldBadge(): string {
    $base = getClubHexagonBase('#FFD700', '#B8860B', 'clubgold');
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <defs>
        <linearGradient id="goldMedalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFE135"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
    </defs>

    <!-- Ribbon -->
    <path d="M35 25 L30 55 L40 50 L50 60 L60 50 L70 55 L65 25" fill="#DC143C"/>
    <path d="M38 25 L35 45 L42 42 L50 50 L58 42 L65 45 L62 25" fill="#FF4444"/>

    <!-- Stack of medals (back) -->
    <g transform="translate(50, 70)" opacity="0.6">
        <circle cx="-12" cy="-5" r="14" fill="url(#goldMedalGrad)" stroke="#8B6914" stroke-width="1"/>
        <circle cx="12" cy="-5" r="14" fill="url(#goldMedalGrad)" stroke="#8B6914" stroke-width="1"/>
    </g>

    <!-- Main medal (front) -->
    <g transform="translate(50, 68)">
        <circle cx="0" cy="0" r="18" fill="url(#goldMedalGrad)" stroke="#8B6914" stroke-width="2"/>
        <!-- Inner ring -->
        <circle cx="0" cy="0" r="14" fill="none" stroke="#FFF8DC" stroke-width="1"/>
        <!-- Star emblem -->
        <polygon points="0,-10 2.5,-3 10,-3 4,2 6,10 0,5 -6,10 -4,2 -10,-3 -2.5,-3" fill="#FFF8DC"/>
        <!-- Shine -->
        <ellipse cx="-5" cy="-5" rx="4" ry="3" fill="#ffffff" opacity="0.4"/>
    </g>

    <!-- Sparkles -->
    <circle cx="25" cy="40" r="2" fill="#ffffff" opacity="0.8"/>
    <circle cx="78" cy="50" r="1.5" fill="#ffffff" opacity="0.6"/>
    <circle cx="30" cy="75" r="1" fill="#FFE135" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render club podium badge SVG - Illustrated podium with positions
 */
function renderClubPodiumBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    <defs>
        <linearGradient id="podiumGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#8E24AA"/>
            <stop offset="100%" stop-color="#4A148C"/>
        </linearGradient>
        <linearGradient id="podiumShine" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
            <stop offset="50%" stop-color="#ffffff" stop-opacity="0.1"/>
            <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="goldPodium" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#FFE135"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
        <linearGradient id="silverPodium" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#E8E8E8"/>
            <stop offset="100%" stop-color="#A0A0A0"/>
        </linearGradient>
        <linearGradient id="bronzePodium" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#E07020"/>
            <stop offset="100%" stop-color="#8B4513"/>
        </linearGradient>
        <filter id="podiumShadow">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.3"/>
        </filter>
    </defs>

    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#podiumGrad)" filter="url(#podiumShadow)"/>
    <path d="M50 6L92 30V86L50 110L8 86V30L50 6Z" fill="none" stroke="url(#podiumShine)" stroke-width="2"/>
    <path d="M50 10L88 32V84L50 106L12 84V32L50 10Z" fill="url(#podiumShine)" opacity="0.3"/>

    <!-- Silver podium (2nd place - left) -->
    <rect x="18" y="60" width="22" height="30" rx="2" fill="url(#silverPodium)"/>
    <text x="29" y="80" text-anchor="middle" fill="#4A4A4A" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">2</text>
    <!-- Silver medal icon -->
    <circle cx="29" cy="52" r="6" fill="#C0C0C0" stroke="#888" stroke-width="1"/>

    <!-- Gold podium (1st place - center) -->
    <rect x="39" y="45" width="22" height="45" rx="2" fill="url(#goldPodium)"/>
    <text x="50" y="70" text-anchor="middle" fill="#5D4E37" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">1</text>
    <!-- Gold medal icon -->
    <circle cx="50" cy="37" r="7" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
    <!-- Crown on gold -->
    <path d="M43 30 L46 35 L50 32 L54 35 L57 30 L55 38 L45 38 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.5"/>

    <!-- Bronze podium (3rd place - right) -->
    <rect x="60" y="68" width="22" height="22" rx="2" fill="url(#bronzePodium)"/>
    <text x="71" y="85" text-anchor="middle" fill="#4A3020" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">3</text>
    <!-- Bronze medal icon -->
    <circle cx="71" cy="60" r="5" fill="#CD7F32" stroke="#8B4513" stroke-width="1"/>

    <!-- Confetti -->
    <rect x="25" y="35" width="3" height="6" fill="#FFD700" transform="rotate(30 26.5 38)" opacity="0.8"/>
    <rect x="70" y="40" width="3" height="6" fill="#C0C0C0" transform="rotate(-20 71.5 43)" opacity="0.8"/>
    <circle cx="35" y="45" r="2" fill="#FF6B6B" opacity="0.7"/>
    <circle cx="65" y="38" r="2" fill="#4ECDC4" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render club series wins badge SVG - Trophy collection with stars
 */
function renderClubSeriesWinsBadge(): string {
    $base = getClubHexagonBase('#FFC107', '#FF8F00', 'clubseries');
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <defs>
        <linearGradient id="trophyGold" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFE135"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
    </defs>

    <!-- Back trophies (smaller) -->
    <g transform="translate(28, 55) scale(0.7)" opacity="0.6">
        <path d="M-8 -12 L8 -12 L6 0 L4 8 L-4 8 L-6 0 Z" fill="url(#trophyGold)"/>
        <path d="M-8 -10 Q-14 -10 -14 -4 Q-14 2 -6 0" fill="none" stroke="#FFD700" stroke-width="2"/>
        <path d="M8 -10 Q14 -10 14 -4 Q14 2 6 0" fill="none" stroke="#FFD700" stroke-width="2"/>
        <rect x="-3" y="8" width="6" height="4" fill="#B8860B"/>
        <rect x="-6" y="12" width="12" height="4" rx="1" fill="#8B6914"/>
    </g>
    <g transform="translate(72, 55) scale(0.7)" opacity="0.6">
        <path d="M-8 -12 L8 -12 L6 0 L4 8 L-4 8 L-6 0 Z" fill="url(#trophyGold)"/>
        <path d="M-8 -10 Q-14 -10 -14 -4 Q-14 2 -6 0" fill="none" stroke="#FFD700" stroke-width="2"/>
        <path d="M8 -10 Q14 -10 14 -4 Q14 2 6 0" fill="none" stroke="#FFD700" stroke-width="2"/>
        <rect x="-3" y="8" width="6" height="4" fill="#B8860B"/>
        <rect x="-6" y="12" width="12" height="4" rx="1" fill="#8B6914"/>
    </g>

    <!-- Main trophy (center, larger) -->
    <g transform="translate(50, 60)">
        <!-- Cup body -->
        <path d="M-12 -18 L12 -18 L10 0 L6 14 L-6 14 L-10 0 Z" fill="url(#trophyGold)" stroke="#B8860B" stroke-width="1"/>
        <!-- Handles -->
        <path d="M-12 -14 Q-20 -14 -20 -4 Q-20 6 -10 4" fill="none" stroke="url(#trophyGold)" stroke-width="4"/>
        <path d="M12 -14 Q20 -14 20 -4 Q20 6 10 4" fill="none" stroke="url(#trophyGold)" stroke-width="4"/>
        <!-- Stem -->
        <rect x="-4" y="14" width="8" height="6" fill="#B8860B"/>
        <!-- Base -->
        <rect x="-10" y="20" width="20" height="6" rx="2" fill="#8B6914"/>
        <!-- Star on trophy -->
        <polygon points="0,-10 2,-4 8,-4 3,0 5,6 0,2 -5,6 -3,0 -8,-4 -2,-4" fill="#ffffff" opacity="0.8"/>
        <!-- Shine -->
        <ellipse cx="-6" cy="-8" rx="3" ry="4" fill="#ffffff" opacity="0.4"/>
    </g>

    <!-- Stars around -->
    <polygon points="25,35 26,38 29,38 27,40 28,43 25,41 22,43 23,40 21,38 24,38" fill="#ffffff" opacity="0.8"/>
    <polygon points="75,35 76,38 79,38 77,40 78,43 75,41 72,43 73,40 71,38 74,38" fill="#ffffff" opacity="0.8"/>
</svg>
SVG;
}

/**
 * Render club SM medals badge SVG - Swedish flag shield with crown and medal
 */
function renderClubSmMedalsBadge(): string {
    $base = getClubHexagonBase('#004a98', '#002d5c', 'clubsm');
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <defs>
        <linearGradient id="smMedalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFE135"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
    </defs>

    <!-- Swedish flag shield -->
    <g transform="translate(50, 50)">
        <!-- Shield shape -->
        <path d="M-25 -20 L25 -20 L25 10 Q25 25 0 30 Q-25 25 -25 10 Z" fill="#004a98" stroke="#002d5c" stroke-width="2"/>

        <!-- Yellow cross -->
        <rect x="-5" y="-20" width="10" height="50" fill="#FECC00"/>
        <rect x="-25" y="-5" width="50" height="10" fill="#FECC00"/>

        <!-- Shield shine -->
        <path d="M-22 -17 L-5 -17 L-5 -5 L-22 -5 Z" fill="#ffffff" opacity="0.2"/>
    </g>

    <!-- Swedish crown on top -->
    <g transform="translate(50, 25)">
        <!-- Crown base -->
        <rect x="-12" y="2" width="24" height="8" rx="1" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
        <!-- Crown peaks -->
        <path d="M-12 2 L-10 -8 L-6 0 L0 -12 L6 0 L10 -8 L12 2" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
        <!-- Crown jewels -->
        <circle cx="-10" cy="-5" r="2" fill="#1E90FF"/>
        <circle cx="0" cy="-9" r="2.5" fill="#DC143C"/>
        <circle cx="10" cy="-5" r="2" fill="#1E90FF"/>
        <!-- Crown orb -->
        <circle cx="0" cy="-12" r="3" fill="#FFD700" stroke="#B8860B" stroke-width="0.5"/>
        <path d="M-1.5 -12 L1.5 -12 M0 -13.5 L0 -10.5" stroke="#B8860B" stroke-width="1"/>
    </g>

    <!-- SM medal at bottom -->
    <g transform="translate(50, 90)">
        <circle cx="0" cy="0" r="10" fill="url(#smMedalGrad)" stroke="#B8860B" stroke-width="1"/>
        <text x="0" y="4" text-anchor="middle" fill="#5D4E37" font-size="10" font-weight="bold" font-family="system-ui, sans-serif">SM</text>
    </g>

    <!-- Sparkles -->
    <circle cx="22" cy="45" r="2" fill="#FECC00" opacity="0.8"/>
    <circle cx="78" cy="55" r="1.5" fill="#ffffff" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render club ranking badge SVG - Compass/leaderboard style
 */
function renderClubRankingBadge(?int $ranking = null): string {
    $base = getClubHexagonBase('#7B1FA2', '#4A148C', 'clubrank');
    $rankText = $ranking ? "#$ranking" : "–";
    $fontSize = $ranking && $ranking >= 100 ? "12" : "16";
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <defs>
        <linearGradient id="compassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#E1BEE7"/>
            <stop offset="100%" stop-color="#CE93D8"/>
        </linearGradient>
    </defs>

    <!-- Compass ring outer -->
    <circle cx="50" cy="58" r="32" fill="none" stroke="#E1BEE7" stroke-width="3"/>
    <circle cx="50" cy="58" r="28" fill="none" stroke="#CE93D8" stroke-width="1"/>

    <!-- Direction markers -->
    <g fill="#E1BEE7">
        <rect x="48" y="24" width="4" height="8"/>
        <rect x="48" y="84" width="4" height="8"/>
        <rect x="16" y="56" width="8" height="4"/>
        <rect x="76" y="56" width="8" height="4"/>
    </g>

    <!-- Compass needle pointing up (to #1) -->
    <g transform="translate(50, 58)">
        <!-- North arrow (gold - pointing to top) -->
        <polygon points="0,-24 6,-8 0,-12 -6,-8" fill="#FFD700"/>
        <!-- South arrow (silver) -->
        <polygon points="0,24 6,8 0,12 -6,8" fill="#9E9E9E"/>
    </g>

    <!-- Center circle with rank -->
    <circle cx="50" cy="58" r="18" fill="#1a1a1a" stroke="#E1BEE7" stroke-width="2"/>
    <text x="50" y="64" text-anchor="middle" fill="#E1BEE7" font-size="{$fontSize}" font-weight="bold" font-family="system-ui, sans-serif">{$rankText}</text>

    <!-- Stars for top rank -->
    <polygon points="50,20 51,23 54,23 52,25 53,28 50,26 47,28 48,25 46,23 49,23" fill="#FFD700" opacity="0.9"/>
</svg>
SVG;
}

/**
 * Render club champions badge SVG - Crown with champion figures
 */
function renderClubChampionsBadge(): string {
    $base = getClubHexagonBase('#FFD700', '#B8860B', 'clubchamps');
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116">
    {$base}

    <defs>
        <linearGradient id="champGold" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFE135"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
        <filter id="champGlow">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <!-- Epic crown -->
    <g transform="translate(50, 38)" filter="url(#champGlow)">
        <!-- Crown base -->
        <rect x="-22" y="8" width="44" height="12" rx="2" fill="url(#champGold)" stroke="#8B6914" stroke-width="1"/>
        <!-- Crown peaks -->
        <path d="M-22 8 L-18 -15 L-10 2 L0 -22 L10 2 L18 -15 L22 8" fill="url(#champGold)" stroke="#8B6914" stroke-width="1"/>
        <!-- Crown jewels -->
        <circle cx="-18" cy="-10" r="3" fill="#DC143C"/>
        <circle cx="0" cy="-17" r="4" fill="#1E90FF"/>
        <circle cx="18" cy="-10" r="3" fill="#DC143C"/>
        <!-- Base jewels -->
        <circle cx="-12" cy="14" r="2.5" fill="#32CD32"/>
        <circle cx="0" cy="14" r="2.5" fill="#FFE135"/>
        <circle cx="12" cy="14" r="2.5" fill="#32CD32"/>
        <!-- Crown shine -->
        <path d="M-18 -5 Q-15 -8 -12 -5" stroke="#ffffff" stroke-width="1" fill="none" opacity="0.5"/>
        <path d="M12 -5 Q15 -8 18 -5" stroke="#ffffff" stroke-width="1" fill="none" opacity="0.5"/>
    </g>

    <!-- Champion figures below -->
    <g transform="translate(50, 75)">
        <!-- Left champion -->
        <g transform="translate(-18, 0)" opacity="0.8">
            <circle cx="0" cy="0" r="6" fill="#ffffff"/>
            <ellipse cx="0" cy="14" rx="5" ry="8" fill="#ffffff"/>
            <circle cx="0" cy="-8" r="4" fill="#FFD700"/>
        </g>
        <!-- Center champion (larger) -->
        <g transform="translate(0, -5)">
            <circle cx="0" cy="0" r="8" fill="#ffffff"/>
            <ellipse cx="0" cy="18" rx="7" ry="10" fill="#ffffff"/>
            <circle cx="0" cy="-10" r="5" fill="#FFD700"/>
        </g>
        <!-- Right champion -->
        <g transform="translate(18, 0)" opacity="0.8">
            <circle cx="0" cy="0" r="6" fill="#ffffff"/>
            <ellipse cx="0" cy="14" rx="5" ry="8" fill="#ffffff"/>
            <circle cx="0" cy="-8" r="4" fill="#FFD700"/>
        </g>
    </g>

    <!-- Sparkles -->
    <circle cx="20" cy="30" r="2" fill="#ffffff" opacity="0.8"/>
    <circle cx="80" cy="35" r="1.5" fill="#FFE135" opacity="0.7"/>
    <circle cx="25" cy="55" r="1" fill="#ffffff" opacity="0.6"/>
    <circle cx="75" cy="50" r="1.5" fill="#ffffff" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render club experience icon SVG
 */
function renderClubExperienceIcon(): string {
    return <<<SVG
<svg class="exp-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
    <path d="M2 17L12 22L22 17" fill="none" stroke="currentColor" stroke-width="2"/>
    <path d="M2 12L12 17L22 12" fill="none" stroke="currentColor" stroke-width="2"/>
</svg>
SVG;
}

/**
 * Render complete club achievements section
 */
function renderClubAchievements(PDO $pdo, int $club_id, array $stats = null): string {
    // Get stats if not provided
    if ($stats === null) {
        $stats = getClubAchievementStats($pdo, $club_id);
    }

    // Calculate experience level
    $expLevel = calculateClubExperienceLevel($stats);
    $expLevelName = getClubExperienceLevelName($expLevel);
    $showLegend = ($expLevel === 6);

    ob_start();
    ?>
    <div class="achievements-card">
        <div class="achievements-card-header">
            <h3 class="achievements-card-title">Klubb Achievements</h3>
            <a href="/achievements#club" class="achievements-info-link"><i data-lucide="info"></i> Visa alla</a>
        </div>

        <!-- Club Experience Slider -->
        <div class="exp-section">
            <div class="exp-header">
                <div class="exp-label">
                    <?= renderClubExperienceIcon() ?>
                    <span class="exp-title"><?= htmlspecialchars($expLevelName) ?></span>
                </div>
                <span class="exp-since">Sedan <?= (int)$stats['first_season_year'] ?></span>
            </div>
            <div class="exp-slider">
                <?php for ($i = 1; $i <= 5; $i++): ?>
                    <div class="exp-step<?= $i <= $expLevel ? ' active' : '' ?>"></div>
                <?php endfor; ?>
                <div class="exp-step<?= $showLegend ? '' : ' hidden' ?><?= $expLevel === 6 ? ' active' : '' ?>"></div>
            </div>
            <div class="exp-labels">
                <span class="<?= $expLevel === 1 ? 'active' : '' ?>">Ny</span>
                <span class="<?= $expLevel === 2 ? 'active' : '' ?>">Etablerad</span>
                <span class="<?= $expLevel === 3 ? 'active' : '' ?>">Växande</span>
                <span class="<?= $expLevel === 4 ? 'active' : 'locked' ?>">Stark</span>
                <span class="<?= $expLevel >= 5 ? 'active' : 'locked' ?>">Elit</span>
                <?php if ($showLegend): ?>
                    <span class="<?= $expLevel === 6 ? 'active' : 'locked' ?>">Legend</span>
                <?php endif; ?>
            </div>
        </div>

        <!-- Club Badge Grid -->
        <div class="badge-grid club-badge-grid">
            <!-- Starter -->
            <div class="badge-item<?= $stats['total_starts'] === 0 ? ' locked' : '' ?>"
                 data-tooltip="Totalt antal starter"
                 data-level="<?= getBadgeLevel($stats['total_starts'], [10, 50, 100, 500]) ?>">
                <?= renderClubStarterBadge() ?>
                <span class="badge-value<?= $stats['total_starts'] === 0 ? ' empty' : '' ?>"><?= $stats['total_starts'] > 0 ? $stats['total_starts'] : '–' ?></span>
                <span class="badge-label">Starter</span>
            </div>

            <!-- Aktiva medlemmar -->
            <div class="badge-item<?= $stats['active_members'] === 0 ? ' locked' : '' ?>"
                 data-tooltip="Aktiva medlemmar (12 mån)"
                 data-level="<?= getBadgeLevel($stats['active_members'], [5, 15, 30, 50]) ?>">
                <?= renderClubActiveBadge() ?>
                <span class="badge-value<?= $stats['active_members'] === 0 ? ' empty' : '' ?>"><?= $stats['active_members'] > 0 ? $stats['active_members'] : '–' ?></span>
                <span class="badge-label">Aktiva</span>
            </div>

            <!-- Klubb-guld -->
            <div class="badge-item<?= $stats['total_gold'] === 0 ? ' locked' : '' ?>" data-tooltip="Totalt antal guld">
                <?= renderClubGoldBadge() ?>
                <span class="badge-value<?= $stats['total_gold'] === 0 ? ' empty' : '' ?>"><?= $stats['total_gold'] > 0 ? $stats['total_gold'] : '–' ?></span>
                <span class="badge-label">Klubb-guld</span>
            </div>

            <!-- Pallplatser -->
            <div class="badge-item<?= $stats['total_podiums'] === 0 ? ' locked' : '' ?>" data-tooltip="Totalt antal pallplatser">
                <?= renderClubPodiumBadge() ?>
                <span class="badge-value<?= $stats['total_podiums'] === 0 ? ' empty' : '' ?>"><?= $stats['total_podiums'] > 0 ? $stats['total_podiums'] : '–' ?></span>
                <span class="badge-label">Pallplatser</span>
            </div>

            <!-- Seriesegrar -->
            <div class="badge-item<?= $stats['series_wins'] === 0 ? ' locked' : '' ?><?= $stats['series_wins'] > 0 ? ' clickable' : '' ?>"
                 data-tooltip="Medlemmars seriesegrar"
                 data-achievement="series_champion"
                 data-label="Seriesegrar">
                <?= renderClubSeriesWinsBadge() ?>
                <span class="badge-value<?= $stats['series_wins'] === 0 ? ' empty' : '' ?>"><?= $stats['series_wins'] > 0 ? $stats['series_wins'] : '–' ?></span>
                <span class="badge-label">Seriesegrar</span>
            </div>

            <!-- SM-medaljer -->
            <div class="badge-item<?= $stats['sm_medals'] === 0 ? ' locked' : '' ?><?= $stats['sm_medals'] > 0 ? ' clickable' : '' ?>"
                 data-tooltip="SM-medaljer för klubben"
                 data-achievement="swedish_champion"
                 data-label="SM-medaljer">
                <?= renderClubSmMedalsBadge() ?>
                <span class="badge-value<?= $stats['sm_medals'] === 0 ? ' empty' : '' ?>"><?= $stats['sm_medals'] > 0 ? $stats['sm_medals'] : '–' ?></span>
                <span class="badge-label">SM-medaljer</span>
            </div>

            <!-- Bästa ranking -->
            <div class="badge-item<?= $stats['best_ranking'] === null ? ' locked' : '' ?><?= $stats['best_ranking'] === 1 ? ' glowing' : '' ?>"
                 data-tooltip="Klubbens bästa ranking"
                 data-glow="<?= $stats['best_ranking'] === 1 ? 'gold' : '' ?>">
                <?= renderClubRankingBadge($stats['best_ranking']) ?>
                <span class="badge-value<?= $stats['best_ranking'] === null ? ' empty' : '' ?>"><?= $stats['best_ranking'] !== null ? '#' . $stats['best_ranking'] : '–' ?></span>
                <span class="badge-label">Ranking</span>
            </div>

            <!-- Seriesegrar i klubben -->
            <div class="badge-item<?= $stats['series_wins'] === 0 ? ' locked' : '' ?><?= $stats['series_wins'] > 0 ? ' clickable' : '' ?>"
                 data-tooltip="<?= $stats['series_wins'] > 0 ? htmlspecialchars(implode(', ', $stats['champion_names'])) : 'Seriesegrar från klubben' ?>"
                 data-achievement="series_champion"
                 data-label="Seriesegrar">
                <?= renderClubChampionsBadge() ?>
                <span class="badge-value<?= $stats['series_wins'] === 0 ? ' empty' : '' ?>"><?= $stats['series_wins'] > 0 ? $stats['series_wins'] : '–' ?></span>
                <span class="badge-label">Seriesegrar</span>
            </div>
        </div>
    </div>
    <?php
    return ob_get_clean();
}

/**
 * Get all club achievement definitions for explanation page
 */
function getClubAchievementDefinitions(): array {
    return [
        'storlek' => [
            'title' => 'Storlek & Aktivitet',
            'icon' => 'users',
            'badges' => [
                [
                    'id' => 'starter',
                    'name' => 'Starter',
                    'requirement' => 'Totalt antal starter för klubben',
                    'description' => 'Räknar alla starter från klubbens medlemmar. Nivåer: Brons (10), Silver (50), Guld (100), Diamant (500).',
                    'has_counter' => true,
                    'has_levels' => true,
                    'accent' => '#61CE70',
                    'svg_function' => 'renderClubStarterBadge'
                ],
                [
                    'id' => 'active_members',
                    'name' => 'Aktiva Medlemmar',
                    'requirement' => 'Unika åkare som tävlat senaste 12 månader',
                    'description' => 'Räknar medlemmar som deltagit i minst ett lopp senaste året. Nivåer: Brons (5), Silver (15), Guld (30), Diamant (50).',
                    'has_counter' => true,
                    'has_levels' => true,
                    'accent' => '#004a98',
                    'svg_function' => 'renderClubActiveBadge'
                ]
            ]
        ],
        'prestationer' => [
            'title' => 'Prestationer',
            'icon' => 'trophy',
            'badges' => [
                [
                    'id' => 'club_gold',
                    'name' => 'Klubb-guld',
                    'requirement' => 'Totalt antal guld för klubben',
                    'description' => 'Summan av alla förstaplatser för klubbens medlemmar.',
                    'has_counter' => true,
                    'accent' => '#FFD700',
                    'svg_function' => 'renderClubGoldBadge'
                ],
                [
                    'id' => 'podiums',
                    'name' => 'Pallplatser',
                    'requirement' => 'Totalt antal pallplatser för klubben',
                    'description' => 'Summan av alla topp-3 placeringar för klubbens medlemmar.',
                    'has_counter' => true,
                    'accent' => 'gradient',
                    'svg_function' => 'renderClubPodiumBadge'
                ],
                [
                    'id' => 'series_wins',
                    'name' => 'Seriesegrar',
                    'requirement' => 'Antal seriesegrar för klubbens medlemmar',
                    'description' => 'Totalt antal gånger klubbens medlemmar vunnit en serietotal.',
                    'has_counter' => true,
                    'accent' => '#FFD700',
                    'svg_function' => 'renderClubSeriesWinsBadge'
                ],
                [
                    'id' => 'sm_medals',
                    'name' => 'SM-medaljer',
                    'requirement' => 'SM-medaljer för klubben',
                    'description' => 'Totalt antal SM-titlar för klubbens medlemmar.',
                    'has_counter' => true,
                    'accent' => '#004a98',
                    'svg_function' => 'renderClubSmMedalsBadge'
                ]
            ]
        ],
        'special' => [
            'title' => 'Special',
            'icon' => 'star',
            'badges' => [
                [
                    'id' => 'best_ranking',
                    'name' => 'Bästa Ranking',
                    'requirement' => 'Klubbens högsta ranking i serierna',
                    'description' => 'Visar klubbens bästa placering i aktuella serieställningar. Glöder extra om klubben är #1.',
                    'has_counter' => false,
                    'accent' => '#5F1D67',
                    'svg_function' => 'renderClubRankingBadge'
                ],
                [
                    'id' => 'series_champion',
                    'name' => 'Seriesegrar',
                    'requirement' => 'Antal seriesegrar från klubbens medlemmar',
                    'description' => 'Räknar totalt antal seriesegrar som klubbens medlemmar tagit.',
                    'has_counter' => true,
                    'accent' => '#FFE009',
                    'svg_function' => 'renderClubChampionsBadge'
                ]
            ]
        ],
        'experience' => [
            'title' => 'Klubb Erfarenhet',
            'icon' => 'layers',
            'badges' => [
                [
                    'id' => 'club_exp_1',
                    'name' => 'Ny Klubb',
                    'requirement' => 'Första säsongen',
                    'description' => 'Klubben har precis börjat på GravitySeries.',
                    'has_counter' => false,
                    'accent' => '#61CE70'
                ],
                [
                    'id' => 'club_exp_2',
                    'name' => 'Etablerad',
                    'requirement' => '2+ säsonger',
                    'description' => 'Klubben har varit med i minst 2 säsonger.',
                    'has_counter' => false,
                    'accent' => '#61CE70'
                ],
                [
                    'id' => 'club_exp_3',
                    'name' => 'Växande',
                    'requirement' => '10+ aktiva medlemmar',
                    'description' => 'Klubben har 10 eller fler aktiva medlemmar.',
                    'has_counter' => false,
                    'accent' => '#61CE70'
                ],
                [
                    'id' => 'club_exp_4',
                    'name' => 'Stark',
                    'requirement' => '25+ aktiva medlemmar',
                    'description' => 'Klubben har 25 eller fler aktiva medlemmar.',
                    'has_counter' => false,
                    'accent' => '#61CE70'
                ],
                [
                    'id' => 'club_exp_5',
                    'name' => 'Elitsklubb',
                    'requirement' => '50+ aktiva medlemmar ELLER 10+ seriesegrar',
                    'description' => 'Klubben har antingen 50+ aktiva eller 10+ seriesegrar.',
                    'has_counter' => false,
                    'accent' => '#FFD700'
                ],
                [
                    'id' => 'club_exp_6',
                    'name' => 'Legendklubb',
                    'requirement' => '100+ medlemmar OCH 25+ seriesegrar',
                    'description' => 'Endast för de största klubbarna. Dold tills uppnådd.',
                    'has_counter' => false,
                    'accent' => '#FFD700',
                    'hidden' => true
                ]
            ]
        ]
    ];
}
