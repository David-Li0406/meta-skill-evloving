---
name: react-best-practices
description: Use this skill when you need to follow best practices and performance optimization techniques for developing high-performance React applications.
---

# React Best Practices

This skill provides a comprehensive set of rules and best practices for developing high-performance React applications, optimized for both human developers and AI-assisted workflows.

## Abstract

This guide offers performance optimization techniques for React and Next.js applications, containing over 40 rules categorized by impact, from critical optimizations like eliminating waterfalls and reducing bundle size to incremental improvements. Each rule includes detailed explanations, real-world examples, and specific impact metrics to assist in automated refactoring and code generation.

## Table of Contents

1. [Eliminating Waterfalls](#1-eliminating-waterfalls) **CRITICAL**
   - 1.1 [Defer Await Until Needed](#11-defer-await-until-needed)
   - 1.2 [Dependency-Based Parallelization](#12-dependency-based-parallelization)
   - 1.3 [Prevent Waterfall Chains in API Routes](#13-prevent-waterfall-chains-in-api-routes)
   - 1.4 [Promise.all() for Independent Operations](#14-promiseall-for-independent-operations)
   - 1.5 [Strategic Suspense Boundaries](#15-strategic-suspense-boundaries)
2. [Bundle Size Optimization](#2-bundle-size-optimization) **CRITICAL**
   - 2.1 [Avoid Barrel File Imports](#21-avoid-barrel-file-imports)
   - 2.2 [Conditional Module Loading](#22-conditional-module-loading)
   - 2.3 [Defer Non-Critical Third-Party Libraries](#23-defer-non-critical-third-party-libraries)
   - 2.4 [Dynamic Imports for Heavy Components](#24-dynamic-imports-for-heavy-components)
   - 2.5 [Preload Based on User Intent](#25-preload-based-on-user-intent)
3. [Server-Side Performance](#3-server-side-performance) **HIGH**
   - 3.1 [Authenticate Server Actions Like API Routes](#31-authenticate-server-actions-like-api-routes)
   - 3.2 [Avoid Duplicate Serialization in RSC Props](#32-avoid-duplicate-serialization-in-rsc-props)