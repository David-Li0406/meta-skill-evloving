# ADR-004 : Supervision Humaine Obligatoire

## Statut

Accepté

## Contexte

Les agents IA produisent des livrables destinés aux clients (propositions commerciales, emails, estimations). La question se pose : **ces outputs peuvent-ils être envoyés automatiquement ?**

Risques identifiés :
- Erreurs factuelles (mauvais chiffres, noms incorrects)
- Ton inapproprié
- Engagement contractuel non souhaité
- Perte de la relation client "humaine"

## Décision

Adopter le principe : **Les agents exécutent, les humains supervisent et décident.**

```
CLIENT ←→ HUMAIN (supervision) ←→ AGENTS (exécution)
```

### Règles

1. **Aucun envoi automatique** : Les agents produisent des drafts, jamais d'envoi direct
2. **Validation explicite** : Chaque livrable client doit être validé par un humain
3. **Escalade claire** : Les agents identifient quand solliciter un humain
4. **Traçabilité** : Toutes les validations sont documentées

### Cas d'Escalade

Les agents doivent explicitement escalader pour :

| Situation | Raison |
|-----------|--------|
| Décisions stratégiques | Impact business |
| Situations conflictuelles | Relation client |
| Dépassements significatifs | Engagement financier |
| Hors périmètre contractuel | Risque juridique |
| Doute sur l'interprétation | Qualité du livrable |

## Conséquences

### Positives

- **Qualité garantie** : Revue humaine avant envoi
- **Responsabilité claire** : L'humain reste décideur
- **Confiance client** : Relation personnalisée maintenue
- **Réduction des risques** : Pas d'engagement automatique
- **Amélioration continue** : Feedback sur les drafts

### Négatives

- **Latence** : Temps de validation humaine
- **Charge de travail** : L'humain doit tout valider
- **Goulot d'étranglement** : Dépendance à la disponibilité humaine

## Implémentation

### Dans les Agents

Chaque agent termine par une section de validation :

```markdown
## Avant Envoi

Ce document est un **draft** qui doit être validé avant envoi au client.

Checklist de validation :
- [ ] Informations factuelles vérifiées
- [ ] Montants corrects
- [ ] Ton approprié au client
- [ ] Pas d'engagement non souhaité
```

### Dans les Templates

Les templates incluent une zone de signature :

```markdown
## Validation

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| Rédacteur (IA) | Agent X | Auto | - |
| Validateur | [Humain] | | |
```

## Alternatives Considérées

### 1. Automatisation complète

Les agents envoient directement les livrables.

**Rejeté car** :
- Risque d'erreurs irréversibles
- Perte de contrôle
- Non conforme aux attentes clients

### 2. Validation par seuil

Automatique en dessous d'un seuil (ex: < 5000€).

**Rejeté car** :
- Complexité de définition des seuils
- Risques non financiers ignorés
- Faux sentiment de sécurité

### 3. Validation asynchrone

Envoi automatique avec possibilité d'annulation.

**Rejeté car** :
- Délai d'annulation insuffisant
- Client reçoit quand même le message
- Image non professionnelle

## Évolution Future

Possibilité d'assouplir pour certains cas à faible risque :
- Rappels internes
- Notifications de statut
- Mises à jour de planning internes

Mais jamais pour les communications client externes.

## Références

- [Human-in-the-Loop AI](https://en.wikipedia.org/wiki/Human-in-the-loop)
- Réglementation EU AI Act : supervision humaine requise
