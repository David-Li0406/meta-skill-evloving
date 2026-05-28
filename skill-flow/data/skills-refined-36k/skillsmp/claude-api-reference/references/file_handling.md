# File Handling Guide

## PDF Document Processing

### Supported Methods

1. **Base64 encoding** (Recommended)
2. **URL reference**
3. **Files API** (Beta - reusable across requests)

### Base64 Complete Example

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Read and encode PDF
with open("document.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "Please analyze the key points of this document"
                }
            ]
        }
    ]
)

print(message.content[0].text)
```

### URL Reference Method

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/document.pdf"
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize this PDF"
                }
            ]
        }
    ]
)
```

### PDF Limits

| Limit | Value |
|-------|-------|
| Max file size | 32 MB |
| Max pages | 100 pages |
| Beyond 100 pages | Text extraction only, no visual analysis |

### Token Calculation

- Text: ~1,500-3,000 tokens per page
- Images: Each page calculated as image tokens
- Use `count_tokens` API to estimate costs

---

## Image Processing

### Supported Formats

- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

### Base64 Method

```python
import base64

with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "Describe this image"
                }
            ]
        }
    ]
)
```

### URL Method

```python
{
    "type": "image",
    "source": {
        "type": "url",
        "url": "https://example.com/image.jpg"
    }
}
```

### Image Limits

| Limit | Value |
|-------|-------|
| Single image max size | 8000 x 8000 px |
| Multi-image per image | 2000 x 2000 px |
| Max images per request | 20 images |
| Recommended optimal size | Long edge ≤ 1568 px |

### Best Practices

1. **Place images before text** - Claude processes better this way
2. **Compress large images** - Images over 1.15 MP will auto-scale
3. **Use PNG** - Lossless format preserves details (tables, charts)

---

## Files API (Beta)

Upload once, reference multiple times:

```python
# Upload file
file = client.files.create(
    file=open("document.pdf", "rb"),
    purpose="user_data"
)

# Reference in message
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file.id
                    }
                },
                {"type": "text", "text": "Analyze this document"}
            ]
        }
    ]
)
```

### Files API Limits

- Max file size: 500 MB
- Default retention: 30 days
- Requires Beta header: `anthropic-beta: files-api-2024-11-08`

---

## Mixed Media Messages

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": chart_data}
                },
                {
                    "type": "text",
                    "text": "Compare the data in the PDF with this chart"
                }
            ]
        }
    ]
)
```