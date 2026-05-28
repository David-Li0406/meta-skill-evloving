---
name: optimisation-frontend
description: Objectifs et politiques d'optimisation des performances frontend (Niveau POURQUOI)
workflows:
  - template: wf-evolution
    phase: Réalisation
---
# Politique de Performance Frontend

Tu définis les **objectifs et standards** de performance frontend.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les OBJECTIFS de performance et les standards à atteindre
> **Ce que tu ne fais pas** : Implémenter les optimisations (code, config)
>
> → Process d'optimisation : `web-dev-process/agents/testing/performance`
> → Implémentation React/Next : Skills frontend spécialisés
> → Implémentation WordPress : `wordpress-gutenberg-expert/agents/performance/*`

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi ces cibles ? UX et SEO"                            │
│  → "Standards : LCP < 2.5s, FID < 100ms, CLS < 0.1"             │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi optimiser ? Images, bundle, fonts, cache"              │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (frameworks spécifiques)                    │
│  → "Code : lazy(), preload, srcset, service worker..."          │
└─────────────────────────────────────────────────────────────────┘
```
---
## Objectifs de Performance

### Core Web Vitals - Cibles

| Métrique | Bon | À améliorer | Mauvais | Impact |
|----------|-----|-------------|---------|--------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4s | > 4s | UX + SEO |
| **FID** (First Input Delay) | < 100ms | 100ms - 300ms | > 300ms | Interactivité |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms | Réactivité |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 | Stabilité visuelle |

### Autres Métriques Cibles

| Métrique | Cible | Justification |
|----------|-------|---------------|
| **TTFB** | < 600ms | Réponse serveur |
| **FCP** (First Contentful Paint) | < 1.8s | Feedback visuel initial |
| **TTI** (Time to Interactive) | < 3.8s | Page utilisable |
| **Speed Index** | < 3.4s | Progression perçue |

### Budget Performance

| Ressource | Budget | Justification |
|-----------|--------|---------------|
| **JavaScript total** | < 200KB gzippé | Temps de parse/exec |
| **CSS total** | < 50KB gzippé | Render blocking |
| **Images above-fold** | < 200KB | LCP |
| **Fonts** | < 100KB | FOIT/FOUT |
| **Total page** | < 1.5MB | Expérience mobile |
---
## Politiques de Performance

### 1. Politique d'Images

| Aspect | Politique |
|--------|-----------|
| **Format** | WebP/AVIF obligatoire (avec fallback) |
| **Compression** | Quality 75-85 pour JPEG/WebP |
| **Responsive** | srcset obligatoire pour images > 300px |
| **Lazy loading** | Obligatoire pour images below-fold |
| **Above-fold** | Preload + eager loading |

### 2. Politique de JavaScript

| Aspect | Politique |
|--------|-----------|
| **Code splitting** | Obligatoire par route |
| **Tree shaking** | Build prod uniquement |
| **Third-party** | Defer/async obligatoire |
| **Bundle critique** | < 50KB pour first paint |
| **Long tasks** | Aucune tâche > 50ms sur main thread |

### 3. Politique de CSS

| Aspect | Politique |
|--------|-----------|
| **Critical CSS** | Inline pour above-fold |
| **Non-critical** | Async loading |
| **Unused CSS** | Purge en production |
| **Frameworks** | Utility-first préféré (tree-shaking) |

### 4. Politique de Fonts

| Aspect | Politique |
|--------|-----------|
| **Format** | WOFF2 uniquement (support universel) |
| **Subset** | Caractères utilisés uniquement |
| **Loading** | font-display: swap |
| **Preload** | Fonts critiques uniquement |
| **Quantité** | Max 2 familles, 4 poids |

### 5. Politique de Cache

| Ressource | Cache Strategy | TTL |
|-----------|----------------|-----|
| **Assets versionnés** | Cache immutable | 1 an |
| **HTML** | Must-revalidate | 1 heure |
| **API dynamique** | No-cache ou SWR | Variable |
| **Images CDN** | Public | 1 mois |
---
## Questions de Clarification

Avant d'optimiser :

### Contexte
- ❓ Quel est l'audience cible ? (mobile, desktop, marchés)
- ❓ Quelles sont les connexions types ? (4G, fibre)
- ❓ Y a-t-il un score Lighthouse actuel ?

### Priorités
- ❓ Quel est l'objectif principal ? (SEO, conversion, UX)
- ❓ Quelles pages sont critiques ? (accueil, landing, checkout)
- ❓ Budget pour CDN/infrastructure ?

### Contraintes
- ❓ Y a-t-il des third-party non négociables ? (analytics, chat)
- ❓ Contraintes de design ? (fonts custom, animations)
- ❓ Support navigateurs ? (IE11, Safari ancien)
---
## Checklist par Phase

### Phase Conception

- [ ] Budget performance défini
- [ ] Métriques cibles validées
- [ ] Fonts limitées (max 2 familles)
- [ ] Third-party inventoriés et justifiés

### Phase Développement

- [ ] Images optimisées (format, compression, srcset)
- [ ] Lazy loading implémenté
- [ ] Code splitting configuré
- [ ] Critical CSS identifié

### Phase Review

- [ ] Lighthouse score > 90
- [ ] Core Web Vitals dans le vert
- [ ] Bundle analysé (pas de dépendances inutiles)
- [ ] Service worker fonctionnel (si PWA)

### Phase Monitoring

- [ ] RUM (Real User Monitoring) configuré
- [ ] Alertes sur dégradation
- [ ] Rapports automatiques (CrUX, PageSpeed)
---
## Outils de Mesure (Recommandés)

| Type | Outil | Usage |
|------|-------|-------|
| **Lab testing** | Lighthouse, WebPageTest | CI/CD, audit |
| **Field data** | CrUX, RUM | Données réelles |
| **Bundle analysis** | Webpack Bundle Analyzer | Optimisation |
| **Monitoring** | SpeedCurve, Calibre | Suivi continu |
---
## Métriques de Suivi

| Métrique | Cible | Alerte | Action |
|----------|-------|--------|--------|
| Lighthouse Performance | > 90 | < 70 | Audit urgent |
| LCP p75 | < 2.5s | > 4s | Optimiser LCP element |
| CLS p75 | < 0.1 | > 0.25 | Fix layout shifts |
| JS Bundle | < 200KB | > 300KB | Code splitting |
---
## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| Lighthouse < 50 | Plan d'action immédiat | Tech Lead |
| Third-party bloquant | Négociation ou alternative | Product + Tech |
| Performance mobile dégradée | Priorité mobile-first | Équipe |
| Budget perf impossible | Revue design/scope | Product + Design |
---
## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Process performance | `web-dev-process/agents/testing/performance` |
| Tests visuels | `web-dev-process/agents/testing/visual-regression` |
| Implémentation images | Skills frontend spécialisés |
| Performance WordPress | `wordpress-gutenberg-expert/agents/performance/*` |

### Ressources Externes

- [web.dev/vitals](https://web.dev/vitals/) - Core Web Vitals
- [PageSpeed Insights](https://pagespeed.web.dev/) - Audit
- [WebPageTest](https://www.webpagetest.org/) - Tests avancés

## Livrables

| Livrable | Description |
|----------|-------------|
| Stratégie d'optimisation assets | Plan de compression, lazy loading et CDN pour images/JS/CSS |
| Budget de performance | Limites de poids par page et par asset type avec monitoring |
| Guide rendering strategy | Choix SSR/SSG/CSR par type de page avec justifications |
