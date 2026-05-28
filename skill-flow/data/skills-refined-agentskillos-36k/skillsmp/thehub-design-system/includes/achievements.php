<?php
/**
 * TheHUB Achievements System - Rider Badges
 * Hexagonal badge components with SVG icons
 * Supports both light and dark themes
 *
 * @version 2.1
 * @package TheHUB
 */

// Prevent direct access
if (!defined('DB_HOST') && !defined('THEHUB_LOADED')) {
    define('THEHUB_LOADED', true);
}

/**
 * Get rider stats for achievements
 */
function getRiderAchievementStats(PDO $pdo, int $rider_id): array {
    $stats = [
        'gold' => 0,
        'silver' => 0,
        'bronze' => 0,
        'hot_streak' => 0,
        'series_completed' => 0,
        'is_serieledare' => false,
        'series_wins' => 0,
        'sm_wins' => 0,
        'seasons_active' => 1,
        'has_series_win' => false,
        'first_season_year' => date('Y'),
        'finisher_100' => false,
        // Fun badges stats
        'total_races' => 0,
        'total_venues' => 0,
        'disciplines' => 0,
        'club_starts' => 0,
        'consecutive_seasons' => 0,
        'is_comeback' => false
    ];

    try {
        $stmt = $pdo->prepare("
            SELECT achievement_type, achievement_value, COUNT(*) as count
            FROM rider_achievements
            WHERE rider_id = ?
            GROUP BY achievement_type, achievement_value
        ");
        $stmt->execute([$rider_id]);
        $achievements = $stmt->fetchAll(PDO::FETCH_ASSOC);

        foreach ($achievements as $ach) {
            switch ($ach['achievement_type']) {
                case 'gold':
                    $stats['gold'] = (int)$ach['achievement_value'];
                    break;
                case 'silver':
                    $stats['silver'] = (int)$ach['achievement_value'];
                    break;
                case 'bronze':
                    $stats['bronze'] = (int)$ach['achievement_value'];
                    break;
                case 'hot_streak':
                    $stats['hot_streak'] = (int)$ach['achievement_value'];
                    break;
                case 'series_leader':
                    $stats['is_serieledare'] = true;
                    break;
                case 'series_champion':
                    $stats['series_wins']++;
                    $stats['has_series_win'] = true;
                    break;
                case 'swedish_champion':
                    $stats['sm_wins']++;
                    break;
                case 'finisher_100':
                    $stats['finisher_100'] = true;
                    $stats['series_completed']++;
                    break;
            }
        }

        // Get rider's first season year
        $stmt = $pdo->prepare("SELECT first_season FROM riders WHERE id = ?");
        $stmt->execute([$rider_id]);
        $rider = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($rider && !empty($rider['first_season'])) {
            $stats['first_season_year'] = (int)$rider['first_season'];
            $stats['seasons_active'] = (int)date('Y') - $stats['first_season_year'] + 1;
        }

        // Get total races for milestone badges
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ? AND status = 'finished'");
        $stmt->execute([$rider_id]);
        $stats['total_races'] = (int)$stmt->fetchColumn();

    } catch (PDOException $e) {
        // Silently fail, use defaults
    }

    return $stats;
}

/**
 * Get detailed achievement data for a specific achievement type
 * Returns full details including event/series names and links
 */
function getDetailedAchievements(PDO $pdo, int $rider_id, string $achievement_type): array {
    $stmt = $pdo->prepare("
        SELECT
            ra.id,
            ra.achievement_type,
            ra.achievement_value,
            ra.series_id,
            ra.season_year,
            ra.event_id,
            ra.earned_at,
            e.name as event_name,
            e.date as event_date,
            e.discipline,
            s.name as series_name,
            c.name as class_name
        FROM rider_achievements ra
        LEFT JOIN events e ON ra.event_id = e.id
        LEFT JOIN series s ON ra.series_id = s.id
        LEFT JOIN results r ON r.event_id = ra.event_id AND r.cyclist_id = ra.rider_id AND r.position = 1
        LEFT JOIN classes c ON r.class_id = c.id
        WHERE ra.rider_id = ? AND ra.achievement_type = ?
        ORDER BY ra.season_year DESC, ra.earned_at DESC
    ");
    $stmt->execute([$rider_id, $achievement_type]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get all achievements with details for a rider
 * Groups achievements by type with full metadata
 */
function getAllDetailedAchievements(PDO $pdo, int $rider_id): array {
    $achievements = [];

    // Swedish Championships
    $championships = getDetailedAchievements($pdo, $rider_id, 'swedish_champion');
    if (!empty($championships)) {
        $achievements['swedish_champion'] = [
            'label' => 'Svensk mästare',
            'count' => count($championships),
            'items' => $championships
        ];
    }

    // Series Championships
    $seriesWins = getDetailedAchievements($pdo, $rider_id, 'series_champion');
    if (!empty($seriesWins)) {
        $achievements['series_champion'] = [
            'label' => 'Serieseger',
            'count' => count($seriesWins),
            'items' => $seriesWins
        ];
    }

    // Finisher 100%
    $finisher = getDetailedAchievements($pdo, $rider_id, 'finisher_100');
    if (!empty($finisher)) {
        $achievements['finisher_100'] = [
            'label' => '100% Genomfört',
            'count' => count($finisher),
            'items' => $finisher
        ];
    }

    return $achievements;
}

/**
 * Get experience level name
 */
function getExperienceLevelName(int $level): string {
    $levels = [
        1 => '1:a året',
        2 => '2:a året',
        3 => 'Erfaren',
        4 => 'Expert',
        5 => 'Veteran',
        6 => 'Legend'
    ];
    return $levels[$level] ?? '1:a året';
}

/**
 * Calculate experience level (1-6)
 */
function calculateExperienceLevel(int $seasons, bool $has_series_win): int {
    if ($seasons >= 5 && $has_series_win) {
        return 6;
    }
    return min($seasons, 5);
}

// ============================================================================
// HEXAGONAL BADGE SVGs - Illustrated Collectible Style
// Zwift-inspired detailed badges in hexagon form for GravitySeries
// ViewBox: 100x116 for proper hexagon proportions
// ============================================================================

/**
 * Generate hexagonal badge base with gradient background
 * @param string $gradientStart - Top color of gradient
 * @param string $gradientEnd - Bottom color of gradient
 * @param string $strokeColor - Border color
 * @param string $uniqueId - Unique identifier for gradients
 */
function getHexagonBase(string $gradientStart, string $gradientEnd = '', string $strokeColor = '', string $uniqueId = ''): string {
    $id = $uniqueId ?: uniqid('badge-');
    $gradEnd = $gradientEnd ?: $gradientStart;
    $stroke = $strokeColor ?: $gradientStart;

    return <<<SVG
    <defs>
        <linearGradient id="bg-{$id}" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="{$gradientStart}"/>
            <stop offset="100%" stop-color="{$gradEnd}"/>
        </linearGradient>
        <filter id="shadow-{$id}">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.2"/>
        </filter>
        <clipPath id="hex-clip-{$id}">
            <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z"/>
        </clipPath>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z"
          fill="url(#bg-{$id})"
          stroke="{$stroke}"
          stroke-width="2.5"
          filter="url(#shadow-{$id})"/>
    <path d="M50 10L88 32V84L50 106L12 84V32L50 10Z"
          fill="none"
          stroke="{$stroke}"
          stroke-width="0.5"
          opacity="0.3"/>
SVG;
}

/**
 * Render illustrated gold badge SVG - Trophy with confetti
 */
function renderGoldBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="goldBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF8E1"/>
            <stop offset="100%" stop-color="#FFD54F"/>
        </linearGradient>
        <linearGradient id="trophyGold" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFE082"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
        <filter id="goldShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#goldBg)" stroke="#B8860B" stroke-width="2.5" filter="url(#goldShadow)"/>
    <!-- Light rays behind trophy -->
    <g opacity="0.4">
        <path d="M50 25L55 45L70 35L58 50L75 55L55 55L60 75L50 58L40 75L45 55L25 55L42 50L30 35L45 45Z" fill="#FFF9C4"/>
    </g>
    <!-- Confetti -->
    <rect x="18" y="30" width="5" height="10" rx="1" fill="#EF4444" transform="rotate(-15 18 30)"/>
    <rect x="78" y="35" width="5" height="10" rx="1" fill="#3B82F6" transform="rotate(20 78 35)"/>
    <rect x="22" y="75" width="5" height="10" rx="1" fill="#10B981" transform="rotate(-10 22 75)"/>
    <rect x="75" y="70" width="5" height="10" rx="1" fill="#F59E0B" transform="rotate(15 75 70)"/>
    <circle cx="12" cy="55" r="4" fill="#EC4899"/>
    <circle cx="88" cy="50" r="4" fill="#8B5CF6"/>
    <circle cx="15" cy="40" r="2.5" fill="#06B6D4"/>
    <circle cx="85" cy="75" r="2.5" fill="#F43F5E"/>
    <!-- Trophy shadow -->
    <ellipse cx="50" cy="95" rx="22" ry="6" fill="#000" opacity="0.1"/>
    <!-- Trophy cup -->
    <path d="M36 42H64V48H60C60 48 58 44 50 44C42 44 40 48 40 48H36V42Z" fill="#B8860B"/>
    <path d="M40 48V56C40 68 44 76 50 76C56 76 60 68 60 56V48H40Z" fill="url(#trophyGold)"/>
    <!-- Trophy highlight -->
    <path d="M44 50C44 50 46 54 46 62C46 68 45 72 45 72" stroke="#FFF8E1" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
    <!-- Handles -->
    <path d="M36 48C36 48 28 48 28 56C28 64 36 64 36 64" stroke="#B8860B" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M64 48C64 48 72 48 72 56C72 64 64 64 64 64" stroke="#B8860B" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M36 48C36 48 28 48 28 56C28 64 36 64 36 64" stroke="#FFD700" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M64 48C64 48 72 48 72 56C72 64 64 64 64 64" stroke="#FFD700" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- Stem and base -->
    <rect x="46" y="76" width="8" height="8" fill="url(#trophyGold)"/>
    <rect x="38" y="84" width="24" height="6" rx="2" fill="url(#trophyGold)"/>
    <rect x="34" y="90" width="32" height="4" rx="1" fill="#B8860B"/>
    <!-- Star on trophy -->
    <path d="M50 58L52 62L56 62.5L53 65.5L54 70L50 68L46 70L47 65.5L44 62.5L48 62Z" fill="#FFF8E1"/>
</svg>
SVG;
}

/**
 * Render illustrated silver badge SVG - Silver trophy
 */
function renderSilverBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="silverBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#F5F5F5"/>
            <stop offset="100%" stop-color="#BDBDBD"/>
        </linearGradient>
        <linearGradient id="trophySilver" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E0E0E0"/>
            <stop offset="50%" stop-color="#C0C0C0"/>
            <stop offset="100%" stop-color="#808080"/>
        </linearGradient>
        <filter id="silverShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#silverBg)" stroke="#808080" stroke-width="2.5" filter="url(#silverShadow)"/>
    <!-- Subtle sparkles -->
    <circle cx="20" cy="35" r="3" fill="#E0E0E0" opacity="0.6"/>
    <circle cx="80" cy="40" r="3" fill="#E0E0E0" opacity="0.6"/>
    <circle cx="25" cy="80" r="2" fill="#BDBDBD" opacity="0.5"/>
    <circle cx="75" cy="75" r="2" fill="#BDBDBD" opacity="0.5"/>
    <!-- Trophy shadow -->
    <ellipse cx="50" cy="95" rx="20" ry="5" fill="#000" opacity="0.08"/>
    <!-- Trophy cup -->
    <path d="M38 44H62V50H58C58 46 50 46 50 46C50 46 42 46 42 50H38V44Z" fill="#808080"/>
    <path d="M42 50V58C42 68 45 74 50 74C55 74 58 68 58 58V50H42Z" fill="url(#trophySilver)"/>
    <!-- Trophy highlight -->
    <path d="M45 52C45 52 47 56 47 62C47 66 46 70 46 70" stroke="#F5F5F5" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
    <!-- Handles -->
    <path d="M38 50C38 50 30 50 30 56C30 62 38 62 38 62" stroke="#808080" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M62 50C62 50 70 50 70 56C70 62 62 62 62 62" stroke="#808080" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M38 50C38 50 30 50 30 56C30 62 38 62 38 62" stroke="#C0C0C0" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path d="M62 50C62 50 70 50 70 56C70 62 62 62 62 62" stroke="#C0C0C0" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Stem and base -->
    <rect x="46" y="74" width="8" height="8" fill="url(#trophySilver)"/>
    <rect x="40" y="82" width="20" height="5" rx="2" fill="url(#trophySilver)"/>
    <rect x="36" y="87" width="28" height="4" rx="1" fill="#808080"/>
    <!-- Number 2 on trophy -->
    <text x="50" y="66" text-anchor="middle" fill="#F5F5F5" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">2</text>
</svg>
SVG;
}

/**
 * Render illustrated bronze badge SVG - Bronze trophy
 */
function renderBronzeBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bronzeBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFECB3"/>
            <stop offset="100%" stop-color="#D7A574"/>
        </linearGradient>
        <linearGradient id="trophyBronze" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#DEB887"/>
            <stop offset="50%" stop-color="#CD7F32"/>
            <stop offset="100%" stop-color="#8B4513"/>
        </linearGradient>
        <filter id="bronzeShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#bronzeBg)" stroke="#8B4513" stroke-width="2.5" filter="url(#bronzeShadow)"/>
    <!-- Warm glow spots -->
    <circle cx="22" cy="38" r="3" fill="#DEB887" opacity="0.5"/>
    <circle cx="78" cy="42" r="3" fill="#DEB887" opacity="0.5"/>
    <circle cx="18" cy="75" r="2" fill="#CD7F32" opacity="0.4"/>
    <circle cx="82" cy="70" r="2" fill="#CD7F32" opacity="0.4"/>
    <!-- Trophy shadow -->
    <ellipse cx="50" cy="95" rx="20" ry="5" fill="#000" opacity="0.08"/>
    <!-- Trophy cup -->
    <path d="M38 44H62V50H58C58 46 50 46 50 46C50 46 42 46 42 50H38V44Z" fill="#8B4513"/>
    <path d="M42 50V58C42 68 45 74 50 74C55 74 58 68 58 58V50H42Z" fill="url(#trophyBronze)"/>
    <!-- Trophy highlight -->
    <path d="M45 52C45 52 47 56 47 62C47 66 46 70 46 70" stroke="#FFECB3" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
    <!-- Handles -->
    <path d="M38 50C38 50 30 50 30 56C30 62 38 62 38 62" stroke="#8B4513" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M62 50C62 50 70 50 70 56C70 62 62 62 62 62" stroke="#8B4513" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M38 50C38 50 30 50 30 56C30 62 38 62 38 62" stroke="#CD7F32" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path d="M62 50C62 50 70 50 70 56C70 62 62 62 62 62" stroke="#CD7F32" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Stem and base -->
    <rect x="46" y="74" width="8" height="8" fill="url(#trophyBronze)"/>
    <rect x="40" y="82" width="20" height="5" rx="2" fill="url(#trophyBronze)"/>
    <rect x="36" y="87" width="28" height="4" rx="1" fill="#8B4513"/>
    <!-- Number 3 on trophy -->
    <text x="50" y="66" text-anchor="middle" fill="#FFECB3" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">3</text>
</svg>
SVG;
}

/**
 * Render illustrated hot streak (pallserie) badge SVG - Three trophies with flames
 */
function renderHotStreakBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="hotstreakBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF3E0"/>
            <stop offset="100%" stop-color="#FFAB91"/>
        </linearGradient>
        <linearGradient id="flameGrad" x1="50%" y1="100%" x2="50%" y2="0%">
            <stop offset="0%" stop-color="#FF5722"/>
            <stop offset="50%" stop-color="#FF9800"/>
            <stop offset="100%" stop-color="#FFC107"/>
        </linearGradient>
        <filter id="hotstreakShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#hotstreakBg)" stroke="#FF5722" stroke-width="2.5" filter="url(#hotstreakShadow)"/>
    <!-- Flames behind -->
    <path d="M30 75C30 55 40 45 50 35C60 45 70 55 70 75C70 85 60 95 50 95C40 95 30 85 30 75Z" fill="url(#flameGrad)" opacity="0.4"/>
    <path d="M38 80C38 65 45 55 50 48C55 55 62 65 62 80C62 88 56 93 50 93C44 93 38 88 38 80Z" fill="url(#flameGrad)" opacity="0.6"/>
    <!-- Silver trophy (left) -->
    <rect x="18" y="60" width="14" height="22" rx="2" fill="#C0C0C0"/>
    <rect x="21" y="82" width="8" height="3" fill="#808080"/>
    <rect x="19" y="85" width="12" height="3" rx="1" fill="#808080"/>
    <path d="M22 64C22 64 25 68 25 74C25 78 23 80 23 80" stroke="#E0E0E0" stroke-width="1.5" opacity="0.5"/>
    <!-- Gold trophy (center, tallest) -->
    <rect x="40" y="48" width="20" height="32" rx="3" fill="#FFD700"/>
    <rect x="44" y="80" width="12" height="4" fill="#B8860B"/>
    <rect x="42" y="84" width="16" height="4" rx="1" fill="#B8860B"/>
    <path d="M45 54C45 54 48 60 48 70C48 76 46 78 46 78" stroke="#FFF8E1" stroke-width="2" opacity="0.6"/>
    <!-- Star on gold trophy -->
    <path d="M50 60L52 64L56 64.5L53 67L54 71L50 69L46 71L47 67L44 64.5L48 64Z" fill="#FFF8E1"/>
    <!-- Bronze trophy (right) -->
    <rect x="68" y="65" width="14" height="18" rx="2" fill="#CD7F32"/>
    <rect x="71" y="83" width="8" height="3" fill="#8B4513"/>
    <rect x="69" y="86" width="12" height="2" rx="1" fill="#8B4513"/>
    <path d="M72 68C72 68 74 72 74 76C74 79 73 81 73 81" stroke="#DEB887" stroke-width="1.5" opacity="0.5"/>
    <!-- Fire sparks -->
    <circle cx="35" cy="40" r="3" fill="#FF9800" opacity="0.7"/>
    <circle cx="65" cy="38" r="3" fill="#FFC107" opacity="0.7"/>
    <circle cx="50" cy="28" r="4" fill="#FF5722" opacity="0.6"/>
</svg>
SVG;
}

/**
 * Render illustrated fullföljare badge SVG - Checkered flag with cyclist crossing
 */
function renderFinisherBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="finisherBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <filter id="finisherShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#finisherBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#finisherShadow)"/>
    <!-- Checkered flag pattern -->
    <g transform="translate(55, 25) rotate(15)">
        <rect x="0" y="0" width="30" height="40" fill="none" stroke="#333" stroke-width="1"/>
        <!-- Checkered squares -->
        <rect x="0" y="0" width="7.5" height="8" fill="#333"/>
        <rect x="15" y="0" width="7.5" height="8" fill="#333"/>
        <rect x="7.5" y="8" width="7.5" height="8" fill="#333"/>
        <rect x="22.5" y="8" width="7.5" height="8" fill="#333"/>
        <rect x="0" y="16" width="7.5" height="8" fill="#333"/>
        <rect x="15" y="16" width="7.5" height="8" fill="#333"/>
        <rect x="7.5" y="24" width="7.5" height="8" fill="#333"/>
        <rect x="22.5" y="24" width="7.5" height="8" fill="#333"/>
        <rect x="0" y="32" width="7.5" height="8" fill="#333"/>
        <rect x="15" y="32" width="7.5" height="8" fill="#333"/>
        <!-- Flag pole -->
        <rect x="-3" y="-5" width="3" height="50" fill="#8B4513"/>
    </g>
    <!-- Cyclist silhouette crossing finish -->
    <g transform="translate(25, 55)">
        <!-- Bike wheels -->
        <circle cx="12" cy="30" r="10" fill="none" stroke="#333" stroke-width="2"/>
        <circle cx="38" cy="30" r="10" fill="none" stroke="#333" stroke-width="2"/>
        <!-- Bike frame -->
        <path d="M12 30 L25 15 L38 30 M25 15 L25 25 L12 30 M25 25 L38 30" stroke="#333" stroke-width="2" fill="none"/>
        <!-- Cyclist body -->
        <circle cx="25" cy="8" r="6" fill="#61CE70"/>
        <path d="M20 15 L25 25 M30 15 L25 25" stroke="#61CE70" stroke-width="3" stroke-linecap="round"/>
        <!-- Arms raised in victory -->
        <path d="M18 12 L10 2 M32 12 L40 2" stroke="#61CE70" stroke-width="3" stroke-linecap="round"/>
    </g>
    <!-- 100% circle indicator -->
    <circle cx="75" cy="85" r="12" fill="#4CAF50"/>
    <text x="75" y="89" text-anchor="middle" fill="#FFF" font-size="8" font-weight="bold" font-family="system-ui">100%</text>
</svg>
SVG;
}

/**
 * Render illustrated serieledare badge SVG - Crown on helmet with #1
 */
function renderSeriesLeaderBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="leaderBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF3E0"/>
            <stop offset="100%" stop-color="#FFCC80"/>
        </linearGradient>
        <linearGradient id="helmetGrad" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#EF761F"/>
            <stop offset="100%" stop-color="#D84315"/>
        </linearGradient>
        <filter id="leaderShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#leaderBg)" stroke="#EF761F" stroke-width="2.5" filter="url(#leaderShadow)"/>
    <!-- Crown -->
    <g transform="translate(50, 28)">
        <path d="M-25 0 L-20 -18 L-10 -8 L0 -20 L10 -8 L20 -18 L25 0 Z" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
        <!-- Jewels on crown -->
        <circle cx="-20" cy="-14" r="3" fill="#E53935"/>
        <circle cx="0" cy="-16" r="4" fill="#1E88E5"/>
        <circle cx="20" cy="-14" r="3" fill="#43A047"/>
        <!-- Crown base -->
        <rect x="-25" y="0" width="50" height="6" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
    </g>
    <!-- Helmet -->
    <ellipse cx="50" cy="58" rx="28" ry="20" fill="url(#helmetGrad)"/>
    <path d="M22 58 Q22 75 50 80 Q78 75 78 58" fill="#EF761F"/>
    <!-- Helmet visor -->
    <ellipse cx="50" cy="65" rx="20" ry="8" fill="#333" opacity="0.8"/>
    <!-- Helmet highlight -->
    <path d="M30 50 Q40 45 55 48" stroke="#FFAB91" stroke-width="2" fill="none" opacity="0.6"/>
    <!-- Number plate -->
    <rect x="35" y="82" width="30" height="18" rx="3" fill="#FFF" stroke="#333" stroke-width="1"/>
    <text x="50" y="96" text-anchor="middle" fill="#333" font-size="14" font-weight="bold" font-family="system-ui">1</text>
</svg>
SVG;
}

/**
 * Render illustrated seriemästare badge SVG - Epic crown with jewels (LEGENDARY)
 */
function renderSeriesChampionBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="champBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF8E1"/>
            <stop offset="100%" stop-color="#FFD54F"/>
        </linearGradient>
        <linearGradient id="champCrown" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFE082"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
        <filter id="champGlow">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="champShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#champBg)" stroke="#B8860B" stroke-width="2.5" filter="url(#champShadow)"/>
    <!-- Radiant glow behind crown -->
    <g opacity="0.3" filter="url(#champGlow)">
        <path d="M50 20L55 50L80 35L60 55L85 60L55 60L65 85L50 62L35 85L45 60L15 60L40 55L20 35L45 50Z" fill="#FFD700"/>
    </g>
    <!-- Stars decoration -->
    <path d="M20 30L22 34L26 34L23 37L24 41L20 38L16 41L17 37L14 34L18 34Z" fill="#FFD700" opacity="0.8"/>
    <path d="M80 30L82 34L86 34L83 37L84 41L80 38L76 41L77 37L74 34L78 34Z" fill="#FFD700" opacity="0.8"/>
    <path d="M15 70L16 73L19 73L17 75L17.5 78L15 76L12.5 78L13 75L11 73L14 73Z" fill="#FFD700" opacity="0.6"/>
    <path d="M85 70L86 73L89 73L87 75L87.5 78L85 76L82.5 78L83 75L81 73L84 73Z" fill="#FFD700" opacity="0.6"/>
    <!-- Confetti -->
    <rect x="25" y="85" width="4" height="8" rx="1" fill="#E53935" transform="rotate(-10 25 85)"/>
    <rect x="72" y="82" width="4" height="8" rx="1" fill="#1E88E5" transform="rotate(15 72 82)"/>
    <circle cx="18" cy="55" r="3" fill="#43A047"/>
    <circle cx="82" cy="50" r="3" fill="#9C27B0"/>
    <!-- Majestic Crown -->
    <g transform="translate(50, 50)">
        <path d="M-30 10 L-25 -25 L-12 -10 L0 -35 L12 -10 L25 -25 L30 10 Z" fill="url(#champCrown)" stroke="#B8860B" stroke-width="1.5"/>
        <!-- Large jewels -->
        <circle cx="-25" cy="-20" r="5" fill="#E53935" stroke="#B71C1C" stroke-width="0.5"/>
        <circle cx="0" cy="-30" r="7" fill="#1E88E5" stroke="#0D47A1" stroke-width="0.5"/>
        <circle cx="25" cy="-20" r="5" fill="#43A047" stroke="#1B5E20" stroke-width="0.5"/>
        <!-- Crown base with gems -->
        <rect x="-30" y="10" width="60" height="10" rx="2" fill="url(#champCrown)" stroke="#B8860B" stroke-width="1"/>
        <circle cx="-20" cy="15" r="3" fill="#9C27B0"/>
        <circle cx="0" cy="15" r="3" fill="#FF9800"/>
        <circle cx="20" cy="15" r="3" fill="#00BCD4"/>
        <!-- Small jewels on spikes -->
        <circle cx="-12" cy="-7" r="3" fill="#FFD700" stroke="#B8860B" stroke-width="0.5"/>
        <circle cx="12" cy="-7" r="3" fill="#FFD700" stroke="#B8860B" stroke-width="0.5"/>
    </g>
    <!-- Pillow/cushion under crown -->
    <ellipse cx="50" cy="72" rx="32" ry="10" fill="#7B1FA2" opacity="0.3"/>
    <ellipse cx="50" cy="70" rx="30" ry="8" fill="#9C27B0"/>
    <path d="M25 70 Q50 62 75 70" stroke="#E1BEE7" stroke-width="2" fill="none" opacity="0.5"/>
</svg>
SVG;
}

/**
 * Render illustrated SM-vinnare badge SVG - Swedish crown with flag (LEGENDARY)
 */
function renderSwedishChampionBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="smBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E3F2FD"/>
            <stop offset="100%" stop-color="#90CAF9"/>
        </linearGradient>
        <linearGradient id="smCrown" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFE082"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#B8860B"/>
        </linearGradient>
        <filter id="smGlow">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="smShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#smBg)" stroke="#004B87" stroke-width="2.5" filter="url(#smShadow)"/>
    <!-- Swedish flag background -->
    <g clip-path="url(#smClip)">
        <rect x="15" y="35" width="70" height="50" rx="4" fill="#004B87"/>
        <rect x="35" y="35" width="12" height="50" fill="#FECC00"/>
        <rect x="15" y="52" width="70" height="12" fill="#FECC00"/>
    </g>
    <!-- Swedish style crown (Kungakrona) -->
    <g transform="translate(50, 32)" filter="url(#smGlow)">
        <!-- Crown base arches -->
        <path d="M-28 5 Q-28 -5 -20 -5 Q-12 -5 -12 5" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <path d="M-12 5 Q-12 -5 0 -12 Q12 -5 12 5" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <path d="M12 5 Q12 -5 20 -5 Q28 -5 28 5" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <!-- Crown orbs -->
        <circle cx="-20" cy="-8" r="5" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <circle cx="0" cy="-16" r="6" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <circle cx="20" cy="-8" r="5" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <!-- Cross on top -->
        <rect x="-2" y="-28" width="4" height="14" fill="#FFD700" stroke="#B8860B" stroke-width="0.5"/>
        <rect x="-6" y="-24" width="12" height="4" fill="#FFD700" stroke="#B8860B" stroke-width="0.5"/>
        <!-- Crown band -->
        <rect x="-28" y="5" width="56" height="8" rx="2" fill="url(#smCrown)" stroke="#B8860B" stroke-width="1"/>
        <!-- Gems on band -->
        <circle cx="-18" cy="9" r="2.5" fill="#004B87"/>
        <circle cx="0" cy="9" r="2.5" fill="#004B87"/>
        <circle cx="18" cy="9" r="2.5" fill="#004B87"/>
    </g>
    <!-- SM text badge -->
    <rect x="35" y="88" width="30" height="18" rx="4" fill="#FFD700" stroke="#B8860B" stroke-width="1.5"/>
    <text x="50" y="101" text-anchor="middle" fill="#004B87" font-size="12" font-weight="bold" font-family="system-ui">SM</text>
    <!-- Swedish decorative elements -->
    <circle cx="20" cy="28" r="4" fill="#FECC00" opacity="0.6"/>
    <circle cx="80" cy="28" r="4" fill="#FECC00" opacity="0.6"/>
</svg>
SVG;
}

// ============================================================================
// FUN BADGES - Loyalty & Endurance
// ============================================================================

/**
 * Render IronRider badge - All series in one season
 * (Renamed from Järnman to IronRider)
 */
function renderIronmanBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="ironBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#ECEFF1"/>
            <stop offset="100%" stop-color="#90A4AE"/>
        </linearGradient>
        <linearGradient id="ironMetal" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#B0BEC5"/>
            <stop offset="50%" stop-color="#78909C"/>
            <stop offset="100%" stop-color="#455A64"/>
        </linearGradient>
        <filter id="ironShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
        <filter id="ironGlow">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#ironBg)" stroke="#455A64" stroke-width="2.5" filter="url(#ironShadow)"/>
    <!-- Metallic cyclist silhouette -->
    <g transform="translate(50, 55)">
        <!-- Bike wheels -->
        <circle cx="-18" cy="25" r="14" fill="none" stroke="url(#ironMetal)" stroke-width="3"/>
        <circle cx="18" cy="25" r="14" fill="none" stroke="url(#ironMetal)" stroke-width="3"/>
        <!-- Wheel spokes -->
        <g stroke="#607D8B" stroke-width="1" opacity="0.6">
            <line x1="-18" y1="11" x2="-18" y2="39"/>
            <line x1="-32" y1="25" x2="-4" y2="25"/>
            <line x1="18" y1="11" x2="18" y2="39"/>
            <line x1="4" y1="25" x2="32" y2="25"/>
        </g>
        <!-- Bike frame -->
        <path d="M-18 25 L0 5 L18 25 M0 5 L0 18 L-18 25 M0 18 L18 25" stroke="url(#ironMetal)" stroke-width="3" fill="none"/>
        <!-- Cyclist body (metallic) -->
        <circle cx="0" cy="-10" r="10" fill="url(#ironMetal)"/>
        <path d="M-8 0 L0 18 M8 0 L0 18" stroke="url(#ironMetal)" stroke-width="4" stroke-linecap="round"/>
        <!-- Arm forward (riding position) -->
        <path d="M-6 -5 L-15 5 M6 -5 L15 5" stroke="url(#ironMetal)" stroke-width="3" stroke-linecap="round"/>
        <!-- Helmet shine -->
        <path d="M-5 -15 Q0 -20 5 -15" stroke="#CFD8DC" stroke-width="2" fill="none" opacity="0.7"/>
    </g>
    <!-- "IRON" badge ribbon -->
    <path d="M20 85 L50 92 L80 85 L80 100 L50 107 L20 100 Z" fill="#455A64"/>
    <path d="M25 87 L50 93 L75 87 L75 98 L50 104 L25 98 Z" fill="#607D8B"/>
    <text x="50" y="99" text-anchor="middle" fill="#ECEFF1" font-size="10" font-weight="bold" font-family="system-ui">IRON</text>
    <!-- Metallic shine effects -->
    <circle cx="25" cy="30" r="3" fill="#CFD8DC" opacity="0.5"/>
    <circle cx="75" cy="35" r="3" fill="#CFD8DC" opacity="0.5"/>
</svg>
SVG;
}

/**
 * Render Klubbhjälte badge - 10+ starts for same club
 */
function renderClubHeroBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="clubheroBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E3F2FD"/>
            <stop offset="100%" stop-color="#90CAF9"/>
        </linearGradient>
        <linearGradient id="shieldGrad" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#1976D2"/>
            <stop offset="100%" stop-color="#0D47A1"/>
        </linearGradient>
        <filter id="clubheroShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#clubheroBg)" stroke="#1976D2" stroke-width="2.5" filter="url(#clubheroShadow)"/>
    <!-- Shield shape -->
    <path d="M50 20 L78 32 L78 60 Q78 85 50 100 Q22 85 22 60 L22 32 Z" fill="url(#shieldGrad)" stroke="#0D47A1" stroke-width="2"/>
    <!-- Inner shield decoration -->
    <path d="M50 28 L70 38 L70 58 Q70 78 50 90 Q30 78 30 58 L30 38 Z" fill="none" stroke="#64B5F6" stroke-width="1.5" opacity="0.6"/>
    <!-- Heart in center -->
    <g transform="translate(50, 55)">
        <path d="M0 -8 C-5 -18 -20 -15 -20 -2 C-20 8 0 22 0 22 C0 22 20 8 20 -2 C20 -15 5 -18 0 -8 Z" fill="#E53935"/>
        <!-- Heart shine -->
        <path d="M-8 -8 Q-5 -12 -2 -8" stroke="#FFCDD2" stroke-width="2" fill="none" opacity="0.7"/>
    </g>
    <!-- Hands holding together (community) -->
    <g transform="translate(50, 85)" opacity="0.9">
        <path d="M-15 0 L-8 -5 L0 0 L8 -5 L15 0" stroke="#FFD700" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>
    <!-- Stars decoration -->
    <circle cx="25" cy="35" r="3" fill="#FFD700" opacity="0.7"/>
    <circle cx="75" cy="35" r="3" fill="#FFD700" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render Trogen badge - 3+ consecutive seasons (chain links)
 */
function renderLoyalBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="loyalBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <linearGradient id="chainGrad" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#81C784"/>
            <stop offset="100%" stop-color="#388E3C"/>
        </linearGradient>
        <filter id="loyalShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#loyalBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#loyalShadow)"/>
    <!-- Chain link 1 (left) -->
    <g transform="translate(28, 58)">
        <ellipse cx="0" cy="0" rx="12" ry="18" fill="none" stroke="url(#chainGrad)" stroke-width="6"/>
        <ellipse cx="0" cy="0" rx="12" ry="18" fill="none" stroke="#81C784" stroke-width="2"/>
    </g>
    <!-- Chain link 2 (center) - interlocked -->
    <g transform="translate(50, 58)">
        <ellipse cx="0" cy="0" rx="12" ry="18" fill="none" stroke="url(#chainGrad)" stroke-width="6"/>
        <ellipse cx="0" cy="0" rx="12" ry="18" fill="none" stroke="#81C784" stroke-width="2"/>
    </g>
    <!-- Chain link 3 (right) -->
    <g transform="translate(72, 58)">
        <ellipse cx="0" cy="0" rx="12" ry="18" fill="none" stroke="url(#chainGrad)" stroke-width="6"/>
        <ellipse cx="0" cy="0" rx="12" ry="18" fill="none" stroke="#81C784" stroke-width="2"/>
    </g>
    <!-- Connection points (overlap effect) -->
    <rect x="34" y="50" width="10" height="16" fill="url(#loyalBg)"/>
    <rect x="56" y="50" width="10" height="16" fill="url(#loyalBg)"/>
    <!-- "3+" indicator -->
    <circle cx="50" cy="28" r="12" fill="#4CAF50"/>
    <text x="50" y="33" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold" font-family="system-ui">3+</text>
    <!-- Years text -->
    <text x="50" y="100" text-anchor="middle" fill="#388E3C" font-size="10" font-weight="600" font-family="system-ui">SÄSONGER</text>
</svg>
SVG;
}

/**
 * Render Comeback badge - Phoenix rising from ashes
 */
function renderComebackBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="comebackBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF3E0"/>
            <stop offset="100%" stop-color="#FFCC80"/>
        </linearGradient>
        <linearGradient id="phoenixGrad" x1="50%" y1="100%" x2="50%" y2="0%">
            <stop offset="0%" stop-color="#E65100"/>
            <stop offset="50%" stop-color="#FF6D00"/>
            <stop offset="100%" stop-color="#FFAB00"/>
        </linearGradient>
        <linearGradient id="fireGrad" x1="50%" y1="100%" x2="50%" y2="0%">
            <stop offset="0%" stop-color="#BF360C"/>
            <stop offset="50%" stop-color="#FF5722"/>
            <stop offset="100%" stop-color="#FFC107"/>
        </linearGradient>
        <filter id="comebackShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
        <filter id="fireGlow">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#comebackBg)" stroke="#EF6C00" stroke-width="2.5" filter="url(#comebackShadow)"/>
    <!-- Flames/ashes at bottom -->
    <g filter="url(#fireGlow)">
        <path d="M25 100 Q35 80 50 90 Q65 80 75 100" fill="url(#fireGrad)" opacity="0.5"/>
        <path d="M30 100 Q40 85 50 92 Q60 85 70 100" fill="url(#fireGrad)" opacity="0.7"/>
    </g>
    <!-- Phoenix bird rising -->
    <g transform="translate(50, 55)">
        <!-- Body -->
        <ellipse cx="0" cy="10" rx="12" ry="20" fill="url(#phoenixGrad)"/>
        <!-- Head -->
        <circle cx="0" cy="-18" r="10" fill="url(#phoenixGrad)"/>
        <!-- Beak -->
        <path d="M0 -15 L5 -10 L0 -8 L-5 -10 Z" fill="#FFD54F"/>
        <!-- Eye -->
        <circle cx="-3" cy="-20" r="2" fill="#1A1A1A"/>
        <circle cx="-2" cy="-21" r="0.5" fill="#FFF"/>
        <!-- Wings spread upward -->
        <path d="M-10 5 Q-35 -20 -25 -40 Q-15 -25 -5 -10" fill="url(#phoenixGrad)"/>
        <path d="M10 5 Q35 -20 25 -40 Q15 -25 5 -10" fill="url(#phoenixGrad)"/>
        <!-- Wing details -->
        <path d="M-15 -5 Q-25 -15 -20 -30" stroke="#FFAB00" stroke-width="1.5" fill="none" opacity="0.7"/>
        <path d="M15 -5 Q25 -15 20 -30" stroke="#FFAB00" stroke-width="1.5" fill="none" opacity="0.7"/>
        <!-- Tail feathers -->
        <path d="M-5 30 Q-10 45 -15 50" stroke="url(#fireGrad)" stroke-width="3" fill="none"/>
        <path d="M0 30 Q0 48 0 55" stroke="url(#fireGrad)" stroke-width="3" fill="none"/>
        <path d="M5 30 Q10 45 15 50" stroke="url(#fireGrad)" stroke-width="3" fill="none"/>
    </g>
    <!-- Sparkles around phoenix -->
    <circle cx="20" cy="30" r="3" fill="#FFD700" opacity="0.8"/>
    <circle cx="80" cy="35" r="3" fill="#FFD700" opacity="0.8"/>
    <circle cx="25" cy="60" r="2" fill="#FF9800" opacity="0.6"/>
    <circle cx="75" cy="55" r="2" fill="#FF9800" opacity="0.6"/>
</svg>
SVG;
}

// ============================================================================
// FUN BADGES - Exploration
// ============================================================================

/**
 * Render Allrounder badge - 4 discipline icons in pattern
 */
function renderAllrounderBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="allroundBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#F3E5F5"/>
            <stop offset="100%" stop-color="#CE93D8"/>
        </linearGradient>
        <filter id="allroundShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#allroundBg)" stroke="#9C27B0" stroke-width="2.5" filter="url(#allroundShadow)"/>
    <!-- Central circle connecting all -->
    <circle cx="50" cy="58" r="30" fill="none" stroke="#9C27B0" stroke-width="2" opacity="0.3"/>
    <!-- Enduro icon (top-left) - Mountain -->
    <g transform="translate(28, 40)">
        <path d="M0 20 L12 0 L24 20 Z" fill="#FFE009" stroke="#F9A825" stroke-width="1"/>
        <path d="M8 20 L12 12 L16 20" fill="#FFF59D"/>
    </g>
    <!-- DH icon (top-right) - Down arrow -->
    <g transform="translate(60, 35)">
        <circle cx="10" cy="10" r="12" fill="#5F1D67"/>
        <path d="M10 4 L10 16 M5 12 L10 17 L15 12" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round"/>
    </g>
    <!-- XCO icon (bottom-left) - Circle track -->
    <g transform="translate(20, 65)">
        <circle cx="12" cy="12" r="12" fill="#004a98"/>
        <circle cx="12" cy="12" r="7" fill="none" stroke="#FFF" stroke-width="2"/>
        <circle cx="12" cy="12" r="2" fill="#FFF"/>
    </g>
    <!-- Dual icon (bottom-right) - Two arrows -->
    <g transform="translate(56, 65)">
        <circle cx="14" cy="14" r="14" fill="#61CE70"/>
        <path d="M8 8 L8 20 M20 8 L20 20 M5 12 L8 8 L11 12 M17 12 L20 8 L23 12" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round"/>
    </g>
    <!-- Center connector star -->
    <circle cx="50" cy="58" r="8" fill="#9C27B0"/>
    <text x="50" y="62" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">4</text>
    <!-- Text label -->
    <text x="50" y="102" text-anchor="middle" fill="#7B1FA2" font-size="9" font-weight="600" font-family="system-ui">ALLROUND</text>
</svg>
SVG;
}

/**
 * Render Äventyrare badge - Mountain with flag (5+ venues)
 */
function renderAdventurerBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="adventureBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <linearGradient id="mountainGrad" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#66BB6A"/>
            <stop offset="100%" stop-color="#2E7D32"/>
        </linearGradient>
        <filter id="adventureShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#adventureBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#adventureShadow)"/>
    <!-- Background mountains -->
    <path d="M10 90 L30 55 L45 70 L60 45 L75 65 L90 90 Z" fill="#81C784" opacity="0.5"/>
    <!-- Main mountain -->
    <path d="M15 95 L50 35 L85 95 Z" fill="url(#mountainGrad)"/>
    <!-- Snow cap -->
    <path d="M50 35 L40 55 L45 50 L50 55 L55 50 L60 55 Z" fill="#FAFAFA"/>
    <!-- Flag on top -->
    <g transform="translate(50, 25)">
        <rect x="-1" y="-10" width="2" height="20" fill="#8B4513"/>
        <path d="M1 -10 L18 -5 L1 0 Z" fill="#E53935"/>
        <!-- Flag shine -->
        <path d="M3 -8 L12 -5" stroke="#FFCDD2" stroke-width="1" opacity="0.6"/>
    </g>
    <!-- Trail path up mountain -->
    <path d="M25 90 Q35 75 40 65 Q50 50 50 45" stroke="#FFF" stroke-width="2" stroke-dasharray="4 3" fill="none" opacity="0.6"/>
    <!-- Location markers -->
    <circle cx="30" cy="80" r="4" fill="#FFD700"/>
    <circle cx="45" cy="65" r="4" fill="#FFD700"/>
    <circle cx="55" cy="55" r="4" fill="#FFD700"/>
    <circle cx="65" cy="70" r="4" fill="#FFD700"/>
    <circle cx="50" cy="38" r="4" fill="#FFD700"/>
    <!-- "5+" badge -->
    <circle cx="78" cy="30" r="10" fill="#4CAF50"/>
    <text x="78" y="34" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">5+</text>
</svg>
SVG;
}

/**
 * Render Nomad badge - Map with many location pins (10+ venues)
 */
function renderNomadBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="nomadBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFFDE7"/>
            <stop offset="100%" stop-color="#FFF59D"/>
        </linearGradient>
        <linearGradient id="mapGrad" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFECB3"/>
            <stop offset="100%" stop-color="#FFE082"/>
        </linearGradient>
        <filter id="nomadShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#nomadBg)" stroke="#FFC107" stroke-width="2.5" filter="url(#nomadShadow)"/>
    <!-- Map (rolled parchment style) -->
    <path d="M15 30 Q12 30 12 35 L12 85 Q12 90 17 90 L83 90 Q88 90 88 85 L88 35 Q88 30 85 30 Z" fill="url(#mapGrad)" stroke="#D4A54A" stroke-width="1.5"/>
    <!-- Map lines (terrain) -->
    <path d="M20 45 Q35 40 50 48 Q65 56 80 50" stroke="#D4A54A" stroke-width="1" fill="none" opacity="0.4"/>
    <path d="M20 60 Q40 55 60 62 Q75 68 80 65" stroke="#D4A54A" stroke-width="1" fill="none" opacity="0.4"/>
    <path d="M20 75 Q30 70 45 75 Q60 80 80 72" stroke="#D4A54A" stroke-width="1" fill="none" opacity="0.4"/>
    <!-- Dotted travel path connecting pins -->
    <path d="M25 40 Q35 55 45 50 Q55 45 50 60 Q45 75 60 70 Q75 65 75 50 Q75 35 60 38" stroke="#E65100" stroke-width="1.5" stroke-dasharray="3 2" fill="none"/>
    <!-- Location pins (10) -->
    <g fill="#E53935">
        <path d="M25 42 C25 36 20 33 20 38 C20 43 25 48 25 48 C25 48 30 43 30 38 C30 33 25 36 25 42 Z"/>
        <path d="M45 52 C45 46 40 43 40 48 C40 53 45 58 45 58 C45 58 50 53 50 48 C50 43 45 46 45 52 Z"/>
        <path d="M35 65 C35 59 30 56 30 61 C30 66 35 71 35 71 C35 71 40 66 40 61 C40 56 35 59 35 65 Z"/>
        <path d="M55 45 C55 39 50 36 50 41 C50 46 55 51 55 51 C55 51 60 46 60 41 C60 36 55 39 55 45 Z"/>
        <path d="M70 55 C70 49 65 46 65 51 C65 56 70 61 70 61 C70 61 75 56 75 51 C75 46 70 49 70 55 Z"/>
        <path d="M60 72 C60 66 55 63 55 68 C55 73 60 78 60 78 C60 78 65 73 65 68 C65 63 60 66 60 72 Z"/>
        <path d="M75 40 C75 34 70 31 70 36 C70 41 75 46 75 46 C75 46 80 41 80 36 C80 31 75 34 75 40 Z"/>
        <path d="M22 58 C22 52 17 49 17 54 C17 59 22 64 22 64 C22 64 27 59 27 54 C27 49 22 52 22 58 Z"/>
        <path d="M78 68 C78 62 73 59 73 64 C73 69 78 74 78 74 C78 74 83 69 83 64 C83 59 78 62 78 68 Z"/>
        <path d="M50 80 C50 74 45 71 45 76 C45 81 50 86 50 86 C50 86 55 81 55 76 C55 71 50 74 50 80 Z"/>
    </g>
    <!-- Pin centers (white dots) -->
    <g fill="#FFF">
        <circle cx="25" cy="40" r="2"/>
        <circle cx="45" cy="50" r="2"/>
        <circle cx="35" cy="63" r="2"/>
        <circle cx="55" cy="43" r="2"/>
        <circle cx="70" cy="53" r="2"/>
        <circle cx="60" cy="70" r="2"/>
        <circle cx="75" cy="38" r="2"/>
        <circle cx="22" cy="56" r="2"/>
        <circle cx="78" cy="66" r="2"/>
        <circle cx="50" cy="78" r="2"/>
    </g>
    <!-- "10+" badge -->
    <circle cx="50" cy="22" r="12" fill="#FF9800"/>
    <text x="50" y="27" text-anchor="middle" fill="#FFF" font-size="11" font-weight="bold">10+</text>
</svg>
SVG;
}

// ============================================================================
// FUN BADGES - Performance
// ============================================================================

/**
 * Render Raketstart badge - Rocket launching cyclist (podium in first race)
 */
function renderRocketStartBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="rocketBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF3E0"/>
            <stop offset="100%" stop-color="#FFCC80"/>
        </linearGradient>
        <linearGradient id="rocketBody" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FF7043"/>
            <stop offset="100%" stop-color="#D84315"/>
        </linearGradient>
        <linearGradient id="rocketFlame" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFC107"/>
            <stop offset="50%" stop-color="#FF9800"/>
            <stop offset="100%" stop-color="#FF5722"/>
        </linearGradient>
        <filter id="rocketShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#rocketBg)" stroke="#FF5722" stroke-width="2.5" filter="url(#rocketShadow)"/>
    <!-- Speed lines -->
    <g stroke="#FFB74D" stroke-width="2" opacity="0.5">
        <line x1="15" y1="75" x2="30" y2="70"/>
        <line x1="12" y1="65" x2="25" y2="62"/>
        <line x1="18" y1="85" x2="28" y2="82"/>
        <line x1="70" y1="72" x2="85" y2="77"/>
        <line x1="72" y1="62" x2="88" y2="67"/>
        <line x1="68" y1="82" x2="82" y2="87"/>
    </g>
    <!-- Rocket body -->
    <g transform="translate(50, 50)">
        <!-- Rocket nose cone -->
        <path d="M0 -35 C8 -35 12 -25 12 -15 L12 15 L-12 15 L-12 -15 C-12 -25 -8 -35 0 -35 Z" fill="url(#rocketBody)"/>
        <!-- Window -->
        <circle cx="0" cy="-10" r="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1"/>
        <circle cx="0" cy="-10" r="5" fill="#64B5F6"/>
        <!-- Window shine -->
        <path d="M-3 -13 Q0 -16 3 -13" stroke="#FFF" stroke-width="1.5" fill="none" opacity="0.7"/>
        <!-- Fins -->
        <path d="M-12 10 L-22 25 L-12 20 Z" fill="#D84315"/>
        <path d="M12 10 L22 25 L12 20 Z" fill="#D84315"/>
        <!-- Center stripe -->
        <rect x="-3" y="-20" width="6" height="35" fill="#FFC107" opacity="0.8"/>
        <!-- Rocket flames -->
        <path d="M-8 15 Q-10 35 -5 45 Q0 55 5 45 Q10 35 8 15" fill="url(#rocketFlame)"/>
        <path d="M-5 15 Q-6 30 0 40 Q6 30 5 15" fill="#FFF176" opacity="0.7"/>
    </g>
    <!-- Stars/sparkles around -->
    <path d="M20 25L22 30L27 30L23 33L24 38L20 35L16 38L17 33L13 30L18 30Z" fill="#FFD700"/>
    <path d="M80 30L81 33L84 33L82 35L82.5 38L80 36L77.5 38L78 35L76 33L79 33Z" fill="#FFD700"/>
    <circle cx="25" cy="45" r="2" fill="#FF9800"/>
    <circle cx="75" cy="50" r="2" fill="#FF9800"/>
</svg>
SVG;
}

/**
 * Render Konsekvent badge - Steady graph line (top 10 consistency)
 */
function renderConsistentBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="consistentBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <filter id="consistentShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#consistentBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#consistentShadow)"/>
    <!-- Graph background -->
    <rect x="20" y="30" width="60" height="50" rx="4" fill="#FFF" stroke="#E0E0E0" stroke-width="1"/>
    <!-- Grid lines -->
    <g stroke="#E8E8E8" stroke-width="1">
        <line x1="20" y1="40" x2="80" y2="40"/>
        <line x1="20" y1="50" x2="80" y2="50"/>
        <line x1="20" y1="60" x2="80" y2="60"/>
        <line x1="20" y1="70" x2="80" y2="70"/>
        <line x1="30" y1="30" x2="30" y2="80"/>
        <line x1="45" y1="30" x2="45" y2="80"/>
        <line x1="60" y1="30" x2="60" y2="80"/>
        <line x1="75" y1="30" x2="75" y2="80"/>
    </g>
    <!-- Steady performance line -->
    <path d="M25 55 L35 52 L45 54 L55 51 L65 53 L75 50" fill="none" stroke="#4CAF50" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Data points -->
    <circle cx="25" cy="55" r="4" fill="#4CAF50" stroke="#FFF" stroke-width="2"/>
    <circle cx="35" cy="52" r="4" fill="#4CAF50" stroke="#FFF" stroke-width="2"/>
    <circle cx="45" cy="54" r="4" fill="#4CAF50" stroke="#FFF" stroke-width="2"/>
    <circle cx="55" cy="51" r="4" fill="#4CAF50" stroke="#FFF" stroke-width="2"/>
    <circle cx="65" cy="53" r="4" fill="#4CAF50" stroke="#FFF" stroke-width="2"/>
    <circle cx="75" cy="50" r="4" fill="#4CAF50" stroke="#FFF" stroke-width="2"/>
    <!-- "TOP 10" label -->
    <rect x="30" y="88" width="40" height="16" rx="4" fill="#4CAF50"/>
    <text x="50" y="100" text-anchor="middle" fill="#FFF" font-size="9" font-weight="bold" font-family="system-ui">TOP 10</text>
    <!-- Checkmark -->
    <circle cx="75" cy="25" r="8" fill="#4CAF50"/>
    <path d="M71 25 L74 28 L79 22" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round"/>
</svg>
SVG;
}

/**
 * Render Förbättrare badge - Arrow graph going up (improvement streak)
 */
function renderImproverBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="improverBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#81C784"/>
        </linearGradient>
        <linearGradient id="arrowGrad" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#43A047"/>
            <stop offset="100%" stop-color="#66BB6A"/>
        </linearGradient>
        <filter id="improverShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#improverBg)" stroke="#43A047" stroke-width="2.5" filter="url(#improverShadow)"/>
    <!-- Background glow -->
    <ellipse cx="50" cy="55" rx="35" ry="35" fill="#C8E6C9" opacity="0.4"/>
    <!-- Upward arrow path -->
    <path d="M20 85 L30 72 L40 65 L50 52 L60 42 L70 30" fill="none" stroke="url(#arrowGrad)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Arrow head -->
    <path d="M70 30 L78 22" stroke="url(#arrowGrad)" stroke-width="6" stroke-linecap="round"/>
    <path d="M70 22 L78 22 L78 30" stroke="url(#arrowGrad)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <!-- Progress markers -->
    <circle cx="20" cy="85" r="5" fill="#43A047"/>
    <circle cx="30" cy="72" r="5" fill="#4CAF50"/>
    <circle cx="40" cy="65" r="5" fill="#66BB6A"/>
    <circle cx="50" cy="52" r="5" fill="#81C784"/>
    <circle cx="60" cy="42" r="5" fill="#A5D6A7"/>
    <!-- "5x" improvement badge -->
    <circle cx="25" cy="30" r="12" fill="#2E7D32"/>
    <text x="25" y="35" text-anchor="middle" fill="#FFF" font-size="11" font-weight="bold" font-family="system-ui">5×</text>
    <!-- Sparkles -->
    <path d="M80 35L82 40L87 40L83 43L84 48L80 45L76 48L77 43L73 40L78 40Z" fill="#FFD700" opacity="0.8"/>
</svg>
SVG;
}

// ============================================================================
// FUN BADGES - Milestones
// ============================================================================

/**
 * Render First Race badge - Starting gate with cyclist
 */
function renderFirstRaceBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="firstraceBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <filter id="firstraceShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#firstraceBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#firstraceShadow)"/>
    <!-- Starting gate -->
    <rect x="20" y="30" width="6" height="55" fill="#5D4037"/>
    <rect x="74" y="30" width="6" height="55" fill="#5D4037"/>
    <rect x="20" y="30" width="60" height="8" fill="#4CAF50"/>
    <text x="50" y="37" text-anchor="middle" fill="#FFF" font-size="6" font-weight="bold" font-family="system-ui">START</text>
    <!-- Gate mechanism -->
    <rect x="26" y="38" width="48" height="4" fill="#795548"/>
    <!-- Cyclist at start -->
    <g transform="translate(50, 68)">
        <!-- Bike wheels -->
        <circle cx="-12" cy="15" r="10" fill="none" stroke="#333" stroke-width="2"/>
        <circle cx="12" cy="15" r="10" fill="none" stroke="#333" stroke-width="2"/>
        <!-- Bike frame -->
        <path d="M-12 15 L0 2 L12 15 M0 2 L0 10 L-12 15 M0 10 L12 15" stroke="#333" stroke-width="2" fill="none"/>
        <!-- Cyclist ready position -->
        <circle cx="0" cy="-8" r="7" fill="#4CAF50"/>
        <path d="M-5 0 L0 10 M5 0 L0 10" stroke="#4CAF50" stroke-width="3" stroke-linecap="round"/>
        <!-- Hands on handlebars -->
        <path d="M-4 -3 L-10 5 M4 -3 L10 5" stroke="#4CAF50" stroke-width="2" stroke-linecap="round"/>
    </g>
    <!-- "1st" badge -->
    <circle cx="78" cy="25" r="10" fill="#FFD700"/>
    <text x="78" y="29" text-anchor="middle" fill="#5D4037" font-size="9" font-weight="bold" font-family="system-ui">1st</text>
    <!-- Confetti dots -->
    <circle cx="15" cy="45" r="3" fill="#E53935" opacity="0.7"/>
    <circle cx="85" cy="50" r="3" fill="#1E88E5" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render 5 Races badge - Early milestone
 */
function render5RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races5Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E3F2FD"/>
            <stop offset="100%" stop-color="#BBDEFB"/>
        </linearGradient>
        <linearGradient id="medal5" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#64B5F6"/>
            <stop offset="100%" stop-color="#2196F3"/>
        </linearGradient>
        <filter id="races5Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races5Bg)" stroke="#2196F3" stroke-width="2.5" filter="url(#races5Shadow)"/>
    <!-- Ribbon -->
    <path d="M35 20 L35 55 L50 70 L65 55 L65 20" fill="#2196F3"/>
    <path d="M35 20 L50 35 L65 20" fill="#1976D2"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="28" fill="url(#medal5)" stroke="#1976D2" stroke-width="2"/>
    <circle cx="50" cy="58" r="22" fill="none" stroke="#BBDEFB" stroke-width="2"/>
    <!-- Number -->
    <text x="50" y="68" text-anchor="middle" fill="#FFF" font-size="24" font-weight="bold" font-family="system-ui">5</text>
</svg>
SVG;
}

/**
 * Render 10 Races badge - Bronze milestone circle
 */
function render10RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races10Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#C8E6C9"/>
        </linearGradient>
        <linearGradient id="medal10" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#81C784"/>
            <stop offset="100%" stop-color="#4CAF50"/>
        </linearGradient>
        <filter id="races10Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races10Bg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#races10Shadow)"/>
    <!-- Ribbon -->
    <path d="M35 20 L35 55 L50 70 L65 55 L65 20" fill="#4CAF50"/>
    <path d="M35 20 L50 35 L65 20" fill="#388E3C"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="28" fill="url(#medal10)" stroke="#388E3C" stroke-width="2"/>
    <circle cx="50" cy="58" r="22" fill="none" stroke="#C8E6C9" stroke-width="2"/>
    <!-- Number -->
    <text x="50" y="68" text-anchor="middle" fill="#FFF" font-size="24" font-weight="bold" font-family="system-ui">10</text>
    <!-- Laurel leaves -->
    <g stroke="#388E3C" stroke-width="1.5" fill="none" opacity="0.6">
        <path d="M22 58 Q25 45 30 40"/>
        <path d="M20 65 Q25 55 28 50"/>
        <path d="M78 58 Q75 45 70 40"/>
        <path d="M80 65 Q75 55 72 50"/>
    </g>
</svg>
SVG;
}

/**
 * Render 15 Races badge - Teal milestone
 */
function render15RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races15Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E0F2F1"/>
            <stop offset="100%" stop-color="#B2DFDB"/>
        </linearGradient>
        <linearGradient id="medal15" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#4DB6AC"/>
            <stop offset="100%" stop-color="#009688"/>
        </linearGradient>
        <filter id="races15Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races15Bg)" stroke="#009688" stroke-width="2.5" filter="url(#races15Shadow)"/>
    <!-- Ribbon -->
    <path d="M35 20 L35 55 L50 70 L65 55 L65 20" fill="#009688"/>
    <path d="M35 20 L50 35 L65 20" fill="#00796B"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="28" fill="url(#medal15)" stroke="#00796B" stroke-width="2"/>
    <circle cx="50" cy="58" r="22" fill="none" stroke="#B2DFDB" stroke-width="2"/>
    <!-- Number -->
    <text x="50" y="68" text-anchor="middle" fill="#FFF" font-size="22" font-weight="bold" font-family="system-ui">15</text>
</svg>
SVG;
}

/**
 * Render 20 Races badge - Orange milestone
 */
function render20RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races20Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF3E0"/>
            <stop offset="100%" stop-color="#FFE0B2"/>
        </linearGradient>
        <linearGradient id="medal20" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFB74D"/>
            <stop offset="100%" stop-color="#FF9800"/>
        </linearGradient>
        <filter id="races20Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races20Bg)" stroke="#FF9800" stroke-width="2.5" filter="url(#races20Shadow)"/>
    <!-- Ribbon -->
    <path d="M35 20 L35 55 L50 70 L65 55 L65 20" fill="#FF9800"/>
    <path d="M35 20 L50 35 L65 20" fill="#F57C00"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="28" fill="url(#medal20)" stroke="#F57C00" stroke-width="2"/>
    <circle cx="50" cy="58" r="22" fill="none" stroke="#FFE0B2" stroke-width="2"/>
    <!-- Number -->
    <text x="50" y="68" text-anchor="middle" fill="#FFF" font-size="22" font-weight="bold" font-family="system-ui">20</text>
</svg>
SVG;
}

/**
 * Render 25 Races badge - Silver milestone medal
 */
function render25RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races25Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#F5F5F5"/>
            <stop offset="100%" stop-color="#E0E0E0"/>
        </linearGradient>
        <linearGradient id="medal25" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E0E0E0"/>
            <stop offset="50%" stop-color="#BDBDBD"/>
            <stop offset="100%" stop-color="#9E9E9E"/>
        </linearGradient>
        <filter id="races25Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races25Bg)" stroke="#9E9E9E" stroke-width="2.5" filter="url(#races25Shadow)"/>
    <!-- Ribbon -->
    <path d="M35 18 L35 50 L50 65 L65 50 L65 18" fill="#9E9E9E"/>
    <path d="M35 18 L50 32 L65 18" fill="#757575"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="30" fill="url(#medal25)" stroke="#757575" stroke-width="2"/>
    <circle cx="50" cy="58" r="24" fill="none" stroke="#E0E0E0" stroke-width="2"/>
    <!-- Number -->
    <text x="50" y="68" text-anchor="middle" fill="#424242" font-size="22" font-weight="bold" font-family="system-ui">25</text>
    <!-- Shine effect -->
    <path d="M35 45 Q45 35 50 35" stroke="#FFF" stroke-width="2" fill="none" opacity="0.5"/>
    <!-- Stars decoration -->
    <circle cx="22" cy="40" r="3" fill="#BDBDBD"/>
    <circle cx="78" cy="40" r="3" fill="#BDBDBD"/>
    <circle cx="20" cy="75" r="2" fill="#9E9E9E"/>
    <circle cx="80" cy="75" r="2" fill="#9E9E9E"/>
</svg>
SVG;
}

/**
 * Render 50 Races badge - Gold milestone medal
 */
function render50RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races50Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF8E1"/>
            <stop offset="100%" stop-color="#FFE082"/>
        </linearGradient>
        <linearGradient id="medal50" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFE082"/>
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#FFA000"/>
        </linearGradient>
        <filter id="races50Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races50Bg)" stroke="#FFA000" stroke-width="2.5" filter="url(#races50Shadow)"/>
    <!-- Ribbon -->
    <path d="M32 15 L32 48 L50 68 L68 48 L68 15" fill="#FFA000"/>
    <path d="M32 15 L50 32 L68 15" fill="#E65100"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="32" fill="url(#medal50)" stroke="#E65100" stroke-width="2"/>
    <circle cx="50" cy="58" r="26" fill="none" stroke="#FFF8E1" stroke-width="2"/>
    <!-- Number -->
    <text x="50" y="68" text-anchor="middle" fill="#5D4037" font-size="24" font-weight="bold" font-family="system-ui">50</text>
    <!-- Shine effect -->
    <path d="M32 48 Q42 35 50 32" stroke="#FFF" stroke-width="2.5" fill="none" opacity="0.6"/>
    <!-- Stars -->
    <path d="M20 35L22 40L27 40L23 43L24 48L20 45L16 48L17 43L13 40L18 40Z" fill="#FFD700"/>
    <path d="M80 35L82 40L87 40L83 43L84 48L80 45L76 48L77 43L73 40L78 40Z" fill="#FFD700"/>
</svg>
SVG;
}

/**
 * Render 100 Races badge - Legendary diamond medal with glow
 */
function render100RacesBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="races100Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF8E1"/>
            <stop offset="100%" stop-color="#FFD54F"/>
        </linearGradient>
        <linearGradient id="medal100" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFE082"/>
            <stop offset="30%" stop-color="#FFD700"/>
            <stop offset="70%" stop-color="#FFA000"/>
            <stop offset="100%" stop-color="#FF6F00"/>
        </linearGradient>
        <filter id="races100Glow">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="races100Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#races100Bg)" stroke="#FF6F00" stroke-width="2.5" filter="url(#races100Shadow)"/>
    <!-- Radiant glow -->
    <g filter="url(#races100Glow)" opacity="0.4">
        <path d="M50 20L55 50L80 35L60 55L85 60L55 60L65 85L50 62L35 85L45 60L15 60L40 55L20 35L45 50Z" fill="#FFD700"/>
    </g>
    <!-- Ribbon with crown -->
    <path d="M30 12 L30 45 L50 68 L70 45 L70 12" fill="#FF6F00"/>
    <path d="M30 12 L50 28 L70 12" fill="#E65100"/>
    <!-- Crown on top -->
    <path d="M35 8 L40 2 L50 6 L60 2 L65 8 L60 12 L40 12 Z" fill="#FFD700" stroke="#E65100" stroke-width="1"/>
    <!-- Medal circle -->
    <circle cx="50" cy="58" r="34" fill="url(#medal100)" stroke="#E65100" stroke-width="2.5"/>
    <circle cx="50" cy="58" r="28" fill="none" stroke="#FFF8E1" stroke-width="2"/>
    <circle cx="50" cy="58" r="22" fill="none" stroke="#FFE082" stroke-width="1" opacity="0.5"/>
    <!-- Number -->
    <text x="50" y="66" text-anchor="middle" fill="#5D4037" font-size="20" font-weight="bold" font-family="system-ui">100</text>
    <!-- Shine effect -->
    <path d="M28 50 Q40 35 50 30" stroke="#FFF" stroke-width="3" fill="none" opacity="0.6"/>
    <!-- Stars around -->
    <path d="M15 50L17 55L22 55L18 58L19 63L15 60L11 63L12 58L8 55L13 55Z" fill="#FFD700"/>
    <path d="M85 50L87 55L92 55L88 58L89 63L85 60L81 63L82 58L78 55L83 55Z" fill="#FFD700"/>
    <!-- Sparkles -->
    <circle cx="25" cy="30" r="2" fill="#FFC107"/>
    <circle cx="75" cy="32" r="2" fill="#FFC107"/>
    <circle cx="20" cy="85" r="1.5" fill="#FF9800"/>
    <circle cx="80" cy="82" r="1.5" fill="#FF9800"/>
</svg>
SVG;
}

/**
 * Render Säsongsstartare badge - Calendar with start flag
 */
function renderSeasonStarterBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="starterBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <filter id="starterShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#starterBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#starterShadow)"/>
    <!-- Calendar -->
    <rect x="22" y="35" width="56" height="55" rx="4" fill="#FFF" stroke="#4CAF50" stroke-width="2"/>
    <rect x="22" y="35" width="56" height="15" rx="4" fill="#4CAF50"/>
    <!-- Calendar hooks -->
    <rect x="32" y="30" width="4" height="12" rx="2" fill="#388E3C"/>
    <rect x="64" y="30" width="4" height="12" rx="2" fill="#388E3C"/>
    <!-- Calendar title -->
    <text x="50" y="47" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold" font-family="system-ui">START</text>
    <!-- Day number "1" highlighted -->
    <rect x="32" y="55" width="18" height="18" rx="3" fill="#4CAF50"/>
    <text x="41" y="69" text-anchor="middle" fill="#FFF" font-size="14" font-weight="bold" font-family="system-ui">1</text>
    <!-- Other calendar squares (faded) -->
    <rect x="52" y="55" width="18" height="18" rx="3" fill="#E8E8E8"/>
    <rect x="32" y="75" width="18" height="10" rx="2" fill="#E8E8E8"/>
    <rect x="52" y="75" width="18" height="10" rx="2" fill="#E8E8E8"/>
    <!-- Flag -->
    <g transform="translate(75, 20)">
        <rect x="0" y="0" width="3" height="25" fill="#8B4513"/>
        <path d="M3 0 L18 6 L3 12 Z" fill="#E53935"/>
    </g>
    <!-- Sparkles -->
    <circle cx="20" cy="50" r="3" fill="#FFD700" opacity="0.7"/>
</svg>
SVG;
}

/**
 * Render Säsongsavslutare badge - Checkered flag calendar
 */
function renderSeasonFinisherBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="seasonfinishBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <filter id="seasonfinishShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#seasonfinishBg)" stroke="#4CAF50" stroke-width="2.5" filter="url(#seasonfinishShadow)"/>
    <!-- Calendar -->
    <rect x="22" y="35" width="56" height="55" rx="4" fill="#FFF" stroke="#4CAF50" stroke-width="2"/>
    <rect x="22" y="35" width="56" height="15" rx="4" fill="#4CAF50"/>
    <!-- Calendar hooks -->
    <rect x="32" y="30" width="4" height="12" rx="2" fill="#388E3C"/>
    <rect x="64" y="30" width="4" height="12" rx="2" fill="#388E3C"/>
    <!-- Calendar title -->
    <text x="50" y="47" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold" font-family="system-ui">FINAL</text>
    <!-- Checkered pattern in calendar -->
    <g transform="translate(30, 55)">
        <rect x="0" y="0" width="10" height="10" fill="#333"/>
        <rect x="20" y="0" width="10" height="10" fill="#333"/>
        <rect x="10" y="10" width="10" height="10" fill="#333"/>
        <rect x="30" y="10" width="10" height="10" fill="#333"/>
        <rect x="0" y="20" width="10" height="10" fill="#333"/>
        <rect x="20" y="20" width="10" height="10" fill="#333"/>
        <rect x="10" y="0" width="10" height="10" fill="#FFF" stroke="#E0E0E0" stroke-width="0.5"/>
        <rect x="30" y="0" width="10" height="10" fill="#FFF" stroke="#E0E0E0" stroke-width="0.5"/>
        <rect x="0" y="10" width="10" height="10" fill="#FFF" stroke="#E0E0E0" stroke-width="0.5"/>
        <rect x="20" y="10" width="10" height="10" fill="#FFF" stroke="#E0E0E0" stroke-width="0.5"/>
        <rect x="10" y="20" width="10" height="10" fill="#FFF" stroke="#E0E0E0" stroke-width="0.5"/>
        <rect x="30" y="20" width="10" height="10" fill="#FFF" stroke="#E0E0E0" stroke-width="0.5"/>
    </g>
    <!-- Trophy icon -->
    <circle cx="78" cy="25" r="10" fill="#FFD700"/>
    <path d="M74 22 L82 22 L81 28 L75 28 Z" fill="#B8860B"/>
</svg>
SVG;
}

/**
 * Render Connected badge - Social media network
 */
function renderConnectedBadge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="connectedBg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E3F2FD"/>
            <stop offset="100%" stop-color="#90CAF9"/>
        </linearGradient>
        <filter id="connectedShadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <!-- Hexagon background -->
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#connectedBg)" stroke="#1976D2" stroke-width="2.5" filter="url(#connectedShadow)"/>
    <!-- Connection lines -->
    <g stroke="#64B5F6" stroke-width="2">
        <line x1="50" y1="50" x2="25" y2="35"/>
        <line x1="50" y1="50" x2="75" y2="35"/>
        <line x1="50" y1="50" x2="25" y2="75"/>
        <line x1="50" y1="50" x2="75" y2="75"/>
        <line x1="50" y1="50" x2="50" y2="25"/>
    </g>
    <!-- Center node (profile) -->
    <circle cx="50" cy="50" r="15" fill="#1976D2"/>
    <circle cx="50" cy="45" r="6" fill="#FFF"/>
    <path d="M40 58 Q50 52 60 58" fill="#FFF"/>
    <!-- Social platform nodes -->
    <!-- Instagram (gradient pink) -->
    <circle cx="25" cy="35" r="10" fill="#E1306C"/>
    <rect x="21" y="31" width="8" height="8" rx="2" fill="none" stroke="#FFF" stroke-width="1.5"/>
    <circle cx="25" cy="35" r="2" fill="none" stroke="#FFF" stroke-width="1.5"/>
    <!-- Facebook (blue) -->
    <circle cx="75" cy="35" r="10" fill="#1877F2"/>
    <text x="75" y="40" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold" font-family="system-ui">f</text>
    <!-- Strava (orange) -->
    <circle cx="50" cy="25" r="10" fill="#FC4C02"/>
    <path d="M47 28 L50 22 L53 28 M50 25 L50 28" stroke="#FFF" stroke-width="1.5" fill="none"/>
    <!-- YouTube (red) -->
    <circle cx="25" cy="75" r="10" fill="#FF0000"/>
    <path d="M22 75 L29 75 L29 71 L22 71 Z M22 79 L29 79 L29 75 Z" fill="#FFF"/>
    <path d="M24 73 L27 75 L24 77 Z" fill="#FF0000"/>
    <!-- TikTok (black) -->
    <circle cx="75" cy="75" r="10" fill="#000"/>
    <path d="M72 72 L72 80 Q72 82 74 82 Q76 82 76 80 L76 72 M76 72 Q78 72 78 70" stroke="#FFF" stroke-width="1.5" fill="none"/>
    <!-- Link icon -->
    <circle cx="85" cy="55" r="8" fill="#4CAF50"/>
    <path d="M82 55 L88 55 M85 52 L85 58" stroke="#FFF" stroke-width="2" stroke-linecap="round"/>
</svg>
SVG;
}

/**
 * Render experience star icon SVG
 */
function renderExperienceIcon(): string {
    return <<<SVG
<svg class="exp-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
</svg>
SVG;
}

// ============================================================================
// EXPERIENCE LEVEL BADGES - Tree Growth Theme
// ============================================================================

/**
 * Render 1:a året badge - Small seedling sprouting
 */
function renderExp1Badge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="exp1Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#C8E6C9"/>
        </linearGradient>
        <linearGradient id="soilGrad" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#8D6E63"/>
            <stop offset="100%" stop-color="#5D4037"/>
        </linearGradient>
        <filter id="exp1Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#exp1Bg)" stroke="#81C784" stroke-width="2.5" filter="url(#exp1Shadow)"/>
    <!-- Soil/ground -->
    <ellipse cx="50" cy="85" rx="35" ry="12" fill="url(#soilGrad)"/>
    <!-- Cute seedling -->
    <g transform="translate(50, 55)">
        <!-- Stem -->
        <path d="M0 30 Q-2 15 0 0" stroke="#66BB6A" stroke-width="4" fill="none" stroke-linecap="round"/>
        <!-- First leaves (cute, rounded) -->
        <ellipse cx="-12" cy="-5" rx="10" ry="6" fill="#81C784" transform="rotate(-30)"/>
        <ellipse cx="12" cy="-5" rx="10" ry="6" fill="#81C784" transform="rotate(30)"/>
        <!-- Leaf veins -->
        <path d="M-8 -8 L-4 -5" stroke="#A5D6A7" stroke-width="1" opacity="0.7"/>
        <path d="M8 -8 L4 -5" stroke="#A5D6A7" stroke-width="1" opacity="0.7"/>
        <!-- Tiny bud on top -->
        <circle cx="0" cy="-5" r="4" fill="#AED581"/>
    </g>
    <!-- Sunlight rays -->
    <g stroke="#FFF59D" stroke-width="2" opacity="0.6">
        <line x1="70" y1="25" x2="60" y2="35"/>
        <line x1="78" y1="35" x2="65" y2="42"/>
        <line x1="75" y1="45" x2="62" y2="50"/>
    </g>
    <!-- Small sun -->
    <circle cx="80" cy="25" r="10" fill="#FFD54F"/>
    <!-- Year badge -->
    <circle cx="20" cy="95" r="10" fill="#4CAF50"/>
    <text x="20" y="99" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">1</text>
</svg>
SVG;
}

/**
 * Render 2:a året badge - Small tree with branches
 */
function renderExp2Badge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="exp2Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#A5D6A7"/>
        </linearGradient>
        <linearGradient id="trunk2" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#8D6E63"/>
            <stop offset="100%" stop-color="#5D4037"/>
        </linearGradient>
        <filter id="exp2Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#exp2Bg)" stroke="#66BB6A" stroke-width="2.5" filter="url(#exp2Shadow)"/>
    <!-- Ground -->
    <ellipse cx="50" cy="95" rx="30" ry="8" fill="#8D6E63"/>
    <!-- Small tree -->
    <g transform="translate(50, 50)">
        <!-- Trunk -->
        <rect x="-4" y="10" width="8" height="40" fill="url(#trunk2)"/>
        <!-- Tree crown (layered) -->
        <ellipse cx="0" cy="-5" rx="25" ry="20" fill="#66BB6A"/>
        <ellipse cx="0" cy="5" rx="22" ry="15" fill="#4CAF50"/>
        <!-- Leaves detail -->
        <circle cx="-12" cy="-10" r="8" fill="#81C784"/>
        <circle cx="12" cy="-8" r="8" fill="#81C784"/>
        <circle cx="0" cy="-18" r="7" fill="#81C784"/>
        <!-- Highlight -->
        <ellipse cx="-8" cy="-12" rx="5" ry="4" fill="#A5D6A7" opacity="0.6"/>
    </g>
    <!-- Year badge -->
    <circle cx="20" cy="95" r="10" fill="#4CAF50"/>
    <text x="20" y="99" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">2</text>
</svg>
SVG;
}

/**
 * Render Erfaren (3:e året) badge - Medium tree with bird
 */
function renderExp3Badge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="exp3Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#81C784"/>
        </linearGradient>
        <linearGradient id="trunk3" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#6D4C41"/>
            <stop offset="100%" stop-color="#4E342E"/>
        </linearGradient>
        <filter id="exp3Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#exp3Bg)" stroke="#43A047" stroke-width="2.5" filter="url(#exp3Shadow)"/>
    <!-- Ground with grass -->
    <ellipse cx="50" cy="100" rx="35" ry="8" fill="#5D4037"/>
    <path d="M20 98 Q25 90 30 98 Q35 92 40 98" stroke="#66BB6A" stroke-width="2" fill="none"/>
    <path d="M60 98 Q65 92 70 98 Q75 90 80 98" stroke="#66BB6A" stroke-width="2" fill="none"/>
    <!-- Medium tree -->
    <g transform="translate(50, 45)">
        <!-- Trunk with texture -->
        <rect x="-6" y="20" width="12" height="45" fill="url(#trunk3)"/>
        <path d="M-4 30 L-2 40 M2 25 L4 35 M0 35 L1 50" stroke="#4E342E" stroke-width="1" opacity="0.5"/>
        <!-- Branches -->
        <path d="M-6 25 L-20 15" stroke="url(#trunk3)" stroke-width="4"/>
        <path d="M6 20 L22 10" stroke="url(#trunk3)" stroke-width="4"/>
        <!-- Tree crown (fuller) -->
        <ellipse cx="0" cy="0" rx="30" ry="25" fill="#43A047"/>
        <circle cx="-15" cy="-10" r="12" fill="#4CAF50"/>
        <circle cx="15" cy="-8" r="12" fill="#4CAF50"/>
        <circle cx="0" cy="-20" r="10" fill="#66BB6A"/>
        <circle cx="-20" cy="5" r="10" fill="#4CAF50"/>
        <circle cx="20" cy="5" r="10" fill="#4CAF50"/>
    </g>
    <!-- Bird sitting on branch -->
    <g transform="translate(72, 40)">
        <ellipse cx="0" cy="0" rx="6" ry="5" fill="#FF7043"/>
        <circle cx="5" cy="-3" r="4" fill="#FF7043"/>
        <path d="M8 -3 L12 -2" stroke="#FFB74D" stroke-width="2"/>
        <circle cx="6" cy="-4" r="1" fill="#1A1A1A"/>
        <path d="M-3 4 L-2 8 M1 4 L2 8" stroke="#5D4037" stroke-width="1"/>
    </g>
    <!-- Year badge -->
    <circle cx="18" cy="25" r="10" fill="#388E3C"/>
    <text x="18" y="29" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">3</text>
</svg>
SVG;
}

/**
 * Render Expert (4:e året) badge - Strong sturdy tree
 */
function renderExp4Badge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="exp4Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E0F2F1"/>
            <stop offset="100%" stop-color="#80CBC4"/>
        </linearGradient>
        <linearGradient id="trunk4" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#5D4037"/>
            <stop offset="100%" stop-color="#3E2723"/>
        </linearGradient>
        <filter id="exp4Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#exp4Bg)" stroke="#2E7D32" stroke-width="2.5" filter="url(#exp4Shadow)"/>
    <!-- Ground -->
    <ellipse cx="50" cy="102" rx="38" ry="8" fill="#4E342E"/>
    <!-- Strong tree -->
    <g transform="translate(50, 40)">
        <!-- Thick trunk -->
        <path d="M-10 25 L-8 60 L8 60 L10 25" fill="url(#trunk4)"/>
        <!-- Root bulges -->
        <ellipse cx="-12" cy="58" rx="6" ry="4" fill="#5D4037"/>
        <ellipse cx="12" cy="58" rx="6" ry="4" fill="#5D4037"/>
        <!-- Major branches -->
        <path d="M-8 30 L-28 15" stroke="url(#trunk4)" stroke-width="6"/>
        <path d="M8 25 L30 10" stroke="url(#trunk4)" stroke-width="6"/>
        <path d="M-5 20 L-18 5" stroke="url(#trunk4)" stroke-width="4"/>
        <path d="M5 15 L20 0" stroke="url(#trunk4)" stroke-width="4"/>
        <!-- Rich crown -->
        <ellipse cx="0" cy="-5" rx="38" ry="30" fill="#2E7D32"/>
        <circle cx="-20" cy="-15" r="15" fill="#388E3C"/>
        <circle cx="20" cy="-12" r="15" fill="#388E3C"/>
        <circle cx="0" cy="-25" r="12" fill="#43A047"/>
        <circle cx="-28" cy="0" r="12" fill="#388E3C"/>
        <circle cx="28" cy="2" r="12" fill="#388E3C"/>
        <!-- Leaf highlights -->
        <circle cx="-15" cy="-20" r="6" fill="#66BB6A" opacity="0.6"/>
        <circle cx="10" cy="-22" r="5" fill="#66BB6A" opacity="0.6"/>
    </g>
    <!-- Year badge -->
    <circle cx="18" cy="22" r="10" fill="#1B5E20"/>
    <text x="18" y="26" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">4</text>
</svg>
SVG;
}

/**
 * Render Veteran (5:e året) badge - Mighty oak tree
 */
function renderExp5Badge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="exp5Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#E8F5E9"/>
            <stop offset="100%" stop-color="#66BB6A"/>
        </linearGradient>
        <linearGradient id="trunk5" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#4E342E"/>
            <stop offset="100%" stop-color="#3E2723"/>
        </linearGradient>
        <filter id="exp5Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#exp5Bg)" stroke="#1B5E20" stroke-width="2.5" filter="url(#exp5Shadow)"/>
    <!-- Ground with roots showing -->
    <ellipse cx="50" cy="105" rx="40" ry="8" fill="#3E2723"/>
    <!-- Mighty oak -->
    <g transform="translate(50, 35)">
        <!-- Massive trunk -->
        <path d="M-14 30 L-12 65 L12 65 L14 30" fill="url(#trunk5)"/>
        <!-- Visible roots -->
        <path d="M-12 62 Q-25 65 -30 70" stroke="#4E342E" stroke-width="5" fill="none"/>
        <path d="M12 62 Q25 65 30 70" stroke="#4E342E" stroke-width="5" fill="none"/>
        <!-- Trunk texture (bark) -->
        <path d="M-8 35 L-6 50 M0 40 L2 55 M8 38 L6 52" stroke="#3E2723" stroke-width="1.5" opacity="0.6"/>
        <!-- Major branches spreading wide -->
        <path d="M-12 35 L-35 10" stroke="url(#trunk5)" stroke-width="8"/>
        <path d="M12 30 L38 8" stroke="url(#trunk5)" stroke-width="8"/>
        <path d="M-8 25 L-25 0" stroke="url(#trunk5)" stroke-width="5"/>
        <path d="M8 20 L28 -5" stroke="url(#trunk5)" stroke-width="5"/>
        <path d="M0 20 L0 -10" stroke="url(#trunk5)" stroke-width="6"/>
        <!-- Massive crown -->
        <ellipse cx="0" cy="-10" rx="42" ry="35" fill="#1B5E20"/>
        <circle cx="-25" cy="-20" r="18" fill="#2E7D32"/>
        <circle cx="25" cy="-18" r="18" fill="#2E7D32"/>
        <circle cx="0" cy="-35" r="15" fill="#388E3C"/>
        <circle cx="-35" cy="-5" r="14" fill="#2E7D32"/>
        <circle cx="35" cy="-2" r="14" fill="#2E7D32"/>
        <circle cx="-15" cy="-30" r="10" fill="#43A047"/>
        <circle cx="15" cy="-28" r="10" fill="#43A047"/>
        <!-- Wisdom owl -->
        <g transform="translate(-30, -25)">
            <ellipse cx="0" cy="0" rx="5" ry="6" fill="#8D6E63"/>
            <circle cx="-2" cy="-2" r="2" fill="#FFF"/>
            <circle cx="2" cy="-2" r="2" fill="#FFF"/>
            <circle cx="-2" cy="-2" r="1" fill="#1A1A1A"/>
            <circle cx="2" cy="-2" r="1" fill="#1A1A1A"/>
            <path d="M-1 1 L0 3 L1 1" fill="#FF9800"/>
        </g>
    </g>
    <!-- Year badge -->
    <circle cx="15" cy="18" r="10" fill="#1B5E20"/>
    <text x="15" y="22" text-anchor="middle" fill="#FFF" font-size="10" font-weight="bold">5</text>
</svg>
SVG;
}

/**
 * Render Legend (5+ år + serieseger) badge - Magical golden tree (HIDDEN)
 */
function renderExp6Badge(): string {
    return <<<SVG
<svg class="badge-svg" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="exp6Bg" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFF8E1"/>
            <stop offset="100%" stop-color="#FFD54F"/>
        </linearGradient>
        <linearGradient id="trunk6" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#8D6E63"/>
            <stop offset="100%" stop-color="#5D4037"/>
        </linearGradient>
        <linearGradient id="goldenLeaves" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#FFA000"/>
        </linearGradient>
        <filter id="exp6Glow">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="exp6Shadow"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15"/></filter>
    </defs>
    <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="url(#exp6Bg)" stroke="#FFB300" stroke-width="2.5" filter="url(#exp6Shadow)"/>
    <!-- Magical glow -->
    <g filter="url(#exp6Glow)" opacity="0.5">
        <ellipse cx="50" cy="50" rx="40" ry="40" fill="#FFD700"/>
    </g>
    <!-- Sparkling stars around -->
    <path d="M15 25L17 30L22 30L18 33L19 38L15 35L11 38L12 33L8 30L13 30Z" fill="#FFD700"/>
    <path d="M85 30L87 35L92 35L88 38L89 43L85 40L81 43L82 38L78 35L83 35Z" fill="#FFD700"/>
    <path d="M12 75L13 78L16 78L14 80L14.5 83L12 81L9.5 83L10 80L8 78L11 78Z" fill="#FFC107"/>
    <path d="M88 70L89 73L92 73L90 75L90.5 78L88 76L85.5 78L86 75L84 73L87 73Z" fill="#FFC107"/>
    <!-- Magical tree -->
    <g transform="translate(50, 38)">
        <!-- Trunk (silvery) -->
        <path d="M-12 30 L-10 60 L10 60 L12 30" fill="url(#trunk6)"/>
        <!-- Roots -->
        <path d="M-10 58 Q-22 62 -28 68" stroke="#6D4C41" stroke-width="4" fill="none"/>
        <path d="M10 58 Q22 62 28 68" stroke="#6D4C41" stroke-width="4" fill="none"/>
        <!-- Branches -->
        <path d="M-10 35 L-32 12" stroke="url(#trunk6)" stroke-width="7"/>
        <path d="M10 30 L35 8" stroke="url(#trunk6)" stroke-width="7"/>
        <path d="M-6 25 L-22 2" stroke="url(#trunk6)" stroke-width="5"/>
        <path d="M6 20 L25 -5" stroke="url(#trunk6)" stroke-width="5"/>
        <!-- Golden crown -->
        <ellipse cx="0" cy="-8" rx="40" ry="32" fill="url(#goldenLeaves)"/>
        <circle cx="-22" cy="-18" r="16" fill="#FFD700"/>
        <circle cx="22" cy="-15" r="16" fill="#FFD700"/>
        <circle cx="0" cy="-32" r="14" fill="#FFEB3B"/>
        <circle cx="-32" cy="-2" r="13" fill="#FFD700"/>
        <circle cx="32" cy="0" r="13" fill="#FFD700"/>
        <!-- Highlights -->
        <circle cx="-15" cy="-25" r="8" fill="#FFF59D" opacity="0.7"/>
        <circle cx="12" cy="-28" r="7" fill="#FFF59D" opacity="0.7"/>
        <!-- Magic sparkles in tree -->
        <circle cx="-25" cy="-10" r="2" fill="#FFF" opacity="0.9"/>
        <circle cx="28" cy="-8" r="2" fill="#FFF" opacity="0.9"/>
        <circle cx="5" cy="-35" r="2" fill="#FFF" opacity="0.9"/>
        <circle cx="-10" cy="-20" r="1.5" fill="#FFF" opacity="0.8"/>
        <circle cx="18" cy="-22" r="1.5" fill="#FFF" opacity="0.8"/>
    </g>
    <!-- "LEGEND" ribbon -->
    <path d="M18 95 L50 102 L82 95 L82 108 L50 115 L18 108 Z" fill="#B8860B"/>
    <path d="M22 97 L50 103 L78 97 L78 106 L50 112 L22 106 Z" fill="#FFD700"/>
    <text x="50" y="107" text-anchor="middle" fill="#5D4037" font-size="9" font-weight="bold" font-family="system-ui">LEGEND</text>
</svg>
SVG;
}

// ============================================================================
// RENDER FUNCTIONS
// ============================================================================

/**
 * Render complete rider achievements section
 */
function renderRiderAchievements(PDO $pdo, int $rider_id, array $stats = null): string {
    if ($stats === null) {
        $stats = getRiderAchievementStats($pdo, $rider_id);
    }

    $expLevel = calculateExperienceLevel($stats['seasons_active'] ?? 1, $stats['has_series_win'] ?? false);
    $expLevelName = getExperienceLevelName($expLevel);
    $showLegend = ($expLevel === 6);

    ob_start();
    ?>
    <section class="section">
        <div class="achievements-card">
            <div class="achievements-card-header">
                <h3 class="achievements-card-title">Achievements</h3>
                <a href="/achievements" class="achievements-info-link">ℹ️ Visa alla</a>
            </div>

            <!-- Experience Slider -->
            <div class="exp-section">
                <div class="exp-header">
                    <div class="exp-label">
                        <?= renderExperienceIcon() ?>
                        <span class="exp-title"><?= htmlspecialchars($expLevelName) ?></span>
                    </div>
                    <span class="exp-since">Sedan <?= (int)($stats['first_season_year'] ?? date('Y')) ?></span>
                </div>
                <div class="exp-slider">
                    <?php for ($i = 1; $i <= 5; $i++): ?>
                        <div class="exp-step<?= $i <= $expLevel ? ' active' : '' ?>"></div>
                    <?php endfor; ?>
                    <div class="exp-step<?= $showLegend ? '' : ' hidden' ?><?= $expLevel === 6 ? ' active' : '' ?>"></div>
                </div>
                <div class="exp-labels">
                    <span class="<?= $expLevel === 1 ? 'active' : '' ?>">1:a året</span>
                    <span class="<?= $expLevel === 2 ? 'active' : '' ?>">2:a året</span>
                    <span class="<?= $expLevel === 3 ? 'active' : '' ?>">Erfaren</span>
                    <span class="<?= $expLevel === 4 ? 'active' : '' ?>">Expert</span>
                    <span class="<?= $expLevel >= 5 ? 'active' : '' ?>">Veteran</span>
                    <?php if ($showLegend): ?>
                        <span class="<?= $expLevel === 6 ? 'active' : '' ?>">Legend</span>
                    <?php endif; ?>
                </div>
            </div>

            <!-- Core Badge Grid -->
            <div class="badge-grid" data-rider-id="<?= $rider_id ?>">
                <div class="badge-item<?= ($stats['gold'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['gold'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="1:a plats i ett lopp" data-achievement="gold" data-label="Guld">
                    <?= renderGoldBadge() ?>
                    <span class="badge-value<?= ($stats['gold'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['gold'] ?? 0) > 0 ? $stats['gold'] : '–' ?></span>
                    <span class="badge-label">Guld</span>
                </div>

                <div class="badge-item<?= ($stats['silver'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['silver'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="2:a plats i ett lopp" data-achievement="silver" data-label="Silver">
                    <?= renderSilverBadge() ?>
                    <span class="badge-value<?= ($stats['silver'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['silver'] ?? 0) > 0 ? $stats['silver'] : '–' ?></span>
                    <span class="badge-label">Silver</span>
                </div>

                <div class="badge-item<?= ($stats['bronze'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['bronze'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="3:e plats i ett lopp" data-achievement="bronze" data-label="Brons">
                    <?= renderBronzeBadge() ?>
                    <span class="badge-value<?= ($stats['bronze'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['bronze'] ?? 0) > 0 ? $stats['bronze'] : '–' ?></span>
                    <span class="badge-label">Brons</span>
                </div>

                <div class="badge-item<?= ($stats['hot_streak'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['hot_streak'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="3+ pallplatser i rad" data-achievement="hot_streak" data-label="Pallserie">
                    <?= renderHotStreakBadge() ?>
                    <span class="badge-value<?= ($stats['hot_streak'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['hot_streak'] ?? 0) > 0 ? $stats['hot_streak'] : '–' ?></span>
                    <span class="badge-label">Pallserie</span>
                </div>

                <div class="badge-item<?= ($stats['series_completed'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['series_completed'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="100% fullföljt i en serie" data-achievement="series_completed" data-label="Fullföljt">
                    <?= renderFinisherBadge() ?>
                    <span class="badge-value<?= ($stats['series_completed'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['series_completed'] ?? 0) > 0 ? $stats['series_completed'] : '–' ?></span>
                    <span class="badge-label">Fullföljt</span>
                </div>

                <div class="badge-item<?= !($stats['is_serieledare'] ?? false) ? ' locked' : '' ?><?= ($stats['is_serieledare'] ?? false) ? ' clickable' : '' ?>" data-tooltip="Leder en serie" data-achievement="series_leader" data-label="Serieledare">
                    <?= renderSeriesLeaderBadge() ?>
                    <span class="badge-value<?= !($stats['is_serieledare'] ?? false) ? ' empty' : '' ?>"><?= ($stats['is_serieledare'] ?? false) ? 'Ja' : '–' ?></span>
                    <span class="badge-label">Serieledare</span>
                </div>

                <div class="badge-item<?= ($stats['series_wins'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['series_wins'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="Vunnit en serietotal" data-achievement="series_champion" data-label="Seriesegrare">
                    <?= renderSeriesChampionBadge() ?>
                    <span class="badge-value<?= ($stats['series_wins'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['series_wins'] ?? 0) > 0 ? $stats['series_wins'] : '–' ?></span>
                    <span class="badge-label">Seriesegrare</span>
                </div>

                <div class="badge-item<?= ($stats['sm_wins'] ?? 0) === 0 ? ' locked' : '' ?><?= ($stats['sm_wins'] ?? 0) > 0 ? ' clickable' : '' ?>" data-tooltip="Vunnit ett SM-event" data-achievement="swedish_champion" data-label="Svensk mästare">
                    <?= renderSwedishChampionBadge() ?>
                    <span class="badge-value<?= ($stats['sm_wins'] ?? 0) === 0 ? ' empty' : '' ?>"><?= ($stats['sm_wins'] ?? 0) > 0 ? $stats['sm_wins'] : '–' ?></span>
                    <span class="badge-label">Svensk mästare</span>
                </div>
            </div>

            <!-- Milestone Badges (if applicable) -->
            <?php
            $totalRaces = $stats['total_races'] ?? 0;
            if ($totalRaces >= 5):
            ?>
            <div class="badge-grid" style="margin-top: var(--space-md, 16px); padding-top: var(--space-md, 16px); border-top: 1px solid var(--achievement-border, #e0e0e0);">
                <div class="badge-item" data-tooltip="Första loppet genomfört">
                    <?= renderFirstRaceBadge() ?>
                    <span class="badge-value">✓</span>
                    <span class="badge-label">Debut</span>
                </div>

                <div class="badge-item<?= $totalRaces < 5 ? ' locked' : '' ?>" data-tooltip="5 lopp genomförda">
                    <?= render5RacesBadge() ?>
                    <span class="badge-value"><?= $totalRaces >= 5 ? '✓' : '–' ?></span>
                    <span class="badge-label">5 lopp</span>
                </div>

                <div class="badge-item<?= $totalRaces < 10 ? ' locked' : '' ?>" data-tooltip="10 lopp genomförda">
                    <?= render10RacesBadge() ?>
                    <span class="badge-value"><?= $totalRaces >= 10 ? '✓' : '–' ?></span>
                    <span class="badge-label">10 lopp</span>
                </div>

                <div class="badge-item<?= $totalRaces < 15 ? ' locked' : '' ?>" data-tooltip="15 lopp genomförda">
                    <?= render15RacesBadge() ?>
                    <span class="badge-value"><?= $totalRaces >= 15 ? '✓' : '–' ?></span>
                    <span class="badge-label">15 lopp</span>
                </div>

                <div class="badge-item<?= $totalRaces < 20 ? ' locked' : '' ?>" data-tooltip="20 lopp genomförda">
                    <?= render20RacesBadge() ?>
                    <span class="badge-value"><?= $totalRaces >= 20 ? '✓' : '–' ?></span>
                    <span class="badge-label">20 lopp</span>
                </div>

                <div class="badge-item<?= $totalRaces < 25 ? ' locked' : '' ?>" data-tooltip="25 lopp genomförda">
                    <?= render25RacesBadge() ?>
                    <span class="badge-value"><?= $totalRaces >= 25 ? '✓' : '–' ?></span>
                    <span class="badge-label">25 lopp</span>
                </div>

                <div class="badge-item<?= $totalRaces < 50 ? ' locked' : '' ?>" data-tooltip="50 lopp genomförda">
                    <?= render50RacesBadge() ?>
                    <span class="badge-value"><?= $totalRaces >= 50 ? '✓' : '–' ?></span>
                    <span class="badge-label">50 lopp</span>
                </div>
            </div>
            <?php endif; ?>
        </div>
    </section>

    <!-- Achievement Events Modal -->
    <div id="achievement-modal" class="achievement-modal" style="display: none;">
        <div class="achievement-modal-overlay" onclick="document.getElementById('achievement-modal').style.display='none';"></div>
        <div class="achievement-modal-content">
            <div class="achievement-modal-header">
                <h3 id="achievement-modal-title">Events</h3>
                <button type="button" class="achievement-modal-close" id="achievement-modal-close-btn" onclick="document.getElementById('achievement-modal').style.display='none'; return false;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
            </div>
            <div class="achievement-modal-body" id="achievement-modal-body">
                <div class="achievement-loading">Laddar...</div>
            </div>
        </div>
    </div>

    <style>
    .badge-item.clickable {
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .badge-item.clickable:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .achievement-modal {
        position: fixed;
        inset: 0;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--space-md, 16px);
    }
    .achievement-modal-overlay {
        position: absolute;
        inset: 0;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(2px);
        z-index: 1;
    }
    .achievement-modal-content {
        position: relative;
        z-index: 2;
        background: var(--color-bg-surface, #fff);
        border-radius: var(--radius-lg, 12px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        max-width: 500px;
        width: 100%;
        max-height: 80vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    .achievement-modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-md, 16px) var(--space-lg, 24px);
        border-bottom: 1px solid var(--color-border, #e5e7eb);
    }
    .achievement-modal-header h3 {
        margin: 0;
        font-size: 1.125rem;
        font-weight: 600;
    }
    .achievement-modal-close {
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--space-sm, 8px);
        color: var(--color-text-secondary, #666);
        border-radius: var(--radius-sm, 6px);
        position: relative;
        z-index: 10;
        min-width: 32px;
        min-height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .achievement-modal-close:hover {
        background: var(--color-bg-hover, #f3f4f6);
        color: var(--color-text, #333);
    }
    .achievement-modal-close svg {
        pointer-events: none;
    }
    .achievement-modal-body {
        padding: var(--space-lg, 24px);
        overflow-y: auto;
        flex: 1;
    }
    .achievement-loading {
        text-align: center;
        color: var(--color-text-secondary, #666);
        padding: var(--space-xl, 32px);
    }
    .achievement-event-list {
        list-style: none;
        margin: 0;
        padding: 0;
    }
    .achievement-event-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-sm, 8px) 0;
        border-bottom: 1px solid var(--color-border, #e5e7eb);
    }
    .achievement-event-item:last-child {
        border-bottom: none;
    }
    .achievement-event-item a {
        color: var(--color-accent, #61CE70);
        text-decoration: none;
        font-weight: 500;
    }
    .achievement-event-item a:hover {
        text-decoration: underline;
    }
    .achievement-event-meta {
        font-size: 0.875rem;
        color: var(--color-text-secondary, #666);
    }
    .achievement-event-position {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        font-weight: 600;
        font-size: 0.75rem;
        margin-right: var(--space-sm, 8px);
    }
    .achievement-event-position.p1 { background: #FFD700; color: #000; }
    .achievement-event-position.p2 { background: #C0C0C0; color: #000; }
    .achievement-event-position.p3 { background: #CD7F32; color: #fff; }
    .achievement-empty {
        text-align: center;
        color: var(--color-text-secondary, #666);
        padding: var(--space-lg, 24px);
    }
    </style>

    <script>
    (function() {
        // Click handler for achievement badges
        document.addEventListener('click', function(e) {
            const badge = e.target.closest('.badge-item.clickable');
            if (!badge) return;

            const grid = badge.closest('.badge-grid');
            const riderId = grid ? grid.dataset.riderId : null;
            const achievementType = badge.dataset.achievement;
            const label = badge.dataset.label || 'Events';

            if (!riderId || !achievementType) return;

            showAchievementModal(riderId, achievementType, label);
        });

        window.showAchievementModal = async function(riderId, type, label) {
            const modal = document.getElementById('achievement-modal');
            const title = document.getElementById('achievement-modal-title');
            const body = document.getElementById('achievement-modal-body');

            title.textContent = label;
            body.innerHTML = '<div class="achievement-loading">Laddar...</div>';
            modal.style.display = 'flex';

            try {
                const response = await fetch(`/api/achievement-events.php?rider_id=${riderId}&type=${type}`);
                const data = await response.json();

                if (data.success && data.events && data.events.length > 0) {
                    let html = '<ul class="achievement-event-list">';
                    data.events.forEach(event => {
                        const date = event.date ? new Date(event.date).toLocaleDateString('sv-SE') : '';
                        const posClass = event.position <= 3 ? 'p' + event.position : '';

                        if (event.series_name) {
                            // Series-type achievement
                            html += `<li class="achievement-event-item">
                                <div>
                                    <strong>${event.series_name}</strong>
                                    ${event.year ? `<span class="achievement-event-meta">(${event.year})</span>` : ''}
                                </div>
                            </li>`;
                        } else {
                            // Event-type achievement
                            html += `<li class="achievement-event-item">
                                <div>
                                    ${event.position ? `<span class="achievement-event-position ${posClass}">${event.position}</span>` : ''}
                                    <a href="/event/${event.id}">${event.name}</a>
                                    ${event.class_name ? `<span class="achievement-event-meta"> - ${event.class_name}</span>` : ''}
                                </div>
                                <span class="achievement-event-meta">${date}</span>
                            </li>`;
                        }
                    });
                    html += '</ul>';
                    body.innerHTML = html;
                } else {
                    body.innerHTML = '<div class="achievement-empty">Inga events hittades</div>';
                }
            } catch (error) {
                body.innerHTML = '<div class="achievement-empty">Kunde inte ladda events</div>';
                console.error('Achievement events error:', error);
            }
        };

        window.closeAchievementModal = function() {
            const modal = document.getElementById('achievement-modal');
            if (modal) {
                modal.style.display = 'none';
            }
        };

        // Close button click - use event delegation for reliability
        const closeBtn = document.getElementById('achievement-modal-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                closeAchievementModal();
            });
        }

        // Also add click handler directly to the modal for close button (fallback)
        const modal = document.getElementById('achievement-modal');
        if (modal) {
            modal.addEventListener('click', function(e) {
                // Close on overlay click
                if (e.target.classList.contains('achievement-modal-overlay')) {
                    closeAchievementModal();
                }
                // Close on X button click (anywhere in the button or SVG)
                if (e.target.closest('.achievement-modal-close')) {
                    e.preventDefault();
                    e.stopPropagation();
                    closeAchievementModal();
                }
            });
        }

        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeAchievementModal();
            }
        });
    })();
    </script>
    <?php
    return ob_get_clean();
}

/**
 * Get all rider achievement definitions for explanation page
 */
function getRiderAchievementDefinitions(): array {
    return [
        'placeringar' => [
            'title' => 'Placeringar',
            'icon' => 'trophy',
            'badges' => [
                ['id' => 'gold', 'name' => 'Guld', 'requirement' => '1:a plats i ett lopp', 'description' => 'Varje gång du vinner ett lopp får du ett guld.', 'has_counter' => true, 'accent' => '#FFD700', 'svg_function' => 'renderGoldBadge'],
                ['id' => 'silver', 'name' => 'Silver', 'requirement' => '2:a plats i ett lopp', 'description' => 'Varje andraplats ger dig ett silver.', 'has_counter' => true, 'accent' => '#C0C0C0', 'svg_function' => 'renderSilverBadge'],
                ['id' => 'bronze', 'name' => 'Brons', 'requirement' => '3:e plats i ett lopp', 'description' => 'Varje tredjeplats ger dig ett brons.', 'has_counter' => true, 'accent' => '#CD7F32', 'svg_function' => 'renderBronzeBadge']
            ]
        ],
        'prestationer' => [
            'title' => 'Prestationer',
            'icon' => 'trending-up',
            'badges' => [
                ['id' => 'hot_streak', 'name' => 'Pallserie', 'requirement' => '3+ pallplatser i rad', 'description' => 'När du tar 3 eller fler pallplatser i följd.', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderHotStreakBadge'],
                ['id' => 'finisher_100', 'name' => 'Fullföljare', 'requirement' => '100% fullföljt i en serie', 'description' => 'Fullföljt alla deltävlingar i en serie.', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderFinisherBadge'],
                ['id' => 'series_leader', 'name' => 'Serieledare', 'requirement' => 'Leder en serie', 'description' => 'Visas när du leder en aktiv serie.', 'has_counter' => false, 'accent' => '#EF761F', 'svg_function' => 'renderSeriesLeaderBadge'],
                ['id' => 'series_champion', 'name' => 'Seriesegrare', 'requirement' => 'Vunnit en serietotal', 'description' => 'Permanent badge för varje serie du vunnit.', 'has_counter' => true, 'accent' => '#FFD700', 'svg_function' => 'renderSeriesChampionBadge'],
                ['id' => 'swedish_champion', 'name' => 'Svensk mästare', 'requirement' => 'Vunnit ett SM-event', 'description' => 'Permanent badge för varje SM-titel.', 'has_counter' => true, 'accent' => '#004a98', 'svg_function' => 'renderSwedishChampionBadge']
            ]
        ],
        'lojalitet' => [
            'title' => 'Lojalitet & Uthållighet',
            'icon' => 'heart',
            'badges' => [
                ['id' => 'ironman', 'name' => 'IronRider', 'requirement' => 'Deltagit i ALLA serier under en säsong', 'description' => 'Du har tävlat i varje serie under ett helt år. Outtröttlig!', 'has_counter' => true, 'accent' => '#607D8B', 'svg_function' => 'renderIronmanBadge'],
                ['id' => 'club_hero', 'name' => 'Klubbhjälte', 'requirement' => '10+ starter för samma klubb', 'description' => 'Lojalitet mot din klubb belönas.', 'has_counter' => true, 'accent' => '#004a98', 'svg_function' => 'renderClubHeroBadge'],
                ['id' => 'loyal', 'name' => 'Trogen', 'requirement' => '3+ säsonger i rad utan uppehåll', 'description' => 'Du kommer tillbaka säsong efter säsong.', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderLoyalBadge'],
                ['id' => 'comeback', 'name' => 'Veteran Comeback', 'requirement' => 'Tillbaka efter 2+ säsongers uppehåll', 'description' => 'Välkommen tillbaka!', 'has_counter' => false, 'accent' => '#EF761F', 'svg_function' => 'renderComebackBadge']
            ]
        ],
        'utforskning' => [
            'title' => 'Mångfald & Utforskning',
            'icon' => 'compass',
            'badges' => [
                ['id' => 'allrounder', 'name' => 'Allrounder', 'requirement' => 'Tävlat i 3+ olika discipliner', 'description' => 'Enduro, DH, XCO, Dual Slalom - du gör allt!', 'has_counter' => false, 'accent' => '#8A9A5B', 'svg_function' => 'renderAllrounderBadge'],
                ['id' => 'adventurer', 'name' => 'Äventyrare', 'requirement' => 'Tävlat på 5+ olika banor', 'description' => 'Du utforskar nya platser.', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderAdventurerBadge'],
                ['id' => 'nomad', 'name' => 'Nomad', 'requirement' => 'Tävlat på 10+ olika banor', 'description' => 'En riktig resenär!', 'has_counter' => true, 'accent' => '#FFE009', 'svg_function' => 'renderNomadBadge']
            ]
        ],
        'prestation' => [
            'title' => 'Prestationer & Rekord',
            'icon' => 'zap',
            'badges' => [
                ['id' => 'rocket', 'name' => 'Raketstart', 'requirement' => 'Pallplats i första tävlingen', 'description' => 'En imponerande debut!', 'has_counter' => false, 'accent' => '#EF761F', 'svg_function' => 'renderRocketStartBadge'],
                ['id' => 'consistent', 'name' => 'Konsekvent', 'requirement' => 'Topp 10 i alla deltävlingar i en serie', 'description' => 'Stabil prestation genom hela serien.', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderConsistentBadge'],
                ['id' => 'improver', 'name' => 'Förbättrare', 'requirement' => 'Förbättrat placering 5 lopp i rad', 'description' => 'Du blir bättre för varje lopp!', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderImproverBadge']
            ]
        ],
        'milstolpar' => [
            'title' => 'Milstolpar',
            'icon' => 'flag',
            'badges' => [
                ['id' => 'first_race', 'name' => 'Första Loppet', 'requirement' => 'Genomfört första tävlingen', 'description' => 'Välkommen till GravitySeries!', 'has_counter' => false, 'accent' => '#61CE70', 'svg_function' => 'renderFirstRaceBadge'],
                ['id' => 'races_10', 'name' => '10 Lopp', 'requirement' => '10 genomförda lopp', 'description' => 'Du börjar få erfarenhet.', 'has_counter' => false, 'accent' => '#61CE70', 'svg_function' => 'render10RacesBadge'],
                ['id' => 'races_25', 'name' => '25 Lopp', 'requirement' => '25 genomförda lopp', 'description' => 'En erfaren tävlande!', 'has_counter' => false, 'accent' => '#C0C0C0', 'svg_function' => 'render25RacesBadge'],
                ['id' => 'races_50', 'name' => '50 Lopp', 'requirement' => '50 genomförda lopp', 'description' => 'En veteran!', 'has_counter' => false, 'accent' => '#FFD700', 'svg_function' => 'render50RacesBadge'],
                ['id' => 'races_100', 'name' => '100 Lopp', 'requirement' => '100 genomförda lopp', 'description' => 'Legendstatus uppnådd!', 'has_counter' => false, 'accent' => '#FFD700', 'svg_function' => 'render100RacesBadge']
            ]
        ],
        'sasong' => [
            'title' => 'Årstider & Timing',
            'icon' => 'calendar',
            'badges' => [
                ['id' => 'season_starter', 'name' => 'Säsongsstartare', 'requirement' => 'Deltog i säsongens första tävling', 'description' => 'Du var med från start!', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderSeasonStarterBadge'],
                ['id' => 'season_finisher', 'name' => 'Finisher', 'requirement' => 'Deltog i säsongens sista tävling', 'description' => 'Du höll ut till slutet!', 'has_counter' => true, 'accent' => '#61CE70', 'svg_function' => 'renderSeasonFinisherBadge']
            ]
        ],
        'social' => [
            'title' => 'Community',
            'icon' => 'share-2',
            'badges' => [
                ['id' => 'connected', 'name' => 'Connected', 'requirement' => 'Länkat minst ett socialt media-konto', 'description' => 'Du har kopplat din profil till sociala medier.', 'has_counter' => false, 'accent' => '#1DA1F2', 'svg_function' => 'renderConnectedBadge']
            ]
        ],
        'experience' => [
            'title' => 'Erfarenhet',
            'icon' => 'star',
            'badges' => [
                ['id' => 'exp_1', 'name' => '1:a året', 'requirement' => 'Första säsongen', 'description' => 'Du är ny på GravitySeries!', 'has_counter' => false, 'accent' => '#61CE70'],
                ['id' => 'exp_2', 'name' => '2:a året', 'requirement' => 'Andra säsongen', 'description' => 'Du har kommit tillbaka.', 'has_counter' => false, 'accent' => '#61CE70'],
                ['id' => 'exp_3', 'name' => 'Erfaren', 'requirement' => 'Tredje säsongen', 'description' => 'Tre säsonger under bältet.', 'has_counter' => false, 'accent' => '#61CE70'],
                ['id' => 'exp_4', 'name' => 'Expert', 'requirement' => 'Fjärde säsongen', 'description' => 'En expert på serien.', 'has_counter' => false, 'accent' => '#61CE70'],
                ['id' => 'exp_5', 'name' => 'Veteran', 'requirement' => 'Femte säsongen', 'description' => 'Du är en veteran!', 'has_counter' => false, 'accent' => '#61CE70'],
                ['id' => 'exp_6', 'name' => 'Legend', 'requirement' => '5+ säsonger OCH minst 1 serieseger', 'description' => 'Dold tills uppnådd.', 'has_counter' => false, 'accent' => '#FFD700', 'hidden' => true]
            ]
        ]
    ];
}
