---
name: microsoft-code-reference
description: Use this skill when you need to look up Microsoft API references, find working code samples, or verify SDK code correctness while working with Azure SDKs, .NET libraries, or Microsoft APIs.
---

# Microsoft Code Reference

## Tools

| Need                    | Tool                           | Example                                                                 |
| ----------------------- | ------------------------------ | ----------------------------------------------------------------------- |
| API method/class lookup | `microsoft_docs_search`        | `"BlobClient UploadAsync Azure.Storage.Blobs"`                          |
| Working code sample     | `microsoft_code_sample_search` | `query: "upload blob managed identity", language: "python"`             |
| Full API reference      | `microsoft_docs_fetch`         | Fetch URL from `microsoft_docs_search` (for overloads, full signatures) |

## Finding Code Samples

Use `microsoft_code_sample_search` to get official, working examples:

```
microsoft_code_sample_search(query: "upload file to blob storage", language: "csharp")
microsoft_code_sample_search(query: "authenticate with managed identity", language: "python")
microsoft_code_sample_search(query: "send message service bus", language: "javascript")
```

**When to use:**

- Before writing code—find a working pattern to follow.
- After errors—compare your code against a known-good sample.
- Unsure of initialization/setup—samples show complete context.

## API Lookups

```
# Verify method exists (include namespace for precision)
"BlobClient UploadAsync Azure.Storage.Blobs"
"GraphServiceClient Users Microsoft.Graph"

# Find class/interface
"DefaultAzureCredential class Azure.Identity"

# Find correct package
"Azure Blob Storage NuGet package"
"azure-storage-blob pip package"
```

Fetch full page when method has multiple overloads or you need complete parameter details.

## Error Troubleshooting

Use `microsoft_code_sample_search` to find working code samples and compare with your implementation. For specific errors, use `microsoft_docs_search` and `microsoft_docs_fetch`:

| Error Type         | Query                                                     |
|--------------------|-----------------------------------------------------------|
| Method not found    | `"[ClassName] methods [Namespace]"`                      |
| Type not found      | `"[TypeName] NuGet package namespace"`                   |
| Wrong signature     | `"[ClassName] [MethodName] overloads"` → fetch full page |
| Deprecated warning   | `"[OldType] migration v12"`                              |
| Auth failure        | `"DefaultAzureCredential troubleshooting"`                |
| 403 Forbidden error | `"403 error troubleshooting"`                             |