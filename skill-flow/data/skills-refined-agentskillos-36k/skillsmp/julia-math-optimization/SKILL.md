---
name: "julia-math-optimization"
description: "Optimización matemática con Julia + Optim.jl y análisis de caos"
version: "2.0.0"
tags: ["julia", "optimization", "chaos", "ffi"]
---

# Julia Mathematical Optimization Skill

Aplica optimización matemática avanzada y análisis de caos usando Julia para MEMORY_P.

## Cuándo Usar
- Optimizar pesos de búsqueda híbrida
- Detectar comportamiento caótico en métricas
- Resolver ecuaciones diferenciales
- Análisis numérico complejo

## Ejemplo
```julia
using Optim
result = optimize(search_quality, [0.33, 0.33, 0.34], NelderMead())
optimal = Optim.minimizer(result)
```

## Integración FFI
```rust
let optimal = julia::optimize_weights(&[0.33, 0.33, 0.34])?;
```

Documentación completa: FFI/src/julia_math.jl
