# Estructura Landing Page

## Seccion 1: Hero

```
[Badge: Open Source / Beta / Nuevo]

[H1] Titulo con propuesta de valor clara
     - Maximo 8 palabras
     - Incluye beneficio principal
     - Usa palabra clave destacada

[Subtitulo]
     - 1-2 oraciones
     - Expande el H1
     - Menciona como funciona

[CTA Principal] [CTA Secundario]
     - "Probar Demo" / "Ver Video"
     - Contraste visual claro

[Visual Hero]
     - Before/After animado
     - O video corto del producto
     - O imagen del resultado final
```

### Ejemplo Handwriting OCR

```
[Badge: Open Source + 100% Offline]

OCR que aprende TU letra

Convierte tus apuntes manuscritos a texto digital.
El sistema aprende de tus correcciones y mejora con el tiempo.

[Probar Demo ->] [Ver como funciona]

[BeforeAfter: OCR raw vs Corregido]
```

## Seccion 2: El Problema

```
[Badge: El Problema]

[H2] Frase que describe el dolor

[Parrafo]
     - Situacion actual
     - Alternativas que fallan
     - Por que es frustrante

[Visuales de Problema]
     - Metricas de competencia
     - Screenshots de errores
     - Comparativa visual
```

### Ejemplo

```
[Badge: El Problema]

Los OCR genericos fallan con letra manuscrita

Google Lens, Tesseract, apps de notas... todos cometen los
mismos errores una y otra vez. "de" se convierte en "ole",
"la" en "le". Sin forma de aprender de las correcciones.

[Cards: qwen2.5vl 82% vs minicpm-v 56%]
```

## Seccion 3: La Solucion

```
[Badge: La Solucion]

[H2] Como tu producto resuelve el problema

[Parrafo]
     - Que hace diferente
     - Mecanismo clave
     - Beneficio para usuario

[Grid de Features]
     - 3 caracteristicas principales
     - Icono + Titulo + Descripcion
     - Beneficios, no funcionalidades
```

### Ejemplo

```
[Badge: La Solucion]

Sistema RAG de correcciones personalizadas

Cada vez que corriges un error, el sistema lo memoriza.
La proxima vez que encuentre el mismo patron, lo corrige
automaticamente.

[Grid]
- [Brain] Aprende de ti
  Sistema RAG que memoriza tus correcciones

- [Zap] 100% Offline
  Funciona local con Ollama, sin APIs caras

- [Shield] Privacidad Total
  Tus documentos nunca salen de tu maquina
```

## Seccion 4: Demo/Benchmark

```
[Badge: Benchmarks]

[H2] Datos que demuestran valor

[Grafico]
     - Comparativa de modelos
     - Tu solucion destacada
     - Leyenda clara

[Metricas Adicionales]
     - 3-4 KPIs importantes
     - Numeros grandes
     - Contexto comparativo
```

## Seccion 5: CTA Final

```
[H2] Llamada a la accion

[Parrafo corto]
     - Resumen del valor
     - Urgencia o beneficio

[CTA Grande]
     - Accion clara
     - Beneficio incluido

[Links Secundarios]
     - GitHub
     - Documentacion
     - Contacto
```

### Ejemplo

```
Prueba la demo ahora

Sube una imagen de tus apuntes y ve como funciona
el sistema de OCR con correcciones aprendidas.

[Ir a la Demo ->]
```

## Seccion 6: Footer

```
[Logo/Nombre] [Badge: Open Source]

[Links]
     - GitHub
     - Documentacion
     - Twitter/LinkedIn

[Tech Stack]
     - Tecnologias principales

[Copyright]
```

## Componentes Clave

### Badge

- Pequeno, colorido
- Informacion de estado
- Categoria o version

### Metricas Card

- Numero grande
- Label descriptivo
- Indicador de cambio (+/-)

### Feature Card

- Icono relevante
- Titulo corto
- Descripcion 1-2 lineas

### Before/After

- Slider interactivo
- Labels claros
- Colores contrastantes

### Benchmark Chart

- Barras horizontales
- Colores semanticos
- Tooltip con detalles

## Paleta de Colores Recomendada

```css
--success: #22c55e (verde) --warning: #eab308 (amarillo) --error: #ef4444 (rojo)
  --primary: #3b82f6 (azul) --muted: #6b7280 (gris);
```

## Responsive Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

Priorizar mobile-first design.
