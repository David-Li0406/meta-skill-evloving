---
name: latex-posters
description: Create professional research posters in LaTeX using beamerposter, tikzposter, or baposter. Support for conference presentations, academic posters, and scientific communication. Includes layout design, color schemes, multi-column formats, figure integration, and poster-specific best practices for visual communication.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# LaTeX Research Posters

## Overview

Research posters are a critical medium for scientific communication at conferences, symposia, and academic events. This skill provides comprehensive guidance for creating professional, visually appealing research posters using LaTeX packages. Generate publication-quality posters with proper layout, typography, color schemes, and visual hierarchy.

## When to Use This Skill

This skill should be used when:
- Creating research posters for conferences, symposia, or poster sessions
- Designing academic posters for university events or thesis defenses
- Preparing visual summaries of research for public engagement
- Converting scientific papers into poster format
- Creating template posters for research groups or departments
- Designing posters that comply with specific conference size requirements (A0, A1, 36×48", etc.)
- Building posters with complex multi-column layouts
- Integrating figures, tables, equations, and citations in poster format

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every research poster MUST include at least 2-3 AI-generated figures using the scientific-schematics skill.**

This is not optional. Posters are primarily visual media - text-heavy posters fail to communicate effectively. Before finalizing any poster:
1. Generate at minimum TWO schematics or diagrams
2. Target 3-4 figures for comprehensive posters (methodology flowchart, key results visualization, conceptual framework)
3. Figures should occupy 40-50% of poster area

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the schematic

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add schematics:**
- Research methodology flowcharts for poster content
- Conceptual framework diagrams
- Experimental design visualizations
- Data analysis pipeline diagrams
- System architecture diagrams
- Biological pathway illustrations
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Core Capabilities

### 1. LaTeX Poster Packages

Support for three major LaTeX poster packages, each with distinct advantages. For detailed comparison and package-specific guidance, refer to `references/latex_poster_packages.md`.

**beamerposter**:
- Extension of the Beamer presentation class
- Familiar syntax for Beamer users
- Excellent theme support and customization
- Best for: Traditional academic posters, institutional branding

**tikzposter**:
- Modern, flexible design with TikZ integration
- Built-in color themes and layout templates
- Extensive customization through TikZ commands
- Best for: Colorful, modern designs, custom graphics

**baposter**:
- Box-based layout system
- Automatic spacing and positioning
- Professional-looking default styles
- Best for: Multi-column layouts, consistent spacing

### 2. Poster Layout and Structure

Create effective poster layouts following visual communication principles. For comprehensive layout guidance, refer to `references/poster_layout_design.md`.

**Common Poster Sections**:
- **Header/Title**: Title, authors, affiliations, logos
- **Introduction/Background**: Research context and motivation
- **Methods/Approach**: Methodology and experimental design
- **Results**: Key findings with figures and data visualizations
- **Conclusions**: Main takeaways and implications
- **References**: Key citations (typically abbreviated)
- **Acknowledgments**: Funding, collaborators, institutions

**Layout Strategies**:
- **Column-based layouts**: 2-column, 3-column, or 4-column grids
- **Block-based layouts**: Flexible arrangement of content blocks
- **Z-pattern flow**: Guide readers through content logically
- **Visual hierarchy**: Use size, color, and spacing to emphasize key points

### 3. Design Principles for Research Posters

Apply evidence-based design principles for maximum impact. For detailed design guidance, refer to `references/poster_design_principles.md`.

**Typography**:
- Title: 72-120pt for visibility from distance
- Section headers: 48-72pt
- Body text: 24-36pt minimum for readability from 4-6 feet
- Use sans-serif fonts (Arial, Helvetica, Calibri) for clarity
- Limit to 2-3 font families maximum

**Color and Contrast**:
- Use high-contrast color schemes for readability
- Institutional color palettes for branding
- Color-blind friendly palettes (avoid red-green combinations)
- White space is active space—don't overcrowd

**Visual Elements**:
- High-resolution figures (300 DPI minimum for print)
- Large, clear labels on all figures
- Consistent figure styling throughout
- Strategic use of icons and graphics
- Balance text with visual content (40-50% visual recommended)

**Content Guidelines**:
- **Less is more**: 300-800 words total recommended
- Bullet points over paragraphs for scannability
- Clear, concise messaging
- Self-explanatory figures with minimal text explanation
- QR codes for supplementary materials or online resources

### 4. Standard Poster Sizes

Support for international and conference-specific poster dimensions:

**International Standards**:
- A0 (841 × 1189 mm / 33.1 × 46.8 inches) - Most common European standard
- A1 (594 × 841 mm / 23.4 × 33.1 inches) - Smaller format
- A2 (420 × 594 mm / 16.5 × 23.4 inches) - Compact posters

**North American Standards**:
- 36 × 48 inches (914 × 1219 mm) - Common US conference size
- 42 × 56 inches (1067 × 1422 mm) - Large format
- 48 × 72 inches (1219 × 1829 mm) - Extra large

**Orientation**:
- Portrait (vertical) - Most common, traditional
- Landscape (horizontal) - Better for wide content, timelines

### 5. Package-Specific Templates

Provide ready-to-use templates for each major package. Templates available in `assets/` directory.

**beamerposter Templates**:
- `beamerposter_classic.tex` - Traditional academic style
- `beamerposter_modern.tex` - Clean, minimal design
- `beamerposter_colorful.tex` - Vibrant theme with blocks

**tikzposter Templates**:
- `tikzposter_default.tex` - Standard tikzposter layout
- `tikzposter_rays.tex` - Modern design with ray theme
- `tikzposter_wave.tex` - Professional wave-style theme

**baposter Templates**:
- `baposter_portrait.tex` - Classic portrait layout
- `baposter_landscape.tex` - Landscape multi-column
- `baposter_minimal.tex` - Minimalist design

### 6. Figure and Image Integration

Optimize visual content for poster presentations:

**Best Practices**:
- Use vector graphics (PDF, SVG) when possible for scalability
- Raster images: minimum 300 DPI at final print size
- Consistent image styling (borders, captions, sizes)
- Group related figures together
- Use subfigures for comparisons

**LaTeX Figure Commands**:
```latex
% Include graphics package
\usepackage{graphicx}

% Simple figure
\includegraphics[width=0.8\linewidth]{figure.pdf}

% Figure with caption in tikzposter
\block{Results}{
  \begin{tikzfigure}
    \includegraphics[width=0.9\linewidth]{results.png}
  \end{tikzfigure}
}

% Multiple subfigures
\usepackage{subcaption}
\begin{figure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig1.pdf}
    \caption{Condition A}
  \end{subfigure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig2.pdf}
    \caption{Condition B}
  \end{subfigure}
\end{figure}
```

### 7. Color Schemes and Themes

Provide professional color palettes for various contexts:

**Academic Institution Colors**:
- Match university or department branding
- Use official color codes (RGB, CMYK, or LaTeX color definitions)

**Scientific Color Palettes** (color-blind friendly):
- Viridis: Professional gradient from purple to yellow
- ColorBrewer: Research-tested palettes for data visualization
- IBM Color Blind Safe: Accessible corporate palette

**Package-Specific Theme Selection**:

**beamerposter**:
```latex
\usetheme{Berlin}
\usecolortheme{beaver}
```

**tikzposter**:
```latex
\usetheme{Rays}
\usecolorstyle{Denmark}
```

**baposter**:
```latex
\begin{poster}{
  background=plain,
  bgColorOne=white,
  headerColorOne=blue!70,
  textborder=rounded
}
```

### 8. Typography and Text Formatting

Ensure readability and visual appeal:

**Font Selection**:
```latex
% Sans-serif fonts recommended for posters
\usepackage{helvet}      % Helvetica
\usepackage{avant}       % Avant Garde
\usepackage{sfmath}      % Sans-serif math fonts

% Set default to sans-serif
\renewcommand{\familydefault}{\sfdefault}
```

**Text Sizing**:
```latex
% Adjust text sizes for visibility
\setbeamerfont{title}{size=\VeryHuge}
\setbeamerfont{author}{size=\Large}
\setbeamerfont{institute}{size=\normalsize}
```

**Emphasis and Highlighting**:
- Use bold for key terms: `\textbf{important}`
- Color highlights sparingly: `\textcolor{blue}{highlight}`
- Boxes for critical information
- Avoid italics (harder to read from distance)

### 9. QR Codes and Interactive Elements

Enhance poster interactivity for modern conferences:

**QR Code Integration**:
```latex
\usepackage{qrcode}

% Link to paper, code repository, or supplementary materials
\qrcode[height=2cm]{https://github.com/username/project}

% QR code with caption
\begin{center}
  \qrcode[height=3cm]{https://doi.org/10.1234/paper}\\
  \small Scan for full paper
\end{center}
```

**Digital Enhancements**:
- Link to GitHub repositories for code
- Link to video presentations or demos
- Link to interactive web visualizations
- Link to supplementary data or appendices

### 10. Compilation and Output

Generate high-quality PDF output for printing or digital display:

**Compilation Commands**:
```bash
# Basic compilation
pdflatex poster.tex

# With bibliography
pdflatex poster.tex
bibtex poster
pdflatex poster.tex
pdflatex poster.tex

# For beamer-based posters
lualatex poster.tex  # Better font support
xelatex poster.tex   # Unicode and modern fonts
```

**Ensuring Full Page Coverage**:

Posters should use the entire page without excessive margins. Configure packages correctly:

**beamerposter - Full Page Setup**:
```latex
\documentclass[final,t]{beamer}
\usepackage[size=a0,scale=1.4,orientation=portrait]{beamerposter}

% Remove default beamer margins
\setbeamersize{text margin left=0mm, text margin right=0mm}

% Use geometry for precise control
\usepackage[margin=10mm]{geometry}  % 10mm margins all around

% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}

% Remove footline and headline if not needed
\setbeamertemplate{footline}{}
\setbeamertemplate{headline}{}
```

**tikzposter - Full Page Setup**:
```latex
\documentclass[
  25pt,                      % Font scaling
  a0paper,                   % Paper size
  portrait,                  % Orientation
  margin=10mm,               % Outer margins (minimal)
  innermargin=15mm,          % Space inside blocks
  blockverticalspace=15mm,   % Space between blocks
  colspace=15mm,             % Space between columns
  subcolspace=8mm            % Space between subcolumns
]{tikzposter}

% This ensures content fills the page
```

**baposter - Full Page Setup**:
```latex
\documentclass[a0paper,portrait,fontscale=0.285]{baposter}

\begin{poster}{
  grid=false,
  columns=3,
  colspacing=1.5em,          % Space between columns
  eyecatcher=true,
  background=plain,
  bgColorOne=white,
  borderColor=blue!50,
  headerheight=0.12\textheight,  % 12% for header
  textborder=roundedleft,
  headerborder=closed,
  boxheaderheight=2em        % Consistent box header heights
}
% Content here
\end{poster}
```

**Common Issues and Fixes**:

**Problem**: Large white margins around poster
```latex
% Fix for beamerposter
\setbeamersize{text margin left=5mm, text margin right=5mm}

% Fix for tikzposter
\documentclass[..., margin=5mm, innermargin=10mm]{tikzposter}

% Fix for baposter - adjust in document class
\documentclass[a0paper, margin=5mm]{baposter}
```

**Problem**: Content doesn't fill vertical space
```latex
% Use \vfill between sections to distribute space
\block{Introduction}{...}
\vfill
\block{Methods}{...}
\vfill
\block{Results}{...}

% Or manually adjust block spacing
\vspace{1cm}  % Add space between specific blocks
```

**Problem**: Poster extends beyond page boundaries
```latex
% Check total width calculation
% For 3 columns with spacing:
% Total = 3×columnwidth + 2×colspace + 2×margins
% Ensure this equals \paperwidth

% Debug by adding visible page boundary
\usepackage{eso-pic}
\AddToShipoutPictureBG{
  \AtPageLowerLeft{
    \put(0,0){\framebox(\LenToUnit{\paperwidth},\LenToUnit{\paperheight}){}}
  }
}
```

**Print Preparation**:
- Generate PDF/X-1a for professional printing
- Embed all fonts
- Convert colors to CMYK if required
- Check resolution of all images (minimum 300 DPI)
- Add bleed area if required by printer (usually 3-5mm)
- Verify page size matches requirements exactly

**Digital Display**:
- RGB color space for screen display
- Optimize file size for email/web
- Test readability on different screens

### 11. PDF Review and Quality Control

**CRITICAL**: Always review the generated PDF before printing or presenting. Use this systematic checklist:

**Step 1: Page Size Verification**
```bash
# Check PDF dimensions (should match poster size exactly)
pdfinfo poster.pdf | grep "Page size"

# Expected outputs:
# A0: 2384 x 3370 points (841 x 1189 mm)
# 36x48": 2592 x 3456 points
# A1: 1684 x 2384 points (594 x 841 mm)
```

**Step 2: Visual Inspection Checklist**

Open PDF at 100% zoom and check:

**Layout and Spacing**:
- [ ] Content fills entire page