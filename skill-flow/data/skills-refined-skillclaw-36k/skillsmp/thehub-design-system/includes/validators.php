<?php
/**
 * Validation Helper Functions for TheHUB
 *
 * Comprehensive validation functions for all data types
 */

/**
 * Validate email address
 *
 * @param string $email Email address to validate
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateEmail($email) {
    if (empty($email)) {
        return ['valid' => true, 'error' => null]; // Empty is OK for optional fields
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return ['valid' => false, 'error' => 'Ogiltig e-postadress'];
    }

    if (strlen($email) > 255) {
        return ['valid' => false, 'error' => 'E-postadress för lång (max 255 tecken)'];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Parse personnummer (Swedish personal identity number) to extract birth_year
 *
 * NOTE: This function is used during CSV import to extract birth_year from
 * personnummer strings. The personnummer itself is NOT stored in the database.
 *
 * @param string $personnummer Personnummer in format YYYYMMDD-XXXX or YYMMDD-XXXX
 * @return array ['valid' => bool, 'error' => string|null, 'birth_year' => int|null]
 */
function validatePersonnummer($personnummer) {
    if (empty($personnummer)) {
        return ['valid' => false, 'error' => 'Personnummer saknas'];
    }

    // Remove any whitespace
    $personnummer = trim($personnummer);

    // Check format: YYYYMMDD-XXXX or YYMMDD-XXXX
    if (!preg_match('/^(\d{6}|\d{8})-\d{4}$/', $personnummer)) {
        return ['valid' => false, 'error' => 'Ogiltigt personnummerformat (använd YYYYMMDD-XXXX eller YYMMDD-XXXX)'];
    }

    // Extract date part
    $parts = explode('-', $personnummer);
    $datePart = $parts[0];

    // Parse date
    if (strlen($datePart) === 8) {
        // YYYYMMDD format
        $year = intval(substr($datePart, 0, 4));
        $month = intval(substr($datePart, 4, 2));
        $day = intval(substr($datePart, 6, 2));
    } else {
        // YYMMDD format - determine century
        $yy = intval(substr($datePart, 0, 2));
        $currentYear = intval(date('Y'));
        $currentCentury = intval(floor($currentYear / 100) * 100);
        $currentYY = $currentYear % 100;

        if ($yy > $currentYY) {
            // Born in previous century
            $year = $currentCentury - 100 + $yy;
        } else {
            // Born in current century
            $year = $currentCentury + $yy;
        }

        $month = intval(substr($datePart, 2, 2));
        $day = intval(substr($datePart, 4, 2));
    }

    // Validate date
    if (!checkdate($month, $day, $year)) {
        return ['valid' => false, 'error' => 'Ogiltigt födelsedatum'];
    }

    // Check reasonable year range
    if ($year < 1900 || $year > date('Y')) {
        return ['valid' => false, 'error' => 'Födelseår utanför rimligt intervall (1900-' . date('Y') . ')'];
    }

    return ['valid' => true, 'error' => null, 'birth_year' => $year];
}

/**
 * Validate date string
 *
 * @param string $date Date string
 * @param string $format Expected format (default: Y-m-d)
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateDate($date, $format = 'Y-m-d') {
    if (empty($date)) {
        return ['valid' => true, 'error' => null]; // Empty is OK for optional fields
    }

    $d = DateTime::createFromFormat($format, $date);

    if (!$d || $d->format($format) !== $date) {
        return ['valid' => false, 'error' => 'Ogiltigt datumformat (använd ' . $format . ')'];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate URL
 *
 * @param string $url URL to validate
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateUrl($url) {
    if (empty($url)) {
        return ['valid' => true, 'error' => null]; // Empty is OK for optional fields
    }

    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        return ['valid' => false, 'error' => 'Ogiltig URL'];
    }

    if (strlen($url) > 255) {
        return ['valid' => false, 'error' => 'URL för lång (max 255 tecken)'];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate phone number (Swedish format)
 *
 * @param string $phone Phone number
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validatePhone($phone) {
    if (empty($phone)) {
        return ['valid' => true, 'error' => null]; // Empty is OK for optional fields
    }

    // Remove common separators
    $cleanPhone = preg_replace('/[\s\-\(\)]+/', '', $phone);

    // Check if it's all digits (possibly with + prefix)
    if (!preg_match('/^\+?\d{7,15}$/', $cleanPhone)) {
        return ['valid' => false, 'error' => 'Ogiltigt telefonnummer (7-15 siffror)'];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate integer in range
 *
 * @param mixed $value Value to validate
 * @param int $min Minimum value (inclusive)
 * @param int $max Maximum value (inclusive)
 * @param bool $required Is field required?
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateInteger($value, $min = null, $max = null, $required = false) {
    if (empty($value) && !$required) {
        return ['valid' => true, 'error' => null];
    }

    if (!is_numeric($value) || intval($value) != $value) {
        return ['valid' => false, 'error' => 'Måste vara ett heltal'];
    }

    $intValue = intval($value);

    if ($min !== null && $intValue < $min) {
        return ['valid' => false, 'error' => "Värdet måste vara minst $min"];
    }

    if ($max !== null && $intValue > $max) {
        return ['valid' => false, 'error' => "Värdet får inte vara större än $max"];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate decimal/float number
 *
 * @param mixed $value Value to validate
 * @param float $min Minimum value (inclusive)
 * @param float $max Maximum value (inclusive)
 * @param bool $required Is field required?
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateDecimal($value, $min = null, $max = null, $required = false) {
    if (empty($value) && !$required) {
        return ['valid' => true, 'error' => null];
    }

    if (!is_numeric($value)) {
        return ['valid' => false, 'error' => 'Måste vara ett nummer'];
    }

    $floatValue = floatval($value);

    if ($min !== null && $floatValue < $min) {
        return ['valid' => false, 'error' => "Värdet måste vara minst $min"];
    }

    if ($max !== null && $floatValue > $max) {
        return ['valid' => false, 'error' => "Värdet får inte vara större än $max"];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate string length
 *
 * @param string $value String to validate
 * @param int $min Minimum length
 * @param int $max Maximum length
 * @param bool $required Is field required?
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateString($value, $min = 0, $max = 255, $required = false) {
    if (empty($value) && !$required) {
        return ['valid' => true, 'error' => null];
    }

    if ($required && empty($value)) {
        return ['valid' => false, 'error' => 'Detta fält är obligatoriskt'];
    }

    $length = strlen($value);

    if ($length < $min) {
        return ['valid' => false, 'error' => "Måste vara minst $min tecken"];
    }

    if ($length > $max) {
        return ['valid' => false, 'error' => "Får inte vara längre än $max tecken"];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate enum value (must be one of allowed values)
 *
 * @param mixed $value Value to validate
 * @param array $allowed Allowed values
 * @param bool $required Is field required?
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateEnum($value, $allowed, $required = false) {
    if (empty($value) && !$required) {
        return ['valid' => true, 'error' => null];
    }

    if (!in_array($value, $allowed, true)) {
        $allowedStr = implode(', ', $allowed);
        return ['valid' => false, 'error' => "Ogiltigt värde. Tillåtna: $allowedStr"];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate time string (HH:MM:SS format)
 *
 * @param string $time Time string
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateTime($time) {
    if (empty($time)) {
        return ['valid' => true, 'error' => null]; // Empty is OK for optional fields
    }

    if (!preg_match('/^([0-9]{1,2}):([0-5][0-9]):([0-5][0-9])$/', $time, $matches)) {
        return ['valid' => false, 'error' => 'Ogiltigt tidsformat (använd HH:MM:SS)'];
    }

    $hours = intval($matches[1]);
    $minutes = intval($matches[2]);
    $seconds = intval($matches[3]);

    // Allow times over 24 hours for race times (e.g., 25:30:00 for a very long race)
    if ($minutes > 59 || $seconds > 59) {
        return ['valid' => false, 'error' => 'Ogiltiga minuter eller sekunder'];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate UCI license code
 *
 * @param string $uciCode UCI license code (format: "101 637 581 11")
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateUciCode($uciCode) {
    if (empty($uciCode)) {
        return ['valid' => true, 'error' => null]; // Empty is OK
    }

    // UCI codes are typically 11 digits with spaces: "123 456 789 01"
    $cleaned = str_replace(' ', '', $uciCode);

    if (!preg_match('/^\d{11}$/', $cleaned)) {
        return ['valid' => false, 'error' => 'Ogiltigt UCI-kod format (11 siffror)'];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Validate birth year
 *
 * @param int $year Birth year
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateBirthYear($year) {
    if (empty($year)) {
        return ['valid' => true, 'error' => null]; // Empty is OK for optional fields
    }

    $currentYear = intval(date('Y'));

    if (!is_numeric($year) || intval($year) != $year) {
        return ['valid' => false, 'error' => 'Födelseår måste vara ett heltal'];
    }

    $intYear = intval($year);

    if ($intYear < 1900 || $intYear > $currentYear) {
        return ['valid' => false, 'error' => "Födelseår måste vara mellan 1900 och $currentYear"];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Sanitize HTML to prevent XSS
 *
 * @param string $html HTML to sanitize
 * @return string Sanitized HTML
 */
function sanitizeHtml($html) {
    return htmlspecialchars($html, ENT_QUOTES, 'UTF-8');
}

/**
 * Validate file upload
 *
 * @param array $file $_FILES array element
 * @param array $allowedTypes Allowed MIME types
 * @param int $maxSize Maximum file size in bytes
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validateFileUpload($file, $allowedTypes = ['text/csv'], $maxSize = 10485760) {
    if (!isset($file['error']) || is_array($file['error'])) {
        return ['valid' => false, 'error' => 'Ogiltig filuppladdning'];
    }

    switch ($file['error']) {
        case UPLOAD_ERR_OK:
            break;
        case UPLOAD_ERR_INI_SIZE:
        case UPLOAD_ERR_FORM_SIZE:
            return ['valid' => false, 'error' => 'Filen är för stor'];
        case UPLOAD_ERR_PARTIAL:
            return ['valid' => false, 'error' => 'Filuppladdning ofullständig'];
        case UPLOAD_ERR_NO_FILE:
            return ['valid' => false, 'error' => 'Ingen fil uppladdad'];
        default:
            return ['valid' => false, 'error' => 'Okänt filuppladdningsfel'];
    }

    if ($file['size'] > $maxSize) {
        $maxMB = round($maxSize / 1024 / 1024, 2);
        return ['valid' => false, 'error' => "Filen är för stor (max {$maxMB}MB)"];
    }

    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mimeType = $finfo->file($file['tmp_name']);

    if (!in_array($mimeType, $allowedTypes, true)) {
        $allowedStr = implode(', ', $allowedTypes);
        return ['valid' => false, 'error' => "Ogiltigt filformat. Tillåtna: $allowedStr"];
    }

    return ['valid' => true, 'error' => null];
}

/**
 * Batch validate multiple fields
 *
 * @param array $validations Array of validation results
 * @return array ['valid' => bool, 'errors' => array]
 */
function batchValidate($validations) {
    $errors = [];
    $allValid = true;

    foreach ($validations as $field => $result) {
        if (!$result['valid']) {
            $errors[$field] = $result['error'];
            $allValid = false;
        }
    }

    return ['valid' => $allValid, 'errors' => $errors];
}
