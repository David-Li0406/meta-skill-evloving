---
name: github-pages-deployment
description: Comprehensive GitHub Pages deployment guidance for static site hosting, CI/CD pipelines, and automated publishing
---

# What I Cover

This skill provides comprehensive guidance on deploying static sites to GitHub Pages, including initial setup, configuring CI/CD pipelines with GitHub Actions, handling custom domains, and implementing automated publishing workflows. It covers both manual and automated deployment strategies, troubleshooting common issues, and optimizing for performance.

# Common Patterns

- **Static Site Generation**: Using frameworks like SvelteKit with adapter-static for prerendered sites
- **GitHub Actions Workflows**: Automated build and deploy pipelines triggered on push to main branch
- **Asset Handling**: Placing .nojekyll in static folder to prevent Jekyll processing of assets
- **Base Path Configuration**: Setting up base paths for deployments in subfolders or custom domains
- **Branch-based Deployments**: Using gh-pages branch for clean separation of source and built code

# Best Practices

- Always use static adapters for frameworks that support it (e.g., SvelteKit's adapter-static)
- Implement CI/CD pipelines to ensure consistent, automated deployments
- Use .nojekyll when your site has underscores in filenames or uses asset folders
- Configure base paths dynamically using environment variables for flexibility
- Enable GitHub Pages settings in repository settings with appropriate source branch
- Test deployments locally before pushing to avoid broken builds
- Use custom domains with proper DNS configuration for production sites

# Related Skills

- frontend-developer: For building the static sites that get deployed
- deployment-specialist: For advanced CI/CD and infrastructure deployment patterns
- sveltekit-development: For SvelteKit-specific deployment configurations

## Project-Specific Examples

In this GoPayShortcuts SvelteKit project, we demonstrate several GitHub Pages deployment patterns:

- **Adapter Configuration**: Using `@sveltejs/adapter-static` with `pages: 'build'` and `assets: 'build'` for complete static generation
- **Base Path Handling**: Dynamic base path configuration using `process.env.BASE_PATH` to support both development and production deployments
- **Jekyll Bypass**: Including `.nojekyll` file in the static directory to ensure proper handling of SvelteKit-generated assets
- **Build Output**: The adapter generates a fully static site in the `build` directory, ready for GitHub Pages hosting</content>
<parameter name="filePath">D:\Git\GoPayShortcuts\.opencode\skill\github-pages-deployment\SKILL.md