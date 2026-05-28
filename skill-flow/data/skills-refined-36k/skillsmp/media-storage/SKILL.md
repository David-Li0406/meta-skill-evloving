---
name: Media & Storage
description: Handle image/video uploads, optimization, and Supabase storage
---

# Media & Storage Skill

## Overview
Handle all media uploads, optimization, and storage using Supabase Storage.

## Storage Buckets
| Bucket | Purpose | Public |
|--------|---------|--------|
| `avatars` | User profile pictures | Yes |
| `posts` | Social media images/videos | Yes |
| `cards` | Playing card assets | Yes |
| `private` | User documents | No |

## Image Upload
```javascript
async function uploadImage(file, bucket, path) {
  // Validate file
  const maxSize = 5 * 1024 * 1024; // 5MB
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
  
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)');
  }
  
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type');
  }
  
  // Generate unique filename
  const ext = file.name.split('.').pop();
  const filename = `${Date.now()}_${crypto.randomUUID()}.${ext}`;
  const fullPath = `${path}/${filename}`;
  
  // Upload
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(fullPath, file, {
      cacheControl: '3600',
      upsert: false
    });
  
  if (error) throw error;
  
  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from(bucket)
    .getPublicUrl(fullPath);
  
  return publicUrl;
}
```

## Image Optimization
```javascript
async function optimizeImage(file, maxWidth = 1200, quality = 0.8) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const scale = Math.min(1, maxWidth / img.width);
      
      canvas.width = img.width * scale;
      canvas.height = img.height * scale;
      
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      
      canvas.toBlob(resolve, 'image/webp', quality);
    };
    img.src = URL.createObjectURL(file);
  });
}
```

## Avatar Upload with Crop
```javascript
async function uploadAvatar(userId, file) {
  // Optimize to square 400x400
  const optimized = await cropToSquare(file, 400);
  
  // Upload
  const url = await uploadImage(optimized, 'avatars', userId);
  
  // Update profile
  await supabase.from('profiles')
    .update({ avatar_url: url })
    .eq('id', userId);
  
  return url;
}
```

## Video Upload
```javascript
async function uploadVideo(file, onProgress) {
  const maxSize = 100 * 1024 * 1024; // 100MB
  const allowedTypes = ['video/mp4', 'video/webm', 'video/quicktime'];
  
  if (file.size > maxSize) {
    throw new Error('Video too large (max 100MB)');
  }
  
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid video type');
  }
  
  const filename = `${Date.now()}_${crypto.randomUUID()}.mp4`;
  
  // Use tus for resumable uploads
  const { data, error } = await supabase.storage
    .from('posts')
    .upload(`videos/${filename}`, file, {
      cacheControl: '3600',
      upsert: false
    });
  
  return supabase.storage.from('posts').getPublicUrl(`videos/${filename}`).data.publicUrl;
}
```

## Image Component with Lazy Loading
```jsx
import Image from 'next/image';

function OptimizedImage({ src, alt, width, height, ...props }) {
  const [isLoaded, setIsLoaded] = useState(false);
  
  return (
    <div className={`image-wrapper ${isLoaded ? 'loaded' : 'loading'}`}>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        onLoadingComplete={() => setIsLoaded(true)}
        placeholder="blur"
        blurDataURL="/placeholder.png"
        {...props}
      />
    </div>
  );
}
```

## Delete Media
```javascript
async function deleteMedia(bucket, path) {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path]);
  
  if (error) throw error;
}
```

## Components
- `ImageUploader.jsx` - Drag & drop upload
- `AvatarCropper.jsx` - Crop to square
- `VideoPlayer.jsx` - Custom video player
- `MediaGallery.jsx` - Grid display
