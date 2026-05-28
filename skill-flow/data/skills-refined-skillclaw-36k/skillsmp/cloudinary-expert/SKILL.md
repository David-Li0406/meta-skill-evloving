---
name: cloudinary-expert
description: Expert in Cloudinary image management, upload patterns, transformations, optimization, and integration with this Next.js project. Use this skill for Cloudinary upload issues, image optimization, signature generation, or folder management.
---

# Cloudinary Expert

You are an expert in Cloudinary integration for this Next.js project, with deep knowledge of upload patterns, image transformations, optimization strategies, signature generation, and folder management.

## Project Configuration

### Environment Variables
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your_cloud_name  # For client-side operations
```

**Important**: 
- Server-side operations use `CLOUDINARY_CLOUD_NAME` (without NEXT_PUBLIC_)
- Client-side operations may need `NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME`
- Always validate all three credentials are set before operations

### Package Dependencies
- **cloudinary**: `^2.8.0` (SDK for advanced operations)
- **crypto**: Node.js built-in (for signature generation)

## Folder Structure

The project uses a consistent folder structure in Cloudinary:

```
authorsinfo/
├── book_cover/              # Book cover images
├── book_entity_header_cover/ # Book entity header covers
├── authorimage/             # Author profile images
├── entity_header_cover/      # Generic entity header covers
├── user_photos/             # User uploaded photos
├── {entityType}_photos/     # Dynamic entity photo folders (e.g., author_photos, publisher_photos)
└── link_previews/           # Optimized link preview images
```

**Pattern**: All images are stored under `authorsinfo/` prefix for organization.

## Upload Patterns

### 1. Base64 Image Upload (Server Action)

**Location**: `app/actions/upload.ts`

```typescript
import { uploadImage } from '@/app/actions/upload'

// Upload with base64 string
const result = await uploadImage(
  base64Image: string,        // Base64 string or data URL
  folder = 'general',         // Cloudinary folder path
  alt_text = '',              // Alt text for database
  maxWidth?: number,          // Optional max width
  maxHeight?: number,         // Optional max height
  img_type_id?: string        // Optional image type ID
)
```

**Features**:
- Automatically converts to WebP format (`f_webp`)
- Handles both raw base64 and data URLs
- Generates signed uploads with SHA1 signature
- Saves to Supabase `images` table
- Returns Cloudinary URL and database record

**Transformation Pattern**:
```typescript
let transformationString = 'f_webp' // Always WebP
if (maxWidth && maxHeight) {
  transformationString += `,c_fit,w_${maxWidth},h_${maxHeight}`
} else if (maxWidth) {
  transformationString += `,c_fit,w_${maxWidth}`
} else if (maxHeight) {
  transformationString += `,c_fit,h_${maxHeight}`
}
```

### 2. File Upload (Server Action)

**Location**: `app/actions/upload-photo.ts`

```typescript
import { uploadPhoto } from '@/app/actions/upload-photo'

const result = await uploadPhoto(
  file: File,                 // File object from form
  entityType: string,         // 'author', 'publisher', 'book', etc.
  entityId: string,           // Entity ID
  albumId?: string            // Optional album ID
)
```

**Features**:
- Validates file type (images only)
- Validates file size (10MB limit)
- Converts to WebP with 95% quality (`f_webp,q_95`)
- Stores in `authorsinfo/{entityType}_photos` folder
- Creates database record in `images` table
- Optionally links to album via `album_images` table

### 3. Entity Image Upload (API Route)

**Location**: `app/api/upload/entity-image/route.ts`

**Endpoint**: `POST /api/upload/entity-image`

**FormData Parameters**:
- `file`: File object
- `entityType`: Entity type (author, publisher, book, etc.)
- `entityId`: Entity ID
- `imageType`: Image type (avatar, bookCover, entityHeaderCover)
- `originalType`: Original type for folder determination

**Features**:
- Comprehensive error handling with rollback
- Validates Cloudinary URL before saving
- Deletes from Cloudinary if database operations fail
- Supports multiple image types with folder mapping
- Updates entity records with image relationships

**Folder Mapping**:
```typescript
let folderType = imageType // Default
if (originalType === 'entityHeaderCover') {
  folderType = 'entity_header_cover'
} else if (originalType === 'bookCover') {
  folderType = 'book_cover'
}
const folderPath = `authorsinfo/${folderType}`
```

### 4. Cloudinary SDK Upload (Advanced)

**Location**: `lib/link-preview/image-optimizer.ts`, `app/actions/bulk-import-books.ts`

```typescript
import { v2 as cloudinary } from 'cloudinary'

// Configure once
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
})

// Upload with transformations
const result = await cloudinary.uploader.upload(imageUrl, {
  folder: 'authorsinfo/book_cover',
  transformation: [
    {
      width: 1200,
      height: 630,
      crop: 'fill',
      quality: 'auto',
      fetch_format: 'auto',
    },
  ],
  resource_type: 'image',
})
```

**Use Cases**:
- Bulk imports from external URLs
- Link preview optimization
- Advanced transformations
- Stream-based uploads

## Signature Generation

### Server-Side Signature API

**Location**: `app/api/cloudinary/signature/route.ts`

**Endpoint**: `POST /api/cloudinary/signature`

**Request Body**:
```json
{
  "folder": "book_cover"
}
```

**Response**:
```json
{
  "timestamp": 1234567890,
  "signature": "abc123...",
  "folder": "authorsinfo/book_cover",
  "apiKey": "your_api_key",
  "cloudName": "your_cloud_name"
}
```

**Signature Generation Pattern**:
```typescript
// 1. Create timestamp
const timestamp = Math.round(new Date().getTime() / 1000)

// 2. Prepare parameters
const params: Record<string, string> = {
  timestamp: timestamp.toString(),
  folder: folderPath,
  // Add other params (transformation, etc.)
}

// 3. Sort alphabetically (REQUIRED)
const sortedParams = Object.keys(params)
  .sort()
  .reduce((acc: Record<string, string>, key) => {
    acc[key] = params[key]
    return acc
  }, {})

// 4. Create signature string
const signatureString =
  Object.entries(sortedParams)
    .map(([key, value]) => `${key}=${value}`)
    .join('&') + apiSecret

// 5. Generate SHA1 hash
const signature = crypto.createHash('sha1')
  .update(signatureString)
  .digest('hex')
```

**Critical Rules**:
1. Parameters MUST be sorted alphabetically
2. Signature string format: `key1=value1&key2=value2&...apiSecret`
3. Use SHA1 hash (not SHA256)
4. Include timestamp in seconds (not milliseconds)

## Image Transformations

### Standard Transformations

**WebP Conversion** (Always Applied):
```typescript
transformation: 'f_webp'                    // Format: WebP
transformation: 'f_webp,q_95'              // Format: WebP, Quality: 95%
```

**Resizing**:
```typescript
// Fit to dimensions (maintains aspect ratio)
transformation: 'c_fit,w_1200,h_630'

// Fill (crops to fit)
transformation: 'c_fill,w_1200,h_630'

// Scale (maintains aspect ratio, may not match exact dimensions)
transformation: 'c_scale,w_1200'
```

**Link Preview Optimization**:
```typescript
// Main image: 1200x630 (Open Graph standard)
{
  width: 1200,
  height: 630,
  crop: 'fill',
  quality: 'auto',
  fetch_format: 'auto',
}

// Thumbnail: 400x210
{
  width: 400,
  height: 210,
  crop: 'fill',
  quality: 'auto',
  fetch_format: 'auto',
}
```

### Transformation String Format

Cloudinary uses comma-separated transformation parameters:

```typescript
// Format: f_webp
// Crop: c_fit, c_fill, c_scale
// Width: w_1200
// Height: h_630
// Quality: q_95, q_auto

// Examples:
'f_webp'                                    // WebP only
'f_webp,q_95'                               // WebP with quality
'f_webp,c_fit,w_1200,h_630'                // WebP, fit, dimensions
'f_webp,q_auto,c_fill,w_1200,h_630'        // Full optimization
```

## Delete Operations

### Delete API Route

**Location**: `app/api/cloudinary/delete/route.ts`

**Endpoint**: `POST /api/cloudinary/delete`

**Request Body**:
```json
{
  "publicId": "authorsinfo/book_cover/image_id"
}
```

**Implementation**:
```typescript
// 1. Generate signature for delete
const timestamp = Math.round(new Date().getTime() / 1000)
const signature = crypto.createHash('sha1')
  .update(`public_id=${publicId}&timestamp=${timestamp}${apiSecret}`)
  .digest('hex')

// 2. Create form data
const formData = new FormData()
formData.append('public_id', publicId)
formData.append('api_key', apiKey)
formData.append('timestamp', timestamp.toString())
formData.append('signature', signature)

// 3. Delete via API
const response = await fetch(
  `https://api.cloudinary.com/v1_1/${cloudName}/image/destroy`,
  {
    method: 'POST',
    body: formData,
  }
)
```

**SDK Delete**:
```typescript
await cloudinary.uploader.destroy(publicId)
```

**Important**: Always delete from Cloudinary when database operations fail to prevent orphaned assets.

## List Operations

### List API Route

**Location**: `app/api/cloudinary/list/route.ts`

**Endpoint**: `GET /api/cloudinary/list?folder=authorsinfo/book_cover&max_results=50`

**Query Parameters**:
- `folder`: Folder prefix to filter (optional)
- `max_results`: Maximum number of results (default: 50)

**Response**:
```json
{
  "success": true,
  "data": {
    "resources": [...],
    "next_cursor": "cursor_string",
    "total_count": 50
  }
}
```

## URL Validation

### Validation Utilities

**Location**: `lib/utils/image-url-validation.ts`

**Functions**:

```typescript
// Validate Cloudinary URL
isValidCloudinaryUrl(url: string | null | undefined): boolean

// Validate and sanitize
validateAndSanitizeImageUrl(url: string | null | undefined): string | null

// Check if URL should be rejected
shouldRejectUrl(url: string | null | undefined): boolean

// Add cache-busting
addCacheBusting(url: string | null | undefined): string | null
```

**Validation Rules**:
- ✅ Accepts: `https://res.cloudinary.com/{cloud_name}/image/upload/...`
- ✅ Accepts: `https://api.cloudinary.com/{cloud_name}/image/upload/...`
- ❌ Rejects: `blob:` URLs
- ❌ Rejects: `data:` URLs
- ❌ Rejects: Local file paths (`file://`, `C:\`, `/Users/`)

**Pattern**:
```typescript
const cloudinaryPattern = 
  /^https?:\/\/(res|api)\.cloudinary\.com\/[^\/]+\/(image|video)\/upload\//
```

## Link Preview Optimization

### Image Optimizer

**Location**: `lib/link-preview/image-optimizer.ts`

**Function**:
```typescript
import { optimizeLinkPreviewImage } from '@/lib/link-preview/image-optimizer'

const result = await optimizeLinkPreviewImage(
  imageUrl: string,
  linkId?: string
)
```

**Returns**:
```typescript
{
  original_url: string
  optimized_url: string      // 1200x630 main image
  thumbnail_url: string       // 400x210 thumbnail
  width: number
  height: number
  format: 'webp' | 'avif' | 'jpeg' | 'png'
  size_bytes: number
  cloudinary_public_id: string
}
```

**Process**:
1. Validates image URL
2. Downloads image with timeout (10 seconds)
3. Uploads optimized main image (1200x630)
4. Uploads thumbnail (400x210)
5. Stores in `authorsinfo/link_previews` folder
6. Returns both URLs and metadata

**Delete Function**:
```typescript
import { deleteOptimizedImage } from '@/lib/link-preview/image-optimizer'

await deleteOptimizedImage(publicId: string)
```

## Error Handling & Rollback

### Rollback Pattern

When database operations fail after Cloudinary upload:

```typescript
try {
  // 1. Upload to Cloudinary
  const cloudinaryResult = await uploadToCloudinary(...)
  
  // 2. Save to database
  const dbResult = await saveToDatabase(...)
  
  if (!dbResult.success) {
    // 3. ROLLBACK: Delete from Cloudinary
    await deleteFromCloudinary(cloudinaryResult.public_id)
    throw new Error('Database save failed, image removed from Cloudinary')
  }
} catch (error) {
  // Cleanup on any error
  if (cloudinaryResult?.public_id) {
    await deleteFromCloudinary(cloudinaryResult.public_id)
  }
  throw error
}
```

**Helper Function** (from `app/api/upload/entity-image/route.ts`):
```typescript
async function deleteFromCloudinary(publicId: string): Promise<void> {
  const cloudName = process.env.CLOUDINARY_CLOUD_NAME
  const apiKey = process.env.CLOUDINARY_API_KEY
  const apiSecret = process.env.CLOUDINARY_API_SECRET

  if (!cloudName || !apiKey || !apiSecret) {
    console.error('⚠️ Cannot delete from Cloudinary: credentials not configured')
    return
  }

  const timestamp = Math.round(new Date().getTime() / 1000)
  const signature = crypto.createHash('sha1')
    .update(`public_id=${publicId}&timestamp=${timestamp}${apiSecret}`)
    .digest('hex')

  const formData = new FormData()
  formData.append('public_id', publicId)
  formData.append('api_key', apiKey)
  formData.append('timestamp', timestamp.toString())
  formData.append('signature', signature)

  const response = await fetch(
    `https://api.cloudinary.com/v1_1/${cloudName}/image/destroy`,
    { method: 'POST', body: formData }
  )

  if (response.ok) {
    console.log(`✅ Rollback: Deleted orphaned image from Cloudinary: ${publicId}`)
  } else {
    console.error(`⚠️ Rollback failed: Could not delete image from Cloudinary: ${publicId}`)
  }
}
```

## Rate Limiting

### Handling Rate Limits

Cloudinary may return `429 Too Many Requests`. Handle gracefully:

```typescript
if (!response.ok) {
  if (response.status === 429) {
    console.error('Cloudinary rate limit exceeded. Waiting before retrying...')
    await new Promise((resolve) => setTimeout(resolve, 1000))
    throw new Error('Cloudinary rate limit exceeded. Please try again in a moment.')
  }
  // Handle other errors...
}
```

## Public ID Extraction

### Extract Public ID from URL

```typescript
function extractPublicIdFromUrl(url: string): string | null {
  if (!url || !url.includes('cloudinary.com')) return null
  
  // Pattern: https://res.cloudinary.com/{cloud_name}/image/upload/{folder}/public_id.ext
  const match = url.match(/\/upload\/(.+?)(?:\.[^.]+)?$/)
  return match ? match[1] : null
}

// Example:
// URL: https://res.cloudinary.com/demo/image/upload/authorsinfo/book_cover/my_image
// Returns: authorsinfo/book_cover/my_image
```

## Database Integration

### Images Table Schema

Images are stored in Supabase `images` table with:

- `url`: Cloudinary secure URL
- `storage_provider`: Always `'cloudinary'`
- `storage_path`: Folder path (e.g., `authorsinfo/book_cover`)
- `cloudinary_public_id`: Public ID for deletion
- `original_filename`: Original file name
- `file_size`: File size in bytes
- `mime_type`: MIME type
- `is_processed`: Boolean
- `processing_status`: Status string

### Entity Relationships

Images are linked to entities via:
- `book_cover_image_id` → `images.id`
- `author_image_id` → `images.id`
- `publisher_image_id` → `images.id`
- `entity_header_cover_image_id` → `images.id`
- `album_images` table for photo galleries

## Best Practices

### ✅ DO

1. **Always validate Cloudinary URLs** before saving to database
2. **Use rollback pattern** when database operations fail
3. **Generate signatures correctly** (sorted params, SHA1)
4. **Convert to WebP** for better performance
5. **Use appropriate folder structure** (`authorsinfo/{type}`)
6. **Store public_id** in database for easy deletion
7. **Handle rate limits** gracefully
8. **Validate file types and sizes** before upload
9. **Use signed uploads** for security
10. **Clean up orphaned assets** when operations fail

### ❌ DON'T

1. **Don't store blob/data URLs** in database
2. **Don't skip signature validation** in folder paths
3. **Don't forget to sort parameters** for signatures
4. **Don't use SHA256** for signatures (use SHA1)
5. **Don't hardcode credentials** (use environment variables)
6. **Don't skip error handling** and rollback
7. **Don't upload without transformations** (always optimize)
8. **Don't ignore rate limits** (implement retry logic)
9. **Don't store local file paths** in database
10. **Don't create orphaned assets** (always clean up on failure)

## Common Issues & Solutions

### Issue: "Invalid folder path" Error

**Cause**: Folder path contains invalid characters or doesn't match pattern.

**Solution**:
```typescript
// Validate folder path
if (!folder || typeof folder !== 'string' || !folder.match(/^[a-zA-Z0-9_/-]+$/)) {
  throw new Error('Invalid folder path')
}
```

### Issue: Signature Validation Failed

**Cause**: Parameters not sorted or signature string format incorrect.

**Solution**:
```typescript
// Always sort parameters alphabetically
const sortedParams = Object.keys(params)
  .sort()
  .reduce((acc, key) => {
    acc[key] = params[key]
    return acc
  }, {})
```

### Issue: Orphaned Images in Cloudinary

**Cause**: Database operations failed after Cloudinary upload.

**Solution**: Implement rollback pattern (see Error Handling section).

### Issue: Rate Limit Errors

**Cause**: Too many requests to Cloudinary API.

**Solution**: Implement exponential backoff and retry logic.

### Issue: Invalid Cloudinary URL

**Cause**: URL doesn't match Cloudinary pattern or is a blob/data URL.

**Solution**: Use `isValidCloudinaryUrl()` before saving.

## Testing & Validation

### Validate Configuration

```typescript
// Check environment variables
const cloudName = process.env.CLOUDINARY_CLOUD_NAME
const apiKey = process.env.CLOUDINARY_API_KEY
const apiSecret = process.env.CLOUDINARY_API_SECRET

if (!cloudName || !apiKey || !apiSecret) {
  throw new Error('Cloudinary credentials are not properly configured')
}
```

### Test Upload

```typescript
// Test with minimal image
const testImage = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='

const result = await uploadImage(testImage, 'test', 'Test image')
console.log('Upload successful:', result.url)
```

### Verify URL Format

```typescript
import { isValidCloudinaryUrl } from '@/lib/utils/image-url-validation'

const isValid = isValidCloudinaryUrl(url)
if (!isValid) {
  console.error('Invalid Cloudinary URL:', url)
}
```

## Code Review Checklist

When reviewing Cloudinary code:

- [ ] Environment variables are validated before use
- [ ] Signatures are generated with sorted parameters
- [ ] SHA1 hash is used (not SHA256)
- [ ] Folder paths are validated for security
- [ ] Rollback pattern is implemented for failed database operations
- [ ] Cloudinary URLs are validated before saving
- [ ] File types and sizes are validated
- [ ] Transformations are applied (WebP conversion)
- [ ] Public IDs are stored for deletion
- [ ] Error handling includes rate limit handling
- [ ] No blob/data URLs are stored in database
- [ ] Appropriate folder structure is used
- [ ] Cache-busting is considered for updated images

## Related Files

### Core Upload Functions
- `app/actions/upload.ts` - Base64 upload
- `app/actions/upload-photo.ts` - File upload
- `app/api/upload/entity-image/route.ts` - Entity image API

### API Routes
- `app/api/cloudinary/signature/route.ts` - Signature generation
- `app/api/cloudinary/delete/route.ts` - Delete operation
- `app/api/cloudinary/list/route.ts` - List resources

### Utilities
- `lib/utils/image-url-validation.ts` - URL validation
- `lib/link-preview/image-optimizer.ts` - Link preview optimization

### Bulk Operations
- `app/actions/bulk-import-books.ts` - Bulk book import with images
- `app/actions/bulk-add-books-from-search.ts` - Search-based import

## Resources

- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Cloudinary Transformation Reference](https://cloudinary.com/documentation/transformation_reference)
- [Cloudinary Upload API](https://cloudinary.com/documentation/upload_images)
- [Cloudinary Node.js SDK](https://cloudinary.com/documentation/node_integration)
