---
name: x-scraper
description: Rastrear y extraer las 5 mejores publicaciones (por relevancia o interacción) de cualquier perfil de X (antiguo Twitter) utilizando el subagente del navegador.
---

# X Scraper (Rastreador de X)

Esta habilidad te permite obtener información actualizada de perfiles públicos de X sin necesidad de una API, utilizando la navegación del subagente.

## Cuándo usar esta habilidad
- Cuando el usuario te pida ver qué está publicando alguien en X.
- Cuando necesites analizar las 5 mejores publicaciones de un perfil específico.
- Cuando busques tendencias o noticias recientes de una cuenta concreta.

## Instrucciones para el Agente

### 1. Preparación de la Búsqueda
- Identifica si el usuario quiere un **perfil específico** o una **temática/palabra clave**.
- **Si es un Perfil**: La URL es `https://x.com/[usuario]`.
- **Si es una Temática**: La URL es `https://x.com/search?q=[palabra_clave]&src=typed_query`.

### 2. Extracción con Browser Subagent
Usa el `browser_subagent` con las siguientes instrucciones:
- Navegar a la URL correspondiente.
- **Para temáticas**: Si es posible, haz clic en la pestaña "Destacados" (Top) para obtener los mejores resultados.
- Esperar a que el feed cargue.
- Localizar los primeros 5 elementos de tipo `article`.
- **Extraer**:
  - Texto del post.
  - Nombre del autor.
  - Métricas (Likes, Reposts) para identificar los "mejores".

### 3. Criterios de Selección
- Selecciona los 5 posts con mayor interacción visual o los 5 más recientes si es una búsqueda de noticias.

### 4. Formato de Salida
Presenta los resultados organizados:
- **Búsqueda**: [Temática o Perfil]
- **Top 5 Publicaciones**: [Lista detallada]

## Mejores Prácticas
- **Codificación**: Asegúrate de que los espacios en la temática se conviertan en `%20` en la URL de búsqueda.
- **Scroll**: Realiza un scroll suave si el contenido inicial no es suficiente.

## Ejemplo de Instrucción al Subagente
`"Busca la temática 'Inteligencia Artificial' en X (search?q=Inteligencia%20Artificial) y extrae los 5 posts más destacados con sus respectivos autores y likes."`
