---
name: n8n-commander-v2
description: Pilotage complet de l'instance N8N pour le Cycle 12WY.
---

# CAPACITÉS
1.  **Recycle Workflow** : `n8n_recycle(workflow_id)` -> Archive la version actuelle et injecte le `00_Master_Template_v2`.
2.  **Deploy Agent** : `n8n_deploy(blast_blueprint)` -> Crée un nouveau workflow basé sur un fichier `gemini.md` (B.L.A.S.T.).
3.  **Audit Health** : `n8n_audit()` -> Vérifie que tous les workflows actifs respectent la **Ralph Loop** (Idempotence).
