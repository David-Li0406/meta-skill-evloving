<?php
/**
 * Admin Event Edit - V3 Unified Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Check column status for debugging
$columnStatus = 'unknown';
$columnInfo = [];

// Ensure is_championship column exists using SHOW COLUMNS (more reliable)
try {
    $columns = $db->getAll("SHOW COLUMNS FROM events LIKE 'is_championship'");
    if (empty($columns)) {
        $result = $db->query("ALTER TABLE events ADD COLUMN is_championship TINYINT(1) NOT NULL DEFAULT 0");
        $columnStatus = $result ? 'created' : 'create_failed';
        error_log("EVENT EDIT: Added is_championship column to events table");
    } else {
        $columnStatus = 'exists';
        $columnInfo = $columns[0];
    }
} catch (Exception $e) {
    $columnStatus = 'error: ' . $e->getMessage();
    error_log("EVENT EDIT: Error checking/adding is_championship column: " . $e->getMessage());
}

// Check if payment_recipient_id column exists and get recipients
$paymentRecipientColumnExists = false;
$paymentRecipients = [];
try {
    $columns = $db->getAll("SHOW COLUMNS FROM events LIKE 'payment_recipient_id'");
    $paymentRecipientColumnExists = !empty($columns);
    if ($paymentRecipientColumnExists) {
        $tables = $db->getAll("SHOW TABLES LIKE 'payment_recipients'");
        if (!empty($tables)) {
            $paymentRecipients = $db->getAll("SELECT id, name, swish_number, swish_name FROM payment_recipients WHERE active = 1 ORDER BY name ASC");
        }
    }
} catch (Exception $e) {
    error_log("EVENT EDIT: Error checking payment_recipient_id column: " . $e->getMessage());
}

// Check/create header_banner_media_id column
$headerBannerColumnExists = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM events LIKE 'header_banner_media_id'");
    if (empty($columns)) {
        $db->query("ALTER TABLE events ADD COLUMN header_banner_media_id INT NULL");
        error_log("EVENT EDIT: Added header_banner_media_id column to events table");
    }
    $headerBannerColumnExists = true;
} catch (Exception $e) {
    error_log("EVENT EDIT: Error checking/adding header_banner_media_id column: " . $e->getMessage());
}

// Check/create pricing_template_id column
try {
    $columns = $db->getAll("SHOW COLUMNS FROM events LIKE 'pricing_template_id'");
    if (empty($columns)) {
        $db->query("ALTER TABLE events ADD COLUMN pricing_template_id INT NULL");
        error_log("EVENT EDIT: Added pricing_template_id column to events table");
    }
} catch (Exception $e) {
    error_log("EVENT EDIT: Error checking/adding pricing_template_id column: " . $e->getMessage());
}

// Get media files from events folder for banner selection
$eventMediaFiles = [];
try {
    global $pdo;
    $stmt = $pdo->prepare("SELECT id, filename, original_filename, filepath FROM media WHERE folder = 'events' ORDER BY uploaded_at DESC");
    $stmt->execute();
    $eventMediaFiles = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    error_log("EVENT EDIT: Error fetching event media: " . $e->getMessage());
}

// Check/create _hidden columns for event content fields
$hiddenColumns = [
    'invitation_hidden', 'hydration_hidden', 'toilets_hidden', 'bike_wash_hidden',
    'food_hidden', 'shops_hidden', 'exhibitors_hidden', 'parking_hidden',
    'hotel_hidden', 'local_hidden', 'media_hidden', 'contacts_hidden',
    'pm_hidden', 'driver_meeting_hidden', 'training_hidden', 'timing_hidden',
    'lift_hidden', 'rules_hidden', 'insurance_hidden', 'equipment_hidden',
    'medical_hidden', 'scf_hidden', 'jury_hidden', 'schedule_hidden', 'start_times_hidden'
];
try {
    foreach ($hiddenColumns as $col) {
        $columns = $db->getAll("SHOW COLUMNS FROM events LIKE ?", [$col]);
        if (empty($columns)) {
            $db->query("ALTER TABLE events ADD COLUMN {$col} TINYINT(1) NOT NULL DEFAULT 0");
            error_log("EVENT EDIT: Added {$col} column to events table");
        }
    }
} catch (Exception $e) {
    error_log("EVENT EDIT: Error checking/adding hidden columns: " . $e->getMessage());
}

// Get event ID from URL (supports both /admin/events/edit/123 and ?id=123)
$id = 0;
if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
} else {
    // Check for pretty URL format
    $uri = $_SERVER['REQUEST_URI'];
    if (preg_match('#/admin/events/edit/(\d+)#', $uri, $matches)) {
        $id = intval($matches[1]);
    }
}

if ($id <= 0) {
    $_SESSION['message'] = 'Ogiltigt event-ID';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/events');
    exit;
}

// Fetch event data
$event = $db->getRow("SELECT * FROM events WHERE id = ?", [$id]);

if (!$event) {
    $_SESSION['message'] = 'Event hittades inte';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/events');
    exit;
}

// Check if user is promotor (can only edit certain sections)
$isPromotorOnly = function_exists('isRole') && isRole('promotor');

// If promotor, verify they have access to this event
if ($isPromotorOnly) {
    $canAccess = function_exists('canAccessEvent') && canAccessEvent($id);
    if (!$canAccess) {
        $_SESSION['message'] = 'Du har inte behörighet att redigera detta event';
        $_SESSION['messageType'] = 'error';
        header('Location: /admin/events');
        exit;
    }
}

// Function to save sponsor assignments for events
function saveEventSponsorAssignments($db, $eventId, $postData) {
    $pdo = $db->getPdo();

    error_log("saveEventSponsorAssignments called for event $eventId");
    error_log("POST data: sponsor_header=" . ($postData['sponsor_header'] ?? 'empty') . ", sponsor_content=" . json_encode($postData['sponsor_content'] ?? []) . ", sponsor_sidebar=" . ($postData['sponsor_sidebar'] ?? 'empty'));

    // CRITICAL FIX: Ensure placement ENUM includes all values
    try {
        $pdo->exec("ALTER TABLE event_sponsors MODIFY COLUMN placement ENUM('header', 'sidebar', 'footer', 'content', 'partner') DEFAULT 'sidebar'");
        $pdo->exec("ALTER TABLE series_sponsors MODIFY COLUMN placement ENUM('header', 'sidebar', 'footer', 'content', 'partner') DEFAULT 'sidebar'");
    } catch (Exception $e) {
        // May already be correct
    }

    // First, delete existing sponsor assignments for this event
    $deleteStmt = $pdo->prepare("DELETE FROM event_sponsors WHERE event_id = ?");
    $deleteStmt->execute([$eventId]);
    error_log("Deleted existing sponsor assignments for event $eventId");

    // Insert new assignments
    $insertStmt = $pdo->prepare("INSERT INTO event_sponsors (event_id, sponsor_id, placement, display_order) VALUES (?, ?, ?, ?)");

    $insertedCount = 0;

    // Header sponsors (banner at top - single select)
    if (!empty($postData['sponsor_header'])) {
        $insertStmt->execute([$eventId, (int)$postData['sponsor_header'], 'header', 0]);
        $insertedCount++;
        error_log("Inserted header sponsor: " . $postData['sponsor_header']);
    }

    // Content sponsors (logo row - multiple checkboxes)
    if (!empty($postData['sponsor_content']) && is_array($postData['sponsor_content'])) {
        $order = 0;
        foreach ($postData['sponsor_content'] as $sponsorId) {
            $insertStmt->execute([$eventId, (int)$sponsorId, 'content', $order++]);
            $insertedCount++;
            error_log("Inserted content sponsor: $sponsorId");
        }
    }

    // Sidebar/Results sponsor (single select)
    if (!empty($postData['sponsor_sidebar'])) {
        $insertStmt->execute([$eventId, (int)$postData['sponsor_sidebar'], 'sidebar', 0]);
        $insertedCount++;
    }

    // Partner sponsors (bottom logo row - unlimited)
    if (!empty($postData['sponsor_partner']) && is_array($postData['sponsor_partner'])) {
        $order = 0;
        foreach ($postData['sponsor_partner'] as $sponsorId) {
            $insertStmt->execute([$eventId, (int)$sponsorId, 'partner', $order++]);
            $insertedCount++;
        }
    }

    // VERIFY: Check what was actually saved
    $verifyStmt = $pdo->prepare("SELECT sponsor_id, placement FROM event_sponsors WHERE event_id = ?");
    $verifyStmt->execute([$eventId]);
    $savedSponsors = $verifyStmt->fetchAll(PDO::FETCH_ASSOC);
    error_log("VERIFY: Actually saved sponsors: " . json_encode($savedSponsors));
}

// Initialize message variables
$message = '';
$messageType = 'info';

// Check if we just saved
if (isset($_GET['saved']) && $_GET['saved'] == '1' && isset($_SESSION['message'])) {
    $message = $_SESSION['message'];
    $messageType = $_SESSION['messageType'] ?? 'success';
    unset($_SESSION['message'], $_SESSION['messageType']);
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $name = trim($_POST['name'] ?? '');
    $date = trim($_POST['date'] ?? '');

    if (empty($name) || empty($date)) {
        $message = 'Namn och datum är obligatoriska';
        $messageType = 'error';
    } else {
        $eventData = [
            'name' => $name,
            'advent_id' => trim($_POST['advent_id'] ?? '') ?: null,
            'date' => $date,
            'location' => trim($_POST['location'] ?? ''),
            'venue_id' => !empty($_POST['venue_id']) ? intval($_POST['venue_id']) : null,
            'discipline' => trim($_POST['discipline'] ?? ''),
            'event_level' => in_array($_POST['event_level'] ?? '', ['national', 'sportmotion']) ? $_POST['event_level'] : 'national',
            'event_format' => trim($_POST['event_format'] ?? 'ENDURO'),
            'stage_names' => !empty($_POST['stage_names']) ? trim($_POST['stage_names']) : null,
            'series_id' => !empty($_POST['series_id']) ? intval($_POST['series_id']) : null,
            'point_scale_id' => !empty($_POST['point_scale_id']) ? intval($_POST['point_scale_id']) : null,
            'pricing_template_id' => !empty($_POST['pricing_template_id']) ? intval($_POST['pricing_template_id']) : null,
            'distance' => !empty($_POST['distance']) ? floatval($_POST['distance']) : null,
            'elevation_gain' => !empty($_POST['elevation_gain']) ? intval($_POST['elevation_gain']) : null,
            'organizer_club_id' => !empty($_POST['organizer_club_id']) ? intval($_POST['organizer_club_id']) : null,
            'organizer' => '', // Keep for backwards compatibility
            'website' => trim($_POST['website'] ?? ''),
            'registration_deadline' => !empty($_POST['registration_deadline']) ? trim($_POST['registration_deadline']) : null,
            'registration_deadline_time' => !empty($_POST['registration_deadline_time']) ? trim($_POST['registration_deadline_time']) : null,
            'active' => isset($_POST['active']) ? 1 : 0,
            'is_championship' => isset($_POST['is_championship']) ? 1 : 0,
            'contact_email' => trim($_POST['contact_email'] ?? ''),
            'contact_phone' => trim($_POST['contact_phone'] ?? ''),
            // Extended fields
            'venue_details' => trim($_POST['venue_details'] ?? ''),
            'venue_coordinates' => trim($_POST['venue_coordinates'] ?? ''),
            'venue_map_url' => trim($_POST['venue_map_url'] ?? ''),
            'pm_content' => trim($_POST['pm_content'] ?? ''),
            'pm_use_global' => isset($_POST['pm_use_global']) ? 1 : 0,
            'pm_publish_at' => !empty($_POST['pm_publish_at']) ? trim($_POST['pm_publish_at']) : null,
            'jury_communication' => trim($_POST['jury_communication'] ?? ''),
            'jury_use_global' => isset($_POST['jury_use_global']) ? 1 : 0,
            'competition_schedule' => trim($_POST['competition_schedule'] ?? ''),
            'schedule_use_global' => isset($_POST['schedule_use_global']) ? 1 : 0,
            'start_times' => trim($_POST['start_times'] ?? ''),
            'start_times_use_global' => isset($_POST['start_times_use_global']) ? 1 : 0,
            'starttider_publish_at' => !empty($_POST['starttider_publish_at']) ? trim($_POST['starttider_publish_at']) : null,
            // Note: karta_publish_at is managed in the map editor (event-map.php)
            'driver_meeting' => trim($_POST['driver_meeting'] ?? ''),
            'driver_meeting_use_global' => isset($_POST['driver_meeting_use_global']) ? 1 : 0,
            'competition_rules' => trim($_POST['competition_rules'] ?? ''),
            'rules_use_global' => isset($_POST['rules_use_global']) ? 1 : 0,
            'insurance_info' => trim($_POST['insurance_info'] ?? ''),
            'insurance_use_global' => isset($_POST['insurance_use_global']) ? 1 : 0,
            'equipment_info' => trim($_POST['equipment_info'] ?? ''),
            'equipment_use_global' => isset($_POST['equipment_use_global']) ? 1 : 0,
            'training_info' => trim($_POST['training_info'] ?? ''),
            'training_use_global' => isset($_POST['training_use_global']) ? 1 : 0,
            'timing_info' => trim($_POST['timing_info'] ?? ''),
            'timing_use_global' => isset($_POST['timing_use_global']) ? 1 : 0,
            'lift_info' => trim($_POST['lift_info'] ?? ''),
            'lift_use_global' => isset($_POST['lift_use_global']) ? 1 : 0,
            'invitation' => trim($_POST['invitation'] ?? ''),
            'invitation_use_global' => isset($_POST['invitation_use_global']) ? 1 : 0,
            'hydration_stations' => trim($_POST['hydration_stations'] ?? ''),
            'hydration_use_global' => isset($_POST['hydration_use_global']) ? 1 : 0,
            'toilets_showers' => trim($_POST['toilets_showers'] ?? ''),
            'toilets_use_global' => isset($_POST['toilets_use_global']) ? 1 : 0,
            'shops_info' => trim($_POST['shops_info'] ?? ''),
            'shops_use_global' => isset($_POST['shops_use_global']) ? 1 : 0,
            'bike_wash' => trim($_POST['bike_wash'] ?? ''),
            'bike_wash_use_global' => isset($_POST['bike_wash_use_global']) ? 1 : 0,
            'food_cafe' => trim($_POST['food_cafe'] ?? ''),
            'food_use_global' => isset($_POST['food_use_global']) ? 1 : 0,
            'exhibitors' => trim($_POST['exhibitors'] ?? ''),
            'exhibitors_use_global' => isset($_POST['exhibitors_use_global']) ? 1 : 0,
            'parking_detailed' => trim($_POST['parking_detailed'] ?? ''),
            'parking_use_global' => isset($_POST['parking_use_global']) ? 1 : 0,
            'hotel_accommodation' => trim($_POST['hotel_accommodation'] ?? ''),
            'hotel_use_global' => isset($_POST['hotel_use_global']) ? 1 : 0,
            'local_info' => trim($_POST['local_info'] ?? ''),
            'local_use_global' => isset($_POST['local_use_global']) ? 1 : 0,
            'media_production' => trim($_POST['media_production'] ?? ''),
            'media_use_global' => isset($_POST['media_use_global']) ? 1 : 0,
            'medical_info' => trim($_POST['medical_info'] ?? ''),
            'medical_use_global' => isset($_POST['medical_use_global']) ? 1 : 0,
            'contacts_info' => trim($_POST['contacts_info'] ?? ''),
            'contacts_use_global' => isset($_POST['contacts_use_global']) ? 1 : 0,
            'scf_representatives' => trim($_POST['scf_representatives'] ?? ''),
            'scf_use_global' => isset($_POST['scf_use_global']) ? 1 : 0,
            // Hidden flags for each content section
            'invitation_hidden' => isset($_POST['invitation_hidden']) ? 1 : 0,
            'hydration_hidden' => isset($_POST['hydration_hidden']) ? 1 : 0,
            'toilets_hidden' => isset($_POST['toilets_hidden']) ? 1 : 0,
            'bike_wash_hidden' => isset($_POST['bike_wash_hidden']) ? 1 : 0,
            'food_hidden' => isset($_POST['food_hidden']) ? 1 : 0,
            'shops_hidden' => isset($_POST['shops_hidden']) ? 1 : 0,
            'exhibitors_hidden' => isset($_POST['exhibitors_hidden']) ? 1 : 0,
            'parking_hidden' => isset($_POST['parking_hidden']) ? 1 : 0,
            'hotel_hidden' => isset($_POST['hotel_hidden']) ? 1 : 0,
            'local_hidden' => isset($_POST['local_hidden']) ? 1 : 0,
            'media_hidden' => isset($_POST['media_hidden']) ? 1 : 0,
            'contacts_hidden' => isset($_POST['contacts_hidden']) ? 1 : 0,
            'pm_hidden' => isset($_POST['pm_hidden']) ? 1 : 0,
            'driver_meeting_hidden' => isset($_POST['driver_meeting_hidden']) ? 1 : 0,
            'training_hidden' => isset($_POST['training_hidden']) ? 1 : 0,
            'timing_hidden' => isset($_POST['timing_hidden']) ? 1 : 0,
            'lift_hidden' => isset($_POST['lift_hidden']) ? 1 : 0,
            'rules_hidden' => isset($_POST['rules_hidden']) ? 1 : 0,
            'insurance_hidden' => isset($_POST['insurance_hidden']) ? 1 : 0,
            'equipment_hidden' => isset($_POST['equipment_hidden']) ? 1 : 0,
            'medical_hidden' => isset($_POST['medical_hidden']) ? 1 : 0,
            'scf_hidden' => isset($_POST['scf_hidden']) ? 1 : 0,
            'jury_hidden' => isset($_POST['jury_hidden']) ? 1 : 0,
            'schedule_hidden' => isset($_POST['schedule_hidden']) ? 1 : 0,
            'start_times_hidden' => isset($_POST['start_times_hidden']) ? 1 : 0,
        ];

        try {
            error_log("EVENT EDIT: Saving event ID {$id}, name: {$name}");

            // Store is_championship separately
            $isChampionship = $eventData['is_championship'];
            unset($eventData['is_championship']);

            // First, update the core fields (original 10 that always work)
            $basicResult = $db->query(
                "UPDATE events SET name = ?, date = ?, location = ?, venue_id = ?,
                 discipline = ?, event_level = ?, event_format = ?, series_id = ?,
                 active = ?, website = ? WHERE id = ?",
                [
                    $eventData['name'], $eventData['date'], $eventData['location'],
                    $eventData['venue_id'], $eventData['discipline'], $eventData['event_level'],
                    $eventData['event_format'], $eventData['series_id'], $eventData['active'],
                    $eventData['website'], $id
                ]
            );

            if (!$basicResult) {
                throw new Exception("Kunde inte uppdatera grunddata - kontrollera databasen");
            }

            // Try to update organizer_club_id separately (may not exist in older installs)
            try {
                $db->query("UPDATE events SET organizer_club_id = ? WHERE id = ?",
                    [$eventData['organizer_club_id'], $id]);
            } catch (Exception $clubEx) {
                error_log("EVENT EDIT: organizer_club_id update failed: " . $clubEx->getMessage());
            }

            // Now try to update extended fields (these might not exist in all installs)
            try {
                unset($eventData['name'], $eventData['date'], $eventData['location'],
                      $eventData['venue_id'], $eventData['discipline'], $eventData['event_level'],
                      $eventData['event_format'], $eventData['series_id'], $eventData['active'],
                      $eventData['website'], $eventData['organizer_club_id']);

                if (!empty($eventData)) {
                    $db->update('events', $eventData, 'id = ?', [$id]);
                }
            } catch (Exception $extEx) {
                error_log("EVENT EDIT: Extended fields update failed (non-critical): " . $extEx->getMessage());
            }

            // Update is_championship separately
            try {
                $db->query("UPDATE events SET is_championship = ? WHERE id = ?", [$isChampionship, $id]);
            } catch (Exception $smEx) {
                error_log("EVENT EDIT: SM column update failed: " . $smEx->getMessage());
            }

            // Update header_banner_media_id separately
            if ($headerBannerColumnExists) {
                try {
                    $headerBannerMediaId = !empty($_POST['header_banner_media_id']) ? intval($_POST['header_banner_media_id']) : null;
                    $db->query("UPDATE events SET header_banner_media_id = ? WHERE id = ?", [$headerBannerMediaId, $id]);
                } catch (Exception $hbEx) {
                    error_log("EVENT EDIT: header_banner_media_id update failed: " . $hbEx->getMessage());
                }
            }

            // Update payment_recipient_id separately (if column exists)
            if ($paymentRecipientColumnExists) {
                try {
                    $paymentRecipientId = !empty($_POST['payment_recipient_id']) ? intval($_POST['payment_recipient_id']) : null;
                    $db->query("UPDATE events SET payment_recipient_id = ? WHERE id = ?", [$paymentRecipientId, $id]);
                } catch (Exception $prEx) {
                    error_log("EVENT EDIT: payment_recipient_id update failed: " . $prEx->getMessage());
                }
            }

            // Update gravity_id_discount (0 = use series setting, >0 = specific discount)
            try {
                $gravityIdDiscount = floatval($_POST['gravity_id_discount'] ?? 0);
                $db->query("UPDATE events SET gravity_id_discount = ? WHERE id = ?", [$gravityIdDiscount, $id]);
            } catch (Exception $gidEx) {
                error_log("EVENT EDIT: gravity_id_discount update failed: " . $gidEx->getMessage());
            }

            // Sync series_events junction table with events.series_id
            try {
                $newSeriesId = !empty($_POST['series_id']) ? intval($_POST['series_id']) : null;

                // Remove from any previous series_events entries that don't match
                $db->query(
                    "DELETE FROM series_events WHERE event_id = ? AND series_id != ?",
                    [$id, $newSeriesId ?? 0]
                );

                // Add to series_events if series_id is set and not already there
                if ($newSeriesId) {
                    $existingLink = $db->getRow(
                        "SELECT id FROM series_events WHERE series_id = ? AND event_id = ?",
                        [$newSeriesId, $id]
                    );

                    if (!$existingLink) {
                        // Get max sort order for this series
                        $maxOrder = $db->getRow(
                            "SELECT MAX(sort_order) as max_order FROM series_events WHERE series_id = ?",
                            [$newSeriesId]
                        );
                        $sortOrder = ($maxOrder['max_order'] ?? 0) + 1;

                        $db->insert('series_events', [
                            'series_id' => $newSeriesId,
                            'event_id' => $id,
                            'sort_order' => $sortOrder
                        ]);
                    }
                }
            } catch (Exception $syncEx) {
                error_log("EVENT EDIT: series_events sync failed (non-critical): " . $syncEx->getMessage());
            }

            // Verify basic fields were saved
            $verifyEvent = $db->getRow("SELECT name FROM events WHERE id = ?", [$id]);
            $savedName = $verifyEvent['name'] ?? '';

            if ($savedName !== $name) {
                $message = "VARNING: Namnet sparades inte! Försökte: '{$name}', DB har: '{$savedName}'";
                $messageType = 'error';
                error_log("EVENT EDIT ERROR: Name mismatch");
            } else {
                // Save sponsor assignments
                $sponsorError = null;
                try {
                    saveEventSponsorAssignments($db, $id, $_POST);
                    error_log("EVENT EDIT: Sponsor assignments saved successfully for event $id");
                    error_log("EVENT EDIT: sponsor_header=" . ($_POST['sponsor_header'] ?? 'none'));
                    error_log("EVENT EDIT: sponsor_content=" . json_encode($_POST['sponsor_content'] ?? []));
                    error_log("EVENT EDIT: sponsor_sidebar=" . ($_POST['sponsor_sidebar'] ?? 'none'));
                } catch (Exception $sponsorEx) {
                    error_log("EVENT EDIT: Sponsor assignments save failed: " . $sponsorEx->getMessage());
                    $sponsorError = $sponsorEx->getMessage();
                }

                if ($sponsorError) {
                    $_SESSION['message'] = 'Event sparat, men fel vid sponsorsparning: ' . $sponsorError;
                    $_SESSION['messageType'] = 'warning';
                } else {
                    $_SESSION['message'] = 'Event uppdaterat!';
                    $_SESSION['messageType'] = 'success';
                }
                header('Location: /admin/events/edit/' . $id . '?saved=1');
                exit;
            }
        } catch (Exception $e) {
            error_log("EVENT EDIT ERROR: " . $e->getMessage());
            $message = 'Ett fel uppstod: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Fetch data for dropdowns
// Get series with brand and year info for better grouping
// Include completed series so events can be added back if needed
$series = $db->getAll("
    SELECT s.id, s.name, s.year, s.brand_id, s.status, sb.name as brand_name
    FROM series s
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE s.status IN ('active', 'planning', 'completed')
    ORDER BY sb.name ASC, s.year DESC, s.name ASC
");

// Group series by brand for display
$seriesByBrand = [];
foreach ($series as $s) {
    $brandName = $s['brand_name'] ?? 'Utan varumärke';
    if (!isset($seriesByBrand[$brandName])) {
        $seriesByBrand[$brandName] = [];
    }
    $seriesByBrand[$brandName][] = $s;
}

// Get event year from date for auto-suggestion
$eventYear = !empty($event['date']) ? date('Y', strtotime($event['date'])) : date('Y');
$venues = $db->getAll("SELECT id, name, city FROM venues WHERE active = 1 ORDER BY name");
$clubs = $db->getAll("SELECT id, name, city FROM clubs WHERE active = 1 ORDER BY name");
$pricingTemplates = $db->getAll("SELECT id, name, is_default FROM pricing_templates ORDER BY is_default DESC, name ASC");
$pointScales = $db->getAll("SELECT id, name, discipline FROM point_scales WHERE active = 1 ORDER BY name ASC");

// Fetch global texts
$globalTexts = $db->getAll("SELECT field_key, content FROM global_texts WHERE is_active = 1");
$globalTextMap = [];
foreach ($globalTexts as $gt) {
    $globalTextMap[$gt['field_key']] = $gt['content'];
}

// Get configured classes for this event (from event_pricing_rules)
$eventClasses = [];
try {
    $eventClasses = $db->getAll("
        SELECT c.id, c.name, c.display_name, c.gender, epr.base_price
        FROM event_pricing_rules epr
        JOIN classes c ON epr.class_id = c.id
        WHERE epr.event_id = ?
        ORDER BY c.sort_order ASC, c.name ASC
    ", [$id]);
} catch (Exception $e) {
    error_log("EVENT EDIT: Could not load event classes: " . $e->getMessage());
}

// Get pricing template and its prices if a template is assigned
$assignedTemplate = null;
$templatePrices = [];
if (!empty($event['pricing_template_id'])) {
    try {
        $assignedTemplate = $db->getRow("SELECT * FROM pricing_templates WHERE id = ?", [$event['pricing_template_id']]);
        if ($assignedTemplate) {
            $templatePrices = $db->getAll("
                SELECT ptr.*, c.id as class_id, c.name as class_name, c.display_name, c.gender
                FROM pricing_template_rules ptr
                JOIN classes c ON c.id = ptr.class_id
                WHERE ptr.template_id = ?
                ORDER BY c.sort_order ASC, c.name ASC
            ", [$event['pricing_template_id']]);
        }
    } catch (Exception $e) {
        error_log("EVENT EDIT: Could not load pricing template: " . $e->getMessage());
    }
}

// Get all sponsors for selection
$allSponsors = [];
$eventSponsors = ['header' => [], 'content' => [], 'sidebar' => [], 'partner' => []];
try {
    $allSponsors = $db->getAll("SELECT id, name, logo, tier FROM sponsors WHERE active = 1 ORDER BY tier ASC, name ASC");

    $sponsorAssignments = $db->getAll("
        SELECT sponsor_id, placement
        FROM event_sponsors
        WHERE event_id = ?
    ", [$id]);
    foreach ($sponsorAssignments as $sa) {
        $placement = $sa['placement'] ?? 'sidebar';
        if (!isset($eventSponsors[$placement])) {
            $eventSponsors[$placement] = [];
        }
        $eventSponsors[$placement][] = (int)$sa['sponsor_id'];
    }
} catch (Exception $e) {
    error_log("EVENT EDIT: Could not load sponsors: " . $e->getMessage());
}

// Page config
$page_title = 'Redigera Event';
$breadcrumbs = [
    ['label' => 'Events', 'url' => '/admin/events'],
    ['label' => htmlspecialchars($event['name'])]
];
$page_actions = '<a href="/event/' . $id . '" target="_blank" class="btn-admin btn-admin-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-sm"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>
    Visa event
</a>
<a href="/admin/event-pricing.php?id=' . $id . '" class="btn-admin btn-admin-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-sm"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
    Klasser &amp; Priser
</a>
<a href="/admin/event-map.php?id=' . $id . '" class="btn-admin btn-admin-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-sm"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/></svg>
    Karta &amp; POI
</a>
<a href="/admin/event-import-paste.php?event_id=' . $id . '" class="btn-admin btn-admin-primary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-sm"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M9 14l2 2 4-4"/></svg>
    Importera resultat
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?> mb-lg">
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<form method="POST" id="eventEditForm">
    <?= csrf_field() ?>

    <!-- BASIC INFO - Locked for promotors -->
    <?php if ($isPromotorOnly): ?>
    <!-- Hidden fields to preserve locked values for promotors -->
    <input type="hidden" name="name" value="<?= h($event['name']) ?>">
    <input type="hidden" name="date" value="<?= h($event['date']) ?>">
    <input type="hidden" name="advent_id" value="<?= h($event['advent_id'] ?? '') ?>">
    <input type="hidden" name="location" value="<?= h($event['location'] ?? '') ?>">
    <input type="hidden" name="venue_id" value="<?= h($event['venue_id'] ?? '') ?>">
    <?php endif; ?>
    <details class="admin-card mb-lg <?= $isPromotorOnly ? 'locked-section' : '' ?>">
        <summary class="admin-card-header collapsible-header">
            <h2>Grundläggande information</h2>
            <?php if ($isPromotorOnly): ?>
            <span class="locked-badge">
                <i data-lucide="lock"></i> Låst
            </span>
            <?php else: ?>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
            <?php endif; ?>
        </summary>
        <fieldset class="admin-card-body fieldset-reset" style="padding: var(--space-lg);" <?= $isPromotorOnly ? 'disabled' : '' ?>>
            <div class="form-grid form-grid-2">
                <div class="admin-form-group form-full-width">
                    <label class="admin-form-label">Namn <span class="required">*</span></label>
                    <input type="text" class="admin-form-input" <?= $isPromotorOnly ? '' : 'name="name" required' ?> value="<?= h($event['name']) ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Datum <span class="required">*</span></label>
                    <input type="date" class="admin-form-input" <?= $isPromotorOnly ? '' : 'name="date" required' ?> value="<?= h($event['date']) ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Advent ID</label>
                    <input type="text" name="advent_id" class="admin-form-input" value="<?= h($event['advent_id'] ?? '') ?>" placeholder="Externt ID för import">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Plats</label>
                    <input type="text" name="location" class="admin-form-input" value="<?= h($event['location'] ?? '') ?>" placeholder="T.ex. Järvsö">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Bana/Anläggning</label>
                    <select name="venue_id" class="admin-form-select">
                        <option value="">Ingen specifik bana</option>
                        <?php foreach ($venues as $venue): ?>
                            <option value="<?= $venue['id'] ?>" <?= ($event['venue_id'] == $venue['id']) ? 'selected' : '' ?>>
                                <?= h($venue['name']) ?><?php if ($venue['city']): ?> (<?= h($venue['city']) ?>)<?php endif; ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>
        </fieldset>
    </details>

    <!-- COMPETITION SETTINGS - Locked for promotors -->
    <?php if ($isPromotorOnly): ?>
    <!-- Hidden fields to preserve locked values for promotors -->
    <input type="hidden" name="discipline" value="<?= h($event['discipline'] ?? '') ?>">
    <input type="hidden" name="series_id" value="<?= h($event['series_id'] ?? '') ?>">
    <input type="hidden" name="event_level" value="<?= h($event['event_level'] ?? 'national') ?>">
    <input type="hidden" name="event_format" value="<?= h($event['event_format'] ?? 'ENDURO') ?>">
    <input type="hidden" name="point_scale_id" value="<?= h($event['point_scale_id'] ?? '') ?>">
    <input type="hidden" name="pricing_template_id" value="<?= h($event['pricing_template_id'] ?? '') ?>">
    <input type="hidden" name="distance" value="<?= h($event['distance'] ?? '') ?>">
    <input type="hidden" name="elevation_gain" value="<?= h($event['elevation_gain'] ?? '') ?>">
    <input type="hidden" name="stage_names" value="<?= h($event['stage_names'] ?? '') ?>">
    <?php endif; ?>
    <details class="admin-card mb-lg <?= $isPromotorOnly ? 'locked-section' : '' ?>">
        <summary class="admin-card-header collapsible-header">
            <h2>Tävlingsinställningar</h2>
            <?php if ($isPromotorOnly): ?>
            <span class="locked-badge">
                <i data-lucide="lock"></i> Låst
            </span>
            <?php else: ?>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
            <?php endif; ?>
        </summary>
        <fieldset class="admin-card-body fieldset-reset" style="padding: var(--space-lg);" <?= $isPromotorOnly ? 'disabled' : '' ?>>
            <div class="form-grid form-grid-2">
                <div class="admin-form-group">
                    <label class="admin-form-label">Tävlingsformat</label>
                    <select name="discipline" class="admin-form-select">
                        <option value="">Välj format...</option>
                        <option value="ENDURO" <?= ($event['discipline'] ?? '') === 'ENDURO' ? 'selected' : '' ?>>Enduro</option>
                        <option value="DH" <?= ($event['discipline'] ?? '') === 'DH' ? 'selected' : '' ?>>Downhill</option>
                        <option value="XC" <?= ($event['discipline'] ?? '') === 'XC' ? 'selected' : '' ?>>XC</option>
                        <option value="XCO" <?= ($event['discipline'] ?? '') === 'XCO' ? 'selected' : '' ?>>XCO</option>
                        <option value="DUAL_SLALOM" <?= ($event['discipline'] ?? '') === 'DUAL_SLALOM' ? 'selected' : '' ?>>Dual Slalom</option>
                        <option value="PUMPTRACK" <?= ($event['discipline'] ?? '') === 'PUMPTRACK' ? 'selected' : '' ?>>Pumptrack</option>
                        <option value="GRAVEL" <?= ($event['discipline'] ?? '') === 'GRAVEL' ? 'selected' : '' ?>>Gravel</option>
                        <option value="E-MTB" <?= ($event['discipline'] ?? '') === 'E-MTB' ? 'selected' : '' ?>>E-MTB</option>
                    </select>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">
                        Serie (direktkoppling)
                        <span class="text-xs text-secondary font-normal">
                            - eventet läggs också till via
                            <a href="/admin/series" class="text-accent">seriehantering</a>
                        </span>
                    </label>
                    <select name="series_id" id="series_id" class="admin-form-select">
                        <option value="">Ingen serie</option>
                        <?php foreach ($seriesByBrand as $brandName => $brandSeries): ?>
                            <optgroup label="<?= h($brandName) ?>">
                                <?php foreach ($brandSeries as $s):
                                    $yearMatch = ($s['year'] == $eventYear);
                                    $isCompleted = ($s['status'] ?? '') === 'completed';
                                    $matchIndicator = $yearMatch ? ' ✓' : '';
                                    $completedIndicator = $isCompleted ? ' [Avslutad]' : '';
                                ?>
                                    <option value="<?= $s['id'] ?>"
                                            data-year="<?= $s['year'] ?>"
                                            <?= ($event['series_id'] == $s['id']) ? 'selected' : '' ?>
                                            <?= $yearMatch ? 'style="font-weight: bold;"' : '' ?>>
                                        <?= h($s['name']) ?><?= $matchIndicator ?><?= $completedIndicator ?>
                                    </option>
                                <?php endforeach; ?>
                            </optgroup>
                        <?php endforeach; ?>
                    </select>
                    <small class="form-help">
                        Välj serie som matchar eventets år (<?= $eventYear ?>).
                        = matchar år. [Avslutad] = serien är markerad som avslutad.
                    </small>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Rankingklass</label>
                    <select name="event_level" class="admin-form-select">
                        <option value="national" <?= ($event['event_level'] ?? 'national') === 'national' ? 'selected' : '' ?>>Nationell (100%)</option>
                        <option value="sportmotion" <?= ($event['event_level'] ?? 'national') === 'sportmotion' ? 'selected' : '' ?>>Sportmotion (50%)</option>
                    </select>
                    <small class="form-help">Styr rankingpoäng</small>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Event-format</label>
                    <select name="event_format" class="admin-form-select">
                        <option value="ENDURO" <?= ($event['event_format'] ?? 'ENDURO') === 'ENDURO' ? 'selected' : '' ?>>Enduro (en tid, splittider)</option>
                        <option value="DH_STANDARD" <?= ($event['event_format'] ?? '') === 'DH_STANDARD' ? 'selected' : '' ?>>Downhill Standard (två åk, snabbaste räknas)</option>
                        <option value="DH_SWECUP" <?= ($event['event_format'] ?? '') === 'DH_SWECUP' ? 'selected' : '' ?>>SweCUP Downhill (Kval + Final, ranking efter Final)</option>
                        <option value="DUAL_SLALOM" <?= ($event['event_format'] ?? '') === 'DUAL_SLALOM' ? 'selected' : '' ?>>Dual Slalom</option>
                    </select>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Poängskala (ranking)</label>
                    <select name="point_scale_id" class="admin-form-select">
                        <option value="">Ingen poängskala</option>
                        <?php foreach ($pointScales as $scale): ?>
                            <option value="<?= $scale['id'] ?>" <?= ($event['point_scale_id'] ?? '') == $scale['id'] ? 'selected' : '' ?>>
                                <?= h($scale['name']) ?><?php if ($scale['discipline']): ?> (<?= h($scale['discipline']) ?>)<?php endif; ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="form-help">Används för att beräkna rankingpoäng</small>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Prismall</label>
                    <select name="pricing_template_id" class="admin-form-select">
                        <option value="">Ingen prismall</option>
                        <?php foreach ($pricingTemplates as $template): ?>
                            <option value="<?= $template['id'] ?>" <?= ($event['pricing_template_id'] ?? '') == $template['id'] ? 'selected' : '' ?>>
                                <?= h($template['name']) ?><?php if ($template['is_default']): ?> (Standard)<?php endif; ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="form-help">Välj prismall för detta event.<?php if (isRole('super_admin')): ?> <a href="/admin/pricing-templates.php">Hantera prismallar</a><?php elseif (!empty($event['pricing_template_id'])): ?> <a href="/admin/pricing-template-edit.php?id=<?= $event['pricing_template_id'] ?>&event=<?= $id ?>">Redigera prismall</a><?php endif; ?></small>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Distans (km)</label>
                    <input type="number" name="distance" class="admin-form-input" step="0.01" min="0" value="<?= h($event['distance'] ?? '') ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Höjdmeter (m)</label>
                    <input type="number" name="elevation_gain" class="admin-form-input" min="0" value="<?= h($event['elevation_gain'] ?? '') ?>">
                </div>
            </div>

            <div class="admin-form-group mt-md">
                <label class="admin-form-label">Sträcknamn (JSON)</label>
                <input type="text" name="stage_names" class="admin-form-input" value="<?= h($event['stage_names'] ?? '') ?>" placeholder='{"1":"SS1","2":"SS2","3":"SS3"}'>
                <small class="form-help">Anpassade namn. Lämna tomt för standard.</small>
            </div>
        </fieldset>
    </details>

    <!-- EVENT CLASSES & PRICING - Hidden for promotors -->
    <?php if (!$isPromotorOnly): ?>
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>Klasser och Startavgifter</h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <?php if ($assignedTemplate && !empty($templatePrices)):
                // Get pricing settings
                $ebPercent = $assignedTemplate['early_bird_percent'] ?? 15;
                $latePercent = $assignedTemplate['late_fee_percent'] ?? 25;
                $ebDays = $assignedTemplate['early_bird_days_before'] ?? 21;
                $lateDays = $assignedTemplate['late_fee_days_before'] ?? 3;
            ?>
                <!-- Template header -->
                <div class="flex items-center justify-between mb-md">
                    <div class="flex items-center gap-sm">
                        <span class="text-secondary">Prismall:</span>
                        <span class="admin-badge admin-badge-success"><?= htmlspecialchars($assignedTemplate['name']) ?></span>
                    </div>
                    <a href="/admin/pricing-templates.php?edit=<?= $event['pricing_template_id'] ?>" class="text-accent text-sm">Redigera mall</a>
                </div>

                <!-- Compact price table -->
                <div class="admin-table-container">
                    <table class="admin-table" style="font-size: 0.875rem;">
                        <thead>
                            <tr>
                                <th>Klass</th>
                                <th style="text-align: right; color: var(--color-success);">Early Bird (-<?= $ebPercent ?>%)</th>
                                <th style="text-align: right;">Ordinarie</th>
                                <th style="text-align: right; color: var(--color-warning);">Efteranmälan (+<?= $latePercent ?>%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($templatePrices as $price):
                                $basePrice = $price['base_price'];
                                $ebPrice = round($basePrice * (1 - $ebPercent / 100));
                                $latePrice = round($basePrice * (1 + $latePercent / 100));
                            ?>
                            <tr>
                                <td>
                                    <?= htmlspecialchars($price['display_name'] ?? $price['class_name']) ?>
                                    <?php if ($price['gender'] === 'M'): ?>
                                        <span class="text-xs text-secondary">(H)</span>
                                    <?php elseif ($price['gender'] === 'K' || $price['gender'] === 'F'): ?>
                                        <span class="text-xs text-secondary">(D)</span>
                                    <?php endif; ?>
                                </td>
                                <td style="text-align: right; color: var(--color-success); font-weight: 600;"><?= number_format($ebPrice, 0) ?> kr</td>
                                <td style="text-align: right; font-weight: 600;"><?= number_format($basePrice, 0) ?> kr</td>
                                <td style="text-align: right; color: var(--color-warning); font-weight: 600;"><?= number_format($latePrice, 0) ?> kr</td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>

                <!-- Pricing rules info -->
                <div class="mt-md p-sm" style="background: var(--color-bg-hover); border-radius: var(--radius-sm); font-size: 0.8rem;">
                    <div class="flex gap-lg flex-wrap">
                        <span><strong style="color: var(--color-success);">Early Bird:</strong> När anmälan öppnar t.o.m. <?= $ebDays ?> dagar före</span>
                        <span><strong>Ordinarie:</strong> <?= $ebDays ?>-<?= $lateDays ?> dagar före</span>
                        <span><strong style="color: var(--color-warning);">Efteranmälan:</strong> Sista <?= $lateDays ?> dagarna</span>
                    </div>
                </div>

            <?php elseif ($assignedTemplate): ?>
                <div class="text-center p-md">
                    <p class="text-secondary mb-sm">Mallen "<?= htmlspecialchars($assignedTemplate['name']) ?>" saknar klasspriser.</p>
                    <a href="/admin/pricing-templates.php?edit=<?= $event['pricing_template_id'] ?>" class="btn-admin btn-admin-sm btn-admin-primary">Konfigurera priser</a>
                </div>

            <?php else: ?>
                <div class="text-center p-md">
                    <p class="text-secondary mb-sm">Ingen prismall tilldelad. Välj en mall i <strong>Tävlingsinställningar</strong> ovan.</p>
                    <a href="/admin/pricing-templates.php" class="text-accent text-sm">Hantera prismallar</a>
                </div>
            <?php endif; ?>
        </div>
    </details>
    <?php endif; /* End hide Klasser for promotors */ ?>

    <!-- ORGANIZER & CONTACT - Editable for promotors -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>Arrangör & Kontakt</h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <div class="form-grid form-grid-2">
                <div class="admin-form-group">
                    <label class="admin-form-label">Arrangör (klubb)</label>
                    <select name="organizer_club_id" class="admin-form-select">
                        <option value="">Välj klubb...</option>
                        <?php foreach ($clubs as $club): ?>
                            <option value="<?= $club['id'] ?>" <?= ($event['organizer_club_id'] ?? '') == $club['id'] ? 'selected' : '' ?>>
                                <?= h($club['name']) ?><?php if ($club['city']): ?> (<?= h($club['city']) ?>)<?php endif; ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Webbplats</label>
                    <input type="url" name="website" class="admin-form-input" value="<?= h($event['website'] ?? '') ?>" placeholder="https://...">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Kontakt e-post</label>
                    <input type="email" name="contact_email" class="admin-form-input" value="<?= h($event['contact_email'] ?? '') ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Kontakt telefon</label>
                    <input type="tel" name="contact_phone" class="admin-form-input" value="<?= h($event['contact_phone'] ?? '') ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Anmälningsfrist (datum)</label>
                    <input type="date" name="registration_deadline" class="admin-form-input" value="<?= h($event['registration_deadline'] ?? '') ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Anmälningsfrist (klockslag)</label>
                    <input type="time" name="registration_deadline_time" class="admin-form-input" value="<?= h($event['registration_deadline_time'] ?? '') ?>">
                    <small class="form-help">Lämna tomt för 23:59</small>
                </div>
            </div>
        </div>
    </details>

    <!-- PAYMENT SETTINGS - Locked for promotors -->
    <?php if ($paymentRecipientColumnExists && !empty($paymentRecipients)): ?>
    <?php if ($isPromotorOnly): ?>
    <input type="hidden" name="payment_recipient_id" value="<?= h($event['payment_recipient_id'] ?? '') ?>">
    <?php endif; ?>
    <details class="admin-card mb-lg <?= $isPromotorOnly ? 'locked-section' : '' ?>">
        <summary class="admin-card-header collapsible-header">
            <h2>Betalning</h2>
            <?php if ($isPromotorOnly): ?>
            <span class="locked-badge">
                <i data-lucide="lock"></i> Låst
            </span>
            <?php else: ?>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
            <?php endif; ?>
        </summary>
        <fieldset class="admin-card-body fieldset-reset" style="padding: var(--space-lg);" <?= $isPromotorOnly ? 'disabled' : '' ?>>
            <div class="admin-form-group">
                <label class="admin-form-label">Betalningsmottagare (Swish)</label>
                <select name="payment_recipient_id" class="admin-form-select">
                    <option value="">Använd seriens mottagare</option>
                    <?php foreach ($paymentRecipients as $recipient): ?>
                        <option value="<?= $recipient['id'] ?>" <?= ($event['payment_recipient_id'] ?? '') == $recipient['id'] ? 'selected' : '' ?>>
                            <?= h($recipient['name']) ?> (<?= h($recipient['swish_number']) ?>)
                        </option>
                    <?php endforeach; ?>
                </select>
                <small class="form-help">
                    Välj en specifik mottagare för detta event, eller lämna tomt för att använda seriens mottagare.
                    <a href="/admin/payment-recipients" class="text-accent">Hantera mottagare</a>
                </small>
            </div>
        </fieldset>
    </details>
    <?php endif; ?>

    <!-- GRAVITY ID DISCOUNT -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2><i data-lucide="badge-check" class="icon-md"></i> Gravity ID-rabatt</h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <p class="text-secondary text-sm mb-md">
                Sätt rabatt för deltagare med Gravity ID. Lämna 0 för att använda seriens inställning.
            </p>
            <div class="admin-form-group">
                <label class="admin-form-label">Rabatt (SEK)</label>
                <input type="number" name="gravity_id_discount" class="admin-form-input" style="max-width: 200px;"
                       value="<?= h($event['gravity_id_discount'] ?? 0) ?>"
                       min="0" step="1" placeholder="0">
                <small class="form-help">
                    0 = använd seriens inställning, >0 = specifik rabatt för detta event
                </small>
            </div>
            <?php
            // Get series GID discount if available
            if (!empty($event['series_id'])) {
                try {
                    $seriesGid = $db->getRow("SELECT gravity_id_discount FROM series WHERE id = ?", [$event['series_id']]);
                    $seriesDiscount = floatval($seriesGid['gravity_id_discount'] ?? 0);
                    if ($seriesDiscount > 0):
            ?>
            <div class="info-box mt-sm">
                Seriens rabatt: <strong><?= $seriesDiscount ?> kr</strong>
            </div>
            <?php
                    endif;
                } catch (Exception $e) {}
            }
            ?>
        </div>
    </details>

    <!-- LOCATION DETAILS - Editable for promotors -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>Platsdetaljer</h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <div class="form-grid form-grid-2">
                <div class="admin-form-group">
                    <label class="admin-form-label">GPS-koordinater</label>
                    <input type="text" name="venue_coordinates" class="admin-form-input" value="<?= h($event['venue_coordinates'] ?? '') ?>" placeholder="59.3293, 18.0686">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Google Maps URL</label>
                    <input type="url" name="venue_map_url" class="admin-form-input" value="<?= h($event['venue_map_url'] ?? '') ?>">
                </div>

                <div class="admin-form-group form-full-width">
                    <label class="admin-form-label">Platsdetaljer</label>
                    <textarea name="venue_details" class="admin-form-input" rows="3"><?= h($event['venue_details'] ?? '') ?></textarea>
                </div>
            </div>
        </div>
    </details>

    <!-- INVITATION & FACILITIES - Editable for promotors -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>Inbjudan</h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <!-- Invitation field - shown first -->
            <div class="admin-form-group mb-lg pb-lg border-bottom">
                <label class="admin-form-label text-base font-semibold">
                    Inbjudningstext
                    <label class="checkbox-inline">
                        <input type="checkbox" name="invitation_use_global" <?= !empty($event['invitation_use_global']) ? 'checked' : '' ?>>
                        <span class="text-xs">Global</span>
                    </label>
                    <label class="checkbox-inline checkbox-hidden">
                        <input type="checkbox" name="invitation_hidden" <?= !empty($event['invitation_hidden']) ? 'checked' : '' ?>>
                        <span class="text-xs">Visa ej</span>
                    </label>
                </label>
                <textarea name="invitation" class="admin-form-input" rows="4" placeholder="Välkommen till... (visas högst upp på Inbjudan-fliken)"><?= h($event['invitation'] ?? '') ?></textarea>
                <small class="form-help">Inledande text som visas högst upp på Inbjudan-fliken på event-sidan.</small>
            </div>

            <p class="text-secondary text-sm mb-lg">
                <strong>Faciliteter & Logistik</strong> - Övrig information för Inbjudan-fliken.
            </p>

            <?php
            $facilityFields = [
                ['key' => 'hydration_stations', 'label' => 'Vätskekontroller', 'global_key' => 'hydration_use_global', 'hidden_key' => 'hydration_hidden'],
                ['key' => 'toilets_showers', 'label' => 'Toaletter/Dusch', 'global_key' => 'toilets_use_global', 'hidden_key' => 'toilets_hidden'],
                ['key' => 'bike_wash', 'label' => 'Cykeltvätt', 'global_key' => 'bike_wash_use_global', 'hidden_key' => 'bike_wash_hidden'],
                ['key' => 'food_cafe', 'label' => 'Mat/Café', 'global_key' => 'food_use_global', 'hidden_key' => 'food_hidden'],
                ['key' => 'shops_info', 'label' => 'Affärer', 'global_key' => 'shops_use_global', 'hidden_key' => 'shops_hidden'],
                ['key' => 'exhibitors', 'label' => 'Utställare', 'global_key' => 'exhibitors_use_global', 'hidden_key' => 'exhibitors_hidden'],
                ['key' => 'parking_detailed', 'label' => 'Parkering', 'global_key' => 'parking_use_global', 'hidden_key' => 'parking_hidden'],
                ['key' => 'hotel_accommodation', 'label' => 'Hotell/Boende', 'global_key' => 'hotel_use_global', 'hidden_key' => 'hotel_hidden'],
                ['key' => 'local_info', 'label' => 'Lokal information', 'global_key' => 'local_use_global', 'hidden_key' => 'local_hidden'],
                ['key' => 'media_production', 'label' => 'Media', 'global_key' => 'media_use_global', 'hidden_key' => 'media_hidden'],
                ['key' => 'contacts_info', 'label' => 'Kontakter', 'global_key' => 'contacts_use_global', 'hidden_key' => 'contacts_hidden'],
            ];
            ?>

            <div class="form-grid form-grid-2">
                <?php foreach ($facilityFields as $field): ?>
                    <div class="admin-form-group">
                        <label class="admin-form-label">
                            <?= $field['label'] ?>
                            <label class="checkbox-inline">
                                <input type="checkbox" name="<?= $field['global_key'] ?>" <?= !empty($event[$field['global_key']]) ? 'checked' : '' ?>>
                                <span class="text-xs">Global</span>
                            </label>
                            <label class="checkbox-inline checkbox-hidden">
                                <input type="checkbox" name="<?= $field['hidden_key'] ?>" <?= !empty($event[$field['hidden_key']]) ? 'checked' : '' ?>>
                                <span class="text-xs">Visa ej</span>
                            </label>
                        </label>
                        <textarea name="<?= $field['key'] ?>" class="admin-form-input" rows="2"><?= h($event[$field['key']] ?? '') ?></textarea>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    </details>

    <!-- PM (PROMEMORIA) - Collapsible -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>PM (Promemoria)</h2>
            <span class="text-secondary text-sm">Klicka för att expandera</span>
        </summary>
        <div class="admin-card-body">
            <!-- Publish date/time for PM -->
            <div class="admin-form-group mb-lg pb-md border-bottom">
                <div class="flex items-center gap-sm flex-wrap">
                    <label class="text-sm font-medium whitespace-nowrap">
                        <i data-lucide="calendar-clock" class="icon-sm inline-block"></i>
                        Publiceras:
                    </label>
                    <input type="datetime-local" name="pm_publish_at"
                           class="admin-form-input admin-form-input-sm"
                           style="max-width: 220px;"
                           value="<?= !empty($event['pm_publish_at']) ? date('Y-m-d\TH:i', strtotime($event['pm_publish_at'])) : '' ?>">
                    <small class="form-help text-xs">Lämna tomt = synlig direkt</small>
                </div>
            </div>

            <p class="text-secondary text-sm mb-lg">
                Innehåll för PM-fliken. Markera "Global" för att använda standardtext.
            </p>

            <?php
            $pmFields = [
                ['key' => 'pm_content', 'label' => 'PM Huvudtext', 'global_key' => 'pm_use_global', 'hidden_key' => 'pm_hidden'],
                ['key' => 'driver_meeting', 'label' => 'Förarmöte', 'global_key' => 'driver_meeting_use_global', 'hidden_key' => 'driver_meeting_hidden'],
                ['key' => 'training_info', 'label' => 'Träning', 'global_key' => 'training_use_global', 'hidden_key' => 'training_hidden'],
                ['key' => 'timing_info', 'label' => 'Tidtagning', 'global_key' => 'timing_use_global', 'hidden_key' => 'timing_hidden'],
                ['key' => 'lift_info', 'label' => 'Lift', 'global_key' => 'lift_use_global', 'hidden_key' => 'lift_hidden'],
                ['key' => 'competition_rules', 'label' => 'Tävlingsregler', 'global_key' => 'rules_use_global', 'hidden_key' => 'rules_hidden'],
                ['key' => 'insurance_info', 'label' => 'Försäkring', 'global_key' => 'insurance_use_global', 'hidden_key' => 'insurance_hidden'],
                ['key' => 'equipment_info', 'label' => 'Utrustning', 'global_key' => 'equipment_use_global', 'hidden_key' => 'equipment_hidden'],
                ['key' => 'medical_info', 'label' => 'Sjukvård', 'global_key' => 'medical_use_global', 'hidden_key' => 'medical_hidden'],
                ['key' => 'scf_representatives', 'label' => 'SCF Representanter', 'global_key' => 'scf_use_global', 'hidden_key' => 'scf_hidden'],
            ];
            ?>

            <div class="form-grid form-grid-2">
                <?php foreach ($pmFields as $field): ?>
                    <div class="admin-form-group">
                        <label class="admin-form-label">
                            <?= $field['label'] ?>
                            <label class="checkbox-inline">
                                <input type="checkbox" name="<?= $field['global_key'] ?>" <?= !empty($event[$field['global_key']]) ? 'checked' : '' ?>>
                                <span class="text-xs">Global</span>
                            </label>
                            <label class="checkbox-inline checkbox-hidden">
                                <input type="checkbox" name="<?= $field['hidden_key'] ?>" <?= !empty($event[$field['hidden_key']]) ? 'checked' : '' ?>>
                                <span class="text-xs">Visa ej</span>
                            </label>
                        </label>
                        <textarea name="<?= $field['key'] ?>" class="admin-form-input" rows="3"><?= h($event[$field['key']] ?? '') ?></textarea>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    </details>

    <!-- ÖVRIGA EVENT-FLIKAR - Collapsible -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>Övriga event-flikar</h2>
            <span class="text-secondary text-sm">Jury, Schema, Starttider</span>
        </summary>
        <div class="admin-card-body">
            <p class="text-secondary text-sm mb-lg">
                Separata flikar som visas om innehåll finns (eller global text aktiverad).
            </p>

            <?php
            $otherTabFields = [
                ['key' => 'jury_communication', 'label' => 'Jurykommuniké', 'global_key' => 'jury_use_global', 'hidden_key' => 'jury_hidden'],
                ['key' => 'competition_schedule', 'label' => 'Tävlingsschema', 'global_key' => 'schedule_use_global', 'hidden_key' => 'schedule_hidden'],
                ['key' => 'start_times', 'label' => 'Starttider', 'global_key' => 'start_times_use_global', 'hidden_key' => 'start_times_hidden', 'publish_key' => 'starttider_publish_at'],
            ];
            ?>

            <div class="form-grid form-grid-2">
                <?php foreach ($otherTabFields as $field): ?>
                    <div class="admin-form-group">
                        <label class="admin-form-label">
                            <?= $field['label'] ?>
                            <label class="checkbox-inline">
                                <input type="checkbox" name="<?= $field['global_key'] ?>" <?= !empty($event[$field['global_key']]) ? 'checked' : '' ?>>
                                <span class="text-xs">Global</span>
                            </label>
                            <label class="checkbox-inline checkbox-hidden">
                                <input type="checkbox" name="<?= $field['hidden_key'] ?>" <?= !empty($event[$field['hidden_key']]) ? 'checked' : '' ?>>
                                <span class="text-xs">Visa ej</span>
                            </label>
                        </label>
                        <textarea name="<?= $field['key'] ?>" class="admin-form-input" rows="3"><?= h($event[$field['key']] ?? '') ?></textarea>
                        <?php if (!empty($field['publish_key'])): ?>
                        <div class="mt-sm flex items-center gap-sm">
                            <label class="text-xs text-secondary whitespace-nowrap">
                                <i data-lucide="calendar-clock" class="icon-xs inline-block"></i>
                                Publiceras:
                            </label>
                            <input type="datetime-local" name="<?= $field['publish_key'] ?>"
                                   class="admin-form-input text-xs"
                                   value="<?= !empty($event[$field['publish_key']]) ? date('Y-m-d\TH:i', strtotime($event[$field['publish_key']])) : '' ?>">
                            <small class="form-help text-xs">Lämna tomt = synlig direkt</small>
                        </div>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            </div>

            <!-- Map Link -->
            <div class="admin-form-group mt-lg">
                <label class="admin-form-label">Karta</label>
                <div class="flex gap-sm items-center">
                    <?php if (!empty($event['map_image_url'])): ?>
                    <span class="badge badge-success">Kartbild aktiv</span>
                    <?php endif; ?>
                    <a href="/admin/event-map.php?id=<?= $id ?>" class="btn-admin btn-admin-secondary btn-admin-sm">
                        <i data-lucide="map" class="icon-sm"></i>
                        Hantera karta
                    </a>
                </div>
                <small class="form-help">Ladda upp GPX-fil för interaktiv karta eller statisk kartbild.</small>
            </div>
        </div>
    </details>

    <!-- SPONSORS - Editable for promotors -->
    <?php if (!empty($allSponsors)): ?>
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
                Sponsorer
            </h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <p class="mb-md text-secondary text-sm">
                Välj sponsorer specifikt för detta event. <strong>OBS:</strong> Seriens sponsorer visas om inga event-sponsorer anges.
            </p>

            <div class="flex flex-col gap-lg">
                <!-- Header Banner from Media Library -->
                <div class="admin-form-group">
                    <label class="admin-form-label">Header-banner (stor banner högst upp)</label>
                    <select name="header_banner_media_id" class="admin-form-select">
                        <option value="">-- Ingen (använd seriens) --</option>
                        <?php foreach ($eventMediaFiles as $media): ?>
                        <option value="<?= $media['id'] ?>" <?= ($event['header_banner_media_id'] ?? '') == $media['id'] ? 'selected' : '' ?>>
                            <?= htmlspecialchars($media['original_filename']) ?>
                        </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="form-help block mt-sm">
                        Välj bild från <a href="/admin/media?folder=events" target="_blank">Mediabiblioteket (Event-mappen)</a>
                    </small>
                </div>

                <!-- Header Banner Sponsor -->
                <div class="admin-form-group">
                    <label class="admin-form-label">Banner-sponsor (bred banner högst upp)</label>
                    <select name="sponsor_header" class="admin-form-select">
                        <option value="">-- Ingen (använd seriens) --</option>
                        <?php foreach ($allSponsors as $sp): ?>
                        <option value="<?= $sp['id'] ?>" <?= in_array((int)$sp['id'], $eventSponsors['header']) ? 'selected' : '' ?>>
                            <?= htmlspecialchars($sp['name']) ?> (<?= ucfirst($sp['tier']) ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="form-help block mt-sm">
                        Sponsorns banner-logo visas som bred banner högst upp på event-sidan
                    </small>
                </div>

                <!-- Content Logo Row - Max 5 -->
                <div class="admin-form-group">
                    <label class="admin-form-label">
                        Logo-rad (under event-info)
                        <span id="logoRowCount" class="font-normal text-secondary ml-sm">
                            (<?= count($eventSponsors['content']) ?>/5 valda)
                        </span>
                    </label>
                    <div id="logoRowSponsors" class="tag-list">
                        <?php foreach ($allSponsors as $sp): ?>
                        <label class="sponsor-checkbox">
                            <input type="checkbox" name="sponsor_content[]" value="<?= $sp['id'] ?>" class="logo-row-checkbox" <?= in_array((int)$sp['id'], $eventSponsors['content']) ? 'checked' : '' ?>>
                            <?= htmlspecialchars($sp['name']) ?>
                        </label>
                        <?php endforeach; ?>
                    </div>
                    <small class="form-help block mt-sm">
                        Max 5 sponsorer i logo-raden. Visas på desktop i en rad, mobil i 3-kolumner.
                    </small>
                </div>

                <!-- Results Sponsor -->
                <div class="admin-form-group">
                    <label class="admin-form-label">Resultat-sponsor ("Resultat sponsrat av")</label>
                    <select name="sponsor_sidebar" class="admin-form-select">
                        <option value="">-- Ingen (använd seriens) --</option>
                        <?php foreach ($allSponsors as $sp): ?>
                        <option value="<?= $sp['id'] ?>" <?= in_array((int)$sp['id'], $eventSponsors['sidebar']) ? 'selected' : '' ?>>
                            <?= htmlspecialchars($sp['name']) ?> (<?= ucfirst($sp['tier']) ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>
        </div>
    </details>

    <!-- SAMARBETSPARTNERS - Partner logo row at bottom -->
    <details class="admin-card mb-lg">
        <summary class="admin-card-header collapsible-header">
            <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><path d="M11 17a1 1 0 0 1 2 0c0 .5-.34 3-.5 4.5a.5.5 0 0 1-1 0c-.16-1.5-.5-4-.5-4.5Z"/><path d="M8 14a6 6 0 1 1 8 0"/><path d="M12 2v1"/><path d="m4.93 4.93.71.71"/><path d="M2 12h1"/><path d="m4.93 19.07.71-.71"/><path d="m19.07 4.93-.71.71"/><path d="M22 12h-1"/><path d="m19.07 19.07-.71-.71"/></svg>
                Samarbetspartners
            </h2>
            <span class="text-secondary text-sm">Klicka för att expandera/minimera</span>
        </summary>
        <div class="admin-card-body">
            <p class="mb-md text-secondary text-sm">
                Visa lokala samarbetspartners längst ner på event-sidan.
            </p>

            <div class="admin-form-group">
                <label class="admin-form-label">
                    Partner-logorad (längst ner på sidan)
                    <span id="partnerCount" class="font-normal text-secondary ml-sm">
                        (<?= count($eventSponsors['partner']) ?> valda)
                    </span>
                </label>
                <div id="partnerSponsors" class="partner-grid">
                    <?php foreach ($allSponsors as $sp): ?>
                    <label class="sponsor-checkbox">
                        <input type="checkbox" name="sponsor_partner[]" value="<?= $sp['id'] ?>" class="partner-checkbox" <?= in_array((int)$sp['id'], $eventSponsors['partner']) ? 'checked' : '' ?>>
                        <?= htmlspecialchars($sp['name']) ?>
                    </label>
                    <?php endforeach; ?>
                </div>
                <small class="form-help block mt-sm">
                    Visas i en egen sektion längst ner på event-sidan. 4 i bredd på desktop, 2 på mobil.
                </small>

                <!-- Link to sponsors page to add new partners -->
                <a href="/admin/sponsors.php" class="btn btn-secondary mt-md">
                    <i data-lucide="plus" class="icon-sm"></i>
                    Lägg till ny partner
                </a>
            </div>
        </div>
    </details>
    <?php endif; ?>

    <!-- STATUS & ACTIONS -->
    <div class="admin-card">
        <div class="admin-card-body">
            <div class="flex items-center justify-between flex-wrap gap-md">
                <?php if ($isPromotorOnly): ?>
                <!-- Readonly status display for promotors -->
                <div class="flex items-center gap-sm text-secondary">
                    <input type="checkbox" disabled <?= $event['active'] ? 'checked' : '' ?>>
                    <span>Aktivt event</span>
                </div>
                <div class="flex items-center gap-sm text-secondary">
                    <input type="checkbox" disabled <?= !empty($event['is_championship']) ? 'checked' : '' ?>>
                    <span><i data-lucide="trophy" class="icon-sm"></i> Svenskt Mästerskap</span>
                    <?php if (!empty($event['is_championship'])): ?>
                    <span class="admin-badge admin-badge-success text-xs ml-sm">SM</span>
                    <?php endif; ?>
                </div>
                <!-- Hidden fields to preserve values -->
                <input type="hidden" name="active" value="<?= $event['active'] ? '1' : '0' ?>">
                <input type="hidden" name="is_championship" value="<?= !empty($event['is_championship']) ? '1' : '0' ?>">
                <?php else: ?>
                <label class="flex items-center gap-sm cursor-pointer">
                    <input type="checkbox" name="active" <?= $event['active'] ? 'checked' : '' ?>>
                    <span>Aktivt event</span>
                </label>

                <label class="flex items-center gap-sm cursor-pointer">
                    <input type="checkbox" name="is_championship" value="1" <?= !empty($event['is_championship']) ? 'checked' : '' ?>>
                    <span><i data-lucide="trophy" class="icon-sm"></i> Svenskt Mästerskap</span>
                    <?php if (!empty($event['is_championship'])): ?>
                    <span class="admin-badge admin-badge-success text-xs ml-sm">SM</span>
                    <?php endif; ?>
                </label>
                <?php endif; ?>

                <div class="flex gap-sm">
                    <a href="/admin/events" class="btn-admin btn-admin-secondary">Avbryt</a>
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                        Spara Ändringar
                    </button>
                </div>
            </div>
        </div>
    </div>
</form>

<!-- Floating Save Button -->
<div class="floating-save-bar">
    <div class="floating-save-content">
        <a href="/admin/events" class="btn-admin btn-admin-secondary">Avbryt</a>
        <button type="submit" form="eventEditForm" class="btn-admin btn-admin-primary">
            <i data-lucide="save" class="icon-sm"></i>
            Spara Ändringar
        </button>
    </div>
</div>

<style>
.floating-save-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--color-bg);
    border-top: 1px solid var(--color-border);
    box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
    padding: var(--space-sm) var(--space-md);
    z-index: 1000;
    padding-bottom: calc(var(--space-sm) + env(safe-area-inset-bottom, 0));
}
@media (min-width: 769px) {
    .floating-save-bar {
        left: var(--sidebar-width, 280px);
    }
}
/* Mobile portrait: Position above mobile nav */
@media (max-width: 899px) and (orientation: portrait) {
    .floating-save-bar {
        bottom: calc(var(--mobile-nav-height, 64px) + env(safe-area-inset-bottom, 0px));
        padding-bottom: var(--space-sm);
    }
}
.floating-save-content {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    max-width: 1200px;
    margin: 0 auto;
}
/* Mobile: Stack buttons */
@media (max-width: 599px) {
    .floating-save-content {
        flex-direction: column;
    }
    .floating-save-content .btn {
        width: 100%;
        justify-content: center;
    }
}
/* Add padding at bottom of page to account for floating bar */
.admin-content {
    padding-bottom: 80px !important;
}
/* Extra padding on mobile for floating bar + mobile nav */
@media (max-width: 899px) and (orientation: portrait) {
    .admin-content {
        padding-bottom: calc(80px + var(--mobile-nav-height, 64px) + env(safe-area-inset-bottom, 0px)) !important;
    }
}
/* Styling for hidden checkbox to indicate hiding content */
.checkbox-hidden span {
    color: var(--color-danger);
}
.checkbox-hidden input:checked + span {
    font-weight: 600;
}
</style>

<script>
// Limit checkbox selections for sponsor rows (maxCount = 0 means unlimited)
function setupCheckboxLimit(containerSelector, maxCount, countDisplayId) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const checkboxes = container.querySelectorAll('input[type="checkbox"]');
    const countDisplay = document.getElementById(countDisplayId);
    const unlimited = maxCount === 0;

    function updateCount() {
        const checked = container.querySelectorAll('input[type="checkbox"]:checked').length;
        if (countDisplay) {
            if (unlimited) {
                countDisplay.textContent = `(${checked} valda)`;
                countDisplay.style.color = 'var(--color-text-secondary)';
            } else {
                countDisplay.textContent = `(${checked}/${maxCount} valda)`;
                countDisplay.style.color = checked >= maxCount ? 'var(--color-warning)' : 'var(--color-text-secondary)';
            }
        }
        return checked;
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const checked = updateCount();
            if (!unlimited && checked > maxCount) {
                this.checked = false;
                updateCount();
                alert(`Max ${maxCount} val tillåtet`);
            }
        });
    });

    updateCount();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupCheckboxLimit('#logoRowSponsors', 5, 'logoRowCount');
    setupCheckboxLimit('#partnerSponsors', 0, 'partnerCount'); // 0 = unlimited
});

</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
