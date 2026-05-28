# Guia de Frameworks para Showcase

## Matriz de Decision

| Necesidad          | Framework          | Complejidad | Deploy          |
| ------------------ | ------------------ | ----------- | --------------- |
| Landing rapida     | Tailwind + HTML    | Baja        | Cualquier       |
| Demo con API       | Next.js 14         | Media       | Vercel          |
| Dashboard datos    | Next.js + Recharts | Media       | Vercel          |
| App ML interactiva | Streamlit          | Baja        | Streamlit Cloud |
| Demo GPU/ML        | Gradio             | Baja        | HuggingFace     |
| Blog + Landing     | Astro              | Baja        | Netlify         |
| Prototipo rapido   | Remix              | Media       | Fly.io          |

## Next.js 14 (Recomendado para este proyecto)

### Cuando Usar

- Necesitas SSR para SEO
- API routes para backend ligero
- Deploy facil en Vercel
- Integracion con React ecosystem

### Setup Basico

```bash
npx create-next-app@latest showcase --typescript --tailwind --app
cd showcase
npm install framer-motion recharts lucide-react
```

### Estructura Recomendada

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── demo/page.tsx
│   └── api/
├── components/
│   ├── ui/
│   └── [feature]/
└── lib/
```

### Pros

- Server Components
- API Routes integradas
- Image optimization
- Incremental Static Regeneration

### Cons

- Curva de aprendizaje App Router
- Build time puede ser lento
- Vendor lock-in con Vercel

## Tailwind + shadcn/ui

### Cuando Usar

- UI profesional rapida
- Componentes accesibles
- Personalizacion necesaria
- No quieres reinventar la rueda

### Setup

```bash
npx shadcn@latest init
npx shadcn@latest add button card badge
```

### Componentes Utiles para Showcase

- Button (CTAs)
- Card (Features, Metricas)
- Badge (Labels, Status)
- Tabs (Navegacion)
- Dialog (Modales)
- Tooltip (Ayuda contextual)

## Recharts para Graficos

### Cuando Usar

- Benchmarks comparativos
- Metricas de rendimiento
- Graficos de progreso
- Data viz simple

### Tipos de Graficos Utiles

```typescript
// Barras para comparar modelos
<BarChart data={benchmarkData}>
  <Bar dataKey="accuracy" fill="#22c55e" />
</BarChart>

// Lineas para progreso temporal
<LineChart data={progressData}>
  <Line type="monotone" dataKey="accuracy" />
</LineChart>

// Area para rangos
<AreaChart data={rangeData}>
  <Area dataKey="improvement" />
</AreaChart>
```

## Framer Motion para Animaciones

### Animaciones Esenciales

```typescript
// Fade in al cargar
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
>

// Stagger para listas
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

// Hover effects
<motion.button whileHover={{ scale: 1.05 }}>
```

### Animaciones para Showcase

1. Hero text entrance
2. Feature cards stagger
3. Metric counter animation
4. Before/after slider
5. Success confirmation

## Streamlit (Alternativa para ML)

### Cuando Usar

- Demo ML rapida
- No necesitas UI custom
- Prototipo interno
- Data science focus

### Setup

```bash
pip install streamlit
streamlit run app.py
```

### Ejemplo Basico

```python
import streamlit as st

st.title("Handwriting OCR Demo")

uploaded = st.file_uploader("Sube imagen")
if uploaded:
    result = process_ocr(uploaded)
    st.text_area("Resultado", result)
```

## Gradio (ML + HuggingFace)

### Cuando Usar

- Modelo ML en HuggingFace
- Demo publica rapida
- Interfaz generica suficiente

### Setup

```python
import gradio as gr

demo = gr.Interface(
    fn=ocr_function,
    inputs=gr.Image(type="filepath"),
    outputs="text"
)
demo.launch()
```

## Deploy Options

### Vercel (Next.js)

- Free tier generoso
- Deploy automatico desde Git
- Edge Functions
- Analytics incluidos

### Netlify (Estatico/Astro)

- Free tier bueno
- Forms integrados
- Split testing
- Identity management

### Streamlit Cloud

- Free para proyectos publicos
- Deploy desde GitHub
- Sin configuracion

### HuggingFace Spaces

- Free para Gradio/Streamlit
- GPU disponible (limitado)
- Comunidad ML

## Checklist de Seleccion

Responde estas preguntas:

1. **Necesito backend?**
   - Si -> Next.js o FastAPI
   - No -> Astro o HTML estatico

2. **Es una demo ML?**
   - Si, rapida -> Streamlit/Gradio
   - Si, custom -> Next.js + API Python

3. **SEO importante?**
   - Si -> Next.js SSR o Astro
   - No -> SPA esta bien

4. **Necesito graficos?**
   - Simples -> Recharts
   - Complejos -> D3.js
   - Datos -> Observable

5. **Cuanto tiempo tengo?**
   - Horas -> Streamlit/Gradio
   - Dias -> Next.js + Tailwind
   - Semanas -> Custom completo
