---
name: Quality Assurance
description: Skill experta en Linting, Formateo y Estrategia de Testing Inteligente.
---

# 🛡️ Protocolo Antigravity: Skill QA & Robustez

> **Mantra:** "Si no está probado y no pasa el linter, no existe."

Esta Skill define las herramientas y estrategias mandatorias para garantizar la calidad del código.

## 1. Stack de Herramientas (Tooling Standards)

### 1.1. Frontend (React/TS)
- **Linter:** ESLint con configuración estricta.
    - Plugins obligatorios: `react-hooks` (para reglas de hooks), `jsx-a11y` (accesibilidad), `import` (orden de imports).
    - Regla de oro: `no-explicit-any: error`.
- **Formatter:** Prettier.
    - Configuración estándar: `singleQuote: true`, `semi: true`, `trailingComma: 'all'`, `printWidth: 100`.
- **Pre-commit:** Husky + lint-staged (para correr linter antes de cada commit).

### 1.2. Backend (Supabase/SQL)
- **SQL Linter:** `sqlfluff` o similar (dialecto postgres).
- **Formateo:** Palabras clave en MAYÚSCULAS (`SELECT`, `FROM`), nombres en `snake_case`.

## 2. Estrategia de Testing Inteligente ("Smart Testing")

No testeamos *todo*. Testeamos donde hay **valor**.

### 2.1. ¿Qué testear? (High Value)
- **Lógica de Negocio Pura:** Funciones que calculan precios, validan reglas complejas o transforman datos críticos.
- **Utilidades Compartidas:** Helpers que se usan en toda la app (`formatDate`, `calculateTax`).
- **Componentes Críticos:** Botones de "Pagar", "Enviar", o flows de autenticación.
- **Hooks Personalizados:** Especialmente aquellos con manejo de estado complejo.

### 2.2. ¿Qué NO testear? (Low Value)
- **Configuración:** Archivos de setup si son estándar.
- **UI Trivial:** "El botón es azul". (Esto se ve en revisión visual, no en unit test, a menos que sea un Design System).
- **Librerías de Terceros:** No testeamos que `react` funcione, testeamos que *usamos* react correctamente.

### 2.3. Reglas de Unit Testing
- **Arrange-Act-Assert:** Estructura clara en cada test.
- **Aislamiento:** Mocks para todo lo externo (API calls, base de datos).
- **Nombres Descriptivos:** `it('calculates total with discount correctly')`.

## 3. Workflow de Validación
Antes de dar una tarea por "Done":
1.  **Lint:** `npm run lint` → Debe pasar sin warnings.
2.  **Format:** `npm run format` → Archivos formateados.
3.  **Test:** `npm run test` → Tests de unidades afectadas en verde.
4.  **Build:** `npm run build` → Sin errores de compilación.

---
**Recuerda:** La calidad no es un acto, es un hábito automatizado.
