---
name: changelog-gen
description: Crea automáticamente changelogs orientados al usuario a partir de commits de git. Analiza el historial, categoriza los cambios y transforma commits técnicos en notas de release claras y amigables para el cliente.
---

# Generador de Changelog

Esta skill transforma los commits técnicos de git en changelogs elegantes y fáciles de usar que tus clientes y usuarios realmente entenderán y apreciarán.

## Cuándo usar esta Skill

- Preparar las notas para una nueva release de software.
- Crear resúmenes semanales o mensuales de actualizaciones de producto.
- Documentar cambios para los clientes.
- Escribir las novedades para las tiendas de aplicaciones (App Store, Play Store).
- Generar notificaciones de actualización.
- Crear documentación interna sobre los lanzamientos.
- Mantener una página pública de changelog o actualizaciones de producto.

## Qué Hace esta Skill

1.  **Escanea el Historial de Git**: Analiza los commits de un período de tiempo específico o entre versiones.
2.  **Categoriza los Cambios**: Agrupa los commits en categorías lógicas (funcionalidades, mejoras, correcciones de errores, cambios disruptivos, seguridad).
3.  **Traduce de Técnico a Amigable**: Convierte el lenguaje de los commits de desarrollador a uno orientado al cliente.
4.  **Formatea Profesionalmente**: Crea entradas de changelog limpias y estructuradas.
5.  **Filtra el Ruido**: Excluye commits internos (refactorización, tests, etc.).
6.  **Sigue las Mejores Prácticas**: Aplica directrices de changelog y la voz de tu marca.

## Cómo Usar

### Uso Básico

Desde el repositorio de tu proyecto:

```
Crea un changelog con los commits desde la última release
```

```
Genera un changelog para todos los commits de la última semana
```

```
Crea las notas de la release para la versión 2.5.0
```

### Con Rango de Fechas Específico

```
Crea un changelog para los commits entre el 1 y el 15 de marzo
```

### Con Guías de Estilo Personalizadas

```
Crea un changelog para los commits desde la v2.4.0, usando mis guías de estilo definidas en ESTILO_XXX.md.
```

Si el cliente no indica un estilo explícitamente, usa [ESTILO_CHANGELOG](references/ESTILO_CHANGELOG.md) como estilo predeterminado.

## Ejemplo

**Usuario**: "genera el changelog de esta semana"

**Salida**:

```markdown
# Actualizaciones - Semana del 2026-01-07 al 2026-01-14

  ## Nuevas funcionalidades

  - Soporte A2A end-to-end: bindings HTTP+JSON y JSON-RPC, scaffolding gRPC, almacenamiento de tareas, suscripciones y push config para interoperar entre agentes.
  - Discovery avanzado: nuevos providers, registro y soporte de AgentCard para descubrimiento de agentes y reintentos.
  - Gobernanza configurable: loader y motor de politicas con integracion en demos y ejemplo de politica deny.
  - Planner mas rico: condiciones avanzadas y auditoria; mejora de hooks de auditoria.

  ## Mejoras

  - Experiencia de demo y UI: streaming web, estilos finales de UI, defaults de discovery y guias de ejecucion mas claras.
  - CLI y operaciones: comandos avanzados, overrides de config via CLI y barrido runtime.
  - Observabilidad: propagacion de trace context en A2A gRPC.

  ## Correcciones

  - Runner y scripts: arreglos en argumentos y expansion de config del demo runner; flag verbose consistente.
  - A2A y tareas: correcciones en manejo de task id y validacion de recursos/operaciones terminales.

  ## Documentacion

  - Arquitectura y roadmap: actualizaciones de estado A2A/planner y avances de roadmap.e
  - Demos y ejemplos: referencias de ejecucion de agentes y ajustes en ejemplos MCP.

```

## Consejos

- Ejecuta la skill desde la raíz de tu repositorio git.
- Especifica rangos de fechas para changelogs más acotados.
- Usa tu propio fichero `ESTILO_CHANGELOG.md` para un formato consistente. Si no se especifica, se usa [ESTILO_CHANGELOG.md](references/ESTILO_CHANGELOG.md) por defecto.
- Revisa y ajusta el changelog generado antes de publicarlo.
- Guarda la salida directamente en tu fichero `CHANGELOG.md`.

## Casos de Uso Relacionados

- Crear las notas de una release en GitHub.
- Escribir las descripciones de actualización para tiendas de aplicaciones.
- Generar correos electrónicos de actualización para usuarios.
- Crear publicaciones para anunciar novedades en redes sociales.
