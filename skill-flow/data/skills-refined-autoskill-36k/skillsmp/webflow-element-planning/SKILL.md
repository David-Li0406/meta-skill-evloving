---
name: webflow-element-planning
description: |
  Maps page briefs and component specs to Webflow element structures. Generates element trees with Client-First class names, CMS bindings, and responsive breakpoint planning.

  USE THIS SKILL WHEN:
  - Translating page briefs to Webflow element structures
  - Planning CMS bindings before build
  - Generating Client-First class names
  - Creating element trees for sections/components
  - Planning responsive layouts for Webflow

  PROVIDES: Element mapping tables, Client-First patterns, CMS binding templates, responsive layout patterns
allowed-tools: Read, Grep, Glob
---

# Webflow Element Planning Skill

## Overview

This skill bridges strategic page briefs and Webflow implementation. It provides systematic mappings from content requirements to Webflow elements, ensuring consistent Client-First naming and proper CMS binding structure.

---

## Framework 1: Page Brief to Element Mapping

### Section Type to Webflow Structure

Every section in a page brief maps to a consistent Webflow structure:

```
PAGE BRIEF SECTION           WEBFLOW STRUCTURE
────────────────────────────────────────────────────────────────

Hero Section                 section_hero
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-large
                                       └─ hero_component
                                          ├─ hero-content
                                          │  ├─ heading-style-h1
                                          │  ├─ text-size-regular
                                          │  └─ button-primary
                                          └─ hero-image-wrapper
                                             └─ hero-image

Features Grid                section_features
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-medium
                                       └─ features_component
                                          ├─ features-header
                                          │  ├─ heading-style-h2
                                          │  └─ text-size-regular
                                          └─ features-grid
                                             └─ card_component (repeat)
                                                ├─ card-icon-wrapper
                                                ├─ card-title
                                                └─ card-description

Testimonials                 section_testimonials
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-medium
                                       └─ testimonials_component
                                          ├─ testimonials-header
                                          └─ testimonials-grid
                                             └─ testimonial_component (CMS)
                                                ├─ testimonial-quote
                                                ├─ testimonial-author
                                                └─ testimonial-role

Pricing                      section_pricing
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-large
                                       └─ pricing_component
                                          ├─ pricing-header
                                          └─ pricing-grid
                                             └─ pricing-card_component
                                                ├─ pricing-card-header
                                                ├─ pricing-card-price
                                                ├─ pricing-card-features
                                                └─ pricing-card-cta

CTA Banner                   section_cta
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-medium
                                       └─ cta_component
                                          ├─ cta-content
                                          │  ├─ heading-style-h2
                                          │  └─ text-size-regular
                                          └─ cta-actions
                                             ├─ button-primary
                                             └─ button-secondary

Logo Bar                     section_logos
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-small
                                       └─ logos_component
                                          ├─ logos-heading (optional)
                                          └─ logos-grid
                                             └─ logo-item (repeat)

FAQ Accordion                section_faq
                              └─ padding-global
                                 └─ container-large
                                    └─ padding-section-medium
                                       └─ faq_component
                                          ├─ faq-header
                                          └─ faq-list
                                             └─ faq-item_component (CMS)
                                                ├─ faq-question
                                                └─ faq-answer

Contact Form                 section_contact
                              └─ padding-global
                                 └─ container-medium
                                    └─ padding-section-medium
                                       └─ contact_component
                                          ├─ contact-content
                                          └─ contact-form
                                             ├─ form-group (repeat)
                                             └─ form-submit
```

---

## Framework 2: Client-First Class Naming

### Naming Convention Reference

```
CLIENT-FIRST CLASS PATTERNS
────────────────────────────────────────────────────────────────

SECTIONS (Top-level containers)
Pattern: section_[name]
Examples:
  section_hero
  section_features
  section_pricing
  section_contact
  section_footer

COMPONENTS (Reusable elements)
Pattern: [name]_component
Examples:
  hero_component
  card_component
  testimonial_component
  pricing-card_component

ELEMENTS (Within components)
Pattern: [component]-[element] or [element-name]
Examples:
  hero-content
  hero-image
  card-title
  card-description
  pricing-card-price

GLOBAL ELEMENTS (Typography, spacing)
Predefined by Client-First:
  heading-style-h1 through h6
  text-size-regular
  text-size-small
  button-primary
  button-secondary
  padding-global
  container-small / container-medium / container-large
  padding-section-small / medium / large / huge

STATE CLASSES (Modifiers)
Pattern: is-[state]
Examples:
  is-active
  is-featured
  is-current
  is-open
  is-hidden
```

### Common Class Combinations

```
HERO SECTION
────────────────────────────────────────────────────────────────
section_hero                          Section wrapper
  padding-global                      Horizontal page margins
    container-large                   Max-width container
      padding-section-large           Vertical spacing
        hero_component                Component wrapper
          hero-content                Text content area
            heading-style-h1          Main headline
            text-size-regular         Subheadline
            hero-cta-wrapper          Button container
              button-primary          Primary CTA
              button-secondary        Secondary CTA (optional)
          hero-image-wrapper          Image container
            hero-image                Main hero image


FEATURE CARDS
────────────────────────────────────────────────────────────────
features-grid                         Grid container
  card_component                      Individual card
    card-icon-wrapper                 Icon container
      card-icon                       Icon image/SVG
    card-content                      Text area
      card-title                      Card heading
      card-description                Card body text
    card-link (optional)              Card link wrapper


TESTIMONIAL
────────────────────────────────────────────────────────────────
testimonial_component                 Testimonial card
  testimonial-quote                   Quote text
  testimonial-author-wrapper          Author info container
    testimonial-image                 Author photo
    testimonial-author-info           Name/role container
      testimonial-author              Author name
      testimonial-role                Author title/company


NAVIGATION
────────────────────────────────────────────────────────────────
nav_component                         Navigation wrapper
  nav-container                       Inner container
    nav-logo-wrapper                  Logo area
      nav-logo                        Logo image
    nav-menu                          Menu wrapper
      nav-link                        Menu link
      nav-link is-current             Active menu link
    nav-actions                       CTA area
      button-secondary                Secondary action
      button-primary                  Primary action
```

---

## Framework 3: CMS Binding Planning

### CMS Field to Webflow Element Mapping

```
CMS FIELD TYPES → WEBFLOW ELEMENTS
────────────────────────────────────────────────────────────────

PlainText / RichText
  → Heading (H1-H6)
  → Paragraph
  → Text Block
  Binding: Text content

Image
  → Image element
  Binding: Image source + alt text

Link
  → Link Block
  → Button
  → Text Link
  Binding: href URL

Reference
  → Collection List (filtered)
  → Single reference lookup
  Binding: Related collection item

MultiReference
  → Collection List
  Binding: Multiple related items

Switch (Boolean)
  → Conditional visibility
  → Class modifier (is-featured)
  Binding: Show/hide element

DateTime
  → Text Block with formatting
  Binding: Formatted date string

Number
  → Text Block
  → Counter display
  Binding: Numeric value

Color
  → Background color
  → Text color
  → Border color
  Binding: CSS color property

File
  → Download link
  → Embedded document
  Binding: File URL

Video
  → Video embed
  → Background video
  Binding: Video URL
```

### CMS Collection Structure Template

```
COLLECTION: [Name]
Slug: [collection-slug]

FIELDS:
────────────────────────────────────────────────────────────────
Field Name          Type            Binding Target
────────────────────────────────────────────────────────────────
name                PlainText       Heading, Card title
slug                Slug            URL structure
description         RichText        Body text, Card description
thumbnail           Image           Card image, List image
heroImage           Image           Hero background/main image
excerpt             PlainText       Short description, meta
authorRef           Reference       Related author collection
categoryRef         Reference       Related category
tags                MultiReference  Tag list, filtering
isFeatured          Switch          Featured badge, sorting
publishDate         DateTime        Display date, sorting
ctaText             PlainText       Button text
ctaLink             Link            Button destination
price               Number          Pricing display
```

### CMS-Ready Element Markers

When planning elements, mark CMS-bound fields:

```json
{
  "element": "Heading",
  "tag": "h3",
  "class": "card-title",
  "cms_binding": {
    "field": "name",
    "type": "PlainText",
    "collection": "BlogPost"
  }
}
```

---

## Framework 4: Responsive Layout Patterns

### Breakpoint Strategy

```
WEBFLOW BREAKPOINTS
────────────────────────────────────────────────────────────────

Desktop (Base)           1920px and above
                          └─ Design starting point

Laptop (1440px)          1440px - 1919px
                          └─ Common laptop screens

Tablet (991px)           768px - 990px
                          └─ Portrait tablets

Mobile Landscape (767px) 480px - 767px
                          └─ Phones landscape

Mobile Portrait (478px)  479px and below
                          └─ Phones portrait
```

### Responsive Grid Patterns

```
GRID BEHAVIOR BY BREAKPOINT
────────────────────────────────────────────────────────────────

4-Column Grid (Features, Pricing)
  Desktop:    4 columns
  Laptop:     4 columns
  Tablet:     2 columns
  Mobile:     1 column

3-Column Grid (Cards, Team)
  Desktop:    3 columns
  Laptop:     3 columns
  Tablet:     2 columns (or 3 compact)
  Mobile:     1 column

2-Column Grid (Hero, CTA)
  Desktop:    2 columns (50/50 or 40/60)
  Laptop:     2 columns
  Tablet:     Stacked (1 column)
  Mobile:     Stacked (1 column)

Logo Bar
  Desktop:    6 logos inline
  Laptop:     6 logos inline
  Tablet:     4 logos (wrap)
  Mobile:     3 logos (wrap) or slider
```

### Responsive Typography Scale

```
TYPOGRAPHY BY BREAKPOINT
────────────────────────────────────────────────────────────────

Element              Desktop    Tablet     Mobile
────────────────────────────────────────────────────────────────
heading-style-h1     72px       56px       40px
heading-style-h2     48px       40px       32px
heading-style-h3     36px       32px       28px
heading-style-h4     24px       22px       20px
heading-style-h5     20px       18px       18px
heading-style-h6     16px       16px       16px
text-size-regular    18px       17px       16px
text-size-small      14px       14px       14px
```

### Responsive Spacing Scale

```
SPACING BY BREAKPOINT
────────────────────────────────────────────────────────────────

Token                Desktop    Tablet     Mobile
────────────────────────────────────────────────────────────────
padding-section-huge   160px     120px      80px
padding-section-large  120px     80px       64px
padding-section-medium 80px      64px       48px
padding-section-small  40px      32px       24px
container max-width    1200px    90%        90%
padding-global         48px      32px       20px
```

---

## Framework 5: Webflow Element Types

### Element Selection Guide

```
ELEMENT TYPE DECISION TREE
────────────────────────────────────────────────────────────────

Is it the full page wrapper?
  └─ YES → Body element (automatic)

Is it a major page section?
  └─ YES → Section element
           Class: section_[name]

Is it a horizontal content container?
  └─ YES → Container or Div Block
           Container if needs max-width
           Div Block for custom width

Is it a grid of items?
  └─ YES → Grid or Flexbox
           Grid: Fixed columns/rows
           Flexbox: Dynamic wrapping

Is it text content?
  └─ Heading → Heading (select H1-H6)
  └─ Paragraph → Paragraph
  └─ Mixed → Rich Text
  └─ Label → Text Block

Is it interactive?
  └─ Navigation → Link Block or Button
  └─ Form → Form Block + Form elements
  └─ Accordion → Native Webflow component

Is it media?
  └─ Photo → Image
  └─ Video → Video or Embed
  └─ Background → Div with BG image

Is it from CMS?
  └─ List → Collection List
  └─ Single → Collection Page elements
```

### Webflow-Specific Elements

```
WEBFLOW NATIVE COMPONENTS
────────────────────────────────────────────────────────────────

Navigation
  └─ Navbar (includes mobile menu behavior)
  └─ Contains: Brand, Nav Menu, Nav Button

Slider
  └─ Slider component (with arrows, nav)
  └─ Contains: Slide elements

Tabs
  └─ Tabs component
  └─ Contains: Tabs Menu, Tabs Content, Tab Link, Tab Pane

Accordion (via Interactions)
  └─ Div Block structure + IX2
  └─ Contains: Trigger, Content

Lightbox
  └─ Lightbox Link + Lightbox Media
  └─ Built-in gallery behavior

Forms
  └─ Form Block
  └─ Contains: Input, Textarea, Select, Checkbox, Radio, Submit

Collection List
  └─ CMS content repeater
  └─ Contains: Collection Item wrapper

Dynamic content
  └─ Bound to CMS fields on Collection Pages
```

---

## Framework 6: Element Tree JSON Schema

### Output Format for Wireframes

```json
{
  "page": "homepage",
  "url": "/",
  "target_awareness": "Solution-Aware",
  "source_brief": "page_briefs.json",

  "sections": [
    {
      "section_id": "hero",
      "section_name": "Hero Section",
      "purpose": "Primary value proposition and CTA",

      "webflow_element": "Section",
      "class": "section_hero",

      "responsive": {
        "desktop": "2-column layout",
        "tablet": "Stacked, content first",
        "mobile": "Stacked, reduced spacing"
      },

      "children": [
        {
          "element": "Div Block",
          "class": "padding-global",
          "children": [
            {
              "element": "Container",
              "class": "container-large",
              "children": [
                {
                  "element": "Div Block",
                  "class": "padding-section-large",
                  "children": [
                    {
                      "element": "Div Block",
                      "class": "hero_component",
                      "layout": {
                        "type": "grid",
                        "columns": 2,
                        "gap": "48px"
                      },
                      "children": [
                        {
                          "element": "Div Block",
                          "class": "hero-content",
                          "children": [
                            {
                              "element": "Heading",
                              "tag": "h1",
                              "class": "heading-style-h1",
                              "content_slot": "hero_headline",
                              "content_direction": "[From ICP: Primary pain point solution]",
                              "cms_binding": null
                            },
                            {
                              "element": "Paragraph",
                              "class": "text-size-regular hero-description",
                              "content_slot": "hero_subheadline",
                              "content_direction": "[From ICP: Supporting value proposition]",
                              "cms_binding": null
                            },
                            {
                              "element": "Div Block",
                              "class": "hero-cta-wrapper",
                              "children": [
                                {
                                  "element": "Link Block",
                                  "class": "button-primary",
                                  "content_slot": "primary_cta",
                                  "content_direction": "[From page brief: Primary CTA]",
                                  "link_to": "/contact"
                                },
                                {
                                  "element": "Link Block",
                                  "class": "button-secondary",
                                  "content_slot": "secondary_cta",
                                  "content_direction": "[From page brief: Secondary CTA]",
                                  "link_to": "/learn-more"
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "element": "Div Block",
                          "class": "hero-image-wrapper",
                          "children": [
                            {
                              "element": "Image",
                              "class": "hero-image",
                              "content_slot": "hero_image",
                              "alt_direction": "[Describe primary offering in action]",
                              "cms_binding": null
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ],

  "cms_collections_referenced": [],

  "animation_opportunities": [
    {
      "element": "heading-style-h1",
      "suggestion": "Fade in from bottom on scroll into view",
      "implementation": "Webflow IX2 or GSAP"
    }
  ],

  "accessibility_notes": [
    "Ensure hero image has descriptive alt text",
    "CTAs must have clear focus states",
    "Heading hierarchy must be semantic"
  ]
}
```

---

## Framework 7: Webflow API Element IDs

### Element Type Mapping for API

When using Webflow Designer API via MCP tools:

```
WEBFLOW ELEMENT BUILDER TYPES
────────────────────────────────────────────────────────────────

Container      → "Container"
Section        → "Section"
Div Block      → "DivBlock"
Heading        → "Heading" (with set_heading_level: 1-6)
Paragraph      → "Paragraph"
Text Block     → "TextBlock"
Button         → "Button" (with set_link)
Text Link      → "TextLink" (with set_link)
Link Block     → "LinkBlock" (with set_link)
Image          → "Image" (with set_image_asset)
DOM Element    → "DOM" (with set_dom_config for span, code, etc.)
```

### MCP Tool Integration Notes

```
ELEMENT CREATION PATTERN
────────────────────────────────────────────────────────────────

1. Get current page
   → de_page_tool: get_current_page

2. Get parent element
   → element_tool: get_all_elements

3. Create element
   → element_builder: with element_schema

4. Apply styles
   → style_tool: create_style or get_styles + apply

5. Set text/images
   → element_tool: set_text, set_image_asset, set_link
```

---

## Usage Guidelines

### When to Use This Skill

1. **After `/strategy`** - When page briefs exist and need element planning
2. **Before `/vibe`** - To inform React component structure
3. **During `/wireframe`** - Primary skill for wireframe generation
4. **Before `/push-to-webflow`** - To plan exact element structure

### Quality Checklist

Before completing element planning:

- [ ] Every section maps to page brief
- [ ] Client-First naming is consistent
- [ ] CMS bindings are identified
- [ ] Responsive behavior is specified
- [ ] Content slots are documented
- [ ] Animation opportunities noted
- [ ] Accessibility considered

### Anti-Patterns to Avoid

```
DO NOT:
────────────────────────────────────────────────────────────────
❌ Use Webflow-generated class names (w-1, div-block-23)
❌ Create deeply nested structures (5+ levels)
❌ Mix naming conventions (BEM + Client-First)
❌ Forget CMS binding markers
❌ Skip responsive planning
❌ Assume content without page brief reference

INSTEAD:
────────────────────────────────────────────────────────────────
✓ Use semantic Client-First names
✓ Keep nesting to 4 levels max
✓ Follow Client-First exclusively
✓ Mark every CMS-bound field
✓ Define all breakpoints
✓ Reference page brief for all content
```
