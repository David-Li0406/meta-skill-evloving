#!/bin/bash

# Initialize TypeScript project with linting, formatting, and testing
# Usage: ./init_typescript.sh [--biome|--eslint-prettier]

set -e

TOOLING="ask"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --biome)
            TOOLING="biome"
            shift
            ;;
        --eslint-prettier)
            TOOLING="eslint-prettier"
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--biome|--eslint-prettier]"
            exit 1
            ;;
    esac
done

echo "🚀 Initializing TypeScript project tooling"
echo ""

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ No package.json found. Please run 'npm init' first."
    exit 1
fi

# Detect package manager
if [ -f "pnpm-lock.yaml" ]; then
    PKG_MGR="pnpm"
elif [ -f "yarn.lock" ]; then
    PKG_MGR="yarn"
else
    PKG_MGR="npm"
fi

echo "📦 Using package manager: $PKG_MGR"
echo ""

# Ask about tooling choice if not specified
if [ "$TOOLING" = "ask" ]; then
    echo "Choose linting/formatting approach:"
    echo "  1. Biome (fast, modern, all-in-one)"
    echo "  2. ESLint + Prettier (traditional, extensible)"
    read -p "Choice (1 or 2): " choice

    case $choice in
        1) TOOLING="biome" ;;
        2) TOOLING="eslint-prettier" ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
fi

echo "Using: $TOOLING"
echo ""

# Install dependencies based on choice
if [ "$TOOLING" = "biome" ]; then
    echo "📦 Installing Biome toolchain..."
    $PKG_MGR add -D @biomejs/biome typescript vitest @vitest/ui

    # Create biome.json
    cat > biome.json << 'EOF'
{
  "$schema": "https://biomejs.dev/schemas/1.5.3/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingComma": "es5"
    }
  }
}
EOF
    echo "✓ Created biome.json"

else
    echo "📦 Installing ESLint + Prettier toolchain..."
    $PKG_MGR add -D eslint @eslint/js typescript-eslint prettier \
        eslint-config-prettier eslint-plugin-prettier \
        typescript vitest @vitest/ui

    # Create eslint.config.js
    cat > eslint.config.js << 'EOF'
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import prettierConfig from 'eslint-config-prettier'

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  prettierConfig,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }],
    },
  }
)
EOF
    echo "✓ Created eslint.config.js"

    # Create .prettierrc.json
    cat > .prettierrc.json << 'EOF'
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2
}
EOF
    echo "✓ Created .prettierrc.json"
fi

# Create tsconfig.json
if [ ! -f "tsconfig.json" ]; then
    cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts"]
}
EOF
    echo "✓ Created tsconfig.json"
fi

# Create vitest.config.ts
cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
})
EOF
echo "✓ Created vitest.config.ts"

# Update package.json scripts
echo ""
echo "📝 Updating package.json scripts..."

if [ "$TOOLING" = "biome" ]; then
    SCRIPTS='{
  "dev": "tsc --watch",
  "build": "tsc",
  "lint": "biome lint .",
  "lint:fix": "biome lint --apply .",
  "format": "biome format --write .",
  "format:check": "biome format .",
  "check": "biome check .",
  "check:fix": "biome check --apply .",
  "type-check": "tsc --noEmit",
  "test": "vitest",
  "test:ui": "vitest --ui",
  "test:coverage": "vitest --coverage",
  "validate": "npm run type-check && npm run check && npm test run"
}'
else
    SCRIPTS='{
  "dev": "tsc --watch",
  "build": "tsc",
  "lint": "eslint .",
  "lint:fix": "eslint . --fix",
  "format": "prettier --write .",
  "format:check": "prettier --check .",
  "type-check": "tsc --noEmit",
  "test": "vitest",
  "test:ui": "vitest --ui",
  "test:coverage": "vitest --coverage",
  "validate": "npm run lint && npm run type-check && npm test run"
}'
fi

# Merge scripts (requires jq)
if command -v jq &> /dev/null; then
    jq ".scripts += $SCRIPTS" package.json > package.json.tmp
    mv package.json.tmp package.json
    echo "✓ Added scripts to package.json"
else
    echo "⚠️  jq not found - please add scripts manually"
    echo "$SCRIPTS"
fi

echo ""
echo "✅ TypeScript tooling setup complete!"
echo ""
echo "📋 What was configured:"
if [ "$TOOLING" = "biome" ]; then
    echo "  - Biome (linting + formatting)"
else
    echo "  - ESLint (linting)"
    echo "  - Prettier (formatting)"
fi
echo "  - TypeScript (strict mode)"
echo "  - Vitest (testing)"
echo ""
echo "💡 Next steps:"
echo "  1. Create src/ directory with your code"
echo "  2. Run: $PKG_MGR run dev"
echo "  3. Set up Git hooks: ./scripts/setup_lefthook.sh"
echo ""
echo "📚 See: references/typescript.md for more details"
