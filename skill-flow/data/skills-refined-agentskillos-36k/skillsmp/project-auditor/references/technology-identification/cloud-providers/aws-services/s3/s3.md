# Amazon S3 (Simple Storage Service)

**Category**: cloud-providers/aws-services
**Description**: Object storage service
**Homepage**: https://aws.amazon.com/s3

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*S3 JavaScript packages*

- `@aws-sdk/client-s3` - S3 SDK v3
- `@aws-sdk/lib-storage` - S3 Upload utility
- `@aws-sdk/s3-request-presigner` - Presigned URLs
- `multer-s3` - Multer S3 storage
- `s3-upload-stream` - Streaming uploads

#### PYPI
*S3 Python packages*

- `boto3` - AWS SDK (includes S3)
- `s3fs` - S3 filesystem interface
- `smart-open` - S3 file streaming
- `django-storages` - Django S3 storage

#### GO
*S3 Go packages*

- `github.com/aws/aws-sdk-go-v2/service/s3` - S3 SDK v2
- `github.com/minio/minio-go` - MinIO client (S3-compatible)

#### MAVEN
*S3 Java packages*

- `software.amazon.awssdk:s3` - SDK v2
- `com.amazonaws:aws-java-sdk-s3` - SDK v1

#### RUBYGEMS
*S3 Ruby packages*

- `aws-sdk-s3` - S3 SDK
- `fog-aws` - Fog AWS provider
- `shrine-s3` - Shrine S3 storage

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-s3['"]`
- S3 SDK v3 import
- Example: `import { S3Client } from '@aws-sdk/client-s3';`

**Pattern**: `from\s+['"]multer-s3['"]`
- Multer S3 import
- Example: `import multerS3 from 'multer-s3';`

#### Python
Extensions: `.py`

**Pattern**: `boto3\.resource\(['"]s3['"]\)|boto3\.client\(['"]s3['"]\)`
- Boto3 S3 resource/client
- Example: `s3 = boto3.client('s3')`

**Pattern**: `^import\s+s3fs`
- S3FS import
- Example: `import s3fs`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/aws/aws-sdk-go-v2/service/s3"`
- S3 Go SDK import
- Example: `import "github.com/aws/aws-sdk-go-v2/service/s3"`

### Code Patterns

**Pattern**: `s3://[a-z0-9.-]+/`
- S3 URI format
- Example: `s3://my-bucket/path/to/file`

**Pattern**: `\.s3\.[a-z0-9-]+\.amazonaws\.com|s3\.amazonaws\.com`
- S3 URLs
- Example: `https://my-bucket.s3.us-east-1.amazonaws.com/file`

**Pattern**: `S3_BUCKET|AWS_S3_BUCKET|S3_REGION`
- S3 environment variables
- Example: `S3_BUCKET=my-bucket`

**Pattern**: `PutObject|GetObject|DeleteObject|ListObjects|HeadObject`
- S3 operations
- Example: `client.send(new PutObjectCommand(...))`

**Pattern**: `arn:aws:s3:::`
- S3 bucket ARN
- Example: `arn:aws:s3:::my-bucket`

**Pattern**: `Type:\s*['"]?AWS::S3::Bucket`
- CloudFormation S3 resource

---

## Environment Variables

- `S3_BUCKET` - S3 bucket name
- `AWS_S3_BUCKET` - Alternative bucket name
- `S3_REGION` - S3 region
- `S3_ENDPOINT` - Custom S3 endpoint (MinIO, etc.)
- `AWS_S3_ENDPOINT_URL` - Endpoint URL

## Detection Notes

- s3:// URIs for S3 paths
- Multiple URL formats (path-style, virtual-hosted)
- MinIO and other S3-compatible services
- Presigned URLs for temporary access
- Multipart uploads for large files

---

## Secrets Detection

### Credentials

See AWS patterns for credential detection. S3 uses standard AWS authentication via IAM.

---

## TIER 3: Configuration Extraction

### Bucket Name Extraction

**Pattern**: `(?:bucket|S3_BUCKET|AWS_S3_BUCKET)\s*[=:]\s*['"]?([a-z0-9.-]{3,63})['"]?`
- S3 bucket name
- Extracts: `bucket_name`
- Example: `S3_BUCKET=my-bucket`

**Pattern**: `s3://([a-z0-9.-]+)/`
- Bucket from S3 URI
- Extracts: `bucket_name`
- Example: `s3://my-bucket/path`

### Region Extraction

**Pattern**: `(?:region|S3_REGION|AWS_REGION)\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9]+)['"]?`
- AWS region
- Extracts: `region`
- Example: `S3_REGION=us-east-1`

### Endpoint Extraction

**Pattern**: `(?:endpoint|S3_ENDPOINT)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- Custom S3 endpoint
- Extracts: `endpoint`
- Example: `S3_ENDPOINT=http://localhost:9000`
