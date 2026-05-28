---
name: resize-and-upload-card-image
description: Resize and upload images for vocabulary cards. Use when the user wants to resize and upload an image for a card, process images from a folder, or says "resize and upload [image]" or "upload images from [folder]". Resizes to 500px JPEG, uploads to Pi, and updates the card via API.
---

# Resize and Upload Card Image

This skill resizes and uploads images for vocabulary cards on the Pi.

## Workflow

1. **Identify image(s)** → Find image file(s) to upload
2. **Match to card(s)** → Find card ID by word or use provided ID
3. **Resize image** → Use sips to resize to 500px, convert to JPEG 85%
4. **Upload to Pi** → rsync to ~/learn-language/data/images/
5. **Update card** → PATCH the card with new image_url

## API Configuration

- **Base URL:** `https://learn.rocksbythesea.uk`
- **API Token:** Get from `.env.local` (`API_TOKEN`)
- **Pi Host:** `pi` (ssh alias)
- **Pi Images Path:** `~/learn-language/data/images/`

## Image Specifications

- **Max dimension:** 500px (maintains aspect ratio)
- **Format:** JPEG
- **Quality:** 85%
- **Naming:** `card-{id}-{word}.jpg`

## Step 1: Identify Images

Images can come from:
- Single file: `/path/to/image.png`
- Folder: `/Users/camilarondinini/Documents/project/learn-language/new-image-input/`

List images in the input folder:
```bash
ls -la /Users/camilarondinini/Documents/project/learn-language/new-image-input/*.{png,jpg,jpeg} 2>/dev/null
```

## Step 2: Match to Cards

### Option A: User provides card ID
If user says "upload image for card 123", use that ID directly.

### Option B: Match by filename/word
If image is named `behind.png`, search for a card with "behind" in the back:

```bash
# Search all decks for a word
for id in $(curl -s -H "Authorization: Bearer $API_TOKEN" https://learn.rocksbythesea.uk/api/decks | jq -r '.[].id'); do
  curl -s -H "Authorization: Bearer $API_TOKEN" "https://learn.rocksbythesea.uk/api/decks/$id/cards" | jq -r --arg word "behind" '.[] | select(.back | ascii_downcase | contains($word | ascii_downcase)) | "\(.id) - \(.back)"'
done
```

### Option C: List cards in a deck for user to choose
```bash
curl -s -H "Authorization: Bearer $API_TOKEN" "https://learn.rocksbythesea.uk/api/decks/{deck_id}/cards" | jq -r '.[] | "\(.id) - \(.back)"'
```

## Step 3: Resize Image

Use macOS `sips` to resize and convert:

```bash
# Single image
sips -Z 500 input.png --out card-{id}-{word}.jpg -s format jpeg -s formatOptions 85

# Create resized folder and process
mkdir -p /Users/camilarondinini/Documents/project/learn-language/new-image-input/resized
cd /Users/camilarondinini/Documents/project/learn-language/new-image-input
sips -Z 500 image.png --out resized/card-{id}-{word}.jpg -s format jpeg -s formatOptions 85
```

The `-Z 500` flag resizes to fit within 500x500 while maintaining aspect ratio.

## Step 4: Upload to Pi

```bash
rsync -avz /path/to/card-{id}-{word}.jpg pi:~/learn-language/data/images/
```

For multiple images:
```bash
rsync -avz /Users/camilarondinini/Documents/project/learn-language/new-image-input/resized/card-*.jpg pi:~/learn-language/data/images/
```

## Step 5: Update Card via API

```bash
curl -s -X PATCH \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"image_url":"/api/media/images/card-{id}-{word}.jpg"}' \
  "https://learn.rocksbythesea.uk/api/cards/{id}"
```

## Examples

### Example 1: Single image with known card ID
```
User: upload behind.png for card 121

1. Resize: sips -Z 500 behind.png --out card-121-behind.jpg -s format jpeg -s formatOptions 85
2. Upload: rsync card-121-behind.jpg pi:~/learn-language/data/images/
3. Update: curl -X PATCH ... -d '{"image_url":"/api/media/images/card-121-behind.jpg"}' .../api/cards/121
4. Report: "Uploaded image for card 121 (behind)"
```

### Example 2: Image matched by filename
```
User: upload hospital.png

1. Search cards for "hospital" → Found card 122
2. Resize: sips -Z 500 hospital.png --out card-122-hospital.jpg ...
3. Upload to Pi
4. Update card 122
5. Report: "Uploaded image for card 122 (hospital)"
```

### Example 3: Batch upload from folder
```
User: upload all images from new-image-input

1. List images: behind.png, below.png, hospital.png
2. For each image:
   - Match filename to card (ask user if ambiguous)
   - Resize to resized/card-{id}-{word}.jpg
3. Upload all: rsync resized/card-*.jpg pi:~/learn-language/data/images/
4. Update each card via API
5. Report summary:
   - card 121 (behind)
   - card 119 (below)
   - card 122 (hospital)
```

### Example 4: Ambiguous match
```
User: upload on-top-of.png

1. Search for "on top of" → Found 2 cards:
   - 114: فوقَ (above / on top of)
   - 117: على (on / on top of)
2. Ask user: "Which card should this image go to?"
   - 114: فوقَ - above / on top of (not touching)
   - 117: على - on / on top of (touching)
3. User selects 117
4. Proceed with resize, upload, update
```

## Verify Upload

Check image exists on Pi:
```bash
ssh pi "ls -lah ~/learn-language/data/images/card-{id}*.jpg"
```

Test image URL:
```bash
curl -s -o /dev/null -w '%{http_code}' "https://learn.rocksbythesea.uk/api/media/images/card-{id}-{word}.jpg"
```

## Notes

- Images are stored on Pi at `~/learn-language/data/images/`
- Images are served via `/api/media/images/{filename}`
- Original images in `new-image-input/` are preserved
- Resized images go to `new-image-input/resized/`
- Always confirm card match with user if multiple matches found
- File size typically reduces from ~1.5MB to ~50-150KB after resize
