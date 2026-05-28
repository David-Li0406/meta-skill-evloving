# Section Definitions

This file defines the rule categories for Sanity best practices. Rules are automatically assigned to sections based on their filename prefix.

---

## 1. GROQ Performance (groq)
Query optimization, index usage, and performance patterns. Covers optimizable filters, avoiding joins in filters, cursor pagination, and projection best practices.

## 2. Schema Design (schema)
Content modeling philosophy, field patterns, references vs objects, validation, and safe deprecation. Foundation for maintainable, scalable content architecture.

## 3. Visual Editing (visual)
Presentation Tool setup, Content Source Maps (Stega), overlays, and live preview configuration. Critical for editor experience and real-time content editing.

## 4. Images (image)
Image schema with hotspots, URL builder patterns, LQIP (blur placeholders), and Next.js Image integration.

## 5. Portable Text (pte)
Rich text rendering, custom block types, mark components, and presentation queries for live editing.

## 6. Page Builder (pagebuilder)
Flexible page composition with block arrays, component rendering patterns, and TypeScript typing.

## 7. Studio Configuration (studio)
Desk structure customization, singleton patterns, document views, and navigation organization.

## 8. TypeGen (typegen)
TypeScript type generation from schema and queries, configuration patterns, and workflow integration.

## 9. Localization (i18n)
Document-level and field-level internationalization, locale management, and querying patterns.

## 10. Migration (migration)
Content import from HTML/Markdown, image handling, and schema validation during migrations.
