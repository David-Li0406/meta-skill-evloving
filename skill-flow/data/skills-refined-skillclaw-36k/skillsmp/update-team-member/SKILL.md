---
name: update-team-member
description: Update team member information and profile photo in the Jekyll academic website
---

## What I do

Update team member information in `_data/team.csv` and manage profile photos in the `assets/images/team/` directory. This includes updating metadata (name, affiliation, title, URL) and replacing or downloading new profile photos.

## Team data file

Location: `_data/team.csv`

CSV format with columns:
- `username` - Unique identifier (kebab-case, used in publications)
- `name` - Full name with proper diacritics
- `affiliation` - Primary institution/organization (displayed on publication pages)
- `title` - Academic or professional title
- `url` - Personal website or profile URL
- `image` - Path to profile photo (local or external URL)

**Important**: The `affiliation` field is displayed on publication detail pages under each author's name, so it should be the primary institution readers would want to know (e.g., "CEU", "LSE", "Bielefeld University and IfW Kiel").

## Profile photo requirements

### Image specifications
- **Size**: 320x320 pixels (square)
- **Format**: JPEG (.jpg)
- **Location**: `assets/images/team/[username].jpg`
- **Aspect ratio**: 1:1 (must not stretch)

### Image processing workflow

1. **Download from external URL** (if applicable):
   ```bash
   curl -s "[URL]" -o assets/images/team/[username]-temp.jpg
   ```

2. **Check original dimensions**:
   ```bash
   sips -g pixelWidth -g pixelHeight assets/images/team/[username]-temp.jpg
   ```

3. **If not square, crop first** (preserve aspect ratio):
   - For portrait photos (height > width): Crop to square keeping face centered
   - For landscape photos (width > height): Crop to square
   - Use image editing tools or ask user to crop manually
   - Save original for user to crop: `assets/images/team/[username].jpg`

4. **If already square or after cropping, resize**:
   ```bash
   sips -z 320 320 assets/images/team/[username].jpg
   ```

5. **Verify final dimensions**:
   ```bash
   file assets/images/team/[username].jpg
   # Should show: JPEG image data ... 320x320
   ```

### Image path conventions

**Prefer local paths**:
- Local: `/assets/images/team/[username].jpg` (recommended)
- External: Full HTTPS URL (avoid - links break over time)

**Migration from external to local**:
When replacing broken external URLs (Google Sites, etc.), always download and save locally.

## Common tasks

### Update basic information

Edit `_data/team.csv` to update:
- Name (ensure proper diacritics)
- Affiliation (primary institution - this is shown on publication pages)
- Title (e.g., "Professor", "Associate Professor", "PhD Candidate")
- URL

**Note**: Since affiliation is displayed on publication detail pages, ensure it accurately represents the person's current primary institution.

### Replace broken photo URL

1. Identify broken external URL (Google Sites, university sites, etc.)
2. Download photo from source or user's website
3. Save original to `assets/images/team/[username].jpg`
4. Let user crop if needed (don't stretch)
5. Resize to 320x320
6. Update CSV with local path: `/assets/images/team/[username].jpg`

### Add new team member

1. Choose username (kebab-case, usually lastname)
2. Add row to `team.csv` with all fields
3. Download and process photo following workflow above
4. Verify photo is 320x320 and not stretched

## Example workflow

```bash
# Download photo
curl -s "https://example.com/photo.jpg" -o assets/images/team/smith.jpg

# Check if square
sips -g pixelWidth -g pixelHeight assets/images/team/smith.jpg

# If not square, user crops manually, then resize
sips -z 320 320 assets/images/team/smith.jpg

# Verify
file assets/images/team/smith.jpg
```

Update CSV:
```csv
smith,John Smith,University Name,Assistant Professor,https://johnsmith.com,/assets/images/team/smith.jpg
```

## Important notes

- **Never stretch images** - Always maintain aspect ratio
- **Crop before resize** - If image is not square, crop first
- **User review** - Let user verify cropped photos before resizing
- **Local storage preferred** - External URLs break over time
- **Proper diacritics** - Ensure names use correct special characters
- **Consistent titles** - Use standard academic titles

## Display on website

- **Publication pages**: Shows author name (linked) and affiliation
- **Team/About pages**: May show name, title, affiliation, and photo

The affiliation field is particularly important as it appears prominently on publication detail pages.

## Verification checklist

- [ ] Photo is 320x320 pixels
- [ ] Photo is not stretched (1:1 aspect ratio)
- [ ] Photo uses local path in CSV
- [ ] All CSV fields are filled correctly
- [ ] Name has proper diacritics
- [ ] Affiliation is current primary institution
- [ ] Title is appropriate and consistent
- [ ] Changes committed to git
