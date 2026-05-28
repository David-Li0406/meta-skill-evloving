---
name: compile
description: Compilar Libro
allowed-tools:
  - Bash
---

# Compilar Libro LaTeX

Este skill compila un libro LaTeX del proyecto mathcode.

## Instrucciones

1. Determina qué libro compilar basándote en el contexto actual:
   - Si el usuario está trabajando en `math_fundamentals/`, compila ese libro
   - Si el usuario está trabajando en `geometry/`, compila ese libro
   - Si el usuario especifica un libro, usa ese

2. Ejecuta el script de compilación desde el directorio raíz:

```bash
cd /Users/asanchezyali/Documents/Own/mathcode && ./compile.sh <nombre_libro>
```

## Libros disponibles

- `math_fundamentals`
- `geometry`
- `deep_learning`
- `machine_learning`
- `llms`
- `inferencial_statistics`
- `src`

**Nota**: Cuando se cree un nuevo libro con `/new-book`, se debe agregar automáticamente a `compile.sh`.

## Ejemplo

Si el usuario dice "compila" y está en math_fundamentals:

```bash
cd /Users/asanchezyali/Documents/Own/mathcode && ./compile.sh math_fundamentals
```
