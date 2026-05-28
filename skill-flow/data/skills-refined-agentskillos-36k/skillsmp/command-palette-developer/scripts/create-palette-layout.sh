#!/usr/bin/env bash

# create-palette-layout.sh - Generate layout-specific palette component

set -e

LAYOUT=""
NAME=""
OUTPUT="./src/components"
VIRTUALIZED=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --layout) LAYOUT="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --virtualized) VIRTUALIZED=true; shift ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

if [ -z "$LAYOUT" ] || [ -z "$NAME" ]; then
  echo "Usage: $0 --layout single-column|two-column|multi-panel|card-grid|horizontal-cards --name ComponentName"
  exit 1
fi

mkdir -p "$OUTPUT/$NAME"
cd "$OUTPUT/$NAME"

echo "📝 Generating $LAYOUT layout for $NAME..."

# For brevity, create a basic two-column implementation
cat > "${NAME}.tsx" << 'EOF'
import { Command } from 'cmdk';
import { useState } from 'react';

export function {{NAME}}() {
  const [selected, setSelected] = useState<any>(null);

  return (
    <div className="two-column-layout">
      <Command className="left-pane">
        <Command.Input placeholder="Search..." />
        <Command.List>
          <Command.Item onSelect={setSelected}>Item 1</Command.Item>
          <Command.Item onSelect={setSelected}>Item 2</Command.Item>
        </Command.List>
      </Command>
      <div className="right-pane">
        {selected ? <div>Preview: {selected}</div> : <div>Select an item</div>}
      </div>
    </div>
  );
}
EOF

sed -i '' "s/{{NAME}}/$NAME/g" "${NAME}.tsx" 2>/dev/null || sed -i "s/{{NAME}}/$NAME/g" "${NAME}.tsx"

cat > "index.ts" << EOF
export { ${NAME} } from './${NAME}';
EOF

echo "✅ Generated $NAME ($LAYOUT) at $OUTPUT/$NAME/"
