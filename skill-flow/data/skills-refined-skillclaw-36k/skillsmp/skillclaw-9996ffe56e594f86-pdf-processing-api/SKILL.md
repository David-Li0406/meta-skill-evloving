---
name: pdf-processing-api
description: Use this skill when you need to perform various operations on PDF files, such as conversion, extraction, merging, and compression.
---

# Skill body

## When to Use

Use this skill when you need to:

- Convert documents to/from PDF (Word, Excel, PowerPoint, HTML, images)
- Extract text, tables, or images from PDF (with OCR support)
- Merge multiple PDFs into one
- Split PDF into multiple files
- Compress PDF to reduce file size
- Add watermarks, stamps, or page numbers
- Fill PDF forms programmatically
- Protect/unlock PDF with password
- Create barcodes and QR codes

## Prerequisites

1. Create an account at the respective PDF processing service (e.g., PDF4ME or PDF.co).
2. Get your API key from the service dashboard.

Set environment variable:

```bash
export PDF_API_KEY="your-api-key-here"
```

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a known bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### 1. Convert to PDF

Convert Word, Excel, PowerPoint, images to PDF:

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

Write to `/tmp/request.json`:

```json
{
  "urls": [
    "https://example.com/sample1.pdf",
    "https://example.com/sample2.pdf"
  ]
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/merge" --header "x-api-key: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```

### 4. Compress PDF

Compress a PDF to reduce file size:

Write to `/tmp/request.json`:

```json
{
  "url": "https://example.com/sample.pdf"
}
```

```bash
bash -c 'curl --location --request POST "https://api.pdf.co/v1/pdf/compress" --header "x-api-key: ${PDF_API_KEY}" --header "Content-Type: application/json" -d @/tmp/request.json'
```