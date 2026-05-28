---
name: go-storage
description: >
  Blob storage patterns for file persistence. Use when implementing
  storage operations or file management.
  Triggers: storage.System, Store, Retrieve, Delete, Validate, Path,
  atomic writes, path traversal protection, storage keys, filesystem,
  base_path, temp file.
  File patterns: pkg/storage/*.go
---

# Go Storage Patterns

## When This Skill Applies

- Implementing file storage operations
- Adding new storage backends
- Working with storage keys
- Handling file uploads
- Integrating with external tools that need file paths

## Principles

### 1. System Interface

```go
type System interface {
    Store(ctx context.Context, key string, data []byte) error
    Retrieve(ctx context.Context, key string) ([]byte, error)
    Delete(ctx context.Context, key string) error
    Validate(ctx context.Context, key string) (bool, error)
    Path(ctx context.Context, key string) (string, error)
    Start(lc *lifecycle.Coordinator) error
}
```

The `Path` method returns the absolute filesystem path for a storage key, used when external tools need direct file access (e.g., document-context library for PDF rendering).

### 2. Error Types

```go
var (
    ErrNotFound         = errors.New("storage: key not found")
    ErrPermissionDenied = errors.New("storage: permission denied")
    ErrInvalidKey       = errors.New("storage: invalid key")
)
```

### 3. Atomic File Writes

Store uses temp file + rename for crash safety:

```go
func (f *filesystem) Store(ctx context.Context, key string, data []byte) error {
    path, err := f.fullPath(key)
    if err != nil {
        return err
    }

    dir := filepath.Dir(path)
    if err := os.MkdirAll(dir, 0755); err != nil {
        return fmt.Errorf("create directory: %w", err)
    }

    tmpPath := path + ".tmp"
    if err := os.WriteFile(tmpPath, data, 0644); err != nil {
        return fmt.Errorf("write temp file: %w", err)
    }

    if err := os.Rename(tmpPath, path); err != nil {
        os.Remove(tmpPath)
        return fmt.Errorf("rename temp file: %w", err)
    }

    return nil
}
```

### 4. Path Traversal Protection

The `fullPath` helper validates keys and prevents directory traversal:

```go
func (f *filesystem) fullPath(key string) (string, error) {
    if key == "" {
        return "", ErrInvalidKey
    }

    cleaned := filepath.Clean(key)
    if strings.HasPrefix(cleaned, "..") || filepath.IsAbs(cleaned) {
        return "", ErrInvalidKey
    }

    fullPath := filepath.Join(f.basePath, cleaned)

    if !strings.HasPrefix(fullPath, f.basePath) {
        return "", ErrInvalidKey
    }

    return fullPath, nil
}
```

### 5. Delete with Directory Cleanup

Delete removes the file and cleans up empty parent directories (but never the base path):

```go
func (f *filesystem) Delete(ctx context.Context, key string) error {
    path, err := f.fullPath(key)
    if err != nil {
        return err
    }

    dir := filepath.Dir(path)

    if err := os.Remove(path); err != nil {
        if errors.Is(err, fs.ErrNotExist) {
            return nil // Idempotent
        }
        return err
    }

    // Clean up empty parent directory
    if dir != f.basePath && strings.HasPrefix(dir, f.basePath) {
        entries, err := os.ReadDir(dir)
        if err != nil {
            return nil // Log warning, don't fail
        }

        if len(entries) == 0 {
            os.Remove(dir) // Best effort
        }
    }

    return nil
}
```

### 6. Lifecycle Integration

Storage uses OnStartup only (directory creation). No OnShutdown needed for filesystem:

```go
func (f *filesystem) Start(lc *lifecycle.Coordinator) error {
    f.logger.Info("starting storage system", "base_path", f.basePath)

    lc.OnStartup(func() {
        if err := os.MkdirAll(f.basePath, 0755); err != nil {
            f.logger.Error("storage initialization failed", "error", err)
            return
        }
        f.logger.Info("storage directory initialized")
    })

    return nil
}
```

## Patterns

### Storage-First Atomicity

When storing files with database records, store the file first and rollback on DB failure:

```go
func (r *repo) Create(ctx context.Context, data []byte, metadata Metadata) (*Document, error) {
    key := generateStorageKey(metadata)

    // Store file first
    if err := r.storage.Store(ctx, key, data); err != nil {
        return nil, fmt.Errorf("store file: %w", err)
    }

    // Then create database record
    doc, err := repository.WithTx(ctx, r.db, func(tx *sql.Tx) (Document, error) {
        return repository.QueryOne(ctx, tx, insertSQL, args, scanDocument)
    })

    if err != nil {
        // Rollback: delete stored file
        r.storage.Delete(ctx, key)
        return nil, fmt.Errorf("create record: %w", err)
    }

    return &doc, nil
}
```

### Storage Key Generation

```go
func generateStorageKey(docID uuid.UUID, filename string) string {
    return fmt.Sprintf("documents/%s/%s", docID.String(), filename)
}
```

## Anti-Patterns

### Direct File Path Construction

```go
// Bad: Manual path joining without validation
path := filepath.Join(basePath, userProvidedKey)

// Good: Use fullPath helper with traversal protection
path, err := f.fullPath(userProvidedKey)
if err != nil {
    return ErrInvalidKey
}
```

### Non-Atomic Writes

```go
// Bad: Direct write (can leave partial files on crash)
os.WriteFile(path, data, 0644)

// Good: Temp file + rename (atomic)
tmpPath := path + ".tmp"
os.WriteFile(tmpPath, data, 0644)
os.Rename(tmpPath, path)
```
