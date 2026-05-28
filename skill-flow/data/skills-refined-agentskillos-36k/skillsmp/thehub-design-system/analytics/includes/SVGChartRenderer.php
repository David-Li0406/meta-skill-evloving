<?php
/**
 * SVGChartRenderer
 *
 * Renderar grafer som SVG for PDF-export utan Node.js-beroenden.
 * Designad for TheHUB's designsystem med korrekt fargschema.
 *
 * Stodda graftyper:
 * - Line chart (trender, retention over tid)
 * - Bar chart (aldersfordelning, discipliner)
 * - Stacked bar chart (status breakdown)
 * - Donut/Pie chart (procentfordelningar)
 * - Sparkline (mini-trender)
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

class SVGChartRenderer {
    // TheHUB designsystem farger
    private const COLORS = [
        'accent' => '#37d4d6',
        'accent_light' => 'rgba(55, 212, 214, 0.15)',
        'success' => '#10b981',
        'warning' => '#fbbf24',
        'error' => '#ef4444',
        'info' => '#38bdf8',
        'text_primary' => '#f8f2f0',
        'text_secondary' => '#c7cfdd',
        'text_muted' => '#868fa2',
        'bg_card' => '#0e1621',
        'border' => 'rgba(55, 212, 214, 0.2)',
    ];

    // Serie-farger fran TheHUB
    private const SERIES_COLORS = [
        '#37d4d6', // Accent (cyan)
        '#10b981', // Success (green)
        '#fbbf24', // Warning (yellow)
        '#ef4444', // Error (red)
        '#38bdf8', // Info (blue)
        '#8b5cf6', // Purple
        '#ec4899', // Pink
        '#f97316', // Orange
    ];

    private array $options;

    /**
     * Constructor
     *
     * @param array $options Globala optioner
     */
    public function __construct(array $options = []) {
        $this->options = array_merge([
            'width' => 600,
            'height' => 300,
            'padding' => [
                'top' => 20,
                'right' => 20,
                'bottom' => 40,
                'left' => 50,
            ],
            'font_family' => 'Manrope, Arial, sans-serif',
            'font_size' => 12,
            'animate' => false, // Animationer i SVG (for web)
        ], $options);
    }

    // =========================================================================
    // LINE CHART
    // =========================================================================

    /**
     * Rendera ett linjediagram
     *
     * @param array $data Data med labels och datasets
     * @param array $options Grafspecifika optioner
     * @return string SVG-kod
     */
    public function lineChart(array $data, array $options = []): string {
        $opts = array_merge($this->options, $options);
        $w = $opts['width'];
        $h = $opts['height'];
        $p = $opts['padding'];

        $chartWidth = $w - $p['left'] - $p['right'];
        $chartHeight = $h - $p['top'] - $p['bottom'];

        $labels = $data['labels'] ?? [];
        $datasets = $data['datasets'] ?? [];

        if (empty($labels) || empty($datasets)) {
            return $this->emptyChart($w, $h, 'Ingen data');
        }

        // Hitta min/max for Y-axeln
        $allValues = [];
        foreach ($datasets as $ds) {
            $allValues = array_merge($allValues, $ds['data'] ?? []);
        }
        $minY = min(0, min($allValues));
        $maxY = max($allValues) * 1.1; // 10% marginal

        $svg = $this->startSvg($w, $h);

        // Bakgrund
        $svg .= $this->rect(0, 0, $w, $h, self::COLORS['bg_card']);

        // Gridlines
        $svg .= $this->drawGridlines($p['left'], $p['top'], $chartWidth, $chartHeight, 5);

        // Y-axel labels
        $svg .= $this->drawYAxis($p['left'], $p['top'], $chartHeight, $minY, $maxY, 5);

        // X-axel labels
        $svg .= $this->drawXAxisLabels($p['left'], $p['top'] + $chartHeight, $chartWidth, $labels);

        // Rita varje dataset
        foreach ($datasets as $i => $ds) {
            $color = $ds['color'] ?? self::SERIES_COLORS[$i % count(self::SERIES_COLORS)];
            $points = $this->calculateLinePoints(
                $ds['data'] ?? [],
                $p['left'], $p['top'],
                $chartWidth, $chartHeight,
                $minY, $maxY
            );

            // Area fill (optional)
            if (!empty($ds['fill'])) {
                $areaPoints = $points;
                $areaPoints[] = [$p['left'] + $chartWidth, $p['top'] + $chartHeight];
                $areaPoints[] = [$p['left'], $p['top'] + $chartHeight];
                $svg .= $this->polygon($areaPoints, $this->hexToRgba($color, 0.2));
            }

            // Linje
            $svg .= $this->polyline($points, $color, 2);

            // Punkter
            foreach ($points as $point) {
                $svg .= $this->circle($point[0], $point[1], 4, $color);
            }
        }

        // Legend
        if (count($datasets) > 1) {
            $svg .= $this->drawLegend($datasets, $w - $p['right'] - 100, $p['top']);
        }

        // Titel (om angiven)
        if (!empty($options['title'])) {
            $svg .= $this->text($w / 2, 15, $options['title'], self::COLORS['text_primary'], 14, 'middle');
        }

        $svg .= '</svg>';
        return $svg;
    }

    // =========================================================================
    // BAR CHART
    // =========================================================================

    /**
     * Rendera ett stapeldiagram
     *
     * @param array $data Data med labels och values
     * @param array $options Grafspecifika optioner
     * @return string SVG-kod
     */
    public function barChart(array $data, array $options = []): string {
        $opts = array_merge($this->options, $options);
        $w = $opts['width'];
        $h = $opts['height'];
        $p = $opts['padding'];

        $chartWidth = $w - $p['left'] - $p['right'];
        $chartHeight = $h - $p['top'] - $p['bottom'];

        $labels = $data['labels'] ?? [];
        $values = $data['values'] ?? $data['data'] ?? [];

        if (empty($labels) || empty($values)) {
            return $this->emptyChart($w, $h, 'Ingen data');
        }

        $maxValue = max($values) * 1.1;
        $barCount = count($labels);
        $barWidth = ($chartWidth / $barCount) * 0.7;
        $barGap = ($chartWidth / $barCount) * 0.3;

        $svg = $this->startSvg($w, $h);
        $svg .= $this->rect(0, 0, $w, $h, self::COLORS['bg_card']);

        // Gridlines
        $svg .= $this->drawGridlines($p['left'], $p['top'], $chartWidth, $chartHeight, 5);

        // Y-axel
        $svg .= $this->drawYAxis($p['left'], $p['top'], $chartHeight, 0, $maxValue, 5);

        // Staplar
        $color = $options['color'] ?? self::COLORS['accent'];
        foreach ($values as $i => $value) {
            $barHeight = ($value / $maxValue) * $chartHeight;
            $x = $p['left'] + ($i * ($barWidth + $barGap)) + ($barGap / 2);
            $y = $p['top'] + $chartHeight - $barHeight;

            // Stapel med rundade horn
            $svg .= $this->rect($x, $y, $barWidth, $barHeight, $color, 4);

            // Varde over stapeln
            if ($barHeight > 20) {
                $svg .= $this->text(
                    $x + $barWidth / 2,
                    $y - 5,
                    $this->formatNumber($value),
                    self::COLORS['text_secondary'],
                    10,
                    'middle'
                );
            }
        }

        // X-axel labels (under staplarna)
        foreach ($labels as $i => $label) {
            $x = $p['left'] + ($i * ($barWidth + $barGap)) + ($barGap / 2) + $barWidth / 2;
            $y = $p['top'] + $chartHeight + 15;

            // Rotera text om den ar for lang
            if (strlen($label) > 10) {
                $svg .= $this->text($x, $y, substr($label, 0, 10), self::COLORS['text_muted'], 9, 'middle', -45);
            } else {
                $svg .= $this->text($x, $y, $label, self::COLORS['text_muted'], 10, 'middle');
            }
        }

        // Titel
        if (!empty($options['title'])) {
            $svg .= $this->text($w / 2, 15, $options['title'], self::COLORS['text_primary'], 14, 'middle');
        }

        $svg .= '</svg>';
        return $svg;
    }

    // =========================================================================
    // DONUT CHART
    // =========================================================================

    /**
     * Rendera ett donut-diagram
     *
     * @param array $data Data med labels och values
     * @param array $options Grafspecifika optioner
     * @return string SVG-kod
     */
    public function donutChart(array $data, array $options = []): string {
        $opts = array_merge($this->options, $options);
        $w = $opts['width'];
        $h = $opts['height'];

        $labels = $data['labels'] ?? [];
        $values = $data['values'] ?? $data['data'] ?? [];

        if (empty($values)) {
            return $this->emptyChart($w, $h, 'Ingen data');
        }

        $total = array_sum($values);
        if ($total == 0) {
            return $this->emptyChart($w, $h, 'Summa = 0');
        }

        $centerX = $w / 2 - 50; // Plats for legend till hoger
        $centerY = $h / 2;
        $outerRadius = min($w, $h) / 2 - 30;
        $innerRadius = $outerRadius * 0.6; // Donut hole

        $svg = $this->startSvg($w, $h);
        $svg .= $this->rect(0, 0, $w, $h, self::COLORS['bg_card']);

        $startAngle = -90; // Starta fran toppen

        foreach ($values as $i => $value) {
            $percentage = $value / $total;
            $sweepAngle = $percentage * 360;
            $color = $options['colors'][$i] ?? self::SERIES_COLORS[$i % count(self::SERIES_COLORS)];

            $svg .= $this->arcPath(
                $centerX, $centerY,
                $outerRadius, $innerRadius,
                $startAngle, $startAngle + $sweepAngle,
                $color
            );

            $startAngle += $sweepAngle;
        }

        // Center text (total)
        $svg .= $this->text($centerX, $centerY - 5, $this->formatNumber($total), self::COLORS['text_primary'], 20, 'middle');
        $svg .= $this->text($centerX, $centerY + 15, 'Total', self::COLORS['text_muted'], 11, 'middle');

        // Legend
        $legendX = $centerX + $outerRadius + 30;
        $legendY = 30;
        foreach ($labels as $i => $label) {
            $color = $options['colors'][$i] ?? self::SERIES_COLORS[$i % count(self::SERIES_COLORS)];
            $percentage = round(($values[$i] / $total) * 100, 1);

            $svg .= $this->rect($legendX, $legendY + ($i * 22), 12, 12, $color, 2);
            $svg .= $this->text(
                $legendX + 18,
                $legendY + ($i * 22) + 10,
                "{$label}: {$percentage}%",
                self::COLORS['text_secondary'],
                11
            );
        }

        // Titel
        if (!empty($options['title'])) {
            $svg .= $this->text($w / 2, 15, $options['title'], self::COLORS['text_primary'], 14, 'middle');
        }

        $svg .= '</svg>';
        return $svg;
    }

    // =========================================================================
    // SPARKLINE
    // =========================================================================

    /**
     * Rendera en sparkline (mini-trend)
     *
     * @param array $values Numeriska varden
     * @param array $options Optioner (width, height, color)
     * @return string SVG-kod
     */
    public function sparkline(array $values, array $options = []): string {
        $w = $options['width'] ?? 100;
        $h = $options['height'] ?? 30;
        $color = $options['color'] ?? self::COLORS['accent'];

        if (count($values) < 2) {
            return $this->emptyChart($w, $h, '');
        }

        $min = min($values);
        $max = max($values);
        $range = $max - $min ?: 1;

        $points = [];
        $stepX = $w / (count($values) - 1);

        foreach ($values as $i => $value) {
            $x = $i * $stepX;
            $y = $h - (($value - $min) / $range * ($h - 4)) - 2;
            $points[] = [$x, $y];
        }

        $svg = $this->startSvg($w, $h);

        // Area fill
        $areaPoints = $points;
        $areaPoints[] = [$w, $h];
        $areaPoints[] = [0, $h];
        $svg .= $this->polygon($areaPoints, $this->hexToRgba($color, 0.1));

        // Linje
        $svg .= $this->polyline($points, $color, 1.5);

        // Sista punkten
        $lastPoint = end($points);
        $svg .= $this->circle($lastPoint[0], $lastPoint[1], 3, $color);

        $svg .= '</svg>';
        return $svg;
    }

    // =========================================================================
    // STACKED BAR CHART
    // =========================================================================

    /**
     * Rendera ett stacked bar chart
     *
     * @param array $data Data med labels och datasets
     * @param array $options Grafspecifika optioner
     * @return string SVG-kod
     */
    public function stackedBarChart(array $data, array $options = []): string {
        $opts = array_merge($this->options, $options);
        $w = $opts['width'];
        $h = $opts['height'];
        $p = $opts['padding'];

        $chartWidth = $w - $p['left'] - $p['right'];
        $chartHeight = $h - $p['top'] - $p['bottom'];

        $labels = $data['labels'] ?? [];
        $datasets = $data['datasets'] ?? [];

        if (empty($labels) || empty($datasets)) {
            return $this->emptyChart($w, $h, 'Ingen data');
        }

        // Berakna totaler for varje bar
        $totals = [];
        foreach ($labels as $i => $label) {
            $totals[$i] = 0;
            foreach ($datasets as $ds) {
                $totals[$i] += $ds['data'][$i] ?? 0;
            }
        }
        $maxTotal = max($totals) * 1.1;

        $barCount = count($labels);
        $barWidth = ($chartWidth / $barCount) * 0.7;
        $barGap = ($chartWidth / $barCount) * 0.3;

        $svg = $this->startSvg($w, $h);
        $svg .= $this->rect(0, 0, $w, $h, self::COLORS['bg_card']);

        // Gridlines och Y-axel
        $svg .= $this->drawGridlines($p['left'], $p['top'], $chartWidth, $chartHeight, 5);
        $svg .= $this->drawYAxis($p['left'], $p['top'], $chartHeight, 0, $maxTotal, 5);

        // Rita stacked bars
        foreach ($labels as $barIndex => $label) {
            $x = $p['left'] + ($barIndex * ($barWidth + $barGap)) + ($barGap / 2);
            $currentY = $p['top'] + $chartHeight;

            foreach ($datasets as $dsIndex => $ds) {
                $value = $ds['data'][$barIndex] ?? 0;
                $barHeight = ($value / $maxTotal) * $chartHeight;
                $color = $ds['color'] ?? self::SERIES_COLORS[$dsIndex % count(self::SERIES_COLORS)];

                $currentY -= $barHeight;
                $svg .= $this->rect($x, $currentY, $barWidth, $barHeight, $color);
            }

            // X-label
            $svg .= $this->text(
                $x + $barWidth / 2,
                $p['top'] + $chartHeight + 15,
                $label,
                self::COLORS['text_muted'],
                10,
                'middle'
            );
        }

        // Legend
        $legendX = $w - $p['right'] - 120;
        $legendY = $p['top'];
        foreach ($datasets as $i => $ds) {
            $color = $ds['color'] ?? self::SERIES_COLORS[$i % count(self::SERIES_COLORS)];
            $svg .= $this->rect($legendX, $legendY + ($i * 18), 10, 10, $color, 2);
            $svg .= $this->text($legendX + 15, $legendY + ($i * 18) + 9, $ds['label'] ?? "Serie $i", self::COLORS['text_secondary'], 10);
        }

        $svg .= '</svg>';
        return $svg;
    }

    // =========================================================================
    // HELPER METHODS
    // =========================================================================

    private function startSvg(int $width, int $height): string {
        return sprintf(
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">',
            $width, $height, $width, $height
        );
    }

    private function rect(float $x, float $y, float $w, float $h, string $fill, int $radius = 0): string {
        if ($radius > 0) {
            return sprintf(
                '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" fill="%s"/>',
                $x, $y, $w, $h, $radius, $fill
            );
        }
        return sprintf(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>',
            $x, $y, $w, $h, $fill
        );
    }

    private function circle(float $cx, float $cy, float $r, string $fill): string {
        return sprintf(
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>',
            $cx, $cy, $r, $fill
        );
    }

    private function text(float $x, float $y, string $content, string $fill, int $size = 12, string $anchor = 'start', int $rotate = 0): string {
        $transform = $rotate !== 0 ? sprintf(' transform="rotate(%d %.1f %.1f)"', $rotate, $x, $y) : '';
        return sprintf(
            '<text x="%.1f" y="%.1f" fill="%s" font-size="%d" font-family="%s" text-anchor="%s"%s>%s</text>',
            $x, $y, $fill, $size, $this->options['font_family'], $anchor, $transform, htmlspecialchars($content)
        );
    }

    private function polyline(array $points, string $stroke, float $strokeWidth = 1): string {
        $pointsStr = implode(' ', array_map(fn($p) => sprintf('%.1f,%.1f', $p[0], $p[1]), $points));
        return sprintf(
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"/>',
            $pointsStr, $stroke, $strokeWidth
        );
    }

    private function polygon(array $points, string $fill): string {
        $pointsStr = implode(' ', array_map(fn($p) => sprintf('%.1f,%.1f', $p[0], $p[1]), $points));
        return sprintf('<polygon points="%s" fill="%s"/>', $pointsStr, $fill);
    }

    private function arcPath(float $cx, float $cy, float $outerR, float $innerR, float $startAngle, float $endAngle, string $fill): string {
        // Konvertera vinklar till radianer
        $start = deg2rad($startAngle);
        $end = deg2rad($endAngle);

        // Berakna punkter
        $x1 = $cx + $outerR * cos($start);
        $y1 = $cy + $outerR * sin($start);
        $x2 = $cx + $outerR * cos($end);
        $y2 = $cy + $outerR * sin($end);
        $x3 = $cx + $innerR * cos($end);
        $y3 = $cy + $innerR * sin($end);
        $x4 = $cx + $innerR * cos($start);
        $y4 = $cy + $innerR * sin($start);

        $largeArc = ($endAngle - $startAngle) > 180 ? 1 : 0;

        $d = sprintf(
            'M %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 0 %.1f %.1f Z',
            $x1, $y1,
            $outerR, $outerR, $largeArc, $x2, $y2,
            $x3, $y3,
            $innerR, $innerR, $largeArc, $x4, $y4
        );

        return sprintf('<path d="%s" fill="%s"/>', $d, $fill);
    }

    private function drawGridlines(float $x, float $y, float $w, float $h, int $count): string {
        $svg = '';
        $step = $h / $count;

        for ($i = 0; $i <= $count; $i++) {
            $lineY = $y + ($i * $step);
            $svg .= sprintf(
                '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" opacity="0.3"/>',
                $x, $lineY, $x + $w, $lineY, self::COLORS['border']
            );
        }

        return $svg;
    }

    private function drawYAxis(float $x, float $y, float $h, float $min, float $max, int $count): string {
        $svg = '';
        $step = $h / $count;
        $valueStep = ($max - $min) / $count;

        for ($i = 0; $i <= $count; $i++) {
            $lineY = $y + $h - ($i * $step);
            $value = $min + ($i * $valueStep);
            $svg .= $this->text($x - 5, $lineY + 4, $this->formatNumber($value), self::COLORS['text_muted'], 10, 'end');
        }

        return $svg;
    }

    private function drawXAxisLabels(float $x, float $y, float $w, array $labels): string {
        $svg = '';
        $count = count($labels);
        if ($count == 0) return $svg;

        $step = $w / ($count - 1);

        foreach ($labels as $i => $label) {
            $labelX = $x + ($i * $step);
            $svg .= $this->text($labelX, $y + 15, (string)$label, self::COLORS['text_muted'], 10, 'middle');
        }

        return $svg;
    }

    private function drawLegend(array $datasets, float $x, float $y): string {
        $svg = '';

        foreach ($datasets as $i => $ds) {
            $color = $ds['color'] ?? self::SERIES_COLORS[$i % count(self::SERIES_COLORS)];
            $label = $ds['label'] ?? "Serie " . ($i + 1);

            $svg .= $this->rect($x, $y + ($i * 18), 10, 10, $color, 2);
            $svg .= $this->text($x + 15, $y + ($i * 18) + 9, $label, self::COLORS['text_secondary'], 10);
        }

        return $svg;
    }

    private function calculateLinePoints(array $data, float $x, float $y, float $w, float $h, float $min, float $max): array {
        $points = [];
        $count = count($data);
        if ($count < 2) return $points;

        $stepX = $w / ($count - 1);
        $range = $max - $min ?: 1;

        foreach ($data as $i => $value) {
            $px = $x + ($i * $stepX);
            $py = $y + $h - (($value - $min) / $range * $h);
            $points[] = [$px, $py];
        }

        return $points;
    }

    private function formatNumber(float $value): string {
        if ($value >= 1000000) {
            return round($value / 1000000, 1) . 'M';
        }
        if ($value >= 1000) {
            return round($value / 1000, 1) . 'k';
        }
        if ($value == (int)$value) {
            return (string)(int)$value;
        }
        return number_format($value, 1);
    }

    private function hexToRgba(string $hex, float $alpha): string {
        $hex = ltrim($hex, '#');
        if (strlen($hex) === 3) {
            $hex = $hex[0] . $hex[0] . $hex[1] . $hex[1] . $hex[2] . $hex[2];
        }
        $r = hexdec(substr($hex, 0, 2));
        $g = hexdec(substr($hex, 2, 2));
        $b = hexdec(substr($hex, 4, 2));
        return "rgba($r, $g, $b, $alpha)";
    }

    private function emptyChart(int $w, int $h, string $message): string {
        $svg = $this->startSvg($w, $h);
        $svg .= $this->rect(0, 0, $w, $h, self::COLORS['bg_card']);
        $svg .= $this->text($w / 2, $h / 2, $message, self::COLORS['text_muted'], 12, 'middle');
        $svg .= '</svg>';
        return $svg;
    }

    // =========================================================================
    // v3.0.1: PNG EXPORT WITH GRACEFUL FALLBACK
    // =========================================================================

    /** @var bool|null Cache for Imagick availability */
    private static ?bool $imagickAvailable = null;

    /**
     * Kontrollera om PNG-konvertering ar tillganglig
     *
     * @return bool True om Imagick ar tillganglig och fungerar
     */
    public static function canConvertToPng(): bool {
        if (self::$imagickAvailable !== null) {
            return self::$imagickAvailable;
        }

        if (!extension_loaded('imagick')) {
            self::$imagickAvailable = false;
            return false;
        }

        // Testa faktisk konvertering
        try {
            $testSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect fill="red" width="10" height="10"/></svg>';
            $im = new \Imagick();
            $im->readImageBlob($testSvg);
            $im->setImageFormat('png');
            $im->getImageBlob();
            $im->destroy();

            self::$imagickAvailable = true;
        } catch (\Exception $e) {
            self::$imagickAvailable = false;
        }

        return self::$imagickAvailable;
    }

    /**
     * Konvertera SVG till PNG med Imagick (om tillganglig)
     *
     * v3.0.1: Forbattrad felhantering och graceful fallback
     *
     * @param string $svg SVG-kod
     * @param int $scale Skalningsfaktor (2 = 2x resolution)
     * @return string|null PNG data eller null om konvertering misslyckades
     */
    public function svgToPng(string $svg, int $scale = 2): ?string {
        if (!self::canConvertToPng()) {
            return null;
        }

        try {
            $im = new \Imagick();

            // Satt bakgrundsfargen for transparens
            $im->setBackgroundColor(new \ImagickPixel('transparent'));

            // Las SVG
            $im->readImageBlob($svg);
            $im->setImageFormat('png');

            // Skala upp for battre resolution
            if ($scale > 1) {
                $w = $im->getImageWidth() * $scale;
                $h = $im->getImageHeight() * $scale;
                $im->resizeImage($w, $h, \Imagick::FILTER_LANCZOS, 1);
            }

            $png = $im->getImageBlob();
            $im->destroy();

            return $png;
        } catch (\Exception $e) {
            // Logga fel men returnera null for graceful fallback
            error_log('SVGChartRenderer::svgToPng failed: ' . $e->getMessage());
            return null;
        }
    }

    /**
     * Hamta chart som PNG eller SVG (graceful fallback)
     *
     * v3.0.1: Om Imagick saknas, returneras SVG istallet med en flagga
     *
     * @param string $svg SVG-kod
     * @param int $scale Skalningsfaktor
     * @return array ['format' => 'png'|'svg', 'data' => binary data, 'mime' => 'image/png'|'image/svg+xml']
     */
    public function getChartAsImage(string $svg, int $scale = 2): array {
        $png = $this->svgToPng($svg, $scale);

        if ($png !== null) {
            return [
                'format' => 'png',
                'data' => $png,
                'mime' => 'image/png',
                'base64' => base64_encode($png),
            ];
        }

        // Graceful fallback to SVG
        return [
            'format' => 'svg',
            'data' => $svg,
            'mime' => 'image/svg+xml',
            'base64' => base64_encode($svg),
            'fallback_reason' => 'Imagick not available',
        ];
    }

    /**
     * Spara SVG till fil
     *
     * @param string $svg SVG-kod
     * @param string $path Filsokvag
     * @return bool Lyckades
     */
    public function saveToFile(string $svg, string $path): bool {
        return file_put_contents($path, $svg) !== false;
    }

    /**
     * Spara som PNG till fil (eller SVG om PNG inte tillgangligt)
     *
     * v3.0.1: Graceful fallback - sparar som SVG om Imagick saknas
     *
     * @param string $svg SVG-kod
     * @param string $path Filsokvag (utan extension)
     * @param int $scale Skalningsfaktor
     * @return array ['success' => bool, 'path' => string, 'format' => 'png'|'svg']
     */
    public function saveAsImage(string $svg, string $path, int $scale = 2): array {
        $image = $this->getChartAsImage($svg, $scale);

        if ($image['format'] === 'png') {
            $fullPath = $path . '.png';
            $success = file_put_contents($fullPath, $image['data']) !== false;
        } else {
            $fullPath = $path . '.svg';
            $success = file_put_contents($fullPath, $image['data']) !== false;
        }

        return [
            'success' => $success,
            'path' => $fullPath,
            'format' => $image['format'],
            'fallback_reason' => $image['fallback_reason'] ?? null,
        ];
    }

    /**
     * Generera inline data URI for HTML/PDF embedding
     *
     * @param string $svg SVG-kod
     * @param bool $preferPng Forsok konvertera till PNG om mojligt
     * @return string Data URI (data:image/...)
     */
    public function toDataUri(string $svg, bool $preferPng = false): string {
        if ($preferPng) {
            $image = $this->getChartAsImage($svg);
            return 'data:' . $image['mime'] . ';base64,' . $image['base64'];
        }

        return 'data:image/svg+xml;base64,' . base64_encode($svg);
    }

    /**
     * Hamta systeminformation om PNG-support
     *
     * @return array Information om Imagick-tillganglighet
     */
    public static function getPngSupportInfo(): array {
        $info = [
            'imagick_extension' => extension_loaded('imagick'),
            'can_convert' => self::canConvertToPng(),
            'php_version' => PHP_VERSION,
        ];

        if (extension_loaded('imagick')) {
            try {
                $info['imagick_version'] = \Imagick::getVersion()['versionString'] ?? 'unknown';
                $info['supported_formats'] = \Imagick::queryFormats('SVG') ? ['SVG'] : [];
            } catch (\Exception $e) {
                $info['imagick_error'] = $e->getMessage();
            }
        }

        return $info;
    }
}
