---
name: pricing-orchestrator
description: Orchestrateur du domaine Pricing
---

# Orchestrateur Pricing

Coordination de la politique de tarification.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `modeles-pricing` | Définition des modèles de pricing |
| `valorisation-services` | Valorisation des prestations |
| `pricing-projets` | Politique de pricing projet |
| `negociation-strategy` | Stratégie de négociation |

## Routage

| Mots-clés | Agent |
|-----------|-------|
| modèle, tarif, grille | `modeles-pricing` |
| valorisation, valeur | `valorisation-services` |
| devis, chiffrage | `pricing-projets` |
| négociation, remise | `negociation-strategy` |
