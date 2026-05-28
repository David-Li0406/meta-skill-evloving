# React + TailwindCSS to WeChat Mini Program Migration Skill

This repository contains the definition and resources for an AI Agent Skill designed to migrate React + TailwindCSS web applications to native WeChat Mini Programs.

## Overview

The **React to WeChat Mini Program Migrator** skill provides a systematic workflow for converting modern web tech stacks (React, TailwindCSS) into the specific architecture of WeChat Mini Programs (WXML, WXSS, logical layer).

It ensures a functional and stylistically faithful conversion by mapping modern web development patterns to Mini Program equivalents.

## Repository Structure

- **`SKILL.md`**: The core instruction file for the AI agent. It details the step-by-step migration process, from project analysis to final debugging.
- **`references/`**: Contains helper documents.
  - `MIGRATION_MAP.md`: Detailed mapping tables for HTML-to-WXML, Event bindings, Lifecycles, and APIs.

## How It Works

The skill guides the agent through the following phases:

1.  **Analysis & Setup**: Analyzing the React source and creating the Mini Program directory structure.
2.  **Component & JSX Conversion**: Transforming React components into WXML templates (e.g., `div` → `view`, `className` → `class`).
3.  **TailwindCSS to WXSS**: Converting utility classes to static WXSS styles, handling unit conversion (`rem` → `rpx`), and addressing WXSS limitations.
4.  **Logic Migration**: Adapting React Hooks (`useState`, `useEffect`) to Mini Program `data` and lifecycle methods (`onLoad`, `onShow`).
5.  **API Replacement**: swapping browser APIs (e.g., `fetch`, `localStorage`) with WeChat native APIs (`wx.request`, `wx.setStorageSync`).

## Resources

See [`references/MIGRATION_MAP.md`](./references/MIGRATION_MAP.md) for a comprehensive lookup table covering:
- Component Tags
- Event Bindings
- Lifecycle Methods
- API Equivalents
- Tailwind Class Conversions

## License

MIT
