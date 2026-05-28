---
name: ralph_bridge
description: Protocole de communication et de délégation entre R0 et le Technicien.
---

# Ralph Bridge Skill

## 🎯 MISSION
Opérer la transition entre la Stratégie (Manager) et l'Action (Technicien) sans perte d'information.

## 🔄 LES HOOKS (Anti-Fragile)
*   **HOOK 0 : Health Check** : Lister les outils disponibles.
*   **HOOK 1 : Phase ID** : Lire `tracks.md` et identifier la phase courante.
*   **HOOK 2 : Commitment** : Annoncer l'outil utilisé pour la tâche.
*   **HOOK 3 : Atomic Execution** : Une action, une vérification.
*   **HOOK 4 : Failure Audit** : Documentation brute de l'erreur en cas d'échec.
