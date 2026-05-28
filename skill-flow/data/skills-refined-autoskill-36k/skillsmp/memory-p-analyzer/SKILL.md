---
name: "memory-p-analyzer"
description: "Analiza y optimiza código Rust de MEMORY_P"
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["rust", "analysis", "optimization", "rayon"]
---

# MEMORY_P Code Analyzer Skill

## Descripción
Analiza código Rust identificando oportunidades de optimización con Rayon y mejores prácticas.

## Cuándo Usar
- Revisar nuevo código antes de merge
- Detectar cuellos de botella
- Sugerir paralelización
- Validar uso de memoria

## Patrones a Detectar

### 1. Oportunidades de Paralelización
```rust
// ❌ DETECTAR: Loop secuencial con >100 elementos
for item in large_vec.iter() {
    process(item);
}

// ✅ SUGERIR: Usar par_iter
use rayon::prelude::*;
large_vec.par_iter().for_each(|item| process(item));
```

### 2. Clones Innecesarios
```rust
// ❌ DETECTAR: Clone sin necesidad
fn process(data: String) -> Result<(), Error> {
    // Solo lee, no modifica
}

// ✅ SUGERIR: Usar referencia
fn process(data: &str) -> Result<(), Error> {
    // ...
}
```

### 3. Allocations Evitables
```rust
// ❌ DETECTAR: Vec sin capacity
let mut results = Vec::new();
for i in 0..1000 {
    results.push(i);
}

// ✅ SUGERIR: Pre-alocar
let mut results = Vec::with_capacity(1000);
for i in 0..1000 {
    results.push(i);
}
```

## Métricas a Reportar
- Funciones sin tests
- Uso de `unwrap()` en producción
- Complejidad ciclomática >10
- Funciones >100 líneas
- Módulos sin documentación

## Script de Análisis
```bash
#!/bin/bash
# Ejecutar análisis completo
cargo clippy -- -D warnings
cargo audit
cargo outdated
```

---

## 📚 Ver También

- [SKILLS.md](../../../SKILLS.md) - Documentación completa de Skills
- [AGENTS.md](../../../AGENTS.md) - Guía de Agents
- [Agent memory-p-optimizer](../../agents/memory-p-optimizer.agent.md) - Aplica sugerencias de análisis
- [Skill rust-parallel-testing](../rust-parallel-testing/SKILL.md) - Tests para código paralelo

**Última actualización**: Enero 2026 (Post-merge PR #4)  
**Compatibilidad**: GitHub Copilot, Cursor, Windsurf, Claude Desktop
