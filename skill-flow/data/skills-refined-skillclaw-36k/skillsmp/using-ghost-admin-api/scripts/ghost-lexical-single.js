/**
 * Ghost Lexical Builder - Complete Single File
 * A fluent API for building Ghost Lexical JSON content
 * 
 * Usage:
 *   const { LexicalBuilder, text } = require('./ghost-lexical');
 *   
 *   const content = new LexicalBuilder()
 *     .h1('Title')
 *     .paragraph('Some text with ', text.bold('bold'), ' and ', text.italic('italic'))
 *     .build();
 */

// ============================================================================
// FORMAT CONSTANTS
// ============================================================================

const FORMAT = {
  NORMAL: 0,
  ITALIC: 1,
  BOLD: 2,
  BOLD_ITALIC: 3,
  UNDERLINE: 4,
  STRIKETHROUGH: 8,
  CODE: 16,
  BOLD_CODE: 18,
};

function combineFormats(...flags) {
  return flags.reduce((acc, flag) => acc | flag, 0);
}

// ============================================================================
// TEXT NODE
// ============================================================================

class TextNode {
  constructor(text, format = FORMAT.NORMAL) {
    this.text = text;
    this.format = format;
  }

  build() {
    return {
      type: 'extended-text',
      text: this.text,
      format: this.format,
      detail: 0,
      mode: 'normal',
      style: '',
      version: 1,
    };
  }

  static normal(text) {
    return new TextNode(text, FORMAT.NORMAL);
  }

  static bold(text) {
    return new TextNode(text, FORMAT.BOLD);
  }

  static italic(text) {
    return new TextNode(text, FORMAT.ITALIC);
  }

  static boldItalic(text) {
    return new TextNode(text, FORMAT.BOLD_ITALIC);
  }

  static code(text) {
    return new TextNode(text, FORMAT.CODE);
  }

  static underline(text) {
    return new TextNode(text, FORMAT.UNDERLINE);
  }

  static strikethrough(text) {
    return new TextNode(text, FORMAT.STRIKETHROUGH);
  }
}

// ============================================================================
// LINK
// ============================================================================

class Link {
  constructor(url, children = [], options = {}) {
    this.url = url;
    this.children = children;
    this.rel = options.rel || null;
    this.target = options.target || null;
    this.title = options.title || null;
  }

  build() {
    const childrenNodes = this.children.map((child) => {
      if (typeof child === 'string') {
        return TextNode.normal(child).build();
      }
      if (child instanceof TextNode) {
        return child.build();
      }
      return child;
    });

    return {
      type: 'link',
      url: this.url,
      children: childrenNodes,
      direction: 'ltr',
      format: '',
      indent: childrenNodes.length > 0 ? 0 : undefined,
      version: 1,
      rel: this.rel,
      target: this.target,
      title: this.title,
    };
  }

  static bare(url, options = {}) {
    return new Link(url, [], options);
  }

  static withText(url, text, options = {}) {
    const children = Array.isArray(text) ? text : [text];
    return new Link(url, children, options);
  }
}

// ============================================================================
// PARAGRAPH
// ============================================================================

class Paragraph {
  constructor(content = []) {
    this.content = Array.isArray(content) ? content : [content];
  }

  add(...items) {
    this.content.push(...items);
    return this;
  }

  build() {
    const children = this.content.map((item) => {
      if (typeof item === 'string') {
        return TextNode.normal(item).build();
      }
      if (item instanceof TextNode || item instanceof Link) {
        return item.build();
      }
      return item;
    });

    return {
      type: 'paragraph',
      children,
      direction: 'ltr',
      format: '',
      indent: 0,
      version: 1,
    };
  }

  static simple(text) {
    return new Paragraph([text]);
  }

  static create(...items) {
    return new Paragraph(items);
  }
}

// ============================================================================
// HEADING
// ============================================================================

class Heading {
  constructor(level, content = []) {
    if (level < 1 || level > 6) {
      throw new Error('Heading level must be between 1 and 6');
    }
    this.level = level;
    this.content = Array.isArray(content) ? content : [content];
  }

  build() {
    const children = this.content.map((item) => {
      if (typeof item === 'string') {
        return TextNode.normal(item).build();
      }
      if (item instanceof TextNode) {
        return item.build();
      }
      return item;
    });

    return {
      type: 'extended-heading',
      tag: `h${this.level}`,
      children,
      direction: 'ltr',
      format: '',
      indent: 0,
      version: 1,
    };
  }

  static h1(content) {
    return new Heading(1, content);
  }

  static h2(content) {
    return new Heading(2, content);
  }

  static h3(content) {
    return new Heading(3, content);
  }

  static h4(content) {
    return new Heading(4, content);
  }

  static h5(content) {
    return new Heading(5, content);
  }

  static h6(content) {
    return new Heading(6, content);
  }
}

// ============================================================================
// LIST
// ============================================================================

class ListItem {
  constructor(content, value = 1) {
    this.content = Array.isArray(content) ? content : [content];
    this.value = value;
  }

  build() {
    const children = this.content.map((item) => {
      if (typeof item === 'string') {
        return TextNode.normal(item).build();
      }
      if (item instanceof TextNode || item instanceof Link) {
        return item.build();
      }
      return item;
    });

    return {
      type: 'listitem',
      value: this.value,
      children,
      direction: 'ltr',
      format: '',
      indent: 0,
      version: 1,
    };
  }
}

class List {
  constructor(type = 'bullet', items = []) {
    if (!['bullet', 'number'].includes(type)) {
      throw new Error('List type must be "bullet" or "number"');
    }
    this.listType = type;
    this.items = items;
  }

  addItem(item) {
    this.items.push(item);
    return this;
  }

  build() {
    const children = this.items.map((item, index) => {
      if (item instanceof ListItem) {
        return item.build();
      }
      const listItem = new ListItem(item, index + 1);
      return listItem.build();
    });

    return {
      type: 'list',
      listType: this.listType,
      start: 1,
      tag: this.listType === 'bullet' ? 'ul' : 'ol',
      children,
      direction: 'ltr',
      format: '',
      indent: 0,
      version: 1,
    };
  }

  static bullet(items) {
    return new List('bullet', items);
  }

  static numbered(items) {
    return new List('number', items);
  }
}

// ============================================================================
// IMAGE
// ============================================================================

class Image {
  constructor(src, options = {}) {
    this.src = src;
    this.alt = options.alt || '';
    this.title = options.title || '';
    this.caption = options.caption || '';
    this.width = options.width;
    this.height = options.height;
    this.href = options.href || null;
    this.cardWidth = options.cardWidth || 'regular';
  }

  build() {
    const node = {
      type: 'image',
      version: 1,
      src: this.src,
      alt: this.alt,
      title: this.title,
      caption: this.caption,
      cardWidth: this.cardWidth,
      href: this.href,
    };

    if (this.width) node.width = this.width;
    if (this.height) node.height = this.height;

    return node;
  }

  static simple(src, alt = '') {
    return new Image(src, { alt });
  }

  static withDimensions(src, width, height, options = {}) {
    return new Image(src, { ...options, width, height });
  }

  static withCaption(src, caption, options = {}) {
    return new Image(src, { ...options, caption });
  }

  setCardWidth(width) {
    this.cardWidth = width;
    return this;
  }
}

// ============================================================================
// CODE BLOCK
// ============================================================================

class CodeBlock {
  constructor(code, language = '', caption = '') {
    this.code = code;
    this.language = language;
    this.caption = caption;
  }

  build() {
    return {
      type: 'codeblock',
      version: 1,
      code: this.code,
      language: this.language,
      caption: this.caption,
    };
  }

  setLanguage(language) {
    this.language = language;
    return this;
  }

  setCaption(caption) {
    this.caption = caption;
    return this;
  }

  static create(code, language = '') {
    return new CodeBlock(code, language);
  }

  static javascript(code) {
    return new CodeBlock(code, 'javascript');
  }

  static python(code) {
    return new CodeBlock(code, 'python');
  }

  static typescript(code) {
    return new CodeBlock(code, 'typescript');
  }

  static html(code) {
    return new CodeBlock(code, 'html');
  }

  static css(code) {
    return new CodeBlock(code, 'css');
  }

  static json(code) {
    return new CodeBlock(code, 'json');
  }

  static bash(code) {
    return new CodeBlock(code, 'bash');
  }
}

// ============================================================================
// BOOKMARK
// ============================================================================

class Bookmark {
  constructor(url, options = {}) {
    this.url = url;
    this.metadata = options.metadata || {};
    this.caption = options.caption || '';
  }

  setMetadata(metadata) {
    this.metadata = { ...this.metadata, ...metadata };
    return this;
  }

  setCaption(caption) {
    this.caption = caption;
    return this;
  }

  build() {
    return {
      type: 'bookmark',
      version: 1,
      url: this.url,
      metadata: {
        url: this.url,
        title: this.metadata.title || null,
        description: this.metadata.description || null,
        author: this.metadata.author || null,
        publisher: this.metadata.publisher || null,
        thumbnail: this.metadata.thumbnail || null,
        icon: this.metadata.icon || null,
      },
      caption: this.caption,
    };
  }

  static simple(url) {
    return new Bookmark(url);
  }

  static withMetadata(url, metadata) {
    return new Bookmark(url, { metadata });
  }
}

// ============================================================================
// SIGNUP CARD
// ============================================================================

class Signup {
  constructor(options = {}) {
    this.header = options.header || '';
    this.subheader = options.subheader || '';
    this.buttonText = options.buttonText || 'Subscribe';
    this.disclaimer = options.disclaimer || '';
    this.successMessage =
      options.successMessage ||
      'Email sent! Check your inbox to complete your signup.';
    this.alignment = options.alignment || 'left';
    this.layout = options.layout || 'wide';
    this.backgroundColor = options.backgroundColor || '#F0F0F0';
    this.backgroundImageSrc = options.backgroundImageSrc || '';
    this.backgroundSize = options.backgroundSize || 'cover';
    this.textColor = options.textColor || '#000000';
    this.buttonColor = options.buttonColor || 'accent';
    this.buttonTextColor = options.buttonTextColor || '#FFFFFF';
    this.labels = options.labels || [];
    this.swapped = options.swapped || false;
  }

  build() {
    const wrapText = (text) => {
      if (!text) return text;
      if (text.startsWith('<')) return text;
      return `<span style="white-space: pre-wrap;">${text}</span>`;
    };

    return {
      type: 'signup',
      version: 1,
      alignment: this.alignment,
      backgroundColor: this.backgroundColor,
      backgroundImageSrc: this.backgroundImageSrc,
      backgroundSize: this.backgroundSize,
      textColor: this.textColor,
      buttonColor: this.buttonColor,
      buttonTextColor: this.buttonTextColor,
      buttonText: this.buttonText,
      disclaimer: wrapText(this.disclaimer),
      header: wrapText(this.header),
      labels: this.labels,
      layout: this.layout,
      subheader: wrapText(this.subheader),
      successMessage: this.successMessage,
      swapped: this.swapped,
    };
  }

  setHeader(header) {
    this.header = header;
    return this;
  }

  setSubheader(subheader) {
    this.subheader = subheader;
    return this;
  }

  setButtonText(buttonText) {
    this.buttonText = buttonText;
    return this;
  }

  setDisclaimer(disclaimer) {
    this.disclaimer = disclaimer;
    return this;
  }

  setBackgroundColor(color) {
    this.backgroundColor = color;
    return this;
  }

  setLayout(layout) {
    if (!['wide', 'full'].includes(layout)) {
      throw new Error('Layout must be "wide" or "full"');
    }
    this.layout = layout;
    return this;
  }

  setAlignment(alignment) {
    if (!['left', 'center', 'right'].includes(alignment)) {
      throw new Error('Alignment must be "left", "center", or "right"');
    }
    this.alignment = alignment;
    return this;
  }

  static simple(header, subheader = '') {
    return new Signup({ header, subheader });
  }

  static create(options) {
    return new Signup(options);
  }
}

// ============================================================================
// TOGGLE
// ============================================================================

class Toggle {
  constructor(heading, content = '') {
    this.heading = heading;
    this.content = content;
  }

  setHeading(heading) {
    this.heading = heading;
    return this;
  }

  setContent(content) {
    this.content = content;
    return this;
  }

  build() {
    const wrapText = (text) => {
      if (!text) return text;
      if (text.startsWith('<')) return text;
      return `<span style="white-space: pre-wrap;">${text}</span>`;
    };

    return {
      type: 'toggle',
      version: 1,
      heading: wrapText(this.heading),
      content: this.content,
    };
  }

  static create(heading, content = '') {
    return new Toggle(heading, content);
  }

  static tableOfContents(items) {
    const listItems = items
      .map(
        (item, index) =>
          `<li value="${index + 1}"><a href="${item.href}" rel="noreferrer"><span style="white-space: pre-wrap;">${item.text}</span></a></li>`
      )
      .join('');

    const content = `<ol>${listItems}</ol>`;
    return new Toggle('Table of Contents', content);
  }

  static faq(question, answer) {
    return new Toggle(question, answer);
  }
}

// ============================================================================
// LINE BREAK
// ============================================================================

class LineBreak {
  build() {
    return {
      type: 'linebreak',
      version: 1,
    };
  }

  static create() {
    return new LineBreak();
  }
}

// ============================================================================
// LEXICAL BUILDER (Main Class)
// ============================================================================

class LexicalBuilder {
  constructor() {
    this.nodes = [];
  }

  addNode(node) {
    this.nodes.push(node);
    return this;
  }

  paragraph(...content) {
    this.nodes.push(Paragraph.create(...content));
    return this;
  }

  heading(level, content) {
    this.nodes.push(new Heading(level, content));
    return this;
  }

  h1(content) {
    return this.heading(1, content);
  }

  h2(content) {
    return this.heading(2, content);
  }

  h3(content) {
    return this.heading(3, content);
  }

  h4(content) {
    return this.heading(4, content);
  }

  h5(content) {
    return this.heading(5, content);
  }

  h6(content) {
    return this.heading(6, content);
  }

  bulletList(items) {
    this.nodes.push(List.bullet(items));
    return this;
  }

  numberedList(items) {
    this.nodes.push(List.numbered(items));
    return this;
  }

  image(src, options = {}) {
    this.nodes.push(new Image(src, options));
    return this;
  }

  codeBlock(code, language = '', caption = '') {
    this.nodes.push(new CodeBlock(code, language, caption));
    return this;
  }

  bookmark(url, options = {}) {
    this.nodes.push(new Bookmark(url, options));
    return this;
  }

  signupCard(options = {}) {
    this.nodes.push(new Signup(options));
    return this;
  }

  toggle(heading, content = '') {
    this.nodes.push(new Toggle(heading, content));
    return this;
  }

  lineBreak() {
    this.nodes.push(new LineBreak());
    return this;
  }

  hr() {
    return this.lineBreak();
  }

  build() {
    const children = this.nodes.map((node) => {
      if (typeof node.build === 'function') {
        return node.build();
      }
      return node;
    });

    return {
      root: {
        children,
        direction: 'ltr',
        format: '',
        indent: 0,
        type: 'root',
        version: 1,
      },
    };
  }

  toJSON() {
    return JSON.stringify(this.build());
  }

  toPost(metadata = {}) {
    return {
      posts: [
        {
          title: metadata.title,
          slug: metadata.slug,
          lexical: this.toJSON(),
          status: metadata.status || 'draft',
          visibility: metadata.visibility || 'public',
          featured: metadata.featured || false,
          custom_excerpt: metadata.custom_excerpt,
          feature_image: metadata.feature_image,
          feature_image_caption: metadata.feature_image_caption,
          tags: metadata.tags,
          authors: metadata.authors,
          published_at: metadata.published_at,
          updated_at: metadata.updated_at,
        },
      ],
    };
  }
}

// ============================================================================
// TEXT HELPERS
// ============================================================================

const text = {
  normal: (content) => TextNode.normal(content),
  bold: (content) => TextNode.bold(content),
  italic: (content) => TextNode.italic(content),
  boldItalic: (content) => TextNode.boldItalic(content),
  code: (content) => TextNode.code(content),
  underline: (content) => TextNode.underline(content),
  strikethrough: (content) => TextNode.strikethrough(content),
};

// ============================================================================
// GITHUB FOOTER HELPER
// ============================================================================

/**
 * Adds GitHub repository footer to post content
 * @param {LexicalBuilder} builder - LexicalBuilder instance
 * @param {string} folderName - Post folder name (e.g., "prompt-engineering-wrong")
 * @returns {LexicalBuilder} Builder with footer appended
 */
function addGitHubFooter(builder, folderName) {
  if (!folderName) return builder;

  const githubUrl = `https://github.com/houfu/blog-alt-counsel/tree/main/posts/${folderName}`;

  return builder
    .hr()  // Visual separator (creates LineBreak card, not markdown ---)
    .h3('Behind the Scenes')
    .paragraph('See how this post evolved from initial pitch to final draft. Includes research sources, iterations, and decisions along the way.')
    .bookmark(githubUrl, {
      metadata: {
        title: `${folderName} - blog-alt-counsel`,
        description: 'Source files and research notes for this blog post',
        publisher: 'GitHub',
        icon: 'https://github.githubassets.com/favicons/favicon.svg'
      }
    });
}

// ============================================================================
// EXPORTS
// ============================================================================

// Add static properties to LexicalBuilder
LexicalBuilder.Paragraph = Paragraph;
LexicalBuilder.Heading = Heading;
LexicalBuilder.List = List;
LexicalBuilder.ListItem = ListItem;
LexicalBuilder.Image = Image;
LexicalBuilder.CodeBlock = CodeBlock;
LexicalBuilder.Bookmark = Bookmark;
LexicalBuilder.Signup = Signup;
LexicalBuilder.Toggle = Toggle;
LexicalBuilder.LineBreak = LineBreak;
LexicalBuilder.Link = Link;
LexicalBuilder.TextNode = TextNode;
LexicalBuilder.text = text;
LexicalBuilder.FORMAT = FORMAT;

// Module exports
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    LexicalBuilder,
    text,
    FORMAT,
    combineFormats,
    addGitHubFooter,
    // Export all classes for advanced usage
    TextNode,
    Link,
    Paragraph,
    Heading,
    List,
    ListItem,
    Image,
    CodeBlock,
    Bookmark,
    Signup,
    Toggle,
    LineBreak,
  };
}
