---
name: Backend Supabase
description: Skill experta en desarrollo Backend con Supabase, Postgres y RLS.
---

# 🐘 Protocolo Antigravity: Skill Backend (Supabase)

> **Core Principle:** "Supabase Native". Utiliza la potencia de Postgres antes de escribir código externo.

## 1. Principios Generales
- **Supabase-Native:** RLS, Triggers, Functions y Realtime nativos preferidos sobre middleware externo.
- **Seguridad por Defecto (RLS):** NUNCA crear una tabla pública sin Row Level Security habilitado.
- **Integridad:** La base de datos es la fuente de la verdad. Usa Foreign Keys, Constraints y Tipos estrictos.
- **Escalabilidad:** Evita N+1 y consultas no indexadas desde el día 1.

## 2. Nomenclatura (Naming Conventions)
- **Tablas:** `snake_case` y **plural** (ej. `users`, `order_items`).
- **Columnas:** `snake_case` (ej. `created_at`, `is_active`).
- **Funciones (RPC):** `snake_case` (ej. `get_user_balance`).
- **IDs:**
    - PK: `id` (uuid v4).
    - FK: `singular_table_name_id` (ej. `user_id` -> `users.id`).

## 3. Seguridad y RLS
> 🚨 **Mandatorio:** `ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;`

### 3.1. Políticas (Policies)
- Definir políticas explícitas para `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
- Usar funciones helper seguras (ej. `auth.uid()`).
- Evitar joins complejos en políticas que se ejecutan por cada fila (impacto de performance).

### 3.2. Roles
- Entender y respetar la diferencia `anon` vs `authenticated`.
- Roles de servicio (`service_role`) solo para tareas administrativas backend-only.

## 4. Estructura de Datos
- **UUID:** Usar `gen_random_uuid()` por defecto.
- **Timestamps:** `created_at` (default `now()`), `updated_at`.
- **JSONB:** Solo para datos flexibles sin esquema fijo. Preferir columnas relacionales.

## 5. Lógica de Negocio
- **Triggers:** Para consistencia de datos (ej. actualizar `updated_at`, contadores cacheados).
- **Edge Functions:** Para lógica compleja, integraciones externas (Stripe, AI), o webhooks.
- **Database Functions:** Para operaciones atómicas transaccionales.

## 6. Performance Checklist
- [ ] ¿Tienen índices las Foreign Keys?
- [ ] ¿Están indexadas las columnas de filtrado frecuente (`WHERE`, `ORDER BY`)?
- [ ] ¿Se usa `limit()` y paginación en queries de listas?
- [ ] ¿RLS policies optimizadas (evitar select n+1 dentro de policies)?

## 7. Control de Cambios
- **Migraciones:** Todo cambio de esquema va en un archivo de migración `.sql`.
- **No UI Edits:** No editar esquema manualmente en producción desde el dashboard.

## 8. Calidad SQL
> Consulta la skill `quality-assurance` para detalles.
- **Linting:** SQL debe ser legible y formateado (`sqlfluff`).
- **Testing:** Unit tests para Edge Functions complejas y PL/pgSQL functions críticas.

---
**Recuerda:** Una base de datos bien diseñada es el cimiento de una aplicación robusta. No tomes atajos aquí.
