---
name: gravatar-download
description: Download Gravatar avatar images to local files. Use when the user wants to save Gravatar images, download profile pictures, or create local avatar caches.
---

# Download Gravatar Images

Download Gravatar avatar images to local files.

## Usage

```bash
npx tsx scripts/download.ts <email> <output-file> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `email` | Yes | Email address |
| `output-file` | Yes | Path where image will be saved |

### Options

| Option | Description |
|--------|-------------|
| `--size=N` | Image size in pixels (default: 200, max: 2048) |
| `--default=TYPE` | Default image type: mp, identicon, monsterid, wavatar, retro, robohash, blank |
| `--rating=LEVEL` | Rating level: g, pg, r, x (default: g) |
| `--no-cache` | Bypass cache and fetch fresh data |

### Output

```
Email: user@example.com
Output: avatar.jpg
Hash: b48bf4373d7b7374351c0544f36f7fc3

✓ Downloaded successfully
  Size: 12.4 KB
  File: avatar.jpg
```

## Script Execution (Preferred)

```bash
npx tsx scripts/download.ts <email> <output-file> [options]
```

Options:
- `--size=N` - Image size in pixels (default: 200, max: 2048)
- `--default=TYPE` - Default image type: mp, identicon, monsterid, wavatar, retro, robohash, blank
- `--rating=LEVEL` - Rating level: g, pg, r, x (default: g)
- `--no-cache` - Bypass cache and fetch fresh data

Run from the gravatar plugin directory: `~/.claude/plugins/cache/gravatar/`

## How It Works

1. Generates Gravatar URL with specified parameters
2. Downloads image using cached HTTP request
3. Saves image to specified file path
4. Caches downloaded images for 24 hours

## Examples

Basic download (200px PNG):
```bash
npx tsx scripts/download.ts user@example.com avatar.png
```

Large avatar (800px):
```bash
npx tsx scripts/download.ts user@example.com large-avatar.jpg --size=800
```

Download with fallback to identicon:
```bash
npx tsx scripts/download.ts newuser@example.com avatar.png --default=identicon
```

Force fresh download:
```bash
npx tsx scripts/download.ts user@example.com avatar.png --no-cache
```

## Image Size Options

| Size | Use Case | File Size (approx) |
|------|----------|-------------------|
| 80 | Small thumbnails | 2-4 KB |
| 200 | Profile avatars (default) | 8-15 KB |
| 400 | Large profile images | 20-35 KB |
| 800 | High-resolution displays | 50-90 KB |
| 2048 | Maximum quality | 200-400 KB |

## Default Image Types

When no Gravatar exists, these defaults are used:

| Type | Description |
|------|-------------|
| `mp` | Mystery Person (simple silhouette) |
| `identicon` | Geometric pattern based on email hash |
| `monsterid` | Unique monster generated from email |
| `wavatar` | Unique face generated from email |
| `retro` | 8-bit arcade-style face |
| `robohash` | Unique robot generated from email |
| `blank` | Transparent PNG |

## Use Cases

### Team Avatar Cache
Download avatars for all team members:
```bash
for email in dev1@company.com dev2@company.com dev3@company.com; do
  npx tsx scripts/download.ts "$email" "avatars/${email}.png" --size=400
done
```

### Profile Image Backup
Save user avatars locally:
```bash
npx tsx scripts/download.ts maintainer@project.org backup/maintainer.jpg --size=800
```

### Generate Placeholder Avatars
Create consistent default avatars:
```bash
npx tsx scripts/download.ts user1@example.com user1.png --default=identicon
npx tsx scripts/download.ts user2@example.com user2.png --default=identicon
```

### High-Resolution Display
Download retina-ready images:
```bash
npx tsx scripts/download.ts user@example.com avatar@2x.png --size=400
```

## Caching

Downloaded images are cached for 24 hours:
- Same email + parameters = cached file returned
- Different parameters = new download
- `--no-cache` = fresh download

This reduces API calls and bandwidth usage.

## Error Handling

The script will fail if:
- Email is missing or invalid format
- Output file path is missing
- Network errors occur
- Disk write fails

Error messages indicate the specific failure for troubleshooting.

## File Formats

Gravatar serves images in these formats:
- **JPG** - Smaller file size, good for photos
- **PNG** - Better for geometric/generated images (identicon, robohash)
- **WebP** - Modern format, smallest size (when supported)

The file extension in the output path determines the format saved.

## Related

- Use `gravatar-check` skill to verify Gravatar exists before downloading
- Use `gravatar-url` skill to generate URLs for web display
- Combine with npm/GitHub user data to download contributor avatars
