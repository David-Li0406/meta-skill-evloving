<?php
/**
 * Flik-konfiguration för admin-grupper
 * Definierar flikar för varje huvudgrupp i Admin 2.0
 *
 * Struktur:
 * 1. Tävlingar - Events, resultat, venues, biljetter
 * 2. Serier - Serier, ranking, klubbpoäng
 * 3. Deltagare - Deltagare och klubbar
 * 4. Konfiguration - Klasser, licenser, poängskalor, regler, texter
 * 5. Import - All dataimport
 * 6. System - Användarhantering och systemadmin (super admin)
 */

$ADMIN_TABS = [

    // ========================================
    // TÄVLINGAR
    // ========================================
    'competitions' => [
        'title' => 'Tävlingar',
        'icon' => 'calendar-check',
        'tabs' => [
            [
                'id' => 'events',
                'label' => 'Events',
                'icon' => 'calendar',
                'url' => '/admin/events.php',
                'pages' => ['events.php', 'event-create.php', 'event-edit.php', 'event-delete.php', 'event-map.php']
            ],
            [
                'id' => 'results',
                'label' => 'Resultat',
                'icon' => 'trophy',
                'url' => '/admin/results.php',
                'pages' => ['results.php', 'edit-results.php', 'clear-event-results.php']
            ],
            [
                'id' => 'global-texts',
                'label' => 'Texter',
                'icon' => 'file-text',
                'url' => '/admin/global-texts.php',
                'pages' => ['global-texts.php']
            ],
            [
                'id' => 'pricing-templates',
                'label' => 'Prismallar',
                'icon' => 'receipt',
                'url' => '/admin/pricing-templates.php',
                'pages' => ['pricing-templates.php'],
                'role' => 'super_admin' // Only visible for super_admin
            ],
            [
                'id' => 'elimination',
                'label' => 'Elimination',
                'icon' => 'git-branch',
                'url' => '/admin/elimination.php',
                'pages' => ['elimination.php', 'elimination-manage.php', 'elimination-live.php', 'elimination-import-qualifying.php', 'elimination-add-qualifying.php', 'elimination-create.php']
            ],
            [
                'id' => 'classes',
                'label' => 'Klasser',
                'icon' => 'layers',
                'url' => '/admin/classes.php',
                'pages' => ['classes.php']
            ]
        ]
    ],

    // ========================================
    // SERIER
    // ========================================
    'standings' => [
        'title' => 'Serier',
        'icon' => 'medal',
        'tabs' => [
            [
                'id' => 'series',
                'label' => 'Serier',
                'icon' => 'award',
                'url' => '/admin/series.php',
                'pages' => ['series.php', 'series-events.php', 'series-pricing.php', 'series-manage.php', 'series-edit.php']
            ],
            [
                'id' => 'ranking',
                'label' => 'Ranking',
                'icon' => 'trending-up',
                'url' => '/admin/ranking.php',
                'pages' => ['ranking.php', 'ranking-minimal.php']
            ],
            [
                'id' => 'club-points',
                'label' => 'Klubbpoäng',
                'icon' => 'building-2',
                'url' => '/admin/club-points.php',
                'pages' => ['club-points.php', 'club-points-detail.php']
            ],
            [
                'id' => 'rules',
                'label' => 'Anmälningsregler',
                'icon' => 'shield-check',
                'url' => '/admin/registration-rules.php',
                'pages' => ['registration-rules.php']
            ]
        ]
    ],

    // ========================================
    // DATABAS (Riders + Clubs under one section)
    // ========================================
    'database' => [
        'title' => 'Databas',
        'icon' => 'database',
        'tabs' => [
            [
                'id' => 'riders',
                'label' => 'Deltagare',
                'icon' => 'user',
                'url' => '/admin/riders.php',
                'pages' => ['riders.php', 'rider-edit.php', 'rider-delete.php', 'enrich-riders.php', 'check-license-numbers.php']
            ],
            [
                'id' => 'clubs',
                'label' => 'Klubbar',
                'icon' => 'building-2',
                'url' => '/admin/clubs.php',
                'pages' => ['clubs.php', 'club-edit.php']
            ],
            [
                'id' => 'destinations',
                'label' => 'Destinations',
                'icon' => 'mountain',
                'url' => '/admin/destinations.php',
                'pages' => ['destinations.php', 'destination-edit.php', 'venues.php', 'venue-edit.php', 'destination-duplicates.php']
            ]
        ]
    ],

    // ========================================
    // KONFIGURATION
    // ========================================
    'config' => [
        'title' => 'Konfiguration',
        'icon' => 'sliders',
        'tabs' => [
            [
                // EKONOMI - Samlar allt betalningsrelaterat på ett ställe
                'id' => 'economy',
                'label' => 'Ekonomi',
                'icon' => 'wallet',
                'url' => '/admin/ekonomi.php',
                'pages' => [
                    // Huvudpanel
                    'ekonomi.php',
                    // Ordrar & betalningar
                    'orders.php',
                    'payment-settings.php',
                    'payment-recipients.php',
                    'gateway-settings.php',
                    'certificates.php',
                    'swish-accounts.php',
                    // Event-specifika
                    'event-payment.php',
                    'event-orders.php',
                    'event-registrations.php',
                    'event-ticketing.php',
                    'event-pricing.php',
                    // Biljetter & prismallar
                    'ticketing.php',
                    'event-tickets.php',
                    'refund-requests.php',
                    'pricing-templates.php',
                    'pricing-template-edit.php',
                    // Rabatter
                    'discount-codes.php',
                    'gravity-id.php',
                    // Anmälningsregler
                    'registration-rules.php',
                    // Promotor
                    'promotor-payments.php'
                ]
            ],
            [
                'id' => 'discount-codes',
                'label' => 'Rabattkoder',
                'icon' => 'tag',
                'url' => '/admin/discount-codes.php',
                'pages' => ['discount-codes.php']
            ],
            [
                'id' => 'gravity-id',
                'label' => 'Gravity ID',
                'icon' => 'badge-check',
                'url' => '/admin/gravity-id.php',
                'pages' => ['gravity-id.php']
            ],
            [
                'id' => 'license-matrix',
                'label' => 'Licenser',
                'icon' => 'grid-3x3',
                'url' => '/admin/license-class-matrix.php',
                'pages' => ['license-class-matrix.php']
            ],
            [
                'id' => 'point-scales',
                'label' => 'Poängskalor',
                'icon' => 'calculator',
                'url' => '/admin/point-scales.php',
                'pages' => ['point-scales.php', 'point-scale-edit.php', 'point-templates.php']
            ],
            [
                'id' => 'public',
                'label' => 'Publikt',
                'icon' => 'globe',
                'url' => '/admin/public-settings.php',
                'pages' => ['public-settings.php']
            ],
            [
                'id' => 'media',
                'label' => 'Media',
                'icon' => 'image',
                'url' => '/admin/media.php',
                'pages' => ['media.php']
            ],
            [
                'id' => 'sponsors',
                'label' => 'Sponsorer',
                'icon' => 'heart-handshake',
                'url' => '/admin/sponsors.php',
                'pages' => ['sponsors.php', 'sponsor-edit.php']
            ],
            [
                'id' => 'sponsor-placements',
                'label' => 'Reklamplatser',
                'icon' => 'layout-grid',
                'url' => '/admin/sponsor-placements.php',
                'pages' => ['sponsor-placements.php'],
                'role' => 'super_admin'
            ],
            [
                'id' => 'race-reports',
                'label' => 'Race Reports',
                'icon' => 'file-text',
                'url' => '/admin/race-reports.php',
                'pages' => ['race-reports.php', 'race-report-edit.php'],
                'role' => 'super_admin'
            ],
            [
                'id' => 'news-moderation',
                'label' => 'Nyheter',
                'icon' => 'newspaper',
                'url' => '/admin/news-moderation.php',
                'pages' => ['news-moderation.php']
            ]
        ]
    ],

    // ========================================
    // ANALYTICS (super_admin eller statistics-behorighet)
    // ========================================
    'analytics' => [
        'title' => 'Analytics',
        'icon' => 'chart-line',
        'super_admin_only' => true,  // Visas bara for super_admin (eller statistics-behorighet via hasPermission)
        'tabs' => [
            [
                'id' => 'dashboard',
                'label' => 'Dashboard',
                'icon' => 'layout-dashboard',
                'url' => '/admin/analytics-dashboard.php',
                // Alla analytics-sidor nås via dashboard navigation grid
                'pages' => [
                    'analytics-dashboard.php',
                    'analytics-cohorts.php',
                    'analytics-atrisk.php',
                    'analytics-geography.php',
                    'analytics-flow.php',
                    'analytics-reports.php',
                    'analytics-clubs.php',
                    'analytics-trends.php',
                    'analytics-series-compare.php',
                    'analytics-first-season.php',
                    'analytics-event-participation.php',
                    'analytics-class-structure.php',
                    'analytics-data-quality.php',
                    'analytics-diagnose.php',
                    'analytics-export-center.php',
                    'analytics-populate.php',
                    'analytics-reset.php',
                    'analytics-report.php'
                ]
            ]
        ]
    ],

    // ========================================
    // IMPORT
    // ========================================
    'import' => [
        'title' => 'Import',
        'icon' => 'upload',
        'tabs' => [
            [
                'id' => 'overview',
                'label' => 'Översikt',
                'icon' => 'layout-grid',
                'url' => '/admin/import.php',
                'pages' => ['import.php']
            ],
            [
                'id' => 'riders',
                'label' => 'Deltagare',
                'icon' => 'user-plus',
                'url' => '/admin/import-riders.php',
                'pages' => ['import-riders.php', 'import-gravity-id.php']
            ],
            [
                'id' => 'results',
                'label' => 'Resultat',
                'icon' => 'file-spreadsheet',
                'url' => '/admin/import-results.php',
                'pages' => ['import-results.php', 'import-results-preview.php']
            ],
            [
                'id' => 'events',
                'label' => 'Events',
                'icon' => 'calendar-plus',
                'url' => '/admin/import-events.php',
                'pages' => ['import-events.php', 'import-series.php', 'import-classes.php', 'import-clubs.php']
            ],
            [
                'id' => 'uci',
                'label' => 'UCI',
                'icon' => 'globe',
                'url' => '/admin/import-uci.php',
                'pages' => ['import-uci.php', 'import-uci-preview.php']
            ],
            [
                'id' => 'venues',
                'label' => 'Venues',
                'icon' => 'mountain',
                'url' => '/admin/import-venues.php',
                'pages' => ['import-venues.php']
            ],
            [
                'id' => 'history',
                'label' => 'Historik',
                'icon' => 'history',
                'url' => '/admin/import-history.php',
                'pages' => ['import-history.php']
            ]
        ]
    ],

    // ========================================
    // SYSTEM (Super Admin)
    // ========================================
    'settings' => [
        'title' => 'System',
        'icon' => 'settings',
        'super_admin_only' => true,
        'tabs' => [
            [
                'id' => 'users',
                'label' => 'Användare',
                'icon' => 'users',
                'url' => '/admin/users.php',
                'pages' => ['users.php', 'user-edit.php', 'user-events.php', 'user-rider.php']
            ],
            [
                'id' => 'permissions',
                'label' => 'Behörigheter',
                'icon' => 'shield',
                'url' => '/admin/role-permissions.php',
                'pages' => ['role-permissions.php']
            ],
            [
                'id' => 'system',
                'label' => 'Databas',
                'icon' => 'server',
                'url' => '/admin/system-settings.php',
                'pages' => ['system-settings.php', 'settings.php', 'run-migrations.php', 'recalculate-all-points.php', 'fix-time-format.php', 'debug-series-points.php', 'clear-cache.php']
            ],
            [
                'id' => 'tools',
                'label' => 'Verktyg',
                'icon' => 'wrench',
                'url' => '/admin/tools.php',
                'pages' => [
                    'tools.php',
                    'normalize-names.php',
                    'find-duplicates.php',
                    'cleanup-duplicates.php',
                    'cleanup-clubs.php',
                    'search-uci-id.php',
                    'diagnose-series.php',
                    'rebuild-stats.php',
                    'fix-result-club-ids.php',
                    'sync-club-membership.php',
                    'sync-rider-clubs.php',
                    // Tools subfolder
                    'tools/yearly-rebuild.php',
                    'tools/yearly-import-review.php',
                    'tools/analyze-data-quality.php',
                    'tools/diagnose-class-errors.php',
                    'tools/diagnose-club-times.php',
                    'tools/fix-club-times.php',
                    'tools/fix-uci-conflicts.php',
                    'tools/auto-create-venues.php'
                ]
            ],
            [
                'id' => 'branding',
                'label' => 'Branding',
                'icon' => 'palette',
                'url' => '/admin/branding.php',
                'pages' => ['branding.php']
            ],
            [
                'id' => 'scf-license',
                'label' => 'SCF Licens',
                'icon' => 'badge-check',
                'url' => '/admin/scf-sync-status.php',
                'pages' => ['scf-sync-status.php', 'scf-match-review.php']
            ]
        ]
    ]
];

/**
 * Hämta aktiv flik baserat på nuvarande sida
 *
 * @param string $group Grupp-ID
 * @param string $current_page Nuvarande sidnamn
 * @return string|null Flik-ID eller null
 */
function get_active_tab($group, $current_page) {
    global $ADMIN_TABS;

    if (!isset($ADMIN_TABS[$group])) {
        return null;
    }

    foreach ($ADMIN_TABS[$group]['tabs'] as $tab) {
        if (in_array($current_page, $tab['pages'])) {
            return $tab['id'];
        }
    }

    // Default till första fliken
    return $ADMIN_TABS[$group]['tabs'][0]['id'];
}

/**
 * Hämta grupp för en sida
 *
 * @param string $current_page Nuvarande sidnamn
 * @return string|null Grupp-ID eller null
 */
function get_group_for_page($current_page) {
    global $ADMIN_TABS;

    foreach ($ADMIN_TABS as $group_id => $group) {
        foreach ($group['tabs'] as $tab) {
            if (in_array($current_page, $tab['pages'])) {
                return $group_id;
            }
        }
    }

    return null;
}

/**
 * Hämta alla sidor i en grupp
 *
 * @param string $group Grupp-ID
 * @return array Lista med sidnamn
 */
function get_pages_in_group($group) {
    global $ADMIN_TABS;

    if (!isset($ADMIN_TABS[$group])) {
        return [];
    }

    $pages = [];
    foreach ($ADMIN_TABS[$group]['tabs'] as $tab) {
        $pages = array_merge($pages, $tab['pages']);
    }

    return $pages;
}
?>
