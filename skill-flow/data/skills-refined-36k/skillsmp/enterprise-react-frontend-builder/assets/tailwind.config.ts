import type { Config } from 'tailwindcss'

export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    // Include TakeOff UI components
    './node_modules/@takeoff-ui/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Add your brand colors here
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        // Add custom spacing if needed
      },
      borderRadius: {
        // Add custom border radius
      },
      boxShadow: {
        // Add custom shadows
      },
    },
  },
  plugins: [
    // TakeOff UI Tailwind plugin
    // Uncomment when TakeOff UI provides a Tailwind plugin
    // require('@takeoff-ui/tailwind'),
    
    // Other useful Tailwind plugins
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
  // Dark mode configuration
  darkMode: 'class', // or 'media' for system preference
} satisfies Config