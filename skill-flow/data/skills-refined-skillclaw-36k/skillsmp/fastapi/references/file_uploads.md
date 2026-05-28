# File Upload Patterns in FastAPI

Comprehensive guide for handling file uploads in FastAPI applications.

## Table of Contents

1. [Single File Upload](#single-file-upload)
2. [Multiple File Upload](#multiple-file-upload)
3. [File Validation](#file-validation)
4. [Large File Uploads](#large-file-uploads)
5. [File Storage](#file-storage)
6. [Image Processing](#image-processing)
7. [CSV/Excel Processing](#csvexcel-processing)

---

## Single File Upload

### Basic File Upload

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file."""
    contents = await file.read()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }
```

### Save File to Disk

```python
from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload and save file."""
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "location": str(file_path),
        "size": file_path.stat().st_size
    }
```

### With Metadata

```python
from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    filename: str
    content_type: str
    size: int
    upload_path: str


@app.post("/upload/", response_model=FileUploadResponse)
async def upload_file_with_metadata(file: UploadFile = File(...)):
    """Upload file with detailed response."""
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return FileUploadResponse(
        filename=file.filename,
        content_type=file.content_type,
        size=file_path.stat().st_size,
        upload_path=str(file_path)
    )
```

---

## Multiple File Upload

### Upload Multiple Files

```python
from typing import List


@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files."""
    uploaded_files = []

    for file in files:
        file_path = UPLOAD_DIR / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append({
            "filename": file.filename,
            "size": file_path.stat().st_size
        })

    return {
        "uploaded_count": len(uploaded_files),
        "files": uploaded_files
    }
```

### Limit Number of Files

```python
from fastapi import HTTPException


@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files with limit."""
    MAX_FILES = 10

    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files. Maximum {MAX_FILES} allowed."
        )

    uploaded_files = []
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_files.append(file.filename)

    return {"files": uploaded_files}
```

---

## File Validation

### Validate File Type

```python
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf"}
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/pdf"
}


def validate_file(file: UploadFile):
    """Validate file type and extension."""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Check content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Content type not allowed: {file.content_type}"
        )


@app.post("/upload-validated/")
async def upload_validated_file(file: UploadFile = File(...)):
    """Upload file with validation."""
    validate_file(file)

    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "uploaded"}
```

### Validate File Size

```python
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def validate_file_size(file: UploadFile):
    """Validate file size."""
    # Read file in chunks to check size
    size = 0
    chunk_size = 1024 * 1024  # 1 MB chunks

    while chunk := await file.read(chunk_size):
        size += len(chunk)
        if size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)} MB"
            )

    # Reset file pointer to beginning
    await file.seek(0)
    return size


@app.post("/upload-size-validated/")
async def upload_size_validated_file(file: UploadFile = File(...)):
    """Upload file with size validation."""
    validate_file(file)
    size = await validate_file_size(file)

    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "size": size,
        "status": "uploaded"
    }
```

### Comprehensive Validation

```python
from fastapi import Depends


class FileValidator:
    def __init__(
        self,
        max_size: int = 5 * 1024 * 1024,
        allowed_extensions: set = None,
        allowed_content_types: set = None
    ):
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions or {".jpg", ".png", ".pdf"}
        self.allowed_content_types = allowed_content_types or {
            "image/jpeg", "image/png", "application/pdf"
        }

    async def __call__(self, file: UploadFile = File(...)):
        # Validate extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {self.allowed_extensions}"
            )

        # Validate content type
        if file.content_type not in self.allowed_content_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid content type: {file.content_type}"
            )

        # Validate size
        size = 0
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > self.max_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max: {self.max_size / (1024*1024)} MB"
                )

        await file.seek(0)
        return file


# Use the validator
@app.post("/upload/")
async def upload_file(file: UploadFile = Depends(FileValidator())):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "uploaded"}
```

---

## Large File Uploads

### Stream Large Files

```python
CHUNK_SIZE = 1024 * 1024  # 1 MB


@app.post("/upload-large/")
async def upload_large_file(file: UploadFile = File(...)):
    """Upload large file with streaming."""
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        while chunk := await file.read(CHUNK_SIZE):
            buffer.write(chunk)

    return {
        "filename": file.filename,
        "size": file_path.stat().st_size,
        "status": "uploaded"
    }
```

### With Progress Tracking

```python
from fastapi import BackgroundTasks

# In-memory progress storage (use Redis in production)
upload_progress = {}


async def process_upload(file: UploadFile, upload_id: str):
    """Process upload with progress tracking."""
    file_path = UPLOAD_DIR / file.filename
    total_size = 0

    with file_path.open("wb") as buffer:
        while chunk := await file.read(CHUNK_SIZE):
            buffer.write(chunk)
            total_size += len(chunk)
            upload_progress[upload_id] = {
                "uploaded": total_size,
                "status": "uploading"
            }

    upload_progress[upload_id] = {
        "uploaded": total_size,
        "status": "completed"
    }


@app.post("/upload-with-progress/")
async def upload_with_progress(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Upload file with progress tracking."""
    import uuid
    upload_id = str(uuid.uuid4())

    upload_progress[upload_id] = {"uploaded": 0, "status": "started"}
    background_tasks.add_task(process_upload, file, upload_id)

    return {
        "upload_id": upload_id,
        "message": "Upload started"
    }


@app.get("/upload-progress/{upload_id}")
async def get_upload_progress(upload_id: str):
    """Get upload progress."""
    if upload_id not in upload_progress:
        raise HTTPException(status_code=404, detail="Upload not found")

    return upload_progress[upload_id]
```

---

## File Storage

### Local Storage with Unique Names

```python
import uuid
from datetime import datetime


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    file_ext = Path(original_filename).suffix
    return f"{timestamp}_{unique_id}{file_ext}"


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload file with unique name."""
    unique_filename = generate_unique_filename(file.filename)
    file_path = UPLOAD_DIR / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "path": str(file_path)
    }
```

### Organized Directory Structure

```python
from datetime import datetime


def get_upload_path(filename: str) -> Path:
    """Create organized directory structure by date."""
    today = datetime.now()
    date_path = UPLOAD_DIR / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}"
    date_path.mkdir(parents=True, exist_ok=True)

    unique_filename = generate_unique_filename(filename)
    return date_path / unique_filename


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload file to organized directory."""
    file_path = get_upload_path(file.filename)

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "path": str(file_path.relative_to(UPLOAD_DIR))
    }
```

### Cloud Storage (AWS S3)

```bash
pip install boto3
```

```python
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='us-east-1'
)

BUCKET_NAME = "my-fastapi-uploads"


@app.post("/upload-to-s3/")
async def upload_to_s3(file: UploadFile = File(...)):
    """Upload file to AWS S3."""
    try:
        s3_key = f"uploads/{generate_unique_filename(file.filename)}"

        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.content_type,
                "Metadata": {
                    "original-filename": file.filename
                }
            }
        )

        # Generate presigned URL (valid for 1 hour)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=3600
        )

        return {
            "filename": file.filename,
            "s3_key": s3_key,
            "url": url
        }

    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Image Processing

```bash
pip install pillow
```

### Resize Image

```python
from PIL import Image
from io import BytesIO


@app.post("/upload-image/")
async def upload_and_resize_image(
    file: UploadFile = File(...),
    max_width: int = 800,
    max_height: int = 600
):
    """Upload and resize image."""
    # Validate image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read and process image
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    # Resize while maintaining aspect ratio
    image.thumbnail((max_width, max_height))

    # Save resized image
    output_path = UPLOAD_DIR / f"resized_{file.filename}"
    image.save(output_path)

    return {
        "original_size": f"{image.size}",
        "filename": file.filename,
        "path": str(output_path)
    }
```

### Generate Thumbnail

```python
@app.post("/upload-with-thumbnail/")
async def upload_image_with_thumbnail(file: UploadFile = File(...)):
    """Upload image and generate thumbnail."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    image = Image.open(BytesIO(contents))

    # Save original
    original_path = UPLOAD_DIR / file.filename
    image.save(original_path)

    # Create thumbnail
    thumbnail = image.copy()
    thumbnail.thumbnail((200, 200))
    thumb_path = UPLOAD_DIR / f"thumb_{file.filename}"
    thumbnail.save(thumb_path)

    return {
        "original": str(original_path),
        "thumbnail": str(thumb_path)
    }
```

---

## CSV/Excel Processing

```bash
pip install pandas openpyxl
```

### Process CSV Upload

```python
import pandas as pd
from io import StringIO


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV")

    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode('utf-8')))

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "sample": df.head().to_dict('records')
    }
```

### Process Excel Upload

```python
@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    """Upload and process Excel file."""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be Excel")

    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "summary": df.describe().to_dict()
    }
```

---

## Best Practices

1. **Always validate file types and sizes**
2. **Use unique filenames** to prevent conflicts
3. **Organize files** in directory structures
4. **Stream large files** instead of loading into memory
5. **Limit upload sizes** to prevent DoS
6. **Scan for viruses** in production
7. **Use cloud storage** for scalability
8. **Clean up temporary files**
9. **Add proper error handling**
10. **Implement rate limiting** for uploads

### Complete Example with Best Practices

```python
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pathlib import Path
import shutil
import uuid
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}


class FileUploadService:
    @staticmethod
    def validate_file(file: UploadFile):
        # Validate extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"
            )

    @staticmethod
    def generate_unique_filename(original: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        ext = Path(original).suffix
        return f"{timestamp}_{unique_id}{ext}"

    @staticmethod
    def get_organized_path(filename: str) -> Path:
        today = datetime.now()
        date_path = UPLOAD_DIR / str(today.year) / f"{today.month:02d}"
        date_path.mkdir(parents=True, exist_ok=True)
        return date_path / filename

    async def save_file(self, file: UploadFile) -> dict:
        # Validate
        self.validate_file(file)

        # Generate path
        unique_filename = self.generate_unique_filename(file.filename)
        file_path = self.get_organized_path(unique_filename)

        # Save file
        size = 0
        with file_path.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    file_path.unlink()  # Delete partial file
                    raise HTTPException(
                        status_code=400,
                        detail="File too large"
                    )
                buffer.write(chunk)

        return {
            "filename": file.filename,
            "stored_name": unique_filename,
            "path": str(file_path.relative_to(UPLOAD_DIR)),
            "size": size
        }


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    service: FileUploadService = Depends()
):
    return await service.save_file(file)
```
