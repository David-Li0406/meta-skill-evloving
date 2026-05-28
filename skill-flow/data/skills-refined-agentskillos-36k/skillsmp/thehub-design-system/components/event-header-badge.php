<?php
/**
 * Event Header Badge Component
 *
 * Renders a wide-format event header with gradient background,
 * event info, and optional sponsor logos.
 *
 * Usage:
 *   <?php render_event_header_badge($event, $options); ?>
 *
 * Expected $event array:
 *   - name: string (required)
 *   - date: string (required)
 *   - location: string (optional)
 *   - discipline: string (optional)
 *   - status: string (optional) - 'upcoming', 'ongoing', 'completed', 'cancelled'
 *   - series: array (optional) - Associated series with gradient_start, gradient_end, accent_color
 *
 * Options:
 *   - sponsors: array (optional) - Array of sponsor data for header display
 *   - gradient_start: string (optional) - Override gradient start color
 *   - gradient_end: string (optional) - Override gradient end color
 *   - accent_color: string (optional) - Override accent color
 *   - show_status: bool (default: true)
 *   - cta_text: string (optional) - Call-to-action button text
 *   - cta_url: string (optional) - Call-to-action button URL
 */

if (!function_exists('render_event_header_badge')) {
    /**
     * Render an event header badge
     *
     * @param array $event Event data
     * @param array $options Display options
     * @return void Outputs HTML directly
     */
    function render_event_header_badge(array $event, array $options = []): void {
        // Extract event data
        $name = htmlspecialchars($event['name'] ?? 'Event');
        $date = $event['date'] ?? '';
        $location = htmlspecialchars($event['location'] ?? '');
        $discipline = $event['discipline'] ?? '';
        $status = $event['status'] ?? 'upcoming';
        $series = $event['series'] ?? [];

        // Extract options
        $sponsors = $options['sponsors'] ?? [];
        $showStatus = $options['show_status'] ?? true;
        $ctaText = $options['cta_text'] ?? '';
        $ctaUrl = $options['cta_url'] ?? '';

        // Get gradient colors (priority: options > series > defaults)
        $gradientStart = $options['gradient_start'] ?? $series['gradient_start'] ?? '#004A98';
        $gradientEnd = $options['gradient_end'] ?? $series['gradient_end'] ?? '#001f3f';
        $accentColor = $options['accent_color'] ?? $series['accent_color'] ?? '#61CE70';

        // Format date
        $formattedDate = '';
        if ($date) {
            $dateObj = is_string($date) ? new DateTime($date) : $date;
            $formattedDate = $dateObj->format('j M Y');
        }

        // Status label mapping
        $statusLabels = [
            'upcoming' => 'KOMMANDE',
            'ongoing' => 'LIVE',
            'completed' => 'AVSLUTAD',
            'cancelled' => 'INSTÄLLD'
        ];
        $statusLabel = $statusLabels[$status] ?? strtoupper($status);

        // Accent name for CSS class
        $accentName = function_exists('hub_get_accent_name')
            ? hub_get_accent_name($accentColor)
            : 'green';

        ?>
        <div class="badge-event-header"
             style="--badge-gradient-start: <?= htmlspecialchars($gradientStart) ?>;
                    --badge-gradient-end: <?= htmlspecialchars($gradientEnd) ?>;
                    --badge-accent: <?= htmlspecialchars($accentColor) ?>;">

            <?php if ($showStatus && $status): ?>
                <span class="badge-status badge-status-<?= htmlspecialchars($status) ?>">
                    <?= $statusLabel ?>
                </span>
            <?php endif; ?>

            <div class="badge-event-header-content">
                <?php if ($discipline): ?>
                    <span class="badge-discipline" data-accent="<?= htmlspecialchars($accentName) ?>">
                        <?= htmlspecialchars($discipline) ?>
                    </span>
                <?php endif; ?>

                <h1 class="badge-title"><?= $name ?></h1>

                <p class="badge-meta">
                    <?php if ($formattedDate): ?>
                        <span class="badge-date"><?= $formattedDate ?></span>
                    <?php endif; ?>
                    <?php if ($formattedDate && $location): ?>
                        <span class="badge-separator"> • </span>
                    <?php endif; ?>
                    <?php if ($location): ?>
                        <span class="badge-location"><?= $location ?></span>
                    <?php endif; ?>
                </p>

                <?php if ($ctaText && $ctaUrl): ?>
                    <a href="<?= htmlspecialchars($ctaUrl) ?>" class="badge-cta">
                        <?= htmlspecialchars($ctaText) ?>
                        <span class="badge-cta-arrow">→</span>
                    </a>
                <?php endif; ?>
            </div>

            <?php if (!empty($sponsors)): ?>
                <div class="badge-event-header-sponsors">
                    <?php foreach ($sponsors as $sponsor): ?>
                        <?php
                        $sponsorLogo = $sponsor['logo'] ?? '';
                        $sponsorName = htmlspecialchars($sponsor['name'] ?? '');
                        $sponsorUrl = $sponsor['website'] ?? '';
                        ?>
                        <?php if ($sponsorLogo): ?>
                            <?php if ($sponsorUrl): ?>
                                <a href="<?= htmlspecialchars($sponsorUrl) ?>"
                                   target="_blank"
                                   rel="noopener sponsored"
                                   title="<?= $sponsorName ?>">
                                    <img src="<?= htmlspecialchars($sponsorLogo) ?>"
                                         alt="<?= $sponsorName ?>"
                                         class="badge-event-sponsor-logo"
                                         loading="lazy">
                                </a>
                            <?php else: ?>
                                <img src="<?= htmlspecialchars($sponsorLogo) ?>"
                                     alt="<?= $sponsorName ?>"
                                     class="badge-event-sponsor-logo"
                                     loading="lazy">
                            <?php endif; ?>
                        <?php endif; ?>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
        </div>
        <?php
    }
}

// If this file is included with $event set, render it
if (isset($event) && is_array($event)) {
    $headerOptions = $headerOptions ?? [];
    render_event_header_badge($event, $headerOptions);
}
