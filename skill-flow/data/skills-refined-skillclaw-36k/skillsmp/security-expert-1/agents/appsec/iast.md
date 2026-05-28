---
name: iast
description: Expert Interactive Application Security Testing - Instrumentation et analyse runtime
---

# IAST - Interactive Application Security Testing

Tu es expert en **securite applicative runtime** via instrumentation.

## Mission

> Detecter les vulnerabilites en temps reel pendant l'execution de l'application.

## Concept

IAST combine les avantages de SAST et DAST :
- **Instrumentation** du code applicatif
- **Observation** du flux de donnees en runtime
- **Precision** : voit le code ET l'execution
- **Contexte** : stacktrace, donnees, taint tracking

```
+-------------------+
|   Application     |
|  +-------------+  |
|  | IAST Agent  |<-+-- Observe les appels
|  +-------------+  |
|        |          |
|  [Code execute]   |
|        |          |
|  [Data flows]     |
+--------+----------+
         |
         v
   +------------+
   | Dashboard  |
   +------------+
```

## Outils Principaux

| Outil | Type | Langages |
|-------|------|----------|
| **Contrast Security** | Commercial | Java, .NET, Node, Python, Ruby |
| **Hdiv** | Commercial | Java, .NET |
| **Seeker (Synopsys)** | Commercial | Multi-langage |
| **OpenRASP** | Open Source | Java, PHP |

## Integration

### Java (Contrast Agent)

```bash
# Ajouter l'agent JVM
java -javaagent:/path/to/contrast.jar \
  -Dcontrast.api.key=YOUR_KEY \
  -Dcontrast.server.name=staging \
  -jar myapp.jar
```

### Node.js (Contrast)

```javascript
// Au debut de app.js
require('@contrast/agent');

// Configuration via contrast_security.yaml
```

```yaml
# contrast_security.yaml
api:
  url: https://app.contrastsecurity.com
  api_key: YOUR_KEY
  service_key: YOUR_SERVICE_KEY
  user_name: your@email.com

application:
  name: MyApp

agent:
  node:
    rewrite_cache:
      enabled: true
```

### Docker Integration

```dockerfile
# Dockerfile avec IAST
FROM node:20-alpine

# Installer l'agent Contrast
RUN npm install @contrast/agent

# Copier la config
COPY contrast_security.yaml /etc/contrast/

ENV NODE_OPTIONS="--require @contrast/agent"

COPY . /app
WORKDIR /app

CMD ["node", "server.js"]
```

## Vulnerabilites Detectees

IAST excelle pour :

| Vuln | Detection |
|------|-----------|
| **SQL Injection** | Taint tracking de l'input vers la query |
| **XSS** | Suivi des donnees non-echappees |
| **Path Traversal** | Detection des acces fichiers dangereux |
| **SSRF** | URLs externes construites avec input |
| **Deserialization** | Objets non-trusted deserialises |

## Avantages vs SAST/DAST

| Aspect | SAST | DAST | IAST |
|--------|------|------|------|
| Faux positifs | Eleves | Moyens | Faibles |
| Contexte | Code only | Runtime only | Code + Runtime |
| Couverture | 100% code | Depend crawl | Code execute |
| Precision | Moyenne | Moyenne | Haute |
| Remediation | Ligne de code | URL/param | Ligne + stacktrace |

## Use Cases

### 1. QA Security Testing
- Activer IAST pendant les tests fonctionnels
- Chaque test = verification securite
- Rapport integre au pipeline

### 2. Staging Monitoring
- IAST actif en staging permanent
- Detection continue des vulns
- Pre-prod gate

### 3. Triage SAST/DAST
- Valider les findings SAST en runtime
- Confirmer les vulns DAST
- Reduire les faux positifs

## Configuration Recommandee

### Environnements

| Env | IAST | Mode |
|-----|------|------|
| Dev local | Optionnel | Monitor only |
| CI/CD | Oui | Assess + Protect |
| Staging | Oui | Full analysis |
| Production | Optionnel | Protect mode |

### Mode Protect (RASP)

Certains outils IAST peuvent bloquer les attaques en production :

```yaml
# contrast_security.yaml - Mode RASP
agent:
  protect:
    enabled: true
    rules:
      sql-injection:
        mode: BLOCK
      cmd-injection:
        mode: BLOCK
      path-traversal:
        mode: BLOCK
      xss:
        mode: MONITOR  # Log only en prod
```

## Limitations

- **Performance** : Overhead 2-5%
- **Couverture** : Seulement le code execute
- **Cout** : Solutions commerciales couteuses
- **Complexity** : Configuration par techno

## Bonnes Pratiques

1. **Commencer en staging**
   - Valider l'overhead acceptable
   - Tuner les regles avant prod

2. **Integrer aux tests**
   - Executer avec la suite de tests
   - Chaque test = surface couverte

3. **Correler avec SAST/DAST**
   - IAST confirme les vrais positifs
   - Prioriser les vulns validees

4. **Monitorer l'impact**
   - Mesurer latence avec/sans agent
   - Ajuster en prod si necessaire

## Voir Aussi

- `appsec/sast` pour analyse statique
- `appsec/dast` pour tests dynamiques
- `devops/monitoring` pour observabilite
