# Vision Reference

Claude's vision capabilities allow understanding and analyzing images in multimodal interactions.

## Table of Contents

- [Image Sources](#image-sources)
- [Limits and Costs](#limits-and-costs)
- [Code Examples](#code-examples)
- [Best Practices](#best-practices)
- [Limitations](#limitations)
- [FAQ](#faq)

---

## Image Sources

Provide images to Claude in three ways:

### 1. Base64-Encoded

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image_data
                }
            },
            {"type": "text", "text": "Describe this image."}
        ]
    }]
)
```

### 2. URL Reference

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://example.com/image.jpg"
                }
            },
            {"type": "text", "text": "Describe this image."}
        ]
    }]
)
```

### 3. Files API (Beta)

Upload images once, use them multiple times to reduce encoding overhead.

**Python:**

```python
import anthropic

client = anthropic.Anthropic()

# Upload the image file
with open("image.jpg", "rb") as f:
    file_upload = client.beta.files.upload(file=("image.jpg", f, "image/jpeg"))

# Use the uploaded file in a message
message = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    betas=["files-api-2025-04-14"],
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "file",
                    "file_id": file_upload.id
                }
            },
            {"type": "text", "text": "Describe this image."}
        ]
    }]
)
print(message.content)
```

**TypeScript:**

```typescript
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const client = new Anthropic();

// Upload the image file
const fileUpload = await client.beta.files.upload({
  file: toFile(fs.createReadStream("image.jpg"), undefined, { type: "image/jpeg" })
}, {
  betas: ["files-api-2025-04-14"]
});

// Use the uploaded file in a message
const message = await client.beta.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  betas: ["files-api-2025-04-14"],
  messages: [{
    role: "user",
    content: [
      {
        type: "image",
        source: {
          type: "file",
          file_id: fileUpload.id
        }
      },
      { type: "text", text: "Describe this image." }
    ]
  }]
});
console.log(message);
```

**Java:**

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.File;
import com.anthropic.models.files.FileUploadParams;
import com.anthropic.models.messages.*;

public class ImageFilesExample {
    public static void main(String[] args) throws IOException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // Upload the image file
        File file = client.beta().files().upload(FileUploadParams.builder()
            .file(Files.newInputStream(Path.of("image.jpg")))
            .build());

        // Use the uploaded file in a message
        ImageBlockParam imageParam = ImageBlockParam.builder()
            .fileSource(file.id())
            .build();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_4_5_LATEST)
            .maxTokens(1024)
            .addUserMessageOfBlockParams(List.of(
                ContentBlockParam.ofImage(imageParam),
                ContentBlockParam.ofText(TextBlockParam.builder()
                    .text("Describe this image.")
                    .build())
            ))
            .build();

        Message message = client.messages().create(params);
        System.out.println(message.content());
    }
}
```

**cURL:**

```bash
# First, upload your image to the Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@image.jpg"

# Then use the returned file_id in your message
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "file",
            "file_id": "file_abc123"
          }
        },
        {"type": "text", "text": "Describe this image."}
      ]
    }]
  }'
```

---

## Limits and Costs

### Size Limits

| Limit | API | claude.ai |
|-------|-----|-----------|
| **Max file size** | 5MB | 10MB |
| **Max images per request** | 100 | 20 |
| **Max dimensions** | 8000x8000 px | 8000x8000 px |

### Supported Formats

- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

### Token Calculation

For images that don't need resizing:

```
tokens = (width_px × height_px) / 750
```

### Optimal Sizes (No Resizing)

| Aspect Ratio | Max Size | Tokens | Cost (Sonnet 4.5) |
|--------------|----------|--------|-------------------|
| 1:1 | 1092×1092 px | ~1,590 | ~$0.0048 |
| 3:4 | 951×1268 px | ~1,600 | ~$0.0048 |
| 2:3 | 896×1344 px | ~1,600 | ~$0.0048 |
| 9:16 | 819×1456 px | ~1,600 | ~$0.0048 |
| 1:2 | 784×1568 px | ~1,600 | ~$0.0048 |

### Cost Examples (Claude Sonnet 4.5 at $3/MTok)

| Image Size | Tokens | Cost/Image | Cost/1K Images |
|------------|--------|------------|----------------|
| 200×200 px | ~54 | ~$0.00016 | ~$0.16 |
| 1000×1000 px | ~1,334 | ~$0.004 | ~$4.00 |
| 1092×1092 px | ~1,590 | ~$0.0048 | ~$4.80 |

---

## Code Examples

### Single Image

```python
import anthropic
import base64
import httpx

client = anthropic.Anthropic()

# Load and encode image
image_url = "https://example.com/image.jpg"
image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            },
            {"type": "text", "text": "Describe this image."}
        ]
    }]
)
```

### Multiple Images

Label images for clarity when comparing:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Image 1:"},
            {
                "type": "image",
                "source": {"type": "url", "url": "https://example.com/image1.jpg"}
            },
            {"type": "text", "text": "Image 2:"},
            {
                "type": "image",
                "source": {"type": "url", "url": "https://example.com/image2.jpg"}
            },
            {"type": "text", "text": "How are these images different?"}
        ]
    }]
)
```

### With System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="Respond only in Spanish.",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Image 1:"},
            {"type": "image", "source": {"type": "url", "url": image1_url}},
            {"type": "text", "text": "Image 2:"},
            {"type": "image", "source": {"type": "url", "url": image2_url}},
            {"type": "text", "text": "How are these images different?"}
        ]
    }]
)
```

### TypeScript Examples

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// URL-based image
const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: [
      {
        type: "image",
        source: {
          type: "url",
          url: "https://example.com/image.jpg"
        }
      },
      { type: "text", text: "Describe this image." }
    ]
  }]
});

// Base64-encoded image
const imageData = Buffer.from(imageBytes).toString("base64");

const message2 = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{
    role: "user",
    content: [
      {
        type: "image",
        source: {
          type: "base64",
          media_type: "image/jpeg",
          data: imageData
        }
      },
      { type: "text", text: "What's in this image?" }
    ]
  }]
});
```

### Java Examples

```java
import java.io.IOException;
import java.util.Base64;
import java.io.InputStream;
import java.net.URL;
import java.util.List;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.*;

public class VisionExample {
    public static void main(String[] args) throws IOException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        // URL-based image
        List<ContentBlockParam> urlContent = List.of(
            ContentBlockParam.ofImage(
                ImageBlockParam.builder()
                    .source(UrlImageSource.builder()
                        .url("https://example.com/image.jpg")
                        .build())
                    .build()
            ),
            ContentBlockParam.ofText(TextBlockParam.builder()
                .text("Describe this image.")
                .build())
        );

        Message message = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_SONNET_4_5_LATEST)
                .maxTokens(1024)
                .addUserMessageOfBlockParams(urlContent)
                .build()
        );
        System.out.println(message);

        // Base64-encoded image
        String imageData = downloadAndEncodeImage("https://example.com/image.jpg");

        List<ContentBlockParam> base64Content = List.of(
            ContentBlockParam.ofImage(
                ImageBlockParam.builder()
                    .source(Base64ImageSource.builder()
                        .data(imageData)
                        .build())
                    .build()
            ),
            ContentBlockParam.ofText(TextBlockParam.builder()
                .text("What's in this image?")
                .build())
        );

        Message message2 = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_SONNET_4_5_LATEST)
                .maxTokens(1024)
                .addUserMessageOfBlockParams(base64Content)
                .build()
        );
        System.out.println(message2);
    }

    private static String downloadAndEncodeImage(String imageUrl) throws IOException {
        try (InputStream inputStream = new URL(imageUrl).openStream()) {
            return Base64.getEncoder().encodeToString(inputStream.readAllBytes());
        }
    }
}
```

### cURL Example

```bash
# URL-based
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "url",
            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
          }
        },
        {"type": "text", "text": "Describe this image."}
      ]
    }]
  }'

# Base64-encoded
BASE64_IMAGE=$(base64 -i image.jpg)
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "'"$BASE64_IMAGE"'"
          }
        },
        {"type": "text", "text": "Describe this image."}
      ]
    }]
  }'
```

### Multi-Turn Conversations

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Image 1:"},
            {"type": "image", "source": {"type": "url", "url": image1_url}},
            {"type": "text", "text": "Image 2:"},
            {"type": "image", "source": {"type": "url", "url": image2_url}},
            {"type": "text", "text": "How are these images different?"}
        ]
    },
    {
        "role": "assistant",
        "content": "The first image shows an ant, while the second shows a bee..."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Image 1:"},
            {"type": "image", "source": {"type": "url", "url": image3_url}},
            {"type": "text", "text": "Image 2:"},
            {"type": "image", "source": {"type": "url", "url": image4_url}},
            {"type": "text", "text": "Are these similar to the first two?"}
        ]
    }
]

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
```

---

## Best Practices

### Image Placement

Place images **before** text for best results:

```python
# Good: Image first, then question
content = [
    {"type": "image", "source": {...}},
    {"type": "text", "text": "What is this?"}
]

# Works but less optimal: Text first
content = [
    {"type": "text", "text": "Please analyze:"},
    {"type": "image", "source": {...}}
]
```

### Image Quality

1. **Use supported formats**: JPEG, PNG, GIF, WebP
2. **Ensure clarity**: Avoid blurry or pixelated images
3. **Readable text**: If images contain text, ensure it's legible
4. **Proper orientation**: Don't rotate images unnecessarily

### Multiple Images

1. **Label images**: Use "Image 1:", "Image 2:" etc.
2. **No newlines needed**: Between images or between images and prompts
3. **Be specific**: Tell Claude exactly what to compare or analyze

---

## Limitations

| Limitation | Details |
|------------|---------|
| **People identification** | Cannot identify (name) people in images |
| **Accuracy** | May hallucinate with low-quality, rotated, or <200px images |
| **Spatial reasoning** | Limited precision for layouts, clock faces, chess positions |
| **Counting** | Approximate counts only, especially for many small objects |
| **AI-generated images** | Cannot reliably detect synthetic/AI-generated images |
| **Inappropriate content** | Will not process content violating Acceptable Use Policy |
| **Medical imaging** | Not designed for diagnostic CT/MRI interpretation |
| **Image generation** | Cannot create, edit, or manipulate images |

---

## FAQ

**What image formats are supported?**
- JPEG, PNG, GIF, WebP

**What's the maximum file size?**
- API: 5MB per image
- claude.ai: 10MB per image

**How many images per request?**
- API: Up to 100 images
- claude.ai: Up to 20 images per turn

**Does Claude read image metadata?**
- No, Claude does not parse or receive metadata from images

**Are uploaded images stored?**
- No, image uploads are ephemeral and deleted after processing

**Can Claude generate or edit images?**
- No, Claude can only understand and analyze images

**What if Claude's interpretation seems wrong?**
1. Ensure image is clear, high-quality, and correctly oriented
2. Try prompt engineering techniques
3. Provide feedback via thumbs up/down in claude.ai
