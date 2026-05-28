<?php
/**
 * Admin Competition Tabs - Shared tabs for Events group
 * Include this file in all pages under Tävlingar group
 *
 * Usage: $active_tab = 'events'; include 'components/competition-tabs.php';
 * Valid tabs: events, results, classes, payments
 */

$active_tab = $active_tab ?? 'events';
?>
<!-- Competition Tabs -->
<div class="admin-tabs">
    <a href="/admin/events" class="admin-tab <?= $active_tab === 'events' ? 'active' : '' ?>">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
        Events
    </a>
    <a href="/admin/results.php" class="admin-tab <?= $active_tab === 'results' ? 'active' : '' ?>">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
        Resultat
    </a>
    <a href="/admin/classes" class="admin-tab <?= $active_tab === 'classes' ? 'active' : '' ?>">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/></svg>
        Klasser
    </a>
    <a href="/admin/orders.php" class="admin-tab <?= $active_tab === 'payments' ? 'active' : '' ?>">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
        Betalningar
    </a>
</div>
