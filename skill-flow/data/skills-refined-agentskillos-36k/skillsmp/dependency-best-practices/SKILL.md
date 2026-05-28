---
name: dependency-best-practices
description: Approved libraries, bundle optimization, and security best practices for dependencies. Use when adding new packages, optimizing bundle size, or ensuring secure dependency management.
---

# Dependency Best Practices

Guidelines for selecting, installing, and managing dependencies in the Y-Not Radio site. Focus on security, performance, and maintainability.

## Preferred Dependencies

### State Management

**Use:** React Context or Zustand
**Avoid:** Redux (too much boilerplate for our needs)

```typescript
// ✅ Good: React Context for simple state
export const ArtistContext = createContext<ArtistContextType>(null);

export const ArtistProvider: React.FC = ({ children }) => {
  const [selectedArtist, setSelectedArtist] = useState<Artist | null>(null);
  
  return (
    <ArtistContext.Provider value={{ selectedArtist, setSelectedArtist }}>
      {children}
    </ArtistContext.Provider>
  );
};

// ✅ Good: Zustand for more complex state
import { create } from 'zustand';

interface ArtistStore {
  artists: Artist[];
  addArtist: (artist: Artist) => void;
}

export const useArtistStore = create<ArtistStore>((set) => ({
  artists: [],
  addArtist: (artist) => set((state) => ({ 
    artists: [...state.artists, artist] 
  })),
}));

// ❌ Avoid: Redux for simple use cases
// Too much boilerplate: actions, reducers, store setup, etc.
```

### Date Handling

**Use:** `date-fns` (already installed)
**Avoid:** `moment.js` (large bundle size, deprecated)

```typescript
// ✅ Good: date-fns (tree-shakeable)
import { format, parseISO, addDays } from 'date-fns';

const formatted = format(new Date(), 'yyyy-MM-dd');
const parsed = parseISO('2024-01-15');
const future = addDays(new Date(), 7);

// ❌ Bad: moment.js (large bundle, imports everything)
import moment from 'moment';
const formatted = moment().format('YYYY-MM-DD');
```

### Utility Functions

**Use:** `lodash-es` (ES modules for tree-shaking)
**Avoid:** `lodash` (CommonJS, no tree-shaking)

```typescript
// ✅ Good: Import specific functions from lodash-es
import debounce from 'lodash-es/debounce';
import groupBy from 'lodash-es/groupBy';

const debouncedSearch = debounce(searchArtists, 300);
const artistsByGenre = groupBy(artists, 'genre');

// ❌ Bad: Import entire lodash library
import _ from 'lodash';
const debouncedSearch = _.debounce(searchArtists, 300);
```

### Styling

**Use:** Payload CMS built-in components, utility-first CSS
**Avoid:** Heavy CSS-in-JS libraries (styled-components, emotion)

```typescript
// ✅ Good: Payload UI components
import { Button, Card } from '@payloadcms/ui';

<Card>
  <Button>Click me</Button>
</Card>

// ✅ Good: Utility CSS classes
<div className="flex items-center gap-4 p-4">
  <span className="text-lg font-bold">Artist Name</span>
</div>

// ❌ Avoid: Heavy CSS-in-JS (unless already in use)
import styled from 'styled-components';
const StyledDiv = styled.div`
  display: flex;
  padding: 1rem;
`;
```

### HTTP Clients

**Use:** Native `fetch` (built into Next.js) or `axios` (already installed)
**Avoid:** Adding new HTTP clients unnecessarily

```typescript
// ✅ Good: Native fetch (Next.js optimized)
const response = await fetch('/api/artists');
const artists = await response.json();

// ✅ Good: axios (already installed, more features)
import axios from 'axios';
const { data } = await axios.get('/api/artists');

// ❌ Avoid: Adding new HTTP clients
// Don't install: got, node-fetch, request, etc.
```

## Bundle Optimization

### Dynamic Imports

Use dynamic imports for heavy components not needed immediately:

```typescript
// ✅ Good: Dynamic import for heavy chart library
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // Disable SSR if component uses browser-only APIs
});

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart data={data} />
    </div>
  );
}
```

### Image Optimization

**Always use Next.js Image component:**

```typescript
// ✅ Good: Next.js Image with optimization
import Image from 'next/image';

<Image
  src="/artist-photo.jpg"
  alt="Artist name"
  width={800}
  height={600}
  quality={80} // Default is 75
  priority={false} // Lazy load by default
  formats={['image/webp']} // Use modern formats
/>

// ❌ Bad: Regular img tag (no optimization)
<img src="/artist-photo.jpg" alt="Artist" />
```

**Image format recommendations:**
- Use WebP for photos (better compression)
- Use SVG for logos and icons
- Optimize images before adding to repository
- Keep original images under 500KB

### Code Splitting at Route Level

Next.js automatically code-splits by route. Leverage this:

```typescript
// ✅ Good: Each route is automatically split
// app/artists/page.tsx - Only loaded when visiting /artists
// app/concerts/page.tsx - Only loaded when visiting /concerts
// app/schedule/page.tsx - Only loaded when visiting /schedule

// Each page.tsx is a separate bundle
```

### Lazy Load Below-the-Fold Content

```typescript
// ✅ Good: Lazy load content not immediately visible
import { lazy, Suspense } from 'react';

const Comments = lazy(() => import('@/components/Comments'));
const RelatedArtists = lazy(() => import('@/components/RelatedArtists'));

export default function ArtistPage() {
  return (
    <div>
      <ArtistHeader />
      <ArtistBio />
      
      <Suspense fallback={<div>Loading comments...</div>}>
        <Comments />
      </Suspense>
      
      <Suspense fallback={<div>Loading related artists...</div>}>
        <RelatedArtists />
      </Suspense>
    </div>
  );
}
```

### Bundle Analysis

Run bundle analyzer to identify large dependencies:

```bash
# Add to package.json scripts
"analyze": "ANALYZE=true next build"

# Run analysis
npm run analyze
```

**Red flags to watch for:**
- Any single package > 100KB
- Total bundle size > 500KB (first load)
- Duplicate dependencies
- Unused dependencies

## Security Best Practices

### No Secrets in Code

**NEVER commit secrets to the repository:**

```typescript
// ❌ BAD: Secrets in code
const API_KEY = 'sk-1234567890abcdef';
const DATABASE_URL = 'postgres://user:password@host/db';

// ✅ GOOD: Use environment variables
const API_KEY = process.env.API_KEY;
const DATABASE_URL = process.env.DATABASE_URL;

// Validate required env vars at startup
if (!API_KEY) {
  throw new Error('API_KEY environment variable is required');
}
```

**Environment variable management:**
```bash
# .env.local (not committed)
API_KEY=sk-1234567890abcdef
DATABASE_URL=postgres://user:password@host/db

# .env.example (committed, no real values)
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

### Sanitize User Input

**ALWAYS sanitize before rendering user input:**

```typescript
// ✅ Good: Use DOMPurify for HTML sanitization
import DOMPurify from 'dompurify';

const cleanHTML = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'a'],
  ALLOWED_ATTR: ['href'],
});

// Render safely
<div dangerouslySetInnerHTML={{ __html: cleanHTML }} />

// ✅ Good: Validation for expected formats
import { validateEmail, validateUrl } from '@/utils/validation';

if (!validateEmail(email)) {
  throw new Error('Invalid email format');
}

if (!validateUrl(website)) {
  throw new Error('Invalid URL format');
}
```

**See existing patterns in `bin/migrations/shared/validation.ts`:**
- Email validation
- URL validation
- Phone number validation
- Safe string cleaning

### Dependency Auditing

**Regular security checks:**

```bash
# Check for vulnerabilities
yarn audit

# Fix automatically (if possible)
yarn audit fix

# Check specific package
yarn why package-name
```

**Automated with Dependabot** (see `docs/dependency-management.md`):
- Weekly updates
- Grouped by ecosystem
- Security patches prioritized

### Input Validation

```typescript
// ✅ Good: Validate at boundaries
export async function createArtist(data: unknown) {
  // 1. Validate input structure
  const validated = ArtistSchema.parse(data);
  
  // 2. Sanitize strings
  const sanitized = {
    ...validated,
    name: DOMPurify.sanitize(validated.name),
    bio: DOMPurify.sanitize(validated.bio),
  };
  
  // 3. Process safely
  return await db.artists.create(sanitized);
}

// ❌ Bad: No validation
export async function createArtist(data: any) {
  return await db.artists.create(data); // Dangerous!
}
```

## Adding New Dependencies

### Before Installing

**Ask these questions:**
1. Is this functionality available in existing dependencies?
2. What is the bundle size impact?
3. Is it actively maintained? (recent updates, good docs)
4. Does it have security vulnerabilities?
5. Is it compatible with our stack (React 19, Next.js 15)?

### Installation Process

```bash
# 1. Check bundle size impact
npm install --save-dev bundle-phobia-cli
npx bundle-phobia package-name

# 2. Check security and maintenance
npm info package-name

# 3. Install as appropriate
yarn add package-name              # Production dependency
yarn add -D package-name           # Dev dependency

# 4. Update package.json and yarn.lock
# Commit both files together
```

### ESLint Plugins

**IMPORTANT:** Must be compatible with ESLint 8.x (see `docs/dependency-management.md`)

```bash
# ✅ Good: ESLint 8 compatible
yarn add -D eslint-plugin-react@^7.0.0
yarn add -D eslint-plugin-react-hooks@^4.0.0
yarn add -D eslint-plugin-jsx-a11y@^6.0.0

# ❌ Bad: ESLint 9 required (not yet compatible)
# DO NOT install packages requiring ESLint 9
```

## Dependency Categories

### Production Dependencies

Install with `yarn add`:
- React, Next.js, Payload CMS (core framework)
- Database clients (pg, mysql2)
- Runtime utilities (date-fns, axios)
- UI libraries used in production

### Development Dependencies

Install with `yarn add -D`:
- Testing (vitest, @testing-library/*)
- Linting (eslint, prettier)
- Type definitions (@types/*)
- Build tools (typescript, tsx)
- Storybook (storybook, @storybook/*)

### Peer Dependencies

Let yarn handle automatically. If warnings appear:
```bash
# Check peer dependency requirements
yarn info package-name peerDependencies

# Install missing peers if needed
yarn add peer-dependency-name@version
```

## Maintenance Strategy

### Keep Dependencies Updated

See `docs/dependency-management.md` for full strategy.

**Weekly tasks:**
- Review Dependabot PRs
- Run `yarn audit` for security issues
- Update patch versions liberally
- Test minor updates before merging
- Plan major updates carefully

### Remove Unused Dependencies

```bash
# Find unused dependencies
npx depcheck

# Remove safely
yarn remove unused-package-name

# Clean up after removal
yarn install
```

### Version Pinning

**Exact versions** for critical packages:
```json
{
  "dependencies": {
    "next": "15.5.9",           // Exact version
    "react": "^19.2.3",         // Allow patches
    "payload": "^3.69.0"        // Allow minor updates
  }
}
```

## Quick Reference

### Checklist for New Dependencies

- [ ] Checked bundle size impact
- [ ] Verified no security vulnerabilities
- [ ] Confirmed active maintenance
- [ ] Compatible with ESLint 8 (if ESLint plugin)
- [ ] Compatible with React 19 / Next.js 15
- [ ] Added to correct section (dependencies vs devDependencies)
- [ ] Documented usage in code
- [ ] Committed package.json and yarn.lock together

### Bundle Size Targets

- **First load JS**: < 200KB (gzipped)
- **Route bundles**: < 100KB each
- **Individual packages**: < 50KB (if possible)

### Security Checklist

- [ ] No secrets in code
- [ ] Environment variables for configuration
- [ ] User input sanitized before rendering
- [ ] Dependencies regularly audited
- [ ] Dependabot enabled and monitored

## Resources

- [Dependency Management Docs](../../docs/dependency-management.md)
- [Bundle Size Calculator](https://bundlephobia.com/)
- [NPM Security Advisories](https://www.npmjs.com/advisories)
- [Snyk Vulnerability DB](https://snyk.io/vuln/)
