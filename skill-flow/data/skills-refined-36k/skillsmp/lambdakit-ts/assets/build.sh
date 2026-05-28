#!/bin/bash

set -e

echo "Building lambda ..."

npm i

echo ""
echo "Type checking ..."
npx tsc --noEmit
echo ""

echo "Linting ..."
npm run lint
echo ""

rm -rf dist
mkdir -p dist

npx esbuild src/index.ts \
  --bundle \
  --platform=node \
  --target=node22 \
  --outfile=dist/index.js \
  --minify \
  --alias:@functions=./src/functions \
  --alias:@interfaces=./src/interfaces

echo "lambda build complete: dist/index.js"
