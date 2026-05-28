---
name: web-artifacts-builder
description: 'Build high-quality React + Tailwind + shadcn/ui web artifacts. Tạo interactive components, dashboards, landing pages với production-ready code.'
---

# Web Artifacts Builder Skill

Skill này provide guidelines và patterns cho building high-quality web artifacts using modern stack: React + Tailwind CSS + shadcn/ui.

## Khi Nào Sử Dụng

- Tạo interactive web components
- Build dashboards và admin panels
- Create landing pages
- Prototype UI concepts nhanh
- Build standalone web tools
- Create data visualization components

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | React 18+ |
| Styling | Tailwind CSS v3+ |
| Components | shadcn/ui |
| Icons | Lucide React |
| Charts | Recharts |
| Animation | Framer Motion |

---

## Component Patterns

### Basic Component Structure
```tsx
import { cn } from "@/lib/utils";

interface ComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export function Component({ className, children }: ComponentProps) {
  return (
    <div className={cn("base-classes", className)}>
      {children}
    </div>
  );
}
```

### With State
```tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";

export function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div className="flex items-center gap-4">
      <Button 
        variant="outline" 
        onClick={() => setCount(c => c - 1)}
      >
        -
      </Button>
      <span className="text-2xl font-bold">{count}</span>
      <Button onClick={() => setCount(c => c + 1)}>
        +
      </Button>
    </div>
  );
}
```

### Card Pattern
```tsx
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function FeatureCard({ title, description, icon: Icon }) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <Icon className="h-8 w-8 mb-2 text-primary" />
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Content */}
      </CardContent>
      <CardFooter>
        {/* Actions */}
      </CardFooter>
    </Card>
  );
}
```

---

## Layout Patterns

### Page Layout
```tsx
export function PageLayout({ children }) {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          {/* Nav */}
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="border-t mt-auto">
        <div className="container mx-auto px-4 py-4">
          {/* Footer */}
        </div>
      </footer>
    </div>
  );
}
```

### Grid Layouts
```tsx
// 3-column responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// Sidebar layout
<div className="flex">
  <aside className="w-64 border-r h-screen sticky top-0">
    {/* Sidebar */}
  </aside>
  <main className="flex-1 p-6">
    {/* Content */}
  </main>
</div>

// Dashboard grid
<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
  <StatCard />
  <StatCard />
  <StatCard />
  <StatCard />
</div>
```

---

## Common Components

### Stat Card
```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUpIcon, ArrowDownIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon?: React.ComponentType<{ className?: string }>;
}

export function StatCard({ title, value, change, icon: Icon }: StatCardProps) {
  const isPositive = change && change > 0;
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change !== undefined && (
          <p className={cn(
            "text-xs flex items-center",
            isPositive ? "text-green-600" : "text-red-600"
          )}>
            {isPositive ? <ArrowUpIcon className="h-3 w-3" /> : <ArrowDownIcon className="h-3 w-3" />}
            {Math.abs(change)}%
          </p>
        )}
      </CardContent>
    </Card>
  );
}
```

### Data Table
```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export function DataTable({ columns, data }) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            {columns.map(col => (
              <TableHead key={col.key}>{col.label}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((row, i) => (
            <TableRow key={i}>
              {columns.map(col => (
                <TableCell key={col.key}>{row[col.key]}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

### Form Pattern
```tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function ContactForm() {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Submit logic
    setIsLoading(false);
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input 
          id="email" 
          type="email" 
          placeholder="you@example.com"
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="message">Message</Label>
        <Textarea 
          id="message"
          placeholder="Your message..."
          required
        />
      </div>
      <Button type="submit" disabled={isLoading}>
        {isLoading ? "Sending..." : "Send Message"}
      </Button>
    </form>
  );
}
```

---

## Charts with Recharts

### Line Chart
```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function SimpleLineChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke="hsl(var(--primary))"
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Bar Chart
```tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function SimpleBarChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

---

## Animation with Framer Motion

### Fade In
```tsx
import { motion } from "framer-motion";

export function FadeIn({ children, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
    >
      {children}
    </motion.div>
  );
}
```

### Stagger Children
```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export function StaggerList({ items }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      {items.map(i => (
        <motion.li key={i.id} variants={item}>
          {i.content}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

---

## Tailwind Tips

### Responsive Prefixes
```
sm:  → 640px
md:  → 768px
lg:  → 1024px
xl:  → 1280px
2xl: → 1536px
```

### Common Patterns
```tsx
// Center everything
className="flex items-center justify-center"

// Full-bleed with max-width
className="w-full max-w-4xl mx-auto px-4"

// Aspect ratio
className="aspect-video" // 16:9
className="aspect-square" // 1:1

// Truncate text
className="truncate" // single line
className="line-clamp-2" // 2 lines

// Glass effect
className="bg-white/80 backdrop-blur-sm"

// Smooth scroll
className="scroll-smooth"
```

---

## Artifact Quality Checklist

- [ ] Responsive design (mobile-first)
- [ ] Dark mode support (`dark:` variants)
- [ ] Loading states
- [ ] Error handling
- [ ] Accessibility (proper labels, focus states)
- [ ] Consistent spacing (4px grid)
- [ ] Meaningful animations (không excessive)
- [ ] Clean code structure
- [ ] TypeScript types
- [ ] Comments for complex logic
