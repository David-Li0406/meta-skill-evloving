---
name: monorepo-commands
description: Comprehensive reference for npm scripts in a full-stack monorepo containing FastAPI backend, React Native mobile app, and React/Vite web app. Use when working with build, test, lint, or typecheck commands, or when helping with development workflows in this monorepo structure.
---

# Monorepo Commands

Reference for all npm scripts available in this full-stack monorepo project.

## Project Structure

This monorepo contains three main packages:
- **API Server**: FastAPI (Python)
- **Mobile App**: React Native (TypeScript)
- **Web App**: React + Vite (TypeScript)

## Command Categories

### Global Commands

Commands that run across the entire monorepo:

- `npm run test` - Run all tests (mobile Jest + API pytest)
- `npm run typecheck` - Type check all packages (mobile, web, API)
- `npm run lint` - Lint all packages (mobile, web, API)

### API Server Commands

FastAPI backend commands:

- `npm run api:test` - Run pytest tests
- `npm run api:typecheck` - Run mypy type checking
- `npm run api:lint` - Run Ruff linter

### Mobile App Commands

React Native commands:

- `npm run mobile:ios` - Build and run on iOS simulator (requires Xcode)
- `npm run mobile:android` - Build and run on Android emulator (requires Android SDK)
- `npm run mobile:test` - Run Jest tests
- `npm run mobile:typecheck` - Run TypeScript type checking
- `npm run mobile:lint` - Run ESLint

### Web App Commands

React + Vite commands:

- `npm run web:dev` - Start development server with HMR (http://localhost:5173)
- `npm run web:build` - Build for production (outputs to `web-app/dist`)

## Detailed Command Reference

For complete details on each command including descriptions and usage notes, see:
- [references/commands-reference.md](references/commands-reference.md)

## Usage Patterns

When working with this monorepo:

1. **Starting development**: Use `npm run web:dev` for web or `npm run mobile:ios`/`mobile:android` for mobile
2. **Before committing**: Run `npm run lint` and `npm run typecheck` to catch issues
3. **Running tests**: Use `npm run test` for all tests or specific commands for targeted testing
4. **Building for production**: Use `npm run web:build` for web deployment

## Technology Stack

- **Backend**: Python, FastAPI, pytest, mypy, Ruff
- **Mobile**: React Native, TypeScript, Jest, ESLint
- **Web**: React, Vite, TypeScript, ESLint
- **Monorepo**: npm workspaces
