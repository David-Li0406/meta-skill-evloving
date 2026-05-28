---
name: website-setup
description: Interactive website customization wizard. Gathers user information and configures template files. Use when user says "set up", "configure", "get started", "customize", or wants to personalize the template.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Website Setup Workflow

Guide users through configuring their website with zero coding.

## Phase 1: Information Gathering

Use AskUserQuestion to collect information in batches of 2-3 questions.

### Batch 1: Identity

Ask the user:
- **Site Name**: "What's the name of your website?" (e.g., "My Portfolio", "Acme Corp")
- **Domain**: "What's your domain name?" (e.g., "example.com" - without https://)

### Batch 2: Content

Ask the user:
- **Headline**: "What's your main headline or tagline?" (displays prominently in hero)
- **Description**: "Brief description for search engines?" (1-2 sentences for SEO)

### Batch 3: Branding

Ask the user with options:
- **Primary Color**: "What's your primary accent color?"
  - Blue (#2563eb) - Professional, trustworthy
  - Purple (#7c3aed) - Creative, innovative
  - Teal (#0d9488) - Fresh, modern
  - Amber (#d97706) - Warm, energetic
  - Custom hex code
- **Author**: "Your name or company name?" (for copyright and meta author)

---

## Phase 2: Template Customization

After gathering all information, update the template files:

### 1. Update `index.html`

Replace these elements with user values:

```html
<!-- Title -->
<title>{Site Name} | {Headline}</title>

<!-- Meta tags -->
<meta name="description" content="{Description}">
<meta name="author" content="{Author}">

<!-- Open Graph -->
<meta property="og:url" content="https://{Domain}/">
<meta property="og:title" content="{Site Name}">
<meta property="og:description" content="{Description}">

<!-- Twitter -->
<meta name="twitter:url" content="https://{Domain}/">
<meta name="twitter:title" content="{Site Name}">
<meta name="twitter:description" content="{Description}">

<!-- Canonical -->
<link rel="canonical" href="https://{Domain}/">

<!-- Content -->
<a class="nav-logo">{Site Name}</a>
<h1 class="hero-tagline">{Headline}</h1>
<p class="hero-subtext">{Description}</p>
```

### 2. Update `styles/variables.css`

Set the accent color:

```css
--color-accent: {Primary Color};
```

### 3. Update `.github/workflows/deploy.yml`

Set the domain:

```yaml
env:
  DOMAIN: {Domain}
```

---

## Phase 3: Preview

After customization:

1. Run the local development server:
   ```bash
   just serve
   ```

2. Inform the user:
   > Your website is ready for preview at http://localhost:5174
   >
   > Take a look and let me know if you'd like any changes.

---

## Phase 4: Next Steps

Offer the user options:

- "Would you like to **deploy** your website to SiteGround?"
- "Want to **change colors** or make other adjustments?"
- "Ready to **preview** in the browser?"

If they want to deploy, suggest the `/deployment-guide` skill.
