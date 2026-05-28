---
name: skill-creator
description: Esta habilidad guía al agente en la creación de nuevas habilidades profesionales y consistentes en español, siguiendo los estándares de Google Antigravity.
---

# Skill Creator (Creador de Habilidades)

Esta habilidad te permite crear nuevas habilidades de manera estructurada. Úsala siempre que necesites expandir tus capacidades mediante la creación de una nueva "skill".

## Cuándo usar esta habilidad
- Cuando el usuario te pida crear una nueva habilidad o herramienta interna.
- Cuando identifiques un proceso repetitivo que podría beneficiarse de estar documentado como una habilidad.
- Cuando necesites asegurar que una nueva habilidad siga los estándares de estructura y nomenclatura oficiales.

## Instrucciones para el Agente

### 1. Estructura de la Habilidad
Crea siempre una carpeta dentro de `.agent/skills/` con el nombre de la habilidad en minúsculas y guiones (kebab-case).

Estructura recomendada:
- `SKILL.md` (Obligatorio): Instrucciones principales.
- `scripts/` (Opcional): Scripts de apoyo.
- `examples/` (Opcional): Ejemplos de uso.
- `resources/` (Opcional): Plantillas o recursos estáticos.

### 2. Formato del archivo SKILL.md
El archivo debe comenzar con un frontmatter de YAML y seguir con Markdown:

```markdown
---
name: nombre-de-la-habilidad
description: Descripción clara en tercera persona de lo que hace la habilidad.
---

# Título de la Habilidad

## Cuándo usar esta habilidad
- Caso de uso 1
- Caso de uso 2

## Cómo usarla
Instrucciones detalladas paso a paso.
```

### 3. Mejores Prácticas
- **Idioma**: Escribe las instrucciones y descripciones en **español** si el usuario así lo prefiere.
- **Concisión**: Sé directo y evita explicaciones innecesarias.
- **Accionable**: Las instrucciones deben ser claras para que tú (el agente) sepas exactamente qué herramientas usar y cómo proceder.
- **Frontmatter**: La `description` es crucial porque es lo que usas para decidir qué habilidad activar.

## Ejemplo de creación
Si el usuario pide una habilidad para "limpiar archivos temporales", deberías crear:
1. Carpeta: `.agent/skills/clean-temp-files/`
2. Archivo: `.agent/skills/clean-temp-files/SKILL.md`
