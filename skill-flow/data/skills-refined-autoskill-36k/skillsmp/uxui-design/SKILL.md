---
name: UX/UI Design
description: Skill experta en Diseño, Accesibilidad (A11y) y Experiencia de Usuario.
---

# 🎨 Protocolo Antigravity: Skill UI/UX

> **Core Principle:** "User-Centricity". Diseña para las personas, no para las pantallas. Claridad > Estética.

## 1. Principios Fundamentales
- **Accesibilidad Primero (A11y):** No es negociable. Cumplimiento WCAG 2.1 AA mínimo.
- **Consistencia:** "No me hagas pensar". Patrones predecibles.
- **Feedback:** El sistema siempre debe informar qué está pasando (loading, success, error).

## 2. Accesibilidad (A11y)
- **Contraste:** Texto normal 4.5:1, Texto grande 3:1.
- **Teclado:** Todo debe ser operable sin mouse. (Foco visible obligatorio).
- **Semántica:** Usa HTML correcto (`<button>` vs `div onClick`).
- **Screen Readers:** `alt` text en imágenes, `aria-label` en botones de solo icono.

## 3. Usabilidad & Heurísticas
- **Estado del Sistema:** Spinners, esqueletos, barras de progreso.
- **Lenguaje Humano:** Mensajes de error claros y accionables (No "Error 500").
- **Control:** Permitir deshacer, cerrar modales fácilmente (Esc, click outside).
- **Prevención:** Validación de formularios inline y clara.

## 4. Diseño Visual (UI)
- **Jerarquía:** Tamaño, color y posición indican importancia. Lo más importante destaca más.
- **Espaciado (Whitespace):** El espacio vacío es activo. Usa múltiplos de 4px u 8px sistemáticamente.
- **Tipografía:** Escala definida, longitud de línea legible (45-75 caracteres).
- **Touch Targets:** Mínimo 44x44px en móviles.

## 5. Mobile First & Responsividad
- Diseña primero para móvil, luego escala.
- Columnas se apilan (Stacking).
- Menús accesibles con el pulgar.
- Evitar `hover` como única interacción crítica.

## 6. Checklist de Validación de Diseño
Antes de aprobar una UI:

### A11y
- [ ] ¿Se ve bien el foco al navegar con Tab?
- [ ] ¿Pasamos el test de contraste de color?
- [ ] ¿Imágenes tienen alt text?

### UI
- [ ] ¿Jerarquía clara? (H1 > H2 > Body)
- [ ] ¿Espaciado consistente (grid system)?
- [ ] ¿Feedback inmediato al interactuar?

### Mobile
- [ ] ¿Elementos clickeables suficientemente grandes?
- [ ] ¿No hay scroll horizontal accidental?
- [ ] ¿Texto legible sin zoom?

---
**Recuerda:** Una buena UI es invisible; el usuario logra su objetivo sin notar la interfaz.
