#!/bin/bash

# Setup Tigris object storage for fly.io app
# Usage: ./setup_tigris.sh [--app APP_NAME] [--bucket BUCKET_NAME] [--public]

set -e

APP_NAME=""
BUCKET_NAME=""
PUBLIC_FLAG=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --app)
      APP_NAME="$2"
      shift 2
      ;;
    --bucket)
      BUCKET_NAME="$2"
      shift 2
      ;;
    --public)
      PUBLIC_FLAG="--public"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 --app APP_NAME [--bucket BUCKET_NAME] [--public]"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$APP_NAME" ]; then
  echo "Error: --app APP_NAME is required"
  echo "Usage: $0 --app APP_NAME [--bucket BUCKET_NAME] [--public]"
  exit 1
fi

# Set default bucket name if not provided
if [ -z "$BUCKET_NAME" ]; then
  BUCKET_NAME="${APP_NAME}-storage"
fi

echo "☁️  Setting up Tigris object storage"
echo "   App: $APP_NAME"
echo "   Bucket: $BUCKET_NAME"
echo "   Public: $([ -n "$PUBLIC_FLAG" ] && echo "Yes" || echo "No")"
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
  echo "❌ flyctl is not installed"
  echo "   Install: https://fly.io/docs/flyctl/install/"
  exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
  echo "❌ Not logged in to fly.io"
  echo "   Run: flyctl auth login"
  exit 1
fi

# Check if app exists
if ! flyctl status -a "$APP_NAME" &> /dev/null; then
  echo "❌ App '$APP_NAME' does not exist"
  echo "   Create it first with: flyctl launch"
  exit 1
fi

# Create Tigris bucket
echo "📦 Creating Tigris bucket..."
echo ""

if [ -n "$PUBLIC_FLAG" ]; then
  flyctl storage create --name "$BUCKET_NAME" --app "$APP_NAME" $PUBLIC_FLAG
else
  flyctl storage create --name "$BUCKET_NAME" --app "$APP_NAME"
fi

echo ""
echo "✅ Tigris bucket setup complete!"
echo ""
echo "📋 Connection details:"
echo "   The following secrets have been set on your app:"
echo "   - BUCKET_NAME"
echo "   - AWS_ENDPOINT_URL_S3"
echo "   - AWS_ACCESS_KEY_ID"
echo "   - AWS_SECRET_ACCESS_KEY"
echo ""

if [ -n "$PUBLIC_FLAG" ]; then
  echo "🌍 Public access:"
  echo "   Files are accessible at: https://${BUCKET_NAME}.fly.storage.tigris.dev/<key>"
  echo ""
fi

echo "💡 Usage examples:"
echo ""

echo "   Node.js (AWS SDK v3):"
cat << 'EOF'

   const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

   const s3 = new S3Client({
     region: 'auto',
     endpoint: process.env.AWS_ENDPOINT_URL_S3,
     credentials: {
       accessKeyId: process.env.AWS_ACCESS_KEY_ID,
       secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
     },
   });

   await s3.send(new PutObjectCommand({
     Bucket: process.env.BUCKET_NAME,
     Key: 'file.txt',
     Body: 'Hello World',
   }));
EOF

echo ""
echo "   Python (boto3):"
cat << 'EOF'

   import boto3
   import os

   s3 = boto3.client(
       's3',
       endpoint_url=os.getenv('AWS_ENDPOINT_URL_S3'),
       aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
       aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
       region_name='auto'
   )

   s3.put_object(
       Bucket=os.getenv('BUCKET_NAME'),
       Key='file.txt',
       Body=b'Hello World'
   )
EOF

echo ""
echo "📚 For more details, see: references/data-persistence.md"
