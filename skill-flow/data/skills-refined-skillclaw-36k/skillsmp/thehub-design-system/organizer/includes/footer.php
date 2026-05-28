<?php
/**
 * Organizer App - Footer
 */

if (!defined('THEHUB_INIT')) {
    die('Direct access not allowed');
}
?>
    </main>
</div>

<script>
    // Initialize Lucide icons
    lucide.createIcons();

    // Prevent zoom on double-tap (iPad)
    document.addEventListener('touchend', function(e) {
        const now = Date.now();
        if (now - (this.lastTouch || 0) < 300) {
            e.preventDefault();
        }
        this.lastTouch = now;
    }, { passive: false });

    // Global helper functions
    const OrgApp = {
        // Show loading state
        showLoading: function(element) {
            element.disabled = true;
            element.dataset.originalText = element.innerHTML;
            element.innerHTML = '<span class="org-spinner" style="width:24px;height:24px;border-width:3px;"></span>';
        },

        // Hide loading state
        hideLoading: function(element) {
            element.disabled = false;
            if (element.dataset.originalText) {
                element.innerHTML = element.dataset.originalText;
            }
        },

        // Show alert
        showAlert: function(message, type = 'error') {
            const existing = document.querySelector('.org-alert');
            if (existing) existing.remove();

            const alert = document.createElement('div');
            alert.className = `org-alert org-alert--${type}`;
            alert.textContent = message;

            const main = document.querySelector('.org-main');
            main.insertBefore(alert, main.firstChild);

            if (type !== 'error') {
                setTimeout(() => alert.remove(), 5000);
            }
        },

        // Format price
        formatPrice: function(amount) {
            return new Intl.NumberFormat('sv-SE', {
                style: 'currency',
                currency: 'SEK',
                minimumFractionDigits: 0
            }).format(amount);
        },

        // Debounce function for search
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // API call helper
        api: async function(endpoint, data = {}) {
            const response = await fetch(`<?= ORGANIZER_BASE_URL ?>/api/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    ...data,
                    csrf_token: '<?= generate_csrf_token() ?>'
                })
            });

            if (!response.ok) {
                throw new Error('Nätverksfel');
            }

            return response.json();
        }
    };
</script>

<?php if (isset($pageScripts)): ?>
    <?= $pageScripts ?>
<?php endif; ?>

</body>
</html>
