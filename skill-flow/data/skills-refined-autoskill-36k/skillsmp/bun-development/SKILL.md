---
name: bun-development
description: Comprehensive Bun development guidance for fast builds, package management, and runtime optimization in JavaScript/TypeScript projects
---

## What I Cover

This skill provides guidance on using Bun, a fast JavaScript runtime and package manager, for JavaScript/TypeScript development. It covers:

- Package management with `bun install`, `bun add`, `bun remove`
- Running scripts with `bun run`
- Building and bundling applications
- Runtime optimization techniques
- Integration with build tools like Vite and frameworks like SvelteKit

## Common Patterns

### Package Management

- Use `bun install` instead of `npm install` for faster dependency resolution
- Add dependencies with `bun add package-name`
- Run scripts with `bun run script-name`

### Build Optimization

- Leverage Bun's fast transpiler for development builds
- Use Bun for production builds when possible

### Project Structure

- Organize code with clear separation of concerns
- Use TypeScript for type safety

## Best Practices

- Prefer Bun over npm/yarn for package management when possible
- Use `bun run` for executing scripts to take advantage of Bun's speed
- Optimize bundle sizes by tree-shaking unused dependencies
- Monitor performance with Bun's built-in tools

## Related Skills

- sveltekit-development: For building SvelteKit applications
- frontend-design: For creating user interfaces
- software-architecture: For overall application structure

### Project-Specific Examples

In this GoPayShortcuts project, Bun is utilized in the frontend build process for production deployments. The `predeploy` script in `frontend/package.json` uses `"NODE_ENV=production bun run build"` to take advantage of Bun's high-performance build capabilities, ensuring fast and efficient production builds for the SvelteKit application.