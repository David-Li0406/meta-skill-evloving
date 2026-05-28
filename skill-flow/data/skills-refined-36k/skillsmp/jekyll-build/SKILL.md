---
name: jekyll-build
description: Validate Jekyll build and preview campaign content changes locally
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do
- Run Jekyll build process to validate content and syntax
- Check front matter validity across all campaign files
- Preview site locally with livereload functionality
- Identify and report build errors or warnings
- Test navigation between related articles
- Validate image references and asset paths

## When to use me
Use this when:
- Adding new content to ensure Jekyll compatibility
- Modifying front matter to validate YAML syntax
- Testing major content updates before publication
- Debugging site build issues
- Preparing content for GitHub Pages deployment

## Usage Examples

### Build Validation
```
/skill({ name: "jekyll-build" })
Operation: Validate build
Target: All campaign content
Options: Full syntax check, front matter validation
```

### Preview with Live Reload
```
/skill({ name: "jekyll-build" })
Operation: Development server
Target: Current working directory
Options: Live reload enabled, port 4000
```

### Build Error Diagnosis
```
/skill({ name: "jekyll-build" })
Operation: Debug build
Target: Specific files showing errors
Options: Verbose output, error tracking
```

## Build Operations

### Full Build Validation
1. Execute `bundle exec jekyll build` with error capture
2. Parse build output for warnings and errors
3. Identify problematic files with specific line numbers
4. Check front matter YAML syntax across all `.md` files
5. Validate image references and asset accessibility

### Development Server
1. Launch `bundle exec jekyll serve --livereload`
2. Monitor build process for real-time errors
3. Test navigation between articles while server runs
4. Validate relative URLs resolve correctly
5. Check site functionality across different browsers

### Content Analysis
1. Scan all collection files for front matter completeness
2. Verify required fields exist per content type
3. Check image references match existing files
4. Validate internal link syntax and paths
5. Test site structure and navigation menus

## Validation Checks

### Front Matter Analysis
- Required fields present per content type
- YAML syntax validation and proper indentation
- Layout field correctly set to "page"
- Date formats and special field validation
- Publication status field presence (or absence for published)

### Content Structure
- Headings follow proper hierarchy (H1 from title, H2 for sections)
- Internal links use `relative_url` filter correctly
- Image paths reference existing files in `assets/`
- List formatting follows campaign conventions
- Character token images properly sized and formatted

### Site Architecture
- Collection configuration in `_config.yml` works correctly
- Permalinks generate proper URLs
- Navigation menus update with new content
- Search functionality works with new articles
- Responsive design displays content correctly

## Error Detection

### Common Jekyll Issues
- YAML front matter syntax errors
- Missing required fields
- Invalid permalink patterns
- Broken liquid template syntax
- Missing layout files

### Content-Specific Problems
- Character name mismatches between files
- Broken cross-references and internal links
- Missing image files or incorrect paths
- Invalid URL generation for special characters
- Collection sorting and grouping issues

## Reports Generated

### Build Report
- Successful build status
- List of files with errors or warnings
- Specific error messages and line numbers
- Recommendations for common issues
- Summary of content statistics

### Preview Status
- Development server availability
- Livereload functionality status
- URL for local preview
- Performance metrics and load times
- Browser compatibility notes

### Content Health Check
- Front matter completeness score
- Internal link validation results
- Image reference verification status
- Collection organization summary
- Recommendations for improvements

Ask clarifying questions about:
- Which specific files or content types to focus validation
- Whether to automatically fix common formatting issues
- Preferred development server configuration
- How to handle missing dependencies or build errors
- Whether to generate preview links for testing