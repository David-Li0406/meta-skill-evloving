---
name: Jekyll Development Workflow
description: Complete workflow for developing, testing, and deploying Jekyll blog changes
version: 1.1.0
triggers:
  - Starting Jekyll server
  - Making content changes (posts, pages)
  - Modifying layouts or styles
  - Updating configuration
  - Debugging server failures
  - Need to verify changes before deployment
---

## Context

This blog uses Jekyll 4.3.2 with a custom Economist-inspired theme, deployed via GitHub Actions to GitHub Pages. The workflow is optimized to avoid local server issues (SSL, remote theme fetching) by relying on pre-commit validation and GitHub Actions for builds.

**Environment**:
- Jekyll 4.3.2
- Ruby 3.3 (via rbenv)
- Custom Economist theme (`_sass/economist-theme.scss`)
- GitHub Actions for CI/CD
- Pre-commit hook for validation

## Step-by-Step Instructions

### 0. Environment Pre-Flight Checklist (CRITICAL)

**BEFORE attempting ANY `jekyll serve` command**, run this diagnostic to avoid token waste:

```bash
echo "=== Jekyll Environment Diagnostic ==="
echo "Ruby: $(ruby -v)"
echo "Bundler: $(bundle -v 2>/dev/null || echo '❌ NOT INSTALLED')"
echo "Jekyll: $(bundle exec jekyll -v 2>/dev/null || echo '❌ NOT INSTALLED')"
echo "Port 4000: $(lsof -ti:4000 && echo '⚠️ BUSY' || echo '✅ FREE')"
echo "Config: $([ -f _config_dev.yml ] && echo '✅ YES' || echo '⚠️ NO')"
echo "==================================="
```

**Decision Tree**:

| Diagnostic Result | Fix Command | Wait Until Green |
|------------------|-------------|------------------|
| Ruby = 2.6.x (system) | **rbenv not initialized!** See Pitfall 3 below | ✅ |
| Ruby ≠ 3.3.x | `rbenv local 3.3.6` | ✅ |
| Bundler missing | `gem install bundler` | ✅ |
| Jekyll missing | `bundle install` | ✅ |
| Port 4000 busy | `kill -9 $(lsof -ti:4000)` | ✅ |

**Token Cost Analysis**:
- ❌ **Without diagnostic**: 5 failed attempts × 1000 tokens = 5000 tokens wasted
- ✅ **With diagnostic**: 1 successful attempt × 200 tokens = 200 tokens
- **Net savings**: 4800 tokens (96% reduction)

**Rule**: If 2+ diagnostics show issues, STOP and fix environment before trying server commands.

### 1. Make Changes

Edit the relevant files:
- **Content**: `_posts/YYYY-MM-DD-title.md`, `*.md` pages
- **Styles**: `_sass/economist-theme.scss`
- **Layouts**: `_layouts/*.html`
- **Config**: `_config.yml` (requires server restart if testing locally)

### 2. Test Locally (Optional - Only After Diagnostic Passes)

For CSS/layout work requiring rapid iteration:

```bash
cd /Users/ouray.viney/code/economist-blog-v5
bundle exec jekyll serve --config _config_dev.yml --livereload
```

**URL**: http://localhost:4000/

**Note**: Config changes require full server restart (Ctrl+C, then restart).

### 3. Commit Changes

```bash
git add <files>
git commit -m "description"
```

**Pre-commit hook automatically validates**:
- ✅ Jekyll build succeeds
- ✅ No broken internal links
- ✅ YAML front matter is valid
- ✅ Required fields present (title, date)
- ✅ Future date warnings

**If validation fails**: Fix the issue before committing. Never use `--no-verify`.

### 4. Push to GitHub

```bash
git push origin main
```

### 5. Monitor Deployment

- GitHub Actions builds with Jekyll 4.3.2 (~45 seconds)
- Deploys to GitHub Pages (~30 seconds)
- **Total**: 1-2 minutes
- **Monitor**: https://github.com/oviney/blog/actions

### 6. Verify Production

- Visit https://www.viney.ca/
- Check the specific page/post you modified
- Verify responsive design (mobile, tablet, desktop)
- Check browser console for errors

## Common Pitfalls

### Pitfall 1: Config Changes Don't Reload
**Problem**: Changed `_config.yml` but changes not visible with `jekyll serve`  
**Solution**: Stop server (Ctrl+C) and restart. Config changes require full restart.  
**Note**: CSS/content changes auto-reload, but config does not.

### Pitfall 2: Pre-commit Hook Fails on SSL Error
**Problem**: Remote theme fetching fails with SSL certificate error  
**Solution**: This is expected. The hook is smart enough to skip this error. If Jekyll build fails for other reasons, fix those.  
**Note**: GitHub Actions has no SSL issues—production builds always work.

### Pitfall 3: Forgot to Test Responsive Design
**Problem**: Looks good on desktop but broken on mobile  
**Solution**: Always test at multiple breakpoints (320px, 768px, 1024px, 1920px)  
**Tool**: Browser DevTools responsive mode

## Common Pitfalls

### Pitfall 1: Starting Server Without Diagnostic
**Problem**: Wasting tokens on 5+ failed server start attempts  
**Solution**: ALWAYS run environment diagnostic first (see Step 0)  
**Token Cost**: 4800 tokens wasted per incident  
**Root Cause**: Skipping environment validation

### Pitfall 2: Port 4000 Already in Use
**Problem**: `Address already in use - bind(2) for 127.0.0.1:4000`  
**Solution**: Kill existing process: `kill -9 $(lsof -ti:4000)`  
**Why**: Previous Jekyll process didn't terminate cleanly

### Pitfall 3: rbenv Not Initialized (Ruby shows 2.6.x system version)
**Problem**: Diagnostic shows `Ruby: ruby 2.6.10` (system Ruby instead of rbenv-managed version)  
**Root Cause**: rbenv is not initialized in your shell (missing from ~/.zshrc)  
**Solution**:
```bash
# 1. Add rbenv to ~/.zshrc (one-time setup)
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc

# 2. Reload shell config
source ~/.zshrc

# 3. Verify rbenv is working
rbenv versions  # Should show installed Ruby versions

# 4. Set local Ruby version for this project
cd /Users/ouray.viney/code/economist-blog-v5
rbenv local 3.3.6

# 5. Verify fix
ruby -v  # Should now show 3.3.6, not 2.6.10
```
**Check**: `ruby -v` should show `ruby 3.3.6` (not 2.6.10)  
**Token Cost**: This single pitfall caused the 5-iteration server start failure (5000 tokens wasted)

### Pitfall 4: Bypassing Pre-commit Hook
**Problem**: Used `git commit --no-verify` to skip failing checks  
**Solution**: NEVER bypass checks. Fix the underlying issue. Pre-commit hooks prevent broken deployments.

### Pitfall 5: Hardcoded Values in SCSS
**Problem**: Used magic numbers like `16px`, `#E3120B` directly in styles  
**Solution**: Use variables from `_sass/economist-theme.scss` (e.g., `$economist-red`, `$spacing-unit`)

## Code Snippets/Patterns

### Complete Environment Fix (From Diagnostic Failure)

**When diagnostic shows**: `Ruby: ruby 2.6.10` + `Bundler: ❌ NOT INSTALLED`

```bash
# Step 1: Initialize rbenv in zsh (one-time setup)
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# Step 2: Verify rbenv is working
rbenv versions
# Should show: * 3.3.6 (set by /Users/ouray.viney/code/economist-blog-v5/.ruby-version)

# Step 3: Set local Ruby version
cd /Users/ouray.viney/code/economist-blog-v5
rbenv local 3.3.6

# Step 4: Verify Ruby version switched
ruby -v
# Should show: ruby 3.3.6 (not 2.6.10)

# Step 5: Install bundler
gem install bundler

# Step 6: Install Jekyll and dependencies
bundle install

# Step 7: Re-run diagnostic to confirm all green
echo "Ruby: $(ruby -v)"
echo "Bundler: $(bundle -v)"
echo "Jekyll: $(bundle exec jekyll -v)"
# All should now show proper versions

# Step 8: NOW start server (will succeed on first try)
bundle exec jekyll serve --config _config_dev.yml --livereload
```

**Token Savings**: This workflow replaces 5+ failed iterations (5000 tokens) with 1 successful setup (500 tokens)

### Starting Local Server

```bash
cd /Users/ouray.viney/code/economist-blog-v5
bundle exec jekyll serve --config _config_dev.yml --livereload
```

**When to use**: CSS/layout work requiring rapid iteration  
**Notes**: Config changes require restart; content/CSS auto-reloads

### Committing Changes

```bash
git add <files>
git commit -m "feat: add new blog post about X"
# Pre-commit hook runs automatically
git push origin main
```

**When to use**: Every code change  
**Notes**: Use conventional commit format (feat, fix, docs, style, refactor, test, chore)

### Emergency Bypass (Use Sparingly)

```bash
git commit --no-verify -m "Emergency fix"
```

**When to use**: ONLY in genuine emergencies (production down)  
**Notes**: Document why bypass was needed in commit message

### Manual Pre-commit Test

```bash
.git/hooks/pre-commit
```

**When to use**: Testing hook behavior without committing  
**Notes**: Useful for debugging hook issues

## Related Files

- [`docs/DEVELOPMENT_WORKFLOW.md`](../DEVELOPMENT_WORKFLOW.md) - Full workflow documentation
- [`docs/conventions/testing.md`](../conventions/testing.md) - Testing conventions
- [`.git/hooks/pre-commit`](../../.git/hooks/pre-commit) - Pre-commit validation script
- [`.github/workflows/jekyll.yml`](../../.github/workflows/jekyll.yml) - CI/CD pipeline
- [`_config_dev.yml`](../../_config_dev.yml) - Development config overrides

## Success Criteria

- [ ] Changes committed successfully (pre-commit hook passed)
- [ ] GitHub Actions build succeeded
- [ ] Changes visible on production (https://www.viney.ca/)
- [ ] No console errors in browser
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] No visual regressions on other pages

## Version History

- **1.0.0** (2026-01-05): Initial skill creation from DEVELOPMENT_WORKFLOW.md
