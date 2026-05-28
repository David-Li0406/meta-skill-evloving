# File Upload Handling

## Overview
Handling file uploads in FastAPI efficiently by streaming rather than loading entire files into memory.

## Problem Statement
**File upload anti-patterns:**
- Loading entire file into memory (OOM with large files)
- Not validating file types/size
- No streaming for processing
- Blocking I/O on file operations

## Pattern: Streaming File Uploads

### ❌ Broken (Loads Entire File)
```python
@app.post("/upload")
async def upload_file(file: UploadFile):
    # ❌ Loads entire file into memory!
    content = await file.read()

    # Process entire file in memory
    result = process_in_memory(content)

    return {"size": len(content)}
```

### ✅ Production Pattern
```python
from fastapi import UploadFile
import pandas as pd
import aiofiles

@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    # Stream the file - don't load entirely into memory
    df = pd.read_csv(file.file)

    # Process
    results = process_data_frame(df)

    return {"uploaded": len(results), "data": results}
```

## File Type Handling

### 1. Image Upload
```python
from PIL import Image
import io

@app.post("/upload-image")
async def upload_image(file: UploadFile):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Not an image")

    # Stream process image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Process image
    image.thumbnail((256, 256))

    # Save
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return {"size": len(output.getvalue())}
```

### 2. Large File Streaming
```python
from pathlib import Path

@app.post("/upload-large")
async def upload_large_file(file: UploadFile):
    # Sanitize filename to prevent path traversal
    safe_filename = Path(file.filename).name
    
    # Stream in chunks
    chunk_size = 1024 * 1024  # 1MB chunks
    total_size = 0

    async with aiofiles.open(f"/uploads/{safe_filename}", "wb") as f:
        while chunk := await file.read(chunk_size):
            await f.write(chunk)
            total_size += len(chunk)

    return {"filename": safe_filename, "size": total_size}
```

### 3. Multiple Files
```python
from fastapi import UploadFile, File
from typing import List
from pathlib import Path

@app.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        # Sanitize filename to prevent path traversal
        safe_filename = Path(file.filename).name
        
        # Process each file
        file_path = f"/uploads/{safe_filename}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())

        results.append({
            "filename": safe_filename,
            "content_type": file.content_type
        })

    return {"uploaded": len(results), "files": results}
```

## Validation

### File Type Validation
```python
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json"}
ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/json"
}

@app.post("/upload-data")
async def upload_data(file: UploadFile):
    # Validate extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Extension {ext} not allowed"
        )

    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"MIME type {file.content_type} not allowed"
        )

    # Process file...
```

### File Size Limit
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Check file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {MAX_FILE_SIZE} bytes"
        )

    # Process file...
```

## Async File Operations

```python
import aiofiles
import asyncio

async def process_file_async(file_path: str):
    # Async file read
    async with aiofiles.open(file_path, "r") as f:
        content = await f.read()

    # Process content
    lines = content.splitlines()

    # Async file write
    output_path = file_path + ".processed"
    async with aiofiles.open(output_path, "w") as f:
        for line in lines:
            await f.write(process_line(line) + "\n")

    return output_path
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Loading entire file into memory | OOM with large files | Stream in chunks |
| Not validating file types | Security vulnerability | Check extension + MIME |
| Blocking file I/O | Event loop blocked | Use `aiofiles` |
| No size limits | DoS vulnerability | Enforce max size |
| Synchronous processing | Poor performance | Use async patterns |

## Security Considerations

1. **Validate file extensions** - Prevent executable uploads
2. **Check MIME types** - Double-check with magic bytes
3. **Enforce size limits** - Prevent DoS
4. **Scan for malware** - Use virus scanners in production
5. **Sanitize filenames** - Prevent path traversal

```python
import os

def sanitize_filename(filename: str) -> str:
    # Remove path separators
    filename = os.path.basename(filename)

    # Remove dangerous characters
    filename = "".join(c for c in filename if c.isalnum() or c in "._-")

    # Limit length
    return filename[:255]
```

## Performance Tips

| Optimization | Impact |
|--------------|--------|
| Stream in 1MB chunks | Reduces memory usage 90% |
| Use async I/O | Improves throughput 3x |
| Process in background | Non-blocking for users |
| Compress uploads | Reduces bandwidth |

## See Also
- [Background Tasks](background-tasks.md)
- [Async Conversion](async-conversion.md)
