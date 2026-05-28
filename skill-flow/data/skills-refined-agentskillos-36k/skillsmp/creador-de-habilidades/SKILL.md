---
name: Creador de Habilidades
description: Skill especializado en la creación de nuevas habilidades siguiendo los estándares del proyecto BIZCONTROL.
---

# 🛠️ Creador de Habilidades (Skill Builder)

Este skill proporciona la estructura y las directrices necesarias para expandir las capacidades de los agentes en el espacio de trabajo de **MCH Control**.

## 📁 Estructura de una Habilidad
Cada nueva habilidad debe residir en su propio directorio dentro de `.agent/skills/`:
- `.agent/skills/NOMBRE_HABILIDAD/`
  - `SKILL.md` (Obligatorio: Instrucciones principales y metadatos)
  - `scripts/` (Opcional: Scripts de automatización o ayuda)
  - `resources/` (Opcional: Plantillas, JSONs, o activos)

## 📝 Formato de SKILL.md
El archivo debe comenzar con un encabezado YAML:
```yaml
---
name: Nombre Legible
description: Breve descripción del propósito
---
```

### Secciones Recomendadas:
1. **Perfil**: Identidad del agente al usar esta habilidad.
2. **Misión**: El objetivo principal que persigue.
3. **Protocolos**: Pasos específicos a seguir.
4. **Reglas de Oro**: Restricciones o principios innegociables (ej. Soberanía de Divisas, Estética Premium).

## 🚀 Proceso de Creación
1. **Definición**: Clarificar el rol (ej. Especialista en Inventario, Auditor de Ventas).
2. **Diseño**: Asegurar que las acciones respeten [Diseño.md](file:///c:/Users/Yoe_Laptop/.gemini/antigravity/scratch/business_control_system/Dise%C3%B1o.md) (40px border-radius, colores rosa/negro).
3. **Persistencia**: Asegurar que interactúe correctamente con `data.js` y Firebase.
4. **Validación**: Verificar que el agente pueda leer y aplicar el skill.

## 📋 Plantilla Base para SKILL.md
```markdown
---
name: [Nombre de la Habilidad]
description: [Descripción breve]
---
# [Nombre de la Habilidad]

## Perfil
- [Rol específico]

## Misión de la Habilidad
- [Objetivo principal]

## Protocolos de Ejecución
1. [Paso 1]
2. [Paso 2]

## Reglas de Oro
- **Consistencia**: Siempre sincronizar con Git.
- **Divisas**: Respetar USD, EUR, MN y Transferencias.
```

## ⚠️ Reglas Críticas para el Creador
- **Idioma**: Todas las instrucciones deben estar en **Español**.
- **Memoria**: Siempre citar [MEMORIA_PROYECTO.md](file:///c:/Users/Yoe_Laptop/.gemini/antigravity/scratch/business_control_system/MEMORIA_PROYECTO.md) como fuente de verdad.
- **Git**: Recordar al usuario (o al agente) hacer `git pull` antes y `git push` después.
