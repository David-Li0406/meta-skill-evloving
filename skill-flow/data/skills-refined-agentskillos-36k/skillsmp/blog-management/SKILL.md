---
name: blog-management
description: Personal blog management with Eleventy and Cloudflare Workers. Use when user mentions blog, publishing posts, blog deployment, tj-zhang.com, or writing articles for the blog. Covers content workflow from Obsidian to published post.
---

# Blog Management

Eleventy static blog hosted on Cloudflare Workers.

## Quick Reference

**Repository:** `~/projects/tj-zhang-blog/`
**Live Site:** [tj-zhang.com](https://tj-zhang.com)
**Deploy:** `pnpm ship`

## Content Creation Workflow

Blog posts live in `4_Writing/blog/` in Obsidian (symlinked to the blog repo). Write directly there in blog format.

1. **Create post** in `4_Writing/blog/` with frontmatter:
   ```markdown
   ---
   title: "Article Title"
   description: "Brief description"
   date: 2025-01-07
   tags: ["tag1", "tag2"]
   ---

   Content...
   ```

   - **No H1 header** — title comes from frontmatter
   - **All code blocks need language hints** (e.g., \`\`\`bash) — required for rendering

2. **Deploy:**
   ```bash
   cd ~/projects/tj-zhang-blog && pnpm ship
   ```

3. **Verify** — Check the live URL to confirm the post is up.

## Why No H1 in Markdown

- Industry standard (Dan Abramov, Kent C. Dodds style)
- Single source of truth: title from frontmatter only
- Template handles title rendering
- No duplicate H1 headers

## Architecture

- **Eleventy:** Static site generation
- **Cloudflare Workers:** Hosting with global CDN
- **Local builds:** Faster than CI/CD for single-author blog
