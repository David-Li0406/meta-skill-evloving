---
name: Frontend React
description: Skill experta en desarrollo Frontend con React, TypeScript y Tailwind CSS.
---

# ⚛️ Protocolo Antigravity: Skill Frontend (React)

> **Core Principle:** Componentes puros, predecibles y compostables. UI declarativa sobre imperativa.

## 1. Stack & Principios
- **React:** Functional Components + Hooks (Prohibido Class Components).
- **TypeScript:** Strict Mode. `any` está prohibido (usar `unknown` o generics).
- **Styling:** Tailwind CSS (Utility-first).

## 2. Estructura de Archivos (Feature-First)
Organizar el código por funcionalidad ("Features") en lugar de por tipo técnico.

```text
src/
  features/
    auth/
      components/  # Componentes exclusivos de Auth
      hooks/       # Hooks exclusivos de Auth
      types/       # Interfaces de Auth
    dashboard/
  components/      # Componentes UI compartidos (Button, Input)
  hooks/           # Hooks compartidos
```

## 3. Diseño de Componentes
- **SRP:** Un componente hace una cosa. Si tiene demasiados `useEffect` o estados, divídelo.
- **Contenedor vs Presentacional:** Separar lógica (hooks, data fetching) de vista (JSX, estilos).
- **Props:** Interfaces explícitas. Usar destructuring. Evitar prop-drilling excesivo (usar Context o Composition).

## 4. Estado y Hooks
- **useState:** Para estado local UI simple.
- **useReducer:** Para estado complejo interdependiente.
- **Context:** Para estado global temático o de sesión (evitar abusar para data frecuente).
- **Custom Hooks:** Extraer lógica reutilizable siempre (`useForm`, `useFetch`).

## 5. Rendimiento
- **Re-renders:** Entender cuándo y por qué ocurre un render.
- **Memoización:** Usar `useMemo` y `useCallback` solo ante problemas de performance medidos, o para estabilidad referencial en dependencias de efectos.
- **Code Splitting:** `React.lazy` para rutas y modales pesados.
- **Imágenes:** `loading="lazy"`, formatos modernos (WebP), dimensiones explícitas.

## 6. JSX Limpio
- **Condicionales:** Ternarios para casos simples. Short-circuit (`&&`) con cuidado (cuidado con `0`).
- **Listas:** `key` única y estable (IDs de DB, no índices de array).
- **No Lógica en View:** Extraer cálculos complejos fuera del return.

## 7. Tailwind Best Practices
- Usar clases utilitarias directamente.
- Extraer a componentes (`<Button>`) para reutilización, NO usar `@apply` indiscriminadamente.
- Mantener consistencia con `tailwind.config.js` (colores, espaciado).

## 8. Testing Check
- [ ] ¿Testeas lo que el usuario ve (Behavior), no la implementación interna?
- [ ] ¿Cubres casos de éxito y error?
- [ ] ¿Componentes accesibles (roles ARIA)?

## 9. Tooling & Calidad
> Consulta la skill `quality-assurance` para detalles de configuración.
- **Linter:** ESLint obligatorio (`npm run lint`). Prohibido ignorar reglas de hooks.
- **Formatting:** Prettier (`npm run format`).
- **Commits:** Pre-commit hooks activados.

---
**Recuerda:** El frontend es lo que el usuario toca. Haz que se sienta sólido, rápido y profesional.
