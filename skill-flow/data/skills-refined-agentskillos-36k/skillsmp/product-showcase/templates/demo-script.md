# Guion Demo / GIF

## Estructura General

```
Duracion Total: 15-30 segundos (GIF) / 60-90 segundos (video)

1. [3s] Contexto inicial
2. [5s] Mostrar el problema
3. [10s] Demostrar la solucion
4. [5s] Resultado final
5. [2s] Call to action
```

## GIF Before/After (15s)

### Timeline

```
0-3s:  Mostrar imagen original manuscrita
3-6s:  Texto OCR con errores (resaltados en rojo)
6-9s:  Correccion del usuario (typing)
9-12s: Sistema aprende (animacion)
12-15s: Resultado final limpio (verde)
```

### Puntos Clave a Mostrar

1. **Imagen clara** de apuntes reales
2. **Errores visibles** en el OCR inicial
3. **Proceso de correccion** simplificado
4. **Confirmacion visual** de aprendizaje

### Texto en Pantalla

```
Frame 1: "Tu letra manuscrita"
Frame 2: "OCR tradicional: 56% accuracy"
Frame 3: "Corrige una vez..."
Frame 4: "El sistema aprende"
Frame 5: "95%+ accuracy"
```

## Video Demo Completo (90s)

### Intro (0-10s)

```
[Pantalla]
Logo + "Handwriting OCR"
"OCR que aprende TU letra"

[Voz/Texto]
"Voy a mostrarte como convertir tus apuntes
manuscritos a texto digital de forma inteligente."
```

### El Problema (10-25s)

```
[Pantalla]
Subir imagen de apuntes reales
Mostrar resultado OCR con errores

[Voz/Texto]
"Mira estos apuntes. Cuando uso un OCR normal,
obtengo esto... lleno de errores."

[Highlight]
Resaltar 2-3 errores tipicos
"de" -> "ole", "la" -> "le"
```

### La Solucion (25-50s)

```
[Pantalla]
Editor de texto con correccion
Animacion de guardado

[Voz/Texto]
"Pero con este sistema, simplemente corrijo el error
una vez... y el sistema lo aprende."

[Mostrar]
- Editar texto
- Click en "Guardar"
- Animacion de confirmacion
```

### Demostrar Aprendizaje (50-70s)

```
[Pantalla]
Nueva imagen con mismo patron
Resultado automaticamente correcto

[Voz/Texto]
"La proxima vez que encuentre el mismo patron,
lo corrige automaticamente. Mira..."

[Mostrar]
- Nueva imagen
- OCR correcto desde el inicio
- Badge de "Correccion aplicada"
```

### Metricas y Cierre (70-90s)

```
[Pantalla]
Grafico de benchmark
Numeros de accuracy

[Voz/Texto]
"De 56% a mas del 95% de accuracy.
Funciona 100% offline con tu propia GPU."

[CTA]
"Pruebalo gratis en [link]"
```

## Tips de Grabacion

### Para GIF

1. **Resolucion**: 800x600 o 1200x800
2. **FPS**: 10-15 para menor tamano
3. **Colores**: Reducir paleta a 128-256
4. **Duracion**: Max 20 segundos
5. **Loop**: Debe funcionar en loop

### Para Video

1. **Resolucion**: 1080p minimo
2. **Audio**: Opcional pero recomendado
3. **Subtitulos**: Siempre incluir
4. **Intro/Outro**: Mantener breve
5. **Thumbnail**: Frame mas impactante

### Herramientas Recomendadas

**Grabacion**

- OBS Studio (gratis)
- Loom (facil de usar)
- ScreenFlow (Mac)

**Edicion GIF**

- Gifski (alta calidad)
- ScreenToGif (Windows)
- FFmpeg (CLI)

**Edicion Video**

- DaVinci Resolve (gratis)
- iMovie (Mac)
- Kdenlive (Linux)

## Checklist Pre-Grabacion

- [ ] Pantalla limpia (sin notificaciones)
- [ ] Datos de ejemplo preparados
- [ ] Navegador en modo incognito
- [ ] Resolucion correcta configurada
- [ ] Dark mode consistente (si aplica)
- [ ] Cursor visible pero no distractor
- [ ] Script ensayado 1-2 veces

## Checklist Post-Produccion

- [ ] Recortar inicio/fin innecesarios
- [ ] Agregar texto explicativo
- [ ] Optimizar tamano archivo
- [ ] Probar en mobile
- [ ] Verificar calidad de compresion
- [ ] Crear thumbnail si es video

## Ejemplo de Comandos FFmpeg

### Grabar pantalla a GIF

```bash
# Grabar region de pantalla
ffmpeg -f x11grab -s 800x600 -i :0.0+100,200 -t 15 output.mp4

# Convertir a GIF de alta calidad
ffmpeg -i output.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" \
  -c:v gif output.gif
```

### Optimizar GIF

```bash
# Con gifsicle
gifsicle -O3 --colors 256 input.gif -o output.gif

# Con gifski (mejor calidad)
gifski --fps 10 --quality 80 -o output.gif input.mp4
```

### Crear video con subtitulos

```bash
# Agregar subtitulos embebidos
ffmpeg -i input.mp4 -vf subtitles=subs.srt output.mp4
```
