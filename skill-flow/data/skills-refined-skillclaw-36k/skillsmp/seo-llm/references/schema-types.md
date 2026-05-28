# Schema.org Types

## Most Common Types

### Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Optimize for SEO in 2024",
  "description": "Complete guide to modern SEO techniques",
  "image": "https://example.com/image.jpg",
  "author": {
    "@type": "Person",
    "name": "Jane Doe",
    "url": "https://example.com/authors/jane"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Inc",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/seo-guide"
  }
}
```

### Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Wireless Headphones",
  "image": [
    "https://example.com/photos/1.jpg",
    "https://example.com/photos/2.jpg"
  ],
  "description": "High-quality wireless headphones with noise cancellation",
  "sku": "WH-1000XM5",
  "brand": {
    "@type": "Brand",
    "name": "TechBrand"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product/headphones",
    "priceCurrency": "USD",
    "price": 349.99,
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2024-12-31",
    "itemCondition": "https://schema.org/NewCondition"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.5,
    "reviewCount": 127
  },
  "review": [{
    "@type": "Review",
    "author": {
      "@type": "Person",
      "name": "John"
    },
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": 5
    },
    "reviewBody": "Excellent sound quality!"
  }]
}
```

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example",
    "https://github.com/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service",
    "availableLanguage": ["English", "Spanish"]
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94105",
    "addressCountry": "US"
  }
}
```

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Joe's Pizza",
  "image": "https://example.com/joespizza.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "456 Oak Ave",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10001",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "url": "https://joespizza.com",
  "telephone": "+1-555-987-6543",
  "priceRange": "$$",
  "servesCuisine": ["Italian", "Pizza"],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "11:00",
    "closes": "22:00"
  }]
}
```

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is Schema.org?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Schema.org is a collaborative vocabulary for structured data on the web."
    }
  }, {
    "@type": "Question",
    "name": "Why use structured data?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Structured data helps search engines understand your content better, potentially leading to rich results in search."
    }
  }]
}
```

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Tie a Bow Tie",
  "description": "Learn to tie a perfect bow tie in 5 easy steps",
  "image": "https://example.com/bowtie.jpg",
  "totalTime": "PT5M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": 0
  },
  "supply": [{
    "@type": "HowToSupply",
    "name": "Bow tie"
  }],
  "step": [{
    "@type": "HowToStep",
    "name": "Cross the ends",
    "text": "Cross the longer end over the shorter end",
    "image": "https://example.com/step1.jpg"
  }, {
    "@type": "HowToStep",
    "name": "Loop and pull",
    "text": "Loop the longer end behind and pull through",
    "image": "https://example.com/step2.jpg"
  }]
}
```

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Home",
    "item": "https://example.com"
  }, {
    "@type": "ListItem",
    "position": 2,
    "name": "Products",
    "item": "https://example.com/products"
  }, {
    "@type": "ListItem",
    "position": 3,
    "name": "Headphones",
    "item": "https://example.com/products/headphones"
  }]
}
```

### Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Tech Conference 2024",
  "description": "Annual technology conference",
  "startDate": "2024-06-15T09:00",
  "endDate": "2024-06-17T18:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Convention Center",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "100 Convention Way",
      "addressLocality": "San Francisco",
      "addressRegion": "CA"
    }
  },
  "image": "https://example.com/conference.jpg",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/tickets",
    "price": 299,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2024-01-01"
  },
  "performer": {
    "@type": "Person",
    "name": "Keynote Speaker"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Tech Events Inc",
    "url": "https://techevents.com"
  }
}
```

### SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "MyApp",
  "operatingSystem": "iOS, Android",
  "applicationCategory": "ProductivityApplication",
  "offers": {
    "@type": "Offer",
    "price": 0,
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.7,
    "ratingCount": 5000
  }
}
```

## Validation

```bash
# Google Rich Results Test
https://search.google.com/test/rich-results

# Schema.org Validator
https://validator.schema.org/

# CLI validation
npx structured-data-testing-tool https://example.com
```

## Best Practices

| Practice | Why |
|----------|-----|
| Use JSON-LD | Easiest to implement and maintain |
| Include required properties | Eligibility for rich results |
| Use specific types | `Restaurant` over generic `LocalBusiness` |
| Keep data accurate | Must match visible page content |
| Test before deploying | Catch errors early |
