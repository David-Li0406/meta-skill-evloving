---
name: yukyu-frontend-design-pro
description: "Diseñador Frontend Pro para YuKyuDATA - Crea interfaces distintivas y production-ready. Especializado en vanilla JS ES6+, CSS moderno, Chart.js, ApexCharts, y arquitectura frontend modular. Evita diseños genéricos, crea experiencias únicas."
---

# YuKyu Frontend Design Pro

Sistema experto para crear interfaces frontend distintivas, profesionales y listas para producción. Especializado en el stack tecnológico de YuKyuDATA.

## Stack Tecnológico

| Capa | Tecnología | Versión |
|------|------------|---------|
| JavaScript | Vanilla ES6+ (Modules) | ES2022 |
| CSS | Custom Properties + Glassmorphism | CSS3 |
| Charts | Chart.js + ApexCharts | 4.x / 3.x |
| Icons | Heroicons (SVG inline) | 2.x |
| Fonts | Google Fonts (Poppins, Open Sans) | - |

---

## Arquitectura Frontend

### Estructura de Archivos

```
static/
├── css/
│   ├── unified-design-system.css   # Sistema de diseño principal
│   ├── yukyu-tokens.css            # Design tokens
│   └── components/                  # CSS por componente
├── js/
│   ├── app.js                      # Aplicación principal (legacy)
│   └── modules/                     # Módulos ES6
│       ├── theme-manager.js
│       ├── api-client.js
│       └── ...
└── src/
    ├── components/                  # Componentes modernos
    │   ├── Modal.js
    │   ├── Alert.js
    │   ├── DataTable.js
    │   └── index.js
    └── store/
        └── state.js                 # Estado global
```

### Patrón Singleton (App)

```javascript
const App = {
    // Configuración
    config: {
        apiBase: '/api',
        defaultYear: new Date().getFullYear()
    },

    // Estado
    state: {
        employees: [],
        currentYear: 2025,
        loading: false
    },

    // Módulos
    ui: { /* ... */ },
    data: { /* ... */ },
    theme: { /* ... */ },
    utils: { /* ... */ },

    // Inicialización
    async init() {
        this.theme.init();
        this.ui.setupListeners();
        await this.data.fetchEmployees();
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
```

---

## Diseño Visual Distintivo

### 1. Background con Gradientes

```css
body {
    background-color: #020617;
    background-image:
        radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.1) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.05) 0px, transparent 50%);
    min-height: 100vh;
}
```

### 2. Glass Cards Premium

```css
.glass-card {
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 1rem;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow:
        0 12px 40px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
```

### 3. Botones con Glow

```css
.btn-glow {
    background: linear-gradient(135deg, #06b6d4, #0891b2);
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
    transition: all 0.3s ease;
}

.btn-glow:hover {
    box-shadow: 0 0 30px rgba(6, 182, 212, 0.5);
    transform: translateY(-1px);
}

.btn-glow::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent,
        rgba(255, 255, 255, 0.1),
        transparent
    );
    transform: rotate(45deg);
    transition: all 0.5s ease;
}

.btn-glow:hover::before {
    left: 100%;
}
```

### 4. Inputs Elegantes

```css
.input-modern {
    width: 100%;
    padding: 0.75rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    color: white;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}

.input-modern:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--color-primary-400);
    box-shadow:
        0 0 0 4px rgba(6, 182, 212, 0.15),
        0 0 20px rgba(6, 182, 212, 0.1);
}

.input-modern::placeholder {
    color: rgba(255, 255, 255, 0.4);
}
```

---

## Componentes JavaScript

### 1. Modal Component

```javascript
export class Modal {
    constructor(options = {}) {
        this.id = options.id || `modal-${Date.now()}`;
        this.title = options.title || '';
        this.content = options.content || '';
        this.size = options.size || 'md'; // sm, md, lg
        this.onClose = options.onClose || null;
        this.element = null;
    }

    render() {
        const modal = document.createElement('div');
        modal.id = this.id;
        modal.className = 'confirm-modal';
        modal.innerHTML = `
            <div class="confirm-modal-content modal-${this.size} glass-panel">
                <div class="modal-header">
                    <h2 class="confirm-modal-title">${this.title}</h2>
                    <button class="modal-close" aria-label="閉じる">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                <div class="modal-body">${this.content}</div>
            </div>
        `;

        this.element = modal;
        this.attachEvents();
        document.body.appendChild(modal);

        // Trigger animation
        requestAnimationFrame(() => modal.classList.add('active'));

        return this;
    }

    attachEvents() {
        // Close on backdrop click
        this.element.addEventListener('click', (e) => {
            if (e.target === this.element) this.close();
        });

        // Close button
        this.element.querySelector('.modal-close')
            .addEventListener('click', () => this.close());

        // ESC key
        this.escHandler = (e) => {
            if (e.key === 'Escape') this.close();
        };
        document.addEventListener('keydown', this.escHandler);
    }

    close() {
        this.element.classList.remove('active');
        setTimeout(() => {
            this.element.remove();
            document.removeEventListener('keydown', this.escHandler);
            if (this.onClose) this.onClose();
        }, 300);
    }

    static confirm(message, onConfirm) {
        return new Modal({
            title: '確認',
            content: `
                <p class="mb-lg">${message}</p>
                <div class="flex gap-md justify-end">
                    <button class="btn-secondary" data-action="cancel">キャンセル</button>
                    <button class="btn-primary" data-action="confirm">確認</button>
                </div>
            `,
            size: 'sm'
        }).render();
    }
}
```

### 2. Alert/Toast Component

```javascript
export class Alert {
    static container = null;

    static init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'alert-container';
            this.container.setAttribute('role', 'alert');
            this.container.setAttribute('aria-live', 'polite');
            document.body.appendChild(this.container);
        }
    }

    static show(type, message, duration = 4000) {
        this.init();

        const icons = {
            success: '<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            error: '<path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            warning: '<path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>',
            info: '<path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>'
        };

        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${icons[type]}
            </svg>
            <span class="alert-message">${message}</span>
            <button class="alert-close" aria-label="閉じる">×</button>
        `;

        this.container.appendChild(alert);

        // Animate in
        requestAnimationFrame(() => alert.classList.add('show'));

        // Auto dismiss
        const timer = setTimeout(() => this.dismiss(alert), duration);

        // Manual dismiss
        alert.querySelector('.alert-close').addEventListener('click', () => {
            clearTimeout(timer);
            this.dismiss(alert);
        });
    }

    static dismiss(alert) {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
    }

    static success(msg) { this.show('success', msg); }
    static error(msg) { this.show('error', msg, 6000); }
    static warning(msg) { this.show('warning', msg); }
    static info(msg) { this.show('info', msg); }
}
```

### 3. DataTable Component

```javascript
export class DataTable {
    constructor(container, options = {}) {
        this.container = typeof container === 'string'
            ? document.querySelector(container)
            : container;
        this.columns = options.columns || [];
        this.data = options.data || [];
        this.sortable = options.sortable ?? true;
        this.searchable = options.searchable ?? true;
        this.pagination = options.pagination ?? true;
        this.pageSize = options.pageSize || 20;
        this.currentPage = 1;
        this.sortColumn = null;
        this.sortDirection = 'asc';
        this.searchTerm = '';
        this.onRowClick = options.onRowClick || null;
    }

    render() {
        this.container.innerHTML = `
            ${this.searchable ? this.renderSearch() : ''}
            <div class="table-wrapper">
                <table class="modern-table">
                    <thead>${this.renderHeader()}</thead>
                    <tbody>${this.renderBody()}</tbody>
                </table>
            </div>
            ${this.pagination ? this.renderPagination() : ''}
        `;

        this.attachEvents();
        return this;
    }

    renderHeader() {
        return `<tr>${this.columns.map(col => `
            <th ${this.sortable ? 'class="sortable"' : ''} data-key="${col.key}">
                ${col.label}
                ${this.sortable ? '<span class="sort-icon"></span>' : ''}
            </th>
        `).join('')}</tr>`;
    }

    renderBody() {
        const filtered = this.getFilteredData();
        const paginated = this.getPaginatedData(filtered);

        if (paginated.length === 0) {
            return `<tr><td colspan="${this.columns.length}" class="empty-state">
                データがありません
            </td></tr>`;
        }

        return paginated.map(row => `
            <tr class="table-row" data-id="${row.id || ''}">
                ${this.columns.map(col => `
                    <td>${this.formatCell(row[col.key], col)}</td>
                `).join('')}
            </tr>
        `).join('');
    }

    formatCell(value, column) {
        if (column.render) return column.render(value);
        if (value === null || value === undefined) return '-';
        return this.escapeHtml(String(value));
    }

    escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    setData(data) {
        this.data = data;
        this.currentPage = 1;
        this.render();
    }

    // ... más métodos de sorting, filtering, pagination
}
```

---

## Charts con Chart.js

### Configuración Base

```javascript
// Chart.js defaults para YuKyu theme
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.08)';
Chart.defaults.font.family = "'Open Sans', sans-serif";

const chartColors = {
    primary: '#06b6d4',
    secondary: '#7c3aed',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    gradient: (ctx, c1, c2) => {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, c1);
        gradient.addColorStop(1, c2);
        return gradient;
    }
};
```

### Line Chart (Tendencias)

```javascript
function createTrendChart(canvas, data) {
    const ctx = canvas.getContext('2d');

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: '有給使用率',
                data: data.values,
                borderColor: chartColors.primary,
                backgroundColor: chartColors.gradient(ctx,
                    'rgba(6, 182, 212, 0.3)',
                    'rgba(6, 182, 212, 0)'
                ),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    padding: 12,
                    titleFont: { weight: 'bold' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}
```

### Doughnut Chart (Distribución)

```javascript
function createDistributionChart(canvas, data) {
    return new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    chartColors.primary,
                    chartColors.secondary,
                    chartColors.success,
                    chartColors.warning
                ],
                borderWidth: 0,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            }
        }
    });
}
```

---

## Patrones de Código

### 1. Event Delegation

```javascript
// NO hagas esto
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', handler);
});

// HAZ esto
document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn');
    if (!btn) return;

    const action = btn.dataset.action;
    if (action === 'edit') handleEdit(btn.dataset.id);
    if (action === 'delete') handleDelete(btn.dataset.id);
});
```

### 2. Async/Await con Error Handling

```javascript
async function fetchData(endpoint) {
    try {
        const response = await fetch(`/api/${endpoint}`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        Alert.error('データの取得に失敗しました');
        throw error;
    }
}
```

### 3. Debounce para Búsquedas

```javascript
function debounce(fn, delay = 300) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

// Uso
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', debounce((e) => {
    performSearch(e.target.value);
}, 300));
```

### 4. XSS Prevention

```javascript
const utils = {
    escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    escapeAttr(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    },

    safeNumber(val) {
        const num = parseFloat(val);
        return isNaN(num) ? 0 : num;
    }
};

// Uso en templates
const html = `
    <div data-name="${utils.escapeAttr(user.name)}">
        ${utils.escapeHtml(user.name)}
    </div>
`;
```

---

## Performance

### 1. Lazy Loading de Imágenes

```html
<img src="placeholder.svg"
     data-src="actual-image.jpg"
     loading="lazy"
     alt="Description">
```

### 2. Virtual Scrolling para Tablas Grandes

```javascript
// Para listas con >1000 items, usar virtual scrolling
// o implementar paginación del lado del servidor
```

### 3. Prefers Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

```javascript
const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
).matches;

if (!prefersReducedMotion) {
    // Aplicar animaciones
}
```

---

## Checklist de Calidad

### Código
- [ ] Sin console.log en producción
- [ ] Error handling en todas las llamadas async
- [ ] Event listeners removidos cuando no se usan
- [ ] No memory leaks en componentes

### UI
- [ ] Loading states en todas las operaciones async
- [ ] Empty states cuando no hay datos
- [ ] Error states con opción de retry
- [ ] Skeleton loaders para contenido dinámico

### Performance
- [ ] Imágenes optimizadas (WebP, lazy loading)
- [ ] CSS crítico inline
- [ ] JavaScript minificado
- [ ] Debounce en inputs de búsqueda

### Accesibilidad
- [ ] Navegable por teclado
- [ ] Focus states visibles
- [ ] ARIA labels en botones de icono
- [ ] Reduced motion respetado
