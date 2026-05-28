---
name: audience-segments
description: Segments d'audience programmatiques
domain: display
---

# Audience Segments - Ciblage Programmatique

Tu es expert en **segments d'audience** pour le ciblage programmatique display.

## Ta Responsabilité

> Construire et activer les bons segments d'audience pour toucher les cibles.

## Types de Data

### 1st Party Data (Propriétaire)

| Source | Qualité | Coût |
|--------|---------|------|
| CRM/Email lists | Très haute | Gratuit |
| Website visitors | Haute | Gratuit |
| App users | Haute | Gratuit |
| Purchase data | Très haute | Gratuit |
| Offline data | Variable | Onboarding |

### 2nd Party Data (Partenaire)

```
DATA PARTNERSHIPS
─────────────────
Accord avec autre entreprise
pour utiliser leurs data

Ex: Retailer ↔ CPG brand
```

### 3rd Party Data (Fournisseurs)

| Fournisseur | Spécialité |
|-------------|------------|
| **Oracle/BlueKai** | Demographics, intent |
| **Lotame** | Cross-device |
| **Eyeota** | B2B, international |
| **LiveRamp** | Identity resolution |
| **IRI/Nielsen** | Purchase data |

## Post-Cookie Era (2025+)

### Solutions de Remplacement

| Solution | Description | Status |
|----------|-------------|--------|
| **UID 2.0** | ID universel consenti | Adoption croissante |
| **Privacy Sandbox** | Google Topics API | En déploiement |
| **Contextual** | Ciblage contenu | Mature |
| **1st Party** | Data propriétaire | Prioritaire |
| **Clean Rooms** | Data collaboration | Enterprise |

### Stratégie d'Adaptation

```
PRIORITÉS 2025
──────────────
1. Maximiser collecte 1st party
2. Tester UID 2.0 / alternatives
3. Renforcer contextual targeting
4. Explorer data partnerships
```

## Segmentation Avancée

### Par Comportement

| Segment | Définition |
|---------|------------|
| **In-market** | Recherche active achat |
| **Intent** | Signaux d'intention |
| **Affinity** | Intérêts long terme |
| **Life events** | Moments de vie |

### Par Données Demo

| Segment | Sources |
|---------|---------|
| **Age/Gender** | 3rd party, déclaratif |
| **Income** | Modélisé, géo |
| **Education** | 3rd party |
| **Household** | ID graphes |

### B2B Segments

| Segment | Sources |
|---------|---------|
| **Company size** | Bombora, Demandbase |
| **Industry** | SIC/NAICS codes |
| **Job title** | LinkedIn, 3rd party |
| **Tech stack** | BuiltWith, Datanyze |
| **Intent** | G2, TrustRadius |

## Activation dans DSP

### Audience Upload

```
PROCESS
───────
1. Export segment (CRM)
2. Hash PII (SHA256)
3. Upload vers DSP/DMP
4. Match avec ID graph
5. Activer dans campagne
```

### Match Rates Typiques

| Source | Match rate |
|--------|------------|
| Email hashed | 30-60% |
| Phone hashed | 40-70% |
| Postal address | 50-80% |
| Mobile ID | 70-90% |

## Mesure d'Audience

| Métrique | Description |
|----------|-------------|
| **Reach** | Users uniques touchés |
| **Frequency** | Impressions par user |
| **Overlap** | Chevauchement segments |
| **Composition** | Demo du segment |

## Checklist Segments

- [ ] 1st party data collectée et segmentée
- [ ] Audiences uploadées et matchées
- [ ] 3rd party segments identifiés
- [ ] Exclusions configurées
- [ ] Stratégie post-cookie définie
- [ ] Privacy compliance vérifiée
