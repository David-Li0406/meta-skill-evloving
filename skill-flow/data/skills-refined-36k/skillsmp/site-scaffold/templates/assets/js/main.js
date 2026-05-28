/**
 * {{SITE_NAME}} - Main JavaScript
 * Progressive enhancement - site works without JS
 */

document.addEventListener('DOMContentLoaded', init);

/**
 * Initialize site functionality
 */
function init() {
  initNavigation();
  initForms();
  initAccessibility();
}

/**
 * Navigation enhancements
 * - Mobile menu toggle
 * - Dropdown menus
 * - Current page highlighting
 */
function initNavigation() {
  // Mobile menu toggle (add button in HTML if needed)
  const menuButton = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('header nav');

  if (menuButton && nav) {
    menuButton.addEventListener('click', () => {
      const expanded = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!expanded));
      nav.hidden = expanded;
    });
  }
}

/**
 * Form enhancements
 * - Client-side validation feedback
 * - Submission handling
 */
function initForms() {
  const forms = document.querySelectorAll('form');

  forms.forEach((form) => {
    form.addEventListener('submit', handleFormSubmit);
  });
}

/**
 * Handle form submission
 * @param {SubmitEvent} event
 */
function handleFormSubmit(event) {
  const form = event.target;

  // Let native validation handle required fields
  if (!form.checkValidity()) {
    return;
  }

  // Add custom handling here if needed
  // e.g., AJAX submission, loading states
}

/**
 * Accessibility enhancements
 * - Focus management
 * - Keyboard navigation
 */
function initAccessibility() {
  // Add focus-visible polyfill behavior if needed
  document.body.addEventListener('keydown', (event) => {
    if (event.key === 'Tab') {
      document.body.dataset.userTabbing = 'true';
    }
  });

  document.body.addEventListener('mousedown', () => {
    delete document.body.dataset.userTabbing;
  });
}
