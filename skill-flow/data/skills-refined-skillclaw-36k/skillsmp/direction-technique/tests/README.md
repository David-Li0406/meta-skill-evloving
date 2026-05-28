# Tests Direction Technique

Suite de validation pour le skill `direction-technique`.

## Quick Start

```bash
# Installer (si nécessaire)
npm install

# Lancer tous les tests
npm test

# Tests rapides (structure uniquement)
npm run test:quick

# Tests qualité (markdown, routing, keywords)
npm run test:quality
```

## Scripts Disponibles

| Script | Description |
|--------|-------------|
| `npm test` | Exécute tous les tests |
| `npm run test:quick` | Domains + agents uniquement |
| `npm run test:quality` | Markdown + routing + keywords |
| `npm run test:json` | Sortie JSON pour CI |
| `npm run test:ci` | Alias pour `npm test` |

## Structure des Tests

```
tests/
├── config.js                    # Configuration (domaines, agents)
├── utils.js                     # Utilitaires partagés
├── validate-domains.test.js     # Structure des 10 domaines
├── validate-agents.test.js      # Présence des 52 agents
├── validate-skill.test.js       # SKILL.md principal
├── validate-routing.test.js     # Tables de routage
├── validate-keywords.test.js    # Mots-clés uniques
└── validate-markdown.test.js    # Qualité markdown
```

## Tests Détaillés

### validate-domains.test.js
Vérifie que chaque domaine a :
- Un répertoire existant
- Un orchestrator.md
- Tous les agents attendus

### validate-agents.test.js
Vérifie que chaque agent a :
- Un frontmatter valide (name, description)
- Une section principale (#)
- Du contenu substantiel

### validate-skill.test.js
Vérifie SKILL.md :
- Frontmatter complet
- Sections requises
- Table de routage vers les domaines

### validate-routing.test.js
Vérifie les orchestrators :
- Tables de routage présentes
- Agents référencés existants
- Format correct des références

### validate-keywords.test.js
Vérifie les mots-clés :
- Unicité par agent
- Pas de doublons inter-domaines (sauf documentés)
- Format valide

### validate-markdown.test.js
Vérifie la qualité :
- Blocs de code avec langage
- Tables bien formées
- Checklists techniques
- Longueur minimale

## Mode JSON (CI)

Pour une sortie parseable en CI :

```bash
OUTPUT_FORMAT=json npm test
```

Exemple de sortie :
```json
{
  "name": "validate-domains",
  "duration": 45,
  "passed": 31,
  "failed": 0,
  "total": 31,
  "success": true,
  "results": [...]
}
```

### Utilisation avec TestReporter

```javascript
const { TestReporter } = require('./utils');

const reporter = new TestReporter('my-test');
reporter.header('My Test Suite');
reporter.section('Domain: foo');
reporter.pass('Check passed');
reporter.fail('Check failed', { file: 'bar.md' });
reporter.summarize(); // Outputs JSON if OUTPUT_FORMAT=json
```

## Conventions

### Nommage
- Domaines : `kebab-case` (ex: `avant-projet`)
- Agents : `kebab-case` (ex: `audit-existant`)
- Chiffres autorisés (ex: `adr-001`)

### Mots-clés
- Normalisés en minuscules
- Uniques par agent (sauf exceptions documentées)
- Désambiguïsation requise si partagés

## Ajouter un Test

1. Créer `tests/validate-xxx.test.js`
2. Ajouter le shebang : `#!/usr/bin/env node`
3. Utiliser les utilitaires de `utils.js`
4. Ajouter le script dans `package.json`
5. Rendre exécutable : `chmod +x tests/validate-xxx.test.js`

## Troubleshooting

### "Cannot find module"
```bash
cd .web-agency/skills/direction-technique
npm install
```

### Test échoue sur agent manquant
Vérifier `config.js` pour la liste des agents attendus.

### Faux positif sur routing
Les sections `## Désambiguïsation` sont ignorées par le validateur de routing.
