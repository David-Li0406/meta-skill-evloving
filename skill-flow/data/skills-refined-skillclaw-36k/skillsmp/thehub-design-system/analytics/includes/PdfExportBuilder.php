<?php
/**
 * PdfExportBuilder
 *
 * Bygger professionella PDF-exporter med obligatorisk "Definitions & Provenance" box.
 * Alla PDF-exporter ska inkludera metadata for reproducerbarhet och GDPR-compliance.
 *
 * v3.0.2: TCPDF ar OBLIGATORISK PDF-motor. Ingen HTML-fallback i production.
 *
 * PDF ENGINE POLICY:
 * - TCPDF ar den enda stodda PDF-motorn
 * - Om TCPDF saknas kastas PdfEngineException
 * - HTML-fallback ar INTE tillaten i production
 *
 * @package TheHUB Analytics
 * @version 3.0.2
 */

require_once __DIR__ . '/AnalyticsConfig.php';
require_once __DIR__ . '/ExportLogger.php';
require_once __DIR__ . '/SVGChartRenderer.php';

/**
 * Exception for PDF engine errors
 */
class PdfEngineException extends RuntimeException {}

class PdfExportBuilder {
    private PDO $pdo;
    private ExportLogger $logger;
    private SVGChartRenderer $chartRenderer;

    private string $title = '';
    private string $subtitle = '';
    private array $sections = [];
    private array $metadata = [];
    private int $snapshotId;
    private ?int $seasonYear = null;

    /** @var array KPI-definitioner att inkludera */
    private array $kpiDefinitions = [];

    /** @var bool Om TCPDF ar tillganglig */
    private static ?bool $tcpdfAvailable = null;

    /** @var string|null Path till TCPDF */
    private static ?string $tcpdfPath = null;

    /**
     * Constructor
     *
     * @param PDO $pdo Databasanslutning
     * @param int $snapshotId Obligatorisk snapshot ID
     * @throws PdfEngineException Om TCPDF saknas
     */
    public function __construct(PDO $pdo, int $snapshotId) {
        $this->pdo = $pdo;
        $this->snapshotId = $snapshotId;
        $this->logger = new ExportLogger($pdo);
        $this->chartRenderer = new SVGChartRenderer();

        // v3.0.2: Verifiera att TCPDF ar tillganglig
        if (!self::isTcpdfAvailable()) {
            throw new PdfEngineException(
                'TCPDF is required for PDF export in v3.0.2. ' .
                'Install TCPDF: composer require tecnickcom/tcpdf'
            );
        }

        $this->metadata = [
            'platform_version' => AnalyticsConfig::PLATFORM_VERSION,
            'calculation_version' => AnalyticsConfig::CALCULATION_VERSION,
            'snapshot_id' => $snapshotId,
            'generated_at' => date('Y-m-d H:i:s'),
            'generated_at_utc' => gmdate('Y-m-d\TH:i:s\Z'),
            'pdf_engine' => 'TCPDF',
            'pdf_engine_version' => self::getTcpdfVersion(),
        ];
    }

    /**
     * Kontrollera om TCPDF ar tillganglig
     *
     * @return bool
     */
    public static function isTcpdfAvailable(): bool {
        if (self::$tcpdfAvailable !== null) {
            return self::$tcpdfAvailable;
        }

        // Kolla om TCPDF ar installerat via Composer
        $composerAutoload = __DIR__ . '/../../vendor/autoload.php';
        if (file_exists($composerAutoload)) {
            require_once $composerAutoload;
        }

        // Kolla kanda platser for TCPDF
        $paths = [
            __DIR__ . '/../../vendor/tecnickcom/tcpdf/tcpdf.php',
            __DIR__ . '/../../../vendor/tecnickcom/tcpdf/tcpdf.php',
            '/usr/share/php/tcpdf/tcpdf.php',
            __DIR__ . '/tcpdf/tcpdf.php',
        ];

        foreach ($paths as $path) {
            if (file_exists($path)) {
                self::$tcpdfPath = $path;
                self::$tcpdfAvailable = true;
                return true;
            }
        }

        // Kolla om klassen redan ar laddad
        if (class_exists('TCPDF', false)) {
            self::$tcpdfAvailable = true;
            return true;
        }

        self::$tcpdfAvailable = false;
        return false;
    }

    /**
     * Hamta TCPDF version
     *
     * @return string
     */
    public static function getTcpdfVersion(): string {
        if (!self::isTcpdfAvailable()) {
            return 'NOT_INSTALLED';
        }

        if (self::$tcpdfPath && !class_exists('TCPDF', false)) {
            require_once self::$tcpdfPath;
        }

        if (defined('TCPDF_VERSION')) {
            return TCPDF_VERSION;
        }

        return 'UNKNOWN';
    }

    /**
     * Hamta PDF engine status for diagnostik
     *
     * @return array
     */
    public static function getPdfEngineStatus(): array {
        return [
            'engine' => 'TCPDF',
            'available' => self::isTcpdfAvailable(),
            'version' => self::getTcpdfVersion(),
            'path' => self::$tcpdfPath,
            'status' => self::isTcpdfAvailable() ? 'OK' : 'MISSING (CRITICAL)',
            'fallback_allowed' => false,
            'policy' => 'TCPDF is MANDATORY in v3.0.2. No HTML fallback.',
        ];
    }

    /**
     * Satt titel for rapporten
     *
     * @param string $title Huvudtitel
     * @param string $subtitle Undertitel (optional)
     * @return self
     */
    public function setTitle(string $title, string $subtitle = ''): self {
        $this->title = $title;
        $this->subtitle = $subtitle;
        return $this;
    }

    /**
     * Satt sasong/ar
     *
     * @param int $year Sasong
     * @return self
     */
    public function setSeasonYear(int $year): self {
        $this->seasonYear = $year;
        $this->metadata['season_year'] = $year;
        return $this;
    }

    /**
     * Lagg till en text-sektion
     *
     * @param string $heading Rubrik
     * @param string $content Innehall (kan vara HTML eller Markdown)
     * @return self
     */
    public function addSection(string $heading, string $content): self {
        $this->sections[] = [
            'type' => 'text',
            'heading' => $heading,
            'content' => $content,
        ];
        return $this;
    }

    /**
     * Lagg till en tabell
     *
     * @param string $heading Rubrik
     * @param array $headers Kolumnrubriker
     * @param array $rows Data-rader
     * @return self
     */
    public function addTable(string $heading, array $headers, array $rows): self {
        $this->sections[] = [
            'type' => 'table',
            'heading' => $heading,
            'headers' => $headers,
            'rows' => $rows,
        ];
        return $this;
    }

    /**
     * Lagg till ett diagram
     *
     * @param string $heading Rubrik
     * @param string $chartType Diagramtyp (line, bar, donut, stackedBar)
     * @param array $data Diagramdata
     * @param array $options Diagramoptioner
     * @return self
     */
    public function addChart(string $heading, string $chartType, array $data, array $options = []): self {
        $this->sections[] = [
            'type' => 'chart',
            'heading' => $heading,
            'chart_type' => $chartType,
            'data' => $data,
            'options' => $options,
        ];
        return $this;
    }

    /**
     * Lagg till KPI-definition som ska visas i Definition Box
     *
     * @param string $kpiKey KPI-nyckel
     * @param string|null $customDefinition Anpassad definition (eller hamta fran DB)
     * @return self
     */
    public function addKpiDefinition(string $kpiKey, ?string $customDefinition = null): self {
        if ($customDefinition) {
            $this->kpiDefinitions[$kpiKey] = $customDefinition;
        } else {
            // Hamta fran databasen
            $stmt = $this->pdo->prepare("
                SELECT definition_sv, definition, formula
                FROM analytics_kpi_definitions
                WHERE kpi_key = ?
                ORDER BY calculation_version DESC
                LIMIT 1
            ");
            $stmt->execute([$kpiKey]);
            $row = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($row) {
                $def = $row['definition_sv'] ?: $row['definition'];
                if ($row['formula']) {
                    $def .= " (Formel: {$row['formula']})";
                }
                $this->kpiDefinitions[$kpiKey] = $def;
            }
        }
        return $this;
    }

    /**
     * Lagg till flera standard-KPI-definitioner
     *
     * @param array $kpiKeys Lista med KPI-nycklar
     * @return self
     */
    public function addStandardKpiDefinitions(array $kpiKeys): self {
        foreach ($kpiKeys as $key) {
            $this->addKpiDefinition($key);
        }
        return $this;
    }

    /**
     * Bygg HTML-versionen av rapporten
     *
     * @return string HTML-kod
     */
    public function buildHtml(): string {
        $html = $this->getHtmlHeader();

        // Titel
        $html .= '<div class="report-header">';
        $html .= '<h1>' . htmlspecialchars($this->title) . '</h1>';
        if ($this->subtitle) {
            $html .= '<p class="subtitle">' . htmlspecialchars($this->subtitle) . '</p>';
        }
        $html .= '<p class="meta">Genererad: ' . $this->metadata['generated_at'] . '</p>';
        $html .= '</div>';

        // Sektioner
        foreach ($this->sections as $section) {
            $html .= $this->renderSection($section);
        }

        // MANDATORY: Definition Box
        $html .= $this->renderDefinitionBox();

        $html .= $this->getHtmlFooter();

        return $html;
    }

    /**
     * Rendera en sektion
     *
     * @param array $section Sektionsdata
     * @return string HTML
     */
    private function renderSection(array $section): string {
        $html = '<div class="section">';

        if ($section['heading']) {
            $html .= '<h2>' . htmlspecialchars($section['heading']) . '</h2>';
        }

        switch ($section['type']) {
            case 'text':
                $html .= '<div class="content">' . $section['content'] . '</div>';
                break;

            case 'table':
                $html .= $this->renderTable($section['headers'], $section['rows']);
                break;

            case 'chart':
                $html .= $this->renderChart($section['chart_type'], $section['data'], $section['options']);
                break;
        }

        $html .= '</div>';
        return $html;
    }

    /**
     * Rendera en tabell
     *
     * @param array $headers Kolumnrubriker
     * @param array $rows Data-rader
     * @return string HTML
     */
    private function renderTable(array $headers, array $rows): string {
        $html = '<table class="data-table">';
        $html .= '<thead><tr>';
        foreach ($headers as $header) {
            $html .= '<th>' . htmlspecialchars($header) . '</th>';
        }
        $html .= '</tr></thead>';

        $html .= '<tbody>';
        foreach ($rows as $row) {
            $html .= '<tr>';
            foreach ($row as $cell) {
                $html .= '<td>' . htmlspecialchars((string)$cell) . '</td>';
            }
            $html .= '</tr>';
        }
        $html .= '</tbody></table>';

        return $html;
    }

    /**
     * Rendera ett diagram
     *
     * @param string $type Diagramtyp
     * @param array $data Data
     * @param array $options Optioner
     * @return string HTML
     */
    private function renderChart(string $type, array $data, array $options): string {
        $svg = match($type) {
            'line' => $this->chartRenderer->lineChart($data, $options),
            'bar' => $this->chartRenderer->barChart($data, $options),
            'donut' => $this->chartRenderer->donutChart($data, $options),
            'stackedBar' => $this->chartRenderer->stackedBarChart($data, $options),
            'sparkline' => $this->chartRenderer->sparkline($data['values'] ?? [], $options),
            default => '',
        };

        if (!$svg) {
            return '<p class="error">Kunde inte rendera diagram</p>';
        }

        // Konvertera till bild for PDF-kompatibilitet
        $dataUri = $this->chartRenderer->toDataUri($svg, true);

        return '<div class="chart"><img src="' . $dataUri . '" alt="Chart" /></div>';
    }

    /**
     * Rendera Definition Box (MANDATORY for alla PDF-exporter)
     *
     * @return string HTML
     */
    private function renderDefinitionBox(): string {
        $html = '<div class="definition-box">';
        $html .= '<h3>Definitions & Provenance</h3>';

        // Metadata
        $html .= '<div class="meta-section">';
        $html .= '<h4>Report Metadata</h4>';
        $html .= '<ul>';
        $html .= '<li><strong>Generated:</strong> ' . $this->metadata['generated_at'] . '</li>';
        $html .= '<li><strong>Platform Version:</strong> ' . $this->metadata['platform_version'] . '</li>';
        $html .= '<li><strong>Calculation Version:</strong> ' . $this->metadata['calculation_version'] . '</li>';
        $html .= '<li><strong>Snapshot ID:</strong> #' . $this->snapshotId . '</li>';
        if ($this->seasonYear) {
            $html .= '<li><strong>Season:</strong> ' . $this->seasonYear . '</li>';
        }
        $html .= '</ul>';
        $html .= '</div>';

        // KPI Definitions
        if (!empty($this->kpiDefinitions)) {
            $html .= '<div class="kpi-definitions">';
            $html .= '<h4>KPI Definitions</h4>';
            $html .= '<dl>';
            foreach ($this->kpiDefinitions as $key => $definition) {
                $html .= '<dt>' . htmlspecialchars($this->formatKpiName($key)) . '</dt>';
                $html .= '<dd>' . htmlspecialchars($definition) . '</dd>';
            }
            $html .= '</dl>';
            $html .= '</div>';
        }

        // Reproducibility note
        $html .= '<div class="reproducibility">';
        $html .= '<h4>Reproducibility</h4>';
        $html .= '<p>This report can be reproduced using snapshot #' . $this->snapshotId . '. ';
        $html .= 'Contact system administrator for verification.</p>';
        $html .= '</div>';

        // GDPR note
        $html .= '<div class="gdpr-note">';
        $html .= '<p class="small">Data processed in accordance with GDPR. ';
        $html .= 'Personal data is anonymized where applicable.</p>';
        $html .= '</div>';

        $html .= '</div>';

        return $html;
    }

    /**
     * Formatera KPI-nyckel till lasbart namn
     *
     * @param string $key KPI-nyckel
     * @return string Lasbart namn
     */
    private function formatKpiName(string $key): string {
        return ucwords(str_replace('_', ' ', $key));
    }

    /**
     * Hamta HTML header med CSS
     *
     * @return string HTML header
     */
    private function getHtmlHeader(): string {
        return '<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>' . htmlspecialchars($this->title) . '</title>
    <style>
        :root {
            --color-accent: #37d4d6;
            --color-bg: #0b131e;
            --color-card: #0e1621;
            --color-text: #f8f2f0;
            --color-text-secondary: #c7cfdd;
            --color-border: rgba(55, 212, 214, 0.2);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: "Manrope", "Segoe UI", sans-serif;
            background: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
            padding: 40px;
        }

        .report-header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--color-accent);
        }

        h1 {
            font-family: "Oswald", sans-serif;
            font-size: 2.5em;
            color: var(--color-accent);
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 1.2em;
            color: var(--color-text-secondary);
        }

        .meta {
            font-size: 0.9em;
            color: var(--color-text-secondary);
            margin-top: 10px;
        }

        .section {
            margin-bottom: 40px;
        }

        h2 {
            font-family: "Cabin Condensed", sans-serif;
            font-size: 1.5em;
            color: var(--color-accent);
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--color-border);
        }

        .content { color: var(--color-text-secondary); }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }

        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--color-border);
        }

        .data-table th {
            background: rgba(55, 212, 214, 0.1);
            color: var(--color-accent);
            font-weight: 600;
        }

        .data-table tr:hover { background: rgba(55, 212, 214, 0.05); }

        .chart {
            text-align: center;
            margin: 20px 0;
        }

        .chart img {
            max-width: 100%;
            height: auto;
        }

        /* Definition Box - MANDATORY */
        .definition-box {
            margin-top: 60px;
            padding: 25px;
            background: var(--color-card);
            border: 2px solid var(--color-border);
            border-radius: 10px;
            page-break-inside: avoid;
        }

        .definition-box h3 {
            color: var(--color-accent);
            font-size: 1.3em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--color-border);
        }

        .definition-box h4 {
            color: var(--color-text);
            font-size: 1em;
            margin: 15px 0 10px;
        }

        .definition-box ul {
            list-style: none;
            padding-left: 0;
        }

        .definition-box li {
            color: var(--color-text-secondary);
            margin-bottom: 5px;
            font-size: 0.9em;
        }

        .definition-box dl {
            margin: 10px 0;
        }

        .definition-box dt {
            color: var(--color-text);
            font-weight: 600;
            margin-top: 10px;
        }

        .definition-box dd {
            color: var(--color-text-secondary);
            margin-left: 15px;
            font-size: 0.9em;
        }

        .definition-box .small {
            font-size: 0.8em;
            color: var(--color-text-secondary);
            font-style: italic;
        }

        .error {
            color: #ef4444;
            font-style: italic;
        }

        @media print {
            body { background: white; color: black; padding: 20px; }
            :root {
                --color-accent: #0066cc;
                --color-text: #000;
                --color-text-secondary: #333;
                --color-border: #ccc;
                --color-card: #f5f5f5;
            }
            .definition-box { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
';
    }

    /**
     * Hamta HTML footer
     *
     * @return string HTML footer
     */
    private function getHtmlFooter(): string {
        return '
<footer style="margin-top: 40px; text-align: center; color: var(--color-text-secondary); font-size: 0.8em;">
    <p>TheHUB Analytics Platform ' . AnalyticsConfig::PLATFORM_VERSION . ' | GravitySeries</p>
</footer>
</body>
</html>';
    }

    /**
     * Exportera till PDF
     *
     * v3.0.2: TCPDF ar OBLIGATORISK. Ingen fallback.
     *
     * @param string|null $outputPath Filsokvag (null = returnera binart)
     * @return string|bool PDF-data eller true vid fil-export
     * @throws PdfEngineException Om TCPDF saknas
     */
    public function exportToPdf(?string $outputPath = null): string|bool {
        // v3.0.2: Strikt validering
        if (!self::isTcpdfAvailable()) {
            throw new PdfEngineException(
                'TCPDF is required for PDF export. HTML fallback is NOT allowed in v3.0.2. ' .
                'Install TCPDF: composer require tecnickcom/tcpdf'
            );
        }

        return $this->exportWithTcpdf($outputPath);
    }

    /**
     * Exportera med TCPDF
     *
     * @param string|null $outputPath Utfil
     * @return string|bool PDF data eller true
     */
    private function exportWithTcpdf(?string $outputPath): string|bool {
        // Ladda TCPDF
        if (self::$tcpdfPath && !class_exists('TCPDF', false)) {
            require_once self::$tcpdfPath;
        }

        // Skapa TCPDF-instans
        $pdf = new \TCPDF('P', 'mm', 'A4', true, 'UTF-8', false);

        // Metadata
        $pdf->SetCreator('TheHUB Analytics Platform');
        $pdf->SetAuthor('GravitySeries');
        $pdf->SetTitle($this->title);
        $pdf->SetSubject('Analytics Report');
        $pdf->SetKeywords('analytics, report, gravityseries, thehub');

        // Ta bort default header/footer
        $pdf->setPrintHeader(false);
        $pdf->setPrintFooter(false);

        // Marginaler
        $pdf->SetMargins(15, 15, 15);
        $pdf->SetAutoPageBreak(true, 15);

        // Lagg till sida
        $pdf->AddPage();

        // Generera HTML
        $html = $this->buildHtmlForTcpdf();

        // Skriv HTML till PDF
        $pdf->writeHTML($html, true, false, true, false, '');

        // Output
        if ($outputPath) {
            $pdf->Output($outputPath, 'F');
            return true;
        }

        return $pdf->Output('', 'S');
    }

    /**
     * Bygg HTML optimerad for TCPDF
     *
     * TCPDF har begransat CSS-stod, sa vi anvander enklare markup.
     *
     * @return string HTML
     */
    private function buildHtmlForTcpdf(): string {
        $html = '<style>
            h1 { color: #37d4d6; font-size: 24pt; margin-bottom: 5mm; }
            h2 { color: #37d4d6; font-size: 14pt; margin-top: 8mm; margin-bottom: 3mm; border-bottom: 1px solid #37d4d6; }
            h3 { color: #333; font-size: 12pt; margin-top: 5mm; }
            h4 { color: #333; font-size: 10pt; margin-top: 3mm; }
            p { font-size: 10pt; line-height: 1.4; }
            .subtitle { color: #666; font-size: 12pt; }
            .meta { color: #888; font-size: 9pt; }
            table { border-collapse: collapse; width: 100%; }
            th { background-color: #37d4d6; color: #fff; padding: 3mm; text-align: left; font-size: 9pt; }
            td { padding: 2mm; border-bottom: 1px solid #ddd; font-size: 9pt; }
            .definition-box { background-color: #f5f5f5; border: 1px solid #37d4d6; padding: 5mm; margin-top: 10mm; }
            .small { font-size: 8pt; color: #666; }
            dt { font-weight: bold; margin-top: 2mm; }
            dd { margin-left: 5mm; color: #444; }
        </style>';

        // Titel
        $html .= '<h1>' . htmlspecialchars($this->title) . '</h1>';
        if ($this->subtitle) {
            $html .= '<p class="subtitle">' . htmlspecialchars($this->subtitle) . '</p>';
        }
        $html .= '<p class="meta">Genererad: ' . $this->metadata['generated_at'] . '</p>';

        // Sektioner
        foreach ($this->sections as $section) {
            $html .= $this->renderSectionForTcpdf($section);
        }

        // MANDATORY: Definition Box
        $html .= $this->renderDefinitionBoxForTcpdf();

        // Footer
        $html .= '<br><p class="small" style="text-align: center;">TheHUB Analytics Platform ' .
                 AnalyticsConfig::PLATFORM_VERSION . ' | GravitySeries</p>';

        return $html;
    }

    /**
     * Rendera sektion for TCPDF
     *
     * @param array $section
     * @return string HTML
     */
    private function renderSectionForTcpdf(array $section): string {
        $html = '';

        if (!empty($section['heading'])) {
            $html .= '<h2>' . htmlspecialchars($section['heading']) . '</h2>';
        }

        switch ($section['type']) {
            case 'text':
                $html .= '<p>' . $section['content'] . '</p>';
                break;

            case 'table':
                $html .= $this->renderTableForTcpdf($section['headers'], $section['rows']);
                break;

            case 'chart':
                // TCPDF stodjer SVG begransat - vi embeddar som base64 bild
                $html .= $this->renderChartForTcpdf($section['chart_type'], $section['data'], $section['options']);
                break;
        }

        return $html;
    }

    /**
     * Rendera tabell for TCPDF
     *
     * @param array $headers
     * @param array $rows
     * @return string HTML
     */
    private function renderTableForTcpdf(array $headers, array $rows): string {
        $html = '<table border="0" cellpadding="3">';
        $html .= '<tr>';
        foreach ($headers as $header) {
            $html .= '<th>' . htmlspecialchars($header) . '</th>';
        }
        $html .= '</tr>';

        foreach ($rows as $row) {
            $html .= '<tr>';
            foreach ($row as $cell) {
                $html .= '<td>' . htmlspecialchars((string)$cell) . '</td>';
            }
            $html .= '</tr>';
        }

        $html .= '</table>';
        return $html;
    }

    /**
     * Rendera diagram for TCPDF
     *
     * @param string $type
     * @param array $data
     * @param array $options
     * @return string HTML
     */
    private function renderChartForTcpdf(string $type, array $data, array $options): string {
        $svg = match($type) {
            'line' => $this->chartRenderer->lineChart($data, $options),
            'bar' => $this->chartRenderer->barChart($data, $options),
            'donut' => $this->chartRenderer->donutChart($data, $options),
            'stackedBar' => $this->chartRenderer->stackedBarChart($data, $options),
            'sparkline' => $this->chartRenderer->sparkline($data['values'] ?? [], $options),
            default => '',
        };

        if (!$svg) {
            return '<p><em>[Diagram kunde inte renderas]</em></p>';
        }

        // Konvertera till base64 for embedding
        $base64 = base64_encode($svg);
        return '<p><img src="@' . $base64 . '" width="400" /></p>';
    }

    /**
     * Rendera Definition Box for TCPDF
     *
     * @return string HTML
     */
    private function renderDefinitionBoxForTcpdf(): string {
        $html = '<div class="definition-box">';
        $html .= '<h3>DEFINITIONS &amp; PROVENANCE</h3>';

        // Metadata
        $html .= '<h4>Report Metadata</h4>';
        $html .= '<ul>';
        $html .= '<li><strong>Generated:</strong> ' . $this->metadata['generated_at'] . '</li>';
        $html .= '<li><strong>Platform Version:</strong> ' . $this->metadata['platform_version'] . '</li>';
        $html .= '<li><strong>Calculation Version:</strong> ' . $this->metadata['calculation_version'] . '</li>';
        $html .= '<li><strong>Snapshot ID:</strong> #' . $this->snapshotId . '</li>';
        $html .= '<li><strong>PDF Engine:</strong> TCPDF ' . self::getTcpdfVersion() . '</li>';
        if ($this->seasonYear) {
            $html .= '<li><strong>Season:</strong> ' . $this->seasonYear . '</li>';
        }
        $html .= '</ul>';

        // KPI Definitions
        if (!empty($this->kpiDefinitions)) {
            $html .= '<h4>KPI Definitions</h4>';
            $html .= '<dl>';
            foreach ($this->kpiDefinitions as $key => $definition) {
                $html .= '<dt>' . htmlspecialchars($this->formatKpiName($key)) . '</dt>';
                $html .= '<dd>' . htmlspecialchars($definition) . '</dd>';
            }
            $html .= '</dl>';
        }

        // Reproducibility
        $html .= '<h4>Reproducibility</h4>';
        $html .= '<p>This report can be reproduced using snapshot #' . $this->snapshotId . '. ';
        $html .= 'Contact system administrator for verification.</p>';

        // GDPR
        $html .= '<p class="small">Data processed in accordance with GDPR. Personal data is anonymized where applicable.</p>';

        $html .= '</div>';
        return $html;
    }

    /**
     * Hitta wkhtmltopdf binary
     *
     * @deprecated Anvand TCPDF istallet (v3.0.2)
     * @return string|null Sokvag eller null
     */
    private function findWkhtmltopdf(): ?string {
        // wkhtmltopdf ar DEPRECATED i v3.0.2
        // Returnerar alltid null for att tvinga TCPDF-anvandning
        return null;
    }

    /**
     * Logga exporten
     *
     * @param string $exportType Typ av rapport
     * @param array $data Exporterad data
     * @param array $options Extra optioner
     * @return int Export ID
     */
    public function logExport(string $exportType, array $data, array $options = []): int {
        $options['snapshot_id'] = $this->snapshotId;
        $options['year'] = $this->seasonYear;
        $options['format'] = 'pdf';

        return $this->logger->logExport($exportType, $data, $options);
    }

    /**
     * Hamta snapshot-information
     *
     * @return array|null Snapshot data
     */
    public function getSnapshotInfo(): ?array {
        $stmt = $this->pdo->prepare("
            SELECT * FROM analytics_snapshots WHERE id = ?
        ");
        $stmt->execute([$this->snapshotId]);

        return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
    }
}
