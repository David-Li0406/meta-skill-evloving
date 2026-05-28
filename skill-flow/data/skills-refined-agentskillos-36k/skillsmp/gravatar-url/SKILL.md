---
name: gravatar-url
description: Generate a Gravatar avatar URL from an email address. Use when the user asks for a Gravatar URL, wants to generate an avatar from an email, or needs profile image URLs for developers.
---

# Generate Gravatar URL

Generate a Gravatar avatar URL from an email address.

## Usage

```bash
npx tsx scripts/url.ts <email> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `email` | Yes | Email address |

### Options

| Option | Description |
|--------|-------------|
| `--size=N` | Image size in pixels (default: 80, max: 2048) |
| `--default=TYPE` | Default image type: mp, identicon, monsterid, wavatar, retro, robohash, blank (default: mp) |
| `--rating=LEVEL` | Rating level: g, pg, r, x (default: g) |
| `--force-default` | Force the default image even if user has a Gravatar |

### Output

```
Email: user@example.com
Hash: b48bf4373d7b7374351c0544f36f7fc3
URL: https://www.gravatar.com/avatar/b48bf4373d7b7374351c0544f36f7fc3?s=80&d=mp&r=g
```

## Script Execution (Preferred)

```bash
npx tsx scripts/url.ts <email> [options]
```

Options:
- `--size=N` - Image size in pixels (default: 80, max: 2048)
- `--default=TYPE` - Default image type: mp, identicon, monsterid, wavatar, retro, robohash, blank (default: mp)
- `--rating=LEVEL` - Rating level: g, pg, r, x (default: g)
- `--force-default` - Force the default image even if user has a Gravatar

Run from the gravatar plugin directory: `~/.claude/plugins/cache/gravatar/`

## Gravatar URL Format

```
https://www.gravatar.com/avatar/{hash}?{parameters}
```

The hash is an MD5 hash of the lowercase, trimmed email address.

### URL Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `size` | Image size in pixels | 80 | 1-2048 |
| `default` | Default image when no Gravatar exists | mp | mp, identicon, monsterid, wavatar, retro, robohash, blank |
| `rating` | Content rating level | g | g, pg, r, x |
| `f` | Force default image | y (forced) | y |

### Default Image Types

| Type | Description |
|------|-------------|
| `mp` | Mystery Person (simple, cartoon-style silhouette) |
| `identicon` | Geometric pattern based on email hash |
| `monsterid` | Unique monster generated from email hash |
| `wavatar` | Unique face generated from email hash |
| `retro` | 8-bit arcade-style face |
| `robohash` | Unique robot generated from email hash |
| `blank` | Transparent PNG |

### Rating Levels

| Rating | Description |
|--------|-------------|
| `g` | Suitable for all audiences |
| `pg` | May contain rude gestures or mild violence |
| `r` | May contain harsh language, violence, or partial nudity |
| `x` | May contain explicit content |

## Examples

Basic Gravatar URL:
```bash
npx tsx scripts/url.ts user@example.com
```

Custom size (200px):
```bash
npx tsx scripts/url.ts user@example.com --size=200
```

Use identicon for default:
```bash
npx tsx scripts/url.ts user@example.com --default=identicon
```

Force default image (ignore user's Gravatar):
```bash
npx tsx scripts/url.ts user@example.com --force-default --default=robohash
```

## MD5 Hashing

Gravatar uses MD5 hash of the email address:
1. Convert email to lowercase
2. Trim whitespace
3. Compute MD5 hash
4. Use hex-encoded hash in URL

Example:
```
Email:   User@Example.COM
Step 1:  user@example.com
Step 2:  b48bf4373d7b7374351c0544f36f7fc3 (MD5)
URL:     https://www.gravatar.com/avatar/b48bf4373d7b7374351c0544f36f7fc3
```

## Profile URLs

Gravatar also provides profile pages:
```
https://www.gravatar.com/{hash}
```

Replace `/avatar/` with just the hash to get the profile page, which may contain additional information about the user.

## Related

- Use `gravatar-check` skill to verify if a Gravatar exists for an email
- Use `gravatar-download` skill to download Gravatar images to local files
- Use Gravatar profile URLs to get additional user information
- Combine with npm or GitHub author emails to display author avatars
- Use default images to provide consistent fallbacks

## Use Cases

### Developer Profiles
Generate avatar URLs for package maintainers:
```bash
npx tsx scripts/url.ts maintainer@npmjs.com
```

### Team Pages
Create consistent avatars for team members:
```bash
npx tsx scripts/url.ts dev1@company.com --default=identicon --size=200
npx tsx scripts/url.ts dev2@company.com --default=identicon --size=200
```

### User Comments
Display avatars for user comments:
```bash
npx tsx scripts/url.ts commenter@example.com --rating=pg
```

## Notes

- Gravatar images are served over HTTPS
- Images are cached by browsers and CDNs
- URL generation requires no API calls - it's deterministic
- Users must register on gravatar.com to set their avatar
- Unregistered emails will show the default image
