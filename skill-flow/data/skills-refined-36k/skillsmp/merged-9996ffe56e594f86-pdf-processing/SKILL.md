---
name: pdf-processing
description: Use this skill for comprehensive PDF processing tasks including conversion, extraction, merging, splitting, and compression.
---

# PDF Processing

This skill provides a comprehensive API for various PDF operations, including conversion, extraction, merging, splitting, and compression. It supports OCR for scanned documents and can handle multiple file formats.

> Official docs: [PDF4ME](https://dev.pdf4me.com/apiv2/documentation/) | [PDF.co](https://docs.pdf.co/)

---

## When to Use

Use this skill when you need to:

- Convert documents to/from PDF (Word, Excel, PowerPoint, HTML, images)
- Extract text from PDF files (with OCR support)
- Merge multiple PDFs into one
- Split PDF into multiple files
- Compress PDF to reduce file size
- Convert HTML or URL to PDF
- Parse invoices and documents with AI

---

## Prerequisites

1. Create an account at [PDF4ME](https://dev.pdf4me.com/) or [PDF.co](https://pdf.co/).
2. Get your API key from the respective dashboard.

Set environment variable:

```bash
export PDF_API_KEY="your-api-key-here"
```

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`.

## How to Use

### 1. Convert to PDF

Convert various formats to PDF:

```bash
# Convert a text file to PDF
echo "Hello, PDF!" > /tmp/test.txt
BASE64_CONTENT=$(base64 < /tmp/test.txt)
```

Write to `/tmp/request.json`:

```json
{
  "docContent": "${BASE64_CONTENT}",
  "docName": "test.txt"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdf4me.com/api/v2/ConvertToPdf" --header "Authorization: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json' | jq -r '.docContent' | base64 -d > /tmp/output.pdf
```

### 2. Extract Text from PDF

Extract text from PDF with OCR support:

Write to `/tmp/request.json`:

```json
{
  "url": "https://example.com/sample.pdf",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/to/text" --header "x-api-key: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 3. Merge PDFs

Combine multiple PDFs into one:

```bash
PDF1_BASE64=$(base64 < file1.pdf)
PDF2_BASE64=$(base64 < file2.pdf)
```

Write to `/tmp/request.json`:

```json
{
  "docContent": ["${PDF1_BASE64}", "${PDF2_BASE64}"],
  "docName": "merged.pdf"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdf4me.com/api/v2/Merge" --header "Authorization: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json' | jq -r '.docContent' | base64 -d > merged.pdf
```

### 4. Split PDF

Split PDF by page ranges:

```bash
PDF_BASE64=$(base64 < input.pdf)
```

Write to `/tmp/request.json`:

```json
{
  "docContent": "${PDF_BASE64}",
  "docName": "input.pdf",
  "splitAction": "splitAfterPage",
  "splitAfterPage": 2
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdf4me.com/api/v2/Split" --header "Authorization: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 5. Compress PDF

Reduce PDF file size:

```bash
PDF_BASE64=$(base64 < large.pdf)
```

Write to `/tmp/request.json`:

```json
{
  "docContent": "${PDF_BASE64}",
  "docName": "large.pdf"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.pdf4me.com/api/v2/Compress" --header "Authorization: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json' | jq -r '.docContent' | base64 -d > compressed.pdf
```

### 6. HTML to PDF

Convert HTML content to PDF:

Write to `/tmp/request.json`:

```json
{
  "html": "<h1>Hello World</h1><p>This is a test.</p>",
  "name": "output.pdf"
}
```

Then run:

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/convert/from/html" --header "x-api-key: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 7. AI Invoice Parser

Extract structured data from invoices:

Write to `/tmp/request.json`:

```json
{
  "url": "https://example.com/sample-invoice.pdf",
  "inline": true
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/ai-invoice-parser" --header "x-api-key: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

---

## API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| **Convert** | `/api/v2/ConvertToPdf` | Various formats to PDF |
| | `/pdf/convert/to/text` | PDF to text (OCR supported) |
| | `/pdf/convert/from/html` | HTML to PDF |
| **Merge/Split** | `/api/v2/Merge` | Merge multiple PDFs |
| | `/api/v2/Split` | Split PDF |
| **Optimize** | `/api/v2/Compress` | Compress PDF |
| **AI Parsing** | `/ai-invoice-parser` | AI-powered invoice parsing |

---

## Guidelines

1. **File Size**: Max 20MB per file (varies by plan).
2. **Base64**: All file content must be base64 encoded.
3. **Rate Limits**: Check your plan at the respective service's pricing page.
4. **Output Expiration**: Download results within expiration time (default 60 min).

---

## Resources

- **API Docs**: [PDF4ME](https://dev.pdf4me.com/apiv2/documentation/) | [PDF.co](https://docs.pdf.co/)
- **Postman Collection**: [PDF4ME Postman](https://dev.pdf4me.com/apiv2/documentation/postman/) | [PDF.co Postman](https://docs.pdf.co/)