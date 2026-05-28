/**
 * TheHUB V1.0 - Registration Flow
 * Handles multi-participant event registration
 */

const Registration = {
    participants: [],
    eventId: null,
    eventClasses: [],

    init() {
        const container = document.querySelector('[data-event-id]');
        if (!container) return;

        this.eventId = container.dataset.eventId;
        this.loadEventClasses();
        this.bindEvents();
    },

    bindEvents() {
        // Quick-add self
        document.querySelectorAll('[data-action="add-self"]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.addExistingRider(btn.dataset.riderId);
            });
        });

        // Quick-add child
        document.querySelectorAll('[data-action="add-rider"]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.addExistingRider(btn.dataset.riderId);
            });
        });

        // Checkout button
        document.querySelector('[data-action="checkout"]')?.addEventListener('click', () => {
            this.checkout();
        });

        // Listen for search selection
        document.addEventListener('search:select', (e) => {
            if (e.detail.type === 'rider') {
                this.addExistingRider(e.detail.id);
            }
        });
    },

    async loadEventClasses() {
        try {
            const response = await fetch(`/api/registration.php?action=event_classes&event_id=${this.eventId}`);
            const data = await response.json();
            if (data.success) {
                this.eventClasses = data.classes;
            }
        } catch (error) {
            console.error('Failed to load event classes:', error);
        }
    },

    async addExistingRider(riderId) {
        // Check if already added
        if (this.participants.find(p => p.rider_id == riderId)) {
            this.showMessage('Åkaren är redan tillagd', 'warning');
            return;
        }

        try {
            const response = await fetch(
                `/api/registration.php?action=get_rider&rider_id=${riderId}&event_id=${this.eventId}`
            );
            const data = await response.json();

            if (!data.success) {
                this.showMessage(data.error || 'Kunde inte hämta åkare', 'error');
                return;
            }

            if (!data.eligible_classes || data.eligible_classes.length === 0) {
                this.showMessage('Åkaren är inte behörig för någon klass i detta event', 'error');
                return;
            }

            this.participants.push({
                rider_id: riderId,
                name: data.name,
                class_id: data.suggested_class_id,
                class_name: data.suggested_class_name,
                price: data.price,
                eligible_classes: data.eligible_classes
            });

            this.updateUI();
            this.showMessage(`${data.name} tillagd`, 'success');

        } catch (error) {
            console.error('Error adding rider:', error);
            this.showMessage('Ett fel uppstod', 'error');
        }
    },

    updateUI() {
        const list = document.getElementById('selected-participants');
        const summary = document.getElementById('registration-summary');

        if (!list) return;

        if (this.participants.length === 0) {
            list.innerHTML = '<p class="text-muted">Inga deltagare valda än.</p>';
            if (summary) summary.style.display = 'none';
            return;
        }

        list.innerHTML = this.participants.map((p, i) => `
            <div class="registration-participant">
                <div class="participant-avatar">${p.name.charAt(0).toUpperCase()}</div>
                <div class="participant-info">
                    <span class="participant-name">${this.escapeHtml(p.name)}</span>
                    <select class="participant-class" data-index="${i}" onchange="Registration.updateClass(${i}, this.value)">
                        ${p.eligible_classes.map(c => `
                            <option value="${c.class_id}" ${c.class_id == p.class_id ? 'selected' : ''}>
                                ${this.escapeHtml(c.class_name)}
                            </option>
                        `).join('')}
                    </select>
                </div>
                <span class="participant-price">${p.price} kr</span>
                <button type="button" class="participant-remove" onclick="Registration.remove(${i})" aria-label="Ta bort">
                    ✕
                </button>
            </div>
        `).join('');

        // Update summary
        if (summary) {
            const total = this.participants.reduce((sum, p) => sum + (p.price || 0), 0);
            document.getElementById('summary-total').textContent = `${total} kr`;
            summary.style.display = 'block';
        }
    },

    updateClass(index, classId) {
        const participant = this.participants[index];
        if (!participant) return;

        const newClass = participant.eligible_classes.find(c => c.class_id == classId);
        if (newClass) {
            participant.class_id = newClass.class_id;
            participant.class_name = newClass.class_name;
            // Price might need to be fetched - for now keep same
        }

        this.updateUI();
    },

    remove(index) {
        const removed = this.participants.splice(index, 1)[0];
        this.updateUI();
        if (removed) {
            this.showMessage(`${removed.name} borttagen`, 'info');
        }
    },

    async checkout() {
        if (this.participants.length === 0) {
            this.showMessage('Lägg till minst en deltagare', 'warning');
            return;
        }

        const checkoutBtn = document.querySelector('[data-action="checkout"]');
        if (checkoutBtn) {
            checkoutBtn.disabled = true;
            checkoutBtn.textContent = 'Skapar anmälan...';
        }

        try {
            const response = await fetch('/api/registration.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    event_id: this.eventId,
                    participants: this.participants.map(p => ({
                        rider_id: p.rider_id,
                        class_id: p.class_id,
                        price: p.price
                    }))
                })
            });

            const data = await response.json();

            if (!data.success) {
                if (data.errors) {
                    this.showMessage(data.errors.join('\n'), 'error');
                } else {
                    this.showMessage(data.error || 'Anmälan misslyckades', 'error');
                }
                return;
            }

            // Success - redirect to checkout or show modal
            if (data.checkout_url) {
                if (typeof WooCommerce !== 'undefined' && WooCommerce.openCheckout) {
                    WooCommerce.openCheckout(data.checkout_url);
                } else {
                    window.location.href = data.checkout_url;
                }
            } else {
                this.showMessage('Anmälan skapad!', 'success');
                this.participants = [];
                this.updateUI();
            }

        } catch (error) {
            console.error('Checkout error:', error);
            this.showMessage('Ett fel uppstod vid anmälan', 'error');
        } finally {
            if (checkoutBtn) {
                checkoutBtn.disabled = false;
                checkoutBtn.textContent = 'Gå till betalning';
            }
        }
    },

    showMessage(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;

        // Find or create toast container
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        container.appendChild(toast);

        // Animate in
        requestAnimationFrame(() => {
            toast.classList.add('visible');
        });

        // Remove after delay
        setTimeout(() => {
            toast.classList.remove('visible');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Registration.init());
} else {
    Registration.init();
}

// Export for external use
window.Registration = Registration;
