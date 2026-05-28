<?php
/**
 * Diagnose Class Assignment Errors
 * Finds riders in "Motion Kids" who based on age should be in age-based classes
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();
$currentYear = (int)date('Y');

$pageTitle = 'Diagnostik: Felaktiga klassplaceringar';
include __DIR__ . '/../components/unified-layout.php';
?>

<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="search"></i> Söker efter felaktiga klassplaceringar...</h3>
    </div>
    <div class="card-body">

<?php
// Find all results where rider is in Motion Kids but based on age should be elsewhere
$query = "
    SELECT
        r.id as result_id,
        r.event_id,
        r.class_id,
        r.position,
        e.name as event_name,
        e.date as event_date,
        YEAR(e.date) as event_year,
        c.name as class_name,
        c.display_name as class_display_name,
        rid.id as rider_id,
        rid.firstname,
        rid.lastname,
        rid.birth_year,
        rid.gender,
        (YEAR(e.date) - rid.birth_year) as age_at_event
    FROM results r
    INNER JOIN events e ON r.event_id = e.id
    INNER JOIN classes c ON r.class_id = c.id
    INNER JOIN riders rid ON r.cyclist_id = rid.id
    WHERE (c.name LIKE '%motion%' OR c.display_name LIKE '%motion%')
      AND rid.birth_year IS NOT NULL
      AND rid.birth_year > 0
    ORDER BY e.date DESC, rid.lastname, rid.firstname
";

$results = $db->getAll($query);

// Group by potential issue
$issues = [];
foreach ($results as $row) {
    $age = $row['age_at_event'];
    $gender = $row['gender'];

    // Determine what class they SHOULD be in based on age
    $expectedClass = null;
    if ($age >= 13 && $age <= 14) {
        $expectedClass = $gender === 'F' ? 'Flickor 13-14' : 'Pojkar 13-14';
    } elseif ($age >= 15 && $age <= 16) {
        $expectedClass = $gender === 'F' ? 'Flickor 15-16' : 'Pojkar 15-16';
    } elseif ($age >= 17 && $age <= 18) {
        $expectedClass = $gender === 'F' ? 'Flickor 17-18' : 'Pojkar 17-18';
    } elseif ($age >= 19 && $age <= 34) {
        $expectedClass = $gender === 'F' ? 'Damer' : 'Herrar';
    } elseif ($age >= 35) {
        $expectedClass = $gender === 'F' ? 'Damer 35+' : 'Herrar 35+';
    }

    // If they're in Motion Kids but should be in an age class, flag it
    if ($expectedClass && $age >= 13) {
        $issues[] = [
            'result_id' => $row['result_id'],
            'event_id' => $row['event_id'],
            'event_name' => $row['event_name'],
            'event_date' => $row['event_date'],
            'rider_id' => $row['rider_id'],
            'rider_name' => $row['firstname'] . ' ' . $row['lastname'],
            'birth_year' => $row['birth_year'],
            'age' => $age,
            'gender' => $gender,
            'current_class' => $row['class_display_name'] ?: $row['class_name'],
            'expected_class' => $expectedClass
        ];
    }
}

// Group by event
$byEvent = [];
foreach ($issues as $issue) {
    $eventKey = $issue['event_id'];
    if (!isset($byEvent[$eventKey])) {
        $byEvent[$eventKey] = [
            'event_name' => $issue['event_name'],
            'event_date' => $issue['event_date'],
            'riders' => []
        ];
    }
    $byEvent[$eventKey]['riders'][] = $issue;
}

if (empty($issues)) {
    echo '<div class="alert alert-success"><i data-lucide="check-circle"></i> Inga uppenbara fel hittades!</div>';
} else {
    echo '<div class="alert alert-warning mb-md">';
    echo '<strong>' . count($issues) . ' potentiella fel</strong> hittades i ' . count($byEvent) . ' event.';
    echo '</div>';

    foreach ($byEvent as $eventId => $eventData) {
        echo '<div class="card mb-md">';
        echo '<div class="card-header">';
        echo '<h4>' . htmlspecialchars($eventData['event_name']) . ' (' . $eventData['event_date'] . ')</h4>';
        echo '<a href="/admin/edit-results.php?event_id=' . $eventId . '" class="btn btn--primary btn--sm">Editera</a>';
        echo '</div>';
        echo '<div class="card-body gs-p-0">';
        echo '<table class="table table-sm">';
        echo '<thead><tr><th>Åkare</th><th>Födelseår</th><th>Ålder</th><th>Nuvarande klass</th><th>Borde vara</th></tr></thead>';
        echo '<tbody>';

        foreach ($eventData['riders'] as $rider) {
            echo '<tr>';
            echo '<td><a href="/rider/' . $rider['rider_id'] . '">' . htmlspecialchars($rider['rider_name']) . '</a></td>';
            echo '<td>' . $rider['birth_year'] . '</td>';
            echo '<td>' . $rider['age'] . ' år</td>';
            echo '<td><span class="badge badge-danger">' . htmlspecialchars($rider['current_class']) . '</span></td>';
            echo '<td><span class="badge badge-success">' . htmlspecialchars($rider['expected_class']) . '</span></td>';
            echo '</tr>';
        }

        echo '</tbody></table>';
        echo '</div></div>';
    }
}
?>

    </div>
</div>

<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
