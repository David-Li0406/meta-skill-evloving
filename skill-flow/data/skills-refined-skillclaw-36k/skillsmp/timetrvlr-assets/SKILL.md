---
name: timetrvlr-assets
description: Sync timetrvlr public assets (embeddings, index files) to/from S3. Use this skill before deploying to ensure S3 has the latest assets. Invoke with /timetrvlr-assets.
---

# TimeTraveler Asset Management & Deployment

This skill manages the large public assets for timetrvlr_client and handles deployment to AWS Amplify.

## Amplify App Details

| Property | Value |
|----------|-------|
| App ID | `d1t9je67akz719` |
| Branch | `timetrvlr-amplify` |
| Region | `eu-west-2` |
| Live URL | https://timetrvlr-amplify.d1t9je67akz719.amplifyapp.com |

**URL Format**: `https://<branch>.<app-id>.amplifyapp.com`

## Managed Assets

| File | Size | Description |
|------|------|-------------|
| `iiif_no_text_embedding_index.json` | ~25MB | Master index mapping image IDs to metadata |
| `iiif_no_text_embedding_matrix_vlm_embed_ae3d_hires_1.npy` | ~2.5MB | 3D coordinates from AE3D projection |
| `runs/vlm_embed_ae3d_hires_1/ae.pt` | ~6MB | AE3D model checkpoint |

## Commands

### Upload Assets to S3 (Before Deploy)

**IMPORTANT**: Run this before deploying timetrvlr to ensure Amplify has the latest assets.

```bash
cd /home/ubuntu/wc_simd
uv run python aws/upload_to_s3.py --overwrite \
  demos/timetrvlr/timetrvlr_client/public/iiif_no_text_embedding_index.json

uv run python aws/upload_to_s3.py --overwrite \
  demos/timetrvlr/timetrvlr_client/public/iiif_no_text_embedding_matrix_vlm_embed_ae3d_hires_1.npy

uv run python aws/upload_to_s3.py --overwrite \
  runs/vlm_embed_ae3d_hires_1/ae.pt
```

Or use the helper script:
```bash
cd /home/ubuntu/wc_simd/demos/timetrvlr/timetrvlr_client
./scripts/download_data.sh up
```

### Download Assets from S3 (For Local Dev)

```bash
cd /home/ubuntu/wc_simd/demos/timetrvlr/timetrvlr_client
./scripts/download_data.sh down
```

Or individually:
```bash
cd /home/ubuntu/wc_simd
uv run python aws/upload_to_s3.py --download --overwrite \
  demos/timetrvlr/timetrvlr_client/public/iiif_no_text_embedding_index.json
```

### List Current S3 Assets

```bash
cd /home/ubuntu/wc_simd
uv run python aws/upload_to_s3.py --list demos/timetrvlr/timetrvlr_client/public --sizes
```

### Verify Assets Exist Locally

```bash
ls -lh demos/timetrvlr/timetrvlr_client/public/*.json demos/timetrvlr/timetrvlr_client/public/*.npy
```

## S3 Location

- **Bucket**: `wellcomecollection-dsim`
- **Prefix**: `wc_simd/demos/timetrvlr/timetrvlr_client/public/`
- **Full URI**: `s3://wellcomecollection-dsim/wc_simd/demos/timetrvlr/timetrvlr_client/public/`

## How Amplify Uses These Assets

During `amplify.yml` preBuild phase:
1. `sync_public_assets.sh` downloads assets from `ASSET_S3_ROOT`
2. Assets are placed in `public/` directory
3. Next.js build includes them as static files

## Deploy to Amplify

### Full Deploy (Upload Assets + Trigger Build)

```bash
cd /home/ubuntu/wc_simd

# 1. Upload assets to S3
cd demos/timetrvlr/timetrvlr_client && ./scripts/download_data.sh up
cd /home/ubuntu/wc_simd

# 2. Trigger Amplify build
aws amplify start-job \
  --app-id d1t9je67akz719 \
  --branch-name timetrvlr-amplify \
  --job-type RELEASE \
  --region eu-west-2
```

### Monitor Build Status

```bash
# Get latest job status
aws amplify get-job \
  --app-id d1t9je67akz719 \
  --branch-name timetrvlr-amplify \
  --job-id <JOB_ID> \
  --region eu-west-2 \
  --query "job.summary.status" \
  --output text

# List recent jobs
aws amplify list-jobs \
  --app-id d1t9je67akz719 \
  --branch-name timetrvlr-amplify \
  --region eu-west-2 \
  --max-results 5 \
  --query "jobSummaries[].{jobId:jobId,status:status,startTime:startTime}" \
  --output table
```

### Check Build Logs (if build fails)

```bash
aws amplify get-job \
  --app-id d1t9je67akz719 \
  --branch-name timetrvlr-amplify \
  --job-id <JOB_ID> \
  --region eu-west-2 \
  --query "job.steps[].{name:stepName,status:status,logUrl:logUrl}"
```

## Typical Workflow

### After Generating New Embeddings

1. Run AE3D inference to generate new 3D coords:
   ```bash
   ./scripts/infer_ae3d.sh runs/ae3d_*/ae.pt data/vlm_embed/embeddings.npy data/vlm_embed/index.parquet
   ```

2. Upload new assets to S3:
   ```bash
   cd demos/timetrvlr/timetrvlr_client
   ./scripts/download_data.sh up
   ```

3. Trigger Amplify build:
   ```bash
   aws amplify start-job --app-id d1t9je67akz719 --branch-name timetrvlr-amplify --job-type RELEASE --region eu-west-2
   ```

### Quick Deploy (Assets Already Current)

If assets haven't changed, just trigger a rebuild:
```bash
aws amplify start-job --app-id d1t9je67akz719 --branch-name timetrvlr-amplify --job-type RELEASE --region eu-west-2
```

## Troubleshooting

### SSO Session Expired
The upload script auto-handles SSO login. If prompted, complete the browser auth flow.

### Asset Not Found in S3
Check the exact path matches:
```bash
uv run python aws/upload_to_s3.py --list demos/timetrvlr/timetrvlr_client/public --sizes
```

### Amplify Build Fails on Asset Download
Verify `ASSET_S3_ROOT` env var in Amplify matches S3 location, and IAM role has `s3:GetObject` permission.

### Build Stuck or Failed
1. Check build logs:
   ```bash
   aws amplify list-jobs --app-id d1t9je67akz719 --branch-name timetrvlr-amplify --region eu-west-2 --max-results 3
   ```
2. Get detailed step status for failed job:
   ```bash
   aws amplify get-job --app-id d1t9je67akz719 --branch-name timetrvlr-amplify --job-id <JOB_ID> --region eu-west-2
   ```

### Site Not Updating After Deploy
- Clear browser cache or use incognito
- Verify build status is `SUCCEED`
- Check the correct URL: https://timetrvlr-amplify.d1t9je67akz719.amplifyapp.com

---

## Backend Deployment (SageMaker)

### Backend Details

| Property | Value |
|----------|-------|
| Endpoint | `EmbeddingEndpoint-u6w61sZPU1fj` |
| ECR Repo | `760097843905.dkr.ecr.eu-west-2.amazonaws.com/embed-inference` |
| Instance | `ml.g4dn.xlarge` |
| API Gateway | `https://zymevperp0.execute-api.eu-west-2.amazonaws.com/embed` |

### Rebuild and Deploy Backend

When updating the AE3D checkpoint or backend code:

```bash
cd /home/ubuntu/wc_simd/demos/timetrvlr/timetrvlr_backend

# 1. Copy latest AE checkpoint
./copy_ae_ckpt.sh

# 2. ECR login
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 760097843905.dkr.ecr.eu-west-2.amazonaws.com

# 3. Build and push (use --no-cache if dependencies changed)
docker build -t embed-inference:latest .
docker tag embed-inference:latest 760097843905.dkr.ecr.eu-west-2.amazonaws.com/embed-inference:latest
docker push 760097843905.dkr.ecr.eu-west-2.amazonaws.com/embed-inference:latest

# 4. Update SageMaker endpoint (see /deploy skill for full commands)
```

### Known Issues

#### transformers Version Conflict
The GME-Qwen2-VL model requires `transformers<4.52.0`. If you get errors like:
```
transformers<4.52.0 is required but found transformers==4.57.3
```

Fix in `requirements.txt` and `Dockerfile`:
```
transformers>=4.37.0,<4.52.0
```

#### 504 Errors / "Service Unavailable"
**Cause**: SageMaker auto-scaling is set to `MinCapacity=0`, so the endpoint scales to zero after inactivity.

**Check endpoint status**:
```bash
aws sagemaker describe-endpoint --endpoint-name EmbeddingEndpoint-u6w61sZPU1fj --region eu-west-2 --query 'EndpointStatus'
```

If status is "Updating", wait for "InService".

**Fix: Prevent scale-to-zero** (keeps 1 instance always running):
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace sagemaker \
  --resource-id "endpoint/EmbeddingEndpoint-u6w61sZPU1fj/variant/AllTraffic" \
  --scalable-dimension "sagemaker:variant:DesiredInstanceCount" \
  --min-capacity 1 --max-capacity 1 \
  --region eu-west-2
```

**Cost**: ~$380/month for always-on ml.g4dn.xlarge.

#### Test Backend Directly

```bash
# Test API Gateway
curl -X POST "https://zymevperp0.execute-api.eu-west-2.amazonaws.com/embed" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["medical illustration"], "instruction": "Find an image that matches the given text."}'

# Test SageMaker async directly
S3_KEY="test-$(date +%s).json"
echo '{"texts": ["test"], "instruction": "Find an image."}' | aws s3 cp - "s3://embeddingendpointstack-asyncinputbucketc9af2d68-kutlnuucvpqq/$S3_KEY" --region eu-west-2

aws sagemaker-runtime invoke-endpoint-async \
  --endpoint-name EmbeddingEndpoint-u6w61sZPU1fj \
  --content-type application/json \
  --input-location "s3://embeddingendpointstack-asyncinputbucketc9af2d68-kutlnuucvpqq/$S3_KEY" \
  --region eu-west-2
```

### Full Deploy Checklist

1. **Frontend assets** (3D coords, index):
   ```bash
   cd demos/timetrvlr/timetrvlr_client && ./scripts/download_data.sh up
   ```

2. **Backend checkpoint** (if AE3D model changed):
   ```bash
   cd demos/timetrvlr/timetrvlr_backend && ./copy_ae_ckpt.sh
   # Then rebuild and push Docker image
   ```

3. **Trigger Amplify build**:
   ```bash
   aws amplify start-job --app-id d1t9je67akz719 --branch-name timetrvlr-amplify --job-type RELEASE --region eu-west-2
   ```

4. **Update SageMaker** (if backend code/checkpoint changed):
   See `/deploy` skill for SageMaker endpoint update commands.
