---
name: ui-ux-pro-max
description: "Trí tuệ thiết kế UI/UX toàn diện. 50+ phong cách, 21 bảng màu, 50+ cặp font, 20 loại biểu đồ, 9 stack (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Hành động: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Dự án: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Thành phần: button, modal, navbar, sidebar, card, table, form, chart. Phong cách: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Chủ đề: color palette, accessibility, animation, layout, typography, spacing, hover, shadow, gradient. Tích hợp: shadcn/ui MCP cho component search và examples."
version: "2.0.0"
compatibility: "Claude Code với Python 3.x+"
author: "UI/UX Pro Max Team"
tags: ["ui", "ux", "design", "frontend", "tailwind", "components"]
---

# UI/UX Pro Max - Trí Tuệ Thiết Kế Toàn Diện

## 📋 Mục Lục

1. [Giới Thiệu](#1-giới-thiệu)
2. [Tính Năng Chính](#2-tính-năng-chính)
3. [Kiến Trúc Hệ Thống](#3-kiến-trúc-hệ-thống)
4. [Hướng Dẫn Cài Đặt](#4-hướng-dẫn-cài-đặt)
5. [Cách Sử Dụng Chi Tiết](#5-cách-sử-dụng-chi-tiết)
6. [Tham Chiếu Tìm Kiếm](#6-tham-chiếu-tìm-kiếm)
7. [Quy Trình Thiết Kế](#7-quy-trình-thiết-kế)
8. [Quy Tắc UI Chuyên Nghiệp](#8-quy-tắc-ui-chuyên-nghiệp)
9. [Best Practices](#9-best-practices)
10. [Checklist & Review](#10-checklist--review)
11. [Ví Dụ Thực Tế](#11-ví-dụ-thực-tế)
12. [Hướng Dẫn Mở Rộng](#12-hướng-dẫn-mở-rộng)
13. [Troubleshooting](#13-troubleshooting)
14. [FAQ](#14-faq)

---

## 1. Giới Thiệu

### 1.1 Skill là gì?

**UI/UX Pro Max** là một skill chuyên sâu cho Claude Code, cung cấp:

- **Kho dữ liệu thiết kế**: 50+ phong cách UI, 21 bảng màu, 50+ cặp font chữ
- **Hệ thống tìm kiếm thông minh**: Tìm kiếm theo domain, stack, và use case
- **Best practices theo stack**: Hướng dẫn cụ thể cho React, Next.js, Vue, Svelte, Flutter, v.v.
- **Quy tắc UI chuyên nghiệp**: Auto-check các lỗi phổ biến trong thiết kế
- **Checklist tự động**: Đảm bảo chất lượng code trước khi delivery

### 1.2 Khi Nào Nên Dùng

✅ **Sử dụng skill này khi:**

| Use Case | Ví Dụ Yêu Cầu |
|----------|---------------|
| **Thiết kế từ零** | "Tạo landing page cho SaaS B2B" |
| **Cải thiện UI** | "Fix UI này cho chuyên nghiệp hơn" |
| **Review code** | "Review component này có vấn đề gì" |
| **Tìm inspiration** | "Cho tôi 3 phong cách cho dashboard" |
| **Convert design** | "Chuyển Figma này thành code" |
| **Tối ưu UX** | "Cải thiện accessibility của trang này" |

❌ **Không sử dụng khi:**

- Logic backend, database queries, API design (dùng skill backend khác)
- DevOps, CI/CD, infrastructure setup
- Mobile native (iOS/Android) không phải React Native/Flutter

### 1.3 Workflow Tổng Quản

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parse Request  │ ← Trích xuất: product type, style, stack, industry
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Search Data    │ ← Multi-domain search: product, style, color, typography
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Synthesize     │ ← Tổng hợp thành design system
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Implement      │ ← Code generation theo stack
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Review & Check │ ← Quality assurance
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deliver        │
└─────────────────┘
```

---

## 2. Tính Năng Chính

### 2.1 Database Thiết Kế

#### 2.1.1 Phong Cách UI (50+ Styles)

| Category | Styles |
|----------|--------|
| **Modern** | Minimalism, Flat Design, Neumorphism, Glassmorphism, Claymorphism |
| **Bold** | Brutalism, Neo-Brutalism, Pop Art, Memphis |
| **Elegant** | Luxury, Sophisticated, Classical, Art Deco |
| **Tech** | Cyberpunk, Futuristic, Bento Grid, HUD Interface |
| **Playful** | Cartoon, 3D Cartoon, Doodle, Hand-drawn |
| **Nature** | Organic, Eco-friendly, Botanical, Earthy |
| **Professional** | Corporate, Clean, Enterprise, B2B |

#### 2.1.2 Bảng Màu (21 Color Palettes)

Mỗi palette bao gồm:
- **Primary**: Màu chính cho brand
- **Secondary**: Màu phụ, accent
- **CTA**: Call-to-action button
- **Background**: Background chính, secondary
- **Text**: Primary, secondary, muted text
- **Border**: Border, divider
- **Semantic**: Success, warning, error, info

#### 2.1.3 Typography (50+ Font Pairings)

Mỗi pairing bao gồm:
- **Heading font**: Font cho tiêu đề (Google Font)
- **Body font**: Font cho nội dung
- **Code font**: Font cho code (nếu cần)
- **Weights**: Recommended font weights
- **Import**: Google Fonts import link

#### 2.1.4 Chart Types (20+ Charts)

| Type | Library | Use Case |
|------|---------|----------|
| **Trend** | Line, Area | Timeline, progress |
| **Comparison** | Bar, Column | Side-by-side metrics |
| **Distribution** | Pie, Donut | Market share, categories |
| **Relationship** | Scatter, Bubble | Correlation, clusters |
| **Hierarchy** | Treemap, Sunburst | Folder structure, categories |
| **Flow** | Sankey, Chord | User journey, funnels |

### 2.2 Stack Support

| Stack | Coverage | Examples |
|-------|----------|----------|
| **html-tailwind** | Utilities, responsive, a11y | `<div class="flex items-center gap-4">` |
| **react** | State, hooks, performance | `const [count, setCount] = useState()` |
| **nextjs** | SSR, routing, images | `<Image src="/" alt="" />` |
| **vue** | Composition API, Pinia | `const count = ref(0)` |
| **svelte** | Runes, stores | `let count = $state(0)` |
| **swiftui** | Views, State, Navigation | `VStack { Text("Hello") }` |
| **react-native** | Components, Navigation | `<View><Text>Hello</Text></View>` |
| **flutter** | Widgets, Layout | `Container(child: Text("Hello"))` |
| **shadcn** | Components, theming | `<Button variant="default">Click</Button>` |

---

## 3. Kiến Trúc Hệ Thống

### 3.1 Cấu Trúc Thư Mục

```
.claude/skills/ui-ux-pro-max/
├── SKILL.md                 # File này (tài liệu chính)
├── data/                    # Database thiết kế
│   ├── styles.json          # 50+ phong cách UI
│   ├── colors.json          # 21 bảng màu
│   ├── typography.json      # 50+ font pairings
│   ├── charts.json          # 20+ chart types
│   ├── products.json        # Product type recommendations
│   ├── landing.json         # Landing page structures
│   └── ux.json              # UX best practices
├── scripts/                 # Scripts hỗ trợ
│   └── search.py            # Search engine
└── templates/               # Code templates
    ├── html-tailwind/       # HTML + Tailwind templates
    ├── react/               # React component templates
    ├── nextjs/              # Next.js page templates
    ├── vue/                 # Vue component templates
    └── svelte/              # Svelte component templates
```

### 3.2 Search Engine

**Script:** `.shared/scripts/search.py`

**Cú pháp:**

```bash
python3 .shared/scripts/search.py "<keyword>" --domain <domain> [--stack <stack>] [-n <results>]
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `keyword` | string | ✅ | Từ khóa tìm kiếm |
| `--domain` | string | ✅ | Domain: product, style, color, typography, landing, chart, ux, prompt |
| `--stack` | string | ❌ | Stack: html-tailwind (default), react, nextjs, vue, svelte, swiftui, react-native, flutter, shadcn |
| `-n` | int | ❌ | Số kết quả (default: 5) |

### 3.3 Data Schema

#### 3.3.1 Style Schema

```json
{
  "name": "glassmorphism",
  "category": "modern",
  "description": "Glass-like transparency with blur effects",
  "characteristics": [
    "Background blur: backdrop-blur-md",
    "Transparency: bg-white/10 dark:bg-black/10",
    "Subtle borders: border-white/20",
    "Soft shadows: shadow-lg"
  ],
  "best_for": ["dashboard", "portfolio", "SaaS"],
  "color_schemes": ["gradient", "pastel", "vibrant"],
  "frameworks": ["tailwind", "css"],
  "example_classes": "backdrop-blur-md bg-white/10 border border-white/20 shadow-xl"
}
```

#### 3.3.2 Color Schema

```json
{
  "name": "saas",
  "industry": "SaaS B2B",
  "primary": "#3B82F6",
  "secondary": "#8B5CF6",
  "cta": "#10B981",
  "background": "#FFFFFF",
  "background_secondary": "#F8FAFC",
  "text_primary": "#0F172A",
  "text_secondary": "#475569",
  "text_muted": "#94A3B8",
  "border": "#E2E8F0",
  "success": "#10B981",
  "warning": "#F59E0B",
  "error": "#EF4444",
  "info": "#3B82F6",
  "tailwind_config": {
    "primary": "blue-500",
    "secondary": "violet-500",
    "cta": "emerald-500"
  }
}
```

---

## 4. Hướng Dẫn Cài Đặt

### 4.1 Kiểm Tra Python

```bash
# Kiểm tra version
python3 --version

# Cần Python 3.7+ để chạy search script
```

### 4.2 Cài Đặt Python (nếu chưa có)

#### Windows

```powershell
# Method 1: winget (recommended)
winget install Python.Python.3.12

# Method 2: Download installer
# Visit: https://www.python.org/downloads/
```

#### macOS

```bash
# Method 1: Homebrew (recommended)
brew install python@3.12

# Method 2: pyenv
brew install pyenv
pyenv install 3.12
pyenv global 3.12
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 4.3 Verify Installation

```bash
# Test search script
python3 .shared/scripts/search.py "test" --domain style -n 1

# Expected output: JSON with 1 style result
```

---

## 5. Cách Sử Dụng Chi Tiết

### 5.1 Phân Tích Yêu Cầu

Trước khi search, trích xuất thông tin từ user request:

#### Template Phân Tích

```
USER REQUEST: "[Copy user request here]"

ANALYSIS:
├── Product Type: ___________ (SaaS, e-commerce, portfolio, etc.)
├── Industry: ___________ (healthcare, fintech, education, etc.)
├── Style Keywords: ___________ (minimal, playful, elegant, etc.)
├── Target Audience: ___________ (B2B, B2C, developers, etc.)
├── Platform: ___________ (web, mobile, desktop)
├── Stack: ___________ (React, Next.js, Vue, or default: html-tailwind)
└── Special Requirements: ___________ (dark mode, a11y, i18n, etc.)
```

#### Ví Dụ Phân Tích

**User Request:** "Tạo landing page cho startup AI healthcare, cần trông professional nhưng cũng innovative"

**Analysis:**

```
├── Product Type: Landing page (SaaS)
├── Industry: Healthcare / AI / Tech
├── Style Keywords: Professional, innovative, modern, tech-forward
├── Target Audience: B2B (hospital administrators, healthcare professionals)
├── Platform: Web (responsive)
├── Stack: html-tailwind (default)
└── Special Requirements: Trust/credibility (healthcare), cutting-edge (AI)
```

### 5.2 Multi-Domain Search

**Thứ tự tìm kiếm được khuyến nghị:**

```bash
# 1. Product Type - Lấy khuyến nghiệp tổng thể
python3 .shared/scripts/search.py "saas healthcare ai" --domain product

# 2. Style - Tìm phong cách phù hợp
python3 .shared/scripts/search.py "professional modern innovative tech" --domain style

# 3. Color Palette - Bảng màu theo ngành
python3 .shared/scripts/search.py "healthcare tech ai" --domain color

# 4. Typography - Font phù hợp phong cách
python3 .shared/scripts/search.py "professional modern tech" --domain typography

# 5. Landing Structure - Cấu trúc landing page
python3 .shared/scripts/search.py "saas b2b trust social-proof" --domain landing

# 6. UX Guidelines - Best practices
python3 .shared/scripts/search.py "accessibility" --domain ux
python3 .shared/scripts/search.py "conversion" --domain ux

# 7. Stack Guidelines - Implementation cụ thể
python3 .shared/scripts/search.py "responsive layout" --stack html-tailwind
python3 .shared/scripts/search.py "forms input validation" --stack html-tailwind
```

### 5.3 Synthetic & Implementation

Sau khi có tất cả search results:

#### 5.3.1 Tạo Design System

```yaml
# design-system.yaml

project: "AI Healthcare SaaS Landing Page"

colors:
  primary: "#0EA5E9"        # Sky blue (trust, healthcare)
  secondary: "#8B5CF6"      # Violet (AI, innovation)
  cta: "#10B981"            # Emerald (action, success)
  background: "#FFFFFF"
  background_secondary: "#F8FAFC"
  text_primary: "#0F172A"
  text_secondary: "#475569"

typography:
  heading: "Inter"          # Professional, modern
  body: "Inter"             # Consistent, clean
  weights: [400, 500, 600, 700]

style:
  name: "Clean Tech"
  characteristics:
    - "Card-based layout"
    - "Subtle shadows"
    - "Gradient accents"
    - "Professional imagery"

components:
  - "Hero with value proposition"
  - "Social proof (logos, testimonials)"
  - "Feature grid with icons"
  - "CTA sections"
  - "Trust indicators (certifications, stats)"
```

#### 5.3.2 Generate Code

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Healthcare SaaS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
          },
          colors: {
            primary: '#0EA5E9',
            secondary: '#8B5CF6',
            cta: '#10B981',
          }
        }
      }
    }
  </script>
</head>
<body class="bg-white text-slate-900 antialiased">
  <!-- Hero Section -->
  <section class="relative overflow-hidden bg-gradient-to-br from-slate-50 to-sky-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center">
        <h1 class="text-5xl font-bold text-slate-900 mb-6">
          AI-Powered Healthcare
        </h1>
        <p class="text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
          Revolutionize patient care with cutting-edge artificial intelligence
        </p>
        <div class="flex gap-4 justify-center">
          <button class="px-8 py-3 bg-cta hover:bg-emerald-600 text-white rounded-lg font-semibold transition-colors cursor-pointer">
            Get Started
          </button>
          <button class="px-8 py-3 bg-white hover:bg-slate-50 text-slate-900 rounded-lg font-semibold border border-slate-200 transition-colors cursor-pointer">
            Learn More
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- Social Proof -->
  <section class="py-16 bg-white border-y border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <p class="text-center text-slate-500 mb-8">Trusted by leading healthcare organizations</p>
      <div class="flex justify-center items-center gap-12 opacity-60">
        <!-- Logo placeholders -->
      </div>
    </div>
  </section>

  <!-- Features Grid -->
  <section class="py-24 bg-slate-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-slate-900 mb-4">
          Powerful Features
        </h2>
        <p class="text-lg text-slate-600">
          Everything you need to transform healthcare delivery
        </p>
      </div>
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Feature cards here -->
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-24 bg-gradient-to-r from-primary to-secondary">
    <div class="max-w-4xl mx-auto text-center px-4">
      <h2 class="text-4xl font-bold text-white mb-6">
        Ready to Transform Your Practice?
      </h2>
      <p class="text-xl text-white/90 mb-8">
        Join hundreds of healthcare organizations already using our platform
      </p>
      <button class="px-8 py-4 bg-white hover:bg-slate-50 text-primary rounded-lg font-bold text-lg transition-colors cursor-pointer">
        Start Free Trial
      </button>
    </div>
  </section>
</body>
</html>
```

---

## 6. Tham Chiếu Tìm Kiếm

### 6.1 Domain Reference

| Domain | Mục Đích | Keyword Examples | Output Format |
|--------|----------|------------------|---------------|
| **product** | Khuyến nghị sản phẩm | saas, ecommerce, portfolio, healthcare | { name, best_for, style_recommendations, typical_features } |
| **style** | Phong cách UI | glassmorphism, minimalism, brutalism, dark-mode | { name, characteristics, best_for, example_classes } |
| **color** | Bảng màu | saas, healthcare, fintech, beauty | { hex_codes, tailwind_classes, contrast_ratios } |
| **typography** | Font pairings | elegant, professional, playful, modern | { fonts, import_links, recommended_sizes } |
| **landing** | Cấu trúc landing | hero, testimonial, pricing, social-proof | { sections, layout, cta_strategies } |
| **chart** | Loại biểu đồ | trend, comparison, timeline, distribution | { chart_type, library, use_case } |
| **ux** | Best practices | accessibility, animation, z-index, loading | { do, dont, examples } |
| **prompt** | AI generation keywords | (tên style) | { css_keywords, effects, utilities } |

### 6.2 Stack Reference

| Stack | Search Examples | Output |
|-------|-----------------|--------|
| **html-tailwind** | "responsive", "grid", "flex", "dark-mode" | Tailwind classes, responsive modifiers |
| **react** | "state", "useEffect", "performance", "hooks" | React patterns, hook usage |
| **nextjs** | "ssr", "images", "routing", "api-routes" | Next.js specific APIs |
| **vue** | "composition-api", "pinia", "reactivity" | Vue 3 patterns |
| **svelte** | "runes", "stores", "transitions" | Svelte 5 patterns |
| **swiftui** | "navigation", "state", "animations" | SwiftUI code |
| **react-native** | "navigation", "lists", "gestures" | RN components |
| **flutter** | "widgets", "layout", "state" | Flutter widgets |
| **shadcn** | "button", "form", "dialog", "table" | shadcn/ui components |

---

## 7. Quy Trình Thiết Kế

### 7.1 Design Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: RESEARCH                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Analyze user requirements                                │
│ 2. Search product type recommendations                      │
│ 3. Search industry-specific styles                          │
│ 4. Search color palette                                     │
│ 5. Search typography                                        │
│ 6. Search UX best practices                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 2: DEFINE                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Create design system document                            │
│ 2. Define component library                                 │
│ 3. Establish color/typography scales                        │
│ 4. Set spacing/rhythm rules                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 3: DESIGN                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Create layout structure                                  │
│ 2. Design individual components                             │
│ 3. Define interaction states (hover, focus, disabled)       │
│ 4. Ensure responsive behavior                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 4: IMPLEMENT                       │
├─────────────────────────────────────────────────────────────┤
│ 1. Write HTML/component code                                │
│ 2. Apply styling (Tailwind, CSS, etc.)                     │
│ 3. Add interactivity                                        │
│ 4. Implement accessibility features                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 5: REVIEW                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Check against design system                             │
│ 2. Verify accessibility                                     │
│ 3. Test responsive breakpoints                              │
│ 4. Validate interaction states                              │
│ 5. Run quality checklist                                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 6: DELIVER                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Final code polish                                         │
│ 2. Document usage notes                                     │
│ 3. Provide customization guide                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Design System Template

```yaml
# design-system.yaml

project:
  name: ""
  type: "" # saas, ecommerce, portfolio, etc.
  industry: ""

brand:
  personality: [] # professional, playful, elegant, etc.
  target_audience: "" # b2b, b2c, developers, etc.

colors:
  primary: ""
  primary_hover: ""
  secondary: ""
  cta: ""
  cta_hover: ""
  background: ""
  background_secondary: ""
  text_primary: ""
  text_secondary: ""
  text_muted: ""
  border: ""
  success: ""
  warning: ""
  error: ""
  info: ""

typography:
  font_family: ""
  font_weights: []
  heading_sizes:
    h1: ""
    h2: ""
    h3: ""
    h4: ""
  body_sizes:
    large: ""
    base: ""
    small: ""

spacing:
  xs: ""  # 0.25rem / 4px
  sm: ""  # 0.5rem / 8px
  md: ""  # 1rem / 16px
  lg: ""  # 1.5rem / 24px
  xl: ""  # 2rem / 32px
  2xl: "" # 3rem / 48px

radius:
  sm: ""
  md: ""
  lg: ""
  full: ""

shadows:
  sm: ""
  md: ""
  lg: ""
  xl: ""

breakpoints:
  sm: ""  # 640px
  md: ""  # 768px
  lg: ""  # 1024px
  xl: ""  # 1280px

components:
  buttons:
    primary: ""
    secondary: ""
    ghost: ""
  cards:
    base: ""
    elevated: ""
    outlined: ""
  forms:
    input: ""
    select: ""
    checkbox: ""
```

---

## 8. Quy Tắc UI Chuyên Nghiệp

### 8.1 Icons & Visual Elements

| Quy Tắc | ✅ Nên | ❌ Không Nên | Tại Sao |
|---------|-------|-------------|---------|
| **Không dùng emoji** | SVG icons (Heroicons, Lucide, Phosphor) | 🎨 🚀 ⚙️ làm UI icons | Emoji trông thiếu chuyên nghiệp, không nhất quán across platforms |
| **Icon sizing** | `w-6 h-6` với `viewBox="0 0 24 24"` | Mix `w-4`, `w-5`, `w-8` random | Tạo cảm giác lộn xộn, thiếu rhythm |
| **Stroke width** | `stroke-width="2"` nhất quán | Mix `stroke-width="1"`, `"2"`, `"3"` | Thiếu visual consistency |
| **Brand logos** | SVG chính thức từ Simple Icons | Guess paths hoặc dùng screenshot | Đảm bảo accuracy, scalability |
| **Hover states** | `transition-colors duration-200` | `hover:scale-105` (dịch chuyển layout) | Layout shift gây trải nghiệm kém |

### 8.2 Interaction & Cursor

| Quy Tắc | ✅ Implementation |
|---------|-------------------|
| **Cursor pointer** | Thêm `cursor-pointer` vào tất cả interactable elements |
| **Hover feedback** | `hover:bg-slate-100 dark:hover:bg-slate-800` |
| **Active state** | `active:scale-[0.98]` cho buttons (nhẹ, không shift layout) |
| **Focus visible** | `focus:outline-none focus:ring-2 focus:ring-primary` |
| **Disabled state** | `disabled:opacity-50 disabled:cursor-not-allowed` |

### 8.3 Light/Dark Mode Contrast

#### Common Mistakes

```html
<!-- ❌ WRONG: Glass quá transparent trong light mode -->
<div class="bg-white/10 backdrop-blur-md border border-white/10">
  <!-- Content không đọc được -->
</div>

<!-- ✅ CORRECT: Tăng opacity trong light mode -->
<div class="bg-white/80 dark:bg-black/50 backdrop-blur-md border border-gray-200 dark:border-white/10">
  <!-- Content rõ ràng trong cả 2 mode -->
</div>
```

#### Contrast Requirements

| Element | Light Mode Min | Dark Mode Min |
|---------|---------------|---------------|
| **Body text** | `#475569` (slate-600) | `#94A3B8` (slate-400) |
| **Headings** | `#0F172A` (slate-900) | `#F1F5F9` (slate-100) |
| **Borders** | `#E2E8F0` (gray-200) | `#1E293B` (slate-800) |
| **Dividers** | `#F1F5F9` (slate-100) | `#334155` (slate-700) |

### 8.4 Layout & Spacing

```html
<!-- ❌ WRONG: Navbar dính sát edge -->
<nav class="fixed top-0 left-0 right-0">
  <!-- Không có breathing room -->
</nav>

<!-- ✅ CORRECT: Floating với spacing -->
<nav class="fixed top-4 left-4 right-4 max-w-7xl mx-auto">
  <!-- Professional floating look -->
</nav>
```

| Pattern | ✅ Implementation |
|---------|-------------------|
| **Container** | `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` |
| **Section spacing** | `py-16 md:py-24` cho sections |
| **Content padding** | Account cho fixed header với `scroll-padding-top` |
| **Grid gaps** | `gap-6 md:gap-8` cho responsive gaps |

---

## 9. Best Practices

### 9.1 Performance

#### 9.1.1 Image Optimization

```html
<!-- ✅ Next.js Image component -->
<Image
  src="/hero.jpg"
  alt="Hero section"
  width={1920}
  height={1080}
  priority
  className="object-cover"
/>

<!-- ✅ Regular img với attributes -->
<img
  src="/hero.jpg"
  alt="Hero section"
  loading="lazy"
  decoding="async"
  width="1920"
  height="1080"
/>
```

#### 9.1.2 CSS Performance

| Practice | ✅ Do | ❌ Don't |
|----------|-------|----------|
| **Animations** | `transform`, `opacity` | `width`, `height`, `top`, `left` |
| **Selectors** | Class-based (`.btn-primary`) | Deep nesting (`.nav > ul > li > a`) |
| **Units** | `rem`, `em`, `%` | Fixed `px` (trừ borders) |
| **Colors** | Semantic tokens (`--color-primary`) | Hardcoded hex values |

### 9.2 Accessibility (a11y)

#### 9.2.1 Semantic HTML

```html
<!-- ✅ CORRECT -->
<nav aria-label="Main navigation">
  <ul role="list">
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<aside aria-label="Sidebar">
  <!-- Sidebar content -->
</aside>

<footer>
  <!-- Footer content -->
</footer>
```

#### 9.2.2 ARIA Labels

```html
<!-- Icon buttons cần aria-label -->
<button aria-label="Close dialog">
  <XIcon />
</button>

<button aria-label="Share on Twitter">
  <TwitterIcon />
</button>

<!-- Live regions cho dynamic content -->
<div aria-live="polite" aria-atomic="true">
  <!-- Form errors, success messages -->
</div>
```

#### 9.2.3 Keyboard Navigation

```css
/* ✅ Visible focus states */
.focus-visible:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* ✅ Skip to content link */
.skip-to-content {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: var(--color-primary);
  color: white;
  text-decoration: none;
}

.skip-to-content:focus {
  top: 0;
}
```

#### 9.2.4 Color Contrast

| WCAG Level | Normal Text | Large Text (18pt+) |
|------------|-------------|-------------------|
| **AA** | 4.5:1 | 3:1 |
| **AAA** | 7:1 | 4.5:1 |

**Check contrast:** https://webaim.org/resources/contrastchecker/

### 9.3 Responsive Design

#### Breakpoint Strategy

```css
/* Mobile-first approach */
.component {
  /* Mobile styles (default) */
  padding: 1rem;
}

@media (min-width: 640px) {
  /* Small tablets */
  .component {
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  /* Desktop */
  .component {
    padding: 2rem;
  }
}
```

#### Container Queries (Future)

```css
/* Container queries cho component-level responsive */
@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

### 9.4 Design Tokens

```css
:root {
  /* Colors */
  --color-primary: #3B82F6;
  --color-primary-hover: #2563EB;
  --color-secondary: #8B5CF6;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

---

## 10. Checklist & Review

### 10.1 Pre-Delivery Checklist

#### Visual Quality

- [ ] **Không dùng emoji làm icons** - Chỉ dùng SVG từ icon libraries
- [ ] **Icon sizing nhất quán** - Tất cả icons dùng cùng kích thước (w-6 h-6)
- [ ] **Brand logos chính xác** - Xác thực từ Simple Icons hoặc brand guidelines
- [ ] **No layout shift on hover** - Dùng color/opacity transitions, không scale
- [ ] **Color consistency** - Dùng design tokens, không hardcoded values

#### Interaction

- [ ] **Cursor pointer** - Tất cả clickable elements có `cursor-pointer`
- [ ] **Hover feedback** - Visible hover states cho interactive elements
- [ ] **Active states** - Active feedback cho buttons
- [ ] **Focus visible** - Clear focus rings cho keyboard navigation
- [ ] **Transition smooth** - 150-300ms transitions, không quá chậm

#### Light/Dark Mode

- [ ] **Contrast ratios** - Tối thiểu 4.5:1 cho body text
- [ ] **Glass visibility** - `bg-white/80+` trong light mode
- [ ] **Border visibility** - Borders hiển thị trong cả 2 modes
- [ ] **Test both modes** - Manual test trong cả light và dark

#### Layout

- [ ] **Floating spacing** - `top-4 left-4 right-4` cho floating navbars
- [ ] **Content padding** - Account cho fixed elements
- [ ] **Container max-width** - Nhất quán (`max-w-7xl`)
- [ ] **Responsive test** - Test tại 320px, 768px, 1024px, 1440px

#### Accessibility

- [ ] **Alt text** - Tất cả images có meaningful alt text
- [ ] **Form labels** - Tất cả inputs có labels hoặc `aria-label`
- [ ] **Color contrast** - WCAG AA compliant (4.5:1)
- [ ] **Keyboard navigation** - Tab order logical, focus visible
- [ ] **Semantic HTML** - Dùng proper heading hierarchy, landmarks
- [ ] **Reduced motion** - Respect `prefers-reduced-motion`

#### Performance

- [ ] **Image optimization** - WebP format, lazy loading
- [ ] **Font loading** - `font-display: swap`
- [ ] **Critical CSS** - Inline critical CSS
- [ ] **No unused CSS** - Purge unused styles

#### Code Quality

- [ ] **Semantic class names** - `.btn-primary` không `.button-blue-big`
- [ ] **Consistent formatting** - Proper indentation, line breaks
- [ ] **Comments** - Complex logic có comments
- [ ] **No console.log** - Remove debug statements

### 10.2 Review Template

```markdown
# UI Review Checklist

## Project: [Project Name]

### Visual Quality
- [ ] Icons are SVG, not emojis
- [ ] Icon sizing consistent
- [ ] Brand logos accurate
- [ ] No layout shift on hover
- [ ] Colors use design tokens

Score: ___ / 5

### Interaction
- [ ] Cursor pointer on clickables
- [ ] Hover states visible
- [ ] Active states present
- [ ] Focus rings visible
- [ ] Transitions smooth (150-300ms)

Score: ___ / 5

### Light/Dark Mode
- [ ] Contrast ratios met (4.5:1)
- [ ] Glass elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Both modes tested

Score: ___ / 5

### Layout & Responsive
- [ ] Floating elements have spacing
- [ ] Content accounts for fixed elements
- [ ] Container widths consistent
- [ ] Responsive at all breakpoints

Score: ___ / 5

### Accessibility
- [ ] Alt text on all images
- [ ] Form inputs have labels
- [ ] Keyboard navigation works
- [ ] Semantic HTML used
- [ ] Reduced motion respected

Score: ___ / 5

### Performance
- [ ] Images optimized
- [ ] Fonts loaded efficiently
- [ ] No unused CSS/JS
- [ ] Lighthouse score > 90

Score: ___ / 5

## Overall Score: ___ / 30

## Issues Found:
1.
2.
3.

## Recommendations:
1.
2.
3.
```

---

## 11. Ví Dụ Thực Tế

### 11.1 Example 1: SaaS Landing Page

**Request:** "Create a landing page for a B2B SaaS project management tool"

**Search Queries:**

```bash
# 1. Product type
python3 .shared/scripts/search.py "saas b2b project management" --domain product

# 2. Style
python3 .shared/scripts/search.py "professional clean modern tech" --domain style

# 3. Color
python3 .shared/scripts/search.py "saas b2b tech professional" --domain color

# 4. Typography
python3 .shared/scripts/search.py "professional modern tech" --domain typography

# 5. Landing structure
python3 .shared/scripts/search.py "saas b2b feature-centric social-proof" --domain landing

# 6. UX
python3 .shared/scripts/search.py "conversion optimization" --domain ux
python3 .shared/scripts/search.py "trust signals credibility" --domain ux
```

**Design System Output:**

```yaml
colors:
  primary: "#2563EB"      # Blue (trust, professional)
  secondary: "#7C3AED"    # Violet (innovation)
  cta: "#10B981"          # Green (action)

typography:
  heading: "Inter"
  body: "Inter"

style:
  characteristics:
    - "Clean card-based layout"
    - "Subtle shadows"
    - "Professional imagery"
    - "Data-driven visuals"

sections:
  - "Hero with clear value proposition"
  - "Social proof (logos, customer count)"
  - "Feature grid with screenshots"
  - "Pricing table"
  - "Testimonials"
  - "Final CTA"
```

### 11.2 Example 2: E-commerce Product Page

**Request:** "Design a product page for a luxury skincare brand"

**Search Queries:**

```bash
# 1. Product
python3 .shared/scripts/search.py "ecommerce luxury beauty skincare" --domain product

# 2. Style
python3 .shared/scripts/search.py "elegant sophisticated luxury minimalist" --domain style

# 3. Color
python3 .shared/scripts/search.py "luxury beauty skincare elegant" --domain color

# 4. Typography
python3 .shared/scripts/search.py "elegant luxury sophisticated" --domain typography

# 5. Chart (nếu có reviews visualization)
python3 .shared/scripts/search.py "rating distribution comparison" --domain chart
```

**Key Design Decisions:**

- **Color:** Soft neutrals (cream, beige) với gold accents
- **Typography:** Serif headings (Playfair Display) + Sans body (Inter)
- **Style:** Minimal, plenty of whitespace, high-quality imagery
- **Trust elements:** Reviews, certifications, ingredient transparency

### 11.3 Example 3: Analytics Dashboard

**Request:** "Build a dashboard for tracking marketing metrics"

**Search Queries:**

```bash
# 1. Product
python3 .shared/scripts/search.py "dashboard analytics b2b saas" --domain product

# 2. Style
python3 .shared/scripts/search.py "professional data-heavy clean" --domain style

# 3. Chart types
python3 .shared/scripts/search.py "trend comparison funnel distribution" --domain chart

# 4. UX
python3 .shared/scripts/search.py "data visualization dashboard" --domain ux
python3 .shared/scripts/search.py "information density" --domain ux
```

**Dashboard Components:**

- **Header:** User profile, date range picker, notifications
- **KPI Cards:** 4-6 key metrics với trend indicators
- **Charts:**
  - Line chart cho trends over time
  - Bar chart cho comparison
  - Donut chart cho distribution
- **Data Tables:** Sortable, filterable, paginated
- **Filters:** Sidebar or top bar for filtering data

---

## 12. Hướng Dẫn Mở Rộng

### 12.1 Thêm Style Mới

**Step 1:** Thêm vào `data/styles.json`

```json
{
  "id": "new-style",
  "name": "New Style Name",
  "category": "modern",
  "description": "Style description",
  "characteristics": [
    "Characteristic 1",
    "Characteristic 2"
  ],
  "best_for": ["dashboard", "landing"],
  "color_schemes": ["gradient", "pastel"],
  "frameworks": ["tailwind", "css"],
  "example_classes": "class-names-here",
  "keywords": ["keyword1", "keyword2"]
}
```

**Step 2:** Test search

```bash
python3 .shared/scripts/search.py "keyword1" --domain style
```

### 12.2 Thêm Color Palette Mới

**Step 1:** Thêm vào `data/colors.json`

```json
{
  "id": "new-palette",
  "name": "Palette Name",
  "industry": "Industry",
  "primary": "#HEX",
  "secondary": "#HEX",
  "cta": "#HEX",
  "background": "#HEX",
  "background_secondary": "#HEX",
  "text_primary": "#HEX",
  "text_secondary": "#HEX",
  "text_muted": "#HEX",
  "border": "#HEX",
  "success": "#HEX",
  "warning": "#HEX",
  "error": "#HEX",
  "info": "#HEX",
  "tailwind_config": {
    "primary": "color-name",
    "secondary": "color-name",
    "cta": "color-name"
  },
  "keywords": ["keyword1", "industry"]
}
```

**Step 2:** Verify contrast ratios

Use: https://webaim.org/resources/contrastchecker/

### 12.3 Thêm Typography Pairing Mới

**Step 1:** Thêm vào `data/typography.json`

```json
{
  "id": "new-pairing",
  "name": "Pairing Name",
  "category": "modern",
  "heading_font": "Font Name",
  "body_font": "Font Name",
  "code_font": "Font Name",
  "weights": [400, 500, 600, 700],
  "import": "@import url('https://fonts.googleapis.com/css2?family=...');",
  "best_for": ["saas", "dashboard"],
  "keywords": ["keyword1", "keyword2"]
}
```

### 12.4 Thêm Stack Mới

**Step 1:** Tạo thư mục templates

```
templates/
└── new-stack/
    ├── button.html
    ├── card.html
    ├── form.html
    └── modal.html
```

**Step 2:** Thêm vào stack reference trong SKILL.md

```markdown
| `new-stack` | Description | Coverage examples |
```

**Step 3:** Tạo stack data trong `data/stacks/new-stack.json`

```json
{
  "name": "New Stack",
  "file_extension": ".ext",
  "component_pattern": "pattern",
  "styling": "css/styled/etc",
  "common_patterns": {
    "button": "button code pattern",
    "card": "card code pattern"
  }
}
```

### 12.5 Contributing Guidelines

1. **Fork repository**
2. **Create branch:** `git checkout -b feature/new-style`
3. **Add data:** Follow schema trong "Hướng Dẫn Mở Rộng"
4. **Test:** Run search script để verify
5. **Submit PR:** Với clear description

---

## 13. Troubleshooting

### 13.1 Common Issues

#### Issue 1: Search Script Not Found

**Error:** `python3: can't open file '.shared/scripts/search.py'`

**Solution:**

```bash
# Verify file exists
ls -la .shared/scripts/search.py

# If missing, create from template
mkdir -p .shared/scripts
# Copy search script template
```

#### Issue 2: Python Version Too Old

**Error:** `SyntaxError: invalid syntax` (f-strings require Python 3.6+)

**Solution:**

```bash
# Check version
python3 --version

# Upgrade to Python 3.7+
# macOS
brew upgrade python3

# Ubuntu
sudo apt install python3.9

# Windows
winget upgrade Python.Python.3.12
```

#### Issue 3: No Search Results

**Issue:** Search returns empty results

**Troubleshooting:**

```bash
# 1. Verify keyword
python3 .shared/scripts/search.py "minimalism" --domain style

# 2. Try broader keyword
python3 .shared/scripts/search.py "minimal" --domain style

# 3. Check domain is valid
python3 .shared/scripts/search.py "test" --domain style

# 4. Verify data files exist
ls -la data/
```

#### Issue 4: Low Contrast Scores

**Issue:** WCAG contrast checker fails

**Solution:**

```yaml
# Adjust color values
colors:
  text_primary: "#0F172A"  # Darker for better contrast
  text_secondary: "#475569"  # Was #94A3B8, too light

# Verify with tool
# https://webaim.org/resources/contrastchecker/
```

### 13.2 Debug Mode

Enable debug output in search script:

```bash
python3 .shared/scripts/search.py "keyword" --domain style --debug
```

Expected output:

```json
{
  "query": "keyword",
  "domain": "style",
  "results_found": 5,
  "results": [...]
}
```

---

## 14. FAQ

### Q1: Skill này khác gì các UI/UX tools khác?

**A:** UI/UX Pro Max là:
- **Context-aware**: Hiểu project type, industry, target audience
- **Stack-specific**: Hướng dẫn implementation cụ thể cho từng framework
- **Comprehensive**: Không chỉ color/style, còn có UX best practices, accessibility, performance
- **Integrated**: Hoạt động trực tiếp trong Claude Code workflow

### Q2: Tôi có thể dùng cho production không?

**A:** Có, nhưng:
- ✅ Code generated là production-ready
- ✅ Follow accessibility standards (WCAG AA)
- ✅ Performance optimized
- ⚠️ Nên review và customize cho brand guidelines
- ⚠️ Test trên browsers và devices thực tế

### Q3: Làm sao để customize cho brand của tôi?

**A:**

1. **Create brand tokens:**

```css
:root {
  --color-primary: #YOUR_BRAND_COLOR;
  --color-secondary: #YOUR_SECONDARY_COLOR;
  /* ... */
}
```

2. **Search với brand keywords:**

```bash
python3 .shared/scripts/search.py "YOUR_BRAND_PERSONALITY" --domain style
```

3. **Override colors trong generated code**

### Q4: Có support cho mobile apps không?

**A:** Có, cho:
- ✅ React Native
- ✅ Flutter
- ✅ SwiftUI (iOS)

```bash
python3 .shared/scripts/search.py "mobile pattern" --stack react-native
```

### Q5: Làm sao để request feature mới?

**A:**

1. Check GitHub Issues: https://github.com/your-repo/issues
2. Create new issue với template:
   - Feature description
   - Use cases
   - Examples
3. Hoặc submit PR với contribution guidelines (Section 12.5)

### Q6: Search accuracy có cao không?

**A:** Search engine sử dụng:
- Keyword matching + fuzzy search
- Category filtering
- Relevance scoring

**Tips cho better results:**
- Be specific: "saas b2b healthcare" > "app"
- Try multiple keywords
- Combine domains

### Q7: Có integration với tools khác không?

**A:** Currently:
- ✅ shadcn/ui MCP (component search)
- ✅ Claude Code (native)
- 🔄 Figma (planned)
- 🔄 Framer (planned)

### Q8: License?

**A:** MIT License - Free cho commercial và personal use.

---

## Appendix

### A. Quick Reference Card

```bash
# Search Commands
python3 .shared/scripts/search.py "<keyword>" --domain <domain> [--stack <stack>] [-n <number>]

# Domains: product, style, color, typography, landing, chart, ux, prompt
# Stacks: html-tailwind, react, nextjs, vue, svelte, swiftui, react-native, flutter, shadcn

# Example
python3 .shared/scripts/search.py "glassmorphism" --domain style -n 3
```

### B. Keyboard Shortcuts (VS Code)

| Shortcut | Action |
|----------|--------|
| `Alt+Shift+F` | Format document |
| `Ctrl+/` | Toggle comment |
| `Ctrl+D` | Select next occurrence |
| `Alt+Up/Down` | Move line up/down |

### C. Useful Resources

- **Color Contrast:** https://webaim.org/resources/contrastchecker/
- **Tailwind Docs:** https://tailwindcss.com/docs
- **Accessibility:** https://www.w3.org/WAI/WCAG21/quickref/
- **Icon Libraries:**
  - Heroicons: https://heroicons.com/
  - Lucide: https://lucide.dev/
  - Phosphor: https://phosphoricons.com/
  - Simple Icons: https://simpleicons.org/

### D. Changelog

#### Version 2.0.0 (Current)
- ✨ Complete restructure
- ✨ Vietnamese translation
- ✨ Enhanced documentation
- ✨ More examples
- ✨ Troubleshooting section
- ✨ FAQ section

#### Version 1.0.0
- 🎉 Initial release

---

## Contact & Support

- **Documentation:** [SKILL.md](./SKILL.md)
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

**Made with ❤️ by the UI/UX Pro Max team**

---

*Last updated: 2025-01-23*
