# Optimizacion JS/TS (resumen accionable)

## Principios
- Reusa antes de crear: extiende modulos, hooks y servicios existentes.
- Optimiza tras medir: identifica si el cuello es render, CPU o IO.
- Reduce dependencias: evita paquetes pesados si no aportan valor claro.
- Mantiene tipos simples: tipos estrechos reducen defensiva en runtime.

## Herramientas y medicion
- Frontend: React Profiler o herramientas de Performance del navegador.
- Node: `node --prof` o `node --inspect` para analizar CPU.
- Bundle: analiza con `webpack-bundle-analyzer` o `esbuild --metafile`.

## Patrones recomendados
- Facilita tree-shaking: exports nombrados y evitar `export *` indiscriminado.
- Evitar renders innecesarios: memoizar selectivamente tras medir.
- Preferir datos normalizados y selectores memoizados.
- Evitar conversiones repetidas y work en cada render.
- Mantener dependencias y bundles pequenos.

## Checklist rapido
- Puedo extender un hook/servicio en lugar de crear uno nuevo?
- Hay renders o recomputos medidos que justifiquen memoizacion?
- El cambio aumenta el bundle o dependencias?
- Estoy duplicando logica de validacion o transformacion?
