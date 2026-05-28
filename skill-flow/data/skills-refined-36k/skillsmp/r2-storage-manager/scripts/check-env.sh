#!/bin/bash

ENV_FILE=".env.local"
REQUIRED_VARS=(
  "R2_ACCESS_KEY_ID"
  "R2_SECRET_ACCESS_KEY"
  "R2_ENDPOINT"
  "R2_BUCKET_NAME"
)

echo "Checking R2 Environment Variables in $ENV_FILE..."

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ $ENV_FILE not found!"
  exit 1
fi

MISSING=0
for var in "${REQUIRED_VARS[@]}"; do
  if grep -q "^$var=" "$ENV_FILE"; then
    echo "✅ $var is set"
  else
    echo "❌ $var is MISSING"
    ((MISSING++))
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "-----------------------------------"
  echo "All R2 variables are present!"
  exit 0
else
  echo "-----------------------------------"
  echo "$MISSING variables are missing. Please update your $ENV_FILE"
  exit 1
fi
