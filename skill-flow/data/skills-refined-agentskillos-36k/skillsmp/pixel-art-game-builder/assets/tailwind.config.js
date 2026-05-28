/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Color Palette (12 colors)
      colors: {
        // Backgrounds
        'bg-darker': '#0a0a0f',
        'bg-dark': '#1a1a2e',
        'bg-medium': '#2d2d44',

        // Text
        'text-muted': '#a0a0a0',
        'text-primary': '#e8e8e8',

        // Accents
        'accent-cyan': '#00fff5',
        'accent-green': '#39ff14',
        'accent-yellow': '#ffd93d',
        'accent-orange': '#ff6b35',
        'accent-pink': '#ff1493',
        'accent-purple': '#9d4edd',
        'accent-red': '#ff4757',
      },

      // Font family
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        sans: ['system-ui', '-apple-system', 'sans-serif'],
      },

      // Animation
      animation: {
        'glow-uncommon': 'glow-uncommon 2s ease-in-out infinite',
        'glow-rare': 'glow-rare 2s ease-in-out infinite',
        'glow-epic': 'glow-epic 2s ease-in-out infinite',
        'glow-legendary': 'glow-legendary 2s ease-in-out infinite',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },

      keyframes: {
        'glow-uncommon': {
          '0%, 100%': { filter: 'drop-shadow(0 0 2px #39ff14)' },
          '50%': { filter: 'drop-shadow(0 0 4px #39ff14)' },
        },
        'glow-rare': {
          '0%, 100%': { filter: 'drop-shadow(0 0 3px #00fff5)' },
          '50%': { filter: 'drop-shadow(0 0 6px #00fff5)' },
        },
        'glow-epic': {
          '0%, 100%': { filter: 'drop-shadow(0 0 4px #9d4edd)' },
          '50%': { filter: 'drop-shadow(0 0 8px #9d4edd)' },
        },
        'glow-legendary': {
          '0%, 100%': {
            filter: 'drop-shadow(0 0 5px #ffd93d) drop-shadow(0 0 10px #ffd93d)',
          },
          '50%': {
            filter: 'drop-shadow(0 0 8px #ffd93d) drop-shadow(0 0 15px #ffd93d)',
          },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },

      // Spacing for pixel-perfect alignment
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },

      // Border radius
      borderRadius: {
        'pixel': '2px',
      },

      // Box shadow for panels
      boxShadow: {
        'panel': '0 4px 6px -1px rgba(0, 0, 0, 0.5)',
        'glow-cyan': '0 0 10px rgba(0, 255, 245, 0.3)',
        'glow-green': '0 0 10px rgba(57, 255, 20, 0.3)',
        'glow-yellow': '0 0 10px rgba(255, 217, 61, 0.3)',
      },
    },
  },
  plugins: [],
};
