---
name: secrets-scan
description: Escanea el repositorio FutbolStats buscando secretos expuestos (tokens, credenciales en URLs, api keys, passwords) y genera un reporte con snippets redactados. Usar cuando el usuario pida “escanea secretos”, “secrets scan”, “token”, “api key”, “password”, “dsn”, “credenciales”, “leak”, “hardcoded secret”.
---

# Secrets Scan (FutbolStats)

Eres el skill **secrets-scan** para FutbolStats. Tu objetivo es **identificar posibles secretos expuestos** (con severidad) y devolver un **reporte accionable** sin filtrar el valor completo.

## Reglas estrictas (no negociables)

- **NUNCA** muestres el valor completo de un secreto (aunque sea obvio).
- **Solo** muestra snippets **REDACTADOS** con este formato: **primeros 3 chars + "..." + últimos 3 chars** (ej: `"rpa...7R3"`).
  - Si el string tiene < 7 chars, devuelve `"***"` (no intentes reconstruir nada).
- **Solo usar herramientas**: `Read`, `Grep`, `Glob`.
  - **PROHIBIDO** usar Bash/Shell o editar/escribir archivos como parte del escaneo.
- **No hagas dumps**: evidencia mínima (1–2 líneas por hallazgo).

## Rutas a EXCLUIR (ignorar siempre)

- `CLAUDE.local.md`
- `.env*`
- `.claude/`
- `node_modules/`
- `venv/`, `.venv/`
- `ios/**/Secrets.xcconfig`

## Definición de severidad

- **HIGH**: Token/key real o credenciales claras (ej: `rpa_`, `ghp_`, `Bearer <token>`, `AIza...`, `sk-...`, URL con `user:pass@`) expuesto en archivo trackeado.
- **MED**: Patrón sospechoso que *podría* ser secreto (ej: `api_key=...`, `password: ...`, `dsn=...`) pero requiere contexto.
- **LOW**: String largo alfanumérico (≥ 32) que merece revisión manual; potencial falso positivo.

## Patrones a buscar

### 1) Tokens conocidos (HIGH)
- `rpa_` (RunPod)
- `ghp_` (GitHub)
- `Bearer ` (headers)
- `AIza` (Google)
- `sk-` (OpenAI/Stripe)

### 2) URLs con credenciales (HIGH)
- `postgresql://user:pass@`
- `https://user:pass@`
- `mongodb://...@` (incluye `mongodb+srv://`)

### 3) Claves genéricas (MED)
- `api_key`, `apikey`, `api-key`
- `secret`, `token`, `password`
- `dsn`, `connection_string`

### 4) Strings largos sospechosos (LOW)
- Alfanuméricos **≥ 32 chars** en: `.py`, `.ts`, `.tsx`, `.swift`, `.md`
- Excluir (falso positivo típico): hashes git (40 hex) y UUIDs documentados

## Procedimiento (siempre)

### 0) Preparación rápida (sin side-effects)

- Usa `Glob`/`Grep` para localizar, pero **omite** cualquier match cuya ruta caiga en “Rutas a EXCLUIR”.
- Si necesitas verificar si un archivo “sensible” está ignorado, usa `Read` sobre `.gitignore` y responde **SI/NO**.

### 1) Ejecuta búsquedas con Grep (una por patrón)

Sugerencia: empieza por HIGH y baja.

- **HIGH / tokens conocidos** (búsqueda literal o regex simple):
  - `rpa_`
  - `ghp_`
  - `Bearer `
  - `AIza`
  - `sk-`

- **HIGH / URLs con credenciales** (regex):
  - `postgresql://[^\\s:]+:[^@\\s]+@`
  - `https?://[^\\s:]+:[^@\\s]+@`
  - `mongodb(\\+srv)?://[^\\s:]+:[^@\\s]+@`

- **MED / claves genéricas** (idealmente case-insensitive):
  - `(?i)\\b(api[_-]?key|secret|token|password|dsn|connection_string)\\b`

- **LOW / strings alfanuméricos largos** (solo extensiones objetivo):
  - Regex: `\\b[A-Za-z0-9]{32,}\\b`
  - Ejecuta esta búsqueda **limitada** a `*.{py,ts,tsx,swift,md}` usando el filtro `glob`.

### 2) Filtra falsos positivos

Para cada match:
- **Ignora** ejemplos/documentación explícita si el valor parece placeholder (ej: `YOUR_API_KEY`, `xxxxx`, `example`, `changeme`) y no hay credenciales reales.
- **Ignora** hashes git: `\\b[0-9a-f]{40}\\b` (si el contexto indica commit/hash).
- **Ignora** UUIDs: `\\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\b` cuando estén documentados como IDs.
- Si no es claramente falso positivo, **mantén** el hallazgo pero baja severidad si aplica.

### 3) Redacta el snippet (obligatorio)

Regla fija:
- Extrae el “valor candidato” (token/credencial/string largo).
- Devuelve `"AAA...ZZZ"` donde `AAA` son los primeros 3 chars y `ZZZ` los últimos 3 chars.
- **Nunca** incluyas más del valor.

### 4) Genera reporte (formato requerido)

#### Hallazgos

| Archivo | Línea | Tipo | Snippet (redactado) | Severidad | Acción |
|---------|-------|------|---------------------|-----------|--------|
| `src/config.py` | 42 | `api_key` | `"sk-...xyz"` | HIGH | Mover a env var |

#### Archivos sensibles detectados

- [ ] `archivo` - ¿En `.gitignore`? **SI/NO**

Incluye aquí cualquier archivo que:
- sea un contenedor típico de secretos (ej: `.env`, `Secrets.xcconfig`, `credentials.json`, `*.pem`, `*.p12`), o
- esté en rutas a excluir pero exista en el repo (menciona solo nombre/ruta; no contenido).

#### Recomendaciones

1. Mover secretos a **env vars** y leerlos vía configuración (ej: `os.environ[...]` / settings).
2. **Rotar** tokens/keys que parezcan reales y revocar los antiguos.
3. Añadir archivos sensibles a `.gitignore` (si aplica) y eliminar del historial si ya fueron commiteados.
4. Implementar guardrails: pre-commit secrets scan / CI secret scanning.

