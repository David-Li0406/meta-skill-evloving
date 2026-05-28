# Content Strategy - Validations

## Missing or Weak Headline

### **Id**
content-missing-headline
### **Severity**
error
### **Type**
regex
### **Pattern**
^(?!#\s+.{10,})|(?i)^#\s+(untitled|draft|new post|placeholder)
### **Message**
Content appears to be missing a strong headline or uses placeholder text
### **Fix Action**
Add a compelling, descriptive headline that clearly communicates the content's value proposition
### **Applies To**
  - *.md
  - *.html

## Thin Content (Less than 300 words)

### **Id**
content-thin-content
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?:(?:\s*\w+\s*){1,299})$
### **Message**
Content appears to be thin (under 300 words), which may not provide sufficient value
### **Fix Action**
Expand content with detailed information, examples, or actionable insights to reach at least 300-500 words
### **Applies To**
  - *.md

## Missing Content Structure (No Subheadings)

### **Id**
content-no-structure
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*^##\s+)
### **Message**
Content lacks structural hierarchy - no H2 subheadings detected for scanability
### **Fix Action**
Break content into logical sections using H2 and H3 subheadings to improve readability and SEO
### **Applies To**
  - *.md
  - *.html

## Missing Internal Links

### **Id**
content-no-internal-links
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*\[.+\]\(.+\))
### **Message**
No internal links detected - missing opportunity for content interconnection and SEO
### **Fix Action**
Add 2-5 relevant internal links to related content to improve site architecture and user engagement
### **Applies To**
  - *.md
  - *.html

## Missing Call-to-Action

### **Id**
content-no-cta
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(subscribe|download|learn more|get started|sign up|try|join|contact|book|register))
### **Message**
No clear call-to-action detected in content
### **Fix Action**
Add at least one clear CTA that guides readers to the next step in their journey
### **Applies To**
  - *.md
  - *.html

## Missing Meta Description

### **Id**
content-missing-meta-description
### **Severity**
error
### **Type**
regex
### **Pattern**
^(?!.*<meta\s+name=["']description)|^(?!.*description:\s*.{50,})
### **Message**
Meta description is missing or too short for SEO optimization
### **Fix Action**
Add a meta description between 150-160 characters that summarizes the content and includes target keywords
### **Applies To**
  - *.html
  - *.md

## Potential Keyword Stuffing

### **Id**
content-keyword-stuffing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (\b\w+\b)(?:\s+\1){3,}
### **Message**
Detected repeated keywords that may indicate keyword stuffing
### **Fix Action**
Use natural language and synonyms instead of repeating the same keyword multiple times in succession
### **Applies To**
  - *.md
  - *.html

## Missing Visual Content

### **Id**
content-no-images
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:<img|!\[))
### **Message**
No images or visual content detected - may reduce engagement
### **Fix Action**
Add relevant images, infographics, or visual elements to break up text and increase engagement
### **Applies To**
  - *.md
  - *.html

## Potential Broken Link Patterns

### **Id**
content-broken-links
### **Severity**
warning
### **Type**
regex
### **Pattern**
\[.+\]\((?:localhost|127\.0\.0\.1|example\.com|test\.com|placeholder)\)|\[.+\]\(#\)
### **Message**
Detected placeholder or test links that may be broken
### **Fix Action**
Replace placeholder links with actual URLs or remove them before publishing
### **Applies To**
  - *.md
  - *.html

## Missing Mobile Viewport Meta Tag

### **Id**
content-no-mobile-optimization
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*<meta\s+name=["']viewport)
### **Message**
Missing viewport meta tag - content may not be mobile-optimized
### **Fix Action**
Add <meta name="viewport" content="width=device-width, initial-scale=1.0"> to the HTML head
### **Applies To**
  - *.html

## Excessively Long Paragraphs

### **Id**
content-excessive-length
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?m)^(?!#|\*|-|>|```|\|).{500,}$
### **Message**
Detected paragraphs exceeding 500 characters - may reduce readability
### **Fix Action**
Break long paragraphs into smaller chunks (3-4 sentences max) for better readability and scanability
### **Applies To**
  - *.md

## Missing Structured Data (Schema.org)

### **Id**
content-missing-schema
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:application/ld\+json|itemscope|schema\.org))
### **Message**
No structured data markup detected - missing SEO enhancement opportunity
### **Fix Action**
Add relevant Schema.org markup (Article, BlogPosting, etc.) to enhance search engine understanding
### **Applies To**
  - *.html