'use client';

// ===========================================
// JSON-LD SCHEMA COMPONENTS - SEO Structured Data
// JobPosting for Missions, Course/Event for Services
// ===========================================

export interface MissionJsonLdData {
    id: string;
    title: string;
    description?: string;
    createdAt?: string | Date;
    validUntil?: string | Date | null;
    establishmentName?: string;
    city?: string;
    postalCode?: string;
    hourlyRate?: number | null;
}

export interface ServiceJsonLdData {
    id: string;
    title: string;
    description?: string;
    createdAt?: string | Date;
    providerName?: string;
    city?: string;
    basePrice?: number | null;
    serviceType?: string;
    duration?: number | null;
    category?: string;
}

/**
 * JobPosting JSON-LD for Mission cards (SOS Renfort)
 * https://schema.org/JobPosting
 */
export function JobPostingJsonLd({ data }: { data: MissionJsonLdData }) {
    const datePosted = data.createdAt
        ? new Date(data.createdAt).toISOString()
        : new Date().toISOString();

    const validThrough = data.validUntil
        ? new Date(data.validUntil).toISOString()
        : undefined;

    const jsonLd: Record<string, unknown> = {
        '@context': 'https://schema.org',
        '@type': 'JobPosting',
        '@id': `https://sociopulse.fr/need/${data.id}`,
        title: data.title || 'Mission de renfort',
        description: data.description || data.title || 'Mission de renfort médico-social',
        datePosted,
        employmentType: 'TEMPORARY',
        industry: 'Healthcare',
        occupationalCategory: 'Healthcare Support Workers',
    };

    if (validThrough) {
        jsonLd.validThrough = validThrough;
    }

    if (data.establishmentName) {
        jsonLd.hiringOrganization = {
            '@type': 'Organization',
            name: data.establishmentName,
        };
    }

    if (data.city) {
        jsonLd.jobLocation = {
            '@type': 'Place',
            address: {
                '@type': 'PostalAddress',
                addressLocality: data.city,
                ...(data.postalCode && { postalCode: data.postalCode }),
                addressCountry: 'FR',
            },
        };
    }

    if (data.hourlyRate != null && data.hourlyRate > 0) {
        jsonLd.baseSalary = {
            '@type': 'MonetaryAmount',
            currency: 'EUR',
            value: {
                '@type': 'QuantitativeValue',
                value: data.hourlyRate,
                unitText: 'HOUR',
            },
        };
    }

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
    );
}

/**
 * Course JSON-LD for Workshop/Atelier services
 * https://schema.org/Course
 */
export function CourseJsonLd({ data }: { data: ServiceJsonLdData }) {
    const jsonLd: Record<string, unknown> = {
        '@context': 'https://schema.org',
        '@type': 'Course',
        '@id': `https://sociopulse.fr/offer/${data.id}`,
        name: data.title || 'Atelier',
        description: data.description || data.title || 'Atelier médico-social',
        provider: data.providerName
            ? {
                '@type': 'Person',
                name: data.providerName,
                ...(data.city && { address: { '@type': 'PostalAddress', addressLocality: data.city } }),
            }
            : undefined,
        ...(data.category && { courseCode: data.category }),
        inLanguage: 'fr',
    };

    if (data.basePrice != null && data.basePrice > 0) {
        jsonLd.offers = {
            '@type': 'Offer',
            price: data.basePrice,
            priceCurrency: 'EUR',
            availability: 'https://schema.org/InStock',
        };
    }

    if (data.duration) {
        jsonLd.timeRequired = `PT${data.duration}M`;
    }

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
    );
}

/**
 * Event JSON-LD for SocioLive/Video coaching sessions
 * https://schema.org/Event
 */
export function EventJsonLd({ data }: { data: ServiceJsonLdData }) {
    const jsonLd: Record<string, unknown> = {
        '@context': 'https://schema.org',
        '@type': 'Event',
        '@id': `https://sociopulse.fr/offer/${data.id}`,
        name: data.title || 'Session SocioLive',
        description: data.description || data.title || 'Session vidéo en direct',
        eventAttendanceMode: 'https://schema.org/OnlineEventAttendanceMode',
        eventStatus: 'https://schema.org/EventScheduled',
        organizer: data.providerName
            ? {
                '@type': 'Person',
                name: data.providerName,
            }
            : undefined,
        location: {
            '@type': 'VirtualLocation',
            url: `https://sociopulse.fr/offer/${data.id}`,
        },
        inLanguage: 'fr',
    };

    if (data.basePrice != null && data.basePrice > 0) {
        jsonLd.offers = {
            '@type': 'Offer',
            price: data.basePrice,
            priceCurrency: 'EUR',
            availability: 'https://schema.org/InStock',
            url: `https://sociopulse.fr/offer/${data.id}`,
        };
    }

    if (data.duration) {
        jsonLd.duration = `PT${data.duration}M`;
    }

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
    );
}
