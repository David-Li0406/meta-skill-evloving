# Contact Data Schema

## File Location

`src/lib/constants/contact.ts`

## TypeScript Interface

```typescript
export interface ContactInfo {
  email: string;
  linkedin: string;
  github: string;
  instagram: string;
  location: string;
}
```

## Field Descriptions

| Field     | Type   | Description                        | Example                                    |
| --------- | ------ | ---------------------------------- | ------------------------------------------ |
| email     | string | Primary email address              | `"huntercitation@gmail.com"`               |
| linkedin  | string | Full LinkedIn profile URL          | `"https://www.linkedin.com/in/dadanisme/"` |
| github    | string | Full GitHub profile URL            | `"https://github.com/dadanisme"`           |
| instagram | string | Full Instagram profile URL         | `"https://instagram.com/dadanisme"`        |
| location  | string | Geographic location (city/country) | `"Indonesia"`                              |

## Usage

The contact data is imported by the contact page (`src/app/contact/page.tsx`) and used to render contact cards with icons and links.

## URL Format Guidelines

- **LinkedIn**: Use full URL format `https://www.linkedin.com/in/username/`
- **GitHub**: Use full URL format `https://github.com/username`
- **Instagram**: Use full URL format `https://instagram.com/username`
- **Email**: Plain email address (no `mailto:` prefix)
