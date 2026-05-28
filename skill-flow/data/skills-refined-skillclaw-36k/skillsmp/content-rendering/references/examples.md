# Content Rendering - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating safe HTML content rendering with RenderSanitizedHTML component.

## Example 1: RenderSanitizedHTML Implementation

**File**: `libs/render-sanitized-html/RenderSanitizedHTML.tsx:1`

This example shows the complete implementation of RenderSanitizedHTML component with sanitization and truncation.

```typescript
import { View } from 'react-native';
import type {
  HTMLSourceInline,
  MixedStyleDeclaration,
} from 'react-native-render-html';
import RenderHTML, { useContentWidth } from 'react-native-render-html';
import sanitize from 'sanitize-html';

import { ErrorBoundary } from '@libs/error-boundary';
import { useZestStyles } from '@zest/react-native';

import { stylesConfig } from './styles';

export const RenderSanitizedHTML = ({
  source,
  style,
  config,
  maxWords,
}: {
  source: HTMLSourceInline;
  style?: MixedStyleDeclaration;
  config?: sanitize.IOptions;
  maxWords?: number;
}) => {
  const width = useContentWidth();
  const styles = useZestStyles(stylesConfig);

  const baseStyle = {
    ...styles.baseStyle,
    ...style,
  } as MixedStyleDeclaration;

  return (
    <View>
      <ErrorBoundary scope={{ moduleName: 'RenderSanitizedHTML' }}>
        <RenderHTML
          contentWidth={width}
          source={{
            html: truncateHTML(sanitize(source.html, config), maxWords),
          }}
          enableExperimentalMarginCollapsing={true}
          baseStyle={baseStyle}
        />
      </ErrorBoundary>
    </View>
  );
};

export const needTruncating = (html: string, maxWords: number) => {
  const tempDiv = html.replace(/<[^>]*>/g, ' ');
  return splitToWords(tempDiv).length > maxWords;
};

const splitToWords = (text: string) => {
  return text.trim().split(/\s+/);
};

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
```

**Key patterns demonstrated:**
- RenderSanitizedHTML wraps react-native-render-html with sanitize-html
- sanitize(source.html, config) sanitizes HTML before rendering (XSS prevention)
- truncateHTML(sanitized, maxWords) truncates by word count after sanitization
- ErrorBoundary wraps component for graceful degradation on rendering errors
- useContentWidth() provides responsive width from react-native-render-html
- Optional config prop for custom sanitization rules (allowedTags, allowedAttributes)
- Optional maxWords prop for text truncation
- Optional style prop merged with baseStyle from Zest theme
- needTruncating helper function to check if content exceeds word limit
- splitToWords uses regex /\s+/ to handle multiple spaces, tabs, newlines
- enableExperimentalMarginCollapsing for better paragraph spacing

## Example 2: Empty State with Translated HTML Content

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/components/empty-state/EmptyStateView.tsx:13`

This example shows rendering translated HTML content in empty state component.

```typescript
import { View, Image } from 'react-native';
import { useT9n } from '@libs/localization';
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';
import { useZestStyles, Text, Button, Link } from '@zest/react-native';

const TextContainer = () => {
  const styles = useZestStyles(stylesConfig);
  const { translateRaw } = useT9n('social-recipe-bridge');

  return (
    <View style={styles.textContainer}>
      <Text style={styles.headline} type="headline-md">
        {translateRaw('social-recipe-bridge.empty_state.headline')}
      </Text>
      <RenderSanitizedHTML
        source={{
          html: translateRaw('social-recipe-bridge.empty_state.body_text'),
        }}
        style={styles.bodyText}
      />
    </View>
  );
};

export const EmptyStateView = ({
  onSaveRecipePress,
  onLearnMorePress,
}: EmptyStateViewProps) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <View style={styles.contentCard}>
          <Image
            source={emptyStateIllustration}
            style={styles.image}
            resizeMode="contain"
            accessibilityIgnoresInvertColors
          />
          <TextContainer />
          <ButtonsContainer
            onSaveRecipePress={onSaveRecipePress}
            onLearnMorePress={onLearnMorePress}
          />
        </View>
      </View>
    </View>
  );
};
```

**Key patterns demonstrated:**
- RenderSanitizedHTML with translateRaw for internationalized HTML content
- Translation key returns HTML string from translation file
- Custom style prop (styles.bodyText) for themed typography
- No maxWords - display full translated content
- No custom config - uses default sanitization rules
- Component composition pattern (TextContainer extracted)
- Empty state pattern with illustration, headline, body text, CTA buttons
- useT9n hook for translations with feature namespace

## Example 3: Upsell Nudge with Dynamic HTML

**File**: `modules/store/screens/cart/components/upsell-nudge-button/UpsellNudgeButton.tsx:15`

This example shows rendering dynamic HTML content from API in upsell button.

```typescript
import { Pressable, View } from 'react-native';
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';
import { Icon, useZestStyles } from '@zest/react-native';

type Props = {
  isAddon: boolean;
  onPress: () => void;
};

export const UpsellNudgeButton = ({ isAddon, onPress }: Props) => {
  const styles = useZestStyles(stylesConfig);
  const upsellNudgeButtonInfo = useUpsellNudgeButtonInfo(isAddon);

  if (!upsellNudgeButtonInfo) {
    return null;
  }

  const { isDisabled, title } = upsellNudgeButtonInfo;

  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [styles.container, pressed && styles.pressed]}
      testID={`upsell-nudge-button-${isAddon ? 'addons' : 'meals'}`}
      disabled={isDisabled}
    >
      <View style={styles.innerContainer}>
        <Icon
          icon={isDisabled ? 'CircleInfoOutline24' : 'PlusOutline24'}
          altText="Icon"
          testID="upsell-nudge-button-icon"
        />
        <View style={styles.textContainer}>
          <RenderSanitizedHTML style={styles.text} source={{ html: title }} />
        </View>
      </View>
      {!isDisabled && (
        <Icon
          icon="ChevronRightOutline24"
          altText="Chevron Right Icon"
          testID="upsell-nudge-button-chevron"
          style={styles.chevron}
        />
      )}
    </Pressable>
  );
};
```

**Key patterns demonstrated:**
- RenderSanitizedHTML with dynamic HTML from API (title prop)
- Custom hook useUpsellNudgeButtonInfo provides HTML content
- Inline style prop (styles.text) for button text styling
- No maxWords - display full upsell message
- No custom config - default sanitization for user-facing content
- Conditional rendering (if !upsellNudgeButtonInfo return null)
- Pressable with disabled state and pressed styling
- testID for E2E testing
- Icon with conditional variant (CircleInfoOutline24 or PlusOutline24)
- Chevron icon only shown when not disabled

## Example 4: Sustainability Section with CMS Content

**File**: `features/shoppable-product-sections/sustainability/Sustainability.tsx:19`

This example shows rendering CMS-provided HTML content with null safety checks.

```typescript
import { useMemo } from 'react';
import { Linking, View } from 'react-native';
import { useData } from '@features/shoppable-product-data-provider';
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';
import { useFeatureContent } from '@operations/feature-content/queries';
import { Link, Text, useZestStyles } from '@zest/react-native';

export const Sustainability = () => {
  const { productDetails } = useData();
  const styles = useZestStyles(stylesConfig);
  const { data: content } = useFeatureContent(SustainabilityNudge);

  const sustainabilityTag = productDetails?.product?.tags?.find((tag) =>
    RECIPE_SCORES.includes(tag.handle)
  );

  const sustainabilityScore = useMemo(() => {
    if (!sustainabilityTag) {
      return null;
    }

    return content?.climate?.[sustainabilityTag.handle as RecipeScore];
  }, [content, sustainabilityTag]);

  if (!sustainabilityTag) {
    return null;
  }

  const hasContent =
    !!sustainabilityScore &&
    (sustainabilityScore?.title || sustainabilityScore?.description);

  if (!hasContent) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Text type="headline-md">{sustainabilityScore.title}</Text>
      <View style={styles.gradeContainer}>
        <SustainabilityGrade tag={sustainabilityTag} />
      </View>
      <View>
        {sustainabilityScore.description && (
          <RenderSanitizedHTML
            source={{ html: sustainabilityScore.description }}
          />
        )}
        <Link onPress={() => Linking.openURL(sustainabilityScore.url)}>
          {sustainabilityScore.url_title}
        </Link>
      </View>
    </View>
  );
};
```

**Key patterns demonstrated:**
- RenderSanitizedHTML with CMS content (sustainabilityScore.description)
- Conditional rendering (sustainabilityScore.description &&)
- Multiple null safety checks before rendering
- useMemo for derived sustainabilityScore computation
- Early returns for null states (no tag, no content)
- hasContent guard checks both title and description exist
- useFeatureContent hook fetches CMS data
- Optional chaining throughout (productDetails?.product?.tags)
- No custom style - uses default Zest theme
- Link component for external URL (Linking.openURL)

## Example 5: Testing RenderSanitizedHTML

**File**: `libs/render-sanitized-html/RenderSanitizedHTML.test.tsx:17`

This example shows comprehensive testing patterns for HTML sanitization and truncation.

```typescript
import { render, screen } from '@testing-library/react-native';
import { RenderSanitizedHTML, needTruncating } from './RenderSanitizedHTML';

// Mock only what's necessary for testing
jest.mock('@zest/react-native', () => ({
  useZestStyles: () => ({
    baseStyle: {
      color: 'black',
      fontSize: 16,
      lineHeight: 24,
    },
  }),
  createStylesConfig: (config: Record<string, unknown>) => config,
}));

describe('RenderSanitizedHTML', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Basic Rendering', () => {
    it('renders HTML content correctly', () => {
      const htmlContent = '<p>Hello World</p>';

      render(<RenderSanitizedHTML source={{ html: htmlContent }} />);

      expect(screen.getByText('Hello World')).toBeTruthy();
    });

    it('sanitizes HTML content', () => {
      const maliciousHtml = '<script>alert("hack")</script><p>Safe content</p>';

      render(<RenderSanitizedHTML source={{ html: maliciousHtml }} />);

      // The script tag should be removed by sanitize-html
      expect(screen.getByText(/Safe content/)).toBeTruthy();
      expect(screen.queryByText(/alert/)).toBeNull();
    });

    it('applies custom config for sanitization', () => {
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

      // With restrictive config, only <p> tags should remain
      expect(screen.getByText(/Bold and italic/)).toBeTruthy();
    });
  });

  describe('maxWords functionality', () => {
    const longHtmlContent =
      '<p>This is a very long paragraph with many words that should be truncated when the maximum word limit is exceeded for testing purposes.</p>';

    it('truncates content when maxWords is specified and exceeded', () => {
      render(
        <RenderSanitizedHTML
          source={{ html: longHtmlContent }}
          maxWords={5}
        />
      );

      expect(screen.getByText(/\.\.\./)).toBeTruthy();
      expect(screen.queryByText(/testing purposes/)).toBeNull();
    });

    it('does not truncate when content is shorter than maxWords', () => {
      const shortContent = '<p>Short content</p>';

      render(
        <RenderSanitizedHTML source={{ html: shortContent }} maxWords={10} />
      );

      expect(screen.getByText(/Short content/)).toBeTruthy();
      expect(screen.queryByText(/\.\.\./)).toBeNull();
    });

    it('handles HTML tags correctly when truncating', () => {
      const htmlWithTags =
        '<p><strong>Bold</strong> text <em>italic</em> more words here</p>';

      render(
        <RenderSanitizedHTML source={{ html: htmlWithTags }} maxWords={3} />
      );

      expect(screen.getByText(/\.\.\./)).toBeTruthy();
      expect(screen.queryByText(/more words here/)).toBeNull();
    });
  });

  describe('Integration with sanitization', () => {
    it('truncates after sanitization removes dangerous content', () => {
      const maliciousHtml =
        '<script>alert("hack")</script><p>Safe word1 word2 word3 word4 word5</p>';

      render(
        <RenderSanitizedHTML source={{ html: maliciousHtml }} maxWords={3} />
      );

      // Should be sanitized first, then truncated
      expect(screen.getByText(/Safe.*word1.*word2.*\.\.\./)).toBeTruthy();
      expect(screen.queryByText(/word3 word4 word5/)).toBeNull();
      expect(screen.queryByText(/alert/)).toBeNull();
    });
  });
});

describe('needTruncating', () => {
  it('returns true when text exceeds maxWords limit', () => {
    const longText =
      '<p>This is a very long text with many words that should be truncated</p>';
    const result = needTruncating(longText, 5);
    expect(result).toBe(true);
  });

  it('returns false when text is within maxWords limit', () => {
    const shortText = '<p>Short text</p>';
    const result = needTruncating(shortText, 5);
    expect(result).toBe(false);
  });

  it('ignores HTML tags when counting words', () => {
    const htmlText =
      '<p><strong>One</strong> <em>two</em> <span>three</span></p>';
    const result = needTruncating(htmlText, 5);
    expect(result).toBe(false); // Only 3 words
  });
});
```

**Key patterns demonstrated:**
- Mock useZestStyles for isolated component testing
- Test HTML rendering (renders content correctly)
- Test XSS prevention (script tags removed)
- Test custom sanitization config (allowedTags)
- Test truncation with maxWords
- Test no truncation when content is short
- Test HTML tags ignored when counting words for truncation
- Test sanitization happens before truncation (security first)
- Test needTruncating helper function separately
- Use regex matchers for flexible text matching (/Safe.*word1/)
- Use getByText for existence, queryByText for null checks
- beforeEach clears mocks for test isolation
- Separate describe blocks for feature grouping

## Summary

The YourCompany codebase consistently follows these content rendering patterns:

1. **RenderSanitizedHTML Component** - Wraps react-native-render-html with sanitize-html
2. **XSS Prevention** - Always sanitize HTML before rendering with sanitize(source.html, config)
3. **ErrorBoundary Wrapping** - Wrap component for graceful degradation
4. **Truncation Order** - Sanitize first, then truncate (security before UX)
5. **useContentWidth Hook** - Responsive width from react-native-render-html
6. **Optional Config** - Custom sanitization rules (allowedTags, allowedAttributes)
7. **Optional maxWords** - Word-based truncation with ellipsis
8. **Optional Style** - Merged with baseStyle from Zest theme
9. **Translated Content** - RenderSanitizedHTML with translateRaw for i18n HTML
10. **Dynamic Content** - HTML from API responses, CMS, feature content hooks
11. **Null Safety** - Conditional rendering, optional chaining, early returns
12. **needTruncating Helper** - Check if content exceeds word limit before rendering
13. **Testing Sanitization** - Test XSS prevention (script tags removed)
14. **Testing Truncation** - Test maxWords with long/short content, HTML tag handling
15. **Testing Integration** - Test sanitization happens before truncation

These patterns enable safe HTML rendering, prevent XSS attacks through sanitization, provide flexible truncation for long content, ensure responsive layouts with useContentWidth, and maintain accessibility with error boundaries and graceful degradation.
