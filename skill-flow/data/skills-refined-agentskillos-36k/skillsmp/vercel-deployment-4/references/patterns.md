# Vercel Deployment

## Patterns


---
  #### **Name**
Environment Variables Setup
  #### **Description**
Properly configure environment variables for all environments
  #### **When**
Setting up a new project on Vercel
  #### **Example**
    // Three environments in Vercel:
    // - Development (local)
    // - Preview (PR deployments)
    // - Production (main branch)
    
    // In Vercel Dashboard:
    // Settings → Environment Variables
    
    // PUBLIC variables (exposed to browser)
    NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
    NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
    
    // PRIVATE variables (server only)
    SUPABASE_SERVICE_ROLE_KEY=eyJ...  // Never NEXT_PUBLIC_!
    DATABASE_URL=postgresql://...
    
    // Per-environment values:
    // Production: Real database, production API keys
    // Preview: Staging database, test API keys
    // Development: Local/dev values (also in .env.local)
    
    // In code, check environment:
    const isProduction = process.env.VERCEL_ENV === 'production'
    const isPreview = process.env.VERCEL_ENV === 'preview'
    

---
  #### **Name**
Edge vs Serverless Functions
  #### **Description**
Choose the right runtime for your API routes
  #### **When**
Creating API routes or middleware
  #### **Example**
    // EDGE RUNTIME - Fast cold starts, limited APIs
    // Good for: Auth checks, redirects, simple transforms
    
    // app/api/hello/route.ts
    export const runtime = 'edge'
    
    export async function GET() {
      return Response.json({ message: 'Hello from Edge!' })
    }
    
    // middleware.ts (always edge)
    export function middleware(request: NextRequest) {
      // Fast auth checks here
    }
    
    // SERVERLESS (Node.js) - Full Node APIs, slower cold start
    // Good for: Database queries, file operations, heavy computation
    
    // app/api/users/route.ts
    export const runtime = 'nodejs'  // Default, can omit
    
    export async function GET() {
      const users = await db.query('SELECT * FROM users')
      return Response.json(users)
    }
    

---
  #### **Name**
Build Optimization
  #### **Description**
Optimize build for faster deployments and smaller bundles
  #### **When**
Preparing for production deployment
  #### **Example**
    // next.config.js
    /** @type {import('next').NextConfig} */
    const nextConfig = {
      // Minimize output
      output: 'standalone',  // For Docker/self-hosting
    
      // Image optimization
      images: {
        remotePatterns: [
          { hostname: 'your-cdn.com' },
        ],
      },
    
      // Bundle analyzer (dev only)
      // npm install @next/bundle-analyzer
      ...(process.env.ANALYZE === 'true' && {
        webpack: (config) => {
          const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
          config.plugins.push(new BundleAnalyzerPlugin())
          return config
        },
      }),
    }
    
    // Reduce serverless function size:
    // - Use dynamic imports for heavy libs
    // - Check bundle with: npx @next/bundle-analyzer
    

---
  #### **Name**
Preview Deployment Workflow
  #### **Description**
Use preview deployments for PR reviews
  #### **When**
Setting up team development workflow
  #### **Example**
    // Every PR gets a unique preview URL automatically
    
    // Protect preview deployments with password:
    // Vercel Dashboard → Settings → Deployment Protection
    
    // Use different env vars for preview:
    // - PREVIEW: Use staging database
    // - PRODUCTION: Use production database
    
    // In code, detect preview:
    if (process.env.VERCEL_ENV === 'preview') {
      // Show "Preview" banner
      // Use test payment processor
      // Disable analytics
    }
    
    // Comment preview URL on PR (automatic with Vercel GitHub integration)
    

---
  #### **Name**
Custom Domain Setup
  #### **Description**
Configure custom domains with proper SSL
  #### **When**
Going to production
  #### **Example**
    // In Vercel Dashboard → Domains
    
    // Add domains:
    // - example.com (apex/root)
    // - www.example.com (subdomain)
    
    // DNS Configuration (at your registrar):
    // Type: A, Name: @, Value: 76.76.21.21
    // Type: CNAME, Name: www, Value: cname.vercel-dns.com
    
    // Redirect www to apex (or vice versa):
    // Vercel handles this automatically
    
    // In next.config.js for redirects:
    module.exports = {
      async redirects() {
        return [
          {
            source: '/old-page',
            destination: '/new-page',
            permanent: true,  // 308
          },
        ]
      },
    }
    

## Anti-Patterns


---
  #### **Name**
Secrets in NEXT_PUBLIC_
  #### **Description**
Exposing secret keys with NEXT_PUBLIC_ prefix
  #### **Why**
NEXT_PUBLIC_ variables are bundled into client JavaScript, visible to anyone
  #### **Instead**
Only use NEXT_PUBLIC_ for truly public values (URLs, public API keys)

---
  #### **Name**
Same Database for Preview
  #### **Description**
Using production database for preview deployments
  #### **Why**
Testers can corrupt production data, preview PRs can break production
  #### **Instead**
Use separate staging/preview database with its own env vars

---
  #### **Name**
No Build Cache
  #### **Description**
Not utilizing Vercel's build cache
  #### **Why**
Slower builds, wasted compute, longer deployment times
  #### **Instead**
Use proper caching, remote caching for monorepos

---
  #### **Name**
Oversized Functions
  #### **Description**
Serverless functions over 50MB
  #### **Why**
Slow cold starts, deployment failures, poor user experience
  #### **Instead**
Use dynamic imports, tree shaking, separate heavy functions