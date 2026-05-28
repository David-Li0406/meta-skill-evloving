---
name: revisar-ortografia
description: Revisa la ortografía española en archivos del proyecto (acentos, eñes, signos de interrogación). Usar cuando el usuario diga "revisa ortografía", "busca faltas", "corrige acentos" o invoque /revisar-ortografia.
allowed-tools: Read, Edit, Grep, Glob
---

# Revisar Ortografía en Proyecto QueDure

Esta skill ayuda a revisar y corregir errores ortográficos en español, principalmente acentos y caracteres especiales.

---

## IMPORTANTE: Qué NO cambiar

**NUNCA modificar la ortografía de:**

| Tipo | Ejemplo | Razón |
|------|---------|-------|
| Nombres de campo YAML | `coste_10_anos`, `reparabilidadSource` | Son identificadores del schema |
| Slugs y rutas | `/aprender/indices-reparabilidad` | Son URLs |
| Nombres de archivo | `economia-circular.md` | Rutas del sistema |
| Variables en código | `const anos = 10` | Identificadores de código |
| Tags | `- consumo-consciente` | Identificadores para filtrado |
| IDs y claves | `topic: derecho-reparar` | Valores del sistema |
| Nombres de categoría | `category: electrodomesticos` | Valores predefinidos |

**SÍ modificar:**

| Tipo | Ejemplo incorrecto | Ejemplo correcto |
|------|-------------------|------------------|
| Títulos | `"Indices de reparabilidad"` | `"Índices de reparabilidad"` |
| Descripciones | `"Como elegir productos"` | `"Cómo elegir productos"` |
| Contenido markdown | `## Que es iFixit` | `## Qué es iFixit` |
| Textos en prose | `dura 5 anos` | `dura 5 años` |
| keyTakeaways | `"El indice frances"` | `"El índice francés"` |
| Valores de ejemplo | `"{X-Y anos}"` | `"{X-Y años}"` |

---

## Errores comunes en español

### Acentos en palabras frecuentes

| Incorrecto | Correcto | Contexto |
|------------|----------|----------|
| anos | años | Siempre (excepto variables) |
| indice | índice | Siempre |
| mas | más | Adverbio de cantidad |
| como | cómo | Interrogativo/exclamativo |
| que | qué | Interrogativo/exclamativo |
| cuando | cuándo | Interrogativo |
| donde | dónde | Interrogativo |
| cual | cuál | Interrogativo |
| quien | quién | Interrogativo |
| facil | fácil | Siempre |
| dificil | difícil | Siempre |
| electronica | electrónica | Siempre |
| electrodomesticos | electrodomésticos | En texto (no en slugs) |
| frances | francés | Siempre |
| Espana | España | Siempre |
| reparacion | reparación | Siempre |
| documentacion | documentación | Siempre |
| informacion | información | Siempre |
| puntuacion | puntuación | Siempre |
| evaluacion | evaluación | Siempre |
| metodologia | metodología | Siempre |
| garantia | garantía | Siempre |
| bateria | batería | Siempre |
| categoria | categoría | En texto (no en campos) |
| tecnico | técnico | Siempre |
| estandar | estándar | Siempre |
| movil/moviles | móvil/móviles | Siempre |
| portatil | portátil | Siempre |
| esta (verbo) | está | Verbo estar |
| sera | será | Verbo ser futuro |
| numero | número | Siempre |
| minimo | mínimo | Siempre |
| maximo | máximo | Siempre |
| publico | público | Siempre |
| basico | básico | Siempre |
| diseno | diseño | Siempre |
| tamano | tamaño | Siempre |

### Signos de interrogación y exclamación

En español, siempre usar signos de apertura:

| Incorrecto | Correcto |
|------------|----------|
| Que es esto? | ¿Qué es esto? |
| Cuantos años? | ¿Cuántos años? |
| Increible! | ¡Increíble! |

### Eñe (ñ)

| Incorrecto | Correcto |
|------------|----------|
| anos | años |
| Espana | España |
| diseno | diseño |
| tamano | tamaño |
| danado | dañado |
| ensenanza | enseñanza |

---

## Proceso de revisión

### 1. Identificar archivos a revisar

```bash
# Artículos educativos
content/aprender/*.md

# Fichas de producto
content/**/*.md

# Skills (solo texto descriptivo, NO variables)
.claude/skills/**/*.md
```

### 2. Buscar patrones problemáticos

Usar Grep para encontrar posibles errores:

```
# Palabras sin tilde comunes
grep -E "\banos\b" (pero verificar contexto - puede ser variable)
grep -E "\bindice\b"
grep -E "\bmas\b"
grep -E "\bfacil\b"
grep -E "\bEspana\b"
```

### 3. Revisar en contexto

Antes de corregir, verificar:

1. ¿Es un nombre de campo/variable? → NO cambiar
2. ¿Es un slug o ruta? → NO cambiar
3. ¿Es texto visible para el usuario? → SÍ cambiar

### 4. Aplicar correcciones

Usar Edit para corregir, verificando el contexto de cada cambio.

---

## Checklist de revisión

### Para archivos de contenido (.md en content/)

- [ ] Título (campo `title`) con acentos correctos
- [ ] Descripción (campo `description`) con acentos correctos
- [ ] keyTakeaways con acentos correctos
- [ ] Encabezados (##, ###) con acentos correctos
- [ ] Texto del cuerpo con acentos correctos
- [ ] Signos de interrogación de apertura (¿)
- [ ] Eñes donde corresponda

### Para archivos de skills (.md en .claude/skills/)

- [ ] Texto descriptivo con acentos correctos
- [ ] Ejemplos de texto con acentos correctos
- [ ] Nombres de campo/variables SIN modificar
- [ ] Código de ejemplo SIN modificar

---

## Ejemplo práctico

**Archivo original con errores:**
```yaml
---
title: "Indices de reparabilidad: guia completa"
description: "Que son los indices y como usarlos"
---

## Por que importan

Los indices miden lo facil que es reparar. En Espana...

| Campo | Valor |
|-------|-------|
| coste_10_anos | 1500 |
| duracion | "{X-Y anos}" |
```

**Archivo corregido:**
```yaml
---
title: "Índices de reparabilidad: guía completa"  # ← Corregido
description: "Qué son los índices y cómo usarlos"  # ← Corregido
---

## Por qué importan  # ← Corregido

Los índices miden lo fácil que es reparar. En España...  # ← Corregido

| Campo | Valor |
|-------|-------|
| coste_10_anos | 1500 |  # ← NO cambiar (nombre de campo)
| duracion | "{X-Y años}" |  # ← Valor corregido, campo NO
```

---

## Notas finales

- Cuando haya duda, preguntar al usuario
- Preferir revisar archivo por archivo para evitar errores masivos
- Siempre verificar el contexto antes de aplicar replace_all
- Los nombres de campo en YAML siguen convención sin acentos por compatibilidad
