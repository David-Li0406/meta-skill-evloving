<?php
/**
 * TheHUB V1.0 - Footer
 * Theme toggle removed - users can change theme in profile settings
 */

// Get version info
$versionInfo = null;
if (function_exists('getVersionInfo')) {
    $versionInfo = getVersionInfo();
}
?>
<footer class="site-footer">
    <div class="footer-content">
        <p class="footer-copyright">
            &copy; <?= date('Y') ?> TheHUB
            <?php if ($versionInfo): ?>
            <span class="footer-version">
                v<?= htmlspecialchars($versionInfo['version']) ?>
                <?php if (!empty($versionInfo['build'])): ?>
                [<?= htmlspecialchars($versionInfo['build']) ?>.<?= str_pad($versionInfo['deployment'], 3, '0', STR_PAD_LEFT) ?>]
                <?php endif; ?>
                • <?= htmlspecialchars($versionInfo['name']) ?>
                <?php if (!empty($versionInfo['build_test'])): ?>
                • <strong style="color: #61CE70;"><?= htmlspecialchars($versionInfo['build_test']) ?></strong>
                <?php endif; ?>
            </span>
            <?php endif; ?>
        </p>
    </div>
</footer>

<style>
.site-footer {
    padding: var(--space-lg) var(--space-md);
    text-align: center;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    border-top: 1px solid var(--color-border);
    margin-top: auto;
}
.footer-content {
    max-width: 1200px;
    margin: 0 auto;
}
.footer-copyright {
    margin: 0;
}
.footer-version {
    display: block;
    font-size: var(--text-xs);
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}
@media (min-width: 600px) {
    .footer-version {
        display: inline;
        margin-top: 0;
        margin-left: var(--space-sm);
    }
}
</style>
