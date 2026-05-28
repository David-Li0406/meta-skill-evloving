---
name: Clean Code
description: Guía definitiva para escribir código limpio, legible y mantenible según el Protocolo Antigravity.
---

# 🚀 Protocolo Antigravity: Skill Clean Code

> **Versión:** 1.0.0
> **Objetivo:** Gravedad Cero (Eliminación total de deuda técnica y fricción cognitiva).
> **Mandato Principal:** El código se escribe para humanos primero, para máquinas después.

Esta Skill define las directrices obligatorias para cualquier código escrito en este proyecto.

## 📋 1. Nomenclatura: Semántica y Claridad

Los nombres son la interfaz de usuario del código.

### 1.1. Intención Revelada
El nombre debe responder: ¿Por qué existe? ¿Qué hace? ¿Cómo se usa?
- **❌ Incorrecto:** `var d; // días transcurridos`
- **✅ Correcto:** `var daysSinceModification;`

### 1.2. Evitar Desinformación
No usar términos técnicos (List, Map) si la estructura no lo es. Evitar prefijos/sufijos redundantes.
- **❌ Incorrecto:** `accountList` (si no es una List), `IUser` ( interfaz), `CUser` (clase).
- **✅ Correcto:** `accounts`, `User`, `UserImpl`.

### 1.3. Pronunciabilidad y Búsqueda
Los nombres deben ser pronunciables y fáciles de buscar (Greppable).
- **❌ Incorrecto:** `genymdhms` (Generation Year Month Day...)
- **✅ Correcto:** `generationTimestamp`

### 1.4. Convenciones de Naming
- **Clases/Tipos:** `PascalCase` (Sustantivos, ej. `Customer`, `WikiPage`).
- **Métodos/Funciones:** `camelCase` (Verbos, ej. `postPayment`, `deletePage`).
- **Constantes:** `UPPER_SNAKE_CASE` (ej. `MAX_RETRY_COUNT`).
- **Variables/Propiedades:** `camelCase`.
- **Archivos:** Acorde al framework (ej. React: `PascalCase` componentes, `camelCase` hooks/utils).

---

## ⚡ 2. Funciones: Átomos de Lógica

### 2.1. Pequeñas y de Responsabilidad Única (SRP)
Una función debe hacer **una sola cosa**, hacerla bien y hacerla solo ella.
- Si puedes extraer otra función de su interior con un nombre lógico, tu función original es demasiado grande.

### 2.2. Niveles de Abstracción
**Regla del Paso Descendente:** El código debe leerse como un periódico, de lo más importante a los detalles.
- Una función no debe mezclar lógica de negocio (Alto Nivel) con detalles de implementación (Bajo Nivel, ej. SQL, HTML strings).

### 2.3. Argumentos
- **0 Argumentos:** Ideal.
- **1-2 Argumentos:** Aceptable.
- **3+ Argumentos:** 🚩 **Refactorizar**. Encapsular en un objeto de contexto o configuración.
- **Flag Arguments:** JAMÁS pases un booleano (`render(true)`). Divide la función (`renderForSuite()` y `renderSingle()`).

### 2.4. Pureza y Efectos Secundarios
Evita modificar variables globales o argumentos pasados por referencia si no es explícito.
- **Query/Command Separation:** Una función debe hacer algo (Command) o responder algo (Query), pero no ambas.

---

## 📝 3. Comentarios

*El código limpio se explica a sí mismo. Un comentario es a menudo una disculpa por no haber escrito un código más claro.*

### 3.1. Prohibidos
- **Redundantes:** `i++; // incrementa i`
- **Código comentado:** Bórralo. Git es tu historia.
- **Marcadores:** `////////////` (Ruido visual).
- **Cierre:** `} // end if`

### 3.2. Permitidos / Obligatorios
- **TODO:** Notas de deuda técnica (usar formato `// TODO: descripción`).
- **Explicación de "Por qué" (no "Qué"):** Justificar decisiones no obvias o workarounds necesarios.
- **Advertencias:** "Este test es lento por X razón".

---

## 🧱 4. Objetos, Estructuras y Ley de Demeter

### 4.1. Abstracción
No expongas detalles de implementación.
- **❌ Incorrecto:** `getGallons()`
- **✅ Correcto:** `getFuelPercentage()`

### 4.2. Ley de Demeter (No hables con extraños)
Un método `f` de la clase `C` solo debe llamar a:
1. Métodos de `C`.
2. Objetos creados por `f`.
3. Argumentos de `f`.
4. Variables de instancia de `C`.
- **Evitar Train Wrecks:** `ctx.getOptions().getScratchDir().getAbsolutePath()`

---

## 🛡️ 5. Manejo de Errores

### 5.1. Excepciones > Códigos de Error
Usa Excepciones. No ensucies la lógica principal con nidos de `if (err != null)`.

### 5.2. No Nulos
- **No devuelvas Null:** Devuelve Array vacío, Optional, o Null Object Pattern.
- **No pases Null:** Asume que los argumentos no son null a menos que se especifique lo contrario (defensive programming).

---

## 🏗️ 6. Arquitectura SOLID

1.  **SRP (Single Responsibility):** Una clase, una razón para cambiar.
2.  **OCP (Open/Closed):** Abierto a extensión, cerrado a modificación.
3.  **LSP (Liskov Substitution):** Subclases deben ser sustituibles por sus padres.
4.  **ISP (Interface Segregation):** Interfaces pequeñas específicas > Interfaces grandes generales.
5.  **DIP (Dependency Inversion):** Depende de abstracciones, no de concreciones.

---

## 🧪 7. Testing

El código sin test es deuda técnica instantánea.

- **F.I.R.S.T.:** Fast, Independent, Repeatable, Self-Validating, Timely.
- **Un Assert por Test:** Prueba un solo concepto lógico por test.
- **Separación:** Tests unitarios, Tests de integración, Tests E2E.

---

## ✅ Checklist de Auto-Revisión

Antes de dar una tarea por terminada, verifica:

- [ ] ¿Los nombres revelan intención?
- [ ] ¿Funciones < 20 líneas (aprox) y hacen una sola cosa?
- [ ] ¿No hay números mágicos ni strings hardcodeados?
- [ ] ¿Manejo de errores robusto (sin `try/catch` vacíos)?
- [ ] ¿Tests cubren funcionalidad principal y edge cases?
- [ ] ¿Tests cubren funcionalidad principal y edge cases?
- [ ] ¿Código formateado consistentemente?

## 🤖 8. Automatización
El "Clean Code" también es código estandarizado.
- Usa **Prettier** para no discutir sobre espacios vs tabs.
- Usa **ESLint** para atrapar errores antes de que ocurran.
- Si el linter se queja, el código está sucio. Corrígelo, no lo ignores (`eslint-disable` solo con justificación escrita).
