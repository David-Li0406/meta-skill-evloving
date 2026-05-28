---
name: blast-architect
description: Capacité à structurer des projets complexes via gemini.md et MCP.
---

# B.L.A.S.T. ARCHITECT

Cette compétence permet à l'agent de maintenir la cohérence du projet via un fichier central.

## CAPACITÉS
1.  **Gestion du `gemini.md`** :
    * Lire ce fichier au début de chaque session pour charger le contexte (Map).
    * Mettre à jour le fichier quand de nouveaux outils sont ajoutés.

2.  **Intégration MCP** :
    * Suggérer des configurations MCP basées sur les besoins du Blueprint.
    * Exemple : "Tu as besoin de transcriptions ? Ajoutons le serveur MCP Fireflies."

3.  **Validation Déterministe** :
    * Vérifier que les scripts (Tools) ne "devinent" jamais la logique business. Ils doivent exécuter des règles strictes.

## TRIGGER
Utiliser quand l'utilisateur dit : "Nouveau projet", "Architecture", "Blueprint", ou "/blast".
