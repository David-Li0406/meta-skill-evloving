/**
 * Markdown Parser for md2html
 * Parses markdown slide definitions into structured data
 */

/**
 * @typedef {Object} CardDef
 * @property {string} name
 * @property {string[]} items
 * @property {CodeBlockDef} [codeBlock]
 * @property {'normal'|'good'|'bad'|'step'} [variant] - Card style variant (default: 'normal')
 * @property {number} [number] - Step number (only used when variant='step')
 */

/**
 * @typedef {Object} TableDef
 * @property {string[]} headers
 * @property {string[][]} rows
 */


/**
 * @typedef {Object} CodeBlockDef
 * @property {string} language
 * @property {string} code
 */

/**
 * @typedef {Object} SubItem
 * @property {string} text
 * @property {string[]} [subSubItems]
 */

/**
 * @typedef {Object} ContentItem
 * @property {string} text
 * @property {SubItem[]} [subItems]
 */

/**
 * @typedef {Object} SlideDefinition
 * @property {number} number
 * @property {string} name
 * @property {'title'|'bulletList'|'cards'|'table'|'flow'|'code'} type
 * @property {number} [partNumber]
 * @property {string} [mainTitle]
 * @property {string} [subtitle]
 * @property {string} [section]
 * @property {string} [title]
 * @property {string[]|ContentItem[]} [items]
 * @property {CardDef[]} [cards]
 * @property {TableDef} [table]
 * @property {string[]} [flowItems]
 * @property {CodeBlockDef} [codeBlock]
 * @property {'horizontal'|'vertical'} [layout] - Card layout direction (default: 'horizontal')
 */

/**
 * @typedef {Object} CompositeLayoutDef
 * @property {number} rows
 * @property {number} cols
 * @property {boolean} reverse
 */

/**
 * @typedef {Object} CompositeItemDef
 * @property {'bulletList'|'code'|'table'|'cards'|'flow'|'composite'} type
 * @property {ContentItem[]} [items]
 * @property {CodeBlockDef} [codeBlock]
 * @property {TableDef} [table]
 * @property {CardDef[]} [cards]
 * @property {string[]} [flowItems]
 * @property {CompositeLayoutDef} [compositeLayout]
 * @property {CompositeItemDef[]} [compositeItems]
 * @property {'horizontal'|'vertical'} [layout] - Card layout direction (default: 'horizontal')
 */

/**
 * Maximum nesting depth for composite slides
 */
const MAX_COMPOSITE_DEPTH = 3;

// ============================================================================
// Refactored parsing functions
// ============================================================================

/**
 * Split markdown into slide chunks by ## headers
 * @param {string[]} lines
 * @returns {{header: string, bodyLines: string[]}[]}
 */
function splitBySlideHeaders(lines) {
  const chunks = [];
  let currentChunk = null;
  let inCodeBlock = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // Track code fence boundaries
    if (PATTERNS.codeBlockMarker.test(trimmed)) {
      inCodeBlock = !inCodeBlock;
    }

    if (!inCodeBlock && PATTERNS.slideHeader.test(trimmed)) {
      if (currentChunk) chunks.push(currentChunk);
      currentChunk = { header: trimmed, bodyLines: [] };
    } else if (currentChunk) {
      currentChunk.bodyLines.push(line);
    }
  }
  if (currentChunk) chunks.push(currentChunk);
  return chunks;
}

/**
 * Parse slide header to extract number, section, and title
 * @param {string} header
 * @param {number} index - 0-based chunk index
 * @returns {{number: number, name: string, section?: string, title?: string, partNumber?: number, mainTitle?: string}}
 */
function parseSlideHeader(header, index) {
  // Check for title slide header: ## PART N:メインタイトル
  const titleSlideMatch = header.match(PATTERNS.titleSlideHeader);
  if (titleSlideMatch) {
    const partNumber = parseInt(titleSlideMatch[1], 10);
    const mainTitle = titleSlideMatch[2].trim();
    return {
      number: index + 1,
      name: mainTitle,
      partNumber,
      mainTitle,
    };
  }

  const numberedMatch = header.match(PATTERNS.slideNumbered);
  if (numberedMatch) {
    const sectionStr = numberedMatch[1];
    const titleStr = numberedMatch[2].trim();
    return {
      number: index + 1,
      name: titleStr,
      section: sectionStr,
      title: titleStr,
    };
  }
  const simpleMatch = header.match(PATTERNS.slideSimple);
  return { number: index + 1, name: simpleMatch ? simpleMatch[1].trim() : '' };
}

/**
 * Detect slide type from body lines
 * @param {string[]} bodyLines
 * @returns {string}
 */
function detectSlideType(bodyLines) {
  let hasCards = false;
  let hasOtherElement = false;

  for (const line of bodyLines) {
    const match = line.match(PATTERNS.listItem);
    if (!match) continue;
    const content = match[2];

    if (PATTERNS.composite.test(content)) return 'composite';
    if (PATTERNS.part.test(content)) return 'title';

    // Track cards and other element types at top level (indent=0)
    const indent = match[1].length;
    if (indent === 0) {
      if (PATTERNS.card.test(content) || PATTERNS.good.test(content) || PATTERNS.bad.test(content) || PATTERNS.step.test(content)) {
        hasCards = true;
      } else if (matchElementType(content)) {
        hasOtherElement = true;
      }
    }

    if (PATTERNS.table.test(content)) {
      if (hasCards) return 'composite';
      return 'table';
    }
    if (PATTERNS.flow.test(content)) {
      if (hasCards) return 'composite';
      return 'flow';
    }
  }

  // Cards mixed with other element types → treat as composite
  if (hasCards && hasOtherElement) return 'composite';
  if (hasCards) return 'cards';

  // Check for inline table
  if (bodyLines.some(l => PATTERNS.tableRow.test(l.trim()))) return 'table';
  // Check for code block
  if (bodyLines.some(l => PATTERNS.codeBlockMarker.test(l.trim()))) return 'code';
  return 'bulletList';
}

/**
 * Parse section and title metadata from body lines (pure function)
 * @param {string[]} bodyLines
 * @returns {{section?: string, title?: string, subtitle?: string, layout?: 'horizontal'|'vertical'}}
 */
function parseSlideMetadata(bodyLines) {
  const result = {};

  for (const line of bodyLines) {
    const match = line.match(PATTERNS.listItem);
    if (!match) continue;
    const content = match[2];

    const sectionMatch = content.match(PATTERNS.section);
    if (sectionMatch) {
      result.section = sectionMatch[1].trim();
      continue;
    }

    const titleMatch = content.match(PATTERNS.title);
    if (titleMatch) {
      result.title = titleMatch[1].trim();
      continue;
    }

    const subtitleMatch = content.match(PATTERNS.subtitle);
    if (subtitleMatch) {
      result.subtitle = subtitleMatch[1].trim();
      continue;
    }

    const layoutMatch = content.match(PATTERNS.layout);
    if (layoutMatch) {
      const layoutValue = layoutMatch[1].trim().toLowerCase();
      if (layoutValue === 'vertical' || layoutValue === 'horizontal') {
        result.layout = layoutValue;
      }
    }
  }

  return result;
}

/**
 * Type-specific slide parsers (pure functions returning partial slide data)
 */
const slideParsers = {
  /**
   * Parse title slide - extracts subtitle from body lines
   * partNumber and mainTitle come from header via parseSlideHeader
   * @param {string[]} lines - Body lines
   * @param {{partNumber?: number, mainTitle?: string}} base - Base info from header
   * @returns {{subtitle?: string}}
   */
  title: (lines, _base) => {
    const result = {};

    for (const line of lines) {
      const match = line.match(PATTERNS.listItem);
      if (!match) continue;
      const content = match[2];

      const subtitleMatch = content.match(PATTERNS.subtitle);
      if (subtitleMatch) {
        result.subtitle = subtitleMatch[1].trim();
        break;
      }
    }

    return result;
  },

  bulletList: (lines) => {
    /** @type {{indent: number, content: string}[]} */
    const parsedLines = lines
      .map(line => line.match(PATTERNS.listItem))
      .filter(Boolean)
      .map(([, spaces, content]) => ({ indent: spaces.length, content }));

    const isMetadata = (content) =>
      PATTERNS.section.test(content) || PATTERNS.title.test(content);

    const initialState = {
      items: [],
      active: false,
    };

    const addTopLevelItem = (items, content) => [
      ...items,
      { text: content, subItems: [] },
    ];

    const addSubItem = (items, content) => {
      if (items.length === 0) return items;
      const lastItem = items[items.length - 1];
      return [
        ...items.slice(0, -1),
        {
          ...lastItem,
          subItems: [...lastItem.subItems, { text: content, subSubItems: [] }],
        },
      ];
    };

    const addSubSubItem = (items, content) => {
      if (items.length === 0) return items;
      const lastItem = items[items.length - 1];
      if (lastItem.subItems.length === 0) return items;
      const lastSubItem = lastItem.subItems[lastItem.subItems.length - 1];
      return [
        ...items.slice(0, -1),
        {
          ...lastItem,
          subItems: [
            ...lastItem.subItems.slice(0, -1),
            { ...lastSubItem, subSubItems: [...lastSubItem.subSubItems, content] },
          ],
        },
      ];
    };

    const finalState = parsedLines.reduce((state, { indent, content }) => {
      if (isMetadata(content)) return state;
      if (PATTERNS.bulletList.test(content)) return { ...state, active: true };
      if (!state.active) return state;

      if (indent < INDENT.FIRST_LEVEL) {
        return { ...state, items: addTopLevelItem(state.items, content) };
      }
      if (indent < INDENT.SECOND_LEVEL) {
        return { ...state, items: addSubItem(state.items, content) };
      }
      return { ...state, items: addSubSubItem(state.items, content) };
    }, initialState);

    return { items: finalState.items };
  },

  code: (lines) => {
    const startIdx = lines.findIndex(l => PATTERNS.codeBlockMarker.test(l.trim()));
    if (startIdx === -1) return {};

    const lang = lines[startIdx].trim().slice(3).trim() || 'plaintext';
    const endIdx = lines.findIndex((l, i) => i > startIdx && PATTERNS.codeBlockMarker.test(l.trim()));
    if (endIdx === -1) return {};

    const codeLines = lines.slice(startIdx + 1, endIdx);
    return { codeBlock: { language: lang, code: codeLines.join('\n') } };
  },

  table: (lines) => {
    const tableLines = lines.filter(l => PATTERNS.tableRow.test(l.trim())).map(l => l.trim());
    if (tableLines.length > 0) {
      return { table: parseTable(tableLines) };
    }
    return {};
  },

  cards: (lines) => {
    const isMetadata = (content) =>
      PATTERNS.section.test(content) || PATTERNS.title.test(content) || PATTERNS.layout.test(content);

    const parseCardHeader = (content) => {
      const cardMatch = content.match(PATTERNS.card);
      if (cardMatch) return { name: cardMatch[2].trim(), variant: 'normal', number: null };
      const stepMatch = content.match(PATTERNS.step);
      if (stepMatch) return { name: stepMatch[2].trim(), variant: 'step', number: parseInt(stepMatch[1], 10) };
      const goodMatch = content.match(PATTERNS.good);
      if (goodMatch) return { name: goodMatch[1].trim(), variant: 'good', number: null };
      const badMatch = content.match(PATTERNS.bad);
      if (badMatch) return { name: badMatch[1].trim(), variant: 'bad', number: null };
      return null;
    };

    const finalizeCard = (state) =>
      state.currentCard
        ? { ...state, cards: [...state.cards, state.currentCard], currentCard: null }
        : state;

    const initialState = {
      cards: [],
      currentCard: null,
      inCodeBlock: false,
      codeBlockLang: '',
      codeBlockLines: [],
    };

    const finalState = lines.reduce((state, line) => {
      const trimmed = line.trim();

      // Handle code block markers
      if (PATTERNS.codeBlockMarker.test(trimmed)) {
        if (!state.inCodeBlock) {
          return {
            ...state,
            inCodeBlock: true,
            codeBlockLang: trimmed.slice(3).trim() || 'plaintext',
            codeBlockLines: [],
          };
        }
        // End code block: attach to current card
        if (state.currentCard) {
          return {
            ...state,
            inCodeBlock: false,
            currentCard: {
              ...state.currentCard,
              codeBlock: { language: state.codeBlockLang, code: state.codeBlockLines.join('\n') },
            },
          };
        }
        return { ...state, inCodeBlock: false };
      }

      // Collect code block lines
      if (state.inCodeBlock) {
        return { ...state, codeBlockLines: [...state.codeBlockLines, line] };
      }

      // Parse list items
      const match = line.match(PATTERNS.listItem);
      if (!match) return state;
      const [, spaces, content] = match;
      const indent = spaces.length;

      if (isMetadata(content)) return state;

      // Check for card header
      const header = parseCardHeader(content);
      if (header) {
        const finalized = finalizeCard(state);
        const newCard = createCard(header.name, header.variant);
        if (header.number !== null) {
          newCard.number = header.number;
        }
        return { ...finalized, currentCard: newCard };
      }

      // Add item to current card
      if (state.currentCard && indent >= INDENT.TOP_LEVEL) {
        return {
          ...state,
          currentCard: { ...state.currentCard, items: [...state.currentCard.items, content] },
        };
      }

      return state;
    }, initialState);

    const { cards } = finalizeCard(finalState);
    return { cards };
  },

  flow: (lines) => {
    const parsedLines = lines
      .map(line => line.match(PATTERNS.listItem))
      .filter(Boolean)
      .map(([, spaces, content]) => ({ indent: spaces.length, content }));

    const initialState = { flowItems: [], active: false };

    const { flowItems } = parsedLines.reduce((state, { indent, content }) => {
      if (PATTERNS.flow.test(content)) return { ...state, active: true };
      if (state.active && indent >= INDENT.TOP_LEVEL) {
        return { ...state, flowItems: [...state.flowItems, content] };
      }
      return state;
    }, initialState);

    return { flowItems };
  },

  composite: (lines) => {
    const compositeIndex = lines.findIndex(line => {
      const match = line.match(PATTERNS.listItem);
      return match && PATTERNS.composite.test(match[2]);
    });

    if (compositeIndex === -1) {
      // No explicit 複合: line — implicit composite (e.g., cards + Mermaid mixed)
      const result = parseCompositeItems(lines, 0, 0, 0);
      if (result.items.length >= 2) {
        return { compositeLayout: { rows: 1, cols: result.items.length }, compositeItems: result.items };
      }
      return {};
    }

    const match = lines[compositeIndex].match(PATTERNS.listItem);
    const compositeMatch = match[2].match(PATTERNS.composite);
    const layout = parseCompositeLayout(compositeMatch[1].trim());

    if (!layout) return {};

    const result = parseCompositeItems(lines, compositeIndex + 1, INDENT.TOP_LEVEL, 0);
    return { compositeLayout: layout, compositeItems: result.items };
  },
};

/**
 * Indentation levels in spaces
 */
const INDENT = {
  TOP_LEVEL: 2,
  FIRST_LEVEL: 4,
  SECOND_LEVEL: 6,
};

/**
 * Regex patterns for parsing markdown elements
 */
const PATTERNS = {
  slideNumbered: /^##\s*(\d+(?:\.\d+)?)[:：]\s*(.+)$/,
  slideSimple: /^##\s+(.+)$/,
  slideHeader: /^##\s/,
  titleSlideHeader: /^##\s*(?:PART\s*)?(\d+)部?[:：]\s*(.+)$/i,
  part: /^PART\s*(\d+)$/i,
  section: /^セクション[:：]\s*(.+)$/,
  title: /^タイトル[:：]\s*(.+)$/,
  subtitle: /^副題[:：]\s*(.+)$/,
  layout: /^layout[:：]\s*(.+)$/i,
  composite: /^複合[:：]\s*(.+)$/,
  bulletList: /^(内容|箇条書き|リスト)[:：]?\s*$/,
  code: /^コード[:：]?\s*$/,
  mermaid: /^[Mm]ermaid[:：]?\s*$/,
  table: /^テーブル[:：]?\s*$/,
  flow: /^フロー[:：]?\s*$/,
  card: /^カード(\d+)[:：]\s*(.+)$/,
  step: /^ステップ(\d+)[:：]\s*(.+)$/,
  good: /^Good[:：]\s*(.+)$/,
  bad: /^Bad[:：]\s*(.+)$/,
  tableRow: /^\|.+\|$/,
  tableSeparator: /^\|[-:\s|]+\|$/,
  listItem: /^(\s*)-\s+(.+)$/,
  codeBlockMarker: /^```/,
};

/**
 * Create a card definition
 * @param {string} name - Card name
 * @param {'normal'|'good'|'bad'|'step'} [variant='normal'] - Card variant
 * @returns {CardDef}
 */
function createCard(name, variant = 'normal') {
  const card = { name, items: [] };
  if (variant !== 'normal') {
    card.variant = variant;
  }
  return card;
}

/**
 * Card matcher definitions for declarative card pattern matching
 * Each matcher defines: pattern, variant, name extractor, optional number extractor, and group compatibility check
 */
const CARD_MATCHERS = [
  {
    pattern: PATTERNS.card,
    variant: 'normal',
    getName: (match) => match[2].trim(),
    shouldStartNewGroup: (cards) => cards.length > 0 && cards.every(c => c.variant === 'step')
  },
  {
    pattern: PATTERNS.step,
    variant: 'step',
    getName: (match) => match[2].trim(),
    getNumber: (match) => parseInt(match[1], 10),
    shouldStartNewGroup: (cards) => cards.some(c => c.variant !== 'step')
  },
  {
    pattern: PATTERNS.good,
    variant: 'good',
    getName: (match) => match[1].trim(),
    shouldStartNewGroup: () => false
  },
  {
    pattern: PATTERNS.bad,
    variant: 'bad',
    getName: (match) => match[1].trim(),
    shouldStartNewGroup: () => false
  }
];

/**
 * Find matching card pattern in content
 * @param {string} content - Content to match against
 * @returns {{matcher: Object, match: RegExpMatchArray}|null}
 */
function findCardMatch(content) {
  for (const matcher of CARD_MATCHERS) {
    const match = content.match(matcher.pattern);
    if (match) return { matcher, match };
  }
  return null;
}

/**
 * Process a card match and update state
 * @param {{matcher: Object, match: RegExpMatchArray}} result - Match result from findCardMatch
 * @param {Object} currentItem - Current composite item
 * @param {CardDef|null} currentCard - Current card being built
 * @param {Function} saveCurrentItem - Function to save current item
 * @returns {{currentItem: Object, currentCard: CardDef}}
 */
function processCardMatch(result, currentItem, currentCard, saveCurrentItem) {
  const { matcher, match } = result;

  const needsNewGroup = !currentItem ||
    currentItem.type !== 'cards' ||
    (currentItem.cards.length > 0 && matcher.shouldStartNewGroup(currentItem.cards));

  let newCurrentItem = currentItem;
  if (needsNewGroup) {
    saveCurrentItem();
    newCurrentItem = { type: 'cards', cards: [] };
  } else if (currentCard) {
    newCurrentItem = { ...currentItem, cards: [...currentItem.cards, currentCard] };
  }

  const newCard = createCard(matcher.getName(match), matcher.variant);
  if (matcher.getNumber) {
    newCard.number = matcher.getNumber(match);
  }

  return { currentItem: newCurrentItem, currentCard: newCard };
}

/**
 * Finalize a composite item and add it to the items array
 * @param {CompositeItemDef} item - The composite item to finalize
 * @param {CardDef|null} currentCard - Current card being built
 * @param {CompositeItemDef[]} items - Array to push finalized item to
 * @returns {{card: CardDef|null}} - Reset card values
 */
function finalizeCompositeItem(item, currentCard, items) {
  if (!item) return { card: currentCard };

  let card = currentCard;

  switch (item.type) {
    case 'bulletList':
      if (item.items && item.items.length > 0) {
        items.push(item);
      }
      break;
    case 'cards':
      if (currentCard) {
        item.cards.push(currentCard);
        card = null;
      }
      if (item.cards && item.cards.length > 0) {
        items.push(item);
      }
      break;
    case 'table':
      if (item.tableLines && item.tableLines.length > 0) {
        item.table = parseTable(item.tableLines);
        delete item.tableLines;
        items.push(item);
      }
      break;
    case 'flow':
      if (item.flowItems && item.flowItems.length > 0) {
        items.push(item);
      }
      break;
    case 'code':
      if (item.codeBlock) {
        items.push(item);
      }
      break;
    case 'composite':
      if (item.compositeItems && item.compositeItems.length > 0) {
        items.push(item);
      }
      break;
  }

  return { card };
}

/**
 * Parse composite layout string (e.g., "1:2", "2:1", "1:1:1")
 * @param {string} layoutStr - Layout string like "1:2" or "1:1:1"
 * @returns {CompositeLayoutDef|null}
 */
function parseCompositeLayout(layoutStr) {
  const parts = layoutStr.split(':').map(n => parseInt(n, 10));
  if (parts.some(isNaN)) return null;

  if (parts.length === 2) {
    // "1:2" → horizontal (1 row, 2 cols), "2:1" → vertical (2 rows, 1 col)
    return { rows: parts[0], cols: parts[1] };
  } else if (parts.length === 3) {
    // "1:1:1" → 3 columns
    return { rows: 1, cols: 3 };
  }
  return null;
}

/**
 * Element type declarations and their initial item creators
 * Used to reduce duplication in parseCompositeItems
 */
const ELEMENT_TYPE_CREATORS = {
  bulletList: () => ({ type: 'bulletList', items: [] }),
  code: () => ({ type: 'code', codeBlock: null }),
  table: () => ({ type: 'table', tableLines: [] }),
  flow: () => ({ type: 'flow', flowItems: [] })
};

/**
 * Check if content matches an element type declaration and return the type
 *
 * Note: Mermaid declarations are intentionally treated as 'code' type here.
 * The actual rendering method (Mermaid.js vs highlight.js) is determined
 * in templates.js based on the codeBlock.language property ('mermaid').
 * This design keeps the parser simple while allowing templates.js to handle
 * all rendering decisions.
 *
 * @param {string} content - Content to check
 * @returns {'bulletList'|'code'|'table'|'flow'|null} - Element type or null
 */
function matchElementType(content) {
  if (PATTERNS.bulletList.test(content)) return 'bulletList';
  if (PATTERNS.code.test(content)) return 'code';
  // Mermaid is treated as 'code' - templates.js checks codeBlock.language
  // to determine whether to render with Mermaid.js or highlight.js
  if (PATTERNS.mermaid.test(content)) return 'code';
  if (PATTERNS.table.test(content)) return 'table';
  if (PATTERNS.flow.test(content)) return 'flow';
  return null;
}

/**
 * Handle content at deeper levels within a composite item
 * @param {Object} currentItem - Current composite item
 * @param {Object} currentContentItem - Current content item for bullet lists
 * @param {Object} currentCard - Current card for card items
 * @param {string} content - Content to add
 * @param {number} indent - Current indentation
 * @param {number} baseIndent - Base indentation level
 * @returns {{currentContentItem: Object}} - Updated content item
 */
function handleDeepContent(currentItem, currentContentItem, currentCard, content, indent, baseIndent) {
  if (!currentItem) return { currentContentItem };

  if (currentItem.type === 'bulletList') {
    if (indent < baseIndent + 4) {
      // First level content item
      const newContentItem = { text: content, subItems: [] };
      currentItem.items.push(newContentItem);
      return { currentContentItem: newContentItem };
    } else if (currentContentItem) {
      // Sub-item
      currentContentItem.subItems.push({ text: content, subSubItems: [] });
    }
  } else if (currentItem.type === 'flow') {
    currentItem.flowItems.push(content);
  } else if (currentItem.type === 'cards' && currentCard) {
    currentCard.items.push(content);
  }

  return { currentContentItem };
}

/**
 * Parse composite items recursively
 * @param {string[]} lines - All lines from markdown
 * @param {number} startIndex - Starting line index
 * @param {number} baseIndent - Base indentation level for items
 * @param {number} depth - Current nesting depth
 * @returns {{items: CompositeItemDef[], endIndex: number}}
 */
function parseCompositeItems(lines, startIndex, baseIndent, depth = 0) {
  const items = [];
  let i = startIndex;
  let currentItem = null;
  let currentCard = null;
  let currentContentItem = null;
  let inCodeBlock = false;
  let codeBlockLang = '';
  let codeBlockLines = [];

  // Helper to save current item using shared function
  const saveCurrentItem = () => {
    const result = finalizeCompositeItem(currentItem, currentCard, items);
    currentCard = result.card;
    currentItem = null;
  };

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Check for slide header - end of composite section
    if (!inCodeBlock && PATTERNS.slideHeader.test(trimmed)) {
      break;
    }

    // Handle code blocks
    if (PATTERNS.codeBlockMarker.test(trimmed)) {
      if (!inCodeBlock) {
        inCodeBlock = true;
        codeBlockLang = trimmed.slice(3).trim() || 'plaintext';
        codeBlockLines = [];
        i++;
        continue;
      } else {
        inCodeBlock = false;
        const codeContent = codeBlockLines.join('\n');
        if (currentItem && currentItem.type === 'code') {
          // Standalone code block
          currentItem.codeBlock = {
            language: codeBlockLang,
            code: codeContent
          };
          items.push(currentItem);
          currentItem = null;
        } else if (currentItem && currentItem.type === 'cards' && currentCard) {
          // Code block inside a card - add as codeBlock property
          currentCard.codeBlock = {
            language: codeBlockLang,
            code: codeContent
          };
        }
        i++;
        continue;
      }
    }

    if (inCodeBlock) {
      codeBlockLines.push(line);
      i++;
      continue;
    }

    // Handle table rows
    if (PATTERNS.tableRow.test(trimmed)) {
      if (currentItem && currentItem.type === 'table') {
        currentItem.tableLines.push(trimmed);
      }
      i++;
      continue;
    }

    // Skip empty lines
    if (!trimmed) {
      i++;
      continue;
    }

    // Check indentation
    const indentMatch = line.match(PATTERNS.listItem);
    if (!indentMatch) {
      i++;
      continue;
    }

    const indent = indentMatch[1].length;
    const content = indentMatch[2];

    // If indent is less than baseIndent, we've exited this composite level
    if (indent < baseIndent) {
      break;
    }

    // Item at this level (baseIndent)
    if (indent >= baseIndent && indent < baseIndent + 2) {
      // Check for nested composite
      const nestedCompositeMatch = content.match(PATTERNS.composite);
      if (nestedCompositeMatch && depth < MAX_COMPOSITE_DEPTH) {
        saveCurrentItem();
        const layout = parseCompositeLayout(nestedCompositeMatch[1].trim());
        if (layout) {
          // Parse nested composite items
          const result = parseCompositeItems(lines, i + 1, baseIndent + 2, depth + 1);
          currentItem = {
            type: 'composite',
            compositeLayout: layout,
            compositeItems: result.items
          };
          items.push(currentItem);
          currentItem = null;
          i = result.endIndex;
          continue;
        }
      }

      // Check for element type declarations (bulletList, code, table, flow)
      const elementType = matchElementType(content);
      if (elementType) {
        saveCurrentItem();
        currentItem = ELEMENT_TYPE_CREATORS[elementType]();
        if (elementType === 'bulletList') currentContentItem = null;
        i++;
        continue;
      }

      // カード系パターン (card, step, good, bad) を統一的に処理
      const cardMatchResult = findCardMatch(content);
      if (cardMatchResult) {
        const result = processCardMatch(cardMatchResult, currentItem, currentCard, saveCurrentItem);
        currentItem = result.currentItem;
        currentCard = result.currentCard;
        i++;
        continue;
      }
    }

    // Content at deeper levels
    if (indent >= baseIndent + 2) {
      const deepResult = handleDeepContent(currentItem, currentContentItem, currentCard, content, indent, baseIndent);
      currentContentItem = deepResult.currentContentItem;
    }

    i++;
  }

  // Save any remaining item
  saveCurrentItem();

  return { items, endIndex: i };
}

/**
 * Parse markdown content into slide definitions (refactored version)
 * @param {string} markdown - Markdown content
 * @returns {SlideDefinition[]}
 */
function parseMarkdown(markdown) {
  const lines = markdown.split('\n');
  const chunks = splitBySlideHeaders(lines);

  return chunks.map((chunk, index) => {
    const base = parseSlideHeader(chunk.header, index);
    // Title slide is determined by header pattern (## PART N:メインタイトル)
    const type = base.partNumber !== undefined ? 'title' : detectSlideType(chunk.bodyLines);
    const metadata = parseSlideMetadata(chunk.bodyLines);
    const content = slideParsers[type]?.(chunk.bodyLines, base) ?? {};

    return { ...base, type, ...metadata, ...content };
  });
}

/**
 * Parse a table row into cells
 * @param {string} line - Table row like "| cell1 | cell2 |"
 * @returns {string[]}
 */
const parseTableRow = (line) =>
  line.split('|').slice(1, -1).map(cell => cell.trim());

/**
 * Check if line is a table separator (|---|---|)
 * @param {string} line
 * @returns {boolean}
 */
const isTableSeparator = (line) => PATTERNS.tableSeparator.test(line);

/**
 * Parse markdown table lines into structured data
 * @param {string[]} lines
 * @returns {TableDef}
 */
function parseTable(lines) {
  const dataLines = lines.filter(line => !isTableSeparator(line));
  const [headerLine, ...rowLines] = dataLines;

  return {
    headers: headerLine ? parseTableRow(headerLine) : [],
    rows: rowLines.map(parseTableRow),
  };
}

module.exports = { parseMarkdown };
