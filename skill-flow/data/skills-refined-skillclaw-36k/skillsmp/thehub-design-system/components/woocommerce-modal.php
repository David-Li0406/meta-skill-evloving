<?php
/**
 * TheHUB V1.0 - WooCommerce Checkout Modal
 * Displays checkout in an iframe modal
 */
?>
<div id="wc-modal" class="wc-modal hidden" role="dialog" aria-modal="true" aria-labelledby="wc-modal-title">
    <div class="wc-modal-backdrop" data-action="close-modal"></div>
    <div class="wc-modal-container">
        <div class="wc-modal-header">
            <h2 id="wc-modal-title">Betalning</h2>
            <button type="button" class="wc-modal-close" data-action="close-modal" aria-label="Stäng">
                ✕
            </button>
        </div>
        <div class="wc-modal-content">
            <div class="wc-modal-loading" id="wc-modal-loading">
                <div class="wc-spinner"></div>
                <p>Laddar betalning...</p>
            </div>
            <iframe id="wc-modal-iframe"
                    class="wc-modal-iframe"
                    title="Betalning"
                    sandbox="allow-forms allow-scripts allow-same-origin allow-popups"></iframe>
        </div>
        <div class="wc-modal-footer">
            <p class="wc-modal-secure">
                🔒 Säker betalning via GravitySeries butik
            </p>
        </div>
    </div>
</div>

<style>
.wc-modal {
    position: fixed;
    inset: 0;
    z-index: var(--z-modal, 1000);
    display: flex;
    align-items: center;
    justify-content: center;
}
.wc-modal.hidden {
    display: none;
}
.wc-modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
}
.wc-modal-container {
    position: relative;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    margin: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-xl);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
.wc-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}
.wc-modal-header h2 {
    font-size: var(--text-lg);
    font-weight: var(--weight-semibold);
}
.wc-modal-close {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-bg-card);
    border: none;
    border-radius: var(--radius-full);
    font-size: var(--text-lg);
    cursor: pointer;
    transition: all var(--transition-fast);
}
.wc-modal-close:hover {
    background: var(--color-bg-hover);
}
.wc-modal-content {
    flex: 1;
    position: relative;
    min-height: 400px;
}
.wc-modal-loading {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--space-md);
    background: var(--color-bg-surface);
}
.wc-modal-loading.hidden {
    display: none;
}
.wc-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--color-border);
    border-top-color: var(--color-accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
.wc-modal-iframe {
    width: 100%;
    height: 500px;
    border: none;
    background: white;
}
.wc-modal-footer {
    padding: var(--space-md) var(--space-lg);
    border-top: 1px solid var(--color-border);
    text-align: center;
}
.wc-modal-secure {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

@media (max-width: 600px) {
    .wc-modal-container {
        margin: 0;
        max-width: 100%;
        max-height: 100%;
        height: 100%;
        border-radius: 0;
    }
    .wc-modal-iframe {
        height: calc(100vh - 150px);
    }
}
</style>
