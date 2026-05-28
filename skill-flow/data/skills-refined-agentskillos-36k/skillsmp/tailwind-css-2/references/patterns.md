# Tailwind CSS

## Patterns


---
  #### **Name**
Responsive Design
  #### **Description**
Mobile-first responsive layouts
  #### **When**
Any layout that needs to adapt
  #### **Example**
    # RESPONSIVE DESIGN:
    
    """
    Mobile-first with breakpoint prefixes.
    sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px
    """
    
    <!-- Mobile-first card -->
    <div class="
      p-4 md:p-6 lg:p-8
      grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
      gap-4 md:gap-6
    ">
      <div class="
        bg-white dark:bg-gray-800
        rounded-lg shadow-md
        p-4 md:p-6
      ">
        <h2 class="
          text-lg md:text-xl lg:text-2xl
          font-bold
        ">
          Card Title
        </h2>
        <p class="
          text-sm md:text-base
          text-gray-600 dark:text-gray-300
          mt-2
        ">
          Card content that adapts to screen size.
        </p>
      </div>
    </div>
    
    
    <!-- Responsive navigation -->
    <nav class="
      flex flex-col md:flex-row
      items-center
      justify-between
      p-4
    ">
      <div class="
        w-full md:w-auto
        text-center md:text-left
        mb-4 md:mb-0
      ">
        Logo
      </div>
      <div class="
        hidden md:flex
        gap-4
      ">
        <a href="#">Home</a>
        <a href="#">About</a>
      </div>
    </nav>
    

---
  #### **Name**
Dark Mode
  #### **Description**
Dark mode support with Tailwind
  #### **When**
Sites that support dark/light themes
  #### **Example**
    # DARK MODE:
    
    """
    Use dark: prefix for dark mode styles.
    Configure in tailwind.config.js with 'class' or 'media'.
    """
    
    // tailwind.config.js
    module.exports = {
      darkMode: 'class', // or 'media' for system preference
      // ...
    }
    
    
    <!-- Component with dark mode -->
    <div class="
      bg-white dark:bg-gray-900
      text-gray-900 dark:text-white
      border border-gray-200 dark:border-gray-700
      rounded-lg p-6
      shadow-md dark:shadow-gray-900/50
    ">
      <h2 class="
        text-xl font-bold
        text-gray-900 dark:text-white
      ">
        Dark Mode Ready
      </h2>
      <p class="
        text-gray-600 dark:text-gray-300
        mt-2
      ">
        This component adapts to dark mode automatically.
      </p>
      <button class="
        mt-4 px-4 py-2
        bg-blue-600 hover:bg-blue-700
        dark:bg-blue-500 dark:hover:bg-blue-600
        text-white font-medium
        rounded-md
        transition-colors
      ">
        Click Me
      </button>
    </div>
    
    
    // React dark mode toggle
    function ThemeToggle() {
      const [dark, setDark] = useState(false);
    
      useEffect(() => {
        document.documentElement.classList.toggle('dark', dark);
      }, [dark]);
    
      return (
        <button onClick={() => setDark(!dark)}>
          {dark ? '🌞' : '🌙'}
        </button>
      );
    }
    

---
  #### **Name**
Component Extraction
  #### **Description**
When and how to extract Tailwind components
  #### **When**
Repeated patterns need abstraction
  #### **Example**
    # COMPONENT EXTRACTION:
    
    """
    Extract when you repeat the same class combinations.
    Use @apply sparingly - prefer React components.
    """
    
    // PREFERRED: React component
    function Button({ variant = 'primary', size = 'md', children, ...props }) {
      const baseClasses = 'font-medium rounded-md transition-colors focus:outline-none focus:ring-2';
    
      const variants = {
        primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500',
        secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900 focus:ring-gray-500',
        danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
      };
    
      const sizes = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg',
      };
    
      return (
        <button
          className={`${baseClasses} ${variants[variant]} ${sizes[size]}`}
          {...props}
        >
          {children}
        </button>
      );
    }
    
    
    // WITH TAILWIND-MERGE (handles conflicts)
    import { twMerge } from 'tailwind-merge';
    import { clsx } from 'clsx';
    
    function cn(...inputs) {
      return twMerge(clsx(inputs));
    }
    
    function Button({ className, variant, ...props }) {
      return (
        <button
          className={cn(
            'px-4 py-2 rounded-md font-medium',
            variant === 'primary' && 'bg-blue-600 text-white',
            variant === 'secondary' && 'bg-gray-200 text-gray-900',
            className // Allows override
          )}
          {...props}
        />
      );
    }
    
    
    // @apply (use sparingly, mainly for base styles)
    /* globals.css */
    @layer components {
      .btn {
        @apply px-4 py-2 rounded-md font-medium transition-colors;
      }
    
      .btn-primary {
        @apply bg-blue-600 hover:bg-blue-700 text-white;
      }
    }
    

---
  #### **Name**
Custom Configuration
  #### **Description**
Extending Tailwind with custom values
  #### **When**
Brand colors, custom spacing, fonts
  #### **Example**
    # CUSTOM CONFIGURATION:
    
    """
    Extend the default theme, don't replace it.
    Use CSS variables for dynamic values.
    """
    
    // tailwind.config.js
    const defaultTheme = require('tailwindcss/defaultTheme');
    
    module.exports = {
      content: ['./src/**/*.{js,ts,jsx,tsx}'],
      darkMode: 'class',
      theme: {
        extend: {
          // Custom colors
          colors: {
            brand: {
              50: '#f0f9ff',
              100: '#e0f2fe',
              500: '#0ea5e9',
              600: '#0284c7',
              700: '#0369a1',
            },
            // CSS variable colors (for dynamic theming)
            primary: 'hsl(var(--primary))',
            secondary: 'hsl(var(--secondary))',
            background: 'hsl(var(--background))',
            foreground: 'hsl(var(--foreground))',
          },
    
          // Custom fonts
          fontFamily: {
            sans: ['Inter var', ...defaultTheme.fontFamily.sans],
            display: ['Cal Sans', 'sans-serif'],
          },
    
          // Custom spacing
          spacing: {
            '128': '32rem',
            '144': '36rem',
          },
    
          // Custom animations
          animation: {
            'fade-in': 'fadeIn 0.5s ease-in-out',
            'slide-up': 'slideUp 0.3s ease-out',
          },
          keyframes: {
            fadeIn: {
              '0%': { opacity: '0' },
              '100%': { opacity: '1' },
            },
            slideUp: {
              '0%': { transform: 'translateY(10px)', opacity: '0' },
              '100%': { transform: 'translateY(0)', opacity: '1' },
            },
          },
        },
      },
      plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
      ],
    };
    
    
    /* CSS variables for theming */
    :root {
      --primary: 222.2 47.4% 11.2%;
      --secondary: 210 40% 96.1%;
      --background: 0 0% 100%;
      --foreground: 222.2 47.4% 11.2%;
    }
    
    .dark {
      --primary: 210 40% 98%;
      --secondary: 222.2 47.4% 11.2%;
      --background: 222.2 84% 4.9%;
      --foreground: 210 40% 98%;
    }
    

---
  #### **Name**
Tailwind with React
  #### **Description**
Best practices for Tailwind in React apps
  #### **When**
React/Next.js projects
  #### **Example**
    # TAILWIND + REACT:
    
    """
    Use clsx + tailwind-merge for clean class management.
    Structure components for reusability.
    """
    
    // lib/utils.ts
    import { type ClassValue, clsx } from 'clsx';
    import { twMerge } from 'tailwind-merge';
    
    export function cn(...inputs: ClassValue[]) {
      return twMerge(clsx(inputs));
    }
    
    
    // components/Card.tsx
    import { cn } from '@/lib/utils';
    
    interface CardProps {
      className?: string;
      children: React.ReactNode;
    }
    
    export function Card({ className, children }: CardProps) {
      return (
        <div
          className={cn(
            'rounded-lg border border-gray-200 bg-white p-6 shadow-sm',
            'dark:border-gray-800 dark:bg-gray-950',
            className
          )}
        >
          {children}
        </div>
      );
    }
    
    export function CardHeader({ className, children }: CardProps) {
      return (
        <div className={cn('mb-4', className)}>
          {children}
        </div>
      );
    }
    
    export function CardTitle({ className, children }: CardProps) {
      return (
        <h3 className={cn(
          'text-lg font-semibold text-gray-900 dark:text-white',
          className
        )}>
          {children}
        </h3>
      );
    }
    
    
    // Usage
    <Card className="max-w-md">
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <p className="text-gray-600 dark:text-gray-300">
        Card content here
      </p>
    </Card>
    

---
  #### **Name**
shadcn/ui Integration
  #### **Description**
Using shadcn/ui component library
  #### **When**
Need pre-built accessible components
  #### **Example**
    # SHADCN/UI:
    
    """
    Copy-paste components you own.
    Customize everything.
    Built on Radix UI primitives.
    """
    
    # Install shadcn/ui
    npx shadcn-ui@latest init
    
    # Add components
    npx shadcn-ui@latest add button
    npx shadcn-ui@latest add card
    npx shadcn-ui@latest add dialog
    npx shadcn-ui@latest add dropdown-menu
    
    
    // Components are added to your codebase
    // components/ui/button.tsx - fully customizable
    
    import { Button } from '@/components/ui/button';
    import {
      Card,
      CardContent,
      CardDescription,
      CardHeader,
      CardTitle,
    } from '@/components/ui/card';
    import {
      Dialog,
      DialogContent,
      DialogDescription,
      DialogHeader,
      DialogTitle,
      DialogTrigger,
    } from '@/components/ui/dialog';
    
    function Example() {
      return (
        <Card>
          <CardHeader>
            <CardTitle>Account</CardTitle>
            <CardDescription>Manage your account settings</CardDescription>
          </CardHeader>
          <CardContent>
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">Edit Profile</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Edit Profile</DialogTitle>
                  <DialogDescription>
                    Make changes to your profile here.
                  </DialogDescription>
                </DialogHeader>
                {/* Form content */}
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>
      );
    }
    

## Anti-Patterns


---
  #### **Name**
Too Many Custom Values
  #### **Description**
Using arbitrary values instead of design tokens
  #### **Why**
    Tailwind's scale is designed for consistency. Using arbitrary values
    like p-[13px] everywhere creates an inconsistent design and larger
    bundle sizes.
    
  #### **Instead**
    # WRONG: Arbitrary values everywhere
    <div class="p-[13px] mt-[7px] text-[15px]">
    
    # RIGHT: Use the scale
    <div class="p-3 mt-2 text-sm">
    
    # If you need custom values often, extend the config:
    theme: {
      extend: {
        spacing: {
          '13': '3.25rem',
        }
      }
    }
    

---
  #### **Name**
@apply Everything
  #### **Description**
Overusing @apply for component styles
  #### **Why**
    @apply defeats the purpose of Tailwind. You're back to naming things
    and maintaining CSS files. Use React components for abstraction.
    
  #### **Instead**
    /* WRONG: @apply for everything */
    .card {
      @apply p-6 bg-white rounded-lg shadow-md;
    }
    .card-header {
      @apply text-xl font-bold mb-4;
    }
    
    /* RIGHT: Use React components */
    function Card({ children }) {
      return (
        <div className="p-6 bg-white rounded-lg shadow-md">
          {children}
        </div>
      );
    }
    
    /* OK: @apply for truly global base styles */
    @layer base {
      body {
        @apply bg-white text-gray-900 dark:bg-gray-950 dark:text-white;
      }
    }
    

---
  #### **Name**
Not Purging Properly
  #### **Description**
Shipping unused CSS to production
  #### **Why**
    Tailwind generates thousands of utility classes. Without proper
    content configuration, your CSS bundle will be huge.
    
  #### **Instead**
    // tailwind.config.js
    module.exports = {
      // CRITICAL: Configure content paths
      content: [
        './src/**/*.{js,ts,jsx,tsx,mdx}',
        './pages/**/*.{js,ts,jsx,tsx,mdx}',
        './components/**/*.{js,ts,jsx,tsx,mdx}',
        './app/**/*.{js,ts,jsx,tsx,mdx}',
      ],
    }
    
    // Dynamic classes must be complete strings:
    // WRONG: Won't be detected
    const color = 'blue';
    className={`text-${color}-500`}
    
    // RIGHT: Include full class names
    const colorClasses = {
      blue: 'text-blue-500',
      red: 'text-red-500',
    };
    className={colorClasses[color]}
    

---
  #### **Name**
Reinventing Components
  #### **Description**
Building accessible components from scratch
  #### **Why**
    Dropdowns, modals, and tabs have complex accessibility requirements.
    Building them correctly takes weeks. Use a component library.
    
  #### **Instead**
    # Use Headless UI, Radix, or shadcn/ui
    # They handle:
    # - Keyboard navigation
    # - Focus management
    # - ARIA attributes
    # - Screen reader support
    
    # Instead of building a dropdown:
    npm install @headlessui/react
    # or
    npx shadcn-ui@latest add dropdown-menu
    