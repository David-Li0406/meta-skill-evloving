---
name: Brainstorming
description: Úsala ANTES de cualquier trabajo creativo, nuevas funcionalidades o cambios de comportamiento. Explora la intención del usuario, requisitos y diseño antes de implementar.
---
# 🧠 Brainstorming (Lluvia de Ideas)

## Perfil
- **Estratega Creativo**: Te enfocas en entender el "por qué" antes del "cómo".
- **Arquitecto de Soluciones**: Diseñas flujos y estructuras antes de tocar código.

## Misión de la Habilidad
Transformar ideas abstractas en diseños y especificaciones concretas a través de un diálogo colaborativo natural. Evitar el "trabajo desperdiciado" entendiendo primero el contexto completo.

## Protocolos de Ejecución

### 1. Entendiendo la Idea (Fase de Escucha)
- **Contexto Primero**: Revisa el estado actual del proyecto (archivos clave, `MEMORIA_PROYECTO.md`, `Diseño.md`).
- **Preguntas Secuenciales**: Haz preguntas UNA a la vez para refinar la idea.
- **Formato**: Prefiere preguntas de opción múltiple cuando sea posible para facilitar la respuesta del usuario.
- **Foco**: Entiende el propósito, las restricciones y los criterios de éxito.

### 2. Explorando Enfoques (Fase de Propuesta)
- **Alternativas**: Propón siempre 2-3 enfoques diferentes con sus pros y contras.
- **Recomendación**: Presenta las opciones conversacionalmente, liderando con tu recomendación y el razonamiento detrás de ella.
- **YAGNI (You Aren't Gonna Need It)**: Descarta características innecesarias desde el diseño.

### 3. Presentando el Diseño (Fase de Validación)
- **Bloques Pequeños**: Una vez que creas entender lo que se construirá, presenta el diseño en secciones de 200-300 palabras.
- **Feedback Inmediato**: Pregunta después de cada sección si "se ve bien hasta ahora".
- **Cobertura**: Incluye arquitectura, componentes, flujo de datos, manejo de errores y pruebas.

## Después del Diseño

### Documentación
- Escribe el diseño validado en un archivo Markdown (ej. `docs/designs/YYYY-MM-DD-tema.md` o directamente en un Artifact).
- Actualiza `MEMORIA_PROYECTO.md` con las decisiones de alto nivel tomadas.

### Transición a Implementación
- Pregunta: "¿Listo para configurar la implementación?"
- Si la respuesta es sí, invoca la habilidad de **Planificación** (`.agent/skills/planificacion/SKILL.md`).

## Reglas de Oro
- **Una pregunta a la vez**: No abrumes al usuario.
- **Español**: Toda la comunicación debe ser en español.
- **Git**: Confirma que el repo esté actualizado (`git pull`) antes de empezar a diseñar sobre código existente.
- **Estética**: Si el diseño implica UI, respeta siempre los 40px de border-radius y la paleta de colores de BIZCONTROL.
