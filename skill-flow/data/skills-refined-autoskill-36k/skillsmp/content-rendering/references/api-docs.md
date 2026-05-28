# react-native-render-html + sanitize-html API Reference

**Versions**: react-native-render-html 6.3.4, sanitize-html 2.17.0

## Official Documentation

- **render-html**: https://meliorence.github.io/react-native-render-html/
- **sanitize-html**: https://github.com/apostrophecms/sanitize-html

## react-native-render-html

### RenderHTML

Render HTML content in React Native.

```typescript
import RenderHTML from 'react-native-render-html';

<RenderHTML
  contentWidth={width}
  source={{ html: '<p>Hello <strong>World</strong></p>' }}
  baseStyle={{
    color: 'black',
    fontSize: 16,
  }}
  tagsStyles={{
    p: { marginBottom: 10 },
    strong: { fontWeight: 'bold' },
  }}
  classesStyles={{
    'my-class': { color: 'blue' },
  }}
  enableExperimentalMarginCollapsing={true}
  renderersProps={{
    a: {
      onPress: (event, href) => {
        Linking.openURL(href);
      },
    },
  }}
/>
```

**Props**:
- `contentWidth` - Required. Width for layout (number)
- `source` - HTML source object: `{ html: string }`
- `baseStyle` - Base text styles
- `tagsStyles` - Styles per HTML tag
- `classesStyles` - Styles per CSS class
- `enableExperimentalMarginCollapsing` - Better spacing
- `renderersProps` - Props for custom renderers
- `systemFonts` - Custom font families

### useContentWidth

Get responsive content width.

```typescript
import { useContentWidth } from 'react-native-render-html';

const width = useContentWidth();

<RenderHTML contentWidth={width} source={{ html }} />
```

### Custom Renderers

```typescript
const renderers = {
  img: ({ TDefaultRenderer, ...props }) => {
    return (
      <View>
        <TDefaultRenderer {...props} />
        <Text>Image caption</Text>
      </View>
    );
  },
};

<RenderHTML
  contentWidth={width}
  source={{ html }}
  renderers={renderers}
/>
```

### Ignored Tags

```typescript
<RenderHTML
  contentWidth={width}
  source={{ html }}
  ignoredDomTags={['script', 'style', 'iframe']}
/>
```

## sanitize-html

### sanitize()

Sanitize HTML to remove dangerous content.

```typescript
import sanitize from 'sanitize-html';

const clean = sanitize(dirty, {
  allowedTags: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a'],
  allowedAttributes: {
    a: ['href', 'target'],
  },
  allowedSchemes: ['http', 'https', 'mailto'],
});
```

### Default Configuration

```typescript
// Default allowed tags
sanitize.defaults.allowedTags = [
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
  'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'abbr', 'code', 'hr', 'br',
  'div', 'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe'
];

// Default allowed attributes
sanitize.defaults.allowedAttributes = {
  a: ['href', 'name', 'target'],
  img: ['src', 'srcset', 'alt', 'title', 'width', 'height', 'loading']
};
```

### Options

```typescript
interface IOptions {
  allowedTags?: string[];
  disallowedTagsMode?: 'discard' | 'escape' | 'recursiveEscape';
  allowedAttributes?: { [tag: string]: string[] } | false;
  selfClosing?: string[];
  allowedSchemes?: string[];
  allowedSchemesByTag?: { [tag: string]: string[] };
  allowedSchemesAppliedToAttributes?: string[];
  allowProtocolRelative?: boolean;
  enforceHtmlBoundary?: boolean;
  parseStyleAttributes?: boolean;
}
```

### Restrictive Config

```typescript
const restrictiveConfig = {
  allowedTags: ['p', 'br', 'strong', 'em'],
  allowedAttributes: {}, // No attributes
  allowedSchemes: [],
};

const clean = sanitize(userContent, restrictiveConfig);
```

### Permissive Config

```typescript
const permissiveConfig = {
  allowedTags: sanitize.defaults.allowedTags.concat(['img', 'video']),
  allowedAttributes: {
    ...sanitize.defaults.allowedAttributes,
    img: ['src', 'alt', 'width', 'height'],
    a: ['href', 'target', 'rel'],
  },
  allowedSchemes: ['http', 'https', 'mailto', 'tel'],
};

const clean = sanitize(cmsContent, permissiveConfig);
```

### Custom Transformations

```typescript
const clean = sanitize(html, {
  allowedTags: ['p', 'a'],
  transformTags: {
    'a': (tagName, attribs) => ({
      tagName: 'a',
      attribs: {
        ...attribs,
        target: '_blank',
        rel: 'noopener noreferrer',
      },
    }),
  },
});
```

### Disallowed Tag Modes

```typescript
// Remove tags and content
sanitize(html, {
  disallowedTagsMode: 'discard',
});

// Escape tags
sanitize(html, {
  disallowedTagsMode: 'escape', // <script> becomes &lt;script&gt;
});

// Recursively escape
sanitize(html, {
  disallowedTagsMode: 'recursiveEscape',
});
```

## Combined Usage Pattern

### Safe HTML Rendering Component

```typescript
import RenderHTML, { useContentWidth } from 'react-native-render-html';
import sanitize from 'sanitize-html';

export const RenderSanitizedHTML = ({
  source,
  style,
  config,
  maxWords
}) => {
  const width = useContentWidth();

  const sanitizedHtml = sanitize(source.html, config || {
    allowedTags: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a'],
    allowedAttributes: {
      a: ['href'],
    },
    allowedSchemes: ['http', 'https'],
  });

  const truncated = maxWords
    ? truncateHTML(sanitizedHtml, maxWords)
    : sanitizedHtml;

  return (
    <RenderHTML
      contentWidth={width}
      source={{ html: truncated }}
      baseStyle={style}
      enableExperimentalMarginCollapsing={true}
    />
  );
};
```

### Security Patterns

```typescript
// User-generated content (most restrictive)
const userContentConfig = {
  allowedTags: ['p', 'br', 'strong', 'em'],
  allowedAttributes: {},
  allowedSchemes: [],
};

// CMS content (moderate)
const cmsContentConfig = {
  allowedTags: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'h1', 'h2'],
  allowedAttributes: {
    a: ['href', 'target'],
  },
  allowedSchemes: ['http', 'https', 'mailto'],
};

// Marketing content (permissive)
const marketingConfig = {
  allowedTags: sanitize.defaults.allowedTags.concat(['img']),
  allowedAttributes: {
    ...sanitize.defaults.allowedAttributes,
    img: ['src', 'alt', 'width', 'height'],
  },
  allowedSchemes: ['http', 'https'],
};
```

## XSS Prevention

### Dangerous Patterns to Block

```typescript
// Block script tags
sanitize('<script>alert("xss")</script><p>Safe</p>');
// Result: '<p>Safe</p>'

// Block event handlers
sanitize('<p onclick="alert(\'xss\')">Click</p>');
// Result: '<p>Click</p>'

// Block javascript: protocol
sanitize('<a href="javascript:alert(\'xss\')">Link</a>');
// Result: '<a>Link</a>'

// Block data: URLs (optional)
sanitize('<img src="data:text/html,<script>alert(\'xss\')</script>">');
// Configure allowedSchemes without 'data'
```

### Safe Defaults

```typescript
const safeConfig = {
  allowedTags: ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li'],
  allowedAttributes: {}, // No attributes = no XSS vectors
  allowedSchemes: [], // No schemes = no javascript: or data:
  allowProtocolRelative: false, // No // urls
};
```

## Text Truncation

### Word-Based Truncation

```typescript
const truncateHTML = (html: string, maxWords: number): string => {
  const words = html
    .replace(/<[^>]*>/g, ' ') // Strip tags
    .trim()
    .split(/\s+/);

  if (words.length <= maxWords) {
    return html;
  }

  return words.slice(0, maxWords).join(' ') + '...';
};

const needsTruncation = (html: string, maxWords: number): boolean => {
  const words = html
    .replace(/<[^>]*>/g, ' ')
    .trim()
    .split(/\s+/);

  return words.length > maxWords;
};
```

## Testing

### Mock Sanitization

```typescript
jest.mock('sanitize-html', () => jest.fn((html) => html));

// Or partial mock
jest.mock('sanitize-html', () => ({
  __esModule: true,
  default: jest.fn((html) => html.replace(/<script.*?<\/script>/g, '')),
}));
```

### Test XSS Prevention

```typescript
it('removes script tags', () => {
  const malicious = '<script>alert("xss")</script><p>Safe</p>';
  const clean = sanitize(malicious, config);

  expect(clean).not.toContain('<script');
  expect(clean).toContain('<p>Safe</p>');
});

it('removes event handlers', () => {
  const malicious = '<p onclick="alert(\'xss\')">Text</p>';
  const clean = sanitize(malicious, {
    allowedTags: ['p'],
    allowedAttributes: {},
  });

  expect(clean).toBe('<p>Text</p>');
});
```

## Key Considerations

- Always sanitize before rendering HTML
- Use `contentWidth` from `useContentWidth()` for responsive layouts
- Configure `allowedTags` based on content source (user vs CMS)
- Never allow `onclick`, `onerror`, `onload` attributes
- Block `javascript:` and `data:` URL schemes for user content
- Use `ErrorBoundary` wrapper for graceful failures
- Test XSS prevention with malicious inputs
- Sanitize before truncating (security first)
- Limit `allowedAttributes` for user-generated content
- Use `disallowedTagsMode: 'discard'` to remove dangerous tags
