<?php
/**
 * TheHUB - Share Image Generator
 *
 * Generates a shareable image with rider stats for Instagram/Facebook
 *
 * Usage: /api/share-image.php?rider_id=123
 *
 * @version 1.0
 */

// Include config and database
require_once dirname(__DIR__) . '/config.php';

// Get rider ID
$riderId = intval($_GET['rider_id'] ?? 0);

if (!$riderId) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing rider_id']);
    exit;
}

try {
    $pdo = $GLOBALS['pdo'];

    // Fetch rider data
    $stmt = $pdo->prepare("
        SELECT
            r.id, r.firstname, r.lastname, r.birth_year,
            r.stats_total_starts, r.stats_total_wins, r.stats_total_podiums,
            r.first_season, r.experience_level,
            c.name as club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        http_response_code(404);
        echo json_encode(['error' => 'Rider not found']);
        exit;
    }

    // Calculate stats
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ? AND status = 'finished'");
    $stmt->execute([$riderId]);
    $totalRaces = (int)$stmt->fetchColumn();

    $stmt = $pdo->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ? AND position = 1 AND status = 'finished'");
    $stmt->execute([$riderId]);
    $wins = (int)$stmt->fetchColumn();

    $stmt = $pdo->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ? AND position <= 3 AND status = 'finished'");
    $stmt->execute([$riderId]);
    $podiums = (int)$stmt->fetchColumn();

    // Use cached stats if available, otherwise use calculated
    $totalRaces = $rider['stats_total_starts'] ?: $totalRaces;
    $wins = $rider['stats_total_wins'] ?: $wins;
    $podiums = $rider['stats_total_podiums'] ?: $podiums;

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database error']);
    exit;
}

// Image dimensions (Instagram/Facebook friendly - 1080x1080)
$width = 1080;
$height = 1080;

// Create image
$image = imagecreatetruecolor($width, $height);

// Enable anti-aliasing
imageantialias($image, true);

// Colors
$bgColor = imagecolorallocate($image, 23, 23, 23); // #171717
$accentColor = imagecolorallocate($image, 97, 206, 112); // #61CE70
$goldColor = imagecolorallocate($image, 255, 215, 0); // #FFD700
$silverColor = imagecolorallocate($image, 192, 192, 192); // #C0C0C0
$bronzeColor = imagecolorallocate($image, 205, 127, 50); // #CD7F32
$textColor = imagecolorallocate($image, 255, 255, 255); // White
$mutedColor = imagecolorallocate($image, 150, 150, 150); // Gray
$cardBg = imagecolorallocate($image, 40, 40, 40); // Dark gray for cards

// Fill background
imagefill($image, 0, 0, $bgColor);

// Draw accent gradient bar at top
for ($i = 0; $i < 8; $i++) {
    $ratio = $i / 8;
    $r = (int)(97 + (0 - 97) * $ratio);
    $g = (int)(206 + (74 - 206) * $ratio);
    $b = (int)(112 + (152 - 112) * $ratio);
    $lineColor = imagecolorallocate($image, max(0, min(255, $r)), max(0, min(255, $g)), max(0, min(255, $b)));
    imageline($image, 0, $i, $width, $i, $lineColor);
}

// Font paths (use system fonts or bundled fonts)
$fontPath = dirname(__DIR__) . '/assets/fonts/Inter-Bold.ttf';
$fontPathRegular = dirname(__DIR__) . '/assets/fonts/Inter-Regular.ttf';

// Fallback to built-in font if custom fonts not available
$useBuiltInFont = !file_exists($fontPath);

// Helper function to draw centered text
function drawCenteredText($image, $text, $y, $fontSize, $color, $fontPath, $useBuiltInFont = false) {
    global $width;
    if ($useBuiltInFont) {
        $textWidth = imagefontwidth(5) * strlen($text);
        $x = ($width - $textWidth) / 2;
        imagestring($image, 5, $x, $y, $text, $color);
    } else {
        $bbox = imagettfbbox($fontSize, 0, $fontPath, $text);
        $textWidth = abs($bbox[4] - $bbox[0]);
        $x = ($width - $textWidth) / 2;
        imagettftext($image, $fontSize, 0, $x, $y, $color, $fontPath, $text);
    }
}

// Helper function to draw left-aligned text
function drawText($image, $text, $x, $y, $fontSize, $color, $fontPath, $useBuiltInFont = false) {
    if ($useBuiltInFont) {
        imagestring($image, 5, $x, $y, $text, $color);
    } else {
        imagettftext($image, $fontSize, 0, $x, $y, $color, $fontPath, $text);
    }
}

// Draw GravitySeries logo text
if ($useBuiltInFont) {
    drawCenteredText($image, 'GRAVITYSERIES', 60, 0, $accentColor, '', true);
} else {
    drawCenteredText($image, 'GRAVITYSERIES', 80, 24, $accentColor, $fontPath, false);
}

// Draw rider name
$fullName = strtoupper($rider['firstname'] . ' ' . $rider['lastname']);
if ($useBuiltInFont) {
    drawCenteredText($image, $fullName, 180, 0, $textColor, '', true);
} else {
    drawCenteredText($image, $fullName, 220, 64, $textColor, $fontPath, false);
}

// Draw club name if available
if ($rider['club_name']) {
    if ($useBuiltInFont) {
        drawCenteredText($image, $rider['club_name'], 230, 0, $mutedColor, '', true);
    } else {
        drawCenteredText($image, $rider['club_name'], 280, 24, $mutedColor, $fontPathRegular ?: $fontPath, false);
    }
}

// Draw stat cards background
$cardY = 380;
$cardHeight = 200;
$cardWidth = 220;
$cardGap = 40;
$totalCardsWidth = (4 * $cardWidth) + (3 * $cardGap);
$startX = ($width - $totalCardsWidth) / 2;

// Draw 4 stat cards
$stats = [
    ['value' => $totalRaces, 'label' => 'LOPP', 'color' => $accentColor],
    ['value' => $wins, 'label' => 'SEGRAR', 'color' => $goldColor],
    ['value' => $podiums, 'label' => 'PALLPLATSER', 'color' => $silverColor],
    ['value' => date('Y') - ($rider['first_season'] ?: date('Y')) + 1, 'label' => 'SÄSONGER', 'color' => $bronzeColor]
];

foreach ($stats as $i => $stat) {
    $cardX = $startX + ($i * ($cardWidth + $cardGap));

    // Draw card background with rounded corners effect
    imagefilledrectangle($image, $cardX, $cardY, $cardX + $cardWidth, $cardY + $cardHeight, $cardBg);

    // Draw accent line at top of card
    imagefilledrectangle($image, $cardX, $cardY, $cardX + $cardWidth, $cardY + 4, $stat['color']);

    // Draw value
    if ($useBuiltInFont) {
        $valueWidth = imagefontwidth(5) * strlen((string)$stat['value']);
        imagestring($image, 5, $cardX + ($cardWidth - $valueWidth) / 2, $cardY + 60, (string)$stat['value'], $textColor);
    } else {
        $bbox = imagettfbbox(56, 0, $fontPath, (string)$stat['value']);
        $valueWidth = abs($bbox[4] - $bbox[0]);
        $valueX = $cardX + ($cardWidth - $valueWidth) / 2;
        imagettftext($image, 56, 0, $valueX, $cardY + 120, $textColor, $fontPath, (string)$stat['value']);
    }

    // Draw label
    if ($useBuiltInFont) {
        $labelWidth = imagefontwidth(3) * strlen($stat['label']);
        imagestring($image, 3, $cardX + ($cardWidth - $labelWidth) / 2, $cardY + 150, $stat['label'], $mutedColor);
    } else {
        $bbox = imagettfbbox(16, 0, $fontPathRegular ?: $fontPath, $stat['label']);
        $labelWidth = abs($bbox[4] - $bbox[0]);
        $labelX = $cardX + ($cardWidth - $labelWidth) / 2;
        imagettftext($image, 16, 0, $labelX, $cardY + 170, $mutedColor, $fontPathRegular ?: $fontPath, $stat['label']);
    }
}

// Draw medals row if applicable
if ($wins > 0 || $podiums > 0) {
    $medalY = 650;

    // Draw medal icons (simplified circles)
    $medalSize = 60;
    $medalGap = 30;
    $medalStartX = ($width - (3 * $medalSize + 2 * $medalGap)) / 2;

    // Gold medal
    if ($wins > 0) {
        imagefilledellipse($image, $medalStartX + $medalSize/2, $medalY, $medalSize, $medalSize, $goldColor);
        if (!$useBuiltInFont) {
            $bbox = imagettfbbox(20, 0, $fontPath, '1');
            $x = $medalStartX + ($medalSize - abs($bbox[4] - $bbox[0])) / 2;
            imagettftext($image, 20, 0, $x, $medalY + 8, $bgColor, $fontPath, '1');
        }
    }
}

// Draw experience level
$expLabels = [1 => '1:A ÅRET', 2 => '2:A ÅRET', 3 => 'ERFAREN', 4 => 'EXPERT', 5 => 'VETERAN', 6 => 'LEGEND'];
$expLevel = $rider['experience_level'] ?: 1;
$expLabel = $expLabels[$expLevel] ?? '1:A ÅRET';

if ($useBuiltInFont) {
    drawCenteredText($image, 'ERFARENHET: ' . $expLabel, 750, 0, $accentColor, '', true);
} else {
    drawCenteredText($image, 'ERFARENHET: ' . $expLabel, 800, 20, $accentColor, $fontPathRegular ?: $fontPath, false);
}

// Draw experience bar
$barWidth = 600;
$barHeight = 12;
$barX = ($width - $barWidth) / 2;
$barY = 840;

// Background bar
imagefilledrectangle($image, $barX, $barY, $barX + $barWidth, $barY + $barHeight, $cardBg);

// Filled portion
$fillWidth = (int)(($expLevel / 6) * $barWidth);
imagefilledrectangle($image, $barX, $barY, $barX + $fillWidth, $barY + $barHeight, $accentColor);

// Draw experience segments
$segmentWidth = $barWidth / 6;
for ($i = 1; $i <= 6; $i++) {
    $segX = $barX + ($i * $segmentWidth);
    imageline($image, $segX, $barY, $segX, $barY + $barHeight, $bgColor);
}

// Draw footer with URL
if ($useBuiltInFont) {
    drawCenteredText($image, 'gravityseries.se', 1020, 0, $mutedColor, '', true);
} else {
    drawCenteredText($image, 'gravityseries.se', 1020, 18, $mutedColor, $fontPathRegular ?: $fontPath, false);
}

// Draw watermark
$watermarkText = 'thehub.gravityseries.se/rider/' . $riderId;
if ($useBuiltInFont) {
    drawCenteredText($image, $watermarkText, 1050, 0, $mutedColor, '', true);
} else {
    drawCenteredText($image, $watermarkText, 1050, 14, $mutedColor, $fontPathRegular ?: $fontPath, false);
}

// Output image
header('Content-Type: image/png');
header('Content-Disposition: inline; filename="' . strtolower($rider['firstname'] . '-' . $rider['lastname']) . '-stats.png"');
header('Cache-Control: public, max-age=3600');

imagepng($image);
imagedestroy($image);
