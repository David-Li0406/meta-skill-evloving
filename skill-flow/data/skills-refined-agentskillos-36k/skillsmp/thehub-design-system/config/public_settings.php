<?php
/**
 * Public Display Settings
 * Configure what data is visible on the public website
 */

return [
    // Show all riders publicly or only those with results
    // Options: 'all' or 'with_results'
    'public_riders_display' => 'with_results',

    // Minimum number of results required to show rider (when 'with_results' is selected)
    'min_results_to_show' => 1,

    // Filter riders by discipline
    // Options: null (all disciplines), 'Road', 'Mtb', 'Gravel', 'Cx'
    // This helps reduce database load when you have 3000+ riders
    // Example: Set to 'Mtb' to only show MTB riders
    'filter_discipline' => null,
];
