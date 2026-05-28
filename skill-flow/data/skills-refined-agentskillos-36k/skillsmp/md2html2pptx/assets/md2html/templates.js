/**
 * HTML Templates for md2html
 * Generates html2pptx-compatible HTML slides
 */

const fs = require('fs');
const path = require('path');

let hljs;
try {
  hljs = require('highlight.js');
} catch {
  try {
    hljs = require(path.join(process.cwd(), 'node_modules', 'highlight.js'));
  } catch {
    hljs = null;
  }
}

/**
 * Load mermaid browser bundle from node_modules at build time
 * The content is inlined into HTML for browser-side rendering
 */
let mermaidBundleContent = null;
try {
  const mermaidPath = require.resolve('mermaid/dist/mermaid.min.js');
  mermaidBundleContent = fs.readFileSync(mermaidPath, 'utf-8');
} catch {
  try {
    const mermaidPath = path.join(process.cwd(), 'node_modules', 'mermaid', 'dist', 'mermaid.min.js');
    mermaidBundleContent = fs.readFileSync(mermaidPath, 'utf-8');
  } catch {
    mermaidBundleContent = null;
  }
}

/**
 * Highlight code at build time using highlight.js
 * Returns HTML with <span class="hljs-*"> wrappers (already escaped)
 * Falls back to escapeHtml if highlight.js is not available
 * @param {string} code - Raw code string
 * @param {string} language - Language identifier
 * @returns {string} - Highlighted HTML
 */
function highlightCode(code, language) {
  if (!hljs) return escapeHtml(code);
  try {
    if (language && hljs.getLanguage(language)) {
      return hljs.highlight(code, { language }).value;
    }
    return hljs.highlightAuto(code).value;
  } catch (e) {
    return escapeHtml(code);
  }
}

// Default theme configuration (new unified structure)
const DEFAULT_THEME = {
  fonts: {
    body: "'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif",
    code: "'Consolas', 'Monaco', 'Courier New', monospace"
  },
  primary: '#0891B2',
  titleSlide: {
    background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
    titleColor: '#F8FAFC',
    titleSize: 42,
    subtitleColor: '#94A3B8',
    subtitleSize: 18,
    accentColor: '#22D3EE'
  },
  contentSlide: {
    background: '#F8FAFC',
    titleColor: '#0F172A',
    titleSize: 28,
    textColor: '#0F172A',
    mutedColor: '#64748B',
    listSize: 20,
    subListSize: 18,
    subSubListSize: 16
  },
  codeSlide: {
    titleSize: 28,
    codeSize: 14
  },
  card: {
    background: '#FFFFFF',
    shadow: '0 2px 8px rgba(0,0,0,0.08)',
    border: '#E2E8F0',
    headerBg: '#F1F5F9'
  },
  good: {
    background: '#d4edda',
    foreground: '#155724',
    border: '#28a745'
  },
  bad: {
    background: '#f8d7da',
    foreground: '#721c24',
    border: '#dc3545'
  }
};

// Active theme configuration (mutable)
let THEME = JSON.parse(JSON.stringify(DEFAULT_THEME));

// Syntax highlighting CSS (VS Code Dark+ theme colors)
const SYNTAX_HIGHLIGHT_CSS = `
    .hljs-keyword { color: #569cd6; }
    .hljs-built_in { color: #4ec9b0; }
    .hljs-type { color: #4ec9b0; }
    .hljs-literal { color: #569cd6; }
    .hljs-number { color: #b5cea8; }
    .hljs-string { color: #ce9178; }
    .hljs-comment { color: #6a9955; }
    .hljs-function { color: #dcdcaa; }
    .hljs-class { color: #4ec9b0; }
    .hljs-variable { color: #9cdcfe; }
    .hljs-attr { color: #9cdcfe; }
    .hljs-property { color: #9cdcfe; }
    .hljs-punctuation { color: #d4d4d4; }
    .hljs-operator { color: #d4d4d4; }
    .hljs-tag { color: #569cd6; }
    .hljs-name { color: #569cd6; }
    .hljs-attribute { color: #9cdcfe; }
    .hljs-title { color: #dcdcaa; }
    .hljs-params { color: #9cdcfe; }
    .hljs-meta { color: #569cd6; }
    .hljs-selector-tag { color: #d7ba7d; }
    .hljs-selector-class { color: #d7ba7d; }
    .hljs-selector-id { color: #d7ba7d; }
    .hljs-section { color: #569cd6; font-weight: bold; }
    .hljs-bullet { color: #6796e6; }
    .hljs-emphasis { color: #d4d4d4; font-style: italic; }
    .hljs-strong { color: #d4d4d4; font-weight: bold; }
    .hljs-quote { color: #6a9955; }
    .hljs-code { color: #ce9178; }`;

/**
 * Mermaid initialization code (runs in browser after mermaid bundle loads)
 */
const MERMAID_INIT = `
      mermaid.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        flowchart: { curve: 'basis' },
        sequence: {
          useMaxWidth: true,
          diagramMarginX: 20,
          diagramMarginY: 20,
          actorMargin: 60,
          boxMargin: 10,
          boxTextMargin: 5,
          noteMargin: 10,
          messageMargin: 35
        },
        themeVariables: {
          fontSize: '14px'
        }
      });
      // Run mermaid and mark SVGs for rasterization
      mermaid.run().then(() => {
        document.querySelectorAll('.mermaid svg').forEach((svg, i) => {
          svg.setAttribute('data-rasterize', 'mermaid-' + i);
        });
      });`;

/**
 * Generate mermaid script tags with inlined bundle from node_modules
 * Falls back to CDN if the local bundle is not available
 * @param {string} name - Script name (currently only 'mermaid' supported)
 * @returns {string} - HTML script tags or empty string if not found
 */
function generateCdnScript(name) {
  if (name !== 'mermaid') return '';
  if (mermaidBundleContent) {
    return `
    <script>${mermaidBundleContent}<\/script>
    <script>${MERMAID_INIT}<\/script>`;
  }
  // Fallback to CDN if local bundle not found
  return `
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"><\/script>
    <script>${MERMAID_INIT}<\/script>`;
}

// Legacy alias for backwards compatibility
const MERMAID_SCRIPT = generateCdnScript('mermaid');

/**
 * Check if a code block is Mermaid diagram
 * @param {Object} codeBlock - Code block with language and code
 * @returns {boolean}
 */
function isMermaidCode(codeBlock) {
  return codeBlock && codeBlock.language &&
         codeBlock.language.toLowerCase() === 'mermaid';
}

/**
 * Get the render type for a code block
 * @param {Object} codeBlock - Code block with language and code
 * @returns {'mermaid' | 'code' | null}
 */
function getCodeBlockRenderType(codeBlock) {
  if (!codeBlock) return null;
  if (isMermaidCode(codeBlock)) return 'mermaid';
  return 'code';
}

/**
 * Determine required CDN scripts for a list of items
 * @param {Array} items - Array of composite items
 * @returns {Set<string>} - Set of required script names ('mermaid')
 */
function getRequiredScripts(items) {
  const scripts = new Set();

  for (const item of items) {
    if (item.type === 'code' && item.codeBlock) {
      const renderType = getCodeBlockRenderType(item.codeBlock);
      if (renderType === 'mermaid') scripts.add('mermaid');
    }
  }

  return scripts;
}

// Legacy aliases for backwards compatibility (computed from THEME)
let COLORS = {};
let FONTS = {};
let TYPOGRAPHY = {};

// Update legacy aliases from THEME
function updateLegacyAliases() {
  FONTS = { ...THEME.fonts };
  COLORS = {
    // Title slide
    titleBackground: THEME.titleSlide.background,
    titleText: THEME.titleSlide.titleColor,
    subtitleText: THEME.titleSlide.subtitleColor,
    // Primary colors
    primary: THEME.primary,
    accent: THEME.titleSlide.accentColor,
    // Text colors
    text: THEME.contentSlide.textColor,
    muted: THEME.contentSlide.mutedColor,
    // Background colors
    surface: THEME.contentSlide.background,
    white: THEME.card.background,
    border: THEME.card.border,
    headerBg: THEME.card.headerBg,
    cardShadow: THEME.card.shadow,
    // Good/Bad colors
    good: THEME.good.background,
    goodBackground: THEME.good.background,
    goodForeground: THEME.good.foreground,
    goodBorder: THEME.good.border,
    bad: THEME.bad.background,
    badBackground: THEME.bad.background,
    badForeground: THEME.bad.foreground,
    badBorder: THEME.bad.border,
    // Legacy alias
    darkBg: THEME.titleSlide.background
  };
  TYPOGRAPHY = {
    titleSlide: {
      titleSize: THEME.titleSlide.titleSize,
      subtitleSize: THEME.titleSlide.subtitleSize
    },
    contentSlide: {
      titleSize: THEME.contentSlide.titleSize,
      listSize: THEME.contentSlide.listSize,
      subListSize: THEME.contentSlide.subListSize,
      subSubListSize: THEME.contentSlide.subSubListSize
    },
    codeSlide: {
      titleSize: THEME.codeSlide.titleSize,
      codeSize: THEME.codeSlide.codeSize
    }
  };
}

// Initialize legacy aliases
updateLegacyAliases();

/**
 * Set theme configuration from external JSON
 * Supports new unified structure (titleSlide, contentSlide, etc.)
 */
function setThemeConfig(config) {
  // Deep merge config into THEME
  THEME = JSON.parse(JSON.stringify(DEFAULT_THEME));

  // Handle new unified structure
  if (config.fonts) {
    THEME.fonts = { ...THEME.fonts, ...config.fonts };
  }
  if (config.primary) {
    THEME.primary = config.primary;
  }
  if (config.titleSlide) {
    THEME.titleSlide = { ...THEME.titleSlide, ...config.titleSlide };
  }
  if (config.contentSlide) {
    THEME.contentSlide = { ...THEME.contentSlide, ...config.contentSlide };
  }
  if (config.codeSlide) {
    THEME.codeSlide = { ...THEME.codeSlide, ...config.codeSlide };
  }
  if (config.card) {
    THEME.card = { ...THEME.card, ...config.card };
  }
  if (config.good) {
    THEME.good = { ...THEME.good, ...config.good };
  }
  if (config.bad) {
    THEME.bad = { ...THEME.bad, ...config.bad };
  }

  // Update legacy aliases for backwards compatibility
  updateLegacyAliases();
}

/**
 * Build CSS string from conditional style blocks
 * @param {Object.<string, boolean>} conditions - Style name to condition map
 * @param {Object.<string, string>} styleBlocks - Style name to CSS string map
 * @returns {string} - Combined CSS string
 */
const buildConditionalStyles = (conditions, styleBlocks) =>
  Object.entries(conditions)
    .filter(([_, shouldInclude]) => shouldInclude)
    .map(([key]) => styleBlocks[key] || '')
    .join('');

/**
 * Card slide style blocks for conditional inclusion
 */
const CARD_STYLE_BLOCKS = {
  codeBlock: `
    .card-code {
      background: #1e1e1e;
      border-radius: 8px;
      padding: 12px 16px;
      margin-top: 12px;
      overflow: hidden;
    }
    .card-code .lang-label {
      color: #858585;
      font-size: 10px;
      margin: 0 0 8px 0;
      font-family: var(--font-code);
    }
    .card-code pre {
      margin: 0;
      padding: 0;
      background: transparent;
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    .card-code code {
      font-family: var(--font-code);
      font-size: 11px;
      line-height: 1.4;
      color: #d4d4d4;
    }${SYNTAX_HIGHLIGHT_CSS}`,

  variants: `
    .card-good {
      background: var(--color-good);
    }
    .card-bad {
      background: var(--color-bad);
    }
    .card-good h2, .card-good li {
      color: var(--color-good-fg);
    }
    .card-bad h2, .card-bad li {
      color: var(--color-bad-fg);
    }`,

  steps: `
    .card-step {
      display: flex;
      align-items: flex-start;
      gap: 16px;
    }
    .step-num {
      width: 32px;
      height: 32px;
      flex-shrink: 0;
      background: linear-gradient(135deg, var(--theme-primary) 0%, #0E7490 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .step-num p {
      color: white;
      font-size: 14px;
      font-weight: 700;
      margin: 0;
    }
    .step-content {
      flex: 1;
    }
    .card-step h2 {
      color: var(--theme-text);
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    .card-step ul {
      margin: 0;
      padding-left: 0;
      list-style: none;
    }
    .card-step li {
      color: var(--theme-muted);
      font-size: 13px;
    }`
};

/**
 * Mermaid diagram style blocks
 * Centralized CSS for Mermaid containers across different slide types
 */
const MERMAID_STYLES = {
  /**
   * Base Mermaid container styles (used in standalone Mermaid slides)
   */
  base: (cardShadow) => `
    .mermaid-container {
      background: white;
      border-radius: 12px;
      padding: 24px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: ${cardShadow};
      min-height: 300px;
    }
    .mermaid {
      margin: 0;
      font-family: inherit;
      width: 100%;
      height: 100%;
    }
    .mermaid svg {
      width: 100%;
      height: 100%;
      max-width: 100%;
      max-height: 100%;
    }`,

  /**
   * Grid cell Mermaid styles (used in composite grid layouts)
   * @param {Object} s - Style values from calculateGridStyles
   */
  grid: (s) => `
    .grid-cell-mermaid {
      background: white;
      border-radius: ${s.borderRadius}px;
      box-shadow: var(--card-shadow);
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .grid-cell-mermaid .mermaid-container {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: ${Math.max(8, s.padding)}px;
    }
    .grid-cell-mermaid .mermaid {
      margin: 0;
      font-family: inherit;
      width: 100%;
      height: 100%;
    }
    .grid-cell-mermaid .mermaid svg {
      width: 100%;
      height: 100%;
      max-width: 100%;
      max-height: 100%;
    }`
};

/**
 * Wrap HTML content with base template
 */
function wrapWithBase(styleContent, bodyContent, bodyBackground = null) {
  // Extract background from styleContent if not explicitly provided
  let bgStyle = '';
  let modifiedStyleContent = styleContent;

  if (bodyBackground) {
    bgStyle = bodyBackground;
  } else {
    // Look for .slide background in styleContent and move it to body
    const bgMatch = styleContent.match(/\.slide\s*\{[^}]*background:\s*([^;]+);/);
    if (bgMatch) {
      bgStyle = bgMatch[1].trim();
      // Remove background from .slide in styleContent
      modifiedStyleContent = styleContent.replace(/(\.slide\s*\{[^}]*)background:\s*[^;]+;/, '$1');
    }
  }

  const bodyStyle = bgStyle
    ? `body { margin: 0; width: 960px; height: 540px; background: ${bgStyle}; font-family: ${FONTS.body}; }`
    : `body { margin: 0; width: 960px; height: 540px; font-family: ${FONTS.body}; }`;

  // CSS custom properties for theme colors and fonts
  const cssVars = `:root {
      --theme-primary: ${COLORS.primary};
      --theme-accent: ${COLORS.accent};
      --theme-text: ${COLORS.text};
      --theme-muted: ${COLORS.muted};
      --font-body: ${FONTS.body};
      --font-code: ${FONTS.code};
    }`;

  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="theme.css">
  <style>
    ${cssVars}
    ${bodyStyle}
    .slide {
      width: 960px;
      height: 540px;
      padding: 0;
      box-sizing: border-box;
      overflow: hidden;
    }
    * {
      box-sizing: border-box;
    }
${modifiedStyleContent}
  </style>
</head>
<body>
  <div class="slide">
${bodyContent}
  </div>
</body>
</html>`;
}

/**
 * Generate Title Slide (Dark)
 */
function generateTitleSlide(slide) {
  const style = `    .slide {
      background: ${COLORS.titleBackground || COLORS.darkBg};
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px;
    }
    .part-label {
      color: ${COLORS.accent};
      font-size: 16px;
      font-weight: 600;
      letter-spacing: 2px;
      margin: 0 0 16px 0;
    }
    h1 {
      color: ${COLORS.titleText || COLORS.surface};
      font-size: 42px;
      font-weight: 700;
      text-align: center;
      margin: 0;
      line-height: 1.3;
    }
    .subtitle {
      color: ${COLORS.subtitleText};
      font-size: 20px;
      margin: 32px 0 0 0;
      text-align: center;
    }
    .accent { color: ${COLORS.accent}; }`;

  const partLabel = slide.partNumber ? `    <p class="part-label">PART ${slide.partNumber}</p>\n` : '';
  const mainTitle = slide.mainTitle || slide.name;
  const subtitle = slide.subtitle ? `    <p class="subtitle">${escapeHtml(slide.subtitle)}</p>\n` : '';

  const body = `${partLabel}    <h1>${escapeHtml(mainTitle)}</h1>
${subtitle}`;

  return wrapWithBase(style, body.trimEnd());
}

/**
 * Generate Content Slide with bullet list (supports nested items)
 */
function generateContentSlide(slide) {
  const items = slide.items || [];

  const style = `    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: 28px;
      margin: 0 0 24px 0;
    }
    .content {
      padding: 0;
    }
    .content-list {
      margin: 0;
      padding-left: 24px;
      list-style: none;
    }
    .content-list > li {
      color: ${COLORS.text};
      font-size: 24px;
      font-weight: 600;
      line-height: 1.5;
      margin-bottom: 16px;
    }
    .content-list > li:last-child {
      margin-bottom: 0;
    }
    .sub-list {
      margin: 4px 0 0 0;
      padding-left: 20px;
      list-style: none;
    }
    .sub-list > li {
      color: ${COLORS.muted};
      font-size: 16px;
      font-weight: 400;
      line-height: 1.6;
      margin-bottom: 2px;
    }
    .sub-list > li:last-child {
      margin-bottom: 0;
    }
    .sub-sub-list {
      margin: 2px 0 0 0;
      padding-left: 16px;
      list-style: none;
    }
    .sub-sub-list > li {
      color: #94A3B8;
      font-size: 16px;
      font-weight: 400;
      line-height: 1.6;
      margin-bottom: 2px;
    }
    /* Fallback for flat list */
    ul.flat-list {
      margin: 0;
      padding-left: 24px;
      list-style: none;
    }
    ul.flat-list li {
      color: #475569;
      font-size: 20px;
      line-height: 1.8;
      margin-bottom: 8px;
    }
    ul.flat-list li:last-child {
      margin-bottom: 0;
    }`;

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  // Generate nested list HTML
  const generateNestedList = (items, depth = 0) => {
    const listClass = depth === 0 ? 'content-list' : (depth === 1 ? 'sub-list' : 'sub-sub-list');
    const itemsHtml = items.map(item => {
      if (typeof item === 'object' && item.subItems && item.subItems.length > 0) {
        const subListHtml = generateNestedList(item.subItems, depth + 1);
        return `        <li>${escapeHtml(item.text)}\n${subListHtml}        </li>`;
      } else if (typeof item === 'object' && item.subSubItems && item.subSubItems.length > 0) {
        // Handle subSubItems (third level)
        const subSubListHtml = generateNestedList(item.subSubItems.map(text => ({ text })), depth + 1);
        return `        <li>${escapeHtml(item.text)}\n${subSubListHtml}        </li>`;
      } else {
        const text = typeof item === 'object' ? item.text : item;
        return `        <li>${escapeHtml(text)}</li>`;
      }
    }).join('\n');
    return `      <ul class="${listClass}">\n${itemsHtml}\n      </ul>\n`;
  };

  const listHtml = generateNestedList(items);

  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="content">
${listHtml}    </div>`;

  return wrapWithBase(style, body);
}

/**
 * Process inline code in text (e.g., `code`)
 */
function processInlineCode(text) {
  if (!text) return '';
  return escapeHtml(text).replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
}

/**
 * Generate Card Layout Slide (supports normal, good, bad, step variants)
 */
function generateCardsSlide(slide) {
  const cards = slide.cards || [];
  const cardCount = cards.length;
  const layout = slide.layout || 'horizontal';
  const isVertical = layout === 'vertical';
  const gap = isVertical ? 12 : 20;
  const totalGap = gap * (cardCount - 1);
  const availableWidth = 960 - 120; // 60px padding each side
  const cardWidth = isVertical ? availableWidth : Math.floor((availableWidth - totalGap) / cardCount) - 1;
  const hasCodeBlock = cards.some(c => c.codeBlock);
  const hasVariants = cards.some(c => c.variant === 'good' || c.variant === 'bad');
  const hasSteps = cards.some(c => c.variant === 'step');

  // Build conditional styles using the style builder
  const conditionalStyles = buildConditionalStyles(
    { codeBlock: hasCodeBlock, variants: hasVariants, steps: hasSteps },
    CARD_STYLE_BLOCKS
  );

  // CSS custom properties for card styles
  const cardCssVars = `
    --color-good: ${COLORS.good};
    --color-bad: ${COLORS.bad};
    --color-good-fg: ${COLORS.goodForeground};
    --color-bad-fg: ${COLORS.badForeground};
    --font-code: ${FONTS.code};`;

  const style = `    :root {${cardCssVars}
    }
    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: 28px;
      margin: 0 0 24px 0;
    }
    .cards {
      display: flex;
      ${isVertical ? 'flex-direction: column;' : ''}
      gap: ${gap}px;
    }
    .card {
      width: ${cardWidth}px;
      background: ${COLORS.white};
      border-radius: ${isVertical ? '10px' : '12px'};
      padding: ${isVertical ? '16px 20px' : '20px'};
      box-shadow: ${COLORS.cardShadow};
    }
    h2 {
      color: ${COLORS.primary};
      font-size: 18px;
      margin: 0 0 12px 0;
    }
    ul {
      margin: 0;
      padding-left: 20px;
    }
    li {
      color: ${COLORS.muted};
      font-size: 14px;
      line-height: 1.6;
      margin-bottom: 4px;
    }
    li:last-child {
      margin-bottom: 0;
    }
    .inline-code {
      background: ${COLORS.headerBg};
      color: ${COLORS.primary};
      padding: 2px 6px;
      border-radius: 4px;
      font-family: ${FONTS.code};
      font-size: 12px;
    }${conditionalStyles}`;

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  const cardsHtml = cards.map(card => {
    const items = card.items.map(item => `          <li>${processInlineCode(item)}</li>`).join('\n');
    const codeBlockHtml = card.codeBlock ? `
        <div class="card-code">
          <pre><code class="language-${escapeHtml(card.codeBlock.language)}">${highlightCode(card.codeBlock.code, card.codeBlock.language)}</code></pre>
        </div>` : '';

    // Handle step variant
    if (card.variant === 'step') {
      const stepNum = card.number !== undefined ? card.number : 0;
      return `      <div class="card card-step">
        <div class="step-num"><p>${stepNum}</p></div>
        <div class="step-content">
          <h2>${escapeHtml(card.name)}</h2>
          <ul>
${items}
          </ul>
        </div>
      </div>`;
    }

    const cardClass = card.variant === 'good' ? 'card card-good' : card.variant === 'bad' ? 'card card-bad' : 'card';
    return `      <div class="${cardClass}">
        <h2>${escapeHtml(card.name)}</h2>
        <ul>
${items}
        </ul>${codeBlockHtml}
      </div>`;
  }).join('\n');

  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="cards">
${cardsHtml}
    </div>`;

  return wrapWithBase(style, body);
}

/**
 * Generate Table Slide
 */
function generateTableSlide(slide) {
  const table = slide.table || { headers: [], rows: [] };
  const columnCount = table.headers.length;
  const headerWidth = 180;
  const contentWidth = Math.floor((960 - 120 - headerWidth) / (columnCount - 1));

  const style = `    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: 28px;
      margin: 0 0 24px 0;
    }
    .table {
      background: ${COLORS.white};
      border-radius: 12px;
      overflow: hidden;
      box-shadow: ${COLORS.cardShadow};
    }
    .table-row {
      display: flex;
      border-bottom: 1px solid ${COLORS.border};
    }
    .table-row:last-child { border-bottom: none; }
    .table-row.header {
      background: ${COLORS.darkBg};
    }
    .cell {
      padding: 16px 24px;
      display: flex;
      align-items: center;
    }
    .cell-header {
      width: ${headerWidth}px;
      flex-shrink: 0;
      background: ${COLORS.headerBg};
    }
    .cell-content {
      width: ${contentWidth}px;
      flex-shrink: 0;
    }
    .table-row.header .cell-header { background: transparent; }
    .table-row.header .cell p {
      color: ${COLORS.white};
      font-size: 14px;
      font-weight: 600;
      margin: 0;
    }
    .cell p {
      font-size: 14px;
      line-height: 1.4;
      margin: 0;
    }
    .cell-header p {
      color: ${COLORS.text};
      font-weight: 600;
    }
    .cell-content p { color: #475569; }
    .highlight {
      color: ${COLORS.primary};
      font-weight: 600;
    }`;

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  // Header row
  const headerCells = table.headers.map((h, i) => {
    const cellClass = i === 0 ? 'cell cell-header' : 'cell cell-content';
    return `        <div class="${cellClass}"><p>${escapeHtml(h)}</p></div>`;
  }).join('\n');

  // Data rows
  const dataRows = table.rows.map(row => {
    const cells = row.map((cell, i) => {
      const cellClass = i === 0 ? 'cell cell-header' : 'cell cell-content';
      // Highlight last column values
      const content = i === row.length - 1 && i > 0
        ? `<span class="highlight">${escapeHtml(cell)}</span>`
        : escapeHtml(cell);
      return `        <div class="${cellClass}"><p>${content}</p></div>`;
    }).join('\n');
    return `      <div class="table-row">
${cells}
      </div>`;
  }).join('\n');

  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="table">
      <div class="table-row header">
${headerCells}
      </div>
${dataRows}
    </div>`;

  return wrapWithBase(style, body);
}

/**
 * Generate Flow Slide (horizontal flow with arrows)
 */
function generateFlowSlide(slide) {
  const items = slide.flowItems || slide.items || [];

  const style = `    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
      display: flex;
      flex-direction: column;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: 28px;
      margin: 0 0 32px 0;
    }
    .content {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .flow {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .flow-item {
      width: 140px;
      flex-shrink: 0;
      border-radius: 12px;
      padding: 20px 16px;
      text-align: center;
      background: ${COLORS.primary};
    }
    .flow-item p {
      color: ${COLORS.white};
      font-size: 14px;
      font-weight: 500;
      margin: 0;
    }
    .arrow {
      color: ${COLORS.primary};
      font-size: 24px;
    }
    .arrow p {
      margin: 0;
    }`;

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  const flowHtml = items.map((item, index) => {
    const arrow = index < items.length - 1 ? '\n        <div class="arrow"><p>→</p></div>' : '';
    return `        <div class="flow-item">
          <p>${escapeHtml(item)}</p>
        </div>${arrow}`;
  }).join('\n');

  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="content">
      <div class="flow">
${flowHtml}
      </div>
    </div>`;

  return wrapWithBase(style, body);
}

/**
 * Generate Mermaid Diagram Slide
 */
function generateMermaidSlide(slide) {
  const codeBlock = slide.codeBlock || { language: 'mermaid', code: '' };

  const style = `    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: 28px;
      margin: 0 0 16px 0;
    }${MERMAID_STYLES.base(COLORS.cardShadow)}`;

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  // Mermaid code should NOT be escaped - Mermaid.js parses it directly
  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="mermaid-container">
      <pre class="mermaid">${codeBlock.code}</pre>
    </div>
    ${MERMAID_SCRIPT}`;

  return wrapWithBase(style, body);
}

function generateCodeSlide(slide) {
  const codeBlock = slide.codeBlock || { language: 'plaintext', code: '' };

  // Special handling for Mermaid diagrams
  if (isMermaidCode(codeBlock)) {
    return generateMermaidSlide(slide);
  }

  const lang = codeBlock.language;

  const style = `    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: 28px;
      margin: 0 0 16px 0;
    }
    .code-container {
      background: #1e1e1e;
      border-radius: 12px;
      padding: 20px 24px;
      overflow: hidden;
    }
    .lang-label {
      color: #858585;
      font-size: 12px;
      margin: 0 0 12px 0;
      font-family: ${FONTS.code};
    }
    pre {
      margin: 0;
      padding: 0;
      background: transparent;
    }
    code {
      font-family: ${FONTS.code};
      font-size: 14px;
      line-height: 1.5;
      color: #d4d4d4;
    }${SYNTAX_HIGHLIGHT_CSS}`;

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  const highlightedCode = highlightCode(codeBlock.code, lang);

  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="code-container">
      <pre><code class="language-${escapeHtml(lang)}">${highlightedCode}</code></pre>
    </div>`;

  return wrapWithBase(style, body);
}

/**
 * Generate Composite Slide (content + code)
 */
function generateCompositeSlide(slide) {
  const layout = slide.compositeLayout || { rows: 1, cols: 2 };
  const items = slide.compositeItems || [];

  // All numeric grid layouts use generateCompositeGrid (1x2, 2x1, 1x3, 2x2, etc.)
  if (layout.rows >= 1 && layout.cols >= 1 && layout.rows <= 8 && layout.cols <= 8) {
    return generateCompositeGrid(slide, items, layout.rows, layout.cols);
  }
  // Fallback to 1x2 grid
  return generateCompositeGrid(slide, items, 1, 2);
}

/**
 * Generate HTML for composite table (div-based for html2pptx compatibility)
 */
function generateCompositeTableHtml(table) {
  if (!table || !table.headers || table.headers.length === 0) return '';

  const columnCount = table.headers.length;
  const cellWidth = Math.floor(100 / columnCount);

  const headerCells = table.headers.map(h =>
    `            <div class="composite-table-cell" style="width: ${cellWidth}%;"><p>${escapeHtml(h)}</p></div>`
  ).join('\n');

  const dataRows = table.rows.map(row => {
    const cells = row.map(cell =>
      `            <div class="composite-table-cell" style="width: ${cellWidth}%;"><p>${escapeHtml(cell)}</p></div>`
    ).join('\n');
    return `          <div class="composite-table-row">\n${cells}\n          </div>`;
  }).join('\n');

  return `        <div class="composite-table">
          <div class="composite-table-row composite-table-header">
${headerCells}
          </div>
${dataRows}
        </div>`;
}

/**
 * Generate HTML for composite flow
 */
function generateCompositeFlowHtml(flowItems) {
  if (!flowItems || flowItems.length === 0) return '';

  const flowHtml = flowItems.map((item, index) => {
    const arrow = index < flowItems.length - 1 ? '\n            <div class="composite-flow-arrow"><p>→</p></div>' : '';
    return `            <div class="composite-flow-item">
              <p>${escapeHtml(item)}</p>
            </div>${arrow}`;
  }).join('\n');

  return `        <div class="composite-flow">\n${flowHtml}\n        </div>`;
}

/**
 * Generate HTML for a nested composite item
 * @param {Object} item - The composite item with compositeLayout and compositeItems
 * @param {number} depth - Current nesting depth (0 = root)
 * @returns {string}
 */
function generateNestedCompositeHtml(item, depth = 0) {
  if (!item.compositeLayout || !item.compositeItems) return '';

  const layout = item.compositeLayout;
  const items = item.compositeItems;

  // Calculate scale factor based on depth
  const scale = Math.pow(0.85, depth);
  const gap = Math.round(12 * scale);

  if (layout.rows === 1 && layout.cols === 2) {
    // Horizontal 1:2 layout
    const leftContent = items[0] ? generateCompositeItemHtml(items[0], depth + 1) : '';
    const rightContent = items.slice(1).map(i => generateCompositeItemHtml(i, depth + 1)).join('\n');

    return `        <div class="nested-composite nested-horizontal level-${depth}" style="display: flex; gap: ${gap}px;">
          <div class="nested-left" style="flex: 1;">
${leftContent}
          </div>
          <div class="nested-right" style="flex: 1;">
${rightContent}
          </div>
        </div>`;
  } else if (layout.rows === 2 && layout.cols === 1) {
    // Vertical 2:1 layout
    const topContent = items[0] ? generateCompositeItemHtml(items[0], depth + 1) : '';
    const bottomContent = items.slice(1).map(i => generateCompositeItemHtml(i, depth + 1)).join('\n');

    return `        <div class="nested-composite nested-vertical level-${depth}" style="display: flex; flex-direction: column; gap: ${gap}px;">
          <div class="nested-top">
${topContent}
          </div>
          <div class="nested-bottom">
${bottomContent}
          </div>
        </div>`;
  } else if (layout.rows === 1 && layout.cols === 3) {
    // Three column layout
    const columns = items.slice(0, 3).map(i => generateCompositeItemHtml(i, depth + 1));
    const columnsHtml = columns.map(c => `          <div class="nested-col" style="flex: 1;">\n${c}\n          </div>`).join('\n');

    return `        <div class="nested-composite nested-three-col level-${depth}" style="display: flex; gap: ${gap}px;">
${columnsHtml}
        </div>`;
  }

  // Fallback
  return items.map(i => generateCompositeItemHtml(i, depth + 1)).join('\n');
}

/**
 * Generate HTML for a single composite item (may be nested)
 * @param {Object} item - The composite item
 * @param {number} depth - Current nesting depth
 * @returns {string}
 */
function generateCompositeItemHtml(item, depth = 0) {
  if (!item) return '';

  if (item.type === 'composite') {
    return generateNestedCompositeHtml(item, depth);
  } else if (item.type === 'bulletList') {
    return generateCompositeContentHtmlWithDepth(item.items, depth);
  } else if (item.type === 'code' && item.codeBlock) {
    return generateCompositeCodeHtmlWithDepth(item.codeBlock, depth);
  } else if (item.type === 'table' && item.table) {
    return generateCompositeTableHtml(item.table);
  } else if (item.type === 'cards' && item.cards) {
    return generateCompositeCardsHtmlWithDepth(item.cards, depth);
  } else if (item.type === 'flow' && item.flowItems) {
    return generateCompositeFlowHtml(item.flowItems);
  }

  return '';
}

/**
 * Generate HTML for composite content with depth-based styling
 */
function generateCompositeContentHtmlWithDepth(items, depth) {
  if (!items || items.length === 0) return '';

  const fontSize = Math.round(14 * Math.pow(0.9, depth));

  const generateNestedList = (items, listDepth = 0) => {
    const listClass = listDepth === 0 ? 'content-list' : 'sub-list';
    const itemsHtml = items.map(item => {
      if (typeof item === 'object' && item.subItems && item.subItems.length > 0) {
        const subListHtml = generateNestedList(item.subItems, listDepth + 1);
        return `          <li>${escapeHtml(item.text)}\n${subListHtml}          </li>`;
      } else {
        const text = typeof item === 'object' ? item.text : item;
        return `          <li>${escapeHtml(text)}</li>`;
      }
    }).join('\n');
    return `        <ul class="${listClass}" style="font-size: ${fontSize}px;">\n${itemsHtml}\n        </ul>`;
  };

  return generateNestedList(items);
}

/**
 * Generate HTML for composite code block with depth-based styling
 */
function generateCompositeCodeHtmlWithDepth(codeBlock, depth) {
  if (!codeBlock) return '';

  // Special handling for Mermaid diagrams
  if (isMermaidCode(codeBlock)) {
    return generateCompositeMermaidHtmlWithDepth(codeBlock, depth);
  }

  const lang = codeBlock.language || 'plaintext';
  const highlightedCode = highlightCode(codeBlock.code, lang);
  const fontSize = Math.round(13 * Math.pow(0.9, depth));
  const padding = Math.round(16 * Math.pow(0.9, depth));

  return `        <div class="code-container" style="padding: ${padding}px; font-size: ${fontSize}px;">
          <pre><code class="language-${escapeHtml(lang)}">${highlightedCode}</code></pre>
        </div>`;
}

/**
 * Generate HTML for Mermaid diagram in composite slides
 * Note: Mermaid code is NOT escaped - Mermaid.js parses it directly
 */
function generateCompositeMermaidHtmlWithDepth(codeBlock, depth) {
  if (!codeBlock) return '';
  const padding = Math.round(16 * Math.pow(0.9, depth));

  return `        <div class="mermaid-container" style="padding: ${padding}px;">
          <pre class="mermaid">${codeBlock.code}</pre>
        </div>`;
}

/**
 * Generate HTML for composite cards with depth-based styling (supports normal, good, bad, step variants)
 */
function generateCompositeCardsHtmlWithDepth(cards, depth) {
  if (!cards || cards.length === 0) return '';

  const fontSize = Math.round(12 * Math.pow(0.9, depth));
  const titleSize = Math.round(14 * Math.pow(0.9, depth));
  const padding = Math.round(12 * Math.pow(0.9, depth));
  const gap = Math.round(10 * Math.pow(0.9, depth));
  const stepNumSize = Math.round(24 * Math.pow(0.9, depth));

  const cardsHtml = cards.map(card => {
    const items = card.items.map(item =>
      `              <li style="font-size: ${fontSize}px;">${escapeHtml(item)}</li>`
    ).join('\n');

    // Handle step variant
    if (card.variant === 'step') {
      const stepNum = card.number !== undefined ? card.number : 0;
      return `          <div class="composite-card composite-card-step" style="padding: ${padding}px; display: flex; gap: ${gap}px; align-items: flex-start;">
            <div class="step-num" style="width: ${stepNumSize}px; height: ${stepNumSize}px; font-size: ${Math.round(fontSize * 1.1)}px;"><p>${stepNum}</p></div>
            <div class="step-content" style="flex: 1;">
              <h3 style="font-size: ${titleSize}px; margin: 0 0 4px 0;">${escapeHtml(card.name)}</h3>
              <ul style="margin: 0; padding-left: 0; list-style: none;">
${items}
              </ul>
            </div>
          </div>`;
    }

    const cardClass = card.variant === 'good' ? 'composite-card composite-card-good'
      : card.variant === 'bad' ? 'composite-card composite-card-bad'
        : 'composite-card';
    return `          <div class="${cardClass}" style="padding: ${padding}px;">
            <h3 style="font-size: ${titleSize}px;">${escapeHtml(card.name)}</h3>
            <ul>
${items}
            </ul>
          </div>`;
  }).join('\n');

  return `        <div class="composite-cards" style="gap: ${gap}px;">\n${cardsHtml}\n        </div>`;
}

/**
 * Calculate grid styles based on dimensions and content density
 * @param {number} rows - Number of rows
 * @param {number} cols - Number of columns
 * @param {Array} items - Composite items
 * @returns {Object} - Calculated style values
 */
function calculateGridStyles(rows, cols, items) {
  const gridSize = Math.max(rows, cols);
  const maxCardsInCell = items.reduce((max, item) =>
    item.type === 'cards' && item.cards ? Math.max(max, item.cards.length) : max, 1);

  const densityFactor = maxCardsInCell > 1 ? Math.min(maxCardsInCell, 2) : 0;
  const gridFactor = gridSize <= 1 ? 0 : gridSize - 1;
  const scaleFactor = Math.max(densityFactor, gridFactor);

  const gap = Math.max(4, 16 - scaleFactor * 2);
  const padding = Math.max(6, 16 - scaleFactor * 2);
  const titleFontSize = Math.max(14, 24 - scaleFactor * 3);
  const itemFontSize = Math.max(14, 20 - scaleFactor * 2);
  const codeFontSize = Math.max(11, Math.round(itemFontSize * 0.75));
  const borderRadius = Math.max(4, 12 - scaleFactor);
  const headerMargin = Math.max(2, 10 - scaleFactor);

  const containerWidth = 840;
  const containerHeight = rows >= 5 ? 400 : 380;
  const cellWidth = Math.floor((containerWidth - (cols - 1) * gap) / cols);
  const cellHeight = Math.floor((containerHeight - (rows - 1) * gap) / rows);

  return {
    gap, padding, titleFontSize, itemFontSize, codeFontSize,
    borderRadius, headerMargin, containerWidth, containerHeight,
    cellWidth, cellHeight, rows, cols, scaleFactor
  };
}

/**
 * Generate grid CSS from calculated styles
 * @param {Object} s - Style values from calculateGridStyles
 * @returns {string} - CSS string
 */
function generateGridCss(s) {
  return `    .slide {
      background: ${COLORS.surface};
      padding: 32px 60px;
    }
    .section-num {
      color: ${COLORS.primary};
      font-size: 14px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    h1 {
      color: ${COLORS.text};
      font-size: ${s.rows >= 5 ? 22 : 28}px;
      margin: 0 0 ${s.rows >= 5 ? 10 : 16}px 0;
    }
    .grid-container {
      display: flex;
      flex-wrap: wrap;
      gap: ${s.gap}px;
      width: ${s.containerWidth}px;
      height: ${s.containerHeight}px;
      align-content: flex-start;
    }
    .grid-cell {
      width: ${s.cellWidth}px;
      height: ${s.cellHeight}px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
    }
    .grid-cell-card {
      background: ${COLORS.white};
      border-radius: ${s.borderRadius}px;
      padding: ${s.padding}px;
      box-shadow: ${COLORS.cardShadow};
    }
    .grid-cell h3 {
      color: ${COLORS.primary};
      font-size: ${s.titleFontSize}px;
      font-weight: 600;
      margin: 0 0 ${s.headerMargin}px 0;
      line-height: 1.2;
    }
    .grid-cell ul {
      margin: 0;
      padding-left: ${Math.max(10, 18 - Math.max(s.rows, s.cols))}px;
    }
    .grid-cell li {
      color: ${COLORS.muted};
      font-size: ${s.itemFontSize}px;
      line-height: 1.4;
      margin-bottom: ${Math.max(1, 4 - Math.max(s.rows, s.cols) / 2)}px;
    }
    .grid-cell li:last-child {
      margin-bottom: 0;
    }
    .grid-cell-nested {
      padding: ${Math.max(2, s.padding / 2)}px;
    }
    .nested-grid {
      height: 100%;
    }
    .nested-cell {
      background: ${COLORS.surface};
      border-radius: ${Math.max(2, s.borderRadius / 2)}px;
      padding: ${Math.max(2, s.padding / 2)}px;
      overflow: hidden;
    }
    .nested-cell h4 {
      color: ${COLORS.primary};
      font-size: ${Math.max(8, s.titleFontSize - 2)}px;
      font-weight: 600;
      margin: 0 0 ${Math.max(2, s.headerMargin / 2)}px 0;
      line-height: 1.2;
    }
    .nested-cell ul {
      margin: 0;
      padding-left: ${Math.max(8, 14 - Math.max(s.rows, s.cols))}px;
    }
    .nested-cell li {
      color: ${COLORS.muted};
      font-size: ${Math.max(6, s.itemFontSize - 2)}px;
      line-height: 1.3;
    }
    .grid-cell-code {
      background: #1e1e1e;
      padding: ${Math.max(8, s.padding)}px;
    }
    .grid-cell-code pre {
      margin: 0;
      padding: 0;
      background: transparent;
      white-space: pre-wrap;
    }
    .grid-cell-code code {
      font-family: ${FONTS.code};
      font-size: ${s.codeFontSize}px;
      line-height: 1.4;
      color: #d4d4d4;
    }${SYNTAX_HIGHLIGHT_CSS}${MERMAID_STYLES.grid(s)}
    .grid-cell-multi-cards {
      display: flex;
      flex-direction: column;
      gap: ${Math.max(4, s.gap / 2)}px;
      padding: ${Math.max(6, s.padding / 2)}px;
    }
    .inline-card {
      background: ${COLORS.surface};
      border-radius: ${Math.max(4, s.borderRadius / 2)}px;
      padding: ${Math.max(8, s.padding / 2)}px ${Math.max(8, s.padding / 2)}px ${Math.max(8, s.padding / 2)}px ${Math.max(12, s.padding)}px;
    }
    .inline-card h4 {
      color: ${COLORS.primary};
      font-size: ${Math.max(10, s.titleFontSize - 2)}px;
      font-weight: 600;
      margin: 0 0 ${Math.max(2, s.headerMargin / 2)}px 0;
    }
    .inline-card ul {
      margin: 0;
      padding-left: ${Math.max(10, 16 - Math.max(s.rows, s.cols))}px;
    }
    .inline-card li {
      color: ${COLORS.muted};
      font-size: ${Math.max(8, s.itemFontSize - 1)}px;
      line-height: 1.3;
    }
    .card-code {
      background: #1e1e1e;
      border-radius: ${Math.max(4, s.borderRadius / 2)}px;
      padding: ${Math.max(4, s.padding / 3)}px ${Math.max(6, s.padding / 2)}px;
      margin-top: ${Math.max(4, s.headerMargin / 2)}px;
      overflow: hidden;
    }
    .card-code code {
      font-family: ${FONTS.code};
      font-size: ${Math.max(9, s.codeFontSize - 1)}px;
      line-height: 1.3;
      color: #d4d4d4;
      white-space: pre-wrap;
    }
    .inline-card.inline-card-good {
      background: ${COLORS.goodBackground};
    }
    .inline-card.inline-card-good h4 {
      color: ${COLORS.goodForeground};
    }
    .inline-card.inline-card-good li {
      color: ${COLORS.goodForeground};
    }
    .inline-card.inline-card-bad {
      background: ${COLORS.badBackground};
    }
    .inline-card.inline-card-bad h4 {
      color: ${COLORS.badForeground};
    }
    .inline-card.inline-card-bad li {
      color: ${COLORS.badForeground};
    }
    .inline-card-step {
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }
    .inline-card-step .step-num {
      width: 20px;
      height: 20px;
      flex-shrink: 0;
      background: linear-gradient(135deg, ${COLORS.primary} 0%, #0E7490 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: ${COLORS.white};
      font-size: 11px;
      font-weight: 700;
    }
    .inline-card-step .step-content {
      flex: 1;
      min-width: 0;
    }
    .inline-card-step .step-content h4 {
      margin: 0 0 2px 0;
    }
    .inline-card-step .step-content ul {
      margin: 0;
      padding-left: 0;
      list-style: none;
    }
    .grid-cell-card.grid-cell-card-good {
      background: ${COLORS.goodBackground};
    }
    .grid-cell-card.grid-cell-card-good h3 {
      color: ${COLORS.goodForeground};
    }
    .grid-cell-card.grid-cell-card-good li {
      color: ${COLORS.goodForeground};
    }
    .grid-cell-card.grid-cell-card-bad {
      background: ${COLORS.badBackground};
    }
    .grid-cell-card.grid-cell-card-bad h3 {
      color: ${COLORS.badForeground};
    }
    .grid-cell-card.grid-cell-card-bad li {
      color: ${COLORS.badForeground};
    }
    .nested-cell.nested-cell-good {
      background: ${COLORS.goodBackground};
    }
    .nested-cell.nested-cell-good h4 {
      color: ${COLORS.goodForeground};
    }
    .nested-cell.nested-cell-good li {
      color: ${COLORS.goodForeground};
    }
    .nested-cell.nested-cell-bad {
      background: ${COLORS.badBackground};
    }
    .nested-cell.nested-cell-bad h4 {
      color: ${COLORS.badForeground};
    }
    .nested-cell.nested-cell-bad li {
      color: ${COLORS.badForeground};
    }
    .grid-cell-table {
      padding: ${Math.max(4, s.padding / 2)}px;
    }
    .grid-table {
      width: 100%;
    }
    .grid-table-row {
      display: flex;
      width: 100%;
    }
    .grid-table-header-row {
      background: ${COLORS.primary};
    }
    .grid-table-cell {
      padding: ${Math.max(4, s.padding / 3)}px;
      border: 1px solid ${COLORS.border};
    }
    .grid-table-cell p {
      margin: 0;
      font-size: ${Math.max(8, s.itemFontSize - 1)}px;
      color: ${COLORS.text};
    }
    .grid-table-header-cell p {
      color: ${COLORS.white};
      font-weight: 600;
    }
    .grid-cell-flow {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .grid-flow {
      display: flex;
      align-items: center;
      gap: ${Math.max(4, s.gap / 2)}px;
      flex-wrap: wrap;
      justify-content: center;
    }
    .grid-flow-item {
      background: ${COLORS.primary};
      border-radius: ${Math.max(4, s.borderRadius / 2)}px;
      padding: ${Math.max(4, s.padding / 3)}px ${Math.max(8, s.padding / 2)}px;
    }
    .grid-flow-item p {
      margin: 0;
      color: ${COLORS.white};
      font-size: ${Math.max(9, s.itemFontSize)}px;
      font-weight: 500;
    }
    .grid-flow-arrow p {
      margin: 0;
      color: ${COLORS.muted};
      font-size: ${Math.max(12, s.titleFontSize)}px;
    }`;
}

/**
 * Generate grid composite slide (NxM layout, supports 1x2 to 8x8)
 * @param {Object} slide - Slide data
 * @param {Array} items - Composite items
 * @param {number} rows - Number of rows (2-8)
 * @param {number} cols - Number of columns (2-8)
 */
function generateCompositeGrid(slide, items, rows, cols) {
  const totalCells = rows * cols;

  // Calculate responsive sizes using extracted function
  const s = calculateGridStyles(rows, cols, items);

  // Generate CSS using extracted function
  const style = generateGridCss(s);

  const section = slide.section ? `    <p class="section-num">${escapeHtml(slide.section)}</p>\n` : '';
  const title = slide.title || slide.name;

  // Expand items only if needed to fill the grid
  // If original items count >= totalCells, keep items as-is (each item gets one cell)
  // If original items count < totalCells, expand cards to fill cells
  let expandedItems = [];
  if (items.length >= totalCells) {
    // Keep items as-is - each item gets one cell
    expandedItems = items;
  } else {
    // Expand cards to fill available cells
    for (const item of items) {
      if (item.type === 'cards' && item.cards && item.cards.length > 1) {
        for (const card of item.cards) {
          expandedItems.push({ type: 'cards', cards: [card] });
        }
      } else {
        expandedItems.push(item);
      }
    }
  }

  // Helper to render a cards item (may contain multiple cards)
  const renderCardsCell = (item) => {
    if (item.cards.length === 1) {
      // Single card - with white card container
      const card = item.cards[0];
      const itemsHtml = card.items.map(i => `          <li>${escapeHtml(i)}</li>`).join('\n');
      const codeBlockHtml = card.codeBlock ? `
        <div class="card-code"><pre><code class="language-${escapeHtml(card.codeBlock.language)}">${highlightCode(card.codeBlock.code, card.codeBlock.language)}</code></pre></div>` : '';

      const variantClass = card.variant === 'good' ? ' grid-cell-card-good'
        : card.variant === 'bad' ? ' grid-cell-card-bad'
          : '';

      return `      <div class="grid-cell grid-cell-card${variantClass}">
        <h3>${escapeHtml(card.name)}</h3>
        <ul>
${itemsHtml}
        </ul>${codeBlockHtml}
      </div>`;
    } else {
      // Multiple cards in one cell - render as inline cards
      const cardsHtml = item.cards.map(card => {
        const itemsHtml = card.items.map(i => `            <li>${escapeHtml(i)}</li>`).join('\n');
        const codeBlockHtml = card.codeBlock ? `
            <div class="card-code"><code class="language-${escapeHtml(card.codeBlock.language)}">${highlightCode(card.codeBlock.code, card.codeBlock.language)}</code></div>` : '';

        // Handle step variant with step number badge
        if (card.variant === 'step') {
          const stepNum = card.number !== undefined ? card.number : '';
          return `          <div class="inline-card inline-card-step">
            <div class="step-num"><p>${stepNum}</p></div>
            <div class="step-content">
              <h4>${escapeHtml(card.name)}</h4>
              <ul>
${itemsHtml}
              </ul>${codeBlockHtml}
            </div>
          </div>`;
        }

        const cardClass = card.variant === 'good' ? 'inline-card inline-card-good'
          : card.variant === 'bad' ? 'inline-card inline-card-bad'
            : 'inline-card';
        return `          <div class="${cardClass}">
            <h4>${escapeHtml(card.name)}</h4>
            <ul>
${itemsHtml}
            </ul>${codeBlockHtml}
          </div>`;
      }).join('\n');
      return `      <div class="grid-cell grid-cell-multi-cards">
${cardsHtml}
      </div>`;
    }
  };

  // Generate cells for grid
  const cellsHtml = expandedItems.slice(0, totalCells).map(item => {
    if (item.type === 'composite' && item.compositeLayout && item.compositeItems) {
      // Nested composite - render as nested grid
      const nestedHtml = generateNestedGridHtml(item, rows, cols);
      return `      <div class="grid-cell grid-cell-nested">\n${nestedHtml}\n      </div>`;
    } else if (item.type === 'cards' && item.cards && item.cards.length > 0) {
      return renderCardsCell(item);
    } else if (item.type === 'bulletList' && item.items) {
      const itemsHtml = item.items.map(i => {
        const text = typeof i === 'string' ? i : i.text;
        return `          <li>${escapeHtml(text)}</li>`;
      }).join('\n');
      return `      <div class="grid-cell">
        <ul>
${itemsHtml}
        </ul>
      </div>`;
    } else if (item.type === 'code' && item.codeBlock) {
      // Special handling for Mermaid diagrams (NOT escaped)
      if (isMermaidCode(item.codeBlock)) {
        return `      <div class="grid-cell grid-cell-mermaid">
        <div class="mermaid-container">
          <pre class="mermaid">${item.codeBlock.code}</pre>
        </div>
      </div>`;
      }
      const lang = item.codeBlock.language || 'plaintext';
      const highlightedCode = highlightCode(item.codeBlock.code, lang);
      return `      <div class="grid-cell grid-cell-code">
        <pre><code class="language-${escapeHtml(lang)}">${highlightedCode}</code></pre>
      </div>`;
    } else if (item.type === 'table' && item.table) {
      return generateGridTableCell(item.table);
    } else if (item.type === 'flow' && item.flowItems) {
      return generateGridFlowCell(item.flowItems);
    }
    return `      <div class="grid-cell"></div>`;
  }).join('\n');

  // Fill remaining cells if less than totalCells items
  const filledCells = expandedItems.length < totalCells
    ? cellsHtml + '\n' + Array(totalCells - expandedItems.length).fill('      <div class="grid-cell"></div>').join('\n')
    : cellsHtml;

  // Determine required CDN scripts (check both original items and expanded items)
  const requiredScripts = getRequiredScripts([...items, ...expandedItems]);
  const mermaidScript = requiredScripts.has('mermaid') ? generateCdnScript('mermaid') : '';

  const body = `${section}    <h1>${escapeHtml(title)}</h1>
    <div class="grid-container">
${filledCells}
    </div>${mermaidScript}`;

  return wrapWithBase(style, body);
}

/**
 * Generate HTML for nested grid within a parent grid cell
 * @param {Object} item - Nested composite item
 * @param {number} parentRows - Parent grid rows (for sizing)
 * @param {number} parentCols - Parent grid cols (for sizing)
 */
function generateNestedGridHtml(item, parentRows, parentCols) {
  const layout = item.compositeLayout;
  const items = item.compositeItems || [];
  const nestedRows = layout.rows;
  const nestedCols = layout.cols;
  const totalCells = nestedRows * nestedCols;

  // Calculate gap for nested grid based on parent size
  const depth = Math.max(parentRows, parentCols);
  const gap = Math.max(2, 8 - depth);

  // Expand nested cards
  let expandedItems = [];
  for (const nestedItem of items) {
    if (nestedItem.type === 'cards' && nestedItem.cards && nestedItem.cards.length > 1) {
      for (const card of nestedItem.cards) {
        expandedItems.push({ type: 'cards', cards: [card] });
      }
    } else {
      expandedItems.push(nestedItem);
    }
  }

  // Generate nested cells
  const cellsHtml = expandedItems.slice(0, totalCells).map(nestedItem => {
    if (nestedItem.type === 'cards' && nestedItem.cards && nestedItem.cards.length > 0) {
      const card = nestedItem.cards[0];
      const itemsHtml = card.items.map(i => `              <li>${escapeHtml(i)}</li>`).join('\n');

      const variantClass = card.variant === 'good' ? ' nested-cell-good'
        : card.variant === 'bad' ? ' nested-cell-bad'
          : '';

      return `          <div class="nested-cell${variantClass}">
            <h4>${escapeHtml(card.name)}</h4>
            <ul>
${itemsHtml}
            </ul>
          </div>`;
    } else if (nestedItem.type === 'bulletList' && nestedItem.items) {
      const itemsHtml = nestedItem.items.map(i => {
        const text = typeof i === 'string' ? i : i.text;
        return `              <li>${escapeHtml(text)}</li>`;
      }).join('\n');
      return `          <div class="nested-cell">
            <ul>
${itemsHtml}
            </ul>
          </div>`;
    }
    return `          <div class="nested-cell"></div>`;
  }).join('\n');

  // Fill remaining cells
  const filledCells = expandedItems.length < totalCells
    ? cellsHtml + '\n' + Array(totalCells - expandedItems.length).fill('          <div class="nested-cell"></div>').join('\n')
    : cellsHtml;

  return `        <div class="nested-grid" style="display: grid; grid-template-columns: repeat(${nestedCols}, 1fr); grid-template-rows: repeat(${nestedRows}, 1fr); gap: ${gap}px; height: 100%;">
${filledCells}
        </div>`;
}

/**
 * Generate a table cell for grid layout
 */
function generateGridTableCell(table) {
  if (!table || !table.headers || table.headers.length === 0) return '      <div class="grid-cell"></div>';

  const columnCount = table.headers.length;
  const cellWidth = Math.floor(100 / columnCount);

  const headerCells = table.headers.map(h =>
    `              <div class="grid-table-cell grid-table-header-cell" style="width: ${cellWidth}%;"><p>${escapeHtml(h)}</p></div>`
  ).join('\n');

  const dataRows = table.rows.map(row => {
    const cells = row.map(cell =>
      `              <div class="grid-table-cell" style="width: ${cellWidth}%;"><p>${escapeHtml(cell)}</p></div>`
    ).join('\n');
    return `            <div class="grid-table-row">\n${cells}\n            </div>`;
  }).join('\n');

  return `      <div class="grid-cell grid-cell-table">
          <div class="grid-table">
            <div class="grid-table-row grid-table-header-row">
${headerCells}
            </div>
${dataRows}
          </div>
      </div>`;
}

/**
 * Generate a flow cell for grid layout
 */
function generateGridFlowCell(flowItems) {
  if (!flowItems || flowItems.length === 0) return '      <div class="grid-cell"></div>';

  const flowHtml = flowItems.map((item, index) => {
    const arrow = index < flowItems.length - 1 ? '\n            <div class="grid-flow-arrow"><p>→</p></div>' : '';
    return `            <div class="grid-flow-item">
              <p>${escapeHtml(item)}</p>
            </div>${arrow}`;
  }).join('\n');

  return `      <div class="grid-cell grid-cell-flow">
          <div class="grid-flow">
${flowHtml}
          </div>
      </div>`;
}

/**
 * Generate HTML for a slide based on its type
 */
function generateSlideHtml(slide) {
  switch (slide.type) {
    case 'title':
      return generateTitleSlide(slide);
    case 'composite':
      return generateCompositeSlide(slide);
    case 'cards':
      return generateCardsSlide(slide);
    case 'table':
      return generateTableSlide(slide);
    case 'flow':
      return generateFlowSlide(slide);
    case 'code':
      return generateCodeSlide(slide);
    case 'bulletList':
    default:
      return generateContentSlide(slide);
  }
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

module.exports = { generateSlideHtml, setThemeConfig, THEME, COLORS, FONTS, TYPOGRAPHY };
