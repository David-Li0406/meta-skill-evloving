<?php
$currentPage = $pageInfo['page'] ?? 'dashboard';

// Pages that have their own breadcrumb/navigation (don't show global back link)
$pagesWithOwnNav = [
    'calendar-event',
    'series-show',
    'database-rider',
    'database-club',
    'results-event',
    'event',
    'profile-edit',
    'profile-children',
    'profile-registrations',
    'profile-results',
    'profile-receipts'
];

// Index pages - no back link needed (they ARE the destination from nav)
$indexPages = [
    'calendar-index',
    'results-index',
    'series-index',
    'database-index',
    'ranking-index',
    'profile-index'
];

// Don't show back link on:
// - dashboard/welcome (home pages)
// - pages with their own navigation
// - index pages (main section entry points)
$isIndexPage = in_array($currentPage, $indexPages) || str_ends_with($currentPage, '-index');
if ($currentPage !== 'dashboard' && $currentPage !== 'welcome' && !in_array($currentPage, $pagesWithOwnNav) && !$isIndexPage):
?>
<nav class="back-nav" aria-label="Navigation">
  <a href="javascript:history.back()" class="back-link">
    <span class="back-arrow">←</span>
    <span>Tillbaka</span>
  </a>
</nav>
<?php endif; ?>
