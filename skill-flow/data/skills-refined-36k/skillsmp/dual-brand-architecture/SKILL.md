---
name: Dual-Brand Architecture
description: SocioPulse/MedicoPulse multi-brand configuration, theming, and feature flags.
---

# Dual-Brand Architecture

## Context

Lumira V2 operates two distinct brands from the same codebase:

| Brand | Domain | Sector |
|-------|--------|--------|
| **SocioPulse** | sociopulse.fr | Social & Education |
| **MedicoPulse** | medicopulse.fr | Healthcare & Medical |

---

## Core Principles

1. **Single Codebase**: One app serves both brands.
2. **Dynamic Theming**: Brand detected via subdomain/header.
3. **No Hardcoding**: All brand-specific content via configuration.

---

## Brand Configuration

### Location: `lib/brand.config.ts`

```typescript
export type BrandKey = 'sociopulse' | 'medicopulse';

export interface BrandConfig {
  key: BrandKey;
  name: string;
  tagline: string;
  domain: string;
  colors: {
    primary: string;
    accent: string;
  };
  logo: {
    icon: React.ComponentType;
    text: string;
  };
  features: {
    hasOracle: boolean;
    hasWellbeing: boolean;
  };
}

export const BRANDS: Record<BrandKey, BrandConfig> = {
  sociopulse: {
    key: 'sociopulse',
    name: 'SocioPulse',
    tagline: "L'HUMAIN AU CŒUR DU LIEN.",
    domain: 'sociopulse.fr',
    colors: { primary: 'hsl(220, 80%, 50%)', accent: 'hsl(160, 60%, 45%)' },
    logo: { icon: Heart, text: 'SocioPulse' },
    features: { hasOracle: false, hasWellbeing: true },
  },
  medicopulse: {
    key: 'medicopulse',
    name: 'MedicoPulse',
    tagline: 'VOS RENFORTS, EN UN BATTEMENT.',
    domain: 'medicopulse.fr',
    colors: { primary: 'hsl(350, 70%, 50%)', accent: 'hsl(200, 60%, 50%)' },
    logo: { icon: Cross, text: 'MedicoPulse' },
    features: { hasOracle: true, hasWellbeing: false },
  },
};
```

---

## Brand Detection

### Middleware

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || '';
  
  let brand: BrandKey = 'sociopulse'; // default
  if (hostname.includes('medicopulse')) {
    brand = 'medicopulse';
  }
  
  const response = NextResponse.next();
  response.headers.set('x-brand', brand);
  return response;
}
```

### Hook

```typescript
// hooks/useBrand.ts
export function useBrand(): BrandConfig {
  const brand = useContext(BrandContext);
  if (!brand) throw new Error('useBrand must be within BrandProvider');
  return brand;
}
```

---

## Component Usage

### Conditional Rendering

```tsx
const { key, features } = useBrand();

return (
  <>
    <Logo />
    {features.hasOracle && <OracleSection />}
    {key === 'sociopulse' && <WellbeingBanner />}
  </>
);
```

### Dynamic Styling

```tsx
const { colors } = useBrand();

<div style={{ '--primary': colors.primary } as React.CSSProperties}>
  <Button className="bg-[var(--primary)]">Action</Button>
</div>
```

---

## Cross-Registration

Users can opt to register on both platforms:

```typescript
interface CrossRegistrationDto {
  userId: string;
  targetBrand: BrandKey;
  enableCrossAccess: boolean;
}
```

---

## SEO & Metadata

```tsx
// app/layout.tsx
export async function generateMetadata() {
  const brand = getBrandFromHeaders();
  return {
    title: brand.name,
    description: brand.tagline,
    openGraph: {
      siteName: brand.name,
      images: [`/og-${brand.key}.png`],
    },
  };
}
```

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use `useBrand()` hook | Hardcode brand names |
| Check features via config | Use `if (brand === 'sociopulse')` |
| Store brand in context | Pass brand prop through many levels |
| Test both brands in E2E | Assume one brand is default |
