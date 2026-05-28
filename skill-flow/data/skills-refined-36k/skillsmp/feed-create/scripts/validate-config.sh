#!/bin/bash
# Validate feed config with zod schema
set -euo pipefail

YAML_FILE="${1:?Usage: validate-config.sh <yaml-file>}"

if [ ! -f "$YAML_FILE" ]; then
  echo "Error: File not found: $YAML_FILE"
  exit 1
fi

cd ~/Developer/utils/epub

bun run -e "
import { validateFeedConfig } from './schemas/schema.ts';
import { readFileSync } from 'fs';
import { parse } from 'yaml';

const yaml = readFileSync('$YAML_FILE', 'utf8');
const data = parse(yaml);
const result = validateFeedConfig(data);

if (!result.success) {
  console.error('❌ Validation failed:');
  result.error.issues.forEach(issue => {
    console.error(\`  • \${issue.path.join('.')}: \${issue.message}\`);
  });
  process.exit(1);
}

console.log('✓ Valid feed config');
process.exit(0);
"
