# Content Rendering - Implementation Patterns

Implementation patterns for rendering localized content in web applications.

## Pattern: Use dangerouslySetInnerHTML Safely

Render HTML content with sanitization.

✅ **Good:**
\`\`\`typescript
import DOMPurify from 'dompurify';

const SafeHTML = ({ html }: { html: string }) => {
  const sanitized = DOMPurify.sanitize(html);

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
};
\`\`\`

❌ **Bad:**
\`\`\`typescript
<div dangerouslySetInnerHTML={{ __html: userContent }} />
\`\`\`

**Why:** Sanitization:
- Prevents XSS
- Security
- Safe HTML rendering

## Pattern: Use Trans Component

Render translated content with components.

✅ **Good:**
\`\`\`typescript
import { Trans } from 'react-i18next';

<Trans i18nKey="welcome">
  Welcome <strong>{{name}}</strong>
</Trans>
\`\`\`

**Why:** Trans:
- Components in translations
- Type safety
- Better UX

## Pattern: Sanitize User Content

Always sanitize user-generated content.

✅ **Good:**
\`\`\`typescript
const clean = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong'],
});
\`\`\`

❌ **Bad:**
\`\`\`typescript
<div>{userInput}</div>
\`\`\`

**Why:** Sanitization:
- Security
- Prevent XSS
- Control allowed content

## Summary

**Key Patterns:**
- Sanitize HTML content
- Use Trans component
- Safe innerHTML rendering
- Control allowed tags

**Anti-Patterns:**
- No sanitization
- Direct user content rendering
- Unsafe innerHTML
