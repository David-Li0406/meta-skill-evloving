#!/usr/bin/env bash

# create-result-type.sh - Generate typed result component

set -e

TYPE=""
NAME=""
OUTPUT="./src/components/results"

while [[ $# -gt 0 ]]; do
  case $1 in
    --type) TYPE="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$TYPE" ] || [ -z "$NAME" ]; then
  echo "Usage: $0 --type person|file|action|card --name ComponentName"
  exit 1
fi

mkdir -p "$OUTPUT"

cat > "$OUTPUT/${NAME}.tsx" << 'EOF'
import { Command } from 'cmdk';

interface {{NAME}}Props {
  label: string;
  description?: string;
  icon?: React.ReactNode;
}

export function {{NAME}}({ label, description, icon }: {{NAME}}Props) {
  return (
    <Command.Item className="result-item">
      {icon && <span className="result-icon">{icon}</span>}
      <div className="result-content">
        <div className="result-label">{label}</div>
        {description && <div className="result-description">{description}</div>}
      </div>
    </Command.Item>
  );
}
EOF

sed -i '' "s/{{NAME}}/$NAME/g" "$OUTPUT/${NAME}.tsx" 2>/dev/null || sed -i "s/{{NAME}}/$NAME/g" "$OUTPUT/${NAME}.tsx"

echo "✅ Generated $NAME result component at $OUTPUT/${NAME}.tsx"
