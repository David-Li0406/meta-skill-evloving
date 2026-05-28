---
name: international-page-generator
description: Generates country-specific landing pages for international biology tutoring with WhatsApp CTA priority. Supports 10 markets (US, UK, CA, AU, SG, AE, IE, HK, NZ, ZA).
---

# International Page Generator Skill

## Purpose

Generate high-converting, SEO-optimized landing pages for international students seeking biology tutoring. Each page is customized for the country's exam systems, pricing, and timezone.

## Target Countries

| Code | Country        | Exam Systems                  | Currency |
| ---- | -------------- | ----------------------------- | -------- |
| us   | United States  | AP Biology, SAT Biology, MCAT | USD      |
| uk   | United Kingdom | GCSE, A-Level, BMAT, UCAT     | GBP      |
| ca   | Canada         | Provincial Bio, MCAT          | CAD      |
| au   | Australia      | HSC, VCE, QCE, ATAR           | AUD      |
| sg   | Singapore      | GCE O/A-Level, IP, SBO        | SGD      |
| ae   | UAE/Dubai      | IGCSE, IB, American           | AED      |
| ie   | Ireland        | Leaving Certificate           | EUR      |
| hk   | Hong Kong      | HKDSE, IGCSE, A-Level         | HKD      |
| nz   | New Zealand    | NCEA                          | NZD      |
| za   | South Africa   | NSC/Matric, IEB               | ZAR      |

## Page Structure (10 Sections)

1. **CountryHero** - Hero with country flag, headline, subheadline
2. **WhatsApp Primary CTA** - Prominent green button (ABOVE FOLD - CRITICAL)
3. **CountryExamSystems** - Relevant exams grid
4. **CourseCategories** - High School, Pre-Med, Olympiad, Test Prep
5. **WhatsApp Floating CTA** - Persistent floating button
6. **CountryPricing** - Pricing in local currency
7. **WhyChooseUs** - Differentiators for international students
8. **CountryTestimonials** - Success stories from that country/region
9. **CountryFAQ** - Country-specific questions
10. **Final WhatsApp CTA** - Full-width conversion section

## WhatsApp CTA Priority (CRITICAL)

WhatsApp is the PRIMARY conversion action. Implementation hierarchy:

1. **Hero CTA** - 48px+ height, green (#25D366), above fold
2. **Floating Button** - Fixed bottom-right, visible after 200px scroll
3. **Section CTAs** - After pricing, after testimonials
4. **Exit Intent** - WhatsApp offer on exit attempt
5. **Footer** - Secondary WhatsApp link

### WhatsApp Message Templates

Each country has customized messages. See `whatsapp-cta.md` for full templates.

```typescript
// Example US messages
{
  default: "Hi! I'm a student in the US interested in biology tutoring.",
  apBiology: "Hi! I need help with AP Biology preparation.",
  mcat: "Hi! I'm preparing for MCAT and need biology tutoring.",
  booking: "Hi! I'd like to book a free demo class (US timezone)."
}
```

## Pricing Structure

| Type                       | USD        | Conversion         |
| -------------------------- | ---------- | ------------------ |
| Small Group (3-5 students) | $40/hr     | Apply country rate |
| One-on-One                 | $70-120/hr | Apply country rate |

See `pricing-calculator.py` for currency conversions.

## SEO Requirements

Every country page MUST have:

1. **Unique Title**: `Online Biology Tutoring for {Country} Students | Cerebrum Academy`
2. **Unique Description**: Include exam systems and pricing
3. **Canonical URL**: `https://cerebrumacademy.com/international/{code}/`
4. **Hreflang Tags**: All 10 countries + x-default
5. **Structured Data**: EducationalOrganization with areaServed

See `seo-checklist.md` for full requirements.

## Component Dependencies

```
src/components/international/
├── CountrySelector.tsx       # Country picker modal
├── CountryHero.tsx           # Hero section
├── CountryExamSystems.tsx    # Exam systems grid
├── CountryCourseGrid.tsx     # Course cards
├── CountryPricing.tsx        # Pricing display
├── CountryTestimonials.tsx   # Testimonials
├── CountryFAQ.tsx            # FAQ accordion
├── CountryWhatsAppCTA.tsx    # Primary WhatsApp button
├── CountryFloatingCTA.tsx    # Floating WhatsApp
└── CountryTrustSignals.tsx   # Trust indicators
```

## Design System Compliance

Follow Cerebrum design system:

- **Primary CTA**: Green (#22c55e) or Yellow (#facc15)
- **WhatsApp**: Green (#25D366)
- **Hero Background**: Slate gradient (slate-900 to slate-800)
- **Cards**: White, rounded-xl, shadow-xl
- **Mobile-first**: 375px → 768px → 1280px

## Usage Examples

```bash
# Generate single country page
npm run agent "Create UK landing page with GCSE, A-Level, BMAT focus and GBP pricing"

# Generate all pages
npm run agent "Generate landing pages for all 10 international markets"

# Update testimonials
npm run agent "Add Hong Kong-specific testimonials to the HK landing page"
```

## Files Referenced

- `country-template.md` - Full page template
- `whatsapp-cta.md` - WhatsApp CTA patterns
- `seo-checklist.md` - SEO requirements
- `pricing-calculator.py` - Currency conversion
