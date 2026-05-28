#!/bin/bash
TOKEN="$1"
PROJECT="$2"
NAMESPACE="$3"
VERSION="$4"

# Use default namespace (firebase) if not specified
if [ -z "$NAMESPACE" ] || [ "$NAMESPACE" = "firebase" ]; then
  URL="https://firebaseremoteconfig.googleapis.com/v1/projects/${PROJECT}/remoteConfig:rollback"
else
  URL="https://firebaseremoteconfig.googleapis.com/v1/projects/${PROJECT}/namespaces/${NAMESPACE}/remoteConfig:rollback"
fi

curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: $PROJECT" \
  "$URL" \
  -d "{\"version_number\":${VERSION}}"
