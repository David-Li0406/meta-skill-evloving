# HTTP Sample Collector Plugin

Demonstrates post-processing hooks to upload suspicious files to a collection server.

## Use Case

Automatically collect samples when THOR finds something suspicious:
- Upload files to a malware analysis server
- Send to SIEM/SOAR for automated response
- Archive samples for later analysis

## Implementation

```go
package main

import (
    "bytes"
    "io"
    "mime/multipart"
    "net/http"

    "github.com/NextronSystems/jsonlog/thorlog/v3"
    "github.com/NextronSystems/thor-plugin"
)

const sampleServerUrl = "http://localhost:8084/upload"

func Init(config thor.Configuration, logger thor.Logger, actions thor.RegisterActions) {
    // Post-processing hook fires on each finding
    actions.AddPostProcessingHook(uploadSample)
    logger.Info("HTTPCollector plugin loaded!")
}

func uploadSample(logger thor.Logger, object thor.MatchedObject) {
    // Only process file findings
    file, isFile := object.Finding.Subject.(*thorlog.File)
    if !isFile {
        return
    }

    // Filter: only upload EXE files (customize as needed)
    if file.MagicHeader != "EXE" {
        return
    }

    // Build multipart form
    body := &bytes.Buffer{}
    writer := multipart.NewWriter(body)

    // Add SHA256 hash field
    hashPart, _ := writer.CreateFormField("sha256")
    hashPart.Write([]byte(file.Hashes.Sha256))

    // Add file content
    filePart, _ := writer.CreateFormFile("file", file.Path)
    io.Copy(filePart, object.Content)

    writer.Close()

    // Send HTTP POST
    request, err := http.NewRequest("POST", sampleServerUrl, body)
    if err != nil {
        logger.Error("Failed to create request", "error", err)
        return
    }
    request.Header.Add("Content-Type", writer.FormDataContentType())

    client := &http.Client{}
    response, err := client.Do(request)
    if err != nil {
        logger.Error("Upload failed", "error", err)
        return
    }
    response.Body.Close()

    logger.Info("Uploaded sample", "sha256", file.Hashes.Sha256, "path", file.Path)
}
```

## Key Techniques

### Post-Processing vs Rule Hooks

| Aspect | AddRuleHook | AddPostProcessingHook |
|--------|-------------|----------------------|
| Trigger | YARA/Sigma match | Finding (scored result) |
| Object | Raw `MatchingObject` | `MatchedObject` with `Finding` |
| Scanner | Yes (can rescan) | No (just Logger) |
| Use case | Parse/extract content | React to findings |

### Accessing Finding Details

```go
// The finding contains full detection details
object.Finding.Score      // Detection score
object.Finding.Module     // Which module detected it
object.Finding.Reasons    // List of detection reasons

// Subject is the scanned object
file, isFile := object.Finding.Subject.(*thorlog.File)
file.Hashes.Sha256
file.Hashes.Md5
file.MagicHeader
file.Path
```

### Filtering Findings

```go
// By file type
if file.MagicHeader != "EXE" { return }

// By score
if object.Finding.Score < 60 { return }

// By module
if object.Finding.Module != "Filescan" { return }
```

### Memory Considerations

The example loads files into memory. For large files or high-volume environments:

```go
// Use io.Pipe for streaming upload
pr, pw := io.Pipe()
writer := multipart.NewWriter(pw)

go func() {
    filePart, _ := writer.CreateFormFile("file", file.Path)
    io.Copy(filePart, object.Content)
    writer.Close()
    pw.Close()
}()

request, _ := http.NewRequest("POST", url, pr)
```

## Sample Server

Simple Go server to receive uploads:

```go
package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
)

func main() {
    http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
        sha256 := r.FormValue("sha256")
        file, _, _ := r.FormFile("file")
        defer file.Close()

        outFile, _ := os.Create(fmt.Sprintf("samples/%s", sha256))
        defer outFile.Close()
        io.Copy(outFile, file)

        fmt.Printf("Received: %s\n", sha256)
        w.WriteHeader(http.StatusOK)
    })

    http.ListenAndServe(":8084", nil)
}
```

## metadata.yml

```yaml
name: HTTPCollector
version: v1.0.0
description: Upload suspicious samples to collection server
author: Nextron Systems
requires_thor: v11.0.0
```

## Packaging

```bash
zip -j httpcollector.zip plugin.go metadata.yml
```
