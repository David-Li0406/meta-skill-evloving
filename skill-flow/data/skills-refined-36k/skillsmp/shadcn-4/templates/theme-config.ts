/**
 * Tailwind Theme Configuration Template
 *
 * This template extends the default shadcn/ui theme with custom brand colors,
 * fonts, and design tokens. Copy and customize for your project.
 *
 * Usage:
 * 1. Copy this file to your project's tailwind.config.ts
 * 2. Customize the colors, fonts, and other design tokens
 * 3. Update globals.css with matching CSS variables
 */

import type { Config } from "tailwindcss";
import { fontFamily } from "tailwindcss/defaultTheme";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      // ==========================================
      // COLORS - Customize your brand palette here
      // ==========================================
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
        // Custom brand colors (examples)
        brand: {
          50: "hsl(var(--brand-50))",
          100: "hsl(var(--brand-100))",
          200: "hsl(var(--brand-200))",
          300: "hsl(var(--brand-300))",
          400: "hsl(var(--brand-400))",
          500: "hsl(var(--brand-500))",
          600: "hsl(var(--brand-600))",
          700: "hsl(var(--brand-700))",
          800: "hsl(var(--brand-800))",
          900: "hsl(var(--brand-900))",
          950: "hsl(var(--brand-950))",
        },
      },

      // ==========================================
      // TYPOGRAPHY - Custom fonts and sizes
      // ==========================================
      fontFamily: {
        sans: ["var(--font-sans)", ...fontFamily.sans],
        mono: ["var(--font-mono)", ...fontFamily.mono],
        // Add custom fonts
        heading: ["var(--font-heading)", ...fontFamily.sans],
      },
      fontSize: {
        // Custom text sizes if needed
        "2xs": ["0.625rem", { lineHeight: "0.75rem" }],
      },

      // ==========================================
      // BORDER RADIUS - Consistent rounding
      // ==========================================
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },

      // ==========================================
      // ANIMATIONS - Custom keyframes
      // ==========================================
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "fade-out": {
          from: { opacity: "1" },
          to: { opacity: "0" },
        },
        "slide-in-from-top": {
          from: { transform: "translateY(-100%)" },
          to: { transform: "translateY(0)" },
        },
        "slide-in-from-bottom": {
          from: { transform: "translateY(100%)" },
          to: { transform: "translateY(0)" },
        },
        "slide-in-from-left": {
          from: { transform: "translateX(-100%)" },
          to: { transform: "translateX(0)" },
        },
        "slide-in-from-right": {
          from: { transform: "translateX(100%)" },
          to: { transform: "translateX(0)" },
        },
        "scale-in": {
          from: { transform: "scale(0.95)", opacity: "0" },
          to: { transform: "scale(1)", opacity: "1" },
        },
        "spin-slow": {
          from: { transform: "rotate(0deg)" },
          to: { transform: "rotate(360deg)" },
        },
        shimmer: {
          from: { backgroundPosition: "0 0" },
          to: { backgroundPosition: "-200% 0" },
        },
        pulse: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.2s ease-out",
        "fade-out": "fade-out 0.2s ease-out",
        "slide-in-from-top": "slide-in-from-top 0.3s ease-out",
        "slide-in-from-bottom": "slide-in-from-bottom 0.3s ease-out",
        "slide-in-from-left": "slide-in-from-left 0.3s ease-out",
        "slide-in-from-right": "slide-in-from-right 0.3s ease-out",
        "scale-in": "scale-in 0.2s ease-out",
        "spin-slow": "spin-slow 3s linear infinite",
        shimmer: "shimmer 2s linear infinite",
        pulse: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },

      // ==========================================
      // SPACING - Custom spacing values
      // ==========================================
      spacing: {
        // Custom spacing if needed
        "4.5": "1.125rem",
        "5.5": "1.375rem",
      },

      // ==========================================
      // BOX SHADOW - Custom shadows
      // ==========================================
      boxShadow: {
        "inner-sm": "inset 0 1px 2px 0 rgb(0 0 0 / 0.05)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;

/**
 * ==========================================
 * CORRESPONDING CSS VARIABLES (globals.css)
 * ==========================================
 *
 * Add these to your globals.css file:
 *
 * @layer base {
 *   :root {
 *     --background: 0 0% 100%;
 *     --foreground: 222.2 84% 4.9%;
 *     --card: 0 0% 100%;
 *     --card-foreground: 222.2 84% 4.9%;
 *     --popover: 0 0% 100%;
 *     --popover-foreground: 222.2 84% 4.9%;
 *     --primary: 222.2 47.4% 11.2%;
 *     --primary-foreground: 210 40% 98%;
 *     --secondary: 210 40% 96.1%;
 *     --secondary-foreground: 222.2 47.4% 11.2%;
 *     --muted: 210 40% 96.1%;
 *     --muted-foreground: 215.4 16.3% 46.9%;
 *     --accent: 210 40% 96.1%;
 *     --accent-foreground: 222.2 47.4% 11.2%;
 *     --destructive: 0 84.2% 60.2%;
 *     --destructive-foreground: 210 40% 98%;
 *     --border: 214.3 31.8% 91.4%;
 *     --input: 214.3 31.8% 91.4%;
 *     --ring: 222.2 84% 4.9%;
 *     --radius: 0.5rem;
 *
 *     // Brand color scale (customize these)
 *     --brand-50: 220 100% 97%;
 *     --brand-100: 220 100% 94%;
 *     --brand-200: 220 100% 88%;
 *     --brand-300: 220 100% 78%;
 *     --brand-400: 220 100% 66%;
 *     --brand-500: 220 100% 54%;
 *     --brand-600: 220 100% 46%;
 *     --brand-700: 220 100% 38%;
 *     --brand-800: 220 100% 30%;
 *     --brand-900: 220 100% 22%;
 *     --brand-950: 220 100% 14%;
 *   }
 *
 *   .dark {
 *     --background: 222.2 84% 4.9%;
 *     --foreground: 210 40% 98%;
 *     --card: 222.2 84% 4.9%;
 *     --card-foreground: 210 40% 98%;
 *     --popover: 222.2 84% 4.9%;
 *     --popover-foreground: 210 40% 98%;
 *     --primary: 210 40% 98%;
 *     --primary-foreground: 222.2 47.4% 11.2%;
 *     --secondary: 217.2 32.6% 17.5%;
 *     --secondary-foreground: 210 40% 98%;
 *     --muted: 217.2 32.6% 17.5%;
 *     --muted-foreground: 215 20.2% 65.1%;
 *     --accent: 217.2 32.6% 17.5%;
 *     --accent-foreground: 210 40% 98%;
 *     --destructive: 0 62.8% 30.6%;
 *     --destructive-foreground: 210 40% 98%;
 *     --border: 217.2 32.6% 17.5%;
 *     --input: 217.2 32.6% 17.5%;
 *     --ring: 212.7 26.8% 83.9%;
 *   }
 * }
 */
