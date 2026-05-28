<?php
require_once __DIR__ . '/../config.php';
require_admin();

$template = $_GET['template'] ?? '';

if ($template === 'riders') {
    // CSV template for riders
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub_riders_template.csv"');

    $output = fopen('php://output', 'w');

    // BOM for UTF-8
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));

    // Headers
    // Note: personnummer column is supported for import but only birth_year is extracted and stored
    // The personnummer itself is NOT stored in the database
    fputcsv($output, [
        'first_name',
        'last_name',
        'personnummer',  // Parsed to extract birth_year only - NOT stored
        'birth_year',
        'uci_id',
        'swe_id',
        'club_name',
        'gender',
        'license_type',
        'license_category',
        'discipline',
        'license_valid_until'
    ]);

    // Example rows
    fputcsv($output, [
        'Johan',
        'Andersson',
        '19950525-1234',  // Personnummer (parsas automatiskt)
        '',               // Birth year (lämnas tom om personnummer finns)
        'SWE19950101',
        '',
        'Uppsala Cykelklubb',
        'M',
        'Elite',
        'Elite Men',      // Licenskategori
        'MTB',           // Gren
        '2025-12-31'     // Licens giltig till
    ]);

    fputcsv($output, [
        'Emma',
        'Svensson',
        '19980315-5678',
        '',
        'SWE19980315',
        '',
        'Göteborg MTB',
        'F',
        'Elite',
        'Elite Women',
        'Road',
        '2025-12-31'
    ]);

    fputcsv($output, [
        'Erik',
        'Nilsson',
        '',              // Inget personnummer
        '2003',          // Använd birth_year istället
        '',              // UCI-ID (autogenereras SWE-ID om tomt)
        '',
        'Stockholm CK',
        'M',
        'Youth',
        'U21 Men',
        'CX',
        '2025-12-31'
    ]);

    fputcsv($output, [
        'Anna',
        'Bergström',
        '850812-9876',   // Kort format (YYMMDD-XXXX)
        '',
        'SWE19850812',
        '',
        'Luleå CK',
        'F',
        'Elite',
        'Master Women 35+',
        'MTB',
        '2025-12-31'
    ]);

    fclose($output);
    exit;
}

if ($template === 'results') {
    // CSV template for Enduro results
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub_enduro_results_template.csv"');

    $output = fopen('php://output', 'w');

    // BOM for UTF-8
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));

    // Headers - Enduro format
    fputcsv($output, [
        'Category',
        'PlaceByCategory',
        'FirstName',
        'LastName',
        'Club',
        'UCI-ID',
        'NetTime',
        'Status',
        'SS1',
        'SS2',
        'SS3',
        'SS4',
        'SS5'
    ]);

    // Example rows
    fputcsv($output, [
        'Herrar Elite',
        '1',
        'Johan',
        'ANDERSSON',
        'Uppsala Cykelklubb',
        '10019950101',
        '0:14:16.42',
        'FIN',
        '0:01:58.22',
        '0:01:38.55',
        '0:01:42.33',
        '0:01:55.88',
        '0:01:24.12'
    ]);

    fputcsv($output, [
        'Herrar Elite',
        '2',
        'Erik',
        'NILSSON',
        'Stockholm CK',
        '10020031201',
        '0:14:28.35',
        'FIN',
        '0:02:01.15',
        '0:01:41.22',
        '0:01:45.08',
        '0:01:58.45',
        '0:01:26.78'
    ]);

    fputcsv($output, [
        'Damer Elite',
        '1',
        'Emma',
        'SVENSSON',
        'Göteborg MTB',
        '10019980315',
        '0:15:45.78',
        'FIN',
        '0:02:12.45',
        '0:01:52.33',
        '0:01:58.66',
        '0:02:08.12',
        '0:01:35.45'
    ]);

    fputcsv($output, [
        'Herrar Elite',
        '',
        'Lars',
        'PERSSON',
        'Umeå MTB',
        '10019940205',
        '',
        'DNF',
        '0:02:05.12',
        '0:01:45.33',
        '',
        '',
        ''
    ]);

    fclose($output);
    exit;
}

if ($template === 'results_dh') {
    // CSV template for Downhill results (two runs)
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub_dh_results_template.csv"');

    $output = fopen('php://output', 'w');

    // BOM for UTF-8
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));

    // Headers - DH format
    fputcsv($output, [
        'Category',
        'PlaceByCategory',
        'FirstName',
        'LastName',
        'Club',
        'UCI-ID',
        'NetTime',
        'Status',
        'Run1',
        'Run2'
    ]);

    // Example rows - Standard DH (both runs, fastest counts)
    fputcsv($output, [
        'Herrar Elite',
        '1',
        'Johan',
        'ANDERSSON',
        'Uppsala Cykelklubb',
        '10019950101',
        '0:03:05.12',
        'FIN',
        '0:03:07.45',
        '0:03:05.12'
    ]);

    fputcsv($output, [
        'Herrar Elite',
        '2',
        'Erik',
        'NILSSON',
        'Stockholm CK',
        '10020031201',
        '0:03:06.89',
        'FIN',
        '0:03:08.23',
        '0:03:06.89'
    ]);

    fputcsv($output, [
        'Damer Elite',
        '1',
        'Emma',
        'SVENSSON',
        'Göteborg MTB',
        '10019980315',
        '0:03:15.78',
        'FIN',
        '0:03:18.45',
        '0:03:15.78'
    ]);

    fputcsv($output, [
        'Herrar Elite',
        '',
        'Lars',
        'PERSSON',
        'Umeå MTB',
        '10019940205',
        '',
        'DNF',
        '0:03:12.45',
        ''
    ]);

    fclose($output);
    exit;
}

// If no template selected
header('HTTP/1.1 400 Bad Request');
die('Invalid template requested. Use ?template=riders, ?template=results, or ?template=results_dh');
