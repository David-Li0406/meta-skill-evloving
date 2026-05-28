---
name: yukyu-component-doctor
description: "Doctor de Componentes para YuKyuDATA - Diagnóstico y reparación de componentes rotos, detección de bugs visuales, memory leaks, problemas de accesibilidad, inconsistencias CSS, y refactoring de código legacy. Incluye herramientas de auditoría automatizada."
---

# YuKyu Component Doctor

Sistema experto para diagnosticar, reparar y mejorar componentes del frontend. Especializado en detectar y corregir problemas comunes en aplicaciones web empresariales.

## Cuándo Usar Este Skill

- Componentes que no se renderizan correctamente
- Estilos rotos o inconsistentes
- Memory leaks en JavaScript
- Problemas de accesibilidad
- Bugs visuales en dark/light mode
- Refactoring de código legacy
- Auditorías de calidad de código

---

## Diagnóstico Rápido

### Script de Auditoría Automática

Ejecuta este script en la consola del navegador para detectar problemas comunes:

```javascript
(function auditComponents() {
    const issues = [];

    // 1. Detectar emojis usados como iconos
    document.querySelectorAll('button, a, span').forEach(el => {
        if (/[\u{1F300}-\u{1F9FF}]/u.test(el.textContent)) {
            issues.push({
                type: 'emoji-icon',
                severity: 'medium',
                element: el,
                message: 'Emoji usado como icono - usar SVG en su lugar'
            });
        }
    });

    // 2. Detectar elementos clickeables sin cursor-pointer
    document.querySelectorAll('button, a, [onclick], [data-action]').forEach(el => {
        const cursor = getComputedStyle(el).cursor;
        if (cursor !== 'pointer') {
            issues.push({
                type: 'missing-cursor',
                severity: 'low',
                element: el,
                message: 'Elemento clickeable sin cursor-pointer'
            });
        }
    });

    // 3. Detectar imágenes sin alt
    document.querySelectorAll('img:not([alt])').forEach(el => {
        issues.push({
            type: 'missing-alt',
            severity: 'high',
            element: el,
            message: 'Imagen sin atributo alt'
        });
    });

    // 4. Detectar inputs sin label
    document.querySelectorAll('input, select, textarea').forEach(el => {
        const id = el.id;
        const label = id ? document.querySelector(`label[for="${id}"]`) : null;
        const ariaLabel = el.getAttribute('aria-label');

        if (!label && !ariaLabel) {
            issues.push({
                type: 'missing-label',
                severity: 'high',
                element: el,
                message: 'Input sin label asociado'
            });
        }
    });

    // 5. Detectar problemas de contraste (aproximado)
    document.querySelectorAll('*').forEach(el => {
        const style = getComputedStyle(el);
        const color = style.color;
        const bg = style.backgroundColor;
        // Simplificado - en producción usar librería de contraste
    });

    // 6. Detectar z-index wars
    const zIndexes = [];
    document.querySelectorAll('*').forEach(el => {
        const z = getComputedStyle(el).zIndex;
        if (z !== 'auto' && parseInt(z) > 100) {
            zIndexes.push({ element: el, zIndex: parseInt(z) });
        }
    });
    if (zIndexes.length > 5) {
        issues.push({
            type: 'z-index-war',
            severity: 'medium',
            elements: zIndexes,
            message: `${zIndexes.length} elementos con z-index > 100`
        });
    }

    // Reporte
    console.group('🏥 Component Doctor - Audit Report');
    console.log(`Total issues: ${issues.length}`);

    const grouped = issues.reduce((acc, issue) => {
        acc[issue.severity] = acc[issue.severity] || [];
        acc[issue.severity].push(issue);
        return acc;
    }, {});

    if (grouped.high?.length) {
        console.group('🔴 High Severity');
        grouped.high.forEach(i => console.log(i.message, i.element));
        console.groupEnd();
    }
    if (grouped.medium?.length) {
        console.group('🟡 Medium Severity');
        grouped.medium.forEach(i => console.log(i.message, i.element));
        console.groupEnd();
    }
    if (grouped.low?.length) {
        console.group('🟢 Low Severity');
        grouped.low.forEach(i => console.log(i.message, i.element));
        console.groupEnd();
    }

    console.groupEnd();
    return issues;
})();
```

---

## Problemas Comunes y Soluciones

### 1. Modal No Se Muestra

**Síntomas:**
- Modal existe en DOM pero no es visible
- Click en botón no hace nada

**Diagnóstico:**
```javascript
const modal = document.getElementById('my-modal');
console.log('Display:', getComputedStyle(modal).display);
console.log('Visibility:', getComputedStyle(modal).visibility);
console.log('Opacity:', getComputedStyle(modal).opacity);
console.log('Z-Index:', getComputedStyle(modal).zIndex);
```

**Soluciones:**

```css
/* Problema: display: none que no cambia */
.modal {
    display: flex;  /* Siempre flex */
    visibility: hidden;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s, visibility 0.3s;
}

.modal.active {
    visibility: visible;
    opacity: 1;
    pointer-events: auto;
}
```

```javascript
// Problema: clase no se agrega
function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) {
        console.error(`Modal ${id} not found`);
        return;
    }
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scroll
}
```

---

### 2. Dropdown No Funciona

**Síntomas:**
- Menú no aparece al hacer click
- Menú aparece pero no se cierra

**Diagnóstico:**
```javascript
const dropdown = document.querySelector('.dropdown');
const menu = dropdown.querySelector('.dropdown-menu');
console.log('Menu visibility:', getComputedStyle(menu).visibility);
console.log('Event listeners:', getEventListeners(dropdown)); // Solo en Chrome DevTools
```

**Solución Completa:**

```html
<div class="dropdown" data-dropdown>
    <button class="dropdown-trigger" aria-haspopup="true" aria-expanded="false">
        Opciones
        <svg class="dropdown-arrow">...</svg>
    </button>
    <div class="dropdown-menu" role="menu">
        <a href="#" class="dropdown-item" role="menuitem">Item 1</a>
        <a href="#" class="dropdown-item" role="menuitem">Item 2</a>
    </div>
</div>
```

```css
.dropdown {
    position: relative;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    min-width: 200px;
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.2s ease;
    z-index: 100;
}

.dropdown.open .dropdown-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

```javascript
// Event delegation para todos los dropdowns
document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.dropdown-trigger');

    // Cerrar todos los dropdowns abiertos
    document.querySelectorAll('.dropdown.open').forEach(d => {
        if (!d.contains(e.target)) {
            d.classList.remove('open');
            d.querySelector('.dropdown-trigger')
                ?.setAttribute('aria-expanded', 'false');
        }
    });

    // Toggle el dropdown clickeado
    if (trigger) {
        const dropdown = trigger.closest('.dropdown');
        const isOpen = dropdown.classList.toggle('open');
        trigger.setAttribute('aria-expanded', isOpen);
    }
});

// Cerrar con ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.dropdown.open').forEach(d => {
            d.classList.remove('open');
        });
    }
});
```

---

### 3. Tabla No Se Actualiza

**Síntomas:**
- Datos cambian pero tabla sigue igual
- Filas duplicadas o faltantes

**Diagnóstico:**
```javascript
console.log('Table rows:', document.querySelectorAll('tbody tr').length);
console.log('Data length:', App.state.employees.length);
```

**Solución:**

```javascript
function renderTable(data) {
    const tbody = document.querySelector('#employees-table tbody');

    // IMPORTANTE: Limpiar antes de renderizar
    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state">
                    <div class="empty-icon">📋</div>
                    <p>データがありません</p>
                </td>
            </tr>
        `;
        return;
    }

    // Usar DocumentFragment para mejor performance
    const fragment = document.createDocumentFragment();

    data.forEach(emp => {
        const tr = document.createElement('tr');
        tr.dataset.id = emp.id;
        tr.innerHTML = `
            <td>${escapeHtml(emp.name)}</td>
            <td>${emp.remaining_days}</td>
            <td>${emp.used_days}</td>
            <td>
                <button class="btn-icon" data-action="edit" data-id="${emp.id}">
                    編集
                </button>
            </td>
        `;
        fragment.appendChild(tr);
    });

    tbody.appendChild(fragment);
}
```

---

### 4. Memory Leak en Componentes

**Síntomas:**
- App se vuelve lenta con el tiempo
- Uso de memoria crece constantemente

**Diagnóstico:**
```javascript
// En Chrome DevTools > Memory > Take heap snapshot
// Buscar detached DOM nodes

// O usar Performance Monitor
// DevTools > More tools > Performance monitor
```

**Causas Comunes y Soluciones:**

```javascript
// ❌ PROBLEMA: Event listeners no removidos
class Modal {
    constructor() {
        this.handleEsc = (e) => {
            if (e.key === 'Escape') this.close();
        };
        document.addEventListener('keydown', this.handleEsc);
    }

    close() {
        this.element.remove();
        // ❌ Event listener sigue activo!
    }
}

// ✅ SOLUCIÓN: Remover listeners en cleanup
class Modal {
    constructor() {
        this.handleEsc = (e) => {
            if (e.key === 'Escape') this.close();
        };
        document.addEventListener('keydown', this.handleEsc);
    }

    close() {
        document.removeEventListener('keydown', this.handleEsc);
        this.element.remove();
    }
}

// ❌ PROBLEMA: setInterval sin limpiar
function startPolling() {
    setInterval(() => {
        fetchData();
    }, 5000);
}

// ✅ SOLUCIÓN: Guardar referencia y limpiar
let pollInterval = null;

function startPolling() {
    pollInterval = setInterval(() => {
        fetchData();
    }, 5000);
}

function stopPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
}

// ❌ PROBLEMA: Closures que retienen referencias
function createHandlers(elements) {
    elements.forEach(el => {
        el.addEventListener('click', () => {
            // Esta closure retiene 'elements' completo
            console.log(elements.length);
        });
    });
}

// ✅ SOLUCIÓN: Evitar retener referencias innecesarias
function createHandlers(elements) {
    const count = elements.length;
    elements.forEach(el => {
        el.addEventListener('click', () => {
            console.log(count);  // Solo retiene el número
        });
    });
}
```

---

### 5. Estilos Dark/Light Mode Inconsistentes

**Síntomas:**
- Elementos blancos en dark mode
- Texto ilegible al cambiar tema
- Bordes invisibles

**Diagnóstico:**
```javascript
// Verificar qué tema está activo
console.log('Theme:', document.documentElement.getAttribute('data-theme'));

// Verificar CSS variables
const styles = getComputedStyle(document.documentElement);
console.log('--glass-bg:', styles.getPropertyValue('--glass-bg'));
console.log('--text-primary:', styles.getPropertyValue('--text-primary'));
```

**Solución - Checklist de Variables:**

```css
/* Asegurar que TODAS las variables tengan override en light mode */
[data-theme="light"] {
    /* Backgrounds */
    --glass-bg: rgba(255, 255, 255, 0.85);
    --bg-base: #f8fafc;
    --bg-card: #ffffff;

    /* Text */
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --text-muted: #94a3b8;

    /* Borders */
    --border-color: rgba(0, 0, 0, 0.1);
    --glass-border: rgba(0, 0, 0, 0.08);

    /* Shadows */
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
}

/* Verificar elementos específicos */
[data-theme="light"] .glass-panel {
    background: var(--glass-bg);
    color: var(--text-primary);
    border-color: var(--border-color);
}

[data-theme="light"] .input-glass {
    background: rgba(255, 255, 255, 0.9);
    color: var(--text-primary);
    border: 1px solid rgba(0, 0, 0, 0.15);
}
```

---

### 6. Componente No Responde a Eventos

**Síntomas:**
- Click no hace nada
- Hover no funciona
- Eventos keyboard ignorados

**Diagnóstico:**
```javascript
// Verificar si hay elementos superpuestos
const el = document.querySelector('.my-button');
const rect = el.getBoundingClientRect();
const topEl = document.elementFromPoint(
    rect.left + rect.width/2,
    rect.top + rect.height/2
);
console.log('Top element:', topEl);
console.log('Is same?', topEl === el);

// Verificar pointer-events
console.log('pointer-events:', getComputedStyle(el).pointerEvents);
```

**Soluciones:**

```css
/* Problema: Elemento invisible sobre el botón */
.overlay {
    pointer-events: none;  /* Permite click-through */
}

/* Problema: Parent con overflow */
.container {
    overflow: visible;  /* O ajustar z-index del hijo */
}

/* Problema: Elemento disabled */
.btn:disabled {
    pointer-events: none;
    opacity: 0.5;
}
```

```javascript
// Verificar que el evento se está registrando
const btn = document.querySelector('.my-button');

btn.addEventListener('click', (e) => {
    console.log('Click event fired!', e);
});

// Si usa event delegation, verificar el selector
document.addEventListener('click', (e) => {
    console.log('Click target:', e.target);
    console.log('Closest button:', e.target.closest('.my-button'));
});
```

---

## Refactoring Patterns

### 1. De onclick Inline a Event Delegation

```html
<!-- ❌ ANTES -->
<button onclick="handleClick('123')">Click</button>

<!-- ✅ DESPUÉS -->
<button data-action="click" data-id="123">Click</button>
```

```javascript
// ❌ ANTES
function handleClick(id) { ... }

// ✅ DESPUÉS
document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action="click"]');
    if (btn) {
        const id = btn.dataset.id;
        handleClick(id);
    }
});
```

### 2. De innerHTML Inseguro a Template Seguro

```javascript
// ❌ ANTES - Vulnerable a XSS
element.innerHTML = `<div>${userData.name}</div>`;

// ✅ DESPUÉS - Seguro
function createUserElement(userData) {
    const div = document.createElement('div');
    div.textContent = userData.name;  // Auto-escaped
    return div;
}

// O con template seguro
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

element.innerHTML = `<div>${escapeHtml(userData.name)}</div>`;
```

### 3. De Callbacks a Async/Await

```javascript
// ❌ ANTES - Callback hell
function loadData(callback) {
    fetch('/api/data')
        .then(res => res.json())
        .then(data => {
            fetch(`/api/detail/${data.id}`)
                .then(res => res.json())
                .then(detail => {
                    callback(detail);
                });
        });
}

// ✅ DESPUÉS - Async/await limpio
async function loadData() {
    try {
        const dataRes = await fetch('/api/data');
        const data = await dataRes.json();

        const detailRes = await fetch(`/api/detail/${data.id}`);
        const detail = await detailRes.json();

        return detail;
    } catch (error) {
        console.error('Error loading data:', error);
        throw error;
    }
}
```

---

## Herramientas de Debugging

### 1. CSS Debug Mode

```css
/* Agregar temporalmente para ver layout */
* {
    outline: 1px solid rgba(255, 0, 0, 0.2) !important;
}

/* Ver solo ciertos elementos */
.debug * {
    outline: 1px solid red !important;
    background: rgba(255, 0, 0, 0.1) !important;
}
```

### 2. JavaScript Debug Helpers

```javascript
// Logging mejorado
const debug = {
    log: (...args) => console.log('[DEBUG]', ...args),
    table: (data) => console.table(data),
    time: (label) => console.time(label),
    timeEnd: (label) => console.timeEnd(label),
    trace: () => console.trace(),

    // DOM inspector
    inspect: (selector) => {
        const el = document.querySelector(selector);
        console.log({
            element: el,
            computed: getComputedStyle(el),
            rect: el.getBoundingClientRect(),
            dataset: { ...el.dataset }
        });
    }
};

// Performance measurement
function measurePerformance(fn, label = 'Operation') {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${label}: ${(end - start).toFixed(2)}ms`);
    return result;
}
```

### 3. Network Debug

```javascript
// Interceptar fetch para debugging
const originalFetch = window.fetch;
window.fetch = async (...args) => {
    console.log('[FETCH]', args[0], args[1]);
    const start = performance.now();

    try {
        const response = await originalFetch(...args);
        console.log('[FETCH DONE]', args[0], `${(performance.now() - start).toFixed(0)}ms`);
        return response;
    } catch (error) {
        console.error('[FETCH ERROR]', args[0], error);
        throw error;
    }
};
```

---

## Checklist de Reparación

### Antes de Empezar
- [ ] Reproducir el bug consistentemente
- [ ] Identificar el componente afectado
- [ ] Revisar console errors
- [ ] Revisar network errors

### Durante la Reparación
- [ ] Hacer backup del código original
- [ ] Cambios pequeños e incrementales
- [ ] Probar después de cada cambio
- [ ] Documentar la solución

### Después de Reparar
- [ ] Probar en dark y light mode
- [ ] Probar en diferentes viewports
- [ ] Verificar accesibilidad
- [ ] Verificar que no hay memory leaks
- [ ] Probar edge cases

---

## Recursos

### DevTools
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Firefox Developer Tools](https://firefox-source-docs.mozilla.org/devtools-user/)

### Validadores
- [W3C Markup Validator](https://validator.w3.org/)
- [WAVE Accessibility](https://wave.webaim.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

### Performance
- [WebPageTest](https://www.webpagetest.org/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
