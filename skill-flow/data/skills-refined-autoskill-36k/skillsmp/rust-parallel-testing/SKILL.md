---
name: "rust-parallel-testing"
description: "Genera tests unitarios con rayon para MEMORY_P"
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["rust", "testing", "rayon", "parallel", "mcp"]
---

# Rust Parallel Testing Skill

## Descripción
Genera tests unitarios y de integración optimizados para el proyecto MEMORY_P, con énfasis en paralelismo con Rayon.

## Cuándo Usar
- Crear tests para nuevos módulos
- Validar procesamiento paralelo
- Probar handlers MCP
- Verificar correctitud de optimizaciones

## Template: Tests Paralelos
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use rayon::prelude::*;
    
    #[test]
    fn test_parallel_processing() {
        let data: Vec<u32> = (0..10000).collect();
        
        let results: Vec<_> = data
            .par_iter()
            .map(|x| process(*x))
            .collect();
        
        assert_eq!(results.len(), 10000);
        assert!(results.iter().all(|r| r.is_ok()));
    }
    
    #[tokio::test]
    async fn test_async_handler() {
        let result = async_operation().await;
        assert!(result.is_ok());
    }
}
```

## Comandos
```bash
cargo test --release
cargo test -- --nocapture
cargo test --test-threads=4
```

---

## 📚 Ver También

- [SKILLS.md](../../../SKILLS.md) - Documentación completa de Skills
- [AGENTS.md](../../../AGENTS.md) - Guía de Agents
- [Agent memory-p-refactor](../../agents/memory-p-refactor.agent.md) - Tests para validar refactors
- [Skill memory-p-analyzer](../memory-p-analyzer/SKILL.md) - Análisis pre-testing

**Última actualización**: Enero 2026 (Post-merge PR #4)  
**Compatibilidad**: GitHub Copilot, Cursor, Windsurf, Claude Desktop
