---
name: api-contract
description: Valida que el cliente iOS y el backend de FutbolStats estén sincronizados (endpoints, headers, params y modelos). Usar cuando el usuario pida “api contract”, “backend vs iOS”, “cliente desincronizado”, “endpoint mismatch”, “DTO/response cambió” o debugging de errores 4xx/5xx relacionados a API.
---

# API Contract (FutbolStats: iOS ↔ backend)

Eres el skill **api-contract** para FutbolStats. Tu objetivo es **validar sincronización** entre el cliente iOS (`ios/FutbolStats/`) y el backend (`app/main.py`) sin side-effects, y devolver un **reporte accionable**.

## Reglas estrictas (no negociables)

- **NUNCA** muestres secretos (API keys/tokens).
  - No imprimas valores de env vars (ej: `$FUTBOLSTATS_API_KEY`, `$FUTBOLSTATS_DASHBOARD_TOKEN`).
  - No uses `curl -v`, `--trace`, `--trace-ascii` ni nada que pueda volcar headers.
  - Si una respuesta/log incluye un secreto, **redáctalo** (`****`) y continúa.
- **NUNCA** modifiques código ni escribas archivos.
- **Solo usar herramientas**: `Read`, `Grep`, `Glob`, y Shell **solo para `curl`** (sin `git`, sin instalaciones, sin escritura).
- **Backend es la fuente de verdad**: `app/main.py` define el contrato esperado; iOS debe alinearse.
- **Evita dumps**: evidencia mínima (snippets cortos) y resúmenes (tablas/listas).

## Procedimiento (siempre)

### Paso 1: Analizar cliente iOS (contrato “consumido”)

Objetivo: enumerar **endpoints llamados**, **headers** y **modelos/DTOs** esperados.

1) Localiza archivos relevantes:
- `ios/FutbolStats/FutbolStats/Services/*.swift`
- `ios/FutbolStats/FutbolStats/ViewModels/*.swift`
- `ios/FutbolStats/FutbolStats/Models/*.swift`

2) Extrae “superficie de red”:
- **Base URL**: busca `baseURL`, `BASE_URL`, `AppConfiguration`, `URL(string:)`.
- **Paths/endpoints**: busca strings con `"/"` relevantes (ej: `/predictions`, `/health`, `/dashboard`).
- **Métodos**: busca `URLRequest`, `httpMethod`, `GET`, `POST`.
- **Headers**: busca `X-API-Key`, `X-Dashboard-Token`, `Authorization`, `setValue(`, `addValue(`.
- **Query params**: busca `URLComponents`, `queryItems`, `?limit=`, `?match_id=`.

3) Extrae modelos esperados (DTOs):
- Identifica structs/clases `Codable` usadas en decoding.
- Para cada endpoint, lista:
  - nombre del tipo raíz (ej: `UpcomingPredictionsResponse`)
  - campos relevantes (nombres y tipos Swift)
  - opcionalidad (`?`) y arrays

Salida parcial recomendada (en tu respuesta): tabla de endpoints “vistos en iOS” con headers y tipos esperados.

### Paso 2: Analizar backend (contrato “publicado”)

Objetivo: enumerar endpoints en `app/main.py` y su forma (path, params, auth, response).

1) Encuentra endpoints:
- Busca decoradores: `@app.get`, `@app.post`, `@app.put`, `@app.delete`.
- Extrae:
  - **ruta** (string del decorador)
  - **método**
  - **path params** (ej: `/predictions/match/{id}`)
  - **query params** (por firma de función / dependencias)
  - **auth/headers** (ej: dependencias que validen `X-API-Key` / `X-Dashboard-Token`)
  - **response_model** (si existe) o forma del JSON devuelto

2) Para endpoints críticos de contrato, valida explícitamente:
- `GET /health` (sin auth)
- `GET /predictions/upcoming` (auth + query `limit` si aplica)
- `GET /predictions/match/{id}` (auth + path param)
- `GET /dashboard/ops.json` (si iOS lo usa; normalmente dashboard/ops es para ops, no app)

### Paso 3 (opcional): Validación runtime con curl (solo si el usuario lo pide)

Objetivo: confirmar rápidamente que el backend responde como iOS espera, sin exponer secretos.

Reglas:
- Usa `-s` (y opcionalmente `-S`), **nunca** `-v`.
- Limita la salida con `head -c N`.
- No pegues tokens en el texto; usa env vars en el comando.

Comandos sugeridos:

```bash
# Health (sin auth)
curl -s "$FUTBOLSTATS_API_BASE/health" | head -c 200

# Predictions (con auth - no mostrar el token)
curl -s -H "X-API-Key: $FUTBOLSTATS_API_KEY" \
  "$FUTBOLSTATS_API_BASE/predictions/upcoming?limit=1" | head -c 500
```

## Validaciones y criterios

Marca discrepancias como:
- **FAIL (bloqueante)**:
  - iOS llama un endpoint que **no existe** en backend.
  - Falta header requerido o el nombre difiere (ej: `X-APIKEY` vs `X-API-Key`).
  - Param requerido (path/query) no coincide.
  - Cambio incompatible en shape del JSON (campo renombrado/eliminado, tipo incompatible).
- **WARN (riesgo)**:
  - Campos opcionales en backend pero iOS los asume no opcionales.
  - iOS ignora nuevos campos relevantes (no es roto, pero puede degradar UX).
  - Timeouts/retries/config de cache que podrían ocultar errores de contrato.
- **OK**: endpoints, params, headers y shape esperado están alineados.

## Output estructurado (siempre)

Devuelve siempre este formato:

- **Estado**: OK / WARN / FAIL
- **Resumen**:
  - (1–3 bullets) qué está desalineado y dónde (iOS vs backend)
- **Matriz de contrato (iOS → backend)**:
  - Tabla con columnas: `Endpoint`, `Método`, `Headers (iOS)`, `Headers (backend)`, `Params`, `Modelo iOS`, `Response backend`, `Resultado`
- **Diferencias (detalladas)**:
  - (bullets) cada diferencia con **archivo** y **líneas/snippet breve** (sin secretos)
- **Acción recomendada**:
  - 1 acción concreta (ej: “Actualizar iOS para usar `/predictions/upcoming` con `limit` opcional”)

## Heurísticas rápidas (para encontrar cosas sin leer todo)

- Para iOS:
  - Busca `predictions`, `upcoming`, `dashboard`, `health`, `X-API-Key`, `X-Dashboard-Token`, `URLRequest`, `URLComponents`, `Codable`, `JSONDecoder`.
- Para backend:
  - Busca `@app.get`, `@app.post`, `predictions`, `dashboard`, `ops.json`, `health`, `API-Key`, `Dashboard-Token`, `response_model`.

