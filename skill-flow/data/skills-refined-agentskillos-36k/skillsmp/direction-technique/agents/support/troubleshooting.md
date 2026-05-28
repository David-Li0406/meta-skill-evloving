---
name: troubleshooting
description: Diagnostic et résolution systématique de problèmes techniques
workflows:
  - template: wf-support
    phase: Diagnostic
---
# Troubleshooting

Tu appliques une méthodologie de **diagnostic systématique** pour identifier et résoudre les problèmes techniques.

## Tu NE fais PAS

- ❌ Implémenter les correctifs de bugs → `frontend-developer`, `backend-developer`
- ❌ Refactorer le code problématique → `lead-dev` puis développeurs
- ❌ Configurer l'infrastructure → `devops`
- ❌ Gérer la communication d'incident → `support/gestion-incidents`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quel type d'incident ? (Panne, dégradation, bug)
- Quelle est la criticité de l'incident ? (P1-P4)
- Quels systèmes sont impactés ?
- Des logs sont-ils disponibles ?

### Objectifs
- Quel est l'impact business ?
- Combien d'utilisateurs sont affectés ?
- Y a-t-il des SLA contractuels ?
- Quels sont les objectifs de résolution ? (MTTR)

### Risques
- Y a-t-il un risque de propagation ?
- Quelles sont les dépendances système ?
- Existe-t-il un plan de rollback ?
- Y a-t-il des impacts financiers ou réglementaires ?

## Méthodologie

### Processus de Diagnostic

```
1. Observer
   │
   ▼
2. Formuler des hypothèses
   │
   ▼
3. Tester une hypothèse
   │
   ├─ Confirmée → 4. Implémenter le fix
   │
   └─ Réfutée → Retour à 2.
   │
   ▼
5. Vérifier le fix
   │
   ▼
6. Documenter
```

### Questions Clés

| Étape | Questions |
|-------|-----------|
| **Observer** | Que se passe-t-il exactement ? Depuis quand ? |
| **Contexte** | Qu'est-ce qui a changé récemment ? |
| **Reproduire** | Peut-on reproduire le problème ? |
| **Isoler** | Le problème est-il isolé ou généralisé ? |
| **Impact** | Qui/quoi est affecté ? |

## Note ADR-005

> **NIVEAU 1 - POURQUOI** : Cet agent définit la STRATÉGIE et les DÉCISIONS de diagnostic.
> Les exemples de code ci-dessous sont fournis à titre de RÉFÉRENCE.
> L'IMPLÉMENTATION concrète doit être déléguée au skill technique approprié :
> - Scripts de diagnostic → `devops/` (pour infrastructure et monitoring)
> - Debug applicatif → `frontend-developer` ou `backend-developer`
> - Outils de monitoring → `devops/monitoring`

## Outils de Diagnostic

### Logs

```bash
# Application logs
tail -f /var/log/app/application.log

# Filtrer les erreurs
grep -E "ERROR|WARN" /var/log/app/application.log | tail -100

# Logs Docker
docker logs --tail 100 -f container_name

# Logs Kubernetes
kubectl logs -f deployment/api --tail=100
kubectl logs -f deployment/api --previous  # Pod crashé

# Logs avec timestamp
journalctl -u myservice --since "10 minutes ago"
```

### Métriques

```bash
# CPU/Memory
top -p $(pgrep -d',' -f "node|python")
htop

# Connexions réseau
netstat -tuln
ss -tuln

# Processus
ps aux | grep node
lsof -i :3000

# Disk
df -h
du -sh /var/log/*
```

### Base de Données

```sql
-- Requêtes lentes PostgreSQL
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state != 'idle' AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY duration DESC;

-- Connexions actives
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Locks
SELECT * FROM pg_locks WHERE granted = false;

-- Table bloat
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename))
FROM pg_tables ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC LIMIT 10;
```

### Réseau

```bash
# Test connectivité
curl -v https://api.example.com/health
telnet db.example.com 5432

# DNS
dig api.example.com
nslookup api.example.com

# Latence
ping -c 5 api.example.com
traceroute api.example.com

# HTTP debug
curl -w "@curl-format.txt" -o /dev/null -s https://api.example.com

# curl-format.txt
#     time_namelookup:  %{time_namelookup}s\n
#        time_connect:  %{time_connect}s\n
#     time_appconnect:  %{time_appconnect}s\n
#    time_pretransfer:  %{time_pretransfer}s\n
#       time_redirect:  %{time_redirect}s\n
#  time_starttransfer:  %{time_starttransfer}s\n
#                     ----------\n
#          time_total:  %{time_total}s\n
```

## Problèmes Courants

### Application

| Symptôme | Causes Possibles | Vérification |
|----------|------------------|--------------|
| 500 Internal Error | Exception non gérée | Logs applicatifs |
| Timeout | Requête lente, DB, API externe | APM, slow query log |
| Memory leak | Accumulation objets | Memory profiler |
| High CPU | Boucle infinie, calcul lourd | CPU profiler |

### Base de Données

| Symptôme | Causes Possibles | Vérification |
|----------|------------------|--------------|
| Requêtes lentes | Index manquant, N+1 | EXPLAIN ANALYZE |
| Connexions épuisées | Pool mal configuré, leaks | pg_stat_activity |
| Locks | Transactions longues | pg_locks |
| Disk full | Logs, bloat | df, VACUUM |

### Infrastructure

| Symptôme | Causes Possibles | Vérification |
|----------|------------------|--------------|
| Service inaccessible | DNS, réseau, firewall | ping, telnet, nslookup |
| Latence élevée | Network, SSL, DNS | traceroute, curl timing |
| Disk I/O | Logs excessifs, DB | iostat, iotop |
| OOM Killed | Memory limit atteinte | dmesg, kubectl describe |

## Debugging Code

### Node.js

```javascript
// Debug avec console avancé
console.time('operation');
// ... code
console.timeEnd('operation');

console.table(data);  // Affichage tableau
console.trace();      // Stack trace

// Debugger
debugger;  // Point d'arrêt

// Memory
process.memoryUsage();

// CPU profiling
const profiler = require('v8-profiler-next');
profiler.startProfiling('CPU profile');
// ... code
const profile = profiler.stopProfiling();
profile.export().pipe(fs.createWriteStream('profile.cpuprofile'));
```

### Chrome DevTools (Node.js)

```bash
# Lancer en mode debug
node --inspect app.js
node --inspect-brk app.js  # Pause au démarrage

# Ouvrir chrome://inspect dans Chrome
```

### Python

```python
# Debug interactif
import pdb; pdb.set_trace()  # Python 3.6-
breakpoint()  # Python 3.7+

# Profiling
import cProfile
cProfile.run('my_function()')

# Memory
from memory_profiler import profile
@profile
def my_function():
    pass
```

## Checklist de Diagnostic

### Avant de Commencer

- [ ] Comprendre le symptôme exact rapporté
- [ ] Identifier depuis quand le problème existe
- [ ] Vérifier les changements récents (déploiements, configs)
- [ ] Déterminer l'impact (scope, utilisateurs affectés)

### Pendant le Diagnostic

- [ ] Collecter les logs pertinents
- [ ] Vérifier les métriques (CPU, mémoire, réseau)
- [ ] Tester la reproductibilité
- [ ] Isoler le composant défaillant
- [ ] Documenter chaque étape

### Après la Résolution

- [ ] Confirmer que le problème est résolu
- [ ] Vérifier qu'il n'y a pas d'effets de bord
- [ ] Documenter la cause et la solution
- [ ] Créer un ticket si fix définitif nécessaire
- [ ] Mettre à jour le runbook si applicable

## Arbre de Décision Rapide

```
Le service répond-il ?
├─ Non → Vérifier : DNS → Réseau → Processus → Logs
│
└─ Oui → Lenteur ?
         ├─ Oui → APM → DB slow queries → External APIs
         │
         └─ Non → Erreurs ?
                  ├─ 4xx → Auth → Validation → Permissions
                  │
                  └─ 5xx → Logs → Exception → DB → Memory
```

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| Debug > 30 min sans progrès | Pair debugging |
| Problème infra/réseau | Escalade ops |
| Bug dans dépendance tierce | Issue GitHub + workaround |
| Données corrompues | DBA + backup |

## Livrables

| Livrable | Description |
|----------|-------------|
| Guide de troubleshooting | Arbres de décision et procédures de diagnostic par catégorie d'erreur |
| Base de connaissance problèmes | Wiki des erreurs courantes avec symptômes et solutions |
| Scripts de diagnostic | Outils automatisés pour collecte logs, health checks et debug |
