---
name: rgpd-request
description: Automatiser les demandes RGPD (suppression, accès, portabilité des données personnelles). Utiliser ce skill quand l'utilisateur souhaite exercer ses droits RGPD auprès d'une entreprise, notamment pour la suppression de données marketing, le droit à l'oubli, ou l'accès à ses données personnelles. Déclenché par des demandes comme "supprimer mes données", "RGPD", "désabonnement", "droit à l'oubli", "mes données personnelles".
---

# RGPD Request Skill

Ce skill automatise la rédaction de demandes RGPD conformes au Règlement Général sur la Protection des Données (UE 2016/679).

## Workflow

### 1. Identification du contact DPO

Rechercher le contact DPO/données personnelles de l'entreprise dans cet ordre :
1. Page "Politique de confidentialité" ou "Privacy Policy" du site web
2. Page "Mentions légales" ou "Legal"
3. Page "Contact" avec mention RGPD/DPO
4. Email générique : dpo@[domaine], privacy@[domaine], rgpd@[domaine]

Mots-clés de recherche : `[nom entreprise] DPO contact RGPD` ou `[nom entreprise] privacy policy data protection`

### 2. Types de demandes supportées

| Type | Article RGPD | Description |
|------|--------------|-------------|
| Suppression | Art. 17 | Droit à l'effacement ("droit à l'oubli") |
| Accès | Art. 15 | Obtenir copie de ses données |
| Rectification | Art. 16 | Corriger des données inexactes |
| Portabilité | Art. 20 | Recevoir ses données dans un format structuré |
| Opposition | Art. 21 | S'opposer au traitement (notamment marketing) |
| Limitation | Art. 18 | Limiter le traitement des données |

### 3. Rédaction du mail

Utiliser le template approprié depuis `references/templates.md` selon le type de demande.

Éléments obligatoires :
- Objet clair mentionnant le droit exercé
- Identification du demandeur (nom, email)
- Base légale (article RGPD concerné)
- Demande explicite et précise
- Rappel du délai légal (1 mois)
- Mention de la CNIL en cas de non-réponse

### 4. Délais et recours

- Délai de réponse : 1 mois (extensible à 3 mois si complexe)
- En cas de non-réponse ou refus : plainte CNIL sur https://www.cnil.fr/fr/plaintes
- Conservation : garder une copie de la demande avec date d'envoi

## Références

Pour les templates de mails détaillés, consulter `references/templates.md`.
