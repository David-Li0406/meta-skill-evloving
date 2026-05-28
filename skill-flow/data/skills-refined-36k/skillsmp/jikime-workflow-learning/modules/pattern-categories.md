# Pattern Categories

Detailed documentation for the five types of learning patterns captured by the system.

## 1. Error Resolution

Captures how specific errors were resolved:

```yaml
category: error_resolution
pattern:
  trigger: "TypeError: Cannot read properties of undefined"
  context: "React component accessing props before mount"
  resolution: "Add null check or use optional chaining"
  example: |
    // Before
    const value = data.nested.property;

    // After
    const value = data?.nested?.property;
confidence: 0.92
frequency: 5
last_used: "2024-01-22"
```

## 2. User Corrections

Patterns from user corrections to Claude's output:

```yaml
category: user_correction
pattern:
  original: "Claude suggested inline styles"
  correction: "User preferred Tailwind CSS classes"
  learning: "This project uses Tailwind CSS for styling, avoid inline styles"
  scope: project
confidence: 0.88
frequency: 3
```

## 3. Workarounds

Solutions to framework/library quirks:

```yaml
category: workaround
pattern:
  technology: "Next.js 14"
  issue: "App Router dynamic imports with SSR"
  workaround: |
    Use 'use client' directive or dynamic import with ssr: false
    import dynamic from 'next/dynamic'
    const Component = dynamic(() => import('./Component'), { ssr: false })
confidence: 0.95
source: "official_docs"
```

## 4. Debugging Techniques

Effective debugging approaches:

```yaml
category: debugging
pattern:
  symptom: "State not updating in React"
  technique: "Check for object/array mutation instead of new reference"
  steps:
    1. "Verify state update uses new reference"
    2. "Check useEffect dependencies"
    3. "Look for direct mutation patterns"
  success_rate: 0.87
```

## 5. Project Conventions

Project-specific patterns:

```yaml
category: project_convention
pattern:
  domain: "API responses"
  convention: "All API responses follow { success, data, error } structure"
  example: |
    interface ApiResponse<T> {
      success: boolean;
      data?: T;
      error?: { code: string; message: string };
    }
  enforced: true
```

---

Version: 1.0.0
Source: jikime-workflow-learning SKILL.md
