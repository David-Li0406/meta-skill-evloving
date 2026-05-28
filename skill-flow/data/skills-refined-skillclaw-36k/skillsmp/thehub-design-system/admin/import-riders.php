<?php
// CRITICAL: Show ALL errors for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('log_errors', 1);

// Try to catch fatal errors
register_shutdown_function(function() {
 $error = error_get_last();
 if ($error !== null && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
 echo"<h1>Fatal Error Detected:</h1>";
 echo"<pre class='gs-pre-error'>";
 echo"Type:" . $error['type'] ."\n";
 echo"Message:" . htmlspecialchars($error['message']) ."\n";
 echo"File:" . $error['file'] ."\n";
 echo"Line:" . $error['line'];
 echo"</pre>";
 }
});

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/helpers.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$stats = null;
$errors = [];
$skippedRows = [];
$columnMappings = [];

/**
 * Normalize string for comparison (for UCI ID lookup)
 */
function normalizeStringForImportSearch($str) {
    $str = mb_strtolower(trim($str), 'UTF-8');
    $str = preg_replace('/[åä]/u', 'a', $str);
    $str = preg_replace('/[ö]/u', 'o', $str);
    $str = preg_replace('/[é]/u', 'e', $str);
    $str = preg_replace('/[^a-z0-9]/u', '', $str);
    return $str;
}

/**
 * Parse Swedish personnummer (10 or 12 digits) and extract birth year
 * Formats:
 * - 12 digits: YYYYMMDDXXXX or YYYYMMDD-XXXX → extract YYYY
 * - 10 digits: YYMMDDXXXX or YYMMDD-XXXX → convert YY to YYYY
 * - Just year: YYYY → return as-is
 * @param string $pnr Personnummer string
 * @return int|null Birth year (4 digits) or null if parsing failed
 */
function parsePersonnummer($pnr) {
    if (empty($pnr)) {
        return null;
    }

    // Remove whitespace, dashes, and plus signs
    $pnr = preg_replace('/[\s\-\+]/', '', trim($pnr));

    // If it's already just a 4-digit year, return it
    if (preg_match('/^\d{4}$/', $pnr)) {
        $year = (int)$pnr;
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 12 digits: YYYYMMDDXXXX
    if (preg_match('/^(\d{4})\d{8}$/', $pnr, $matches)) {
        $year = (int)$matches[1];
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 10 digits: YYMMDDXXXX
    if (preg_match('/^(\d{2})\d{8}$/', $pnr, $matches)) {
        $yy = (int)$matches[1];
        $currentYear = (int)date('Y');
        $currentCentury = (int)floor($currentYear / 100) * 100;

        // Determine century: if YY > current year's last 2 digits, it's previous century
        if ($yy > ($currentYear % 100)) {
            $year = $currentCentury - 100 + $yy;
        } else {
            $year = $currentCentury + $yy;
        }

        return $year;
    }

    // 8 digits without last 4: YYYYMMDD
    if (preg_match('/^(\d{4})\d{4}$/', $pnr, $matches)) {
        $year = (int)$matches[1];
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 6 digits: YYMMDD
    if (preg_match('/^(\d{2})\d{4}$/', $pnr, $matches)) {
        $yy = (int)$matches[1];
        $currentYear = (int)date('Y');
        $currentCentury = (int)floor($currentYear / 100) * 100;

        if ($yy > ($currentYear % 100)) {
            $year = $currentCentury - 100 + $yy;
        } else {
            $year = $currentCentury + $yy;
        }

        return $year;
    }

    return null;
}

/**
 * Find rider in database to get UCI ID (license_number)
 */
function findRiderForUciIdImport($db, $firstname, $lastname, $club, $birthYear = null) {
    $normFirstname = normalizeStringForImportSearch($firstname);
    $normLastname = normalizeStringForImportSearch($lastname);
    $normClub = normalizeStringForImportSearch($club);

    // Strategy 1: Exact match with birth year
    if ($birthYear) {
        try {
            $riders = $db->getAll("
                SELECT r.id, r.firstname, r.lastname, r.license_number,
                    r.birth_year, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE LOWER(r.firstname) = ?
                    AND LOWER(r.lastname) = ?
                    AND r.birth_year = ?
                    AND r.license_number IS NOT NULL
                    AND r.license_number != ''
                    AND r.license_number NOT LIKE 'SWE-%'
                ORDER BY r.license_year DESC
                LIMIT 1
            ", [strtolower($firstname), strtolower($lastname), $birthYear]);

            if (!empty($riders)) {
                return $riders[0]['license_number'];
            }
        } catch (Exception $e) {}
    }

    // Strategy 2: Exact match with club
    if (!empty($club)) {
        try {
            $riders = $db->getAll("
                SELECT r.id, r.firstname, r.lastname, r.license_number,
                    r.birth_year, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE LOWER(r.firstname) = ?
                    AND LOWER(r.lastname) = ?
                    AND LOWER(c.name) LIKE ?
                    AND r.license_number IS NOT NULL
                    AND r.license_number != ''
                    AND r.license_number NOT LIKE 'SWE-%'
                ORDER BY r.license_year DESC
                LIMIT 1
            ", [strtolower($firstname), strtolower($lastname), '%' . strtolower($club) . '%']);

            if (!empty($riders)) {
                return $riders[0]['license_number'];
            }
        } catch (Exception $e) {}
    }

    // Strategy 3: Exact name match (any club)
    try {
        $riders = $db->getAll("
            SELECT r.id, r.firstname, r.lastname, r.license_number,
                r.birth_year, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE LOWER(r.firstname) = ?
                AND LOWER(r.lastname) = ?
                AND r.license_number IS NOT NULL
                AND r.license_number != ''
                AND r.license_number NOT LIKE 'SWE-%'
            ORDER BY r.license_year DESC
            LIMIT 1
        ", [strtolower($firstname), strtolower($lastname)]);

        if (!empty($riders)) {
            return $riders[0]['license_number'];
        }
    } catch (Exception $e) {}

    // Strategy 4: Fuzzy match (normalized names)
    try {
        $riders = $db->getAll("
            SELECT r.id, r.firstname, r.lastname, r.license_number,
                r.birth_year, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.license_number IS NOT NULL
                AND r.license_number != ''
                AND r.license_number NOT LIKE 'SWE-%'
            ORDER BY r.license_year DESC
            LIMIT 500
        ", []);

        foreach ($riders as $rider) {
            $riderNormFirst = normalizeStringForImportSearch($rider['firstname']);
            $riderNormLast = normalizeStringForImportSearch($rider['lastname']);

            if ($riderNormFirst === $normFirstname && $riderNormLast === $normLastname) {
                // Extra validation if birth year available
                if ($birthYear && $rider['birth_year'] && $rider['birth_year'] != $birthYear) {
                    continue; // Different birth year, skip
                }
                return $rider['license_number'];
            }
        }
    } catch (Exception $e) {}

    return null;
}

/**
 * Suggest license category based on birth year and gender
 * Swedish cycling categories: Herrar, Damer, Herrar Juniorer, Damer Juniorer, etc.
 */
function suggestLicenseCategory($birthYear, $gender) {
    $currentYear = (int)date('Y');
    $age = $currentYear - $birthYear;

    // Normalize gender
    $gender = strtolower(trim($gender));
    $isFemale = in_array($gender, ['f', 'female', 'kvinna', 'dam', 'damer', 'w', 'women']);

    // Determine category based on age
    if ($age >= 19) {
        return $isFemale ? 'Damer' : 'Herrar';
    } elseif ($age >= 17) {
        return $isFemale ? 'Damer Juniorer' : 'Herrar Juniorer';
    } elseif ($age >= 15) {
        return $isFemale ? 'Flickor 15-16' : 'Pojkar 15-16';
    } elseif ($age >= 13) {
        return $isFemale ? 'Flickor 13-14' : 'Pojkar 13-14';
    } else {
        return $isFemale ? 'Flickor' : 'Pojkar';
    }
}

// Handle confirmed import from preview
if (isset($_GET['do_import']) && isset($_SESSION['import_riders_confirmed']) && $_SESSION['import_riders_confirmed']) {
    $uploaded = $_SESSION['import_riders_file'] ?? null;

    if ($uploaded && file_exists($uploaded)) {
        $seasonYear = $_SESSION['import_riders_season'] ?? (int)date('Y');
        try {
            $result = importRidersFromCSV($uploaded, $db, $seasonYear);

            $stats = $result['stats'];
            $errors = $result['errors'];
            $skippedRows = $result['skipped_rows'] ?? [];
            $columnMappings = $result['column_mappings'] ?? [];

            if ($stats['success'] > 0 || $stats['updated'] > 0) {
                $message = "Import klar! {$stats['success']} nya, {$stats['updated']} uppdaterade.";
                if ($stats['duplicates'] > 0) {
                    $message .= " {$stats['duplicates']} dubletter borttagna.";
                }
                $messageType = 'success';
            } else {
                $message = "Ingen data importerades. Kontrollera filformatet.";
                $messageType = 'error';
            }
        } catch (Exception $e) {
            $message = 'Import misslyckades: ' . $e->getMessage();
            $messageType = 'error';
        }

        @unlink($uploaded);
    }

    // Clean up session
    unset($_SESSION['import_riders_file']);
    unset($_SESSION['import_riders_season']);
    unset($_SESSION['import_riders_create_missing']);
    unset($_SESSION['import_riders_confirmed']);
}

// Handle CSV/Excel upload - Go to preview first
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['import_file'])) {
 // Validate CSRF token
 checkCsrf();

 $file = $_FILES['import_file'];

 // Validate file
 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Filuppladdning misslyckades';
 $messageType = 'error';
 } elseif ($file['size'] > MAX_UPLOAD_SIZE) {
 $message = 'Filen är för stor (max ' . (MAX_UPLOAD_SIZE / 1024 / 1024) . 'MB)';
 $messageType = 'error';
 } else {
 $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

 if (!in_array($extension, ['csv', 'xlsx', 'xls'])) {
  $message = 'Ogiltigt filformat. Tillåtna: CSV, XLSX, XLS';
  $messageType = 'error';
 } else {
  // Save file and redirect to preview
  $uploaded = UPLOADS_PATH . '/' . time() . '_' . basename($file['name']);

  if (move_uploaded_file($file['tmp_name'], $uploaded)) {
  if ($extension !== 'csv') {
   $message = 'Excel-filer stöds inte än. Använd CSV-format istället.';
   $messageType = 'warning';
   @unlink($uploaded);
   goto skip_import;
  }

  // Store in session and redirect to preview
  $_SESSION['import_riders_file'] = $uploaded;
  $_SESSION['import_riders_season'] = (int)($_POST['season_year'] ?? date('Y'));
  $_SESSION['import_riders_create_missing'] = isset($_POST['create_missing']);
  $_SESSION['import_riders_confirmed'] = false;

  header('Location: /admin/import/riders/preview');
  exit;

  } else {
  $message = 'Kunde inte ladda upp filen';
  $messageType = 'error';
  }
 }
 }

 skip_import:
}

/**
 * Ensure file is UTF-8 encoded (convert from Windows-1252 if needed)
 */
function ensureUTF8ForImport($filepath) {
 $content = file_get_contents($filepath);

 // Remove BOM if present
 $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);

 // Check if already valid UTF-8
 if (mb_check_encoding($content, 'UTF-8')) {
  // Look for Windows-1252 byte patterns that aren't proper UTF-8
  if (preg_match('/[\xC0-\xFF]/', $content) && !preg_match('/[\xC0-\xFF][\x80-\xBF]/', $content)) {
   $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
   file_put_contents($filepath, $content);
   return;
  }
  // Check for corrupted Swedish words
  if (preg_match('/F.rnamn|f.rnamn|.delseår|.delse.r/u', $content) &&
   !preg_match('/Förnamn|förnamn|Födelseår|födelseår/u', $content)) {
   $content = file_get_contents($filepath);
   $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
   file_put_contents($filepath, $content);
   return;
  }
  file_put_contents($filepath, $content);
  return;
 }

 // Not valid UTF-8, assume Windows-1252
 $content = mb_convert_encoding($content, 'UTF-8', 'Windows-1252');
 file_put_contents($filepath, $content);
}

/**
 * Import riders from CSV file
 */
function importRidersFromCSV($filepath, $db, $seasonYear = null) {
 // Include club membership functions
 require_once __DIR__ . '/../includes/club-membership.php';
 // Include smart club matching functions
 require_once __DIR__ . '/../includes/club-matching.php';

 // Default to current year if not specified
 if ($seasonYear === null) {
  $seasonYear = (int)date('Y');
 }
 $stats = [
 'total' => 0,
 'success' => 0,
 'updated' => 0,
 'skipped' => 0,
 'failed' => 0,
 'duplicates' => 0
 ];
 $errors = [];
 $skippedRows = []; // Detailed list of skipped rows
 $seenInThisImport = []; // Track riders in this import to detect duplicates
 $columnMappings = []; // Track original -> mapped column names for debugging

 // Ensure UTF-8 encoding
 ensureUTF8ForImport($filepath);

 if (($handle = fopen($filepath, 'r')) === false) {
 throw new Exception('Kunde inte öppna filen');
 }

 // Auto-detect delimiter (comma or semicolon)
 $firstLine = fgets($handle);
 rewind($handle);
 $delimiter = (substr_count($firstLine, ';') > substr_count($firstLine, ',')) ? ';' : ',';

 // Read header row with detected delimiter
 $originalHeader = fgetcsv($handle, 1000, $delimiter);

 if (!$originalHeader) {
 fclose($handle);
 throw new Exception('Tom fil eller ogiltigt format');
 }

 // Store original header for debugging
 $originalHeaderCopy = $originalHeader;

 // Expected columns: firstname, lastname, birth_year, gender, club, license_number, email, phone, city
 $expectedColumns = ['firstname', 'lastname', 'birth_year', 'gender', 'club'];

 // Normalize header - accept multiple variants of column names
 $header = [];
 foreach ($originalHeader as $originalCol) {
 // Use mb_strtolower for proper UTF-8 handling (Swedish characters Ö, Å, Ä)
 $col = mb_strtolower(trim($originalCol), 'UTF-8');
 $col = str_replace([' ', '-', '_'], '', $col); // Remove spaces, hyphens, underscores

 // Map various column name variants to standard names
 $mappings = [
  // Name fields
  'förnamn' => 'firstname',
  'fornamn' => 'firstname',
  'firstname' => 'firstname',
  'fname' => 'firstname',
  'givenname' => 'firstname',
  'first' => 'firstname',

  'efternamn' => 'lastname',
  'lastname' => 'lastname',
  'surname' => 'lastname',
  'familyname' => 'lastname',
  'lname' => 'lastname',
  'last' => 'lastname',

  // Full name (will be split into firstname/lastname later)
  'namn' => 'fullname',
  'name' => 'fullname',
  'fullname' => 'fullname',
  'fullnamn' => 'fullname',
  'åkare' => 'fullname',
  'akare' => 'fullname',
  'rider' => 'fullname',
  'deltagare' => 'fullname',
  'participant' => 'fullname',

  // Birth year / age
  'födelseår' => 'birthyear',
  'fodelsear' => 'birthyear',
  'birthyear' => 'birthyear',
  'född' => 'birthyear',
  'fodd' => 'birthyear',
  'year' => 'birthyear',
  'år' => 'birthyear',
  'ar' => 'birthyear',
  'ålder' => 'birthyear',
  'alder' => 'birthyear',
  'age' => 'birthyear',
  'födelsedatum' => 'birthdate',
  'fodelsedatum' => 'birthdate',
  'birthdate' => 'birthdate',
  'dateofbirth' => 'birthdate',
  'dob' => 'birthdate',
  // Note: personnummer column is parsed to extract birth_year only
  // The personnummer itself is NOT stored in the database
  'personnummer' => 'personnummer',
  'pnr' => 'personnummer',
  'ssn' => 'personnummer',

  // Gender
  'kön' => 'gender',
  'kon' => 'gender',
  'gender' => 'gender',
  'sex' => 'gender',

  // Club
  'klubb' => 'club',
  'club' => 'club',
  'klubbnamn' => 'club',
  'clubname' => 'club',
  'team' => 'club',
  'lag' => 'club',
  'förening' => 'club',
  'forening' => 'club',
  'huvudförening' => 'club',
  'huvudforening' => 'club',
  'organisation' => 'club',
  'organization' => 'club',
  'org' => 'club',

  // District/Region
  'distrikt' => 'district',
  'district' => 'district',
  'region' => 'district',
  'län' => 'district',
  'lan' => 'district',

  // Nationality
  'land' => 'nationality',
  'nationalitet' => 'nationality',
  'nationality' => 'nationality',
  'country' => 'nationality',
  'nation' => 'nationality',

  // License
  'licensnummer' => 'licensenumber',
  'licensnr' => 'licensenumber',
  'licensenumber' => 'licensenumber',
  'licencenumber' => 'licensenumber',
  'uciid' => 'licensenumber',
  'ucikod' => 'licensenumber',
  'uci' => 'licensenumber',
  'sweid' => 'licensenumber',
  'licens' => 'licensenumber',
  'license' => 'licensenumber',

  // Discipline columns (SCF export has separate columns for each)
  'road' => 'discipline_road',
  'track' => 'discipline_track',
  'bmx' => 'discipline_bmx',
  'cx' => 'discipline_cx',
  'trial' => 'discipline_trial',
  'para' => 'discipline_para',
  'mtb' => 'discipline_mtb',
  'ecycling' => 'discipline_ecycling',
  'gravel' => 'discipline_gravel',

  'licenstyp' => 'licensetype',
  'licensetype' => 'licensetype',
  'licensetyp' => 'licensetype',
  'type' => 'licensetype',

  'licenskategori' => 'licensecategory',
  'licensecategory' => 'licensecategory',
  'kategori' => 'licensecategory',
  'category' => 'licensecategory',

  'licensgiltigtill' => 'licensevaliduntil',
  'licensevaliduntil' => 'licensevaliduntil',
  'giltigtill' => 'licensevaliduntil',
  'validuntil' => 'licensevaliduntil',
  'expiry' => 'licensevaliduntil',

  // License year
  'licensår' => 'licenseyear',
  'licensar' => 'licenseyear',
  'licensyear' => 'licenseyear',
  'licenseyear' => 'licenseyear',
  'licyear' => 'licenseyear',

  // Discipline
  'gren' => 'discipline',
  'discipline' => 'discipline',
  'sport' => 'discipline',

  // Contact info
  'epost' => 'email',
  'email' => 'email',
  'mail' => 'email',
  'epostadress' => 'email',
  'emailaddress' => 'email',

  'telefon' => 'phone',
  'phone' => 'phone',
  'tel' => 'phone',
  'mobil' => 'phone',
  'mobile' => 'phone',

  'stad' => 'city',
  'city' => 'city',
  'ort' => 'city',
  'location' => 'city',

  // Notes
  'anteckningar' => 'notes',
  'notes' => 'notes',
  'kommentar' => 'notes',
  'comment' => 'notes',
 ];

 $mappedCol = $mappings[$col] ?? $col;
 $header[] = $mappedCol;
 $columnMappings[] = ['original' => trim($originalCol), 'mapped' => $mappedCol];
 }

 // Cache for club lookups
 $clubCache = [];

 $lineNumber = 1;

 while (($row = fgetcsv($handle, 1000, $delimiter)) !== false) {
 $lineNumber++;
 $stats['total']++;

 // Map row to associative array
 // Handle case where row has different number of columns than header
 if (count($row) !== count($header)) {
  // Pad row with empty strings if too short, or trim if too long
  if (count($row) < count($header)) {
   $row = array_pad($row, count($header), '');
  } else {
   $row = array_slice($row, 0, count($header));
  }
 }
 $data = array_combine($header, $row);

 // Handle fullname column - split into firstname and lastname
 if (!empty($data['fullname']) && (empty($data['firstname']) || empty($data['lastname']))) {
  $fullname = trim($data['fullname']);
  // Try to split on comma first (Lastname, Firstname format)
  if (strpos($fullname, ',') !== false) {
   $parts = array_map('trim', explode(',', $fullname, 2));
   if (count($parts) >= 2) {
    $data['lastname'] = $parts[0];
    $data['firstname'] = $parts[1];
   }
  } else {
   // Split on space (Firstname Lastname format)
   $parts = preg_split('/\s+/', $fullname);
   if (count($parts) >= 2) {
    $data['firstname'] = $parts[0];
    $data['lastname'] = implode(' ', array_slice($parts, 1));
   } elseif (count($parts) === 1) {
    // Only one word - could be either, put in lastname
    $data['lastname'] = $parts[0];
    $data['firstname'] = '';
   }
  }
 }

 // Validate required fields
 if (empty($data['firstname']) || empty($data['lastname'])) {
  $stats['skipped']++;
  $errors[] ="Rad {$lineNumber}: Saknar förnamn eller efternamn";
  $skippedRows[] = [
  'row' => $lineNumber,
  'name' => trim(($data['firstname'] ?? '') . ' ' . ($data['lastname'] ?? '')),
  'reason' => 'Saknar förnamn eller efternamn',
  'type' => 'missing_fields'
  ];
  continue;
 }

 try {
  // Extract birth_year from personnummer if provided
  // Note: personnummer is ONLY used to extract birth_year - it is NOT stored in DB
  $birthYear = null;
  if (!empty($data['personnummer'])) {
  $birthYear = parsePersonnummer($data['personnummer']);
  }
  // Fall back to birthyear column if no personnummer or parsing failed
  // Also try to parse as personnummer (in case someone puts "19901231" or "9012310123" in birthyear column)
  if (!$birthYear && !empty($data['birthyear'])) {
    $birthYearValue = trim($data['birthyear']);
    // First try to parse as personnummer (handles 10/12 digit formats)
    $birthYear = parsePersonnummer($birthYearValue);
    // If that fails and it looks like a 4-digit year, use it directly
    if (!$birthYear && preg_match('/^\d{4}$/', $birthYearValue)) {
      $birthYear = (int)$birthYearValue;
    }
  }
  // Fall back to birthdate column - extract year from date or personnummer
  // NOTE: SCF exports use "Födelsedatum" column but it contains personnummer (YYYYMMDD-XXXX)
  if (!$birthYear && !empty($data['birthdate'])) {
    $dateStr = trim($data['birthdate']);

    // FIRST: Try to parse as personnummer (YYYYMMDD-XXXX or YYMMDD-XXXX)
    // This handles SCF format where "Födelsedatum" contains personnummer
    $birthYear = parsePersonnummer($dateStr);

    // If personnummer parsing failed, try date formats
    if (!$birthYear) {
      if (preg_match('/^(\d{4})[-\/](\d{2})[-\/](\d{2})$/', $dateStr, $m)) {
        // YYYY-MM-DD or YYYY/MM/DD (strict: must have 3 parts)
        $birthYear = (int)$m[1];
      } elseif (preg_match('/^(\d{2})[-\/](\d{2})[-\/](\d{4})$/', $dateStr, $m)) {
        // DD-MM-YYYY or DD/MM/YYYY (strict: must have 3 parts, year at end)
        $birthYear = (int)$m[3];
      } elseif (preg_match('/^(\d{4})$/', $dateStr, $m)) {
        // Just year
        $birthYear = (int)$m[1];
      }
    }
  }

  // Prepare rider data
  // Normalize gender: Woman/Female/Kvinna → F, Man/Male/Herr → M
  // Also check licensecategory for "Men"/"Women" if gender is not explicitly set
  $genderRaw = strtolower(trim($data['gender'] ?? ''));
  $gender = null;

  if (in_array($genderRaw, ['woman', 'female', 'kvinna', 'dam', 'f', 'w'])) {
  $gender = 'F';
  } elseif (in_array($genderRaw, ['man', 'male', 'herr', 'm'])) {
  $gender = 'M';
  } elseif (!empty($genderRaw)) {
  $gender = strtoupper(substr($genderRaw, 0, 1)); // Fallback: first letter
  }

  // If gender still not set, try to extract from license category (SCF format: "Men Elite", "Women Junior", etc.)
  if (!$gender && !empty($data['licensecategory'])) {
  $categoryLower = strtolower($data['licensecategory']);
  if (strpos($categoryLower, 'women') !== false || strpos($categoryLower, 'dam') !== false ||
    strpos($categoryLower, 'flickor') !== false || strpos($categoryLower, 'female') !== false) {
    $gender = 'F';
  } elseif (strpos($categoryLower, 'men') !== false || strpos($categoryLower, 'herr') !== false ||
       strpos($categoryLower, 'pojk') !== false || strpos($categoryLower, 'male') !== false) {
    $gender = 'M';
  }
  }

  // Default to M if still not determined
  if (!$gender) {
  $gender = 'M';
  }

  $riderData = [
  'firstname' => trim($data['firstname']),
  'lastname' => trim($data['lastname']),
  'birth_year' => $birthYear,
  'gender' => $gender,
  'license_number' => !empty($data['licensenumber']) ? trim($data['licensenumber']) : null,
  'email' => !empty($data['email']) ? trim($data['email']) : null,
  'active' => 1
  ];

  // Add district if provided (from 'district' or 'city' column)
  if (!empty($data['district'])) {
    $riderData['district'] = trim($data['district']);
  } elseif (!empty($data['city'])) {
    $riderData['district'] = trim($data['city']);
  }

  // Add nationality if provided
  if (!empty($data['nationality'])) {
    $nat = strtoupper(trim($data['nationality']));
    // Convert common country names to ISO codes
    $nationalityMap = [
      'SVERIGE' => 'SWE', 'SWEDEN' => 'SWE', 'SE' => 'SWE',
      'NORGE' => 'NOR', 'NORWAY' => 'NOR', 'NO' => 'NOR',
      'DANMARK' => 'DEN', 'DENMARK' => 'DEN', 'DK' => 'DEN',
      'FINLAND' => 'FIN', 'FI' => 'FIN',
      'TYSKLAND' => 'GER', 'GERMANY' => 'GER', 'DE' => 'GER',
      'STORBRITANNIEN' => 'GBR', 'UK' => 'GBR', 'GB' => 'GBR', 'GREAT BRITAIN' => 'GBR',
      'USA' => 'USA', 'UNITED STATES' => 'USA', 'US' => 'USA',
    ];
    $riderData['nationality'] = $nationalityMap[$nat] ?? (strlen($nat) === 3 ? $nat : 'SWE');
  }

  // Add new license fields
  $riderData['license_type'] = !empty($data['licensetype']) ? trim($data['licensetype']) : null;
  $riderData['license_valid_until'] = !empty($data['licensevaliduntil']) ? trim($data['licensevaliduntil']) : null;
  $riderData['license_year'] = !empty($data['licenseyear']) ? (int)$data['licenseyear'] : null;

  // Handle disciplines - either single column or multiple SCF columns
  $disciplines = [];
  if (!empty($data['discipline'])) {
    $disciplines[] = trim($data['discipline']);
  }
  // Check individual discipline columns (SCF export format)
  $disciplineColumns = ['discipline_road', 'discipline_track', 'discipline_bmx', 'discipline_cx',
             'discipline_trial', 'discipline_para', 'discipline_mtb', 'discipline_ecycling', 'discipline_gravel'];
  $disciplineNames = ['Road' => 'LVG', 'Track' => 'BANA', 'BMX' => 'BMX', 'CX' => 'CX',
            'Trial' => 'TRIAL', 'Para' => 'PARA', 'MTB' => 'MTB', 'E-cycling' => 'E-CYCLING', 'Gravel' => 'GRAVEL'];
  foreach ($disciplineColumns as $col) {
    if (!empty($data[$col]) && strtolower(trim($data[$col])) !== '' && strtolower(trim($data[$col])) !== 'nej' && strtolower(trim($data[$col])) !== 'no') {
      $discName = str_replace('discipline_', '', $col);
      $discName = ucfirst($discName);
      if ($discName === 'Ecycling') $discName = 'E-cycling';
      $disciplines[] = $disciplineNames[$discName] ?? strtoupper($discName);
    }
  }
  $disciplines = array_unique(array_filter($disciplines));

  if (!empty($disciplines)) {
    $riderData['discipline'] = implode(',', $disciplines); // Legacy single field
    $riderData['disciplines'] = json_encode(array_values($disciplines)); // New JSON field
  } else {
    $riderData['discipline'] = null;
    $riderData['disciplines'] = null;
  }

  // License category - use provided or auto-suggest
  if (!empty($data['licensecategory'])) {
  $riderData['license_category'] = trim($data['licensecategory']);
  } elseif ($birthYear && $gender) {
  // Auto-suggest license category based on age and gender
  $riderData['license_category'] = suggestLicenseCategory($birthYear, $gender);
  } else {
  $riderData['license_category'] = null;
  }

  // License number handling:
  // 1. Use from CSV if provided
  // 2. Otherwise search database for existing UCI ID
  // 3. As last resort, generate SWE-ID
  if (empty($riderData['license_number']) && !empty($data['licensenumber'])) {
  $riderData['license_number'] = trim($data['licensenumber']);
  }
  if (empty($riderData['license_number'])) {
  // Try to find existing UCI ID in database
  $clubName = $data['club'] ?? '';
  $foundUciId = findRiderForUciIdImport($db, $riderData['firstname'], $riderData['lastname'], $clubName, $riderData['birth_year']);
  if ($foundUciId) {
    $riderData['license_number'] = normalizeUciId($foundUciId);
    error_log("Import: Found UCI ID {$riderData['license_number']} for {$riderData['firstname']} {$riderData['lastname']}");
  } else {
    // Generate new SWE-ID as fallback
    $riderData['license_number'] = generateSweId($db);
  }
  }

  // Handle club - use smart matching (handles CK/Ck/Cykelklubben variants, case-insensitive)
  if (!empty($data['club'])) {
  $clubName = trim($data['club']);

  // Normalize for cache key to catch variants
  $normalizedClubName = normalizeClubName($clubName);
  $clubCacheKey = !empty($normalizedClubName) ? $normalizedClubName : strtolower($clubName);

  // Check cache first
  if (isset($clubCache[$clubCacheKey])) {
   $riderData['club_id'] = $clubCache[$clubCacheKey];
  } else {
   // Use smart matching from club-matching.php
   // Handles: case-insensitive, CK/Ck/Cykelklubben variants, fuzzy/typo matching
   $club = findClubByName($db, $clubName);

   if (!$club) {
   // Create new club with the original name from CSV
   $clubId = $db->insert('clubs', [
    'name' => $clubName,
    'active' => 1
   ]);
   $clubCache[$clubCacheKey] = $clubId;
   $riderData['club_id'] = $clubId;
   error_log("Import: Created new club '{$clubName}' with ID {$clubId}");
   } else {
   $clubCache[$clubCacheKey] = $club['id'];
   $riderData['club_id'] = $club['id'];
   error_log("Import: Matched '{$clubName}' to existing club '{$club['name']}' (ID: {$club['id']})");
   }
  }
  } else {
  $riderData['club_id'] = null;
  }

  // Check for duplicates within this import
  // Create unique key: firstname_lastname_birthyear OR original licensenumber (NOT auto-generated SWE-ID)
  $uniqueKey = '';
  // Use original license from data (before generateSweId() was called)
  $originalLicense = !empty($data['licensenumber']) ? trim($data['licensenumber']) : null;
  if ($originalLicense) {
  $uniqueKey = 'lic_' . strtolower($originalLicense);
  } else {
  // Use name + birth_year (this is the key for detecting duplicates without license)
  $uniqueKey = 'name_' . strtolower(trim($riderData['firstname'])) . '_' .
    strtolower(trim($riderData['lastname'])) . '_' .
    ($riderData['birth_year'] ?? '0');
  }

  if (isset($seenInThisImport[$uniqueKey])) {
  // This is a duplicate within the same import - skip it
  $stats['duplicates']++;
  $stats['skipped']++;
  $skippedRows[] = [
   'row' => $lineNumber,
   'name' => $riderData['firstname'] . ' ' . $riderData['lastname'],
   'license' => $riderData['license_number'] ?? '-',
   'reason' => 'Dublett (redan i denna import)',
   'type' => 'duplicate'
  ];
  error_log("Import: Skipped duplicate - {$riderData['firstname']} {$riderData['lastname']} (already in this import)");
  continue;
  }

  // Mark as seen in this import
  $seenInThisImport[$uniqueKey] = true;

  // Check if rider already exists (by license or name+birth_year)
  // Använder case-insensitive matchning för namn
  $existing = null;

  // 1. Försök matcha på licensnummer (exakt)
  if (!empty($riderData['license_number']) && strpos($riderData['license_number'], 'SWE-') !== 0) {
  $existing = $db->getRow(
  "SELECT id FROM riders WHERE license_number = ? LIMIT 1",
   [$riderData['license_number']]
  );
  }

  // 2. Försök matcha på namn + födelseår (case-insensitive)
  if (!$existing && $riderData['birth_year']) {
  $existing = $db->getRow(
  "SELECT id FROM riders WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?) AND birth_year = ? LIMIT 1",
   [$riderData['firstname'], $riderData['lastname'], $riderData['birth_year']]
  );
  }

  // 3. Försök matcha på namn endast (case-insensitive) om födelseår saknas
  if (!$existing && !$riderData['birth_year']) {
  $existing = $db->getRow(
  "SELECT id FROM riders WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?) LIMIT 1",
   [$riderData['firstname'], $riderData['lastname']]
  );
  }

  if ($existing) {
  // Update existing rider
  $db->update('riders', $riderData, 'id = ?', [$existing['id']]);
  $riderId = $existing['id'];
  $stats['updated']++;
  error_log("Import: Updated rider ID {$riderId} - {$riderData['firstname']} {$riderData['lastname']}");
  } else {
  // Insert new rider
  $riderId = $db->insert('riders', $riderData);
  if ($riderId && $riderId > 0) {
    $stats['success']++;
    error_log("Import: Inserted new rider ID {$riderId} - {$riderData['firstname']} {$riderData['lastname']} (active={$riderData['active']})");
  } else {
    $stats['failed']++;
    $errors[] = "Rad {$lineNumber}: Kunde inte spara {$riderData['firstname']} {$riderData['lastname']} till databasen";
    error_log("Import FAILED: Could not insert rider - {$riderData['firstname']} {$riderData['lastname']}");
  }
  }

  // Set club membership for the season year
  if ($riderId && $riderData['club_id']) {
  setRiderClubForYear($db, $riderId, $riderData['club_id'], $seasonYear);
  }

 } catch (Exception $e) {
  $stats['failed']++;
  $errors[] ="Rad {$lineNumber}:" . $e->getMessage();
  $skippedRows[] = [
  'row' => $lineNumber,
  'name' => trim(($data['firstname'] ?? '') . ' ' . ($data['lastname'] ?? '')),
  'license' => $data['licensenumber'] ?? '-',
  'reason' => 'Fel: ' . $e->getMessage(),
  'type' => 'error'
  ];
 }
 }

 fclose($handle);

 // VERIFICATION: Check that data was actually saved
 $verifyCount = $db->getRow("SELECT COUNT(*) as count FROM riders");
 $totalInDb = $verifyCount['count'] ?? 0;
 error_log("Import complete: {$stats['success']} new, {$stats['updated']} updated, {$stats['failed']} failed. Total riders in DB: {$totalInDb}");

 // Add verification count to stats
 $stats['total_in_db'] = $totalInDb;

 return [
 'stats' => $stats,
 'errors' => $errors,
 'skipped_rows' => $skippedRows,
 'column_mappings' => $columnMappings
 ];
}

// Page config for unified layout
$page_title = 'Importera Deltagare';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Deltagare']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

  <!-- Message -->
  <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
   <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
   <?= h($message) ?>
  </div>
  <?php endif; ?>

  <!-- Statistics -->
  <?php if ($stats): ?>
  <div class="admin-card mb-lg">
   <div class="admin-card-header">
   <h2>
    <i data-lucide="bar-chart"></i>
    Import-statistik
   </h2>
   </div>
   <div class="admin-card-body">
   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: var(--space-md);">
    <div class="admin-stat-card">
    <div class="admin-stat-icon" style="background: var(--color-bg-muted);">
     <i data-lucide="file-text"></i>
    </div>
    <div class="admin-stat-value"><?= number_format($stats['total']) ?></div>
    <div class="admin-stat-label">Totalt rader</div>
    </div>
    <div class="admin-stat-card">
    <div class="admin-stat-icon" style="background: rgba(97, 206, 112, 0.1); color: var(--color-success);">
     <i data-lucide="check-circle"></i>
    </div>
    <div class="admin-stat-value text-success"><?= number_format($stats['success']) ?></div>
    <div class="admin-stat-label">Nya</div>
    </div>
    <div class="admin-stat-card">
    <div class="admin-stat-icon" style="background: rgba(0, 74, 152, 0.1); color: var(--color-gs-blue);">
     <i data-lucide="refresh-cw"></i>
    </div>
    <div class="admin-stat-value" style="color: var(--color-gs-blue);"><?= number_format($stats['updated']) ?></div>
    <div class="admin-stat-label">Uppdaterade</div>
    </div>
    <div class="admin-stat-card">
    <div class="admin-stat-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--color-warning);">
     <i data-lucide="minus-circle"></i>
    </div>
    <div class="admin-stat-value" style="color: var(--color-warning);"><?= number_format($stats['skipped']) ?></div>
    <div class="admin-stat-label">Överhoppade</div>
    </div>
    <div class="admin-stat-card">
    <div class="admin-stat-icon" style="background: rgba(239, 68, 68, 0.1); color: var(--color-danger);">
     <i data-lucide="x-circle"></i>
    </div>
    <div class="admin-stat-value" style="color: var(--color-danger);"><?= number_format($stats['failed']) ?></div>
    <div class="admin-stat-label">Misslyckade</div>
    </div>
   </div>

   <!-- Column Mappings (debug info) -->
   <?php if (!empty($columnMappings)): ?>
    <details style="margin-top: var(--space-lg); padding-top: var(--space-lg); border-top: 1px solid var(--color-border);">
    <summary class="cursor-pointer flex items-center gap-sm" style="font-weight: 500; margin-bottom: var(--space-md);">
     <i data-lucide="columns"></i>
     Kolumnmappning (<?= count($columnMappings) ?> kolumner)
    </summary>
    <div class="admin-table-container" style="max-height: 300px; overflow-y: auto;">
     <table class="admin-table admin-table-sm">
     <thead>
      <tr>
      <th>Original kolumnnamn</th>
      <th>Mappat till</th>
      <th>Status</th>
      </tr>
     </thead>
     <tbody>
      <?php foreach ($columnMappings as $cm):
       $important = in_array($cm['mapped'], ['firstname', 'lastname', 'fullname', 'birthyear', 'gender', 'club', 'licensenumber']);
       $nameField = in_array($cm['mapped'], ['firstname', 'lastname', 'fullname']);
      ?>
      <tr>
       <td><code><?= htmlspecialchars($cm['original']) ?></code></td>
       <td>
       <?php if ($nameField): ?>
        <span class="admin-badge admin-badge-success"><?= htmlspecialchars($cm['mapped']) ?></span>
       <?php elseif ($important): ?>
        <span class="admin-badge admin-badge-info"><?= htmlspecialchars($cm['mapped']) ?></span>
       <?php else: ?>
        <span class="text-secondary"><?= htmlspecialchars($cm['mapped']) ?></span>
       <?php endif; ?>
       </td>
       <td>
       <?php if ($cm['original'] === $cm['mapped']): ?>
        <span class="text-secondary">Okänd kolumn</span>
       <?php elseif ($nameField): ?>
        <span class="text-success">Namn-fält</span>
       <?php else: ?>
        <span class="text-success">Mappat</span>
       <?php endif; ?>
       </td>
      </tr>
      <?php endforeach; ?>
     </tbody>
     </table>
    </div>
    <p class="text-secondary" style="font-size: 0.75rem; margin-top: var(--space-sm);">
     <strong>Tips:</strong> Om kolumner inte mappas korrekt, kontrollera att CSV-filen har rubriker som:
     Förnamn, Efternamn (eller Namn för fullständigt namn), Födelseår, Kön, Klubb, Licensnummer
    </p>
    </details>
   <?php endif; ?>

   <!-- Verification Section -->
   <?php if (isset($stats['total_in_db'])): ?>
    <div style="margin-top: var(--space-lg); padding-top: var(--space-lg); border-top: 1px solid var(--color-border);">
    <h3 class="flex items-center gap-sm" class="mb-md">
     <i data-lucide="database"></i>
     Verifiering
    </h3>
    <div class="alert alert-info" class="mb-md">
     <strong>Totalt i databasen:</strong> <?= number_format($stats['total_in_db']) ?> cyklister
    </div>
    <div style="display: flex; gap: var(--space-md);">
     <a href="/admin/riders.php" class="btn-admin btn-admin-primary">
     <i data-lucide="users"></i>
     Se alla deltagare
     </a>
     <a href="/admin/debug-database.php" class="btn-admin btn-admin-secondary">
     <i data-lucide="search"></i>
     Debug databas
     </a>
    </div>
    </div>
   <?php endif; ?>

   <!-- Skipped Rows Details -->
   <?php if (!empty($skippedRows)): ?>
    <div style="margin-top: var(--space-lg); padding-top: var(--space-lg); border-top: 1px solid var(--color-border);">
    <h3 class="flex items-center gap-sm" style="margin-bottom: var(--space-md); color: var(--color-warning);">
     <i data-lucide="alert-circle"></i>
     Överhoppade rader (<?= count($skippedRows) ?>)
    </h3>
    <div class="table-responsive">
     <table class="table">
     <thead>
      <tr>
      <th style="width: 80px;">Rad</th>
      <th>Namn</th>
      <th>Licens</th>
      <th>Anledning</th>
      <th style="width: 100px;">Typ</th>
      </tr>
     </thead>
     <tbody>
      <?php foreach (array_slice($skippedRows, 0, 100) as $skip): ?>
      <tr>
       <td><code style="background: var(--color-bg-muted); padding: 2px 6px; border-radius: var(--radius-sm);"><?= $skip['row'] ?></code></td>
       <td><?= h($skip['name']) ?></td>
       <td><code class="text-sm"><?= h($skip['license'] ?? '-') ?></code></td>
       <td class="text-secondary"><?= h($skip['reason']) ?></td>
       <td>
       <?php if ($skip['type'] === 'duplicate'): ?>
        <span class="badge badge-warning">Dublett</span>
       <?php elseif ($skip['type'] === 'missing_fields'): ?>
        <span class="badge badge-secondary">Saknar fält</span>
       <?php elseif ($skip['type'] === 'error'): ?>
        <span class="badge badge-danger">Fel</span>
       <?php endif; ?>
       </td>
      </tr>
      <?php endforeach; ?>
     </tbody>
     </table>
     <?php if (count($skippedRows) > 100): ?>
     <p class="text-sm text-secondary" style="margin-top: var(--space-sm); font-style: italic;">
      Visar första 100 av <?= count($skippedRows) ?> överhoppade rader
     </p>
     <?php endif; ?>
    </div>
    </div>
   <?php endif; ?>

   <?php if (!empty($errors)): ?>
    <div style="margin-top: var(--space-lg); padding-top: var(--space-lg); border-top: 1px solid var(--color-border);">
    <h3 class="flex items-center gap-sm" style="margin-bottom: var(--space-md); color: var(--color-danger);">
     <i data-lucide="alert-triangle"></i>
     Fel och varningar (<?= count($errors) ?>)
    </h3>
    <div style="max-height: 300px; overflow-y: auto; padding: var(--space-md); background: var(--color-bg-muted); border-radius: var(--radius-md);">
     <?php foreach (array_slice($errors, 0, 50) as $error): ?>
     <div class="text-sm text-secondary" style="margin-bottom: 4px;">
      • <?= h($error) ?>
     </div>
     <?php endforeach; ?>
     <?php if (count($errors) > 50): ?>
     <p class="text-sm text-secondary" style="margin-top: var(--space-sm); font-style: italic;">
      ... och <?= count($errors) - 50 ?> fler
     </p>
     <?php endif; ?>
    </div>
    </div>
   <?php endif; ?>
   </div>
  </div>
  <?php endif; ?>

  <!-- Upload Form -->
  <div class="admin-card mb-lg">
  <div class="admin-card-header">
   <h2>
   <i data-lucide="upload"></i>
   Ladda upp CSV-fil
   </h2>
  </div>
  <div class="admin-card-body">
   <form method="POST" enctype="multipart/form-data" id="uploadForm" style="max-width: 500px;">
   <?= csrf_field() ?>

   <div class="admin-form-group">
    <label class="admin-form-label">
    <i data-lucide="file"></i>
    Välj CSV-fil
    </label>
    <input
    type="file"
    id="import_file"
    name="import_file"
    class="admin-form-input"
    accept=".csv,.xlsx,.xls"
    required
    >
    <small class="text-secondary text-sm">
    Max storlek: <?= round(MAX_UPLOAD_SIZE / 1024 / 1024) ?>MB
    </small>
   </div>

   <div class="admin-form-group">
    <label class="admin-form-label">
    <i data-lucide="calendar"></i>
    Säsongsår för klubbtillhörighet
    </label>
    <?php
    $currentYear = (int)date('Y');
    $availableYears = range($currentYear + 1, $currentYear - 5);
    ?>
    <select name="season_year" class="admin-form-select">
    <?php foreach ($availableYears as $year): ?>
    <option value="<?= $year ?>" <?= $year === $currentYear ? 'selected' : '' ?>><?= $year ?></option>
    <?php endforeach; ?>
    </select>
    <small class="text-secondary text-sm">
    Klubbtillhörighet sätts för detta år
    </small>
   </div>

   <div class="admin-form-group">
    <label class="flex items-center gap-sm cursor-pointer">
    <input type="checkbox" name="create_missing" checked>
    <span>Skapa nya deltagare om de inte finns</span>
    </label>
   </div>

   <button type="submit" class="btn-admin btn-admin-primary">
    <i data-lucide="eye"></i>
    Förhandsgranska import
   </button>
   </form>
  </div>
  </div>

  <!-- File Format Guide -->
  <div class="admin-card">
  <div class="admin-card-header">
   <h2>
   <i data-lucide="info"></i>
   CSV-filformat
   </h2>
  </div>
  <div class="admin-card-body">
   <p class="text-secondary" class="mb-md">
   CSV-filen ska ha följande kolumner i första raden (header):
   </p>

   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th>Kolumn</th>
     <th>Obligatorisk</th>
     <th>Beskrivning</th>
     <th>Exempel</th>
    </tr>
    </thead>
    <tbody>
    <tr>
     <td><code>firstname</code> eller <code>first_name</code></td>
     <td><span class="badge badge-danger">Ja</span></td>
     <td>Förnamn</td>
     <td>Erik</td>
    </tr>
    <tr>
     <td><code>lastname</code> eller <code>last_name</code></td>
     <td><span class="badge badge-danger">Ja</span></td>
     <td>Efternamn</td>
     <td>Andersson</td>
    </tr>
    <tr>
     <td><code>birth_year</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Födelseår</td>
     <td>1995</td>
    </tr>
    <tr>
     <td><code>gender</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Kön (M/F)</td>
     <td>M</td>
    </tr>
    <tr>
     <td><code>club</code> eller <code>club_name</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Klubbnamn (skapas om den inte finns)</td>
     <td>Team GravitySeries</td>
    </tr>
    <tr>
     <td><code>license_number</code> eller <code>uci_id</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>UCI/SCF licensnummer (används för dubbletthantering)</td>
     <td>SWE-2025-1234</td>
    </tr>
    <tr>
     <td><code>email</code> eller <code>e-mail</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>E-postadress</td>
     <td>erik@example.com</td>
    </tr>
    <tr>
     <td><code>phone</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Telefonnummer</td>
     <td>070-1234567</td>
    </tr>
    <tr>
     <td><code>city</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Stad/Ort</td>
     <td>Stockholm</td>
    </tr>
    <tr>
     <td><code>license_type</code> eller <code>licenstyp</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Licenstyp</td>
     <td>Elit</td>
    </tr>
    <tr>
     <td><code>license_year</code> eller <code>licensår</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Licensår</td>
     <td>2025</td>
    </tr>
    <tr>
     <td><code>license_category</code> eller <code>kategori</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Licenskategori</td>
     <td>Herrar</td>
    </tr>
    <tr>
     <td><code>discipline</code> eller <code>gren</code></td>
     <td><span class="badge badge-secondary">Nej</span></td>
     <td>Disciplin/gren</td>
     <td>MTB</td>
    </tr>
    </tbody>
   </table>
   </div>

   <div class="mt-lg gs-info-box-accent">
   <h3 class="text-primary mb-sm">
    <i data-lucide="lightbulb"></i>
    Tips
   </h3>
   <ul class="text-secondary text-sm gs-list-indented">
    <li>Använd komma (,) som separator</li>
    <li>UTF-8 encoding för svenska tecken</li>
    <li>Stöder både <code>first_name</code> och <code>firstname</code> format</li>
    <li>Dubbletter upptäcks via licensnummer eller namn+födelseår</li>
    <li>Befintliga cyklister uppdateras automatiskt</li>
    <li>Klubbar som inte finns skapas automatiskt</li>
    <li>Fuzzy matching används för klubbnamn (matchas även vid små skillnader)</li>
   </ul>
   </div>

   <div class="mt-md">
   <p class="text-sm text-secondary">
    <strong>Exempel på CSV-fil:</strong>
   </p>
   <pre class="gs-code-block">firstname,lastname,birth_year,gender,club,license_number,license_type,license_year,email
Erik,Andersson,1995,M,Team GravitySeries,SWE-2025-1234,Elit,2025,erik@example.com
Anna,Karlsson,1998,F,CK Olympia,SWE-2025-2345,Motion,2025,anna@example.com
Johan,Svensson,1992,M,Uppsala CK,SWE-2025-3456,Elit,2025,johan@example.com</pre>
   </div>
  </div>
  </div>

<script>
 document.addEventListener('DOMContentLoaded', function() {
 // Show progress bar on form submit
 const form = document.getElementById('uploadForm');
 const progressBar = document.getElementById('progressBar');
 const progressFill = document.getElementById('progressFill');
 const progressPercent = document.getElementById('progressPercent');

 if (form) {
  form.addEventListener('submit', function() {
  progressBar.style.display = 'block';

  // Simulate progress (since we can't track real progress in PHP)
  let progress = 0;
  const interval = setInterval(function() {
   progress += Math.random() * 15;
   if (progress > 90) {
   progress = 90;
   clearInterval(interval);
   }
   progressFill.style.width = progress + '%';
   progressPercent.textContent = Math.round(progress) + '%';
  }, 200);
  });
 }
 });
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
