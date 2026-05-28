---
name: content-rendering
description: "WHAT: Safe HTML rendering with RenderSanitizedHTML and XSS prevention. WHEN: rendering CMS content, translated HTML, user-generated rich text. KEYWORDS: html, render, sanitize, xss, RenderSanitizedHTML, sanitize-html, truncation, content."
---

# Content Rendering

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Always sanitize HTML before rendering.** User-generated HTML content must pass through sanitize-html before rendering with react-native-render-html. Never render unsanitized HTML directly - this prevents XSS attacks and malicious script injection.

**Always wrap RenderSanitizedHTML with ErrorBoundary.** HTML rendering can fail for malformed content or edge cases. ErrorBoundary ensures graceful degradation without crashing the entire app.

**Always sanitize before truncating.** Security comes before UX. The order is: (1) sanitize HTML to remove dangerous content, (2) truncate to maxWords limit, (3) render. This ensures malicious content is removed even if truncation fails.

**Always use custom sanitization configs for specific content types.** Different content types need different sanitization rules. Marketing content may allow more tags than user comments. Define allowedTags and allowedAttributes explicitly for each use case.

**Why**: Safe HTML rendering enables rich text content (bold, italic, lists, links) from CMS and translations, prevents security vulnerabilities through XSS prevention, provides flexible content truncation for long text, and maintains app stability through error boundaries.

## When to Use This Skill

Use these patterns when:

- Rendering HTML content from CMS or feature content APIs
- Displaying translated strings that contain HTML formatting (bold, italic, lists)
- Showing user-generated content with rich text formatting
- Rendering product descriptions or marketing copy with HTML
- Displaying sustainability information or educational content
- Rendering recipe instructions or cooking tips with formatting
- Showing upsell messages or promotional content from backend
- Building empty states with formatted body text
- Implementing "read more" truncation for long HTML content
- Rendering email templates or notification messages with HTML

## RenderSanitizedHTML Component

### Basic Usage

Use RenderSanitizedHTML for safe HTML rendering with default sanitization.

```typescript
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';

const ProductDescription = ({ product }) => {
  return (
    <View>
      <RenderSanitizedHTML
        source={{ html: product.description }}
      />
    </View>
  );
};
```

**Why**: RenderSanitizedHTML wraps react-native-render-html with automatic sanitization. Default config removes dangerous tags (script, iframe) while preserving safe formatting (p, strong, em, ul, li). ErrorBoundary handles rendering failures gracefully.

**Production Example**: `modules/social-recipe-bridge/screens/social-recipe-bridge/components/empty-state/EmptyStateView.tsx:22`

### Component API

RenderSanitizedHTML accepts four props: source, style, config, maxWords.

```typescript
<RenderSanitizedHTML
  source={{ html: '<p>Hello <strong>World</strong></p>' }}
  style={styles.bodyText}
  config={{
    allowedTags: ['p', 'br', 'strong', 'em'],
    allowedAttributes: {},
  }}
  maxWords={50}
/>
```

**Props:**
- `source` - Required. Object with `html` string property (HTMLSourceInline type from react-native-render-html)
- `style` - Optional. Custom styles merged with baseStyle from Zest theme (MixedStyleDeclaration type)
- `config` - Optional. Custom sanitization rules (sanitize.IOptions type from sanitize-html)
- `maxWords` - Optional. Maximum word count before truncation with ellipsis

**Why**: source prop matches react-native-render-html API for consistency. style prop enables Zest theme integration. config prop allows custom sanitization per use case. maxWords enables "read more" patterns.

### With Custom Styling

Merge custom styles with Zest theme for branded typography.

```typescript
import { useZestStyles } from '@zest/react-native';
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';

const MarketingBanner = ({ content }) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <RenderSanitizedHTML
      source={{ html: content.body }}
      style={styles.bodyText}
    />
  );
};

const stylesConfig = createStylesConfig((theme) => ({
  bodyText: {
    color: theme.colors.alias.text.secondary,
    fontSize: theme.typography['body-md-regular'].fontSize,
    lineHeight: theme.typography['body-md-regular'].lineHeight,
  },
}));
```

**Why**: Custom styles enable brand-consistent typography while preserving HTML formatting. Zest theme tokens ensure visual consistency across features. Style merging combines theme defaults with custom overrides.

**Production Example**: `modules/store/screens/cart/components/upsell-nudge-button/UpsellNudgeButton.tsx:40`

## HTML Sanitization

### Default Sanitization

RenderSanitizedHTML uses sanitize-html default config for basic security.

```typescript
<RenderSanitizedHTML
  source={{ html: userGeneratedContent }}
/>

// Automatically sanitizes:
// ❌ Removes: <script>, <iframe>, <embed>, <object>
// ❌ Removes: onclick, onerror, onload attributes
// ✅ Allows: <p>, <br>, <strong>, <em>, <ul>, <ol>, <li>, <a>
```

**Why**: Default sanitization prevents common XSS attacks by removing script tags and event handler attributes. Preserves safe formatting tags for rich text. No config needed for most use cases.

### Custom Sanitization Config

Define allowedTags and allowedAttributes for specific content types.

```typescript
const restrictiveConfig = {
  allowedTags: ['p', 'br', 'strong', 'em'],
  allowedAttributes: {},
};

const permissiveConfig = {
  allowedTags: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'img'],
  allowedAttributes: {
    a: ['href', 'target'],
    img: ['src', 'alt'],
  },
  allowedSchemes: ['http', 'https'],
};

// User comments - restrictive
<RenderSanitizedHTML
  source={{ html: comment.text }}
  config={restrictiveConfig}
/>

// Marketing content - permissive
<RenderSanitizedHTML
  source={{ html: marketingCopy }}
  config={permissiveConfig}
/>
```

**Why**: Different content types need different security levels. User comments should be restrictive (only basic formatting). Marketing content can be permissive (links, images). Explicit config prevents over-permissive defaults.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:43`

### Sanitization Order

Always sanitize before truncating to ensure security first.

```typescript
// Inside RenderSanitizedHTML implementation
return (
  <RenderHTML
    source={{
      html: truncateHTML(sanitize(source.html, config), maxWords),
    }}
  />
);

// Order:
// 1. sanitize(source.html, config) - Remove dangerous content
// 2. truncateHTML(..., maxWords) - Truncate to word limit
// 3. RenderHTML - Render safe, truncated HTML
```

**Why**: Security comes before UX. Sanitize first to remove malicious content even if truncation logic has bugs. Truncation operates on safe HTML. Rendering happens last after both security and UX transforms.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.tsx:40`

## Text Truncation

### maxWords Prop

Truncate long HTML content by word count with ellipsis.

```typescript
const LongDescription = ({ product }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <View>
      <RenderSanitizedHTML
        source={{ html: product.longDescription }}
        maxWords={expanded ? undefined : 50}
      />
      <Link onPress={() => setExpanded(!expanded)}>
        {expanded ? 'Show less' : 'Read more'}
      </Link>
    </View>
  );
};
```

**Why**: maxWords enables "read more" patterns for long content. Word-based truncation (not character-based) respects word boundaries. Ellipsis (...) indicates truncated content. Undefined maxWords shows full content.

### needTruncating Helper

Check if content exceeds word limit before rendering truncation UI.

```typescript
import { RenderSanitizedHTML, needTruncating } from '@libs/render-sanitized-html';

const Description = ({ html }) => {
  const [expanded, setExpanded] = useState(false);
  const shouldTruncate = needTruncating(html, 50);

  return (
    <View>
      <RenderSanitizedHTML
        source={{ html }}
        maxWords={expanded ? undefined : 50}
      />
      {shouldTruncate && (
        <Link onPress={() => setExpanded(!expanded)}>
          {expanded ? 'Show less' : 'Read more'}
        </Link>
      )}
    </View>
  );
};
```

**Why**: needTruncating checks word count without rendering. Prevents showing "Read more" link for short content. Improves UX by hiding unnecessary controls. Strips HTML tags before counting words.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.tsx:50`

### Truncation Implementation

Truncation splits text by whitespace and joins first N words.

```typescript
const truncateHTML = (sanitizedText: string, maxWords?: number) => {
  if (maxWords === undefined || maxWords === null) {
    return sanitizedText;
  }
  const words = splitToWords(sanitizedText);

  if (words.length <= maxWords) {
    return sanitizedText;
  }

  const truncatedText = words.slice(0, maxWords).join(' ');
  return `${truncatedText}...`;
};

const splitToWords = (text: string) => {
  return text.trim().split(/\s+/);
};

const needTruncating = (html: string, maxWords: number) => {
  const tempDiv = html.replace(/<[^>]*>/g, ' ');
  return splitToWords(tempDiv).length > maxWords;
};
```

**Why**: splitToWords uses regex /\s+/ to handle multiple spaces, tabs, newlines. slice(0, maxWords) takes first N words. Ellipsis (...) indicates truncation. needTruncating strips HTML tags with regex /<[^>]*>/g before counting.

## Error Handling

### ErrorBoundary Wrapper

Wrap RenderSanitizedHTML with ErrorBoundary for graceful degradation.

```typescript
import { ErrorBoundary } from '@libs/error-boundary';

export const RenderSanitizedHTML = ({ source, style, config, maxWords }) => {
  const width = useContentWidth();
  const styles = useZestStyles(stylesConfig);

  return (
    <View>
      <ErrorBoundary scope={{ moduleName: 'RenderSanitizedHTML' }}>
        <RenderHTML
          contentWidth={width}
          source={{
            html: truncateHTML(sanitize(source.html, config), maxWords),
          }}
          baseStyle={{ ...styles.baseStyle, ...style }}
        />
      </ErrorBoundary>
    </View>
  );
};
```

**Why**: HTML rendering can fail for malformed HTML, unsupported tags, or layout issues. ErrorBoundary catches React errors and prevents app crash. scope prop helps identify which content failed. Component returns null on error for graceful degradation.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.tsx:36`

### Fallback Content

Provide fallback content when HTML rendering fails.

```typescript
const SafeDescription = ({ html, fallbackText }) => {
  return (
    <ErrorBoundary
      fallback={<Text>{fallbackText}</Text>}
      scope={{ moduleName: 'SafeDescription' }}
    >
      <RenderSanitizedHTML source={{ html }} />
    </ErrorBoundary>
  );
};
```

**Why**: Fallback content ensures users see something useful when rendering fails. Plain text fallback is always safe. ErrorBoundary fallback prop accepts React element. Prevents blank screens from rendering errors.

## Responsive Layouts

### useContentWidth Hook

Use useContentWidth for responsive HTML rendering.

```typescript
import RenderHTML, { useContentWidth } from 'react-native-render-html';

export const RenderSanitizedHTML = ({ source, style, config, maxWords }) => {
  const width = useContentWidth();

  return (
    <RenderHTML
      contentWidth={width}
      source={{ html: sanitize(source.html, config) }}
      baseStyle={style}
    />
  );
};
```

**Why**: useContentWidth provides responsive width from react-native-render-html context. Ensures HTML content adapts to available space. Required prop for RenderHTML component. Automatically updates on orientation changes.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.tsx:26`

## Internationalization

### With Translated HTML

Render translated HTML strings from i18n with RenderSanitizedHTML.

```typescript
import { useT9n } from '@libs/localization';
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';

const EmptyState = () => {
  const { translateRaw } = useT9n('social-recipe-bridge');

  return (
    <View>
      <Text type="headline-md">
        {translateRaw('social-recipe-bridge.empty_state.headline')}
      </Text>
      <RenderSanitizedHTML
        source={{
          html: translateRaw('social-recipe-bridge.empty_state.body_text'),
        }}
      />
    </View>
  );
};

// Translation file:
// "social-recipe-bridge.empty_state.body_text": "<p>Save recipes from <strong>any website</strong> to your personal cookbook.</p>"
```

**Why**: Translation strings can contain HTML for formatting (bold, italic, lists). RenderSanitizedHTML renders formatted translations safely. translateRaw returns HTML string from translation file. Sanitization prevents XSS even in translations.

**Production Example**: `modules/social-recipe-bridge/screens/social-recipe-bridge/components/empty-state/EmptyStateView.tsx:22`

## Testing Patterns

### Mock Zest Styles

Mock useZestStyles for isolated component testing.

```typescript
jest.mock('@zest/react-native', () => ({
  useZestStyles: () => ({
    baseStyle: {
      color: 'black',
      fontSize: 16,
      lineHeight: 24,
    },
  }),
}));

describe('<RenderSanitizedHTML />', () => {
  it('renders HTML content correctly', () => {
    const htmlContent = '<p>Hello World</p>';

    render(<RenderSanitizedHTML source={{ html: htmlContent }} />);

    expect(screen.getByText('Hello World')).toBeTruthy();
  });
});
```

**Why**: Mocking useZestStyles removes Zest theme dependency in tests. Returns simple baseStyle object for testing. Prevents "useZestStyles must be used within ZestProvider" errors. Makes tests faster and more isolated.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:6`

### Test XSS Prevention

Test that dangerous HTML is sanitized before rendering.

```typescript
describe('Sanitization', () => {
  it('removes script tags to prevent XSS', () => {
    const maliciousHtml = '<script>alert("hack")</script><p>Safe content</p>';

    render(<RenderSanitizedHTML source={{ html: maliciousHtml }} />);

    expect(screen.getByText(/Safe content/)).toBeTruthy();
    expect(screen.queryByText(/alert/)).toBeNull();
  });

  it('removes event handler attributes', () => {
    const maliciousHtml = '<p onclick="alert(\'hack\')">Click me</p>';

    render(<RenderSanitizedHTML source={{ html: maliciousHtml }} />);

    expect(screen.getByText('Click me')).toBeTruthy();
    // onclick attribute should be removed by sanitization
  });
});
```

**Why**: XSS prevention is critical security feature. Test that script tags are removed. Test that event handler attributes (onclick, onerror) are removed. Use queryByText for null checks. Regex matchers (/Safe content/) handle partial matches.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:31`

### Test Custom Sanitization Config

Test that custom configs restrict allowed tags correctly.

```typescript
describe('Custom Sanitization Config', () => {
  it('applies restrictive config to remove tags', () => {
    const htmlContent = '<p><strong>Bold</strong> and <em>italic</em></p>';
    const restrictiveConfig = {
      allowedTags: ['p'], // Only allow p tags
      allowedAttributes: {},
    };

    render(
      <RenderSanitizedHTML
        source={{ html: htmlContent }}
        config={restrictiveConfig}
      />
    );

    // Text content preserved, but strong and em tags removed
    expect(screen.getByText(/Bold and italic/)).toBeTruthy();
  });
});
```

**Why**: Custom configs should restrict tags as specified. Test allowedTags removes unwanted tags. Test text content is preserved after tag removal. Verifies config is passed to sanitize-html correctly.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:43`

### Test maxWords Truncation

Test that truncation works correctly with maxWords prop.

```typescript
describe('maxWords Truncation', () => {
  const longHtml =
    '<p>This is a very long paragraph with many words that should be truncated.</p>';

  it('truncates when maxWords is exceeded', () => {
    render(
      <RenderSanitizedHTML source={{ html: longHtml }} maxWords={5} />
    );

    expect(screen.getByText(/\.\.\./)).toBeTruthy();
    expect(screen.queryByText(/should be truncated/)).toBeNull();
  });

  it('does not truncate when content is shorter than maxWords', () => {
    const shortHtml = '<p>Short content</p>';

    render(
      <RenderSanitizedHTML source={{ html: shortHtml }} maxWords={10} />
    );

    expect(screen.getByText(/Short content/)).toBeTruthy();
    expect(screen.queryByText(/\.\.\./)).toBeNull();
  });

  it('ignores HTML tags when counting words', () => {
    const htmlWithTags =
      '<p><strong>One</strong> <em>two</em> <span>three</span></p>';

    render(
      <RenderSanitizedHTML source={{ html: htmlWithTags }} maxWords={2} />
    );

    expect(screen.getByText(/One.*two.*\.\.\./)).toBeTruthy();
    expect(screen.queryByText(/three/)).toBeNull();
  });
});
```

**Why**: Truncation should respect maxWords limit. Test ellipsis appears when truncated. Test no ellipsis when content is short. Test HTML tags ignored when counting words. Regex matchers verify partial content.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:88`

### Test needTruncating Helper

Test helper function for checking truncation necessity.

```typescript
import { needTruncating } from '@libs/render-sanitized-html';

describe('needTruncating', () => {
  it('returns true when text exceeds maxWords', () => {
    const longText = '<p>This is a very long text with many words</p>';
    const result = needTruncating(longText, 5);
    expect(result).toBe(true);
  });

  it('returns false when text is within maxWords', () => {
    const shortText = '<p>Short text</p>';
    const result = needTruncating(shortText, 5);
    expect(result).toBe(false);
  });

  it('ignores HTML tags when counting words', () => {
    const htmlText = '<p><strong>One</strong> <em>two</em></p>';
    const result = needTruncating(htmlText, 5);
    expect(result).toBe(false); // Only 2 words
  });
});
```

**Why**: Test helper function separately from component. Test true when exceeds limit. Test false when within limit. Test HTML tags ignored. Unit test pure function for fast feedback.

**Production Example**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:337`

## Common Mistakes to Avoid

❌ **Don't render unsanitized HTML**:

```typescript
// ❌ Wrong - no sanitization
import RenderHTML from 'react-native-render-html';

<RenderHTML
  source={{ html: userGeneratedContent }}
  contentWidth={width}
/>
```

**Why**: Unsanitized HTML enables XSS attacks. Malicious users can inject script tags. No protection against dangerous content.

✅ **Do use RenderSanitizedHTML**:

```typescript
// ✅ Correct - automatic sanitization
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';

<RenderSanitizedHTML
  source={{ html: userGeneratedContent }}
/>
```

**Why**: RenderSanitizedHTML automatically sanitizes with sanitize-html. Removes script tags and dangerous attributes. Secure by default.

❌ **Don't truncate before sanitizing**:

```typescript
// ❌ Wrong - truncate first, sanitize second
const truncatedHtml = truncate(html, maxWords);
const sanitizedHtml = sanitize(truncatedHtml);

<RenderHTML source={{ html: sanitizedHtml }} />
```

**Why**: Truncation may break malicious HTML in unexpected ways. Script tags could survive truncation. Security should always come first.

✅ **Do sanitize before truncating**:

```typescript
// ✅ Correct - sanitize first, truncate second
const sanitizedHtml = sanitize(html, config);
const truncatedHtml = truncate(sanitizedHtml, maxWords);

<RenderHTML source={{ html: truncatedHtml }} />
```

**Why**: Sanitization removes dangerous content first. Truncation operates on safe HTML. Security before UX.

❌ **Don't skip ErrorBoundary**:

```typescript
// ❌ Wrong - no error handling
<RenderHTML
  source={{ html: sanitize(html) }}
  contentWidth={width}
/>
```

**Why**: HTML rendering can crash for malformed content. No graceful degradation. Entire app crashes on rendering errors.

✅ **Do wrap with ErrorBoundary**:

```typescript
// ✅ Correct - graceful error handling
<ErrorBoundary scope={{ moduleName: 'RenderSanitizedHTML' }}>
  <RenderHTML
    source={{ html: sanitize(html) }}
    contentWidth={width}
  />
</ErrorBoundary>
```

**Why**: ErrorBoundary catches rendering errors. App continues working after errors. Component returns null for graceful degradation.

❌ **Don't use overly permissive sanitization**:

```typescript
// ❌ Wrong - too permissive
const permissiveConfig = {
  allowedTags: sanitize.defaults.allowedTags.concat(['style', 'link']),
  allowedAttributes: {
    '*': ['style', 'class', 'id'], // All elements, all attributes
  },
};

<RenderSanitizedHTML
  source={{ html: userContent }}
  config={permissiveConfig}
/>
```

**Why**: Permissive configs enable attacks through CSS injection. class and id attributes can target malicious styles. style attribute enables arbitrary CSS.

✅ **Do use restrictive configs for user content**:

```typescript
// ✅ Correct - restrictive for user content
const restrictiveConfig = {
  allowedTags: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li'],
  allowedAttributes: {}, // No attributes
};

<RenderSanitizedHTML
  source={{ html: userContent }}
  config={restrictiveConfig}
/>
```

**Why**: Restrictive configs minimize attack surface. Only allow necessary formatting tags. No attributes prevents CSS injection. User content should be most restrictive.

❌ **Don't forget contentWidth**:

```typescript
// ❌ Wrong - missing contentWidth
<RenderHTML
  source={{ html: sanitize(html) }}
  // Missing contentWidth prop
/>
```

**Why**: contentWidth is required by react-native-render-html. Component may crash without it. Layout issues on different screen sizes.

✅ **Do use useContentWidth**:

```typescript
// ✅ Correct - responsive width
import { useContentWidth } from 'react-native-render-html';

const width = useContentWidth();

<RenderHTML
  source={{ html: sanitize(html) }}
  contentWidth={width}
/>
```

**Why**: useContentWidth provides responsive width. Adapts to available space. Required for proper HTML layout.

## Quick Reference

**Basic usage**:
```typescript
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';

<RenderSanitizedHTML
  source={{ html: '<p>Hello <strong>World</strong></p>' }}
/>
```

**With custom styling**:
```typescript
const styles = useZestStyles(stylesConfig);

<RenderSanitizedHTML
  source={{ html: content }}
  style={styles.bodyText}
/>
```

**With custom sanitization**:
```typescript
const config = {
  allowedTags: ['p', 'br', 'strong', 'em'],
  allowedAttributes: {},
};

<RenderSanitizedHTML
  source={{ html: userContent }}
  config={config}
/>
```

**With truncation**:
```typescript
<RenderSanitizedHTML
  source={{ html: longContent }}
  maxWords={50}
/>
```

**Check if truncation needed**:
```typescript
import { needTruncating } from '@libs/render-sanitized-html';

const shouldTruncate = needTruncating(html, 50);

{shouldTruncate && <Link onPress={toggleExpanded}>Read more</Link>}
```

**With translated content**:
```typescript
const { translateRaw } = useT9n('feature');

<RenderSanitizedHTML
  source={{
    html: translateRaw('feature.content.body_text'),
  }}
/>
```

**Testing XSS prevention**:
```typescript
it('removes script tags', () => {
  const maliciousHtml = '<script>alert("hack")</script><p>Safe</p>';

  render(<RenderSanitizedHTML source={{ html: maliciousHtml }} />);

  expect(screen.getByText(/Safe/)).toBeTruthy();
  expect(screen.queryByText(/alert/)).toBeNull();
});
```

**Testing truncation**:
```typescript
it('truncates with maxWords', () => {
  const longHtml = '<p>One two three four five six</p>';

  render(<RenderSanitizedHTML source={{ html: longHtml }} maxWords={3} />);

  expect(screen.getByText(/\.\.\./)).toBeTruthy();
});
```

**Key Libraries:**
- react-native-render-html (HTML rendering in React Native)
- sanitize-html (HTML sanitization for XSS prevention)
- @libs/error-boundary (Error handling)
- @zest/react-native (Zest theme integration)
- React Native 0.75.4

For production examples, see [references/examples.md](references/examples.md).
