# Accessibility (a11y)

## Patterns


---
  #### **Name**
Semantic HTML First
  #### **Description**
Use native HTML elements before reaching for ARIA
  #### **When**
Building any interactive component
  #### **Example**
    # SEMANTIC HTML:
    
    """
    Native HTML elements have built-in accessibility.
    Don't rebuild what the browser gives you for free.
    """
    
    <!-- WRONG: Custom button with ARIA -->
    <div role="button" tabindex="0" onclick="submit()">
      Submit
    </div>
    
    <!-- RIGHT: Native button -->
    <button type="submit">Submit</button>
    
    <!-- WRONG: Custom checkbox -->
    <div role="checkbox" aria-checked="false" tabindex="0">
      Accept terms
    </div>
    
    <!-- RIGHT: Native checkbox -->
    <label>
      <input type="checkbox" name="terms" />
      Accept terms
    </label>
    
    <!-- Native elements provide: -->
    - Keyboard handling (Enter, Space)
    - Focus management
    - Form submission
    - Screen reader announcements
    - All for free!
    

---
  #### **Name**
Accessible Modal/Dialog
  #### **Description**
Focus-trapped modal with proper ARIA and keyboard handling
  #### **When**
Building modal dialogs, popups, or overlays
  #### **Example**
    # ACCESSIBLE MODAL:
    
    """
    Modals must:
    1. Trap focus inside when open
    2. Return focus when closed
    3. Close on Escape
    4. Announce properly to screen readers
    """
    
    <!-- HTML structure -->
    <button id="open-modal">Open Settings</button>
    
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-desc"
      id="settings-modal"
      hidden
    >
      <h2 id="modal-title">Settings</h2>
      <p id="modal-desc">Adjust your preferences below.</p>
    
      <!-- Modal content -->
    
      <button id="close-modal">Close</button>
    </div>
    
    // JavaScript
    const modal = document.getElementById('settings-modal');
    const openBtn = document.getElementById('open-modal');
    const closeBtn = document.getElementById('close-modal');
    let previouslyFocused;
    
    function openModal() {
      previouslyFocused = document.activeElement;
      modal.hidden = false;
      closeBtn.focus();  // Move focus into modal
      document.addEventListener('keydown', trapFocus);
    }
    
    function closeModal() {
      modal.hidden = true;
      previouslyFocused?.focus();  // Return focus
      document.removeEventListener('keydown', trapFocus);
    }
    
    function trapFocus(e) {
      if (e.key === 'Escape') {
        closeModal();
        return;
      }
    
      if (e.key !== 'Tab') return;
    
      const focusable = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
    
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
    

---
  #### **Name**
Skip Navigation Link
  #### **Description**
Allow keyboard users to skip repetitive navigation
  #### **When**
Pages with navigation before main content
  #### **Example**
    # SKIP LINK:
    
    """
    Keyboard users shouldn't have to tab through 50 nav items
    on every page. Provide a skip link as the first focusable element.
    """
    
    <!-- HTML - first element in body -->
    <a href="#main-content" class="skip-link">
      Skip to main content
    </a>
    
    <nav>
      <!-- Navigation items -->
    </nav>
    
    <main id="main-content" tabindex="-1">
      <!-- Page content -->
    </main>
    
    /* CSS - visible only on focus */
    .skip-link {
      position: absolute;
      top: -40px;
      left: 0;
      padding: 8px 16px;
      background: #000;
      color: #fff;
      z-index: 100;
      transition: top 0.2s;
    }
    
    .skip-link:focus {
      top: 0;
    }
    
    // Note: tabindex="-1" on main allows programmatic focus
    // but doesn't add to tab order
    

---
  #### **Name**
Accessible Forms
  #### **Description**
Form fields with proper labels and error handling
  #### **When**
Building any form
  #### **Example**
    # ACCESSIBLE FORMS:
    
    """
    Every input needs:
    1. Visible label
    2. Associated programmatically
    3. Error messages linked to field
    4. Required state communicated
    """
    
    <!-- Proper label association -->
    <label for="email">Email address</label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-hint email-error"
    />
    <p id="email-hint" class="hint">We'll never share your email.</p>
    <p id="email-error" class="error" hidden>
      Please enter a valid email address.
    </p>
    
    <!-- Multiple labels with fieldset/legend -->
    <fieldset>
      <legend>Shipping address</legend>
    
      <label for="street">Street</label>
      <input type="text" id="street" name="street" />
    
      <label for="city">City</label>
      <input type="text" id="city" name="city" />
    </fieldset>
    
    <!-- Error handling -->
    function showError(input, message) {
      const errorEl = document.getElementById(`${input.id}-error`);
      errorEl.textContent = message;
      errorEl.hidden = false;
      input.setAttribute('aria-invalid', 'true');
      input.focus();
    }
    
    function clearError(input) {
      const errorEl = document.getElementById(`${input.id}-error`);
      errorEl.hidden = true;
      input.removeAttribute('aria-invalid');
    }
    

---
  #### **Name**
Live Regions for Dynamic Content
  #### **Description**
Announce dynamic changes to screen reader users
  #### **When**
Content updates without page reload (notifications, loading states)
  #### **Example**
    # ARIA LIVE REGIONS:
    
    """
    Screen readers don't automatically announce DOM changes.
    Use aria-live to announce updates.
    """
    
    <!-- Polite announcement (waits for pause) -->
    <div aria-live="polite" aria-atomic="true" id="status">
      <!-- Dynamic content injected here -->
    </div>
    
    <!-- Assertive announcement (interrupts) -->
    <div aria-live="assertive" role="alert" id="error-message">
      <!-- Error messages -->
    </div>
    
    <!-- Status roles (implicit aria-live) -->
    <div role="status">Loading...</div>  <!-- polite -->
    <div role="alert">Error occurred!</div>  <!-- assertive -->
    
    // JavaScript - update live region
    function showNotification(message) {
      const status = document.getElementById('status');
      status.textContent = message;
    
      // Clear after delay to allow re-announcement of same text
      setTimeout(() => {
        status.textContent = '';
      }, 1000);
    }
    
    // For loading states
    <button aria-busy="true" aria-describedby="loading-text">
      Save
    </button>
    <span id="loading-text" class="sr-only">Saving, please wait</span>
    

---
  #### **Name**
Color Contrast and Visual Design
  #### **Description**
Ensure content is perceivable regardless of visual ability
  #### **When**
Designing and styling any interface
  #### **Example**
    # COLOR AND CONTRAST:
    
    """
    WCAG 2.2 Requirements:
    - Normal text: 4.5:1 contrast ratio (AA)
    - Large text (18pt+): 3:1 contrast ratio (AA)
    - UI components/graphics: 3:1 contrast ratio
    """
    
    /* WRONG: Low contrast */
    .text-gray {
      color: #aaa;  /* ~2.3:1 on white - fails! */
    }
    
    /* RIGHT: Sufficient contrast */
    .text-gray {
      color: #767676;  /* 4.5:1 on white - passes AA */
    }
    
    /* Don't rely on color alone */
    
    /* WRONG: Color is only indicator */
    .error { color: red; }
    .success { color: green; }
    
    /* RIGHT: Color + icon/text */
    .error {
      color: #c53030;
      &::before {
        content: "⚠ Error: ";
      }
    }
    
    .success {
      color: #276749;
      &::before {
        content: "✓ Success: ";
      }
    }
    
    /* Focus indicators */
    /* WRONG: Removing focus outline */
    :focus { outline: none; }
    
    /* RIGHT: Custom visible focus */
    :focus {
      outline: 2px solid #2563eb;
      outline-offset: 2px;
    }
    
    :focus:not(:focus-visible) {
      outline: none;  /* Hide for mouse, show for keyboard */
    }
    
    :focus-visible {
      outline: 2px solid #2563eb;
      outline-offset: 2px;
    }
    

## Anti-Patterns


---
  #### **Name**
Div Button
  #### **Description**
Using div or span as clickable elements instead of button
  #### **Why**
    Divs aren't focusable, don't respond to Enter/Space, aren't announced
    as buttons, and aren't included in form submission. You have to
    manually add all of this with JavaScript and ARIA.
    
  #### **Instead**
    <button type="button" onclick="doAction()">Click me</button>
    
    If you need a link that looks like a button:
    <a href="/page" class="button">Go to page</a>
    

---
  #### **Name**
Mouse-Only Interactions
  #### **Description**
Features that only work with hover or click
  #### **Why**
    Keyboard users can't hover. Touch users have no hover state.
    One-arm users might use keyboard only. Screen reader users
    navigate via keyboard.
    
  #### **Instead**
    Make all interactions work with:
    - Mouse (click, hover)
    - Keyboard (Enter, Space, Tab)
    - Touch (tap)
    
    Tooltips should be focusable:
    <button aria-describedby="tooltip">
      Info
    </button>
    <div role="tooltip" id="tooltip">
      Additional information
    </div>
    

---
  #### **Name**
Removing Focus Outline
  #### **Description**
Using outline:none without replacement
  #### **Why**
    Focus indicators tell keyboard users where they are. Without them,
    keyboard navigation is impossible. It's like making cursor invisible
    for mouse users.
    
  #### **Instead**
    /* Provide custom focus styles */
    :focus-visible {
      outline: 2px solid #2563eb;
      outline-offset: 2px;
      border-radius: 2px;
    }
    

---
  #### **Name**
Auto-Playing Media
  #### **Description**
Audio or video that plays automatically
  #### **Why**
    Unexpected sound is jarring. Screen reader users can't hear their
    screen reader over your video. Users with PTSD or anxiety can be
    triggered. It's also just annoying.
    
  #### **Instead**
    <video controls>...</video>
    
    If autoplay is required (muted background):
    <video autoplay muted playsinline>
      <track kind="captions" src="..." />
    </video>
    <button onclick="toggleAudio()">Enable sound</button>
    

---
  #### **Name**
ARIA First
  #### **Description**
Adding ARIA to fix non-semantic HTML
  #### **Why**
    ARIA is a repair tool for when native HTML isn't enough. Semantic
    HTML works out of the box. ARIA requires correct usage, testing,
    and maintenance. Wrong ARIA is worse than no ARIA.
    
  #### **Instead**
    <!-- WRONG: ARIA bandaid -->
    <div role="navigation" aria-label="Main">
      <div role="list">
        <div role="listitem"><a href="/">Home</a></div>
      </div>
    </div>
    
    <!-- RIGHT: Semantic HTML -->
    <nav aria-label="Main">
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
    </nav>
    