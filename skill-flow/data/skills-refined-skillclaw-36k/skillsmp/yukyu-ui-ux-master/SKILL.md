---
name: yukyu-ui-ux-master
description: "Maestro de UI/UX para YuKyuDATA - Diseño de interfaces, experiencia de usuario, accesibilidad WCAG, patrones de interacción japoneses, dark/light mode, glassmorphism, responsive design, micro-interacciones y animaciones fluidas. Especializado en sistemas de gestión empresarial y cumplimiento 労働基準法."
---

# YuKyu UI/UX Master

Sistema experto de UI/UX diseñado específicamente para aplicaciones de gestión empresarial japonesa. Combina las mejores prácticas occidentales con la estética y usabilidad japonesa.

## Cuándo Usar Este Skill

- Diseñar nuevas interfaces o pantallas
- Mejorar la experiencia de usuario existente
- Revisar accesibilidad (WCAG AA/AAA)
- Implementar dark/light mode
- Crear animaciones y micro-interacciones
- Optimizar flujos de trabajo complejos

---

## Principios de Diseño YuKyu

### 1. Filosofía de Diseño

| Principio | Descripción | Implementación |
|-----------|-------------|----------------|
| **清潔感 (Seiketsu-kan)** | Sensación de limpieza | Espacios amplios, colores suaves |
| **使いやすさ (Tsukaiyasusa)** | Facilidad de uso | Acciones en 3 clics máximo |
| **信頼性 (Shinrai-sei)** | Confiabilidad | Feedback inmediato, estados claros |
| **効率性 (Kouritsu-sei)** | Eficiencia | Atajos de teclado, bulk actions |

### 2. Paleta de Colores Oficial

```css
/* Primary - Cyan profesional */
--color-primary-50: #ecfeff;
--color-primary-500: #06b6d4;
--color-primary-700: #0e7490;

/* Accent - Violet elegante */
--color-accent-400: #a78bfa;
--color-accent-600: #7c3aed;

/* Semantic */
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
--color-info: #3b82f6;

/* Neutrals */
--color-neutral-50: #f8fafc;   /* Light bg */
--color-neutral-900: #0f172a;  /* Dark bg */
```

### 3. Tipografía

| Uso | Fuente | Peso | Tamaño |
|-----|--------|------|--------|
| Headings | Poppins | 600-700 | 1.5rem - 2.25rem |
| Body | Open Sans | 400-500 | 0.875rem - 1rem |
| Data/Numbers | JetBrains Mono | 500 | 0.875rem |
| Japanese | Noto Sans JP | 400-600 | Inherit |

---

## Patrones de Componentes

### 1. Glass Panel (Glassmorphism)

```css
.glass-panel {
  background: rgba(15, 23, 42, 0.6);     /* Dark */
  /* background: rgba(255, 255, 255, 0.85); Light */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
```

### 2. Botones con Jerarquía

```css
/* Primary - Acciones principales */
.btn-primary {
  background: linear-gradient(135deg, #06b6d4, #0e7490);
  color: white;
  box-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
}

/* Secondary - Acciones secundarias */
.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Danger - Acciones destructivas */
.btn-danger {
  background: linear-gradient(135deg, #ef4444, #b91c1c);
}
```

### 3. Form Inputs

```css
.input-glass {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  padding: 0.6rem 1rem;
  color: white;
  transition: all 0.3s ease;
}

.input-glass:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--color-primary-400);
  box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.2);
  outline: none;
}
```

### 4. Tablas de Datos

```css
.modern-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.modern-table th {
  background: rgba(15, 23, 42, 0.8);
  position: sticky;
  top: 0;
  z-index: 10;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

.modern-table tbody tr:hover {
  background: rgba(6, 182, 212, 0.05);
}
```

---

## Accesibilidad (WCAG AA)

### Checklist Obligatorio

- [ ] **Contraste**: Mínimo 4.5:1 para texto normal, 3:1 para texto grande
- [ ] **Focus visible**: Anillo de focus en todos los elementos interactivos
- [ ] **Alt text**: Todas las imágenes significativas tienen alt descriptivo
- [ ] **ARIA labels**: Botones con solo icono tienen aria-label
- [ ] **Tab order**: Orden lógico de navegación por teclado
- [ ] **Form labels**: Todos los inputs tienen label asociado
- [ ] **Error messages**: Errores claros y cerca del campo problemático
- [ ] **Reduced motion**: Respetar `prefers-reduced-motion`

### Implementación Focus States

```css
/* Focus visible para navegación por teclado */
:focus-visible {
  outline: 2px solid var(--color-primary-400);
  outline-offset: 2px;
}

/* Ocultar focus para mouse */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Screen Reader Support

```html
<!-- Botón con solo icono -->
<button aria-label="Cerrar modal" class="btn-icon">
  <svg>...</svg>
</button>

<!-- Skip link -->
<a href="#main-content" class="sr-only focus:not-sr-only">
  メインコンテンツへスキップ
</a>

<!-- Live regions para notificaciones -->
<div role="alert" aria-live="polite" class="toast">
  保存しました
</div>
```

---

## Dark/Light Mode

### Variables CSS por Tema

```css
/* Dark Mode (default) */
:root, [data-theme="dark"] {
  --bg-base: #020617;
  --bg-card: rgba(15, 23, 42, 0.6);
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --border-color: rgba(255, 255, 255, 0.08);
}

/* Light Mode */
[data-theme="light"] {
  --bg-base: #f8fafc;
  --bg-card: rgba(255, 255, 255, 0.85);
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: rgba(0, 0, 0, 0.08);
}
```

### JavaScript Toggle

```javascript
// Toggle theme
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}

// Initialize from localStorage
const saved = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', saved);
```

---

## Micro-interacciones

### 1. Hover States

```css
/* Cards */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* Buttons */
.btn:hover {
  filter: brightness(1.1);
}
.btn:active {
  transform: scale(0.98);
}
```

### 2. Loading States

```css
/* Skeleton loading */
.skeleton {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Button loading */
.btn.loading {
  pointer-events: none;
  opacity: 0.7;
}
.btn.loading::after {
  content: '';
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
```

### 3. Transitions

```css
/* Standard durations */
--transition-fast: 150ms ease;
--transition-base: 200ms ease;
--transition-slow: 300ms ease;

/* Prefer transform/opacity over width/height */
.modal {
  transform: scale(0.95);
  opacity: 0;
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.modal.active {
  transform: scale(1);
  opacity: 1;
}
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile first */
--breakpoint-sm: 640px;   /* Tablets */
--breakpoint-md: 768px;   /* Small laptops */
--breakpoint-lg: 1024px;  /* Desktops */
--breakpoint-xl: 1280px;  /* Large screens */
--breakpoint-2xl: 1536px; /* Ultra-wide */
```

### Mobile Considerations

```css
/* Touch targets */
.btn, .nav-link, .table-row {
  min-height: 44px;
  min-width: 44px;
}

/* Readable text */
body {
  font-size: 16px; /* Prevent zoom on iOS */
}

/* Sidebar responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    transform: translateX(-100%);
    z-index: 1000;
  }
  .sidebar.open {
    transform: translateX(0);
  }
}
```

---

## UX Patterns para Gestión Empresarial

### 1. Dashboard KPIs

```
┌─────────────────────────────────────────────────────┐
│  📊 Dashboard                           [2025 ▼]   │
├─────────┬─────────┬─────────┬─────────┬───────────┤
│   125   │   42    │   18    │  94.2%  │   Alert   │
│ 総従業員 │ 有給残高 │ 期限切れ │ 取得率  │  5日義務  │
└─────────┴─────────┴─────────┴─────────┴───────────┘
```

### 2. Data Tables con Acciones

```
┌────┬──────────┬────────┬─────────┬─────────────┐
│ #  │ 名前     │ 残日数 │ 使用日数 │ アクション   │
├────┼──────────┼────────┼─────────┼─────────────┤
│ 01 │ 田中太郎 │ 15.0   │ 5.0     │ [編集] [履歴]│
│ 02 │ 山田花子 │ 12.5   │ 7.5     │ [編集] [履歴]│
└────┴──────────┴────────┴─────────┴─────────────┘
```

### 3. Flujos de Aprobación

```
[申請] ──→ [承認待ち] ──→ [承認済み]
                │
                └──→ [却下]
```

### 4. Estados Visuales

| Estado | Color | Icono | Uso |
|--------|-------|-------|-----|
| Pendiente | Warning (#f59e0b) | ⏳ | Solicitudes en espera |
| Aprobado | Success (#10b981) | ✓ | Acciones completadas |
| Rechazado | Error (#ef4444) | ✗ | Acciones denegadas |
| Crítico | Error pulsante | ⚠ | Requiere atención urgente |

---

## Checklist Pre-Entrega

### Visual
- [ ] No emojis como iconos (usar SVG)
- [ ] Iconos de set consistente (Heroicons/Lucide)
- [ ] Hover states sin layout shift
- [ ] Colores del tema, no hardcodeados

### Interacción
- [ ] cursor-pointer en elementos clickeables
- [ ] Feedback visual en hover
- [ ] Transiciones suaves (150-300ms)
- [ ] Focus states visibles

### Temas
- [ ] Light mode con contraste suficiente
- [ ] Dark mode sin elementos blancos
- [ ] Bordes visibles en ambos modos
- [ ] Probado en ambos temas

### Layout
- [ ] Sin scroll horizontal en móvil
- [ ] Responsive en 375px, 768px, 1024px
- [ ] Contenido no oculto tras elementos fixed
- [ ] Espaciado consistente

### Accesibilidad
- [ ] Alt text en imágenes
- [ ] Labels en formularios
- [ ] ARIA labels en botones de icono
- [ ] prefers-reduced-motion respetado

---

## Recursos

### Iconos Recomendados
- [Heroicons](https://heroicons.com) - Iconos UI
- [Lucide](https://lucide.dev) - Alternativa a Feather
- [Simple Icons](https://simpleicons.org) - Logos de marcas

### Fuentes
- [Google Fonts](https://fonts.google.com)
- Poppins: `https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700`
- Open Sans: `https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600`
- Noto Sans JP: `https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600`

### Herramientas
- [Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors](https://coolors.co) - Paletas de colores
- [Cubic Bezier](https://cubic-bezier.com) - Curvas de animación
