# Country Landing Page Template

## Page Component Structure

```tsx
// src/app/international/[country]/page.tsx

import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getCountryConfig, SUPPORTED_COUNTRIES } from '@/lib/international/countries'
import { CountryHero } from '@/components/international/CountryHero'
import { CountryWhatsAppCTA } from '@/components/international/CountryWhatsAppCTA'
import { CountryExamSystems } from '@/components/international/CountryExamSystems'
import { CountryCourseGrid } from '@/components/international/CountryCourseGrid'
import { CountryPricing } from '@/components/international/CountryPricing'
import { CountryTestimonials } from '@/components/international/CountryTestimonials'
import { CountryFAQ } from '@/components/international/CountryFAQ'
import { CountryFloatingCTA } from '@/components/international/CountryFloatingCTA'
import { CountryTrustSignals } from '@/components/international/CountryTrustSignals'

interface Props {
  params: Promise<{ country: string }>
}

// Generate static params for all 10 countries
export async function generateStaticParams() {
  return SUPPORTED_COUNTRIES.map((code) => ({ country: code }))
}

// Generate metadata per country
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { country } = await params
  const config = getCountryConfig(country)

  if (!config) return {}

  return {
    title: `Online Biology Tutoring for ${config.name} Students | Cerebrum Academy`,
    description: `Expert biology tutoring for ${config.examSystems.slice(0, 3).join(', ')}. Small group from ${config.currency.symbol}${config.pricing.smallGroup}/hr. Free demo class available.`,
    keywords: [
      `biology tutor ${config.name}`,
      `online biology classes ${config.name}`,
      ...config.examSystems.map((exam) => `${exam} tutoring`),
    ],
    alternates: {
      canonical: `https://cerebrumacademy.com/international/${country}/`,
    },
    openGraph: {
      title: `Biology Tutoring for ${config.name} Students`,
      description: `Expert ${config.examSystems[0]} tutoring. Small group from ${config.currency.symbol}${config.pricing.smallGroup}/hr.`,
      locale: config.hreflang.replace('-', '_'),
      type: 'website',
    },
  }
}

export default async function CountryPage({ params }: Props) {
  const { country } = await params
  const config = getCountryConfig(country)

  if (!config) {
    notFound()
  }

  return (
    <main className="min-h-screen">
      {/* 1. Hero Section */}
      <CountryHero country={config} />

      {/* 2. Primary WhatsApp CTA (Above Fold) */}
      <section className="py-8 bg-gradient-to-r from-green-50 to-teal-50">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <CountryWhatsAppCTA
            variant="hero"
            country={country}
            message="booking"
            size="xl"
            className="w-full md:w-auto"
          />
          <p className="mt-3 text-sm text-slate-600">Average response time: &lt; 2 minutes</p>
        </div>
      </section>

      {/* 3. Exam Systems Grid */}
      <CountryExamSystems country={config} />

      {/* 4. Course Categories */}
      <CountryCourseGrid country={config} />

      {/* 5. Trust Signals */}
      <CountryTrustSignals country={config} />

      {/* 6. Pricing Section */}
      <CountryPricing country={config} />

      {/* 7. Testimonials */}
      <CountryTestimonials country={config} />

      {/* 8. FAQ Section */}
      <CountryFAQ country={config} />

      {/* 9. Final CTA */}
      <section className="py-16 bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Excel in Biology?
          </h2>
          <p className="text-lg text-slate-300 mb-8">
            Join students across {config.name} who are achieving their academic goals.
          </p>
          <CountryWhatsAppCTA
            variant="hero"
            country={country}
            message="booking"
            size="xl"
            className="bg-green-500 hover:bg-green-600"
          />
        </div>
      </section>

      {/* 10. Floating WhatsApp Button */}
      <CountryFloatingCTA country={country} />
    </main>
  )
}
```

## Hero Section Template

```tsx
// CountryHero.tsx

interface CountryHeroProps {
  country: CountryConfig
}

export function CountryHero({ country }: CountryHeroProps) {
  return (
    <section className="relative py-20 md:py-28 bg-gradient-to-br from-slate-900 to-slate-800 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-green-500 rounded-full blur-3xl" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-blue-500 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4">
        <div className="text-center">
          {/* Country Flag */}
          <span className="text-6xl md:text-7xl mb-6 block">{country.flag}</span>

          {/* Headline */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
            Expert Biology Tutoring for <span className="text-green-400">{country.name}</span>{' '}
            Students
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto">
            Master {country.examSystems.slice(0, 3).join(', ')} with personalized online tutoring.
            Available in your timezone ({country.timezone}).
          </p>

          {/* Pricing Badge */}
          <div className="inline-flex items-center gap-4 bg-white/10 backdrop-blur-sm rounded-full px-6 py-3 mb-8">
            <span className="text-slate-300">Small Group</span>
            <span className="text-2xl font-bold text-green-400">
              {country.currency.symbol}
              {country.pricing.smallGroup}/hr
            </span>
            <span className="text-slate-500">|</span>
            <span className="text-slate-300">1-on-1</span>
            <span className="text-2xl font-bold text-yellow-400">
              from {country.currency.symbol}
              {country.pricing.oneOnOneMin}/hr
            </span>
          </div>

          {/* Primary CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <CountryWhatsAppCTA variant="hero" country={country.code} message="booking" size="xl" />
            <a
              href="#pricing"
              className="px-8 py-4 text-lg font-semibold text-white border-2 border-white/30 rounded-lg hover:bg-white/10 transition-colors"
            >
              View Pricing
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
```

## Exam Systems Section Template

```tsx
// CountryExamSystems.tsx

export function CountryExamSystems({ country }: { country: CountryConfig }) {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-slate-900 mb-4">
          We Cover All {country.name} Exam Systems
        </h2>
        <p className="text-lg text-slate-600 text-center mb-12 max-w-2xl mx-auto">
          Our expert tutors specialize in the curricula and exam formats specific to {country.name}.
        </p>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {country.examSystems.map((exam) => (
            <div
              key={exam}
              className="bg-gradient-to-br from-green-50 to-teal-50 rounded-xl p-6 text-center hover:shadow-lg transition-shadow"
            >
              <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckIcon className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-slate-900">{exam}</h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

## Pricing Section Template

```tsx
// CountryPricing.tsx

export function CountryPricing({ country }: { country: CountryConfig }) {
  const plans = [
    {
      name: 'Small Group',
      description: '3-5 students per session',
      price: country.pricing.smallGroup,
      features: [
        'Live interactive sessions',
        'Collaborative learning',
        'Peer discussions',
        'Recorded sessions',
        'WhatsApp support',
      ],
      popular: false,
    },
    {
      name: 'One-on-One',
      description: 'Personalized attention',
      price: country.pricing.oneOnOneMin,
      priceMax: country.pricing.oneOnOneMax,
      features: [
        'Fully personalized curriculum',
        'Flexible scheduling',
        'Exam-focused preparation',
        'Progress tracking',
        'Priority WhatsApp support',
        'Mock tests & feedback',
      ],
      popular: true,
    },
  ]

  return (
    <section id="pricing" className="py-16 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-5xl mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-slate-900 mb-4">
          Transparent Pricing for {country.name}
        </h2>
        <p className="text-lg text-slate-600 text-center mb-12">
          All prices in {country.currency.code}. No hidden fees.
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative bg-white rounded-2xl p-8 shadow-xl border-2 ${
                plan.popular ? 'border-green-500' : 'border-slate-200'
              }`}
            >
              {plan.popular && (
                <span className="absolute -top-4 left-1/2 -translate-x-1/2 bg-green-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                  Most Popular
                </span>
              )}

              <h3 className="text-2xl font-bold text-slate-900 mb-2">{plan.name}</h3>
              <p className="text-slate-600 mb-6">{plan.description}</p>

              <div className="mb-6">
                <span className="text-4xl font-bold text-slate-900">
                  {country.currency.symbol}
                  {plan.price}
                </span>
                {plan.priceMax && (
                  <span className="text-slate-600">
                    - {country.currency.symbol}
                    {plan.priceMax}
                  </span>
                )}
                <span className="text-slate-600">/hour</span>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3">
                    <CheckCircleIcon className="w-5 h-5 text-green-500" />
                    <span className="text-slate-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <CountryWhatsAppCTA
                variant={plan.popular ? 'primary' : 'secondary'}
                country={country.code}
                message="courseEnquiry"
                size="lg"
                className="w-full"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

## Mobile Responsiveness Checklist

- [ ] Hero text readable on 375px
- [ ] Pricing cards stack on mobile
- [ ] Exam system grid: 2 cols on mobile, 4 on desktop
- [ ] WhatsApp buttons: 48px minimum touch target
- [ ] No horizontal scroll on any breakpoint
- [ ] Floating CTA doesn't overlap footer
