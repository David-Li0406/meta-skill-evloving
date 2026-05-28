# V0 Dev - Sharp Edges

## Missing Shadcn Components

### **Id**
missing-shadcn-components
### **Summary**
v0 code references components you don't have
### **Severity**
high
### **Situation**
Import errors after copying code
### **Why**
  v0 uses full shadcn/ui library.
  Your project may not have all components.
  Easy to miss dependencies.
  
### **Solution**
  # v0 tells you required components in the code tab
  # Install them before copying:
  
  # Check what's needed
  # v0 shows: "This component uses: Button, Card, Input"
  
  # Add missing components
  npx shadcn-ui@latest add button card input
  
  # Or add multiple at once
  npx shadcn-ui@latest add button card input label checkbox
  
  # If using v0 CLI
  npx v0 add https://v0.dev/t/xxx
  # This auto-installs dependencies
  
  # Common dependency chains:
  # Dialog → needs: dialog, button
  # Command → needs: command, dialog, input
  # Calendar → needs: calendar, button, popover
  # DataTable → needs: table, checkbox, button, dropdown-menu
  
  # Check your components directory
  ls components/ui/
  # Compare with v0 imports
  
### **Symptoms**
  - "Module not found" errors
  - Cannot find './ui/button'
  - Missing component files
### **Detection Pattern**
import.*@/components/ui

## Tailwind Class Conflicts

### **Id**
tailwind-class-conflicts
### **Summary**
Custom Tailwind classes don't work
### **Severity**
medium
### **Situation**
Styles don't match v0 preview
### **Why**
  Custom Tailwind config differs.
  Color names don't match.
  Missing extended utilities.
  
### **Solution**
  # v0 uses specific Tailwind config
  # Check your tailwind.config.js matches
  
  // Required for shadcn/ui
  module.exports = {
    darkMode: ["class"],
    content: [
      "./components/**/*.{ts,tsx}",
      "./app/**/*.{ts,tsx}",
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
          // ... full shadcn color palette
        },
        borderRadius: {
          lg: "var(--radius)",
          md: "calc(var(--radius) - 2px)",
          sm: "calc(var(--radius) - 4px)",
        },
      },
    },
    plugins: [require("tailwindcss-animate")],
  }
  
  # Add CSS variables in globals.css
  @layer base {
    :root {
      --background: 0 0% 100%;
      --foreground: 222.2 84% 4.9%;
      --primary: 222.2 47.4% 11.2%;
      --primary-foreground: 210 40% 98%;
      /* ... full variable set */
    }
    .dark {
      --background: 222.2 84% 4.9%;
      --foreground: 210 40% 98%;
      /* ... dark mode variables */
    }
  }
  
  # Run shadcn init to set up correctly
  npx shadcn-ui@latest init
  
### **Symptoms**
  - Colors don't match
  - Missing animations
  - Wrong border radius
### **Detection Pattern**
hsl\(var\(--

## Hardcoded Content

### **Id**
hardcoded-content
### **Summary**
v0 generates hardcoded text and data
### **Severity**
medium
### **Situation**
Can't use component with different data
### **Why**
  v0 doesn't know your data structure.
  Generates example content.
  Not prop-driven by default.
  
### **Solution**
  # v0 Output (hardcoded):
  function PricingCard() {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Pro Plan</CardTitle>
          <CardDescription>$29/month</CardDescription>
        </CardHeader>
        <CardContent>
          <ul>
            <li>Unlimited projects</li>
            <li>Priority support</li>
          </ul>
        </CardContent>
      </Card>
    )
  }
  
  # Convert to Props:
  interface PricingCardProps {
    name: string
    price: number
    billingPeriod: "monthly" | "yearly"
    features: string[]
    isPopular?: boolean
    onSelect: () => void
  }
  
  function PricingCard({
    name,
    price,
    billingPeriod,
    features,
    isPopular = false,
    onSelect
  }: PricingCardProps) {
    return (
      <Card className={isPopular ? "border-primary" : ""}>
        <CardHeader>
          <CardTitle>{name}</CardTitle>
          <CardDescription>
            ${price}/{billingPeriod === "monthly" ? "mo" : "yr"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul>
            {features.map((feature) => (
              <li key={feature}>{feature}</li>
            ))}
          </ul>
          <Button onClick={onSelect}>
            {isPopular ? "Get Started" : "Select Plan"}
          </Button>
        </CardContent>
      </Card>
    )
  }
  
  # Ask v0 for prop-driven version:
  "Make this component accept props for:
  - plan name
  - price
  - feature list
  - isPopular boolean
  Add TypeScript interface"
  
### **Symptoms**
  - Can't reuse component
  - Have to edit for each use
  - No TypeScript props
### **Detection Pattern**
function \w+\(\)

## Accessibility Gaps

### **Id**
accessibility-gaps
### **Summary**
Generated code missing a11y features
### **Severity**
high
### **Situation**
Screen reader or keyboard issues
### **Why**
  v0 focuses on visual design.
  May skip aria labels.
  Keyboard navigation incomplete.
  
### **Solution**
  # Common Issues and Fixes:
  
  # 1. Missing labels
  # BAD
  <Input placeholder="Email" />
  # GOOD
  <Label htmlFor="email">Email</Label>
  <Input id="email" placeholder="you@example.com" />
  
  # 2. Icon buttons without text
  # BAD
  <Button><TrashIcon /></Button>
  # GOOD
  <Button aria-label="Delete item">
    <TrashIcon aria-hidden="true" />
  </Button>
  
  # 3. Missing focus states (usually OK with shadcn)
  # Verify focus-visible works
  
  # 4. Interactive divs
  # BAD
  <div onClick={handleClick}>Click me</div>
  # GOOD
  <button onClick={handleClick}>Click me</button>
  # Or
  <div
    role="button"
    tabIndex={0}
    onClick={handleClick}
    onKeyDown={(e) => e.key === "Enter" && handleClick()}
  >
    Click me
  </div>
  
  # 5. Missing error announcements
  # BAD
  {error && <p className="text-red-500">{error}</p>}
  # GOOD
  {error && (
    <p role="alert" className="text-red-500">{error}</p>
  )}
  
  # Ask v0 explicitly:
  "Ensure accessibility:
  - All inputs have associated labels
  - Icon buttons have aria-label
  - Focus states are visible
  - Errors are announced to screen readers
  - Keyboard navigation works for all interactive elements"
  
### **Symptoms**
  - Lighthouse accessibility warnings
  - Screen reader can't navigate
  - Keyboard focus invisible
### **Detection Pattern**
aria-label|htmlFor|role=

## Dark Mode Incomplete

### **Id**
dark-mode-incomplete
### **Summary**
Dark mode styling missing or broken
### **Severity**
low
### **Situation**
Component looks wrong in dark mode
### **Why**
  Some classes don't have dark variants.
  Hardcoded colors instead of CSS variables.
  Shadows don't adapt.
  
### **Solution**
  # Check for proper dark mode classes
  
  # BAD - hardcoded colors
  <div className="bg-white text-black">
  
  # GOOD - uses CSS variables
  <div className="bg-background text-foreground">
  
  # BAD - no dark variant
  <div className="bg-gray-100">
  
  # GOOD - with dark mode
  <div className="bg-gray-100 dark:bg-gray-800">
  
  # Shadows in dark mode
  # BAD
  <Card className="shadow-lg">
  # GOOD
  <Card className="shadow-lg dark:shadow-none dark:border">
  
  # Ask v0 explicitly:
  "Ensure full dark mode support:
  - Use CSS variable colors (background, foreground, etc.)
  - Add dark: variants for any custom colors
  - Adjust shadows for dark mode
  - Test contrast ratios"
  
  # Quick check - search for hardcoded colors
  grep -E "(bg-white|bg-black|text-white|text-black|bg-gray-\d+)" component.tsx
  
### **Symptoms**
  - White backgrounds in dark mode
  - Unreadable text
  - Missing visual hierarchy
### **Detection Pattern**
dark:|bg-background