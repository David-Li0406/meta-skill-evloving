#!/usr/bin/env python3
"""
Initialize a new Next.js project with TypeScript, Tailwind CSS, and best practices structure.

Usage:
    python3 init_nextjs_project.py <project-name> [--path <output-directory>]
"""

import argparse
import os
import subprocess
import json
from pathlib import Path


def create_project_structure(project_path: Path):
    """Create the recommended directory structure."""
    directories = [
        "src/app/(routes)",
        "src/app/api",
        "src/components/ui",
        "src/components/features",
        "src/lib",
        "src/hooks",
        "src/types",
        "src/actions",
        "src/services",
    ]
    
    for dir_path in directories:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)


def create_utils_file(project_path: Path):
    """Create the cn utility function."""
    utils_content = '''import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
'''
    utils_path = project_path / "src/lib/utils.ts"
    utils_path.write_text(utils_content)


def create_types_file(project_path: Path):
    """Create base types file."""
    types_content = '''// Base API response types
export type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: ApiError };

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

// Server Action result type
export type ActionResult<T> =
  | { success: true; data: T }
  | { success: false; error: string; fieldErrors?: Record<string, string[]> };

// Common entity types - customize as needed
export interface User {
  id: string;
  name: string;
  email: string;
  image?: string;
  createdAt: Date;
  updatedAt: Date;
}
'''
    types_path = project_path / "src/types/index.ts"
    types_path.write_text(types_content)


def create_env_file(project_path: Path):
    """Create environment validation file."""
    env_content = '''import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  // Add your environment variables here
  // DATABASE_URL: z.string().url(),
  // NEXTAUTH_SECRET: z.string().min(32),
});

const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('❌ Invalid environment variables:', parsed.error.flatten().fieldErrors);
  throw new Error('Invalid environment variables');
}

export const env = parsed.data;
'''
    env_path = project_path / "src/lib/env.ts"
    env_path.write_text(env_content)


def create_sample_component(project_path: Path):
    """Create a sample Button component."""
    button_content = '''import { cva, type VariantProps } from 'class-variance-authority';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground shadow hover:bg-primary/90 active:scale-[0.98]',
        destructive: 'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
        outline: 'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3 text-xs',
        lg: 'h-12 rounded-lg px-8 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export function Button({
  className,
  variant,
  size,
  isLoading = false,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
      {children}
    </button>
  );
}

export { buttonVariants };
'''
    button_path = project_path / "src/components/ui/button.tsx"
    button_path.write_text(button_content)


def create_globals_css(project_path: Path):
    """Create enhanced globals.css with CSS variables."""
    css_content = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
    
    /* Animation easings */
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
'''
    css_path = project_path / "src/app/globals.css"
    if css_path.exists():
        css_path.write_text(css_content)


def update_tailwind_config(project_path: Path):
    """Update tailwind.config.ts with extended configuration."""
    config_content = '''import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out forwards",
        "fade-up": "fadeUp 0.5s ease-out forwards",
        "scale-in": "scaleIn 0.3s ease-out forwards",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        fadeUp: {
          from: { opacity: "0", transform: "translateY(20px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          from: { opacity: "0", transform: "scale(0.9)" },
          to: { opacity: "1", transform: "scale(1)" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
'''
    config_path = project_path / "tailwind.config.ts"
    config_path.write_text(config_content)


def install_dependencies(project_path: Path):
    """Install additional recommended dependencies."""
    dependencies = [
        "clsx",
        "tailwind-merge", 
        "class-variance-authority",
        "lucide-react",
        "zod",
        "@radix-ui/react-slot",
    ]
    
    dev_dependencies = [
        "tailwindcss-animate",
    ]
    
    print("\\n📦 Installing additional dependencies...")
    subprocess.run(
        ["npm", "install"] + dependencies,
        cwd=project_path,
        check=True
    )
    subprocess.run(
        ["npm", "install", "-D"] + dev_dependencies,
        cwd=project_path,
        check=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Next.js project with best practices"
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--path",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip npm install step"
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.path).resolve()
    project_path = output_dir / args.name
    
    print(f"🚀 Creating Next.js project: {args.name}")
    
    # Create Next.js project with create-next-app
    subprocess.run([
        "npx", "create-next-app@latest", args.name,
        "--typescript",
        "--tailwind", 
        "--eslint",
        "--app",
        "--src-dir",
        "--import-alias", "@/*",
        "--no-turbopack",
    ], cwd=output_dir, check=True)
    
    print("\\n📁 Creating project structure...")
    create_project_structure(project_path)
    
    print("📝 Creating utility files...")
    create_utils_file(project_path)
    create_types_file(project_path)
    create_env_file(project_path)
    create_sample_component(project_path)
    create_globals_css(project_path)
    update_tailwind_config(project_path)
    
    if not args.skip_install:
        install_dependencies(project_path)
    
    print(f"""
✅ Project created successfully!

Next steps:
  cd {args.name}
  npm run dev

Project structure:
  src/
  ├── app/           # App Router
  ├── components/
  │   ├── ui/        # Reusable UI components
  │   └── features/  # Feature-specific components
  ├── lib/           # Utilities
  ├── hooks/         # Custom hooks
  ├── types/         # TypeScript types
  ├── actions/       # Server Actions
  └── services/      # API services

Happy coding! 🎨
""")


if __name__ == "__main__":
    main()
