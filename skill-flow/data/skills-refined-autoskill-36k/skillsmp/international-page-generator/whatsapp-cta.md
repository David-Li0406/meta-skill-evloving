# WhatsApp CTA Patterns

## Primary CTA Component

```tsx
// src/components/international/CountryWhatsAppCTA.tsx
'use client'

import { MessageCircle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { trackAndOpenWhatsApp } from '@/lib/whatsapp/tracking'
import { getCountryWhatsAppMessage } from '@/lib/international/whatsapp-messages'

interface CountryWhatsAppCTAProps {
  variant?: 'hero' | 'primary' | 'secondary' | 'inline' | 'floating'
  country: string
  message?: 'default' | 'booking' | 'courseEnquiry' | 'exam'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  className?: string
  children?: React.ReactNode
}

const variantStyles = {
  hero: 'bg-green-500 hover:bg-green-600 text-white shadow-xl hover:shadow-2xl',
  primary: 'bg-green-500 hover:bg-green-600 text-white shadow-lg',
  secondary: 'bg-white border-2 border-green-500 text-green-600 hover:bg-green-50',
  inline: 'bg-green-100 hover:bg-green-200 text-green-700',
  floating: 'bg-green-500 hover:bg-green-600 text-white shadow-2xl rounded-full',
}

const sizeStyles = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg',
  xl: 'px-10 py-5 text-xl',
}

export function CountryWhatsAppCTA({
  variant = 'primary',
  country,
  message = 'default',
  size = 'lg',
  className,
  children,
}: CountryWhatsAppCTAProps) {
  const whatsappMessage = getCountryWhatsAppMessage(country, message)

  const handleClick = async () => {
    await trackAndOpenWhatsApp({
      source: `international-${country}`,
      message: whatsappMessage,
      campaign: `country-landing-${country}`,
    })
  }

  return (
    <button
      onClick={handleClick}
      className={cn(
        'inline-flex items-center justify-center gap-3 font-semibold rounded-lg transition-all duration-200',
        'focus:outline-none focus:ring-4 focus:ring-green-500/30',
        'min-h-[48px]', // Touch-friendly
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
    >
      <MessageCircle className="w-6 h-6" />
      {children || 'Chat on WhatsApp'}
    </button>
  )
}
```

## Floating CTA Component

```tsx
// src/components/international/CountryFloatingCTA.tsx
'use client'

import { useState, useEffect } from 'react'
import { MessageCircle, X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { trackAndOpenWhatsApp } from '@/lib/whatsapp/tracking'
import { getCountryWhatsAppMessage } from '@/lib/international/whatsapp-messages'

interface CountryFloatingCTAProps {
  country: string
  showAfterScroll?: number
  pulseAnimation?: boolean
}

export function CountryFloatingCTA({
  country,
  showAfterScroll = 200,
  pulseAnimation = true,
}: CountryFloatingCTAProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsVisible(window.scrollY > showAfterScroll)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [showAfterScroll])

  const handleClick = async () => {
    await trackAndOpenWhatsApp({
      source: `floating-cta-${country}`,
      message: getCountryWhatsAppMessage(country, 'default'),
      campaign: `country-floating-${country}`,
    })
  }

  if (!isVisible) return null

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Expanded tooltip */}
      {isExpanded && (
        <div className="absolute bottom-16 right-0 bg-white rounded-lg shadow-xl p-4 w-64 mb-2 animate-fade-in">
          <button
            onClick={() => setIsExpanded(false)}
            className="absolute top-2 right-2 text-slate-400 hover:text-slate-600"
          >
            <X className="w-4 h-4" />
          </button>
          <p className="text-slate-800 font-medium mb-2">Need help?</p>
          <p className="text-slate-600 text-sm mb-3">
            Chat with us on WhatsApp for instant support.
          </p>
          <button
            onClick={handleClick}
            className="w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg text-sm font-semibold"
          >
            Start Chat
          </button>
        </div>
      )}

      {/* Floating button */}
      <button
        onClick={() => (isExpanded ? handleClick() : setIsExpanded(true))}
        className={cn(
          'w-14 h-14 bg-green-500 hover:bg-green-600 rounded-full shadow-2xl',
          'flex items-center justify-center text-white',
          'transition-all duration-200 hover:scale-110',
          pulseAnimation && 'animate-pulse-slow'
        )}
        aria-label="Chat on WhatsApp"
      >
        <MessageCircle className="w-7 h-7" />
      </button>

      {/* Notification badge */}
      <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-ping" />
      <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full" />
    </div>
  )
}
```

## Country-Specific WhatsApp Messages

```typescript
// src/lib/international/whatsapp-messages.ts

export interface CountryMessages {
  default: string
  booking: string
  courseEnquiry: string
  exam: string
}

export const countryWhatsAppMessages: Record<string, CountryMessages> = {
  us: {
    default: "Hi! I'm a student in the US interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (US timezone - EST/PST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for US students. Can you share details?",
    exam: 'Hi! I need help with AP Biology / MCAT preparation.',
  },
  uk: {
    default: "Hi! I'm a student in the UK interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (UK timezone - GMT/BST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for UK students. Can you share details?",
    exam: 'Hi! I need help with GCSE / A-Level / BMAT preparation.',
  },
  ca: {
    default: "Hi! I'm a student in Canada interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (Canadian timezone).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for Canadian students. Can you share details?",
    exam: 'Hi! I need help with provincial biology exams / MCAT preparation.',
  },
  au: {
    default: "Hi! I'm a student in Australia interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (Australian timezone - AEST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for Australian students. Can you share details?",
    exam: 'Hi! I need help with HSC / VCE / QCE Biology preparation.',
  },
  sg: {
    default: "Hi! I'm a student in Singapore interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (Singapore timezone - SGT).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for Singapore students. Can you share details?",
    exam: 'Hi! I need help with GCE O-Level / A-Level / Singapore Biology Olympiad preparation.',
  },
  ae: {
    default: "Hi! I'm a student in UAE interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (UAE timezone - GST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for UAE students. Can you share details?",
    exam: 'Hi! I need help with IGCSE / IB / American curriculum biology.',
  },
  ie: {
    default: "Hi! I'm a student in Ireland interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (Irish timezone - IST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for Irish students. Can you share details?",
    exam: 'Hi! I need help with Leaving Certificate Biology preparation.',
  },
  hk: {
    default: "Hi! I'm a student in Hong Kong interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (Hong Kong timezone - HKT).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for Hong Kong students. Can you share details?",
    exam: 'Hi! I need help with HKDSE / IGCSE / A-Level Biology preparation.',
  },
  nz: {
    default: "Hi! I'm a student in New Zealand interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (New Zealand timezone - NZST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for NZ students. Can you share details?",
    exam: 'Hi! I need help with NCEA Biology preparation.',
  },
  za: {
    default: "Hi! I'm a student in South Africa interested in biology tutoring.",
    booking: "Hi! I'd like to book a free demo class (South African timezone - SAST).",
    courseEnquiry:
      "Hi! I'm interested in your biology courses for South African students. Can you share details?",
    exam: 'Hi! I need help with NSC / IEB Biology preparation.',
  },
}

export function getCountryWhatsAppMessage(
  countryCode: string,
  messageType: keyof CountryMessages = 'default'
): string {
  const messages = countryWhatsAppMessages[countryCode]
  if (!messages) {
    return "Hi! I'm interested in online biology tutoring."
  }
  return messages[messageType]
}
```

## CTA Placement Guidelines

### Above the Fold (CRITICAL)

- Minimum 48px height
- Green background (#25D366 or #22c55e)
- White text
- Icon + text
- Response time indicator below

### Floating Button

- Fixed position: bottom-right
- 56px diameter
- Show after 200px scroll
- Pulse animation
- Notification badge

### Section CTAs

- After pricing section
- After testimonials
- Inline with content
- Can be secondary variant

### Exit Intent

- Modal overlay
- Discount offer
- WhatsApp as primary action
- Close button visible

## Tracking Parameters

Every WhatsApp click tracks:

- `source`: Page identifier (e.g., `international-us`)
- `message`: Message type used
- `campaign`: Marketing campaign
- `sessionId`: User session
- `page`: Current URL path
