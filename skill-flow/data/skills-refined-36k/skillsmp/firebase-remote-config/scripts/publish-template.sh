#!/bin/bash
TOKEN="$1"
PROJECT="$2"
NAMESPACE="$3"
ETAG="$4"
FILE="$5"

# Use default namespace (firebase) if not specified
if [ -z "$NAMESPACE" ] || [ "$NAMESPACE" = "firebase" ]; then
  URL="https://firebaseremoteconfig.googleapis.com/v1/projects/${PROJECT}/remoteConfig"
else
  URL="https://firebaseremoteconfig.googleapis.com/v1/projects/${PROJECT}/namespaces/${NAMESPACE}/remoteConfig"
fi

curl -s -f -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "If-Match: $ETAG" \
  -H "X-Goog-User-Project: $PROJECT" \
  "$URL" \
  --data-binary @"$FILE"
