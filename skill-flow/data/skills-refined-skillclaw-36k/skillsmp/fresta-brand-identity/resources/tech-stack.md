# Tech Stack & Implementation Rules

Regras técnicas **obrigatórias** para implementação do Fresta. Não desvie desta stack.

## 🏗️ Core Stack

| Categoria | Tecnologia | Justificativa |
|-----------|------------|---------------|
| **Framework** | React 18+ (TypeScript) | Type-safety e componentização |
| **Styling** | Tailwind CSS 3.4+ | Utility-first, customizável |
| **Component Library** | shadcn/ui | Componentes acessíveis e customizáveis |
| **Icons** | Lucide React | 1000+ ícones consistentes, tree-shakeable |
| **Animations** | Framer Motion | Animações declarativas e performáticas |
| **Forms** | React Hook Form + Zod | Validação type-safe |
| **Estado** | React Context + TanStack Query | Estado local + cache de servidor |
| **Backend** | Supabase | Auth, DB, Storage, Realtime |

## 📦 Dependências Obrigatórias

```bash
npm install tailwindcss @tailwindcss/typography
npm install lucide-react
npm install framer-motion
npm install react-hook-form zod @hookform/resolvers
npm install @tanstack/react-query
npm install clsx tailwind-merge
npm install @supabase/supabase-js
```

## ⚙️ Configuração Tailwind (tailwind.config.js)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          deep: '#1B4D3E',
          DEFAULT: '#2D7A5F',
          light: '#5DBF94',
          lighter: '#A8E6CF',
          foreground: '#FFFFFF',
        },
        accent: {
          warm: '#F9A03F',
          bright: '#FFD166',
          cool: '#4ECDC4',
          sunrise: '#FF6B6B',
        },
        neutral: {
          bg: '#F8F9F5',
          card: '#FFFFFF',
          text: '#1A3E3A',
          'text-secondary': '#5A7470',
          'text-muted': '#9CA3AF',
        },
        card: {
          beige: '#FFF8E8',
          turquoise: '#D4F4F0',
          green: '#E8F5E0',
          pink: '#FFE5EC',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        sm: '8px',
        DEFAULT: '12px',
        md: '16px',
        lg: '20px',
        xl: '24px',
        '2xl': '32px',
        '3xl': '40px',
      },
      boxShadow: {
        sm: '0 2px 8px rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 4px 16px rgba(0, 0, 0, 0.08)',
        md: '0 8px 24px rgba(0, 0, 0, 0.10)',
        lg: '0 16px 48px rgba(0, 0, 0, 0.12)',
        glow: '0 0 20px rgba(255, 209, 102, 0.4)',
        'glow-green': '0 0 20px rgba(45, 122, 95, 0.4)',
        'colored-warm': '0 8px 32px rgba(249, 160, 63, 0.3)',
        'colored-cool': '0 8px 32px rgba(78, 205, 196, 0.3)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'glow-pulse': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(255, 209, 102, 0.4)' },
          '50%': { boxShadow: '0 0 40px rgba(255, 209, 102, 0.6)' },
        },
      },
    },
  },
  plugins: [],
};
```

## 🧩 Padrões de Implementação

### 1. Padrão de Botões

```typescript
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'accent';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

export const Button = ({ variant = 'primary', size = 'md', children, onClick, className }: ButtonProps) => {
  const baseStyles = 'inline-flex items-center justify-center gap-2 font-semibold transition-all rounded-xl';
  
  const variants = {
    primary: 'bg-primary text-white hover:bg-primary-light hover:shadow-glow-green hover:-translate-y-0.5',
    secondary: 'bg-white text-primary border-2 border-primary hover:bg-primary/10',
    ghost: 'bg-transparent text-primary hover:bg-primary/10',
    accent: 'bg-accent-warm text-white hover:bg-accent-bright hover:shadow-colored-warm hover:-translate-y-0.5',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };
  
  return (
    <button 
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### 2. Padrão de Cards (Estilo Solidroad)

```typescript
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface FeatureCardProps {
  title: string;
  description: string;
  bgColor: 'beige' | 'turquoise' | 'green' | 'pink';
  icon?: React.ReactNode;
  illustration?: React.ReactNode;
}

export const FeatureCard = ({ title, description, bgColor, icon, illustration }: FeatureCardProps) => {
  const bgColors = {
    beige: 'bg-card-beige',
    turquoise: 'bg-card-turquoise',
    green: 'bg-card-green',
    pink: 'bg-card-pink'
  };
  
  return (
    <motion.div
      className={cn(
        'relative rounded-3xl p-8 min-h-[420px] border border-neutral-bg/50 overflow-hidden group',
        'hover:-translate-y-2 hover:shadow-lg transition-all duration-300',
        bgColors[bgColor]
      )}
      whileHover={{ scale: 1.02 }}
    >
      {/* Ilustração de fundo */}
      {illustration && (
        <div className="absolute inset-0 opacity-5 group-hover:opacity-10 transition-opacity">
          {illustration}
        </div>
      )}
      
      {/* Conteúdo */}
      <div className="relative z-10">
        {icon && (
          <div className="w-14 h-14 rounded-2xl bg-white/50 backdrop-blur-sm flex items-center justify-center mb-6 shadow-sm">
            {icon}
          </div>
        )}
        
        <h3 className="text-2xl font-bold text-neutral-text mb-3">
          {title}
        </h3>
        
        <p className="text-neutral-text-secondary leading-relaxed">
          {description}
        </p>
      </div>
      
      {/* Borda superior animada */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-accent-warm to-accent-cool transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-500" />
    </motion.div>
  );
};
```

### 3. Padrão de Hero Section

```typescript
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

export const HeroSection = () => {
  return (
    <section className="relative min-h-[700px] overflow-hidden rounded-3xl bg-gradient-to-br from-primary-deep to-primary">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-10">
        <svg className="w-full h-full" viewBox="0 0 1440 800">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <circle cx="20" cy="20" r="1" fill="white" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>
      
      {/* Floating elements */}
      <div className="absolute top-20 right-20 w-64 h-64 bg-accent-warm/20 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-20 left-20 w-48 h-48 bg-accent-cool/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
      
      {/* Content */}
      <div className="relative z-10 container mx-auto px-6 py-24 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 mb-8">
            <span className="w-2 h-2 rounded-full bg-accent-bright animate-pulse" />
            <span className="text-white/80 text-sm font-medium">Novo: Calendários compartilhados</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 leading-tight tracking-tight">
            Organize sua vida,
            <br />
            <span className="text-accent-bright">um evento por vez</span>
          </h1>
          
          <p className="text-xl text-white/70 mb-10 max-w-2xl mx-auto leading-relaxed">
            Calendários inteligentes que se adaptam à sua rotina. 
            Compartilhe momentos especiais com quem você ama.
          </p>
          
          {/* CTA Group */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-4 bg-accent-warm text-white rounded-2xl font-bold text-lg hover:bg-accent-bright hover:shadow-colored-warm hover:-translate-y-1 transition-all duration-300 flex items-center gap-2">
              Começar grátis
              <ArrowRight className="w-5 h-5" />
            </button>
            <button className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white rounded-2xl font-bold text-lg border border-white/20 hover:bg-white/20 transition-all duration-300">
              Ver demonstração
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
```

### 4. Padrão de Animações

```typescript
import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

// Animação ao entrar na viewport
export const AnimatedSection = ({ children }: { children: React.ReactNode }) => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });
  
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
};

// Stagger animation para listas
export const staggerContainer = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

export const staggerItem = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

// Glow button com hover effect
export const GlowButton = ({ children }: { children: React.ReactNode }) => (
  <motion.button
    className="relative px-8 py-4 bg-accent-warm text-white rounded-2xl font-bold overflow-hidden"
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
  >
    <motion.div
      className="absolute inset-0 bg-accent-bright rounded-2xl blur-xl"
      initial={{ opacity: 0 }}
      whileHover={{ opacity: 0.5 }}
      transition={{ duration: 0.3 }}
    />
    <span className="relative z-10">{children}</span>
  </motion.button>
);
```

### 5. Utility Function Obrigatória

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## 🚫 Padrões Proibidos

```typescript
// ❌ NÃO USE:

// jQuery
$('.button').click();

// Bootstrap classes
<button className="btn btn-primary">Click</button>

// Styled-components (exceto casos específicos)
const StyledButton = styled.button``;

// Inline styles (exceto valores dinâmicos)
<div style={{ color: 'red' }}>Text</div>

// CSS genérico azul corporativo
<div className="bg-blue-500">...</div>
```

## ✅ USE SEMPRE:

```typescript
// ✅ Tailwind utilities com cores da marca
<button className="bg-primary hover:bg-primary-light transition-colors">
  Click
</button>

// ✅ Componentes tipados
interface Props {
  variant: 'primary' | 'secondary';
}

// ✅ Framer Motion para animações
<motion.div animate={{ y: -5 }} />

// ✅ Cores do design system
<div className="bg-accent-warm text-white">...</div>
```

## 📱 Responsividade

```typescript
// ✅ Mobile-first com Tailwind breakpoints
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Cards */}
</div>

// Tipografia responsiva com clamp
<h1 className="text-[clamp(2rem,5vw,4rem)] font-bold">
  Título Responsivo
</h1>

// Padding/margin responsivos
<section className="py-16 md:py-24 lg:py-32">
  {/* Content */}
</section>

// Container consistente
<div className="container mx-auto px-4 md:px-6 lg:px-8">
  {/* Content */}
</div>
```

## 🎯 Performance

```typescript
// ✅ Lazy loading de componentes pesados
const HeavyChart = lazy(() => import('./components/HeavyChart'));

// ✅ Memoização quando necessário
const ExpensiveComponent = memo(({ data }) => {
  // Render pesado
});

// ✅ Imagens otimizadas
<img 
  src={image} 
  alt="Description"
  loading="lazy"
  className="object-cover"
/>

// ✅ Prefetch de rotas críticas
import { Link } from 'react-router-dom';
<Link to="/dashboard" prefetch="intent">Dashboard</Link>
```
