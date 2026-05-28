---
name: brand-identity
description: Provides the single source of truth for SpecsVibeCode brand guidelines, design tokens, technology choices, and voice/tone. Use this skill whenever generating UI components, styling applications, writing copy, or creating user-facing assets to ensure brand consistency across the Rails 8 monolith.
---

# Brand Identity & Guidelines

**Brand Name:** SpecsVibeCode

This skill defines the core constraints for visual design and technical implementation for SpecsVibeCode. You must adhere to these guidelines strictly to maintain consistency across the platform.

## Reference Documentation

Depending on the task you are performing, consult the specific resource files below. Do not guess brand elements; always read the corresponding file.

### For Visual Design & UI Styling
If you need exact colors, fonts, border radii, or spacing values, read:
👉 **[`resources/design-tokens.json`](resources/design-tokens.json)**

### For Coding & Component Implementation
If you are generating code, choosing libraries, or structuring UI components, read the technical constraints here:
👉 **[`resources/tech-stack.md`](resources/tech-stack.md)**

### For Copywriting & Content Generation
If you are writing marketing copy, error messages, documentation, or user-facing text, read the persona guidelines here:
👉 **[`resources/voice-tone.md`](resources/voice-tone.md)**

## Quick Reference

### Core Brand Attributes
- **Industry:** SaaS / Developer Tools / Document Generation
- **Target Audience:** Software teams, product managers, technical writers
- **Value Proposition:** AI-powered specification document generation that transforms ideas into comprehensive, professional specs
- **Personality:** Professional, intelligent, efficient, developer-friendly

### Design Philosophy
- **Dark-First Design:** Deep black backgrounds (#0A0A0A) with subtle layers for depth
- **Bold Red Accents:** Primary actions and key UI elements use vibrant red (#EF4444)
- **Minimalist & Clean:** Material Design-inspired widgets with generous rounded corners
- **High Contrast:** Pure white text on dark backgrounds for maximum readability
- **Card-Based Layout:** Floating cards with subtle shadows for content organization
- **Responsive:** Mobile-first approach with desktop optimization
- **Accessibility:** WCAG 2.1 AA compliance with enhanced contrast ratios

### Key User Flows
1. **Authentication:** OAuth-based login via Supabase (GitHub, Google)
2. **Project Creation:** Wizard-based document generation flow
3. **Document Management:** List, view, edit, export specifications
4. **Subscription Management:** Freemium model with usage-based billing
