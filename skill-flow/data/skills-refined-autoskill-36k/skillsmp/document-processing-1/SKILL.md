---
name: document-processing
description: >
  Document processing using document-context library. Use when
  working with PDFs or image rendering.
  Triggers: document-context, PDF, page rendering, RenderOptions,
  page range expressions, documents domain, images domain, pdfcpu,
  ImageMagick, brightness, contrast, saturation.
  File patterns: internal/documents/*.go, internal/images/*.go
---

# Document Processing Patterns

## When This Skill Applies

- Working with document uploads
- Rendering PDF pages to images
- Configuring image enhancement options
- Parsing page range expressions
- Managing document/image relationships

## Principles

### 1. Document-Context Integration

The document-context library handles PDF page rendering with ImageMagick:

```go
import "github.com/JaimeStill/document-context/render"

renderer := render.NewImageMagickRenderer()
result, err := renderer.Render(ctx, pdfPath, &render.Options{
    Format:     opts.Format,
    DPI:        opts.DPI,
    Quality:    opts.Quality,
    Brightness: opts.Brightness,
    Contrast:   opts.Contrast,
    Saturation: opts.Saturation,
    Rotation:   opts.Rotation,
    Background: opts.Background,
    Pages:      pages,
})
```

### 2. Page Range Expressions

Flexible syntax for specifying pages:

| Expression | Meaning |
|------------|---------|
| `1` | Single page |
| `1-5` | Range (inclusive) |
| `1,3,5` | Specific pages |
| `1-5,10,15-20` | Mixed |
| `-3` | First 3 pages |
| `5-` | Page 5 to end |

```go
pages, err := ParsePageRange("1-5,10,15-20", maxPage)
// → [1,2,3,4,5,10,15,16,17,18,19,20]
```

### 3. Render Options

Options with ImageMagick neutral defaults:

```go
type RenderOptions struct {
    Format     string  // png, jpeg, webp (default: png)
    DPI        int     // 72-600 (default: 150)
    Quality    int     // 1-100 (default: 90)
    Brightness int     // 0-200 (default: 100 - neutral)
    Contrast   int     // -100 to 100 (default: 0 - neutral)
    Saturation int     // 0-200 (default: 100 - neutral)
    Rotation   int     // 0, 90, 180, 270 (default: 0)
    Background string  // hex color (default: white)
    Pages      string  // page range expression
    Force      bool    // force re-render
}

func (o *RenderOptions) Validate() error {
    // Apply defaults for zero values
    if o.Format == "" { o.Format = "png" }
    if o.DPI == 0 { o.DPI = 150 }
    if o.Quality == 0 { o.Quality = 90 }
    if o.Brightness == 0 { o.Brightness = 100 }
    if o.Saturation == 0 { o.Saturation = 100 }
    if o.Background == "" { o.Background = "white" }

    // Validate bounds
    if o.DPI < 72 || o.DPI > 600 {
        return ErrInvalidDPI
    }
    // ... more validation
    return nil
}
```

### 4. Cross-Domain Dependencies

Images domain depends on documents domain (unidirectional):

```go
func New(
    docs documents.System,  // Domain dependency first
    db *sql.DB,
    storage storage.System,
    logger *slog.Logger,
    pagination pagination.Config,
) System
```

### 5. Image Deduplication

Same render options returns existing image:

```go
// Check for existing image with same parameters
existing, err := r.findByRenderOptions(ctx, docID, page, opts)
if err == nil && existing != nil && !opts.Force {
    return existing, nil  // Return cached
}

// Force flag bypasses deduplication
if opts.Force {
    // Delete existing and re-render
}
```

### 6. Storage Path Pattern

Uses storage.Path() for document-context library access:

```go
// Get filesystem path for document-context
docPath, err := r.storage.Path(ctx, doc.StorageKey)
if err != nil {
    return nil, fmt.Errorf("get document path: %w", err)
}

// Render using absolute path
result, err := renderer.Render(ctx, docPath, renderOpts)
```

## Patterns

### Render Endpoint

```go
func (h *Handler) Render(w http.ResponseWriter, r *http.Request) {
    docIDStr := r.PathValue("documentId")
    docID, err := uuid.Parse(docIDStr)
    if err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }

    var opts RenderOptions
    if r.ContentLength > 0 {
        if err := json.NewDecoder(r.Body).Decode(&opts); err != nil {
            handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
            return
        }
    }

    images, err := h.sys.Render(r.Context(), docID, opts)
    if err != nil {
        handlers.RespondError(w, h.logger, MapHTTPStatus(err), err)
        return
    }

    handlers.RespondJSON(w, http.StatusCreated, images)
}
```

### Binary Data Endpoint

```go
func (h *Handler) Data(w http.ResponseWriter, r *http.Request) {
    idStr := r.PathValue("id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }

    data, contentType, err := h.sys.Data(r.Context(), id)
    if err != nil {
        handlers.RespondError(w, h.logger, MapHTTPStatus(err), err)
        return
    }

    w.Header().Set("Content-Type", contentType)
    w.Header().Set("Content-Length", strconv.Itoa(len(data)))
    w.WriteHeader(http.StatusOK)
    w.Write(data)
}
```

### Page Count Extraction

```go
import "github.com/pdfcpu/pdfcpu/pkg/api"

func extractPageCount(pdfPath string) (int, error) {
    return api.PageCount(pdfPath, nil)
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/images/{documentId}/render` | Render document pages |
| GET | `/api/images` | List images with filters |
| GET | `/api/images/{id}` | Get image metadata |
| GET | `/api/images/{id}/data` | Get raw image binary |
| DELETE | `/api/images/{id}` | Delete image |

## Anti-Patterns

### Rendering Without Validation

```go
// Bad: No validation
result, err := renderer.Render(ctx, path, &render.Options{
    DPI: userInput.DPI,  // Could be invalid
})

// Good: Validate first
if err := opts.Validate(); err != nil {
    return nil, err
}
result, err := renderer.Render(ctx, path, convertToRenderOpts(opts))
```

### Ignoring Deduplication

```go
// Bad: Always re-render
result, err := renderer.Render(ctx, path, opts)

// Good: Check for existing first
existing, err := r.findByRenderOptions(ctx, docID, page, opts)
if existing != nil && !opts.Force {
    return existing, nil
}
```
