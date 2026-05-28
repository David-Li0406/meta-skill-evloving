<?php
/**
 * Sponsor Badge Component
 *
 * Renders a sponsor badge with logo/name, tier styling, and optional link.
 *
 * Usage:
 *   <?php include_sponsor_badge($sponsor, $options); ?>
 *
 * Or inline:
 *   <?php require 'components/sponsor-badge.php'; ?>
 *
 * Expected $sponsor array:
 *   - name: string (required)
 *   - logo: string (optional) - URL to logo image
 *   - logo_dark: string (optional) - URL to dark theme logo
 *   - website: string (optional) - Sponsor website URL
 *   - tier: string (optional) - 'title', 'gold', 'silver', 'bronze'
 *
 * Options:
 *   - size: 'small', 'medium', 'large' (default: 'medium')
 *   - placement: string for tracking (default: 'unknown')
 *   - show_label: bool (default: true)
 *   - lazy: bool (default: true) - Use lazy loading for images
 */

if (!function_exists('render_sponsor_badge')) {
    /**
     * Render a sponsor badge HTML
     *
     * @param array $sponsor Sponsor data
     * @param array $options Display options
     * @return void Outputs HTML directly
     */
    function render_sponsor_badge(array $sponsor, array $options = []): void {
        // Extract sponsor data with defaults
        $name = htmlspecialchars($sponsor['name'] ?? 'Sponsor');
        $logo = $sponsor['logo'] ?? '';
        $logoDark = $sponsor['logo_dark'] ?? '';
        $website = $sponsor['website'] ?? '';
        $tier = $sponsor['tier'] ?? 'bronze';
        $slug = $sponsor['slug'] ?? '';

        // Extract options with defaults
        $size = $options['size'] ?? 'medium';
        $placement = $options['placement'] ?? 'unknown';
        $showLabel = $options['show_label'] ?? true;
        $lazy = $options['lazy'] ?? true;

        // Aspect ratio based on size
        $aspectRatio = match($size) {
            'small' => '2/1',
            'large' => '16/9',
            default => '3/2'
        };

        // Build tracking URL if website exists
        $href = '';
        if ($website) {
            $href = hub_sponsor_tracking_url($website, $name, $placement);
        }

        // Logo attributes
        $logoAttrs = '';
        if ($logo) {
            $logoAttrs .= sprintf(' src="%s"', htmlspecialchars($logo));
            if ($logoDark) {
                $logoAttrs .= sprintf(' data-light-src="%s"', htmlspecialchars($logo));
                $logoAttrs .= sprintf(' data-dark-src="%s"', htmlspecialchars($logoDark));
            }
            $logoAttrs .= sprintf(' alt="%s"', $name);
            if ($lazy) {
                $logoAttrs .= ' loading="lazy"';
            }
        }

        // Start output
        if ($website): ?>
            <a href="<?= htmlspecialchars($href) ?>"
               class="badge-sponsor"
               data-tier="<?= htmlspecialchars($tier) ?>"
               data-sponsor-name="<?= $name ?>"
               data-placement="<?= htmlspecialchars($placement) ?>"
               style="aspect-ratio: <?= $aspectRatio ?>;"
               target="_blank"
               rel="noopener sponsored"
               title="<?= $name ?>">
        <?php else: ?>
            <div class="badge-sponsor"
                 data-tier="<?= htmlspecialchars($tier) ?>"
                 data-sponsor-name="<?= $name ?>"
                 style="aspect-ratio: <?= $aspectRatio ?>;">
        <?php endif; ?>

            <?php if ($showLabel): ?>
                <span class="badge-sponsor-label">SPONSOR</span>
            <?php endif; ?>

            <?php if ($logo): ?>
                <img <?= $logoAttrs ?> class="badge-sponsor-logo">
            <?php else: ?>
                <span class="badge-sponsor-name"><?= $name ?></span>
            <?php endif; ?>

        <?php if ($website): ?>
            </a>
        <?php else: ?>
            </div>
        <?php endif;
    }
}

// If this file is included with $sponsor set, render it
if (isset($sponsor) && is_array($sponsor)) {
    $badgeOptions = $badgeOptions ?? [];
    render_sponsor_badge($sponsor, $badgeOptions);
}
