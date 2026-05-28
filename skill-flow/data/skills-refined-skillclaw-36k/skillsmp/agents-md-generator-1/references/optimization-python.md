# Optimizacion Python (resumen accionable)

## Principios
- Reusa antes de crear: extiende funciones y modulos existentes.
- Optimiza tras medir: identifica CPU vs IO vs latencia externa.
- Minimiza complejidad: menos archivos nuevos y menos dependencias.
- Mantiene legibilidad: micro-opt solo con evidencia.

## Herramientas y medicion
- CPU: `python -m cProfile -o prof.out script.py` y analiza con `pstats`.
- Muestreo: `py-spy top` o `py-spy record` si esta disponible.
- Linea a linea: `line_profiler` en funciones criticas.

## Patrones recomendados
- Preferir builtins (sum, min, max, any, all) y comprensiones.
- Usar `dict`/`set` para membership O(1).
- Evitar trabajo repetido: caching con `functools.lru_cache`.
- En IO, usar streaming y generadores para evitar cargar todo en memoria.
- Si hay numeric-heavy, considerar vectorizacion (numpy/pandas) en vez de bucles Python.

## Checklist rapido
- Puedo ampliar una funcion existente en lugar de crear otra?
- El cambio reduce el numero de llamadas o loops?
- Estoy evitando trabajo repetido con cache o precomputo?
- Hay un cuello de botella medido que justifique el cambio?
