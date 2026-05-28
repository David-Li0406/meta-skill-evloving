---
name: "rust-documentation"
description: "Genera documentación Rust con rustdoc para MEMORY_P"
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["rust", "documentation", "rustdoc", "comments"]
---

# Rust Documentation Skill

## Descripción
Genera documentación Rust siguiendo convenciones de rustdoc y el estilo del proyecto.

## Cuándo Usar
- Crear nuevas funciones públicas
- Documentar módulos
- Añadir ejemplos de uso
- Actualizar CHANGELOG

## Template de Documentación

### Función Pública
```rust
/// Analiza un archivo Rust en busca de métricas y patrones.
///
/// Esta función escanea el contenido del archivo y extrae información
/// sobre funciones, imports, complejidad y más.
///
/// # Arguments
/// * `path` - Ruta al archivo .rs a analizar
///
/// # Returns
/// * `Ok(Analysis)` - Análisis completo del archivo
/// * `Err(MemoryPError)` - Si el archivo no existe o tiene formato inválido
///
/// # Examples
/// ```
/// use memory_p::analyzer::CodeAnalyzer;
/// use std::path::PathBuf;
///
/// let analyzer = CodeAnalyzer::new();
/// let path = PathBuf::from("src/main.rs");
/// let result = analyzer.analyze_file(&path)?;
///
/// assert!(result.lines > 0);
/// # Ok::<(), Box<dyn std::error::Error>>(())
/// ```
///
/// # Panics
/// Esta función no debería entrar en panic. Si el archivo no existe,
/// retorna `Err(MemoryPError::FileNotFound)`.
///
/// # Errors
/// - `MemoryPError::FileNotFound` si la ruta no existe
/// - `MemoryPError::InvalidFormat` si el archivo no es Rust válido
///
/// # Performance
/// Procesa ~10K líneas/segundo en CPU moderna. Para archivos grandes,
/// considerar usar `analyze_file_async()`.
pub fn analyze_file(path: &Path) -> Result<Analysis, MemoryPError> {
    // ...
}
```

### Módulo
```rust
//! Analyzer module - Análisis de código Rust masivo y paralelo.
//!
//! Este módulo provee herramientas para analizar código Rust a gran escala,
//! extrayendo métricas, patrones y detectando code smells.
//!
//! # Características
//! - Análisis paralelo con Rayon
//! - Detección de patrones comunes
//! - Métricas de complejidad
//! - Sugerencias de optimización
//!
//! # Examples
//! ```
//! use memory_p::analyzer::CodeAnalyzer;
//!
//! let analyzer = CodeAnalyzer::new();
//! let result = analyzer.analyze_directory("./src", "**/*.rs")?;
//!
//! println!("Archivos analizados: {}", result.total_files);
//! # Ok::<(), Box<dyn std::error::Error>>(())
//! ```

use rayon::prelude::*;
use std::path::Path;
```

### Struct
```rust
/// Configuración para el motor de análisis paralelo.
///
/// Controla el comportamiento del análisis, incluyendo número de threads,
/// profundidad de escaneo y filtros de archivos.
///
/// # Examples
/// ```
/// use memory_p::analyzer::AnalysisConfig;
///
/// let config = AnalysisConfig {
///     threads: 4,
///     max_depth: 10,
///     pattern: "**/*.rs".to_string(),
/// };
/// ```
#[derive(Debug, Clone)]
pub struct AnalysisConfig {
    /// Número de threads para paralelización (0 = auto)
    pub threads: usize,
    
    /// Profundidad máxima de directorios a escanear
    pub max_depth: usize,
    
    /// Patrón glob para filtrar archivos
    pub pattern: String,
}
```

### Enum
```rust
/// Errores que pueden ocurrir durante el análisis.
///
/// Cubre casos desde errores de I/O hasta problemas de parsing.
#[derive(Debug, thiserror::Error)]
pub enum MemoryPError {
    /// Archivo o directorio no encontrado
    #[error("File not found: {0}")]
    FileNotFound(String),
    
    /// Formato de archivo inválido
    #[error("Invalid format: {0}")]
    InvalidFormat(String),
    
    /// Error de I/O del sistema
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}
```

## Secciones Importantes

### # Arguments
Lista parámetros con su propósito
```rust
/// # Arguments
/// * `path` - Ruta al archivo
/// * `recursive` - Si debe escanear subdirectorios
```

### # Returns
Describe qué retorna la función
```rust
/// # Returns
/// * `Ok(Vec<String>)` - Lista de archivos encontrados
/// * `Err(Error)` - Si hubo problema al leer directorio
```

### # Examples
Código ejecutable que muestra uso
```rust
/// # Examples
/// ```
/// let result = my_function(42)?;
/// assert_eq!(result, 84);
/// # Ok::<(), Box<dyn std::error::Error>>(())
/// ```
```

### # Panics
Cuándo puede entrar en panic
```rust
/// # Panics
/// Entra en panic si el index está fuera de rango.
```

### # Errors
Qué errores puede retornar
```rust
/// # Errors
/// - `InvalidInput` si el path está vacío
/// - `PermissionDenied` si no tiene permisos
```

### # Safety
Para código unsafe
```rust
/// # Safety
/// El caller debe asegurar que el puntero es válido
/// y vive por al menos la duración del borrow.
```

### # Performance
Notas de rendimiento
```rust
/// # Performance
/// O(n log n) donde n es el número de elementos.
/// Usa algoritmo quicksort optimizado.
```

## Comandos

### Generar Documentación
```bash
# Generar docs
cargo doc --no-deps

# Abrir en browser
cargo doc --no-deps --open

# Con features privadas
cargo doc --document-private-items

# Limpiar y regenerar
cargo clean && cargo doc --no-deps
```

### Verificar Ejemplos
```bash
# Tests en doc comments
cargo test --doc

# Verificar links
cargo rustdoc -- -D rustdoc::broken-intra-doc-links
```

## Mejores Prácticas

### ✅ DO's
1. Documentar todas las APIs públicas
2. Incluir al menos un ejemplo funcional
3. Describir edge cases y errores
4. Usar referencias intra-doc con backticks
5. Mantener ejemplos actualizados

### ❌ DON'Ts
1. No usar comentarios `//` para APIs públicas
2. No dejar TODOs en documentación
3. No copiar-pegar sin actualizar
4. No documentar obviedades
5. No usar ejemplos que no compilan

## Links Intra-Doc
```rust
/// Ver también [`analyze_file`] para archivos individuales.
/// 
/// Para configuración, ver [`AnalysisConfig`].
///
/// Lanza [`MemoryPError::FileNotFound`] si no existe.
```

## Documentación de Módulo Root
```rust
// src/lib.rs
#![doc = include_str!("../README.md")]
#![warn(missing_docs)]
#![warn(rustdoc::broken_intra_doc_links)]
```

## Comandos
```bash
# Generar documentación
cargo doc --no-deps --open

# Con ejemplos
cargo doc --no-deps --document-private-items

# Verificar links
cargo doc --no-deps 2>&1 | grep warning
```

---

## 📚 Ver También

- [SKILLS.md](../../../SKILLS.md) - Documentación completa de Skills
- [AGENTS.md](../../../AGENTS.md) - Guía de Agents
- [Tutorial de Documentación](../../../docs/TUTORIAL_START.md) - Inicio rápido
- [Rustdoc Book](https://doc.rust-lang.org/rustdoc/) - Documentación oficial de rustdoc
- [RFC 1574](https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html) - Convenciones API docs

**Última actualización**: Enero 2026 (Post-merge PR #4)  
**Compatibilidad**: GitHub Copilot, Cursor, Windsurf, Claude Desktop
