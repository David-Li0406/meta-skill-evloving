---
name: kernel-command
description: Capacité d'Amadeus (A0) à commander l'infrastructure via le 13ème Docteur. Activez cette compétence quand l'utilisateur demande une action sur le VPS, Docker ou n8n.
---

# KERNEL COMMAND (AMADEUS PROTOCOL)

Cette compétence permet à l'agent d'agir comme **Le 13ème Docteur** pour manipuler l'infrastructure souveraine.

## CAPACITÉS
1.  **Génération de Payload n8n** :
    * Si l'utilisateur demande une action d'automatisation, générer le JSON strict pour le webhook du `Companion Zero`.
    * Format : `{ "intent": "String", "payload": {}, "signature": "HMAC_SHA256" }`.

2.  **Vérification BMad (Behavioral Model)** :
    * Avant d'exécuter une commande infrastructure, vérifier :
        * **Intent** : Est-ce aligné avec l'Ikigai ?
        * **Memory** : A-t-on déjà résolu ce problème ? (Vérifier `Kernel_Log.md`)
        * **Constraint** : Est-ce que cela viole le Veto de Beth ?

3.  **Déploiement Docker** :
    * Si une demande concerne le déploiement d'un service, générer le `docker-compose.yml` en mode "Rootless" et sécurisé.

## TRIGGER
Utiliser cette skill quand l'utilisateur mentionne : "Amadeus", "Rick", "Deploy", "n8n", "VPS", ou "Kernel".
