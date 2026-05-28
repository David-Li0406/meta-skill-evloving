/**
 * Dropdown toggle functionality
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-dropdown]').forEach(dropdown => {
        const btn = dropdown.querySelector('button');

        btn?.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = dropdown.classList.toggle('is-open');
            btn.setAttribute('aria-expanded', isOpen);

            // Stäng andra dropdowns
            document.querySelectorAll('[data-dropdown].is-open').forEach(d => {
                if (d !== dropdown) d.classList.remove('is-open');
            });
        });
    });

    // Stäng vid klick utanför
    document.addEventListener('click', () => {
        document.querySelectorAll('[data-dropdown].is-open').forEach(d => {
            d.classList.remove('is-open');
        });
    });

    // Stäng vid ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('[data-dropdown].is-open').forEach(d => {
                d.classList.remove('is-open');
            });
        }
    });
});
