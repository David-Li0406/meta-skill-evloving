---
name: publish-article
description: "Publish blog articles to aiandi.dev. Frontmatter, SEO, deployment, verification, announcement. Use at PUBLISH stage of blog pipeline."
---

# Publish Article Skill

**Purpose:** Deploy a finished article and verify it's live correctly.

---

## When to Use

At the PUBLISH stage, after POLISH is complete.

---

## Pre-Publish Checklist

Before publishing, verify:

- [ ] POLISH stage gate passed
- [ ] Article is in `pipeline/active/NNN-slug/05-draft.md`
- [ ] All images/assets are ready
- [ ] Slug is URL-friendly (lowercase, hyphens, no special chars)

---

## Frontmatter Template

```yaml
---
title: "Article Title"
description: "One-sentence description for SEO and social sharing (150-160 chars ideal)"
pubDate: YYYY-MM-DD
updatedDate: YYYY-MM-DD  # Optional, for updates
heroImage: ./hero.jpg  # Optional, path relative to article
---
```

### Frontmatter Guidelines

**Required Fields:**
- `title` - Article title (string)
- `description` - SEO description (string)
- `pubDate` - Publication date (YYYY-MM-DD format)

**Optional Fields:**
- `updatedDate` - Last update date (YYYY-MM-DD format)
- `heroImage` - Hero image path relative to article file

**Title:**
- No colons (commit to one focus)
- Front-load important words (SEO)
- Match the article's actual teaching

**Description:**
- Complete sentence
- Include key terms for search
- Compelling enough to click
- 150-160 characters ideal

**Hero Image:**
- 1200x630px ideal (social sharing)
- Relevant to content
- Path relative to article file (e.g., `./hero.jpg`)
- Not required - skip if no good image
- Fallback image used automatically if omitted

---

## Publishing Process

### 1. Prepare Article

```bash
# Move draft to content, archive pipeline folder
mv packages/blog/pipeline/active/NNN-slug/05-draft.md packages/blog/src/content/blog/NNN-slug.md
mv packages/blog/pipeline/active/NNN-slug packages/blog/pipeline/published/
```

### 2. Add/Verify Frontmatter

Ensure all required fields are present and formatted correctly.

### 3. Handle Assets

```bash
# If article has images
mkdir -p packages/blog/public/blog/[slug]/
# Copy images to that directory
# Update image paths in article to /blog/[slug]/[image]
```

### 4. Local Verification

```bash
cd packages/blog
bun run dev
# Visit http://localhost:4321/blog/[slug]
```

**Check:**
- [ ] Page renders without errors
- [ ] Images load
- [ ] Code blocks formatted correctly
- [ ] Links work
- [ ] No layout issues
- [ ] Mobile view acceptable

### 5. Build Test

```bash
bun run build
bun run preview
```

**Check:**
- [ ] Build completes without errors
- [ ] Preview matches dev

### 6. Deploy

```bash
# Commit changes
git add packages/blog/src/content/blog/[slug].md
git add packages/blog/public/blog/[slug]/  # If assets
git commit -m "blog: publish [slug]"
git push
```

Deployment is automatic via CI/CD (or manual if not configured).

### 7. Production Verification

After deploy completes:
- [ ] Visit live URL: `https://aiandi.dev/blog/[slug]`
- [ ] Page loads correctly
- [ ] Social sharing preview works (use social card validators)
- [ ] RSS feed updated

---

## Update Pipeline Tracking

Edit `packages/blog/PIPELINE.md`:

1. Move article from "Current Articles" to show PUBLISHED status
2. Add publish date
3. Clear from active work

---

## Announcement (Optional)

**Channels to consider:**
- Twitter/X
- Dev.to (cross-post)
- Reddit (relevant subreddits)
- Hacker News (if appropriate)
- LinkedIn

**Cross-posting:**
- Dev.to supports canonical URL - point back to aiandi.dev
- Adjust formatting for platform
- Don't spam - only share where genuinely relevant

---

## Post-Publish

### Monitor (First 24-48 Hours)

- Check for errors in analytics
- Watch for comments/feedback
- Be ready to fix issues quickly

---

## Quality Gate

**Gate question:** Live and rendering correctly?

**Checklist:**
- [ ] Article accessible at expected URL
- [ ] No rendering errors
- [ ] Images load
- [ ] Social sharing preview works
- [ ] PIPELINE.md updated

---

## Rollback

If something is wrong after publish:

```bash
# Revert the commit
git revert HEAD
git push

# Or quick fix
# Edit, commit, push
```

Better to unpublish and fix than leave broken content live.

---

*Publish is not the end. It's the beginning of the article's life in the world.*
