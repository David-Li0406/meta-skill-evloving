<?php
/**
 * Bottom Navigation - Visas på mobil (samma items som desktop header-nav)
 * 5 items: Kalender, Resultat, Serier, Ranking, Profil
 */

$currentPage = basename($_SERVER['PHP_SELF']);
$currentPath = $_SERVER['PHP_SELF'];

$navItems = [
    ['id' => 'events', 'label' => 'Kalender', 'url' => '/calendar', 'icon' => 'calendar'],
    ['id' => 'results', 'label' => 'Resultat', 'url' => '/results', 'icon' => 'flag'],
    ['id' => 'series', 'label' => 'Serier', 'url' => '/series', 'icon' => 'trophy'],
    ['id' => 'ranking', 'label' => 'Ranking', 'url' => '/ranking', 'icon' => 'trending-up'],
    ['id' => 'profile', 'label' => 'Profil', 'url' => '/profile', 'icon' => 'user'],
];

// SVG ikoner
$icons = [
    'calendar' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>',
    'flag' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/></svg>',
    'trophy' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>',
    'trending-up' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    'user' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
];
?>

<nav class="nav-bottom" role="navigation" aria-label="Huvudnavigering">
    <?php foreach ($navItems as $item): ?>
        <?php
        // Determine if this item is active
        $isActive = false;
        if ($item['id'] === 'ranking' && ($currentPage === 'ranking.php' || strpos($currentPath, '/ranking/') !== false)) {
            $isActive = true;
        } elseif ($item['id'] === 'events' && ($currentPage === 'events.php' || $currentPage === 'calendar.php')) {
            $isActive = true;
        } elseif ($item['id'] === 'profile' && $currentPage === 'profile.php') {
            $isActive = true;
        } elseif ($item['id'] !== 'ranking' && $item['id'] !== 'profile') {
            $isActive = ($currentPage === $item['id'] . '.php');
        }
        ?>
        <a href="<?= $item['url'] ?>"
           class="nav-bottom-item <?= $isActive ? 'is-active' : '' ?>"
           <?= $isActive ? 'aria-current="page"' : '' ?>>
            <span class="nav-bottom-icon"><?= $icons[$item['icon']] ?></span>
            <span class="nav-bottom-label"><?= $item['label'] ?></span>
        </a>
    <?php endforeach; ?>
</nav>
