---
name: Component Patterns
description: ProSektorWeb UI bileşen kalıpları ve stil rehberi
---

# Component Patterns Skill

## Renk Paleti
```css
--brand-50: #fef2f2;
--brand-100: #fee2e2;
--brand-500: #ef4444;
--brand-600: #dc2626;
--brand-700: #b91c1c;
```

## Tipik Kart Yapısı
```tsx
<div className="bg-white rounded-2xl border border-neutral-200 p-6 shadow-sm hover:shadow-lg transition-all">
  {/* İçerik */}
</div>
```

## Glassmorphism Kart
```tsx
<div className="backdrop-blur-xl bg-white/10 rounded-3xl border border-white/10 shadow-2xl">
  {/* Koyu arka plan üzerinde kullan */}
</div>
```

## Gradient Buton
```tsx
<button className="px-6 py-3 bg-gradient-to-r from-brand-600 to-brand-500 text-white rounded-xl font-bold shadow-lg shadow-brand-600/30 hover:shadow-brand-600/50 transition-all">
  Buton
</button>
```

## Animasyonlu Wave (Footer için)
- 3 katman: slow (8s), medium (6s), fast (4s)
- CSS keyframes ile d attribute animasyonu

## Form Input
```tsx
<div className="relative">
  <Icon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
  <input className="w-full pl-12 pr-4 py-3.5 bg-neutral-50 border border-neutral-200 rounded-xl focus:border-brand-500 focus:ring-2 focus:ring-brand-100 outline-none transition-all" />
</div>
```

## Particles Arka Plan
```tsx
import Particles from '@/components/ui/Particles'

<Particles
  particleColors={['#dc2626', '#ef4444', '#ffffff']}
  particleCount={150}
  speed={0.08}
/>
```
