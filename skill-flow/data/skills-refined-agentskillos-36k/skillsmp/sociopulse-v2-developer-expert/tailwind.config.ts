import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: 'class',
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            // ===========================================
            // POLYMORPHIC BORDER RADIUS (CSS Variables)
            // ===========================================
            borderRadius: {
                'theme-sm': 'var(--radius-sm)',
                'theme-md': 'var(--radius-md)',
                'theme-lg': 'var(--radius-lg)',
                'theme-xl': 'var(--radius-xl)',
                'theme-2xl': 'var(--radius-2xl)',
                'theme-full': 'var(--radius-full)',
            },

            // ===========================================
            // POLYMORPHIC COLORS (CSS Variables)
            // ===========================================
            colors: {
                // Theme-aware primary color
                primary: {
                    DEFAULT: 'hsl(var(--primary))',
                    50: 'hsl(var(--primary-h) var(--primary-s) 95%)',
                    100: 'hsl(var(--primary-h) var(--primary-s) 90%)',
                    200: 'hsl(var(--primary-h) var(--primary-s) 80%)',
                    300: 'hsl(var(--primary-h) var(--primary-s) 70%)',
                    400: 'hsl(var(--primary-h) var(--primary-s) 60%)',
                    500: 'hsl(var(--primary-h) var(--primary-s) 50%)',
                    600: 'hsl(var(--primary-h) var(--primary-s) var(--primary-l))',
                    700: 'hsl(var(--primary-h) var(--primary-s) 35%)',
                    800: 'hsl(var(--primary-h) var(--primary-s) 25%)',
                    900: 'hsl(var(--primary-h) var(--primary-s) 15%)',
                },
                // Theme-aware secondary color
                secondary: {
                    DEFAULT: 'hsl(var(--secondary))',
                    500: 'hsl(var(--secondary-h) var(--secondary-s) 50%)',
                    600: 'hsl(var(--secondary-h) var(--secondary-s) var(--secondary-l))',
                },
                // Theme-aware accent color
                accent: {
                    DEFAULT: 'hsl(var(--accent))',
                    500: 'hsl(var(--accent-h) var(--accent-s) 50%)',
                    600: 'hsl(var(--accent-h) var(--accent-s) var(--accent-l))',
                },

                // STATIC COLORS (unchanged across themes)
                canvas: "#FAFAFA",

                // Brand (Indigo) - Actions principales, CTA, Login
                brand: {
                    50: "#EEF2FF",
                    100: "#E0E7FF",
                    200: "#C7D2FE",
                    300: "#A5B4FC",
                    400: "#818CF8",
                    500: "#6366F1",
                    600: "#4F46E5",
                    700: "#4338CA",
                    800: "#3730A3",
                    900: "#312E81",
                    DEFAULT: "#4F46E5",
                },
                // Live (Teal) - SocioLive, Visio, Services
                live: {
                    50: "#F0FDFA",
                    100: "#CCFBF1",
                    200: "#99F6E4",
                    300: "#5EEAD4",
                    400: "#2DD4BF",
                    500: "#14B8A6",
                    600: "#0D9488",
                    700: "#0F766E",
                    800: "#115E59",
                    900: "#134E4A",
                    DEFAULT: "#14B8A6",
                },
                // Alert (Rose) - Missions SOS, Urgences
                alert: {
                    50: "#FFF1F2",
                    100: "#FFE4E6",
                    200: "#FECDD3",
                    300: "#FDA4AF",
                    400: "#FB7185",
                    500: "#F43F5E",
                    600: "#E11D48",
                    700: "#BE123C",
                    800: "#9F1239",
                    900: "#881337",
                    DEFAULT: "#F43F5E",
                },
                gray: {
                    50: "#F9FAFB",
                    100: "#F3F4F6",
                    200: "#E5E7EB",
                    300: "#D1D5DB",
                    400: "#9CA3AF",
                    500: "#6B7280",
                    600: "#4B5563",
                    700: "#374151",
                    800: "#1F2937",
                    900: "#111827",
                },
            },

            // ===========================================
            // POLYMORPHIC SPACING (CSS Variables)
            // ===========================================
            spacing: {
                'card': 'var(--spacing-card)',
                'section': 'var(--spacing-section)',
            },

            // ===========================================
            // POLYMORPHIC SHADOWS (CSS Variables)
            // ===========================================
            boxShadow: {
                'theme-sm': 'var(--shadow-sm)',
                'theme-md': 'var(--shadow-md)',
                'theme-lg': 'var(--shadow-lg)',
                'theme-glow': 'var(--shadow-glow-lg)',
                // Static shadows
                soft: "0 4px 16px -4px rgba(0, 0, 0, 0.08)",
                "soft-lg": "0 8px 32px -8px rgba(0, 0, 0, 0.12)",
                // Aurora Glow shadows
                "glow-sm": "0 0 20px -5px var(--glow-primary)",
                "glow-md": "0 0 40px -10px var(--glow-primary), 0 0 20px -5px var(--glow-secondary)",
                "glow-lg": "0 0 60px -15px var(--glow-primary), 0 0 40px -10px var(--glow-secondary)",
                // Glass panel shadows
                "glass": "0 8px 32px -8px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.1)",
            },

            fontFamily: {
                sans: ["Outfit", "Inter", "system-ui", "sans-serif"],
            },
            animation: {
                "modal-in": "modalIn 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
            },
            keyframes: {
                modalIn: {
                    "0%": { opacity: "0", transform: "scale(0.96)" },
                    "100%": { opacity: "1", transform: "scale(1)" },
                },
            },
        },
    },
    plugins: [],
};

export default config;
