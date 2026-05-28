#!/usr/bin/env bash

# setup-palette-stack.sh - Initialize command palette project dependencies and configuration
# Usage: ./setup-palette-stack.sh [--project-root PATH] [--package-manager npm|pnpm|yarn|bun] [--skip-install] [--with-examples]

set -e

# Default values
PROJECT_ROOT="."
PACKAGE_MANAGER=""
SKIP_INSTALL=false
WITH_EXAMPLES=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --project-root)
      PROJECT_ROOT="$2"
      shift 2
      ;;
    --package-manager)
      PACKAGE_MANAGER="$2"
      shift 2
      ;;
    --skip-install)
      SKIP_INSTALL=true
      shift
      ;;
    --with-examples)
      WITH_EXAMPLES=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--project-root PATH] [--package-manager npm|pnpm|yarn|bun] [--skip-install] [--with-examples]"
      exit 1
      ;;
  esac
done

cd "$PROJECT_ROOT"

echo "🎨 Command Palette Stack Setup"
echo "=============================="
echo

# Detect package manager if not specified
if [ -z "$PACKAGE_MANAGER" ]; then
  if [ -f "pnpm-lock.yaml" ]; then
    PACKAGE_MANAGER="pnpm"
  elif [ -f "yarn.lock" ]; then
    PACKAGE_MANAGER="yarn"
  elif [ -f "bun.lockb" ]; then
    PACKAGE_MANAGER="bun"
  else
    PACKAGE_MANAGER="npm"
  fi
  echo "📦 Detected package manager: $PACKAGE_MANAGER"
else
  echo "📦 Using package manager: $PACKAGE_MANAGER"
fi

# Validate Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "❌ Error: Node.js 18 or higher required (found: $(node -v))"
  echo "   Remediation: Install Node.js 18+ from https://nodejs.org"
  exit 1
fi

# Check for TypeScript
if [ ! -f "tsconfig.json" ]; then
  echo "⚠️  Warning: No tsconfig.json found"
  echo "   This setup assumes a TypeScript project"
  echo "   Remediation: Run 'npx tsc --init' to create tsconfig.json"
  read -p "   Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Install dependencies
if [ "$SKIP_INSTALL" = false ]; then
  echo
  echo "📥 Installing dependencies..."

  DEPS="cmdk @floating-ui/react zustand @tanstack/react-query @tanstack/react-virtual"

  case $PACKAGE_MANAGER in
    npm)
      npm install $DEPS
      ;;
    pnpm)
      pnpm add $DEPS
      ;;
    yarn)
      yarn add $DEPS
      ;;
    bun)
      bun add $DEPS
      ;;
  esac

  echo "✅ Dependencies installed"
else
  echo "⏭️  Skipping dependency installation"
fi

# Validate installed dependencies
echo
echo "🔍 Validating dependencies..."

check_dep() {
  if grep -q "\"$1\"" package.json; then
    echo "  ✅ $1"
  else
    echo "  ❌ $1 - Missing!"
    echo "     Remediation: $PACKAGE_MANAGER add $1"
    return 1
  fi
}

MISSING_DEPS=false
check_dep "cmdk" || MISSING_DEPS=true
check_dep "@floating-ui/react" || MISSING_DEPS=true
check_dep "zustand" || MISSING_DEPS=true
check_dep "@tanstack/react-query" || MISSING_DEPS=true
check_dep "@tanstack/react-virtual" || MISSING_DEPS=true

if [ "$MISSING_DEPS" = true ]; then
  echo
  echo "❌ Some dependencies are missing. Run without --skip-install or install manually."
  exit 1
fi

# Create directories
echo
echo "📁 Creating project structure..."
mkdir -p src/components
mkdir -p src/providers
mkdir -p src/lib
mkdir -p src/styles

# Create ThemeProvider
echo "📝 Creating ThemeProvider..."
cat > src/providers/ThemeProvider.tsx << 'EOF'
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'system';
type ResolvedTheme = 'light' | 'dark';

interface ThemeContextValue {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'system';
    return (localStorage.getItem('theme') as Theme) || 'system';
  });

  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>('light');

  useEffect(() => {
    const getSystemTheme = (): ResolvedTheme => {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    const updateResolvedTheme = () => {
      const resolved = theme === 'system' ? getSystemTheme() : theme;
      setResolvedTheme(resolved);
      document.documentElement.setAttribute('data-theme', resolved);

      if (resolved === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    };

    updateResolvedTheme();

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      if (theme === 'system') {
        updateResolvedTheme();
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
EOF

# Create CommandProvider
echo "📝 Creating CommandProvider..."
cat > src/providers/CommandProvider.tsx << 'EOF'
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { ReactNode } from 'react';

export interface Command {
  id: string;
  label: string;
  description?: string;
  keywords: string[];
  icon?: React.ComponentType;
  shortcut?: string;
  group?: string;
  onSelect: () => void | Promise<void>;
}

interface CommandPaletteState {
  isOpen: boolean;
  setOpen: (open: boolean) => void;
  toggle: () => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  commands: Command[];
  registerCommand: (command: Command) => void;
  unregisterCommand: (id: string) => void;
  registerMultiple: (commands: Command[]) => void;
  recentCommands: string[];
  addToRecent: (id: string) => void;
  favorites: string[];
  toggleFavorite: (id: string) => void;
}

export const useCommandStore = create<CommandPaletteState>()(
  devtools(
    persist(
      (set, get) => ({
        isOpen: false,
        searchQuery: '',
        commands: [],
        recentCommands: [],
        favorites: [],

        setOpen: (open) => set({ isOpen: open }),
        toggle: () => set((state) => ({ isOpen: !state.isOpen })),
        setSearchQuery: (query) => set({ searchQuery: query }),

        registerCommand: (command) =>
          set((state) => ({ commands: [...state.commands, command] })),

        unregisterCommand: (id) =>
          set((state) => ({ commands: state.commands.filter((cmd) => cmd.id !== id) })),

        registerMultiple: (commands) =>
          set((state) => ({ commands: [...state.commands, ...commands] })),

        addToRecent: (id) =>
          set((state) => {
            const filtered = state.recentCommands.filter((cmdId) => cmdId !== id);
            return { recentCommands: [id, ...filtered].slice(0, 10) };
          }),

        toggleFavorite: (id) =>
          set((state) => ({
            favorites: state.favorites.includes(id)
              ? state.favorites.filter((fav) => fav !== id)
              : [...state.favorites, id],
          })),
      }),
      {
        name: 'command-palette-storage',
        partialize: (state) => ({
          recentCommands: state.recentCommands,
          favorites: state.favorites,
        }),
      }
    )
  )
);

export function useCommandPalette() {
  return {
    isOpen: useCommandStore((state) => state.isOpen),
    setOpen: useCommandStore((state) => state.setOpen),
    toggle: useCommandStore((state) => state.toggle),
  };
}

export function useCommandRegistry() {
  return {
    register: useCommandStore((state) => state.registerCommand),
    unregister: useCommandStore((state) => state.unregisterCommand),
    registerMultiple: useCommandStore((state) => state.registerMultiple),
  };
}

export function CommandProvider({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
EOF

# Create base command palette CSS
echo "📝 Creating base styles..."
cat > src/styles/command-palette.css << 'EOF'
/* Command Palette Base Styles */
:root {
  /* Backgrounds */
  --palette-bg: #ffffff;
  --palette-bg-secondary: #f9fafb;
  --palette-selection-bg: #eff6ff;
  --palette-hover-bg: #f3f4f6;

  /* Text */
  --palette-text: #111827;
  --palette-text-muted: #6b7280;
  --palette-text-placeholder: #9ca3af;

  /* Borders */
  --palette-border: #e5e7eb;
  --palette-separator: #f3f4f6;

  /* Accents */
  --palette-accent: #3b82f6;
  --palette-accent-hover: #2563eb;

  /* Shadows */
  --palette-shadow: rgba(0, 0, 0, 0.1);
  --palette-shadow-lg: rgba(0, 0, 0, 0.15);
}

[data-theme="dark"] {
  --palette-bg: #1f2937;
  --palette-bg-secondary: #111827;
  --palette-selection-bg: #374151;
  --palette-hover-bg: #2d3748;
  --palette-text: #f9fafb;
  --palette-text-muted: #9ca3af;
  --palette-text-placeholder: #6b7280;
  --palette-border: #374151;
  --palette-separator: #2d3748;
  --palette-accent: #60a5fa;
  --palette-accent-hover: #3b82f6;
  --palette-shadow: rgba(0, 0, 0, 0.3);
  --palette-shadow-lg: rgba(0, 0, 0, 0.5);
}
EOF

# Update tailwind.config if it exists
if [ -f "tailwind.config.js" ] || [ -f "tailwind.config.ts" ]; then
  echo "📝 Tailwind config detected - add the following to your theme.extend.colors:"
  echo
  echo "  palette: {"
  echo "    bg: 'var(--palette-bg)',"
  echo "    'bg-secondary': 'var(--palette-bg-secondary)',"
  echo "    selection: 'var(--palette-selection-bg)',"
  echo "    text: 'var(--palette-text)',"
  echo "    'text-muted': 'var(--palette-text-muted)',"
  echo "    border: 'var(--palette-border)',"
  echo "    accent: 'var(--palette-accent)',"
  echo "  }"
  echo
fi

echo
echo "✨ Setup complete!"
echo
echo "Next steps:"
echo "  1. Import ThemeProvider and CommandProvider in your app:"
echo "     import { ThemeProvider } from './providers/ThemeProvider';"
echo "     import { CommandProvider } from './providers/CommandProvider';"
echo
echo "  2. Wrap your app:"
echo "     <ThemeProvider><CommandProvider><App /></CommandProvider></ThemeProvider>"
echo
echo "  3. Generate your first command palette:"
echo "     ./scripts/create-command-palette.sh --type modal --name SearchPalette"
echo
