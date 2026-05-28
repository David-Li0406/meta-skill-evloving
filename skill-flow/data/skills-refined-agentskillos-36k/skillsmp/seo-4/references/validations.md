# Seo - Validations

## Missing or Generic Meta Title

### **Id**
seo-missing-meta-title
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <title>\s*</title>
  - <title>Home</title>
  - <title>Untitled</title>
  - <title>Document</title>
### **Message**
Missing or generic meta title. Title is the most important on-page SEO element.
### **Fix Action**
Add unique, descriptive title: <title>Primary Keyword - Brand | Value Proposition</title>
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Missing Meta Description

### **Id**
seo-missing-meta-description
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <head>(?!.*meta.*description).*</head>
### **Message**
Missing meta description. Google uses this for search snippets. Controls your click-through rate.
### **Fix Action**
Add compelling meta description (150-160 chars) with target keyword and clear value prop
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Keyword Stuffing Detected

### **Id**
seo-keyword-stuffing
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (\b\w{5,}\b)(?:[^.]*\1){4,}
### **Message**
Same word repeated excessively. Google penalizes keyword stuffing. Write naturally.
### **Fix Action**
Use variations, synonyms, and natural language. If it sounds robotic, rewrite.
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing H1 Tag

### **Id**
seo-missing-h1
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <body>(?!.*<h1).*</body>
### **Message**
Missing H1 tag. Each page needs exactly one H1 with the primary keyword.
### **Fix Action**
Add single H1 at top of content with primary keyword
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Multiple H1 Tags

### **Id**
seo-multiple-h1
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <h1[^>]*>.*<h1[^>]*>
### **Message**
Multiple H1 tags detected. Use only one H1 per page.
### **Fix Action**
Keep primary H1, convert others to H2 or H3
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Image Without Alt Text

### **Id**
seo-img-no-alt
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <img[^>]*(?!.*alt=)[^>]*/>
  - <img[^>]*alt=["']["'][^>]*/>
### **Message**
Image without alt text. Bad for accessibility and misses SEO opportunity.
### **Fix Action**
Add descriptive alt text with relevant keywords where natural
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx
  - *.md

## Thin Content Warning

### **Id**
seo-thin-content
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^.{0,300}$
### **Message**
Content appears thin. Pages with less than 300 words rarely rank well.
### **Fix Action**
Expand with valuable content: examples, details, FAQs, related topics
### **Applies To**
  - *.md
  - *.html

## Potentially Broken Internal Link

### **Id**
seo-broken-internal-link
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - href=["\047]/[^"\047]*\s[^"\047]*["\047]
  - href=["\047]#["\047]
### **Message**
Suspicious internal link pattern. Broken links hurt SEO and user experience.
### **Fix Action**
Verify link works. Use relative paths or proper absolute URLs.
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx
  - *.md

## Missing Canonical URL

### **Id**
seo-no-canonical
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <head>(?!.*rel=["\047]canonical["\047]).*</head>
### **Message**
Missing canonical URL. Duplicate content can split ranking authority.
### **Fix Action**
Add <link rel='canonical' href='https://yoursite.com/page' />
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Non-Descriptive Link Text

### **Id**
seo-non-descriptive-link
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - >click.?here<
  - >read.?more<
  - >learn.?more<
  - >here<
### **Message**
Non-descriptive link text. Anchor text should describe destination content.
### **Fix Action**
Use descriptive anchor: 'click here' → 'view our pricing plans'
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx
  - *.md

## Unoptimized Image Format

### **Id**
seo-slow-image
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - src=["\047][^"\047]*\.(?:bmp|tiff|gif)["\047]
  - src=["\047][^"\047]*\.png["\047](?!.*loading)
### **Message**
Potentially unoptimized image format. Use WebP or compressed JPEG for better performance.
### **Fix Action**
Convert to WebP, add loading='lazy' for below-fold images
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx

## Missing Structured Data

### **Id**
seo-no-schema
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <head>(?!.*application/ld\+json).*</head>
### **Message**
No structured data found. Schema markup enables rich snippets in search results.
### **Fix Action**
Add JSON-LD schema: Organization, Product, FAQ, HowTo as relevant
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx