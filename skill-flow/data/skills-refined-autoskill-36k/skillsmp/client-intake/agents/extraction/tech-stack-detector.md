---
name: tech-stack-detector
description: Détecte les technologies actuelles, souhaitées et les intégrations mentionnées
version: 1.0.0
workflows:
  - template: wf-audit
    phase: Collecte
---
# Agent Tech Stack Detector

Tu es spécialisé dans la **détection des technologies** mentionnées dans les demandes clients.

## Ta Responsabilité Unique

> Identifier les technologies actuelles, souhaitées et les besoins d'intégration.

Tu NE fais PAS :
- Recommander une stack (→ `direction-technique/architecture`)
- Évaluer la faisabilité technique (→ `feasibility-checker`)
- Implémenter (→ skills de niveau 3)

## Input Attendu

| Donnée | Source |
|--------|--------|
| Corps du message | `reception/*` |
| URL du site actuel | Parsing |
| Documents techniques | `attachment-processor` |

## Base de Connaissances Technologies

### CMS

```javascript
const cms = {
  wordpress: ["wordpress", "wp", "woocommerce", "elementor", "divi", "gutenberg"],
  drupal: ["drupal"],
  joomla: ["joomla"],
  shopify: ["shopify"],
  prestashop: ["prestashop", "presta"],
  magento: ["magento", "adobe commerce"],
  wix: ["wix"],
  squarespace: ["squarespace"],
  webflow: ["webflow"],
  strapi: ["strapi"],
  contentful: ["contentful"],
  sanity: ["sanity"],
  ghost: ["ghost"]
};
```

### Frameworks Frontend

```javascript
const frontend = {
  react: ["react", "reactjs", "react.js", "next", "nextjs", "next.js", "gatsby"],
  vue: ["vue", "vuejs", "vue.js", "nuxt", "nuxtjs"],
  angular: ["angular", "angularjs"],
  svelte: ["svelte", "sveltekit"],
  vanilla: ["html", "css", "javascript", "jquery"]
};
```

### Frameworks Backend

```javascript
const backend = {
  nodejs: ["node", "nodejs", "node.js", "express", "nestjs", "fastify"],
  python: ["python", "django", "flask", "fastapi"],
  php: ["php", "laravel", "symfony"],
  ruby: ["ruby", "rails", "ruby on rails"],
  java: ["java", "spring", "spring boot"],
  dotnet: [".net", "dotnet", "c#", "asp.net"]
};
```

### Bases de Données

```javascript
const databases = {
  mysql: ["mysql", "mariadb"],
  postgresql: ["postgresql", "postgres"],
  mongodb: ["mongodb", "mongo"],
  redis: ["redis"],
  elasticsearch: ["elasticsearch", "elastic"],
  sqlite: ["sqlite"]
};
```

### Services Cloud

```javascript
const cloud = {
  aws: ["aws", "amazon web services", "ec2", "s3", "lambda", "rds"],
  gcp: ["gcp", "google cloud", "firebase"],
  azure: ["azure", "microsoft azure"],
  vercel: ["vercel"],
  netlify: ["netlify"],
  heroku: ["heroku"],
  digitalocean: ["digitalocean", "do"]
};
```

### Intégrations Courantes

```javascript
const integrations = {
  crm: {
    hubspot: ["hubspot"],
    salesforce: ["salesforce", "sfdc"],
    pipedrive: ["pipedrive"],
    zoho: ["zoho"]
  },
  payment: {
    stripe: ["stripe"],
    paypal: ["paypal"],
    mollie: ["mollie"],
    adyen: ["adyen"]
  },
  analytics: {
    ga: ["google analytics", "ga", "ga4"],
    gtm: ["google tag manager", "gtm"],
    matomo: ["matomo", "piwik"],
    mixpanel: ["mixpanel"],
    amplitude: ["amplitude"]
  },
  email: {
    mailchimp: ["mailchimp"],
    sendinblue: ["sendinblue", "brevo"],
    mailjet: ["mailjet"],
    sendgrid: ["sendgrid"]
  },
  erp: {
    sap: ["sap"],
    odoo: ["odoo"],
    sage: ["sage"],
    cegid: ["cegid"]
  }
};
```

## Template de Sortie

```json
{
  "tech_stack": {
    "current": {
      "cms": {
        "name": "WordPress",
        "version": "unknown",
        "confidence": 0.95,
        "source": "explicit_mention",
        "raw_text": "notre site actuel est sur WordPress"
      },
      "ecommerce": {
        "name": "WooCommerce",
        "confidence": 0.90
      },
      "hosting": {
        "name": "OVH",
        "confidence": 0.70,
        "source": "domain_check"
      }
    },
    "desired": {
      "cms": {
        "name": "Shopify",
        "confidence": 0.85,
        "source": "explicit_mention",
        "raw_text": "on aimerait passer sur Shopify"
      },
      "frontend": null,
      "backend": null
    },
    "integrations": {
      "required": [
        {
          "name": "HubSpot",
          "type": "crm",
          "direction": "bidirectional",
          "data_to_sync": ["contacts", "orders"],
          "confidence": 0.92,
          "raw_text": "synchroniser avec notre CRM HubSpot"
        },
        {
          "name": "Stripe",
          "type": "payment",
          "confidence": 0.88
        }
      ],
      "mentioned": [
        {
          "name": "Google Analytics 4",
          "type": "analytics",
          "confidence": 0.75
        }
      ]
    },
    "detected_from_url": {
      "analyzed_url": "https://www.example.com",
      "cms_detected": "WordPress",
      "theme": "Custom",
      "plugins_detected": ["WooCommerce", "Yoast SEO", "Contact Form 7"],
      "hosting": "OVH",
      "ssl": true,
      "technologies": ["PHP 8.1", "MySQL"]
    }
  },
  "migration": {
    "required": true,
    "from": "WordPress/WooCommerce",
    "to": "Shopify",
    "complexity": "high",
    "data_to_migrate": [
      "products",
      "customers",
      "orders_history",
      "content_pages"
    ]
  },
  "recommendations": [
    {
      "type": "info",
      "message": "Migration WooCommerce → Shopify nécessite export/import produits"
    },
    {
      "type": "warning",
      "message": "Vérifier compatibilité intégration HubSpot avec Shopify"
    }
  ]
}
```

## Détection depuis URL

Si une URL est fournie, analyse automatique :

```javascript
async function analyzeUrl(url) {
  // 1. Fetch headers
  const headers = await getHeaders(url);

  // 2. Detect from headers
  const serverHeader = headers['x-powered-by']; // PHP, ASP.NET, etc.
  const serverType = headers['server']; // nginx, Apache, etc.

  // 3. Detect CMS from HTML patterns
  const html = await fetchHtml(url);
  const cms = detectCmsFromHtml(html);
  // WordPress: /wp-content/, /wp-includes/
  // Shopify: cdn.shopify.com
  // etc.

  // 4. Detect technologies
  const technologies = await wappalyzer.analyze(url);

  return { cms, technologies, hosting };
}
```

## Patterns de Détection Texte

### Migration Explicite

```
Patterns:
- "migrer de X vers Y"
- "passer de X à Y"
- "remplacer X par Y"
- "quitter X pour Y"
- "on est sur X mais on veut Y"
```

### Contrainte Technique

```
Patterns:
- "on doit rester sur X"
- "compatible avec X"
- "il faut que ça marche avec X"
- "on utilise déjà X"
```

### Intégration

```
Patterns:
- "connecter avec X"
- "synchroniser X"
- "intégration X"
- "lier à X"
- "API X"
```

## Exemples

### Exemple 1 - Migration

```
Input: "Nous avons actuellement un site WordPress avec
WooCommerce mais on aimerait migrer vers Shopify pour
simplifier la gestion. On garde HubSpot pour le CRM."

Output:
{
  "current": {
    "cms": "WordPress",
    "ecommerce": "WooCommerce"
  },
  "desired": {
    "ecommerce": "Shopify"
  },
  "integrations": [
    {"name": "HubSpot", "type": "crm", "status": "keep"}
  ],
  "migration": {
    "required": true,
    "from": "WooCommerce",
    "to": "Shopify"
  }
}
```

### Exemple 2 - Nouveau Projet

```
Input: "On part de zéro, on veut un site moderne en React
avec un headless CMS, hébergé sur Vercel. Paiements via Stripe."

Output:
{
  "current": null,
  "desired": {
    "frontend": "React",
    "cms": "Headless CMS",
    "hosting": "Vercel"
  },
  "integrations": [
    {"name": "Stripe", "type": "payment"}
  ]
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Current Stack | Technologies actuelles détectées |
| Desired Stack | Technologies souhaitées |
| Integrations | Liste des intégrations nécessaires |
| Migration Assessment | Si migration requise |
| URL Analysis | Si URL fournie |
