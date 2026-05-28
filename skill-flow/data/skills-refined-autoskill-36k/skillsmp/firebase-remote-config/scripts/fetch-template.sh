#!/bin/bash
TOKEN="$1"
PROJECT="$2"
NAMESPACE="$3"
OUT="$4"

# Use default namespace (firebase) if not specified
if [ -z "$NAMESPACE" ] || [ "$NAMESPACE" = "firebase" ]; then
  URL="https://firebaseremoteconfig.googleapis.com/v1/projects/${PROJECT}/remoteConfig"
else
  URL="https://firebaseremoteconfig.googleapis.com/v1/projects/${PROJECT}/namespaces/${NAMESPACE}/remoteConfig"
fi

curl -s -f -H "Authorization: Bearer $TOKEN" \
  -H "X-Goog-User-Project: $PROJECT" \
  "$URL" \
  -o "$OUT"

