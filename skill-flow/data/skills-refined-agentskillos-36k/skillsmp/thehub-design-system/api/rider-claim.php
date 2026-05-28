<?php
/**
 * API Endpoint: Profile Claim / Email Connection Request
 *
 * ALL email connections now create a claim that requires admin approval.
 * This ensures proper identity verification before connecting emails to profiles.
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
$targetRiderId = (int)($_POST['target_rider_id'] ?? 0);
$email = trim($_POST['email'] ?? '');
$phone = trim($_POST['phone'] ?? '');
$instagram = trim($_POST['instagram'] ?? '');
$facebook = trim($_POST['facebook'] ?? '');
$reason = trim($_POST['reason'] ?? '');

if (!$targetRiderId) {
    echo json_encode(['success' => false, 'error' => 'Ogiltig profil']);
    exit;
}

// No login required - claims go to admin for approval
// Admin verifies identity before connecting email to profile
$isSuperAdmin = function_exists('hub_is_super_admin') && hub_is_super_admin();
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;

try {
    $db = getDB();

    // Check that target rider exists and has no email
    $targetRider = $db->getRow("SELECT id, email, firstname, lastname FROM riders WHERE id = ?", [$targetRiderId]);

    if (!$targetRider) {
        echo json_encode(['success' => false, 'error' => 'Profilen hittades inte']);
        exit;
    }

    if (!empty($targetRider['email'])) {
        echo json_encode(['success' => false, 'error' => 'Denna profil har redan en e-postadress']);
        exit;
    }

    // Validate email
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['success' => false, 'error' => 'Ogiltig e-postadress']);
        exit;
    }

    // Check if email is already used by another rider
    $existingRider = $db->getRow("SELECT id, firstname, lastname FROM riders WHERE email = ? AND id != ?", [$email, $targetRiderId]);
    if ($existingRider) {
        echo json_encode([
            'success' => false,
            'error' => 'E-postadressen används redan av ' . $existingRider['firstname'] . ' ' . $existingRider['lastname'] . ' (ID: ' . $existingRider['id'] . ')'
        ]);
        exit;
    }

    // Check if there's already a pending claim for this target
    $existingClaim = $db->getRow(
        "SELECT id FROM rider_claims WHERE target_rider_id = ? AND status = 'pending'",
        [$targetRiderId]
    );

    if ($existingClaim) {
        echo json_encode(['success' => false, 'error' => 'Det finns redan en väntande förfrågan för denna profil']);
        exit;
    }

    // Build verification notes
    $verificationNotes = [];
    if ($phone) $verificationNotes[] = "Tel: {$phone}";
    if ($instagram) $verificationNotes[] = "IG: {$instagram}";
    if ($facebook) $verificationNotes[] = "FB: {$facebook}";
    if ($reason) $verificationNotes[] = $reason;
    $fullNotes = implode(' | ', $verificationNotes);

    // Determine who is making the claim
    $claimantRiderId = $currentUser['id'] ?? null;
    $claimantName = $isSuperAdmin ? 'Super Admin' : trim(($currentUser['firstname'] ?? '') . ' ' . ($currentUser['lastname'] ?? ''));

    // Check if new columns exist (migration 077)
    $hasNewColumns = false;
    try {
        $colCheck = $db->getRow("SHOW COLUMNS FROM rider_claims LIKE 'phone'");
        $hasNewColumns = !empty($colCheck);
    } catch (Exception $e) {
        $hasNewColumns = false;
    }

    // Create the claim - requires admin approval
    if ($hasNewColumns) {
        // Use new schema with additional columns
        $db->insert('rider_claims', [
            'claimant_rider_id' => $claimantRiderId,
            'target_rider_id' => $targetRiderId,
            'claimant_email' => $email,
            'claimant_name' => $claimantName,
            'phone' => $phone ?: null,
            'instagram' => $instagram ?: null,
            'facebook' => $facebook ?: null,
            'created_by' => $isSuperAdmin ? 'admin' : 'user',
            'reason' => $fullNotes ?: null,
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]);
    } else {
        // Fallback to old schema (include contact info in reason)
        $db->insert('rider_claims', [
            'claimant_rider_id' => $claimantRiderId,
            'target_rider_id' => $targetRiderId,
            'claimant_email' => $email,
            'claimant_name' => $claimantName,
            'reason' => $fullNotes ?: null,
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]);
    }

    // Log the action
    $targetName = trim($targetRider['firstname'] . ' ' . $targetRider['lastname']);
    error_log("PROFILE CLAIM CREATED: {$claimantName} requested to connect '{$email}' to rider {$targetRiderId} ({$targetName}). Verification: {$fullNotes}");

    echo json_encode([
        'success' => true,
        'message' => 'Förfrågan skickad! En administratör kommer att granska och godkänna kopplingen.',
        'requires_approval' => true
    ]);

} catch (Exception $e) {
    error_log("Rider claim error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Ett fel uppstod. Försök igen senare.']);
}
