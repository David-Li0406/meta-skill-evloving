#!/usr/bin/env bash

# create-command-palette.sh - Generate command palette component
# Usage: ./create-command-palette.sh --type modal --name SearchPalette [OPTIONS]

set -e

TYPE=""
NAME=""
OUTPUT="./src/components"
THEME="system"
WITH_FOOTER=true
WITH_GROUPS=true

while [[ $# -gt 0 ]]; do
  case $1 in
    --type) TYPE="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --theme) THEME="$2"; shift 2 ;;
    --with-footer) WITH_FOOTER=true; shift ;;
    --no-footer) WITH_FOOTER=false; shift ;;
    --with-groups) WITH_GROUPS=true; shift ;;
    --no-groups) WITH_GROUPS=false; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$TYPE" ] || [ -z "$NAME" ]; then
  echo "Usage: $0 --type modal|embedded|drawer --name ComponentName"
  exit 1
fi

# Validate dependencies
echo "🔍 Validating dependencies..."
if ! grep -q "\"cmdk\"" package.json 2>/dev/null; then
  echo "❌ cmdk not found. Run: npm install cmdk"
  exit 1
fi

mkdir -p "$OUTPUT/$NAME"
cd "$OUTPUT/$NAME"

# Generate component
cat > "${NAME}.tsx" << 'EOF'
import { Command } from 'cmdk';
import { useEffect } from 'react';
import { useCommandStore } from '../../providers/CommandProvider';
import './{{NAME}}.css';

export function {{NAME}}() {
  const isOpen = useCommandStore((state) => state.isOpen);
  const setOpen = useCommandStore((state) => state.setOpen);
  const searchQuery = useCommandStore((state) => state.searchQuery);
  const setSearchQuery = useCommandStore((state) => state.setSearchQuery);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen(!isOpen);
      }
    };

    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [isOpen, setOpen]);

  if (!isOpen) return null;

  return (
    <div className="command-palette-overlay" onClick={() => setOpen(false)}>
      <div className="command-palette-container" onClick={(e) => e.stopPropagation()}>
        <Command className="command-palette">
          <Command.Input
            placeholder="Search commands..."
            value={searchQuery}
            onValueChange={setSearchQuery}
          />
          <Command.List>
            <Command.Empty>No results found</Command.Empty>
            <Command.Group heading="Suggestions">
              <Command.Item>Example Command</Command.Item>
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </div>
  );
}
EOF

sed -i '' "s/{{NAME}}/$NAME/g" "${NAME}.tsx" 2>/dev/null || sed -i "s/{{NAME}}/$NAME/g" "${NAME}.tsx"

# Generate styles
cat > "${NAME}.css" << 'EOF'
.command-palette-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 20vh;
  z-index: 9999;
}

.command-palette-container {
  width: 90%;
  max-width: 640px;
}

.command-palette {
  background: var(--palette-bg);
  border: 1px solid var(--palette-border);
  border-radius: 12px;
  box-shadow: 0 20px 25px var(--palette-shadow-lg);
  overflow: hidden;
}
EOF

cat > "index.ts" << EOF
export { ${NAME} } from './${NAME}';
EOF

echo "✅ Generated $NAME at $OUTPUT/$NAME/"
echo
echo "Usage:"
echo "  import { $NAME } from './components/$NAME';"
echo "  <$NAME />"
