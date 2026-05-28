# Exemples d'Utilisation

Ce document présente des exemples concrets d'utilisation des agents web-agency.

## Avant-Projet

### Exemple 1 : Traitement d'un Email Client

**Contexte** : Vous recevez un email d'un prospect.

**Conversation** :

```
👤 Utilisateur :
J'ai reçu cet email d'un client potentiel :

"Bonjour,

Nous sommes une PME de 50 personnes dans le secteur de la distribution de
matériel médical. Notre site web actuel date de 2018 et ne répond plus à
nos besoins. Nous cherchons une refonte complète avec un catalogue produits
et un espace client B2B.

Budget indicatif : 40-60k€
Délai souhaité : mise en ligne avant septembre 2025

Pouvez-vous nous faire une proposition ?

Cordialement,
Marie Martin
Directrice Marketing
MediDistrib"

🤖 Agent collecte-besoin :

# Extraction - Email Client

**Type de source** : Email
**Date** : 21/12/2024
**Auteur** : Marie Martin - Directrice Marketing

---

## Informations Client
- Entreprise : MediDistrib
- Secteur : Distribution matériel médical
- Taille : PME 50 personnes
- Contact : Marie Martin (Directrice Marketing)

## Contexte Identifié
- Site actuel date de 2018
- Ne répond plus aux besoins actuels

## Objectifs Mentionnés
- "Refonte complète"
- "Catalogue produits"
- "Espace client B2B"

## Contraintes Détectées
- Budget : 40-60k€
- Délai : Mise en ligne avant septembre 2025

## Informations Manquantes
- [ ] Nombre de références produits
- [ ] Fonctionnalités B2B attendues (commande, devis, etc.)
- [ ] Intégrations existantes (ERP, CRM)
- [ ] Hébergement actuel
```

### Exemple 2 : Génération de Questions de Clarification

**Suite de l'exemple précédent** :

```
👤 Utilisateur :
Quelles questions dois-je poser au client ?

🤖 Agent questions-clarification :

# Questions de Clarification - MediDistrib

## Périmètre Fonctionnel

### Catalogue Produits
1. Combien de références produits avez-vous à présenter ?
2. Les fiches produits ont-elles des documents techniques (PDF, notices) ?
3. Y a-t-il des variantes de produits (tailles, configurations) ?

### Espace Client B2B
4. Quelles fonctionnalités attendez-vous ?
   - [ ] Consultation des prix personnalisés
   - [ ] Passage de commandes en ligne
   - [ ] Demande de devis
   - [ ] Historique des commandes
   - [ ] Suivi des livraisons

5. Combien de clients actifs utilisent actuellement votre site ?

## Technique

6. Utilisez-vous un ERP ? Si oui, lequel ? (SAP, Sage, etc.)
7. Avez-vous un CRM à intégrer ?
8. Où est hébergé votre site actuel ?

## Contenu

9. Qui rédigera les contenus (textes, fiches produits) ?
10. Avez-vous une charte graphique à respecter ?

## Priorité

⚠️ **Questions critiques** (bloquantes pour l'estimation) :
- Question 1 (volume catalogue)
- Question 4 (périmètre B2B)
- Question 6 (intégration ERP)
```

### Exemple 3 : Chiffrage d'un Projet

```
👤 Utilisateur :
Peux-tu me faire un chiffrage pour ce projet ?
Le client a confirmé : 500 produits, espace client avec commande et devis,
intégration Sage X3.

🤖 Agent chiffrage :

# Estimation - Refonte MediDistrib

**Date** : 21/12/2024
**Version** : 1.0

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| **Total jours** | 85 j |
| **Fourchette budget** | 51 000 € - 68 000 € |

---

## Détail par Lot

### Lot 1 - Socle Technique
| Tâche | Profil | Jours |
|-------|--------|-------|
| Setup projet & environnements | Lead Dev | 2 |
| Architecture technique | Lead Dev | 3 |
| Intégration Sage X3 | Dev Senior | 8 |
| **Sous-total** | | **13 j** |

### Lot 2 - Catalogue Produits
| Tâche | Profil | Jours |
|-------|--------|-------|
| Modélisation données (500 refs) | Dev | 3 |
| Import / synchronisation | Dev | 5 |
| Fiches produits | Dev | 8 |
| Recherche & filtres | Dev | 5 |
| **Sous-total** | | **21 j** |

### Lot 3 - Espace Client B2B
| Tâche | Profil | Jours |
|-------|--------|-------|
| Authentification & rôles | Dev Senior | 4 |
| Prix personnalisés | Dev | 5 |
| Tunnel de commande | Dev Senior | 8 |
| Demande de devis | Dev | 4 |
| Historique & suivi | Dev | 4 |
| **Sous-total** | | **25 j** |

### Lot 4 - Front-End
| Tâche | Profil | Jours |
|-------|--------|-------|
| Maquettes | UX/UI | 8 |
| Intégration | Intégrateur | 12 |
| Responsive | Intégrateur | 4 |
| **Sous-total** | | **24 j** |

### Lot 5 - Recette & MEP
| Tâche | Profil | Jours |
|-------|--------|-------|
| Tests | QA | 5 |
| Corrections | Dev | 3 |
| MEP & formation | Lead Dev | 2 |
| **Sous-total** | | **10 j** |

---

## Hypothèses

- API Sage X3 disponible et documentée
- Contenus fournis par le client
- 1 aller-retour de corrections sur maquettes
- Hébergement cloud (AWS/OVH)

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| API Sage non standard | +5-10j | POC en phase 1 |
| Volume données > prévu | +3-5j | Import par lots |
```

---

## Pilotage

### Exemple 4 : Reporting Hebdomadaire

```
👤 Utilisateur :
Génère le reporting de la semaine. Voici les données :
- Lot 1 terminé
- Lot 2 à 60% (prévu 80%)
- Lot 3 à 20% (prévu 30%)
- 2 jours de retard sur l'intégration Sage

🤖 Agent reporting-hebdo :

# Reporting Projet - MediDistrib

**Semaine** : S51 - du 16/12 au 20/12/2024
**Date** : 20/12/2024

---

## État Global

| Dimension | Statut |
|-----------|--------|
| Délais | 🟡 |
| Budget | 🟢 |
| Qualité | 🟢 |

**Statut global** : 🟡 Attention

---

## Avancement

### Par Lot

| Lot | Prévu | Réalisé | Écart |
|-----|-------|---------|-------|
| Lot 1 - Socle | 100% | 100% | ✅ |
| Lot 2 - Catalogue | 80% | 60% | -20% ⚠️ |
| Lot 3 - Espace B2B | 30% | 20% | -10% |
| **Global** | **55%** | **45%** | **-10%** |

### Progression Visuelle

```
Lot 1 : [████████████████████] 100% ✅
Lot 2 : [████████████░░░░░░░░]  60% ⚠️
Lot 3 : [████░░░░░░░░░░░░░░░░]  20%
Global: [█████████░░░░░░░░░░░]  45%
```

---

## Faits Marquants

### Réalisé cette semaine
- ✅ Finalisation du socle technique
- ✅ Import initial des 500 produits
- ✅ Maquettes validées par le client

### Prévu semaine prochaine
- 📋 Rattrapage retard Lot 2
- 📋 Développement tunnel de commande
- 📋 Intégration front-end catalogue

---

## Points d'Attention

| Point | Impact | Action |
|-------|--------|--------|
| Retard intégration Sage (2j) | Décalage Lot 2 | Renfort dev prévu lundi |
| Client indisponible 23-31/12 | Validation bloquée | Anticiper validations vendredi |

---

## Décisions Requises

| Décision | Options | Deadline |
|----------|---------|----------|
| Renfort développeur | A. Interne / B. Freelance | 23/12 |
```

---

## Communication

### Exemple 5 : Email d'Annonce de Retard

```
👤 Utilisateur :
Je dois annoncer au client qu'on aura 1 semaine de retard sur la livraison
du catalogue. Cause : complexité de l'API Sage plus importante que prévue.

🤖 Agent email-annonce-retard :

**Objet** : Projet MediDistrib - Point d'avancement et ajustement planning

---

Bonjour Marie,

Je reviens vers vous concernant l'avancement du projet de refonte.

**Situation actuelle**

L'intégration avec votre ERP Sage X3 s'avère plus complexe que nos
estimations initiales. L'API nécessite des développements spécifiques
pour synchroniser correctement les prix personnalisés par client.

**Impact**

Cette situation entraîne un décalage d'**une semaine** sur la livraison
du module Catalogue :
- Date initiale : 15 janvier 2025
- Nouvelle date : 22 janvier 2025

**Actions en cours**

Pour limiter l'impact :
- Un développeur senior supplémentaire est mobilisé cette semaine
- Nous parallélisons les développements front-end
- Les autres lots ne sont pas impactés

**Planning mis à jour**

| Jalon | Date initiale | Nouvelle date |
|-------|---------------|---------------|
| Catalogue | 15/01 | 22/01 |
| Espace B2B | 31/01 | 31/01 (inchangé) |
| MEP | 28/02 | 28/02 (inchangé) |

La date de mise en production finale reste inchangée grâce aux mesures
de rattrapage mises en place.

Je reste à votre disposition pour échanger de vive voix si vous le souhaitez.

Cordialement,

[Votre nom]
Chef de projet
```

---

## Livraison

### Exemple 6 : Procès-Verbal de Recette

```
👤 Utilisateur :
La recette est terminée. 45 tests passés, 3 anomalies mineures corrigées,
client satisfait. Génère le PV.

🤖 Agent pv-recette :

# Procès-Verbal de Recette

## Informations Générales

| Champ | Valeur |
|-------|--------|
| **Projet** | Refonte site MediDistrib |
| **Client** | MediDistrib - Marie Martin |
| **Date de recette** | 20/02/2025 |
| **Version testée** | 1.0.0 |

---

## Périmètre de la Recette

### Lots Recettés

| Lot | Statut |
|-----|--------|
| Lot 1 - Socle Technique | ✅ Validé |
| Lot 2 - Catalogue Produits | ✅ Validé |
| Lot 3 - Espace Client B2B | ✅ Validé |
| Lot 4 - Front-End | ✅ Validé |

---

## Résultats des Tests

### Synthèse

| Métrique | Valeur |
|----------|--------|
| Tests exécutés | 45 |
| Tests passés | 45 |
| Tests échoués | 0 |
| **Taux de réussite** | **100%** |

### Anomalies

| # | Description | Sévérité | Statut |
|---|-------------|----------|--------|
| 1 | Alignement bouton panier mobile | Mineure | ✅ Corrigée |
| 2 | Timeout sur export PDF catalogue | Mineure | ✅ Corrigée |
| 3 | Libellé incorrect page devis | Mineure | ✅ Corrigée |

---

## Décision

☑️ **RECETTE VALIDÉE**

Le Client déclare que les livrables sont conformes aux spécifications
et accepte la livraison du projet.

---

## Réserves

Aucune réserve.

---

## Signatures

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| Client | Marie Martin | 20/02/2025 | _____________ |
| Chef de projet | [Nom] | 20/02/2025 | _____________ |

---

## Annexes

- Grille de recette détaillée
- Captures d'écran des corrections
- Documentation utilisateur
```

---

## Conseils d'Utilisation

### Enchaîner les Agents

Les agents sont conçus pour s'enchaîner naturellement :

```
collecte-besoin → formalisation-brief → questions-clarification
                                              ↓
                                        analyse-perimetre → chiffrage
                                                                ↓
                                                      redaction-proposition
```

### Fournir le Contexte

Plus vous donnez de contexte, meilleur sera le résultat :

```
❌ "Fais un chiffrage"

✅ "Fais un chiffrage pour le projet MediDistrib.
    Le client a validé : 500 produits, espace B2B avec commande et devis,
    intégration Sage X3. Budget client : 40-60k€."
```

### Demander des Ajustements

Les agents produisent des versions initiales. N'hésitez pas à demander :

- "Ajoute plus de détails sur le lot 2"
- "Le ton est trop formel, rends-le plus accessible"
- "Ajoute une section sur les risques"
