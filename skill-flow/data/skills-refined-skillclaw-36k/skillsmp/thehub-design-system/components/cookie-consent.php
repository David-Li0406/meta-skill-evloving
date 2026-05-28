<?php
/**
 * Cookie Consent Banner
 * Simple informational banner about cookie usage
 *
 * Since we only use necessary session cookies for login,
 * this is primarily informational (no blocking consent required).
 */
?>
<div id="cookieConsent" class="cookie-consent" style="display: none;">
    <div class="cookie-consent-content">
        <div class="cookie-consent-text">
            <i data-lucide="cookie"></i>
            <p>
                Vi använder cookies för att hantera inloggning och sessionsinformation.
                <a href="/integritetspolicy">Läs mer</a>
            </p>
        </div>
        <button type="button" class="cookie-consent-btn" onclick="acceptCookies()">
            OK, jag förstår
        </button>
    </div>
</div>

<style>
.cookie-consent {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--color-bg-card, #1a1a1a);
    border-top: 1px solid var(--color-border, #333);
    padding: var(--space-md, 16px);
    z-index: 9999;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.3);
}
/* Adjust for mobile nav */
@media (max-width: 767px) {
    .cookie-consent {
        bottom: calc(var(--mobile-nav-height, 65px) + env(safe-area-inset-bottom, 0px));
    }
}
.cookie-consent-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-md, 16px);
    flex-wrap: wrap;
}
.cookie-consent-text {
    display: flex;
    align-items: center;
    gap: var(--space-sm, 8px);
    flex: 1;
    min-width: 200px;
}
.cookie-consent-text i {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    color: var(--color-accent, #61CE70);
}
.cookie-consent-text p {
    margin: 0;
    font-size: var(--text-sm, 14px);
    color: var(--color-text-secondary, #999);
}
.cookie-consent-text a {
    color: var(--color-accent, #61CE70);
    text-decoration: underline;
}
.cookie-consent-btn {
    flex-shrink: 0;
    padding: var(--space-sm, 8px) var(--space-lg, 24px);
    background: var(--color-accent, #61CE70);
    color: #111;
    border: none;
    border-radius: var(--radius-sm, 6px);
    font-weight: 600;
    font-size: var(--text-sm, 14px);
    cursor: pointer;
    transition: all 0.15s ease;
}
.cookie-consent-btn:hover {
    background: #7dd88a;
    transform: translateY(-1px);
}
@media (max-width: 480px) {
    .cookie-consent-content {
        flex-direction: column;
        text-align: center;
    }
    .cookie-consent-text {
        flex-direction: column;
        text-align: center;
    }
    .cookie-consent-btn {
        width: 100%;
    }
}
</style>

<script>
// Check if consent already given
(function() {
    if (!localStorage.getItem('cookieConsent')) {
        document.getElementById('cookieConsent').style.display = 'block';
    }
})();

function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    document.getElementById('cookieConsent').style.display = 'none';
}
</script>
