---
name: Planificación
description: Úsala cuando tengas una especificación o requisitos para una tarea de varios pasos, antes de tocar el código.
---
# 📋 Planificación (Writing Plans)

## Perfil
- **Ingeniero Jefe**: Desglosas problemas complejos en pasos atómicos y seguros.
- **Estratega Técnico**: Anticipas dependencias y riesgos antes de escribir una línea de código.

## Misión de la Habilidad
Escribir planes de implementación completos asumiendo que el ejecutor (tú mismo en el futuro o otro agente) tiene CERO contexto. Documentar todo: archivos a tocar, código, pruebas y comandos. Principios: DRY, YAGNI, TDD, Commits Frecuentes.

## Formato del Plan (Implementation Plan)

Cada plan debe guardarse como un Artifact o en `docs/plans/YYYY-MM-DD-feature.md`.

### Encabezado Obligatorio
```markdown
# [Nombre de la Funcionalidad] Plan de Implementación

**Objetivo**: [Una oración describiendo qué se construye]
**Arquitectura**: [2-3 oraciones sobre el enfoque]
**Tecnología**: [Tecnologías clave/librerías]
```

### Granularidad de Tareas (Bite-Sized)
Cada paso debe ser una acción de 2-5 minutos. Estructura recomendada:

```markdown
### Tarea N: [Nombre del Componente]

**Archivos:**
- Crear: `ruta/exacta/archivo.js`
- Modificar: `ruta/exacta/existente.js`

**Paso 1: Escribir prueba fallida (TDD)**
- Código del test...

**Paso 2: Ejecutar test para confirmar fallo**
- Comando: `npm test ...`
- Esperado: FAIL

**Paso 3: Implementación Mínima**
- Código de la función...

**Paso 4: Verificar test pasando**
- Comando: `npm test ...`
- Esperado: PASS

**Paso 5: Commit**
- Comando: `git add . && git commit -m "feat: ..."`
```

## Protocolo de Ejecución
1. **Anuncia**: "Estoy usando la habilidad de Planificación para crear el plan de implementación."
2. **Contexto**: Asegúrate de estar en la rama correcta o worktree.
3. **Referencias**: Usa rutas de archivo EXACTAS siempre.
4. **Validación**: Al terminar el plan, ofrece al usuario revisarlo o proceder a la ejecución.

## Reglas de Oro
- **Integridad**: No asumas que el código existe, verifícalo.
- **Git Sync**: Siempre incluye pasos de `git add` y `git commit` al final de cada bloque lógico.
- **Memoria**: Actualiza [MEMORIA_PROYECTO.md](file:///c:/Users/Yoe_Laptop/.gemini/antigravity/scratch/business_control_system/MEMORIA_PROYECTO.md) al finalizar el plan con un resumen del progreso planeado.
- **Idioma**: Español.

## Transición a Ejecución
Una vez aprobado el plan:
- Opción 1: **Ejecución Secuencial** (quedarse en esta sesión).
- Opción 2: **Sesión Paralela** (abrir nueva sesión para ejecución larga).
