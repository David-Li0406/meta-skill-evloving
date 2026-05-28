---
name: nextjs-turborepo-web-development
description: Use this skill when building modern full-stack web applications with Next.js and Turborepo, optimizing for performance and managing monorepos.
---

# Skill Body

## Overview

This skill provides a comprehensive guide for building modern full-stack web applications using **Next.js**, **Turborepo**, and **RemixIcon**.

- **Next.js**: A React framework that supports server-side rendering (SSR), static site generation (SSG), and more.
- **Turborepo**: A high-performance build system for managing monorepos in JavaScript/TypeScript projects.
- **RemixIcon**: A library offering over 3,100 SVG icons in outlined and filled styles.

## When to Use This Skill

- Building new full-stack web applications with modern React.
- Setting up monorepos with multiple applications and shared packages.
- Implementing server-side rendering and static generation.
- Optimizing build performance with intelligent caching strategies.
- Creating consistent user interfaces with professional iconography.
- Managing workspace dependencies across multiple projects.
- Deploying production-ready applications with proper optimization.

## Stack Selection Guide

### Single Application: Next.js + RemixIcon

Use this setup for standalone applications such as:
- E-commerce sites
- Marketing websites
- SaaS applications
- Documentation sites
- Blogs and content platforms

**Setup:**
```bash
npx create-next-app@latest my-app
cd my-app
npm install remixicon
```

### Monorepo: Next.js + Turborepo + RemixIcon

Use this setup for building multiple applications with shared code, such as:
- Microfrontends
- Multi-tenant platforms
- Internal tools with shared component libraries
- Multiple apps (web, admin, mobile-web) sharing logic
- Design systems with documentation sites

**Setup:**
```bash
npx create-turbo@latest my-monorepo
# Then configure Next.js apps in the apps/ directory
# Install remixicon in shared UI packages
```

## Key Features

| Feature | Next.js | Turborepo | RemixIcon |
|---------|---------|-----------|-----------|
| Primary Use | Web framework | Build system | UI icons |
| Best For | SSR/SSG apps | Monorepos | Consistent iconography |