<?php
/**
 * Migration 107: Create Test Series for Registration Testing
 *
 * Creates a hidden test series and events for testing the registration module.
 * Only visible to admins.
 */

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 107: Test Series</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 10px; margin-right: 10px; }
    .btn-danger { background: #ef4444; color: white; }
</style>";
echo "</head><body>";
echo "<h1>Migration 107: Test Series for Registration</h1>";

$action = $_GET['action'] ?? 'create';

if ($action === 'delete') {
    // Delete test data
    echo "<div class='box'>";
    echo "<h3>Tar bort testdata...</h3>";

    try {
        // Get test series ID
        $testSeries = $db->getRow("SELECT id FROM series WHERE name = '[TEST] Anmälningstest' LIMIT 1");

        if ($testSeries) {
            // Delete events in test series
            $db->query("DELETE FROM events WHERE series_id = ?", [$testSeries['id']]);
            echo "<p class='success'>Tog bort test-events</p>";

            // Delete series
            $db->query("DELETE FROM series WHERE id = ?", [$testSeries['id']]);
            echo "<p class='success'>Tog bort test-serien</p>";
        } else {
            echo "<p class='info'>Ingen testserie hittades</p>";
        }
    } catch (Exception $e) {
        echo "<p class='error'>Fel: " . htmlspecialchars($e->getMessage()) . "</p>";
    }

    echo "</div>";
    echo "<a href='?action=create' class='btn'>Skapa ny testserie</a>";
    echo "<a href='/admin/series.php' class='btn'>Tillbaka till serier</a>";

} else {
    // Create test data
    echo "<div class='box'>";
    echo "<h3>Skapar testserie...</h3>";

    try {
        // Check if test series already exists
        $existing = $db->getRow("SELECT id FROM series WHERE name = '[TEST] Anmälningstest' LIMIT 1");

        if ($existing) {
            echo "<p class='info'>Testserie finns redan (ID: {$existing['id']})</p>";
            $seriesId = $existing['id'];
        } else {
            // Get default pricing template
            $defaultTemplate = $db->getRow("SELECT id FROM pricing_templates WHERE is_default = 1 LIMIT 1");
            $templateId = $defaultTemplate ? $defaultTemplate['id'] : null;

            // Create test series
            $db->insert('series', [
                'name' => '[TEST] Anmälningstest',
                'year' => date('Y'),
                'discipline' => 'enduro',
                'status' => 'draft', // Draft = not visible to public
                'registration_enabled' => 1,
                'pricing_template_id' => $templateId
            ]);
            $seriesId = $db->lastInsertId();
            echo "<p class='success'>Skapade testserie (ID: $seriesId)</p>";
        }

        // Check for existing test events
        $existingEvents = $db->getAll("SELECT id FROM events WHERE series_id = ?", [$seriesId]);

        if (count($existingEvents) > 0) {
            echo "<p class='info'>" . count($existingEvents) . " test-events finns redan</p>";
        } else {
            // Create test events
            $testEvents = [
                [
                    'name' => '[TEST] Event 1 - Öppen anmälan',
                    'date' => date('Y-m-d', strtotime('+30 days')),
                    'location' => 'Testbanan',
                    'registration_opens' => date('Y-m-d H:i:s', strtotime('-7 days')),
                    'registration_deadline' => date('Y-m-d H:i:s', strtotime('+25 days')),
                ],
                [
                    'name' => '[TEST] Event 2 - Inte öppnat än',
                    'date' => date('Y-m-d', strtotime('+60 days')),
                    'location' => 'Testbanan',
                    'registration_opens' => date('Y-m-d H:i:s', strtotime('+14 days')),
                    'registration_deadline' => date('Y-m-d H:i:s', strtotime('+55 days')),
                ],
                [
                    'name' => '[TEST] Event 3 - Stängd anmälan',
                    'date' => date('Y-m-d', strtotime('+5 days')),
                    'location' => 'Testbanan',
                    'registration_opens' => date('Y-m-d H:i:s', strtotime('-30 days')),
                    'registration_deadline' => date('Y-m-d H:i:s', strtotime('-2 days')),
                ],
            ];

            foreach ($testEvents as $event) {
                $db->insert('events', array_merge($event, [
                    'series_id' => $seriesId,
                    'discipline' => 'enduro',
                    'active' => 0 // Inactive = not visible to public
                ]));
                echo "<p class='success'>Skapade: {$event['name']}</p>";
            }
        }

    } catch (Exception $e) {
        echo "<p class='error'>Fel: " . htmlspecialchars($e->getMessage()) . "</p>";
    }

    echo "</div>";

    echo "<div class='box'>";
    echo "<h3>Testlänkar</h3>";
    echo "<p><a href='/admin/series-pricing.php?id=$seriesId' class='btn'>Anmälan & Priser</a></p>";
    echo "<p><a href='/admin/series.php' class='btn'>Alla serier</a></p>";
    echo "<p><a href='?action=delete' class='btn btn-danger'>Ta bort testdata</a></p>";
    echo "</div>";
}

echo "</body></html>";
