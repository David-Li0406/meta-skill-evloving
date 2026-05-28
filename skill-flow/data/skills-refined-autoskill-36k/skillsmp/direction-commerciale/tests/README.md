# Tests - Direction Commerciale

Suite de tests pour valider la structure et la qualité du skill direction-commerciale.

## Exécution

```bash
# Tous les tests
npm test --prefix .web-agency/skills/direction-commerciale

# Test spécifique
node .web-agency/skills/direction-commerciale/tests/validate-agents.test.js
```

## Tests Disponibles

| Test | Description |
|------|-------------|
| `validate-agents.test.js` | Valide la structure des fichiers agents |

## Configuration

La configuration des tests se trouve dans `config.js` :

- `DOMAINS` : Liste des 5 domaines (strategie-commerciale, pricing, partenariats, rentabilite, relation-client)
- `EXPECTED_AGENTS_PER_DOMAIN` : Agents attendus par domaine (27 total)
- `AGENT_REQUIREMENTS` : Exigences de validation (frontmatter, longueur min, sections)
- `DOMAIN_KEYWORDS` : Mots-clés pour validation du routage

## Critères de Validation

### Fichiers Agents

- ✅ Frontmatter YAML avec `name` et `description`
- ✅ Titre principal (H1)
- ✅ Longueur minimale : 400 caractères (agents), 600 caractères (orchestrators)
- ✅ Au moins un tableau ou bloc de code

### Orchestrators

- ✅ Section "Agents Disponibles"
- ✅ Section "Routage"
