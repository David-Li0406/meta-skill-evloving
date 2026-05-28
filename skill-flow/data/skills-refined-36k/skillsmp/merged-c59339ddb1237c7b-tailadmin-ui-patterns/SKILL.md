---
name: tailadmin-ui-patterns
description: Use this skill when building any dashboard or admin panel interface, creating data tables, cards, charts, or metrics displays, implementing forms, buttons, alerts, or modals, and building navigation that follows TailAdmin design.
---

# TailAdmin UI Patterns Skill

## When to Use This Skill

**ALWAYS invoke this skill for:**
- Dashboard interfaces and admin panels
- Data tables and grid layouts
- Charts, metrics, and KPI displays
- Form components (inputs, selects, checkboxes, toggles)
- Card layouts and stat boxes
- Navigation (sidebar, header, breadcrumbs)
- Buttons, badges, alerts, and modals
- Any UI requiring TailAdmin styling

## Critical Rule: FETCH BEFORE IMPLEMENTING

**NEVER guess or invent classes. ALWAYS fetch from the official repository first.**

```bash
# MANDATORY: Fetch TailAdmin source before ANY UI work
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin 2>/dev/null || echo "Already cloned"

# Verify the clone
ls /tmp/tailadmin/src/
```

## Repository Reference

| Item | Value |
|------|-------|
| **Repository** | https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template |
| **Branch** | `main` |
| **Source Path** | `src/` |
| **CSS Config** | `tailwind.config.js` |
| **Custom CSS** | `src/css/style.css` |

## Mandatory Fetch Commands

**Before implementing ANY TailAdmin UI, run these commands:**

```bash
# 1. Clone repository (if not already done)
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin 2>/dev/null

# 2. Check available page templates
ls /tmp/tailadmin/src/*.html

# 3. Check partials (reusable components)
ls /tmp/tailadmin/src/partials/

# 4. View Tailwind config for custom classes
cat /tmp/tailadmin/tailwind.config.js

# 5. View custom CSS definitions
cat /tmp/tailadmin/src/css/style.css
```

## Finding Specific Components

```bash
# Find dashboard/stats card patterns
grep -A 50 'stat\|kpi\|metric' /tmp/tailadmin/src/index.html | head -80

# Find table patterns
cat /tmp/tailadmin/src/tables.html | head -200

# Find form patterns  
cat /tmp/tailadmin/src/form-elements.html | head -200

# Find button patterns
grep -B 5 -A 10 'btn\|button' /tmp/tailadmin/src/*.html | head -100

# Find card patterns
grep -B 5 -A 20 'rounded-sm border' /tmp/tailadmin/src/*.html | head -100

# Find sidebar patterns
cat /tmp/tailadmin/src/partials/sidebar.html

# Find header patterns
cat /tmp/tailadmin/src/partials/header.html

# Find modal patterns
grep -B 5 -A 30 'modal' /tmp/tailadmin/src/*.html | head -100

# Find alert patterns
cat /tmp/tailadmin/src/alerts.html | head -150

# Search for ANY specific class
grep -r 'class-name-here' /tmp/tailadmin/src/
```

## Class Verification Process

**Before using ANY class, verify it exists:**

```bash
# Step 1: Search in HTML files
grep -r 'bg-boxdark' /tmp/tailadmin/src/ | head -5

# Step 2: Search in Tailwind config (for custom classes)
grep 'boxdark' /tmp/tailadmin/tailwind.config.js

# Step 3: Search in custom CSS
grep 'boxdark' /tmp/tailadmin/src/css/style.css

# If class not found in ANY of these = DO NOT USE IT
```

## TailAdmin Custom Tailwind Configuration

**IMPORTANT**: These custom classes are defined in `tailwind.config.js`. Always verify before using:

```bash
# View the full Tailwind config to see ALL custom values
cat /tmp/tailadmin/tailwind.config.js
```

### Custom Colors (from tailwind.config.js)

```javascript
// Verify with: grep -A 100 'colors:' /tmp/tailadmin/tailwind.config.js
colors: {
  current: 'currentColor',
  transparent: 'transparent',
  white: '#FFFFFF',
  black: '#1C2434',
  'black-2': '#010101',
  body: '#64748B',
  bodydark: '#AEB7C0',
  bodydark1: '#DEE4EE',
  bodydark2: '#8A99AF',
  primary: '#3C50E0',
  secondary: '#80CAEE',
  stroke: '#E2E8F0',
  gray: '#EFF4FB',
  graydark: '#333A48',
  'gray-2': '#F7F9FC',
  'gray-3': '#FAFAFA',
  whiten: '#F1F5F9',
  whiter: '#F5F7FD',
  boxdark: '#24303F',
  'boxdark-2': '#1A222C',
  strokedark: '#2E3A47',
  'form-strokedark': '#3d4d60',
  'form-input': '#1d2a39',
  'meta-1': '#DC3545',
  'meta-2': '#EFF2F7',
  'meta-3': '#10B981',
  'meta-4': '#313D4A',
  'meta-5': '#259AE6',
  'meta-6': '#FFBA00',
  'meta-7': '#FF6766',
  'meta-8': '#F0950C',
  'meta-9': '#E5E7EB',
  'meta-10': '#0FADCF',
  success: '#219653',
  danger: '#D34053',
  warning: '#FFA70B',
}
```

### Custom Spacing (from tailwind.config.js)

```javascript
// Verify with: grep -A 50 'spacing:' /tmp/tailadmin/tailwind.config.js
// Or check extend section
spacing: {
  '4.5': '1.125rem',   // 18px
  '5.5': '1.375rem',   // 22px
  '6.5': '1.625rem',   // 26px
  '7.5': '1.875rem',   // 30px
  '8.5': '2.125rem',   // 34px
  '9.5': '2.375rem',   // 38px
  '10.5': '2.625rem',  // 42px
  '11': '2.75rem',     // 44px
  '11.5': '2.875rem',  // 46px
  '12.5': '3.125rem',  // 50px
  '13': '3.25rem',     // 52px
  '14': '3.5rem',      // 56px
  '15': '3.75rem',     // 60px
  '16': '4rem',        // 64px
  '17': '4.25rem',     // 68px
  '18': '4.5rem',      // 72px
  '19': '4.75rem',     // 76px
  '21': '5.25rem',     // 84px
  '22': '5.5rem',      // 88px
  '22.5': '5.625rem',  // 90px
  '25': '6.25rem',     // 100px
  '27': '6.75rem',     // 108px
  '29': '7.25rem',     // 116px
  '30': '7.5rem',      // 120px
  '35': '8.75rem',     // 140px
  '45': '11.25rem',    // 180px
  '46': '11.5rem',     // 184px
  '54': '13.5rem',     // 216px
  '55': '13.75rem',    // 220px
  '60': '15rem',       // 240px
  '65': '16.25rem',    // 260px
  '70': '17.5rem',     // 280px
  '72.5': '18.125rem', // 290px - Sidebar width
  '90': '22.5rem',     // 360px
  '125': '31.25rem',   // 500px
  '142.5': '35.625rem',// 570px - Modal width
  '180': '45rem',      // 720px
  '203': '50.75rem',   // 812px
  '230': '57.5rem',    // 920px
}
```

### Custom Shadows

```javascript
// Verify with: grep -A 20 'boxShadow:' /tmp/tailadmin/tailwind.config.js
boxShadow: {
  default: '0px 8px 13px -3px rgba(0, 0, 0, 0.07)',
  card: '0px 1px 3px rgba(0, 0, 0, 0.12)',
  'card-2': '0px 1px 2px rgba(0, 0, 0, 0.05)',
  switcher: '0px 2px 4px rgba(0, 0, 0, 0.2), inset 0px 2px 2px #FFFFFF, inset 0px -1px 1px rgba(0, 0, 0, 0.1)',
  'switch-1': '0px 0px 5px rgba(0, 0, 0, 0.15)',
  1: '0px 1px 3px rgba(0, 0, 0, 0.08)',
  2: '0px 1px 4px rgba(0, 0, 0, 0.12)',
  3: '0px 1px 5px rgba(0, 0, 0, 0.14)',
  4: '0px 4px 10px rgba(0, 0, 0, 0.12)',
  5: '0px 1px 1px rgba(0, 0, 0, 0.15)',
  6: '0px 3px 15px rgba(0, 0, 0, 0.1)',
  7: '-5px 0 0 #313D4A, 5px 0 0 #313D4A',
  8: '1px 0 0 #313D4A, -1px 0 0 #313D4A, 0 1px 0 #313D4A, 0 -1px 0 #313D4A, 0 3px 13px rgb(0 0 0 / 8%)',
}

// Drop shadows
dropShadow: {
  1: '0px 1px 0px #E2E8F0',
  2: '0px 1px 4px rgba(0, 0, 0, 0.12)',
}
```

## Layout Structure

### Main Layout Wrapper

```html
<!-- Main container with dark mode support -->
<div class="flex h-screen overflow-hidden">
  <!-- Sidebar -->
  <aside class="absolute left-0 top-0 z-9999 flex h-screen w-72.5 flex-col overflow-y-hidden bg-black duration-300 ease-linear dark:bg-boxdark lg:static lg:translate-x-0">
    <!-- Sidebar content -->
  </aside>

  <!-- Content Area -->
  <div class="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
    <!-- Header -->
    <header class="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
      <!-- Header content -->
    </header>

    <!-- Main Content -->
    <main>
      <div class="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
        <!-- Page content -->
      </div>
    </main>
  </div>
</div>
```

### Page Header / Breadcrumb

```html
<!-- Breadcrumb -->
<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
  <h2 class="text-title-md2 font-semibold text-black dark:text-white">
    Page Title
  </h2>

  <nav>
    <ol class="flex items-center gap-2">
      <li>
        <a class="font-medium" href="index.html">Dashboard /</a>
      </li>
      <li class="font-medium text-primary">Current Page</li>
    </ol>
  </nav>
</div>
```

## Card Components

### Basic Card

```html
<div class="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
  <h4 class="mb-6 text-xl font-semibold text-black dark:text-white">
    Card Title
  </h4>
  
  <!-- Card content -->
</div>
```

### Stats Card (KPI Card)

```html
<div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
  <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
    <!-- Icon SVG -->
    <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16">
      <!-- SVG path -->
    </svg>
  </div>

  <div class="mt-4 flex items-end justify-between">
    <div>
      <h4 class="text-title-md font-bold text-black dark:text-white">
        $3.456K
      </h4>
      <span class="text-sm font-medium">Total Views</span>
    </div>

    <span class="flex items-center gap-1 text-sm font-medium text-meta-3">
      0.43%
      <svg class="fill-meta-3" width="10" height="11" viewBox="0 0 10 11">
        <!-- Up arrow SVG -->
      </svg>
    </span>
  </div>
</div>
```

### Card with Chart

```html
<div class="col-span-12 rounded-sm border border-stroke bg-white px-5 pt-7.5 pb-5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
  <div class="flex flex-wrap items-start justify-between gap-3 sm:flex-nowrap">
    <div class="flex w-full flex-wrap gap-3 sm:gap-5">
      <div class="flex min-w-47.5">
        <span class="mt-1 mr-2 flex h-4 w-full max-w-4 items-center justify-center rounded-full border border-primary">
          <span class="block h-2.5 w-full max-w-2.5 rounded-full bg-primary"></span>
        </span>
        <div class="w-full">
          <p class="font-semibold text-primary">Total Revenue</p>
          <p class="text-sm font-medium