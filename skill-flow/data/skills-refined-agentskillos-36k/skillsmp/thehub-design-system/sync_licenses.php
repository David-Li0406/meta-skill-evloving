<?php
/**
 * TheHUB License Sync Tool
 * Synkroniserar licenser från SCF License Portal API
 * 
 * Funktioner:
 * - Uppdaterar befintliga riders med 2026-licenser
 * - Skapar nya riders från UCI-databasen
 * - Batchbearbetning (25 UCI ID per anrop)
 * - Loggning av alla ändringar
 */

// Inkludera databaskonfiguration
require_once __DIR__ . '/config/database.php';

// Ladda .env-filen för API-nyckel
function loadEnv($path) {
    if (!file_exists($path)) {
        die("Error: .env file not found at $path\n");
    }
    
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $env = [];
    
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        
        list($key, $value) = explode('=', $line, 2);
        $key = trim($key);
        $value = trim($value);
        $value = trim($value, '"\'');
        
        $env[$key] = $value;
    }
    
    return $env;
}

// Läs .env
$env = loadEnv(__DIR__ . '/.env');
$SCF_API_KEY = $env['SCF_LICENSE_API_KEY'] ?? null;

if (!$SCF_API_KEY) {
    die("Error: SCF_LICENSE_API_KEY not found in .env file\n");
}

// API konfiguration
define('SCF_API_BASE', 'https://licens.scf.se/api/1.0');
define('LICENSE_YEAR', 2026);
define('BATCH_SIZE', 25); // Max 25 UCI IDs per API-anrop

// Loggfil
$logFile = __DIR__ . '/logs/license_sync_' . date('Y-m-d_His') . '.log';
if (!is_dir(__DIR__ . '/logs')) {
    mkdir(__DIR__ . '/logs', 0755, true);
}

/**
 * Logga meddelande
 */
function logMessage($message, $level = 'INFO') {
    global $logFile;
    $timestamp = date('Y-m-d H:i:s');
    $logLine = "[$timestamp] [$level] $message\n";
    file_put_contents($logFile, $logLine, FILE_APPEND);
    echo $logLine;
}

/**
 * Gör API-anrop till SCF License Portal
 */
function callSCFAPI($endpoint, $params) {
    global $SCF_API_KEY;
    
    $url = SCF_API_BASE . $endpoint . '?' . http_build_query($params);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $SCF_API_KEY
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if (curl_errno($ch)) {
        $error = curl_error($ch);
        curl_close($ch);
        throw new Exception("cURL error: $error");
    }
    
    curl_close($ch);
    
    if ($httpCode !== 200) {
        throw new Exception("API returned HTTP $httpCode: $response");
    }
    
    $data = json_decode($response, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Failed to parse JSON response: " . json_last_error_msg());
    }
    
    return $data;
}

/**
 * Hämta licenser via UCI ID
 */
function getLicensesByUCIID($uciIds) {
    if (empty($uciIds)) {
        return [];
    }
    
    $params = [
        'year' => LICENSE_YEAR,
        'uciids' => implode(',', $uciIds)
    ];
    
    try {
        return callSCFAPI('/ucilicenselookup', $params);
    } catch (Exception $e) {
        logMessage("API error for UCI IDs [" . implode(',', $uciIds) . "]: " . $e->getMessage(), 'ERROR');
        return [];
    }
}

/**
 * Hämta licens via namn/kön/födelsedatum
 */
function getLicenseByName($firstName, $lastName, $gender, $birthdate = null) {
    $params = [
        'year' => LICENSE_YEAR,
        'firstname' => $firstName,
        'lastname' => $lastName,
        'gender' => $gender
    ];
    
    if ($birthdate) {
        $params['birthdate'] = $birthdate;
    }
    
    try {
        return callSCFAPI('/licenselookup', $params);
    } catch (Exception $e) {
        logMessage("API error for $firstName $lastName: " . $e->getMessage(), 'ERROR');
        return [];
    }
}

/**
 * Uppdatera rider med licensinformation
 */
function updateRiderLicense($pdo, $riderId, $licenseData) {
    // Anpassa dessa fält baserat på din faktiska databasstruktur
    $stmt = $pdo->prepare("
        UPDATE riders 
        SET 
            license_2026 = ?,
            license_type = ?,
            license_valid = 1,
            license_updated = NOW()
        WHERE id = ?
    ");
    
    $licenseNumber = $licenseData['license_number'] ?? null;
    $licenseType = $licenseData['license_type'] ?? 'unknown';
    
    return $stmt->execute([$licenseNumber, $licenseType, $riderId]);
}

/**
 * Skapa ny rider från licensinformation
 */
function createRiderFromLicense($pdo, $licenseData) {
    // Anpassa dessa fält baserat på din faktiska databasstruktur
    $stmt = $pdo->prepare("
        INSERT INTO riders (
            uci_id,
            first_name,
            last_name,
            gender,
            birthdate,
            club,
            license_2026,
            license_type,
            license_valid,
            license_updated,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, NOW(), NOW())
    ");
    
    return $stmt->execute([
        $licenseData['uci_id'] ?? null,
        $licenseData['first_name'] ?? '',
        $licenseData['last_name'] ?? '',
        $licenseData['gender'] ?? '',
        $licenseData['birthdate'] ?? null,
        $licenseData['club'] ?? '',
        $licenseData['license_number'] ?? null,
        $licenseData['license_type'] ?? 'unknown'
    ]);
}

// =============================================================================
// HUVUDLOGIK
// =============================================================================

logMessage("=== TheHUB License Sync Start ===");
logMessage("License year: " . LICENSE_YEAR);
logMessage("Batch size: " . BATCH_SIZE);

try {
    // Hämta alla riders med UCI ID
    $stmt = $pdo->prepare("
        SELECT id, uci_id, first_name, last_name, gender, birthdate
        FROM riders 
        WHERE uci_id IS NOT NULL AND uci_id != ''
        ORDER BY id
    ");
    $stmt->execute();
    $riders = $stmt->fetchAll();
    
    logMessage("Found " . count($riders) . " riders with UCI ID");
    
    // Statistik
    $stats = [
        'total' => count($riders),
        'updated' => 0,
        'failed' => 0,
        'skipped' => 0,
        'new_riders' => 0
    ];
    
    // Bearbeta i batchar
    $batches = array_chunk($riders, BATCH_SIZE);
    logMessage("Processing in " . count($batches) . " batches");
    
    foreach ($batches as $batchIndex => $batch) {
        logMessage("Processing batch " . ($batchIndex + 1) . "/" . count($batches));
        
        // Samla UCI IDs för denna batch
        $uciIds = array_map(function($rider) {
            return $rider['uci_id'];
        }, $batch);
        
        // Hämta licenser från API
        $licenses = getLicensesByUCIID($uciIds);
        
        if (empty($licenses)) {
            logMessage("No license data returned for batch " . ($batchIndex + 1), 'WARNING');
            $stats['skipped'] += count($batch);
            continue;
        }
        
        // Skapa uppslagstabell för snabbare matchning
        $licenseLookup = [];
        foreach ($licenses as $license) {
            if (isset($license['uci_id'])) {
                $licenseLookup[$license['uci_id']] = $license;
            }
        }
        
        // Uppdatera varje rider i batchen
        foreach ($batch as $rider) {
            $uciId = $rider['uci_id'];
            
            if (isset($licenseLookup[$uciId])) {
                $licenseData = $licenseLookup[$uciId];
                
                try {
                    updateRiderLicense($pdo, $rider['id'], $licenseData);
                    $stats['updated']++;
                    logMessage("Updated rider {$rider['first_name']} {$rider['last_name']} (UCI: $uciId)");
                } catch (Exception $e) {
                    $stats['failed']++;
                    logMessage("Failed to update rider ID {$rider['id']}: " . $e->getMessage(), 'ERROR');
                }
            } else {
                $stats['skipped']++;
                logMessage("No license found for {$rider['first_name']} {$rider['last_name']} (UCI: $uciId)", 'WARNING');
            }
        }
        
        // Kort paus mellan batchar för att inte överbelasta API
        if ($batchIndex < count($batches) - 1) {
            sleep(1);
        }
    }
    
    // Logga slutstatistik
    logMessage("=== Sync Completed ===");
    logMessage("Total riders: {$stats['total']}");
    logMessage("Updated: {$stats['updated']}");
    logMessage("Failed: {$stats['failed']}");
    logMessage("Skipped: {$stats['skipped']}");
    logMessage("New riders created: {$stats['new_riders']}");
    logMessage("Log file: $logFile");
    
} catch (Exception $e) {
    logMessage("Fatal error: " . $e->getMessage(), 'ERROR');
    exit(1);
}

logMessage("=== TheHUB License Sync End ===");
?>
