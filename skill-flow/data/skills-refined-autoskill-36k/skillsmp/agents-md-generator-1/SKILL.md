---
name: agents-md-generator
description: Genera y mantiene archivos AGENTS.md para cualquier proyecto, incluyendo estructura, uso, comandos, convenciones y un indice JIT cuando el repo es complejo. Usala cuando el usuario pida crear o mejorar AGENTS.md o incorporar principios de optimizacion para Go, Python o JS/TS.
---

# Generador de AGENTS.md

## Objetivo

Crear `AGENTS.md` utiles, concisos y genericos para cualquier agente compatible con AGENTS.md. Deben servir como guia operativa para trabajar en el repo con minimo contexto.

## Flujo recomendado

1) **Analizar el repositorio**
- Identificar tipo de repo (simple, multi-paquete, monorepo, multi-servicio).
- Detectar lenguajes, frameworks, herramientas de build/test/lint.
- Localizar carpetas clave: apps, services, packages, libs, workers, infra.

2) **Decidir el modo**
- **Proyecto simple**: un unico `AGENTS.md` en raiz.
- **Proyecto complejo**: `AGENTS.md` en raiz + indice JIT que apunte a subcarpetas; crear AGENTS.md adicionales solo cuando aporten valor real.
- Criterios de complejidad: varios lenguajes, multiples servicios/apps, >6 carpetas principales.

3) **Construir el contenido**
- Mantener el archivo < 200 lineas.
- Separar secciones con titulos claros en mayusculas.
- Usar placeholders `TODO:` cuando falte informacion.

4) **Optimizacion y reuso**
- Si el repo usa Go/Python/JS/TS, leer los documentos de `references/` correspondientes y sintetizar en una seccion "OPTIMIZACION Y REUSO".

## Secciones minimas

Incluye siempre estas secciones (ajusta nombres solo si hay una convención local):
- RESUMEN DEL PROYECTO (cometido + descripción + usuarios/ámbito)
- ESTRUCTURA DEL PROYECTO (árbol alto nivel y ubicación de código/tests/docs/config)
- STACK Y HERRAMIENTAS (lenguajes + frameworks + build/test/lint)
- FLUJOS DE TRABAJO (run, test, build/deploy)
- CONVENCIONES Y NORMAS (estilo, naming, commits si aplica)
- USO DEL AGENT (que hacer / que evitar)
- JIT INDEX (solo si proyecto complejo)
- OPTIMIZACION Y REUSO (si aplica)

## Salida

- Entregar **solo** el contenido de cada `AGENTS.md`.
- Si hay multiples archivos, usar este formato por bloque:

```
---
File: `AGENTS.md`
---
[contenido]
```

## Recursos

- Plantilla base: `assets/AGENTS-template.md`
- Optimizacion Go: `references/optimization-go.md`
- Optimizacion Python: `references/optimization-python.md`
- Optimizacion JS/TS: `references/optimization-js-ts.md`
