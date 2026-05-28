# Pandoc Troubleshooting Guide

Common errors and solutions for Pandoc document conversion.

## YAML Frontmatter Errors

### Error: YAML syntax error

**Problem:** Invalid YAML in frontmatter
```
Error: YAML syntax error: mapping values are not allowed here
```

**Common Causes:**
1. **Tabs instead of spaces**
   ```yaml
   # ❌ Wrong (contains tabs)
   title:→"My Paper"

   # ✅ Correct (spaces only)
   title: "My Paper"
   ```

2. **Missing quotes around special characters**
   ```yaml
   # ❌ Wrong
   title: Paper: A Study

   # ✅ Correct
   title: "Paper: A Study"
   ```

3. **Incorrect indentation**
   ```yaml
   # ❌ Wrong
   author:
   - "Name"  # Should be indented

   # ✅ Correct
   author:
     - "Name"
   ```

**Fix:** Use validation to find exact error
```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
```

### Error: YAML not properly closed

**Problem:** Missing second `---` marker
```
Error: YAML frontmatter not properly closed (missing second '---')
```

**Fix:**
```yaml
---
title: "Paper"
author: "Name"
---     # Must have this!

# Content starts here
```

## Bibliography Errors

### Error: Bibliography file not found

**Problem:** `.bib` file doesn't exist or wrong path
```
Error: Bibliography file not found: references.bib
```

**Solutions:**

1. **Create bibliography file:**
   ```bash
   PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
   cp "$PLUGIN_DIR/skills/pandoc/assets/templates/references.bib" references.bib
   ```

2. **Fix path in frontmatter:**
   ```yaml
   # ❌ Wrong (absolute path from another location)
   bibliography: /old/location/refs.bib

   # ✅ Correct (relative path)
   bibliography: references.bib
   bibliography: ./refs/references.bib
   ```

3. **Check file actually exists:**
   ```bash
   ls -la references.bib
   ```

### Error: CSL file not found

**Problem:** Citation style file missing
```
Error: CSL file not found: harvard.csl
```

**Solutions:**

1. **Download CSL file:**
   ```bash
   # Harvard style
   curl -o harvard.csl https://raw.githubusercontent.com/citation-style-language/styles/master/harvard-cite-them-right.csl

   # APA style
   curl -o apa.csl https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl

   # IEEE style
   curl -o ieee.csl https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
   ```

2. **Browse all styles:**
   https://github.com/citation-style-language/styles

3. **Remove CSL if using default:**
   ```yaml
   bibliography: references.bib
   # csl: harvard.csl  # Comment out to use default
   ```

### Error: BibTeX parse error

**Problem:** Invalid BibTeX syntax in `.bib` file

**Common Issues:**

1. **Missing commas:**
   ```bibtex
   # ❌ Wrong
   @article{key,
     author = "Name"
     title = "Title"    # Missing comma after author
   }

   # ✅ Correct
   @article{key,
     author = "Name",   # Comma added
     title = "Title"
   }
   ```

2. **Unclosed braces:**
   ```bibtex
   # ❌ Wrong
   @article{key,
     title = {Unclosed brace
   }

   # ✅ Correct
   @article{key,
     title = {Closed brace}
   }
   ```

3. **Invalid characters in cite key:**
   ```bibtex
   # ❌ Wrong
   @article{smith&jones2024,

   # ✅ Correct
   @article{smith-jones-2024,
   ```

## PDF Generation Errors

### Error: ! LaTeX Error: File not found

**Problem:** Missing LaTeX packages

**Solution:**
```bash
# Fedora/RHEL
sudo dnf install texlive-scheme-medium

# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# macOS
brew install --cask mactex
```

### Error: Unicode characters not supported

**Problem:** Using pdflatex with Unicode
```
! Package inputenc Error: Unicode character ... not set up for use with LaTeX
```

**Solution:** Use XeLaTeX instead
```bash
pandoc document.md -o document.pdf --pdf-engine=xelatex
```

Or update frontmatter:
```yaml
# Add to defaults file
pdf-engine: xelatex
```

### Error: Missing fonts

**Problem:** Custom font not found
```
! Font ... not found
```

**Solutions:**

1. **Use standard fonts:**
   ```yaml
   # Remove custom fonts
   # mainfont: "Custom Font"
   ```

2. **Install font:**
   ```bash
   # Copy font to system
   sudo cp font.ttf /usr/share/fonts/
   sudo fc-cache -f -v
   ```

3. **Use XeLaTeX with system fonts:**
   ```yaml
   mainfont: "Times New Roman"  # Must use XeLaTeX
   ```

### Error: ! Package geometry Error

**Problem:** Invalid geometry specification
```
! Package geometry Error: ... is too large
```

**Fix:**
```yaml
# ❌ Wrong
geometry: margin=5in  # Too large for paper

# ✅ Correct
geometry: margin=1in
geometry: "left=1.5in, right=1in, top=1in, bottom=1in"
```

## Image Errors

### Error: Image file not found

**Problem:** Image path incorrect or file missing

**Solutions:**

1. **Use relative paths:**
   ```markdown
   # ❌ Wrong (absolute path from different location)
   ![](/ old/path/image.png)

   # ✅ Correct
   ![](images/figure1.png)
   ![](./assets/diagram.png)
   ```

2. **Check file exists:**
   ```bash
   ls -la images/figure1.png
   ```

3. **Create images directory:**
   ```bash
   mkdir -p images
   # Copy images there
   ```

### Error: Image format not supported

**Problem:** LaTeX can't handle certain formats

**Supported formats:**
- PDF: PNG, JPEG, PDF
- HTML: PNG, JPEG, GIF, SVG

**Solution:** Convert image format
```bash
# Convert SVG to PNG (for PDF output)
convert diagram.svg diagram.png

# Or use ImageMagick
magick convert image.tiff image.png
```

## Conversion Errors

### Error: Pandoc not found

**Problem:** Pandoc not installed or not in PATH
```
Error: pandoc: command not found
```

**Solution:**
```bash
# Fedora/RHEL
sudo dnf install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc

# Verify installation
pandoc --version
```

### Error: Python not found (validation)

**Problem:** Python3 not available
```
Error: python3: command not found
```

**Solution:**
```bash
# Most Linux distributions have Python3
# But if not:
sudo dnf install python3

# Or use python instead of python3
python --version  # Check if Python 3.x
```

### Error: YAML module not found

**Problem:** PyYAML not installed (for validation)
```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:**
```bash
pip3 install pyyaml

# Or system package
sudo dnf install python3-pyyaml
```

## Output Errors

### Error: Permission denied writing output

**Problem:** Can't write to output location
```
Error: output.pdf: Permission denied
```

**Solutions:**

1. **Check write permissions:**
   ```bash
   ls -la output.pdf  # Check if file locked
   ```

2. **Use different location:**
   ```bash
   pandoc doc.md -o ~/Documents/output.pdf
   ```

3. **Close file in other program:**
   - Close PDF viewer
   - Close Word
   - Close text editor

### Error: Disk full

**Problem:** No space for output file

**Check:**
```bash
df -h .  # Check disk space
```

**Solution:**
- Free up disk space
- Use different output location

## Performance Issues

### Slow Conversion

**Causes:**
1. Large document
2. Many images
3. Complex LaTeX
4. Slow PDF engine

**Solutions:**

1. **Use faster engine:**
   ```bash
   # pdflatex is fastest
   pandoc doc.md -o doc.pdf --pdf-engine=pdflatex
   ```

2. **Optimize images:**
   ```bash
   # Compress images before embedding
   convert large.png -resize 50% smaller.png
   ```

3. **Split large documents:**
   ```bash
   # Convert chapters separately
   pandoc chapter1.md -o chapter1.pdf
   pandoc chapter2.md -o chapter2.pdf
   ```

## Citation Issues

### Citations not appearing

**Checklist:**
1. ✅ Bibliography file exists
2. ✅ CSL file exists (or using default)
3. ✅ Using `--citeproc` flag
4. ✅ Citation keys match bibliography

**Validate:**
```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
```

**Check citation syntax:**
```markdown
# ✅ Correct
[@smith2024]
@jones2023 found that...

# ❌ Wrong
[smith2024]     # Missing @
```

### Wrong citation style

**Problem:** Citations not in expected format

**Solution:** Use correct CSL file
```yaml
csl: harvard.csl  # Harvard
csl: apa.csl      # APA
csl: ieee.csl     # IEEE
```

**Download styles:**
```bash
curl -o style.csl https://raw.githubusercontent.com/citation-style-language/styles/master/[style-name].csl
```

## Debug Workflow

### Step-by-Step Debugging

1. **Validate first:**
   ```bash
   PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
   python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
   ```

2. **Check Pandoc version:**
   ```bash
   pandoc --version
   # Ensure version 2.0+
   ```

3. **Test minimal conversion:**
   ```bash
   # Create minimal test
   echo "# Test" > test.md
   pandoc test.md -o test.pdf
   ```

4. **Add options incrementally:**
   ```bash
   # Start simple
   pandoc doc.md -o doc.pdf

   # Add engine
   pandoc doc.md -o doc.pdf --pdf-engine=pdflatex

   # Add citations
   pandoc doc.md -o doc.pdf --pdf-engine=pdflatex --citeproc
   ```

5. **Check LaTeX intermediate:**
   ```bash
   # Generate .tex file to see LaTeX
   pandoc doc.md -o doc.tex
   cat doc.tex  # Inspect for errors
   ```

## Get Help

### Pandoc Documentation
- Manual: https://pandoc.org/MANUAL.html
- FAQ: https://pandoc.org/faqs.html
- Demos: https://pandoc.org/demos.html

### Community Resources
- Pandoc Discussions: https://github.com/jgm/pandoc/discussions
- Stack Overflow: [pandoc] tag
- LaTeX Stack Exchange: https://tex.stackexchange.com/

### Validation Tool
```bash
PLUGIN_DIR="~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc"
python3 "$PLUGIN_DIR/skills/pandoc/scripts/validate.py" document.md
```

This tool catches most common errors before conversion.
