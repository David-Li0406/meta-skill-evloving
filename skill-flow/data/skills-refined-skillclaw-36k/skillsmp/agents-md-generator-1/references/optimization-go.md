# Optimizacion Go (resumen accionable)

## Principios
- Reusa antes de crear: extiende structs, queries y handlers existentes cuando sea viable.
- Mide antes de optimizar: identifica si el coste real es CPU, IO o GC.
- Reduce complejidad: menos tipos nuevos, menos paquetes nuevos, menos dependencias.
- Mantiene compatibilidad: campos nuevos opcionales, cambios backward-friendly.

## Herramientas y medicion
- Benchmarks: `go test -bench . -benchmem`.
- Pprof: `go test -run '^$' -bench . -cpuprofile cpu.out` y analiza con `go tool pprof`.
- Escape analysis: `go build -gcflags='-m'` para evitar heap innecesario.

## Patrones recomendados
- Preferir slices y reuso de buffers en hot paths (`sync.Pool`).
- Evitar goroutines fugadas; propagar `context.Context`.
- Minimizar reflection fuera de serializacion controlada.
- Limitar allocations: evitar conversiones de `[]byte` <-> `string` en bucles.

## Checklist rapido
- Puedo extender una estructura existente en lugar de crear otra?
- El cambio agrega menos de ~50 lineas nuevas?
- Hay una consulta o servicio que ya devuelve datos relacionados?
- Estoy agregando indices o tablas nuevas sin necesidad?
