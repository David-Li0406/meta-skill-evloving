# Prompts Prêts à l'Emploi

Copie-colle ces prompts pour utiliser le skill efficacement.

---

## 🎯 Créer un Challenge

### Prompt basique
```
Crée un nouveau challenge Kubeasy sur le thème [THEME].
Le concept à enseigner : [CONCEPT]
Difficulté souhaitée : [easy/medium/hard]
```

### Prompt détaillé
```
Crée un challenge Kubeasy avec ces specs :
- Thème : networking
- Type : fix
- Difficulté : medium
- Concept : Un Service ne route pas le trafic vers les pods à cause d'un mismatch de labels

Le scénario doit être réaliste, comme si ça arrivait en prod.
```

### Prompt "je sais pas quoi faire"
```
Propose-moi 3 idées de challenges Kubeasy pour le thème "volumes-secrets", 
avec différents niveaux de difficulté.
```

---

## 🔍 Review un Challenge

### Review simple
```
Review le challenge "bad-config"
```

### Review avec focus
```
Review le challenge "traffic-jam" en portant une attention particulière 
à la résistance aux bypasses.
```

### Review batch
```
Review tous les challenges du repo et génère un rapport consolidé 
avec les scores et recommandations.
```

---

## 💡 Générer des Idées

### Trouver les gaps
```
Analyse les challenges existants et identifie les thèmes Kubernetes 
sous-représentés. Propose des idées pour combler ces lacunes.
```

### Explorer un thème
```
Explore la documentation Kubernetes sur les CronJobs et propose 
3 idées de challenges "fix" basées sur des erreurs courantes.
```

### Idées CKA/CKAD
```
Génère des idées de challenges alignées avec les objectifs de 
certification CKA, en prioritisant les topics à fort coefficient.
```

---

## 🔄 Workflows Combinés

### Cycle complet (idée → création → review)
```
1. Trouve une idée de challenge sur le thème "scheduling-affinity"
2. Crée le challenge complet
3. Review-le pour valider la qualité
```

### Améliorer un challenge existant
```
Review le challenge "pod-evicted", puis propose des améliorations 
basées sur le score et les recommandations.
```

### Comparer avec la concurrence
```
Analyse les challenges Kubernetes de KodeKloud et propose des 
challenges Kubeasy qui couvrent des concepts similaires mais 
avec notre approche "mystery preserving".
```

---

## 🛠️ Maintenance

### Vérifier la cohérence
```
Vérifie que tous les challenges du repo ont :
- Un challenge.yaml valide (selon le schema MCP)
- Des objectives qui testent les outcomes, pas les implémentations
- Une difficulté cohérente avec le temps estimé
```

### Sync database
```
Synchronise les challenges avec la base de données et 
affiche le résultat (created/updated/deleted).
```

### Mettre à jour pour tester
```
Je veux tester le challenge "new-challenge" en local.
Mets à jour la branche dans le CLI, recompile, et lance le test.
```

---

## 📝 Templates de Réponse Attendue

### Après création
```
✅ Challenge créé : <slug>

Fichiers :
- challenges/<slug>/challenge.yaml
- challenges/<slug>/manifests/*.yaml
- challenges/<slug>/policies/protect.yaml (si applicable)

Prochaines étapes :
1. Sync DB : API_TOKEN=xxx node .github/scripts/sync.js
2. Push : git checkout -b challenge/<slug> && git add . && git commit && git push
3. Test : Mettre à jour CLI et tester
```

### Après review
```
📊 Review : <slug>

Score : 17/20 (Bon)
├── Clarté : 4/4
├── Pédagogie : 4/4
├── Validation : 3/4
├── Anti-bypass : 3/4
└── UX : 3/4

Issues :
- Description un peu trop explicite sur le problème

Recommandations :
- Reformuler "The pod keeps crashing" → "Something's wrong with the deployment"

Rapport : /tmp/challenge-review-<slug>.json
```

### Après génération d'idées
```
💡 3 idées pour "scheduling-affinity"

1. **Stuck in Pending** (easy, 10min)
   Pod bloqué car nodeSelector pointe vers un node inexistant
   
2. **Anti-Colocation Failure** (medium, 15min)
   Pod anti-affinity trop strict empêche le scheduling
   
3. **Taint Tolerance** (hard, 25min)
   Workload critique ne démarre pas sur nodes taintés

Gaps identifiés : Aucun challenge sur topology spread constraints
```
