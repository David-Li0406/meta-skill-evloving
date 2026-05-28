/**
 * TheHUB V1.0 - WooCommerce Integration
 * Handles checkout modal and payment flow
 */

const WooCommerce = {
    modal: null,
    iframe: null,
    loading: null,

    init() {
        this.modal = document.getElementById('wc-modal');
        this.iframe = document.getElementById('wc-modal-iframe');
        this.loading = document.getElementById('wc-modal-loading');

        if (!this.modal) return;

        // Bind close buttons
        document.querySelectorAll('[data-action="close-modal"]').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal.classList.contains('hidden')) {
                this.closeModal();
            }
        });

        // Listen for iframe load
        if (this.iframe) {
            this.iframe.addEventListener('load', () => {
                this.hideLoading();
            });
        }

        // Listen for messages from iframe (payment completion)
        window.addEventListener('message', (e) => {
            this.handleMessage(e);
        });
    },

    openCheckout(url) {
        if (!this.modal || !this.iframe) {
            // Fallback to direct navigation
            window.location.href = url;
            return;
        }

        // Show modal and loading
        this.modal.classList.remove('hidden');
        this.showLoading();
        document.body.style.overflow = 'hidden';

        // Load URL in iframe
        this.iframe.src = url;

        // Focus trap
        this.modal.focus();
    },

    closeModal() {
        if (!this.modal) return;

        this.modal.classList.add('hidden');
        document.body.style.overflow = '';

        // Clear iframe
        if (this.iframe) {
            this.iframe.src = '';
        }
    },

    showLoading() {
        if (this.loading) {
            this.loading.classList.remove('hidden');
        }
    },

    hideLoading() {
        if (this.loading) {
            this.loading.classList.add('hidden');
        }
    },

    handleMessage(event) {
        // Only accept messages from same origin or WooCommerce domain
        const allowedOrigins = [
            window.location.origin,
            'https://gravityseries.se',
            'https://www.gravityseries.se'
        ];

        if (!allowedOrigins.includes(event.origin)) {
            return;
        }

        const data = event.data;

        if (typeof data !== 'object') return;

        switch (data.type) {
            case 'payment_complete':
            case 'wc_order_complete':
                this.handlePaymentComplete(data);
                break;

            case 'payment_cancelled':
            case 'wc_checkout_cancelled':
                this.handlePaymentCancelled();
                break;

            case 'resize_iframe':
                if (data.height && this.iframe) {
                    this.iframe.style.height = data.height + 'px';
                }
                break;
        }
    },

    handlePaymentComplete(data) {
        this.closeModal();

        // Show success message
        this.showNotification('Betalning genomförd!', 'success');

        // Redirect to registrations page
        setTimeout(() => {
            window.location.href = '/profile/registrations?success=1';
        }, 1500);
    },

    handlePaymentCancelled() {
        this.closeModal();
        this.showNotification('Betalning avbruten', 'info');
    },

    showNotification(message, type = 'info') {
        // Use Registration's toast if available, otherwise create own
        if (typeof Registration !== 'undefined' && Registration.showMessage) {
            Registration.showMessage(message, type);
            return;
        }

        // Create simple notification
        const notification = document.createElement('div');
        notification.className = `wc-notification wc-notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 24px;
            background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            border-radius: 8px;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => WooCommerce.init());
} else {
    WooCommerce.init();
}

// Export for external use
window.WooCommerce = WooCommerce;
