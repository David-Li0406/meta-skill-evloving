# Viral Marketing - Validations

## Missing Share Triggers

### **Id**
viral-missing-share-triggers
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:share|tweet|post|forward|send|tell|show|tag|mention|spread|retweet|reblog)).*$
### **Message**
No share triggers or calls detected - content unlikely to spread virally
### **Fix Action**
Include explicit share prompts: 'Share this with someone who needs to hear it', 'Tag a friend who...' or social sharing buttons
### **Applies To**
  - *.md
  - *.html

## Missing Strong Emotional Hooks

### **Id**
viral-no-emotional-hooks
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:shocking|amazing|incredible|unbelievable|surprising|stunning|jaw-dropping|mind-blowing|heartwarming|inspiring|outrageous|hilarious|terrifying|devastating)).*$
### **Message**
No strong emotional hooks detected - viral content needs emotional resonance
### **Fix Action**
Create content that triggers high-arousal emotions: awe, anger, anxiety, humor, or inspiration
### **Applies To**
  - *.md
  - *.html

## Complex or Friction-Heavy Sharing Flow

### **Id**
viral-complex-sharing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(?:click here to share|copy this link|go to.*share|follow these steps|first.*then.*share)
### **Message**
Sharing process appears too complex - friction reduces viral potential
### **Fix Action**
Make sharing one-click easy: direct social buttons, pre-written share text, or simple copy-paste
### **Applies To**
  - *.md
  - *.html

## Missing Social Currency (Makes Sharer Look Good)

### **Id**
viral-no-social-currency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:insider|secret|exclusive|first|early|special access|behind the scenes|not many know|little-known|hidden|hack|tip|trick)).*$
### **Message**
Content lacks social currency - people share things that make them look smart, helpful, or in-the-know
### **Fix Action**
Frame content to make sharers look knowledgeable, helpful, or part of exclusive group
### **Applies To**
  - *.md
  - *.html

## Missing Practical Value

### **Id**
viral-not-practical-valuable
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:how to|guide|tips?|ways? to|steps? to|learn|tutorial|free|template|checklist|cheat sheet|tool|resource)).*$
### **Message**
No clear practical value - viral content is often highly useful and shareable
### **Fix Action**
Provide actionable tips, how-to guides, or tools that people want to save and share
### **Applies To**
  - *.md
  - *.html

## Missing Viral Visual Elements

### **Id**
viral-no-visual-elements
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:<img|!\[|<video|iframe|embed)).*$
### **Message**
No images or videos detected - visual content is 40x more likely to be shared
### **Fix Action**
Add eye-catching images, infographics, memes, GIFs, or videos that tell the story visually
### **Applies To**
  - *.md
  - *.html

## Too Safe or Middle-Ground

### **Id**
viral-not-controversial-polarizing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \b(?i)(?:maybe|perhaps|possibly|might|could|some say|it depends|on the other hand|balanced approach)\b
### **Message**
Content appears too safe or balanced - viral content often takes a clear stance
### **Fix Action**
Take a clear position or challenge conventional wisdom (while staying ethical and factual)
### **Applies To**
  - *.md
  - *.html
  - *.txt

## No Curiosity Gap in Headlines

### **Id**
viral-missing-curiosity-gap
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^#\s+(?!.*(?i)(?:\?|what|why|how|when|secret|reason|this is|you won't believe|nobody tells|most people don't|surprising|truth about)).*$
### **Message**
Headline lacks curiosity gap - doesn't create desire to click and share
### **Fix Action**
Create headlines that tease value without giving everything away: 'Why X Does Y (It's Not What You Think)'
### **Applies To**
  - *.md
  - *.html

## Missing Discussion or Debate Trigger

### **Id**
viral-no-controversy-debate
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:debate|controversial|disagree|argue|wrong|right|should|shouldn't|best|worst|vs|versus|better than|overrated|underrated)).*$
### **Message**
No elements that trigger discussion or debate - reduces comment and share activity
### **Fix Action**
Include elements that spark conversation: comparisons, rankings, controversial takes, or provocative questions
### **Applies To**
  - *.md
  - *.html

## Excessively Long Content for Viral Sharing

### **Id**
viral-too-long-form
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?:\w+\s+){1500,}
### **Message**
Content may be too long for viral sharing - optimal is 600-1000 words or quick-scan format
### **Fix Action**
Either shorten content or break into scannable chunks with visuals, bullets, and subheadings
### **Applies To**
  - *.md

## Missing Open Graph Meta Tags for Social Sharing

### **Id**
viral-missing-og-meta
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*<meta\\s+property=["']og:)
### **Message**
Missing Open Graph meta tags - will look unprofessional when shared on social media
### **Fix Action**
Add og:title, og:description, og:image, and og:url meta tags for optimal social sharing appearance
### **Applies To**
  - *.html

## Missing Numbers or Data Points

### **Id**
viral-no-numbers-data
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*\d+(?:%|\+|x|times)).*$
### **Message**
No compelling numbers or statistics - data makes content more credible and shareable
### **Fix Action**
Include specific numbers: percentages, statistics, time savings, or concrete results
### **Applies To**
  - *.md
  - *.html

## Missing Timeliness or Trend Connection

### **Id**
viral-no-timing-relevance
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:2025|2024|latest|new|recent|today|this week|current|now|trending|breaking|just|update)).*$
### **Message**
Content lacks timeliness or trend connection - timely content spreads faster
### **Fix Action**
Connect to current events, trending topics, or emphasize recency and newness
### **Applies To**
  - *.md
  - *.html