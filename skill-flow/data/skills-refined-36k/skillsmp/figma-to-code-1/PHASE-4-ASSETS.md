# Phase 4: Asset Extraction & CDN Upload

## Step 1: Configure Fonts

**For Google Fonts:**

```typescript
// src/app/layout.tsx
import { Inter, Playfair_Display } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-body' });
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-heading' });

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${playfair.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

**For Custom Fonts:**

Place font files in `/public/fonts/` and configure in CSS:

```css
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/CustomFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
```

## Step 2: Export Icons

1. Use Figma MCP to identify all icons
2. Export as SVG or install appropriate icon library
3. For custom icons, create `/src/components/ui/icons/`

## Step 3: Export and Upload Images

### Image Sources During Build

During the initial build, images from Figma MCP are served via temporary Figma API URLs:
```
https://www.figma.com/api/mcp/asset/{asset-id}
```

These URLs will eventually expire. Before going to production, run the **Image Migration Script** (see Step 6) to:
1. Download all Figma-hosted images
2. Upload them to the CMS (which stores them on CDN)
3. Update CMS content entries with permanent CDN URLs

### Manual Upload Process

For images not in Figma (or manual uploads), use the CMS `uploadMedia` mutation:

```typescript
// Upload via CMS API (reference sphereos-cms-api skill for full mutation details)
const result = await uploadMedia({
  file: imageBuffer,
  filename: `${imageName}.webp`,
  organizationId: process.env.CMS_ORGANIZATION_ID,
});
const cdnUrl = result.url; // CMS returns the CDN URL
```

## Step 4: Create Image Manifest

Create `/docs/image-manifest.json` to track all images:

```json
{
  "images": [
    {
      "figmaNodeId": "123:456",
      "originalName": "hero-background",
      "cmsMediaId": "media_xxx",
      "cdnUrl": "https://pub-xxx.r2.dev/media-id/original.webp",
      "dimensions": { "width": 1920, "height": 1080 },
      "usedOn": ["homepage"],
      "fieldPath": "hero.posterUrl"
    }
  ],
  "totalImages": 25,
  "totalSizeKB": 2450
}
```

## Step 5: Image Optimization

Before uploading, optimize images:

- Convert to WebP format where appropriate
- Generate multiple sizes for responsive images
- Compress without visible quality loss

## Step 6: Image Migration Script

**CRITICAL:** Before production deployment, migrate all Figma-hosted images to permanent CDN storage.

Create `scripts/migrate-figma-images.ts`:

```typescript
/**
 * Figma Image Migration Script
 *
 * This script migrates images from temporary Figma MCP URLs to permanent CDN storage.
 * Run BEFORE production deployment to ensure all images are permanently hosted.
 *
 * Usage:
 *   npx tsx scripts/migrate-figma-images.ts
 *
 * Prerequisites:
 *   - CMS_AUTH_TOKEN environment variable (get via login mutation)
 *   - Update constants below for your project
 */

// ============================================
// CONFIGURATION - Update for your project
// ============================================
const CMS_API_URL = 'https://backend-production-162b.up.railway.app/graphql';
const CMS_AUTH_TOKEN = process.env.CMS_AUTH_TOKEN || '';
const ORGANIZATION_ID = 'your-org-id';
const ORGANIZATION_SLUG = 'your-org-slug';
const CONTENT_ENTRY_SLUG = 'home'; // or the page entry to update

// ============================================
// TYPES
// ============================================
interface ImageToMigrate {
  fieldPath: string;
  figmaId: string;
  alt: string;
}

interface MediaUploadResponse {
  uploadMedia: {
    id: string;
    url: string;
    filename: string;
    mimeType: string;
  };
}

// ============================================
// HELPER FUNCTIONS
// ============================================
function extractFigmaAssetId(url: string): string | null {
  const match = url.match(/figma\.com\/api\/mcp\/asset\/([a-f0-9-]+)/i);
  return match ? match[1] : null;
}

async function downloadFigmaImage(assetId: string): Promise<{ buffer: Buffer; mimeType: string }> {
  const url = `https://www.figma.com/api/mcp/asset/${assetId}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to download: ${response.status}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  const contentType = response.headers.get('content-type') || 'image/jpeg';

  return {
    buffer: Buffer.from(arrayBuffer),
    mimeType: contentType,
  };
}

async function uploadToCMS(
  buffer: Buffer,
  filename: string,
  mimeType: string
): Promise<string> {
  const base64 = buffer.toString('base64');

  const mutation = `
    mutation UploadMedia($input: UploadMediaInput!) {
      uploadMedia(input: $input) {
        id
        url
        filename
        mimeType
      }
    }
  `;

  const response = await fetch(CMS_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CMS_AUTH_TOKEN}`,
    },
    body: JSON.stringify({
      query: mutation,
      variables: {
        input: {
          organizationId: ORGANIZATION_ID,
          filename,
          mimeType,
          base64Data: base64,
        },
      },
    }),
  });

  const result = await response.json() as { data?: MediaUploadResponse; errors?: unknown[] };

  if (result.errors) {
    throw new Error(`Upload failed: ${JSON.stringify(result.errors)}`);
  }

  return result.data!.uploadMedia.url;
}

async function updateContentEntry(fieldPath: string, newValue: string): Promise<boolean> {
  // Use inline editor save endpoint for field-level updates
  const saveUrl = CMS_API_URL.replace('/graphql', '/api/inline-editor/save');

  const response = await fetch(saveUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CMS_AUTH_TOKEN}`,
      'X-CMS-Org': ORGANIZATION_SLUG,
    },
    body: JSON.stringify({
      entry: CONTENT_ENTRY_SLUG,
      field: fieldPath,
      value: newValue,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to update: ${response.status} - ${error}`);
  }

  const result = await response.json() as { success: boolean };
  return result.success;
}

// ============================================
// MAIN MIGRATION FUNCTION
// ============================================
async function migrateImages(images: ImageToMigrate[]): Promise<void> {
  console.log(`\nMigrating ${images.length} images...\n`);

  let successCount = 0;
  let failCount = 0;

  for (let i = 0; i < images.length; i++) {
    const image = images[i];
    const figmaId = extractFigmaAssetId(image.figmaId) || image.figmaId;

    console.log(`[${i + 1}/${images.length}] ${image.fieldPath}`);

    try {
      // 1. Download from Figma
      console.log(`  Downloading...`);
      const { buffer, mimeType } = await downloadFigmaImage(figmaId);

      // 2. Determine filename
      const ext = mimeType.includes('svg') ? 'svg'
               : mimeType.includes('png') ? 'png'
               : mimeType.includes('webp') ? 'webp'
               : 'jpg';
      const filename = `${image.fieldPath.replace(/[\[\].]/g, '-')}--${image.alt || 'image'}.${ext}`;

      // 3. Upload to CMS
      console.log(`  Uploading to CDN...`);
      const cdnUrl = await uploadToCMS(buffer, filename, mimeType);

      // 4. Update content entry
      console.log(`  Updating CMS entry...`);
      await updateContentEntry(image.fieldPath, cdnUrl);

      console.log(`  ✓ Migrated to: ${cdnUrl}\n`);
      successCount++;

      // Rate limit
      await new Promise(r => setTimeout(r, 500));

    } catch (error) {
      console.error(`  ✗ FAILED: ${error}\n`);
      failCount++;
    }
  }

  console.log(`\n========================================`);
  console.log(`Migration complete!`);
  console.log(`  Success: ${successCount}`);
  console.log(`  Failed: ${failCount}`);
  console.log(`========================================\n`);
}

// ============================================
// IMAGE LIST - Update for your project
// ============================================
// Extract this from your CMS content entry
const IMAGES_TO_MIGRATE: ImageToMigrate[] = [
  // Example entries - replace with your actual images
  // { fieldPath: 'hero.logoUrl', figmaId: 'xxx-xxx', alt: 'Logo' },
  // { fieldPath: 'hero.posterUrl', figmaId: 'xxx-xxx', alt: 'Hero background' },
  // { fieldPath: 'whyBeckons.cards[0].imageUrl', figmaId: 'xxx-xxx', alt: 'Card 1' },
];

// ============================================
// RUN MIGRATION
// ============================================
if (!CMS_AUTH_TOKEN) {
  console.error('Error: CMS_AUTH_TOKEN environment variable required');
  console.log('\nGet token via login mutation:');
  console.log('mutation { login(input: { email: "...", password: "..." }) { accessToken } }');
  process.exit(1);
}

if (IMAGES_TO_MIGRATE.length === 0) {
  console.log('No images configured. Update IMAGES_TO_MIGRATE array.');
  process.exit(0);
}

migrateImages(IMAGES_TO_MIGRATE).catch(console.error);
```

### Running the Migration

1. **Get auth token:**
   ```bash
   # Use GraphQL playground or curl to login and get token
   curl -X POST https://backend-production-162b.up.railway.app/graphql \
     -H "Content-Type: application/json" \
     -d '{"query":"mutation { login(input: { email: \"...\", password: \"...\" }) { accessToken } }"}'
   ```

2. **Update script configuration** with your organization details

3. **Populate IMAGES_TO_MIGRATE** by extracting Figma URLs from your CMS content

4. **Run migration:**
   ```bash
   CMS_AUTH_TOKEN='your-token' npx tsx scripts/migrate-figma-images.ts
   ```

5. **Verify** images load correctly on the site

## Step 7: Update Next.js Config

```javascript
// next.config.mjs
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'pub-*.r2.dev',  // Cloudflare R2 CDN
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'www.figma.com',  // Figma MCP (dev only)
        pathname: '/api/mcp/asset/**',
      },
    ],
  },
};

export default nextConfig;
```

## Git Commit

```bash
git commit -m "feat: assets extracted and uploaded to CDN"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 4: Assets uploaded" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-5-CONTENT-TYPES.md](PHASE-5-CONTENT-TYPES.md)
