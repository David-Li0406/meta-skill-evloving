# Datasource Plugin Development

Datasource plugins connect external data sources (cloud storage, documents, databases) to Dify.

## Provider Types

| Type Value | Base Class | Use Case |
|------------|------------|----------|
| `online_drive` | `OnlineDriveDatasource` | S3, Google Drive, Dropbox |
| `online_document` | `OnlineDocumentDatasource` | GitHub, Notion, Confluence |
| `website_crawl` | `WebsiteCrawlDatasource` | Firecrawl, Jina Reader |

## Parameter Types

| Type | Description |
|------|-------------|
| `string` | Text input |
| `number` | Numeric value |
| `boolean` | True/false toggle |
| `select` | Dropdown selection |
| `secret-input` | Encrypted credential input |

## File Structure

```
my-datasource/
├── manifest.yaml                # Plugin manifest
├── main.py                      # Entry point
├── pyproject.toml               # Dependencies (uv)
├── README.md                    # Documentation
├── _assets/
│   └── icon.svg                 # Plugin icon
├── provider/
│   └── {provider_name}.yaml     # Provider config (credentials)
└── datasources/
    ├── {datasource_name}.yaml   # Datasource definition
    └── {datasource_name}.py     # Datasource implementation (Retrieve/RetrieveMany)
```

## manifest.yaml

```yaml
version: 0.0.1
type: plugin
author: your-name
name: my_datasource
label:
  en_US: My Datasource
  zh_Hans: 我的数据源
description:
  en_US: Connect to external storage
icon: icon.svg

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main

plugins:
  datasources:
    - provider/my_datasource.yaml

resource:
  memory: 1048576
  permission:
    tool:
      enabled: false
    model:
      enabled: false
```

## provider.yaml

```yaml
identity:
  author: your-name
  name: my_datasource
  label:
    en_US: My Datasource
    zh_Hans: 我的数据源
  description:
    en_US: Connect to cloud storage
  icon: icon.svg

provider_type: online_drive     # or online_document, website_crawl

help:
  title:
    en_US: Get Access Key
  url:
    en_US: https://console.example.com/

credentials_schema:
  - variable: access_key
    type: secret-input
    required: true
    label:
      en_US: Access Key
    placeholder:
      en_US: Enter your access key

  - variable: secret_key
    type: secret-input
    required: true
    label:
      en_US: Secret Key

  - variable: region
    type: text-input
    required: true
    default: us-east-1
    label:
      en_US: Region

# Optional: OAuth support
oauth_schema:
  client_schema:
    - variable: client_id
      type: secret-input
      required: true
    - variable: client_secret
      type: secret-input
      required: true
  credentials_schema:
    - variable: access_token
      type: secret-input
    - variable: refresh_token
      type: secret-input

datasources:
  - datasources/my_datasource.yaml

extra:
  python:
    source: provider/my_datasource.py
```

## datasource.yaml

```yaml
identity:
  name: my_datasource
  author: your-name
  label:
    en_US: My Datasource
    zh_Hans: 我的数据源

description:
  en_US: Access files from cloud storage

parameters: []

output_schema:
  type: object
  properties:
    file:
      $ref: "https://dify.ai/schemas/v1/file.json"

extra:
  python:
    source: datasources/my_datasource.py
```

## OnlineDrive Implementation (S3, Google Drive)

```python
from collections.abc import Generator
import boto3
from botocore.client import Config
from dify_plugin.interfaces.datasource.online_drive import OnlineDriveDatasource
from dify_plugin.entities.datasource import (
    DatasourceMessage,
    OnlineDriveBrowseFilesRequest,
    OnlineDriveBrowseFilesResponse,
    OnlineDriveDownloadFileRequest,
    OnlineDriveFile,
    OnlineDriveFileBucket,
)

class MyDatasource(OnlineDriveDatasource):
    def _browse_files(
        self, request: OnlineDriveBrowseFilesRequest
    ) -> OnlineDriveBrowseFilesResponse:
        """Browse files in storage"""
        credentials = self.runtime.credentials
        bucket = request.bucket
        prefix = request.prefix or ""
        max_keys = request.max_keys or 100
        next_page = request.next_page_parameters or {}

        # Initialize client
        client = self._get_client(credentials)

        # List buckets if none specified
        if not bucket:
            buckets = client.list_buckets()["Buckets"]
            return OnlineDriveBrowseFilesResponse(
                result=[
                    OnlineDriveFileBucket(
                        bucket=b["Name"],
                        files=[],
                        is_truncated=False,
                        next_page_parameters={}
                    )
                    for b in buckets
                ]
            )

        # List objects in bucket
        params = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": max_keys}
        if next_page.get("continuation_token"):
            params["ContinuationToken"] = next_page["continuation_token"]

        response = client.list_objects_v2(**params)

        # Build file list
        files = []
        for obj in response.get("Contents", []):
            files.append(OnlineDriveFile(
                id=obj["Key"],
                name=obj["Key"].split("/")[-1],
                size=obj["Size"],
                type="file"
            ))

        for prefix_obj in response.get("CommonPrefixes", []):
            files.append(OnlineDriveFile(
                id=prefix_obj["Prefix"],
                name=prefix_obj["Prefix"].rstrip("/").split("/")[-1],
                size=0,
                type="folder"
            ))

        return OnlineDriveBrowseFilesResponse(
            result=[OnlineDriveFileBucket(
                bucket=bucket,
                files=files,
                is_truncated=response.get("IsTruncated", False),
                next_page_parameters={
                    "continuation_token": response.get("NextContinuationToken")
                } if response.get("NextContinuationToken") else {}
            )]
        )

    def _download_file(
        self, request: OnlineDriveDownloadFileRequest
    ) -> Generator[DatasourceMessage, None, None]:
        """Download file content"""
        credentials = self.runtime.credentials
        bucket = request.bucket
        key = request.id

        client = self._get_client(credentials)
        response = client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read()

        yield self.create_blob_message(
            content,
            meta={
                "file_name": key.split("/")[-1],
                "mime_type": response.get("ContentType", "application/octet-stream")
            }
        )

    def _get_client(self, credentials: dict):
        return boto3.client(
            "s3",
            aws_access_key_id=credentials.get("access_key"),
            aws_secret_access_key=credentials.get("secret_key"),
            region_name=credentials.get("region"),
            config=Config(s3={"addressing_style": "path"})
        )
```

## OnlineDocument Implementation (GitHub, Notion)

```python
from typing import Any
import httpx
from dify_plugin.interfaces.datasource.online_document import OnlineDocumentDatasource
from dify_plugin.entities.datasource import (
    DatasourceGetPagesResponse,
    DatasourceGetPageContentRequest,
    DatasourceGetPageContentResponse,
    DatasourcePage,
)

class GitHubDatasource(OnlineDocumentDatasource):
    def _get_pages(self) -> DatasourceGetPagesResponse:
        """List available documents/pages"""
        credentials = self.runtime.credentials
        token = credentials.get("access_token")
        repo = credentials.get("repository")

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get repository contents
        response = httpx.get(
            f"https://api.github.com/repos/{repo}/contents",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        pages = []
        for item in response.json():
            if item["type"] == "file":
                pages.append(DatasourcePage(
                    id=item["path"],
                    title=item["name"],
                    url=item["html_url"],
                    type="file"
                ))

        return DatasourceGetPagesResponse(pages=pages)

    def _get_page_content(
        self, request: DatasourceGetPageContentRequest
    ) -> DatasourceGetPageContentResponse:
        """Fetch document content"""
        credentials = self.runtime.credentials
        token = credentials.get("access_token")
        repo = credentials.get("repository")
        path = request.page_id

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3.raw"
        }

        response = httpx.get(
            f"https://api.github.com/repos/{repo}/contents/{path}",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return DatasourceGetPageContentResponse(
            content=response.text,
            metadata={"path": path}
        )

    def _validate_credentials(self) -> None:
        """Validate credentials"""
        credentials = self.runtime.credentials
        token = credentials.get("access_token")

        response = httpx.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token}"},
            timeout=10
        )
        if response.status_code != 200:
            raise ValueError("Invalid access token")
```

## Provider Validation

```python
from dify_plugin import DatasourceProvider
from dify_plugin.errors.datasource import DatasourceProviderCredentialValidationError

class MyDatasourceProvider(DatasourceProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        """Validate provider credentials"""
        try:
            # Test connection
            client = self._get_client(credentials)
            client.list_buckets()
        except Exception as e:
            raise DatasourceProviderCredentialValidationError(f"Invalid credentials: {e}")
```

## Error Handling

```python
from dify_plugin.errors.datasource import (
    DatasourceInvokeError,                      # General invocation error
    DatasourceProviderCredentialValidationError, # Invalid credentials
)

# Validation error
raise DatasourceProviderCredentialValidationError("Invalid access token")

# Invocation error
raise DatasourceInvokeError("Failed to fetch file")
```

## Message Types

```python
# File content (binary)
yield self.create_blob_message(
    file_bytes,
    meta={
        "file_name": "document.pdf",
        "mime_type": "application/pdf"
    }
)

# Text content
yield self.create_text_message("File content as text")

# JSON data
yield self.create_json_message({
    "title": "Document",
    "content": "..."
})
```

## Pagination

```python
def _browse_files(self, request):
    # Get pagination token from previous request
    continuation_token = request.next_page_parameters.get("continuation_token")

    # ... fetch data ...

    return OnlineDriveBrowseFilesResponse(
        result=[OnlineDriveFileBucket(
            bucket=bucket,
            files=files,
            is_truncated=has_more,
            next_page_parameters={
                "continuation_token": next_token
            } if has_more else {}
        )]
    )
```

## OAuth Support

```yaml
# provider.yaml
oauth_schema:
  client_schema:
    - variable: client_id
      type: secret-input
      required: true
    - variable: client_secret
      type: secret-input
      required: true
  credentials_schema:
    - variable: access_token
      type: secret-input
    - variable: refresh_token
      type: secret-input
```

## Best Practices

1. **Handle pagination** - Implement proper cursor-based pagination
2. **Validate credentials** - Check access before listing files
3. **Set timeouts** - Use reasonable timeouts (30s for list, 120s for download)
4. **Return metadata** - Include file_name and mime_type in blob messages
5. **Handle errors** - Return helpful error messages for common issues
