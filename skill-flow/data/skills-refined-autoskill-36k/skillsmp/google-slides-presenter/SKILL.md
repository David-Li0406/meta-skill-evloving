---
name: google-slides-presenter
description: Transforma entradas de blog en esquemas detallados y visuales para presentaciones de Google Slides, incluyendo estructura de diapositivas y prompts para imágenes.
---

# Google Slides Presenter (Presentador de Google Slides)

Esta habilidad te permite convertir contenido textual extenso (como entradas de blog) en presentaciones profesionales, dinámicas y visualmente atractivas.

## Cuándo usar esta habilidad
- Cuando el usuario te proporcione un enlace o texto de un blog y necesite una presentación.
- Cuando necesites estructurar ideas complejas en un formato de diapositivas.
- Cuando el usuario busque inspiración visual y estructural para una charla o webinar.

## Instrucciones para el Agente

### 1. Análisis del Contenido
- Identifica el **tema principal** y el **objetivo** de la presentación.
- Extrae de 5 a 10 **puntos clave** o secciones del blog.
- Determina el **tono** (profesional, inspiracional, educativo, etc.).

### 2. Estructura de la Presentación
Cada diapositiva debe seguir este formato:
- **Título de la Diapositiva**: Breve y directo.
- **Contenido Visual (Prompt)**: Un prompt detallado para generar una imagen impactante usando `generate_image`.
- **Puntos Clave (Bullet points)**: Máximo 3-4 puntos cortos.
- **Notas del Orador**: Un breve guion de lo que se debe decir en esa diapositiva.

### 3. Generación de Activos Visuales
Para cada diapositiva importante:
1. Usa la herramienta `generate_image` para crear una imagen representativa.
2. Describe el estilo visual (ej. "Minimalista", "Futurista", "Fotografía cinematográfica").
3. Asegúrate de que las imágenes tengan una estética coherente en toda la presentación.

### 4. Proceso de Entrega
Presenta el resultado de forma organizada:
1. **Resumen de la Presentación**: Título y descripción general.
2. **Carrusel de Diapositivas**: Usa el formato de `carousel` en markdown para mostrar los diseños de las diapositivas con sus imágenes generadas.
3. **Guía de Implementación**: Instrucciones para que el usuario pueda copiar y pegar el contenido en Google Slides.

## Ejemplo de Prompt para Imagen
`"Una ilustración conceptual de estilo glassmorphism que represente la conectividad global y la inteligencia artificial, paleta de colores azul y violeta vibrante, alta resolución."`

## Flujo de Trabajo
1. Leer el blog.
2. Definir el esquema de 7-10 diapositivas.
3. Generar imágenes para las diapositivas clave.
4. Mostrar el resultado final al usuario.
