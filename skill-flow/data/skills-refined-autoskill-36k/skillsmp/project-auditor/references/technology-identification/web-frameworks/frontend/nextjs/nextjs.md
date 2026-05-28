# Next.js

**Category**: web-frameworks/frontend
**Description**: The React Framework for Production - Server-side rendering and static site generation
**Homepage**: https://nextjs.org

## Package Detection

### NPM
*Next.js framework*

- `next`

### Related Packages
- `react`
- `react-dom`
- `@vercel/analytics`

## Import Detection

### Javascript
File extensions: .js, .jsx, .ts, .tsx

**Pattern**: `import.*from ['"]next/`
- Next.js imports
- Example: `import Link from 'next/link';`

**Pattern**: `export.*getServerSideProps`
- Next.js SSR
- Example: `export async function getServerSideProps()`

**Pattern**: `export.*getStaticProps`
- Next.js SSG
- Example: `export async function getStaticProps()`

### Common Imports
- `next/link`
- `next/router`
- `next/image`
- `next/head`

## Environment Variables

*Next.js public environment variables*

- Prefix: `NEXT_PUBLIC_*`

## Configuration Files

- `next.config.js`
- `next.config.mjs`
- `pages/_app.js`
- `app/layout.js`

## Detection Notes

- Always requires React
- Look for next.config.js
- pages/ or app/ directory structure

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
- **API Endpoint Detection**: 60% (MEDIUM)
