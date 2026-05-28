<?php
/**
 * API Endpoint: Artist Name Claim
 *
 * Allows logged-in users to claim anonymous/artist name profiles.
 * Creates a claim that requires admin approval before merging.
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../hub-config.php';

// Only POST allowed
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Get parameters
$anonymousRiderId = (int)($_POST['anonymous_rider_id'] ?? 0);
$claimingRiderId = (int)($_POST['claiming_rider_id'] ?? 0);
$evidence = trim($_POST['evidence'] ?? '');
$action = trim($_POST['action'] ?? 'claim'); // 'claim' or 'activate'

if (!$anonymousRiderId) {
    echo json_encode(['success' => false, 'error' => 'Ogiltig profil']);
    exit;
}

// Get current user
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;

// For 'claim' action, user must be logged in
if ($action === 'claim' && !$currentUser) {
    echo json_encode(['success' => false, 'error' => 'Du maste vara inloggad for att gora detta']);
    exit;
}

try {
    $db = getDB();

    // Check if artist_name_claims table exists
    $tableExists = false;
    try {
        $db->query("SELECT 1 FROM artist_name_claims LIMIT 1");
        $tableExists = true;
    } catch (Exception $e) {
        $tableExists = false;
    }

    if (!$tableExists) {
        echo json_encode(['success' => false, 'error' => 'Funktionen ar inte aktiverad. Kontakta admin.']);
        exit;
    }

    // Check that anonymous rider exists
    $anonymousRider = $db->getRow("SELECT id, firstname, is_anonymous FROM riders WHERE id = ?", [$anonymousRiderId]);

    if (!$anonymousRider) {
        echo json_encode(['success' => false, 'error' => 'Profilen hittades inte']);
        exit;
    }

    // Verify this is an anonymous/artist name profile
    $isAnonymous = false;
    try {
        $isAnonymous = (bool)$anonymousRider['is_anonymous'];
    } catch (Exception $e) {
        // Column might not exist - check criteria
        $checkRider = $db->getRow("
            SELECT id FROM riders
            WHERE id = ?
              AND (lastname IS NULL OR lastname = '')
              AND (birth_year IS NULL OR birth_year = 0)
              AND club_id IS NULL
        ", [$anonymousRiderId]);
        $isAnonymous = !empty($checkRider);
    }

    if (!$isAnonymous) {
        echo json_encode(['success' => false, 'error' => 'Denna profil ar inte ett artistnamn']);
        exit;
    }

    // Check if there's already a pending claim for this anonymous rider
    $existingClaim = $db->getRow(
        "SELECT id FROM artist_name_claims WHERE anonymous_rider_id = ? AND status = 'pending'",
        [$anonymousRiderId]
    );

    if ($existingClaim) {
        echo json_encode(['success' => false, 'error' => 'Det finns redan en vantande forfragan for denna profil']);
        exit;
    }

    // Handle different actions
    if ($action === 'activate') {
        // User wants to activate/fill in the artist name profile directly
        // This creates a claim that admin needs to approve, then the profile gets updated

        $email = trim($_POST['email'] ?? '');
        $firstname = trim($_POST['firstname'] ?? '');
        $lastname = trim($_POST['lastname'] ?? '');
        $birthYear = (int)($_POST['birth_year'] ?? 0);
        $phone = trim($_POST['phone'] ?? '');

        if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            echo json_encode(['success' => false, 'error' => 'Ogiltig e-postadress']);
            exit;
        }

        if (empty($lastname)) {
            echo json_encode(['success' => false, 'error' => 'Efternamn kravs']);
            exit;
        }

        // Check if email is already used
        $existingRider = $db->getRow("SELECT id, firstname, lastname FROM riders WHERE email = ?", [$email]);
        if ($existingRider) {
            echo json_encode([
                'success' => false,
                'error' => 'E-postadressen anvands redan. Anvand "Koppla till befintlig profil" istallet.'
            ]);
            exit;
        }

        // Create activation claim with profile data in evidence
        $activationData = json_encode([
            'type' => 'activation',
            'email' => $email,
            'firstname' => $firstname ?: $anonymousRider['firstname'],
            'lastname' => $lastname,
            'birth_year' => $birthYear ?: null,
            'phone' => $phone ?: null
        ]);

        $db->insert('artist_name_claims', [
            'anonymous_rider_id' => $anonymousRiderId,
            'claiming_user_id' => $currentUser['id'] ?? null,
            'claiming_rider_id' => null, // No existing rider - activating directly
            'evidence' => $activationData,
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]);

        error_log("ARTIST NAME ACTIVATION: User requested to activate anonymous rider {$anonymousRiderId} ({$anonymousRider['firstname']}) with email {$email}");

        echo json_encode([
            'success' => true,
            'message' => 'Forfragan skickad! En admin kommer granska och godkanna aktiveringen.',
            'type' => 'activation'
        ]);

    } else {
        // User wants to link this artist name to their existing profile
        if (!$claimingRiderId && $currentUser) {
            $claimingRiderId = $currentUser['id'];
        }

        if (!$claimingRiderId) {
            echo json_encode(['success' => false, 'error' => 'Ingen profil att koppla till']);
            exit;
        }

        // Verify claiming rider exists
        $claimingRider = $db->getRow("SELECT id, firstname, lastname FROM riders WHERE id = ?", [$claimingRiderId]);
        if (!$claimingRider) {
            echo json_encode(['success' => false, 'error' => 'Din profil hittades inte']);
            exit;
        }

        // Make sure they're not trying to claim their own profile
        if ($anonymousRiderId === $claimingRiderId) {
            echo json_encode(['success' => false, 'error' => 'Du kan inte gora ansprak pa din egen profil']);
            exit;
        }

        // Create claim
        $db->insert('artist_name_claims', [
            'anonymous_rider_id' => $anonymousRiderId,
            'claiming_user_id' => $currentUser['id'] ?? null,
            'claiming_rider_id' => $claimingRiderId,
            'evidence' => $evidence ?: null,
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]);

        $claimingName = trim($claimingRider['firstname'] . ' ' . $claimingRider['lastname']);
        error_log("ARTIST NAME CLAIM: {$claimingName} (ID: {$claimingRiderId}) claimed anonymous rider {$anonymousRiderId} ({$anonymousRider['firstname']}). Evidence: {$evidence}");

        echo json_encode([
            'success' => true,
            'message' => 'Forfragan skickad! En admin kommer granska och godkanna kopplingen. Dina resultat kommer da sammanfogas.',
            'type' => 'claim'
        ]);
    }

} catch (Exception $e) {
    error_log("Artist name claim error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Ett fel uppstod. Forsok igen senare.']);
}
