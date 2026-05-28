# Form Styling

Customize form appearance with Markdown, HTML, and media.

## Markdown Support

### Headers

```markdown
# Heading 1
## Heading 2
### Heading 3
```

**Note:** Headers in labels/hints must be single-line.

### Emphasis

```markdown
**bold text**
_italic text_
```

### Links

```markdown
[Click here](https://example.com)
```

### Example

| type | name | label |
|------|------|-------|
| note | intro | # Welcome to the Survey |
| note | instructions | Please answer **all** questions _carefully_. |
| note | help | For help, visit [our website](https://example.com) |

---

## HTML Styling

Limited inline HTML with `<span>` tags (mobile only).

### Colors

```html
<span style="color: red;">Warning text</span>
<span style="color: #FF5733;">Custom color</span>
<span style="color: green;">Success text</span>
```

### Fonts

```html
<span style="font-family: monospace;">Code text</span>
<span style="font-family: serif;">Serif text</span>
```

### Text Alignment

```html
<p style="text-align: center;">Centered text</p>
<p style="text-align: right;">Right-aligned text</p>
```

### Example

| type | name | label |
|------|------|-------|
| note | warning | <span style="color: red;">**Warning:** This action cannot be undone</span> |
| note | code | ID: <span style="font-family: monospace;">${patient_id}</span> |

---

## Platform Limitations

| Feature | ODK Collect | Enketo Web |
|---------|-------------|------------|
| Markdown | Yes | Yes |
| HTML `<span>` | Yes | No |
| Choice label styling | Yes | No |

Always test on target platforms.

---

## Media in Questions

Add images, audio, or video to questions.

### Image Column

| type | name | label | image |
|------|------|-------|-------|
| note | anatomy | Point to the affected area | body_diagram.png |
| select_one body_part | location | Where is the pain? | body_parts.png |

### Audio Column

| type | name | label | audio |
|------|------|-------|-------|
| note | instructions | Listen to the instructions | instructions.mp3 |
| select_one options | response | Select your answer | question_audio.mp3 |

### Video Column

| type | name | label | video |
|------|------|-------|-------|
| note | demo | Watch the demonstration | demo_video.mp4 |

### Autoplay

| type | name | label | audio | autoplay |
|------|------|-------|-------|----------|
| note | welcome | Welcome | welcome.mp3 | audio |

---

## Media in Choices

Add images to choice options.

### Choices Sheet

| list_name | name | label | image |
|-----------|------|-------|-------|
| fruit | apple | Apple | apple.png |
| fruit | banana | Banana | banana.png |
| fruit | orange | Orange | orange.png |

### Survey Sheet

| type | name | label | appearance |
|------|------|-------|------------|
| select_one fruit | favorite | Favorite fruit | |

### Image-Only Display

| type | name | label | appearance |
|------|------|-------|------------|
| select_one fruit | favorite | Select fruit | no-buttons |

---

## Emoji

Emoji supported in labels, hints, and choices.

| type | name | label |
|------|------|-------|
| note | warning | ⚠️ Important Notice |
| note | success | ✅ Form completed successfully |
| note | info | ℹ️ Please read carefully |

### Choices with Emoji

| list_name | name | label |
|-----------|------|-------|
| rating | great | 😊 Great |
| rating | good | 🙂 Good |
| rating | ok | 😐 OK |
| rating | poor | 😞 Poor |

**Note:** Emoji appearance varies by device OS.

---

## Image Best Practices

### Size Guidelines

- Keep images under 200KB
- Use `max-pixels` parameter for photos
- Recommended dimensions: 300x300 for icons

### Format

- PNG for icons/diagrams
- JPEG for photos
- SVG not widely supported

### Organization

Place media files in `form_name-media/` folder:

```
forms/
  app/
    registration.xlsx
    registration-media/
      logo.png
      instructions.mp3
      diagram.png
```

---

## Icons in Labels

Use icon libraries (Phosphor, Google Icons, Health Icons) or Unicode:

| type | name | label |
|------|------|-------|
| note | phone | 📱 Phone Information |
| note | location | 📍 Location Details |
| note | calendar | 📅 Schedule |
| note | person | 👤 Personal Information |

---

## Styling Groups

### Section Headers

| type | name | label |
|------|------|-------|
| begin_group | demographics | # Demographics |
| text | name | Name |
| end_group | | |

### Visual Separators

| type | name | label |
|------|------|-------|
| note | separator | ─────────────────────────── |
| note | section | ## Next Section |

---

## Conditional Styling

Use relevance to show styled notes:

| type | name | label | relevant |
|------|------|-------|----------|
| note | warning | <span style="color: red;">⚠️ **High Risk Patient**</span> | ${risk_score} > 80 |
| note | normal | ✅ Normal risk level | ${risk_score} <= 80 |

---

## Summary Pages

Create formatted summaries at end of form:

| type | name | label | appearance |
|------|------|-------|------------|
| begin_group | summary | Summary | field-list |
| note | s_name | **Name:** ${first_name} ${last_name} | |
| note | s_age | **Age:** ${age} years | |
| note | s_location | **Location:** ${village}, ${district} | |
| note | s_date | **Date:** ${visit_date} | |
| end_group | | | |
