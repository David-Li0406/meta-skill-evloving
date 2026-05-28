#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="reports/security/sbom"
mkdir -p "$OUT_DIR"

# Example command (exact goal may differ by plugin config):
# ./mvnw -q org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom -DoutputDirectory="$OUT_DIR"

echo "Generate CycloneDX SBOM into $OUT_DIR"
