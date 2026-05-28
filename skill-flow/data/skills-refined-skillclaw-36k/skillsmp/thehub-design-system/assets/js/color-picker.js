/**
 * TheHUB Advanced Color Picker
 * A beautiful color picker with saturation/brightness gradient and hue slider
 */
const HubColorPicker = (function() {
  'use strict';

  let currentPicker = null;
  let currentCallback = null;
  let currentColor = { h: 0, s: 100, v: 100 };

  // Create the picker modal HTML
  function createPickerHTML() {
    const picker = document.createElement('div');
    picker.className = 'hub-color-picker';
    picker.innerHTML = `
      <div class="hcp-backdrop"></div>
      <div class="hcp-modal">
        <div class="hcp-gradient-area">
          <div class="hcp-gradient-white"></div>
          <div class="hcp-gradient-black"></div>
          <div class="hcp-gradient-cursor"></div>
        </div>
        <div class="hcp-hue-slider">
          <div class="hcp-hue-cursor"></div>
        </div>
        <div class="hcp-preview-row">
          <div class="hcp-preview-swatch"></div>
          <input type="text" class="hcp-hex-input" maxlength="7" placeholder="#FFFFFF">
        </div>
        <div class="hcp-actions">
          <button type="button" class="btn btn--ghost btn--sm hcp-cancel">Avbryt</button>
          <button type="button" class="btn btn--primary btn--sm hcp-confirm">Välj färg</button>
        </div>
      </div>
    `;
    return picker;
  }

  // Convert HSV to RGB
  function hsvToRgb(h, s, v) {
    s /= 100;
    v /= 100;
    const c = v * s;
    const x = c * (1 - Math.abs((h / 60) % 2 - 1));
    const m = v - c;
    let r, g, b;

    if (h < 60) { r = c; g = x; b = 0; }
    else if (h < 120) { r = x; g = c; b = 0; }
    else if (h < 180) { r = 0; g = c; b = x; }
    else if (h < 240) { r = 0; g = x; b = c; }
    else if (h < 300) { r = x; g = 0; b = c; }
    else { r = c; g = 0; b = x; }

    return {
      r: Math.round((r + m) * 255),
      g: Math.round((g + m) * 255),
      b: Math.round((b + m) * 255)
    };
  }

  // Convert RGB to HSV
  function rgbToHsv(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const d = max - min;
    let h = 0;
    const s = max === 0 ? 0 : (d / max) * 100;
    const v = max * 100;

    if (d !== 0) {
      switch (max) {
        case r: h = ((g - b) / d + (g < b ? 6 : 0)) * 60; break;
        case g: h = ((b - r) / d + 2) * 60; break;
        case b: h = ((r - g) / d + 4) * 60; break;
      }
    }

    return { h, s, v };
  }

  // Convert RGB to Hex
  function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('').toUpperCase();
  }

  // Convert Hex to RGB
  function hexToRgb(hex) {
    hex = hex.replace('#', '');
    if (hex.length === 3) {
      hex = hex.split('').map(c => c + c).join('');
    }
    const num = parseInt(hex, 16);
    return {
      r: (num >> 16) & 255,
      g: (num >> 8) & 255,
      b: num & 255
    };
  }

  // Update the picker UI
  function updatePickerUI() {
    if (!currentPicker) return;

    const gradientArea = currentPicker.querySelector('.hcp-gradient-area');
    const gradientCursor = currentPicker.querySelector('.hcp-gradient-cursor');
    const hueCursor = currentPicker.querySelector('.hcp-hue-cursor');
    const preview = currentPicker.querySelector('.hcp-preview-swatch');
    const hexInput = currentPicker.querySelector('.hcp-hex-input');

    // Update gradient background color (pure hue)
    const pureColor = hsvToRgb(currentColor.h, 100, 100);
    const pureHex = rgbToHex(pureColor.r, pureColor.g, pureColor.b);
    gradientArea.style.backgroundColor = pureHex;

    // Update gradient cursor position
    gradientCursor.style.left = (currentColor.s) + '%';
    gradientCursor.style.top = (100 - currentColor.v) + '%';

    // Update hue cursor position and color
    hueCursor.style.left = (currentColor.h / 360 * 100) + '%';
    hueCursor.style.backgroundColor = pureHex;

    // Update preview and hex
    const rgb = hsvToRgb(currentColor.h, currentColor.s, currentColor.v);
    const hex = rgbToHex(rgb.r, rgb.g, rgb.b);
    preview.style.backgroundColor = hex;
    hexInput.value = hex;
  }

  // Handle gradient area interaction
  function handleGradientInteraction(e, gradientArea) {
    const rect = gradientArea.getBoundingClientRect();
    let x = (e.clientX - rect.left) / rect.width;
    let y = (e.clientY - rect.top) / rect.height;

    x = Math.max(0, Math.min(1, x));
    y = Math.max(0, Math.min(1, y));

    currentColor.s = x * 100;
    currentColor.v = (1 - y) * 100;
    updatePickerUI();
  }

  // Handle hue slider interaction
  function handleHueInteraction(e, hueSlider) {
    const rect = hueSlider.getBoundingClientRect();
    let x = (e.clientX - rect.left) / rect.width;
    x = Math.max(0, Math.min(1, x));
    currentColor.h = x * 360;
    updatePickerUI();
  }

  // Open the picker
  function open(initialColor, callback, anchorElement) {
    close(); // Close any existing picker

    currentCallback = callback;

    // Parse initial color
    if (initialColor && initialColor.startsWith('#')) {
      const rgb = hexToRgb(initialColor);
      currentColor = rgbToHsv(rgb.r, rgb.g, rgb.b);
    } else {
      currentColor = { h: 0, s: 100, v: 100 };
    }

    currentPicker = createPickerHTML();
    document.body.appendChild(currentPicker);

    // Modal stays centered (no position override needed)

    // Set up event listeners
    const gradientArea = currentPicker.querySelector('.hcp-gradient-area');
    const hueSlider = currentPicker.querySelector('.hcp-hue-slider');
    const hexInput = currentPicker.querySelector('.hcp-hex-input');
    const backdrop = currentPicker.querySelector('.hcp-backdrop');
    const cancelBtn = currentPicker.querySelector('.hcp-cancel');
    const confirmBtn = currentPicker.querySelector('.hcp-confirm');

    // Gradient area drag
    let isDraggingGradient = false;
    gradientArea.addEventListener('mousedown', (e) => {
      isDraggingGradient = true;
      handleGradientInteraction(e, gradientArea);
    });

    // Hue slider drag
    let isDraggingHue = false;
    hueSlider.addEventListener('mousedown', (e) => {
      isDraggingHue = true;
      handleHueInteraction(e, hueSlider);
    });

    // Global mouse move/up
    const onMouseMove = (e) => {
      if (isDraggingGradient) handleGradientInteraction(e, gradientArea);
      if (isDraggingHue) handleHueInteraction(e, hueSlider);
    };
    const onMouseUp = () => {
      isDraggingGradient = false;
      isDraggingHue = false;
    };
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);

    // Touch support
    gradientArea.addEventListener('touchstart', (e) => {
      e.preventDefault();
      isDraggingGradient = true;
      handleGradientInteraction(e.touches[0], gradientArea);
    });
    gradientArea.addEventListener('touchmove', (e) => {
      e.preventDefault();
      if (isDraggingGradient) handleGradientInteraction(e.touches[0], gradientArea);
    });
    gradientArea.addEventListener('touchend', () => isDraggingGradient = false);

    hueSlider.addEventListener('touchstart', (e) => {
      e.preventDefault();
      isDraggingHue = true;
      handleHueInteraction(e.touches[0], hueSlider);
    });
    hueSlider.addEventListener('touchmove', (e) => {
      e.preventDefault();
      if (isDraggingHue) handleHueInteraction(e.touches[0], hueSlider);
    });
    hueSlider.addEventListener('touchend', () => isDraggingHue = false);

    // Hex input
    hexInput.addEventListener('input', (e) => {
      let val = e.target.value;
      if (!val.startsWith('#')) val = '#' + val;
      if (/^#[0-9A-Fa-f]{6}$/.test(val)) {
        const rgb = hexToRgb(val);
        currentColor = rgbToHsv(rgb.r, rgb.g, rgb.b);
        updatePickerUI();
      }
    });

    // Buttons
    backdrop.addEventListener('click', close);
    cancelBtn.addEventListener('click', close);
    confirmBtn.addEventListener('click', () => {
      const rgb = hsvToRgb(currentColor.h, currentColor.s, currentColor.v);
      const hex = rgbToHex(rgb.r, rgb.g, rgb.b);
      if (currentCallback) currentCallback(hex);
      close();
    });

    // Store cleanup function
    currentPicker._cleanup = () => {
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };

    // Initial update
    updatePickerUI();

    // Animate in
    requestAnimationFrame(() => {
      currentPicker.classList.add('is-open');
    });
  }

  // Close the picker
  function close() {
    if (currentPicker) {
      if (currentPicker._cleanup) currentPicker._cleanup();
      currentPicker.classList.remove('is-open');
      setTimeout(() => {
        if (currentPicker && currentPicker.parentNode) {
          currentPicker.parentNode.removeChild(currentPicker);
        }
        currentPicker = null;
        currentCallback = null;
      }, 150);
    }
  }

  // Public API
  return {
    open,
    close
  };
})();

// Make available globally
window.HubColorPicker = HubColorPicker;
