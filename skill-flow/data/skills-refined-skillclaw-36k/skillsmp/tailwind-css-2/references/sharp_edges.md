# Tailwind Css - Sharp Edges

## Dynamic Classes Purged

### **Id**
dynamic-classes-purged
### **Summary**
Dynamic class names get purged from production build
### **Severity**
critical
### **Situation**
  You build class names dynamically: `text-${color}-500`. Works in dev.
  In production, the text color doesn't apply. The class was purged
  because Tailwind couldn't detect it.
  
### **Why**
  Tailwind scans your files as static text. It can't execute JavaScript
  to see what classes you might generate. Dynamic string concatenation
  creates class names that don't exist in your source code.
  
### **Solution**
  # DYNAMIC CLASSES DON'T WORK
  
  # WRONG: String concatenation
  const color = 'blue';
  <div className={`text-${color}-500`} />
  // Tailwind sees: text-${color}-500
  // Not: text-blue-500
  
  # WRONG: Template literal
  <div className={`bg-${variant}-100`} />
  
  
  # RIGHT: Object mapping with complete class names
  const colorClasses = {
    blue: 'text-blue-500',
    red: 'text-red-500',
    green: 'text-green-500',
  };
  <div className={colorClasses[color]} />
  
  
  # RIGHT: Array of complete classes
  const bgColors = [
    'bg-red-100',
    'bg-blue-100',
    'bg-green-100',
  ];
  <div className={bgColors[index]} />
  
  
  # RIGHT: Conditional with complete strings
  <div className={isActive ? 'text-blue-500' : 'text-gray-500'} />
  
  
  # If you MUST use dynamic classes, safelist them:
  // tailwind.config.js
  module.exports = {
    safelist: [
      'text-blue-500',
      'text-red-500',
      'text-green-500',
      // Or patterns:
      { pattern: /bg-(red|blue|green)-(100|500)/ },
    ],
  }
  
### **Symptoms**
  - Styles work in dev but not production
  - Classes missing from built CSS
  - I swear this worked yesterday
### **Detection Pattern**
className=\{`[^`]*\$\{

## Class Order Conflicts

### **Id**
class-order-conflicts
### **Summary**
Class order matters for conflicting utilities
### **Severity**
high
### **Situation**
  You have `p-4 p-2` or pass className to override padding. Sometimes
  p-4 wins, sometimes p-2. It depends on the order in the generated
  CSS, not the order in your HTML.
  
### **Why**
  CSS specificity is based on source order when selectors are equal.
  Tailwind generates classes in a specific order. The order in your
  className string doesn't matter - CSS cascade order does.
  
### **Solution**
  # CLASS CONFLICTS ARE UNPREDICTABLE
  
  # WRONG: Both classes, unpredictable winner
  <div className="p-4 p-2" />
  
  
  # RIGHT: Use tailwind-merge
  import { twMerge } from 'tailwind-merge';
  
  function Card({ className }) {
    return (
      <div className={twMerge('p-4 bg-white', className)} />
    );
  }
  
  // Usage: className override works correctly
  <Card className="p-2" />
  // Result: "p-2 bg-white" - p-2 wins
  
  
  # RIGHT: Use clsx + tailwind-merge (cn utility)
  import { clsx, type ClassValue } from 'clsx';
  import { twMerge } from 'tailwind-merge';
  
  export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
  }
  
  // Usage
  <div className={cn(
    'p-4 text-gray-900',
    isLarge && 'p-8',
    className
  )} />
  
  
  # Without tailwind-merge, last conflicting class wins
  # based on CSS source order, NOT HTML order
  
### **Symptoms**
  - Overrides not working
  - Inconsistent styling
  - className prop ignored
### **Detection Pattern**


## Content Not Configured

### **Id**
content-not-configured
### **Summary**
Content paths missing classes from your files
### **Severity**
high
### **Situation**
  You add Tailwind classes to a new file or directory. They don't work.
  You check the HTML - classes are there. You check the CSS - classes
  are missing. Tailwind didn't scan that file.
  
### **Why**
  Tailwind only scans files matching the content glob patterns. If your
  file is outside those patterns, classes won't be included in the
  build.
  
### **Solution**
  # CONFIGURE CONTENT PATHS CORRECTLY
  
  // tailwind.config.js
  module.exports = {
    content: [
      // Include ALL files that might have Tailwind classes
      './src/**/*.{js,ts,jsx,tsx,mdx}',
      './pages/**/*.{js,ts,jsx,tsx,mdx}',
      './components/**/*.{js,ts,jsx,tsx,mdx}',
      './app/**/*.{js,ts,jsx,tsx,mdx}',
  
      // Include MDX content
      './content/**/*.mdx',
  
      // Include UI library if it uses Tailwind
      './node_modules/@myorg/ui/**/*.{js,ts,jsx,tsx}',
    ],
  }
  
  # COMMON MISTAKES:
  
  # Missing new directory
  # You add ./lib/ but forget to update content
  
  # Missing file extension
  # You use .mjs but only have *.js in config
  
  # Missing node_modules package
  # UI library uses Tailwind but isn't scanned
  
### **Symptoms**
  - Classes don't apply
  - CSS file missing utilities
  - Works for some files, not others
### **Detection Pattern**


## Dark Mode Not Class

### **Id**
dark-mode-not-class
### **Summary**
Dark mode not working with class strategy
### **Severity**
medium
### **Situation**
  You add dark: classes but they don't change anything. You toggle
  between light and dark but styles stay the same. You're using
  'class' strategy but not adding the dark class.
  
### **Why**
  With darkMode: 'class', Tailwind looks for the 'dark' class on a
  parent element (usually html or body). Without it, dark: classes
  are ignored.
  
### **Solution**
  # DARK MODE WITH CLASS STRATEGY
  
  // tailwind.config.js
  module.exports = {
    darkMode: 'class',  // Not 'media'
  }
  
  
  // You MUST add 'dark' class to html or body
  // Usually in _document.tsx or layout.tsx
  
  // React implementation
  function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
  
    useEffect(() => {
      // Add/remove 'dark' class on html element
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }, [theme]);
  
    return (
      <ThemeContext.Provider value={{ theme, setTheme }}>
        {children}
      </ThemeContext.Provider>
    );
  }
  
  
  // Next.js with next-themes
  import { ThemeProvider } from 'next-themes';
  
  export default function App({ Component, pageProps }) {
    return (
      <ThemeProvider attribute="class" defaultTheme="system">
        <Component {...pageProps} />
      </ThemeProvider>
    );
  }
  
  
  // System preference (no JS needed)
  darkMode: 'media'  // Uses prefers-color-scheme
  
### **Symptoms**
  
---
    ##### **Dark**
classes don't change anything
  
---
Light and dark look the same
  
---
Toggle doesn't affect styles
### **Detection Pattern**


## Spacing Inconsistency

### **Id**
spacing-inconsistency
### **Summary**
Using arbitrary values creates design inconsistency
### **Severity**
medium
### **Situation**
  You use p-[17px], mt-[23px], text-[15px] throughout your app. Each
  component has slightly different spacing. The design looks "off"
  but you can't pinpoint why.
  
### **Why**
  Tailwind's spacing scale is designed for visual harmony. Arbitrary
  values break the rhythm. Your eye notices the inconsistency even
  if you can't articulate it.
  
### **Solution**
  # STICK TO THE SCALE
  
  # WRONG: Arbitrary values everywhere
  <div class="p-[17px] mt-[23px] gap-[11px]">
  
  # RIGHT: Use the spacing scale
  <div class="p-4 mt-6 gap-3">
  
  # Tailwind spacing scale:
  # 0.5: 0.125rem (2px)
  # 1:   0.25rem  (4px)
  # 2:   0.5rem   (8px)
  # 3:   0.75rem  (12px)
  # 4:   1rem     (16px)
  # 5:   1.25rem  (20px)
  # 6:   1.5rem   (24px)
  # 8:   2rem     (32px)
  # 10:  2.5rem   (40px)
  # 12:  3rem     (48px)
  # 16:  4rem     (64px)
  
  
  # If you need custom values, extend the scale:
  // tailwind.config.js
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      }
    }
  }
  
  
  # EXCEPTION: One-off layout values are OK
  <div class="max-w-[calc(100%-2rem)]">
  
### **Symptoms**
  - Design looks unpolished
  - Inconsistent spacing throughout
  - Hard to maintain consistency
### **Detection Pattern**
class="[^"]*\\[[0-9]+px\\]

## Hover Touch Devices

### **Id**
hover-touch-devices
### **Summary**
Hover states stuck on touch devices
### **Severity**
medium
### **Situation**
  User taps a button on mobile. The hover state applies and stays.
  They tap elsewhere but the button still looks hovered. The UI
  feels broken on touch devices.
  
### **Why**
  Touch devices fire hover events on tap and may not fire mouse leave.
  CSS hover states can get "stuck." This is a CSS issue, not Tailwind
  specific, but Tailwind makes hover states easy to add.
  
### **Solution**
  # HOVER ON TOUCH DEVICES
  
  # Use @media (hover: hover) for hover styles
  # Tailwind handles this automatically in v3.4+
  
  # The hover: modifier already handles this correctly
  <button class="
    bg-blue-500
    hover:bg-blue-600
    active:bg-blue-700
  ">
    Click
  </button>
  
  
  # For complex hover effects, use media query:
  @media (hover: hover) {
    .card:hover {
      transform: translateY(-2px);
    }
  }
  
  
  # In Tailwind, use arbitrary media query:
  <div class="
    [@media(hover:hover)]:hover:translate-y-[-2px]
  ">
  
  
  # Or add a custom variant:
  // tailwind.config.js
  plugins: [
    plugin(function({ addVariant }) {
      addVariant('hover-hover', '@media (hover: hover) { &:hover }')
    })
  ]
  
  <div class="hover-hover:translate-y-[-2px]">
  
### **Symptoms**
  - Hover states stuck on mobile
  - Touch interactions feel wrong
  - Buttons stay "hovered" after tap
### **Detection Pattern**


## Z Index Chaos

### **Id**
z-index-chaos
### **Summary**
Z-index conflicts with arbitrary values
### **Severity**
medium
### **Situation**
  You set z-[9999] to make a modal appear above everything. Then you
  need a tooltip above the modal, so z-[99999]. Soon you have z-index
  values in the millions and still have stacking issues.
  
### **Why**
  Arbitrary z-index values don't scale. When everything is trying to
  be "on top," nothing has a clear hierarchy.
  
### **Solution**
  # USE A Z-INDEX SCALE
  
  # Tailwind's default scale:
  # z-0: 0
  # z-10: 10
  # z-20: 20
  # z-30: 30
  # z-40: 40
  # z-50: 50
  
  # Define semantic z-index in config:
  // tailwind.config.js
  theme: {
    extend: {
      zIndex: {
        'dropdown': '100',
        'sticky': '200',
        'modal': '300',
        'toast': '400',
        'tooltip': '500',
      }
    }
  }
  
  # Usage
  <div class="z-dropdown">  <!-- Dropdown content -->
  <div class="z-modal">     <!-- Modal overlay -->
  <div class="z-tooltip">   <!-- Tooltip always on top -->
  
  
  # ALSO: Use stacking contexts
  # Instead of fighting z-index, create new stacking contexts
  <div class="relative z-0">
    <!-- Everything inside has its own stacking context -->
  </div>
  
  
  # Portal-based modals avoid most z-index issues
  # Render at document root, not nested in components
  
### **Symptoms**
  - Modal behind dropdown
  - Z-index arms race
  - Random stacking order
### **Detection Pattern**
z-\\[\\d{4,}\\]