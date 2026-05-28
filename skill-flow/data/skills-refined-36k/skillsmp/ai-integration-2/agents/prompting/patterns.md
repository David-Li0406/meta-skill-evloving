---
name: prompting-patterns
description: Expert patterns de prompts - Few-shot, Chain-of-Thought, ReAct, et techniques avancees
---

# Prompt Engineering Patterns

Tu es expert en **prompt engineering** et techniques d'optimisation.

## Principes Fondamentaux

1. **Etre specifique** : Instructions claires et detaillees
2. **Donner du contexte** : Role, domaine, contraintes
3. **Structurer** : Format attendu, sections
4. **Iterer** : Tester et affiner

## Zero-Shot Prompting

Pour taches simples sans exemples.

```typescript
const prompt = `Tu es un expert en SEO.

Analyse le titre suivant et suggere 3 ameliorations:
Titre: "${title}"

Pour chaque suggestion, explique pourquoi elle ameliore le SEO.`;
```

## Few-Shot Prompting

Fournir des exemples pour guider le format.

```typescript
const prompt = `Tu es un classificateur de sentiment.

Exemples:
- "J'adore ce produit!" → positif
- "Tres decu, ne fonctionne pas" → negatif
- "Ca fait le job" → neutre

Classifie ce commentaire:
"${comment}"

Reponds uniquement par: positif, negatif ou neutre`;
```

### Few-Shot avec Format Complexe

```typescript
const prompt = `Tu extrais des informations structurees.

Exemples:

Input: "Jean Dupont, 35 ans, developpeur chez Acme Corp"
Output:
{
  "nom": "Jean Dupont",
  "age": 35,
  "poste": "developpeur",
  "entreprise": "Acme Corp"
}

Input: "Marie Martin travaille comme designer, elle a 28 ans"
Output:
{
  "nom": "Marie Martin",
  "age": 28,
  "poste": "designer",
  "entreprise": null
}

Input: "${input}"
Output:`;
```

## Chain-of-Thought (CoT)

Pour raisonnement complexe.

### Explicite

```typescript
const prompt = `Resous ce probleme etape par etape.

Probleme: ${problem}

Reflechis methodiquement:
1. Identifie les donnees
2. Determine l'approche
3. Execute les calculs
4. Verifie le resultat

Solution:`;
```

### Zero-Shot CoT

```typescript
const prompt = `${question}

Reflechissons etape par etape.`;
```

### CoT avec Verification

```typescript
const prompt = `${question}

Suis ce processus:
1. ANALYSE: Comprends le probleme
2. PLAN: Definis ta strategie
3. EXECUTION: Resous etape par etape
4. VERIFICATION: Verifie ta reponse
5. REPONSE: Donne la reponse finale`;
```

## ReAct (Reasoning + Acting)

Pour agents avec outils.

```typescript
const prompt = `Tu es un assistant avec acces a des outils.

Outils disponibles:
- search(query): Recherche sur internet
- calculator(expression): Calcule une expression
- weather(city): Obtient la meteo

Format de reponse:
Thought: [ton raisonnement]
Action: [outil a utiliser]
Action Input: [parametre de l'outil]

Apres avoir recu le resultat:
Thought: [analyse du resultat]
... (repete si necessaire)
Final Answer: [reponse finale]

Question: ${question}`;
```

## Self-Consistency

Generer plusieurs reponses et voter.

```typescript
async function selfConsistency(
  prompt: string,
  n: number = 5
): Promise<string> {
  // Generer n reponses avec temperature elevee
  const responses = await Promise.all(
    Array(n).fill(null).map(() =>
      llm.invoke(prompt, { temperature: 0.7 })
    )
  );

  // Extraire les reponses finales
  const answers = responses.map(r => extractFinalAnswer(r));

  // Voter pour la plus frequente
  const counts = answers.reduce((acc, ans) => {
    acc[ans] = (acc[ans] || 0) + 1;
    return acc;
  }, {});

  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])[0][0];
}
```

## Role Prompting

Definir un persona expert.

```typescript
const systemPrompt = `Tu es un architecte logiciel senior avec 15 ans d'experience.

EXPERTISE:
- Architecture microservices
- Domain-Driven Design
- Cloud (AWS, GCP)
- Performance et scalabilite

STYLE:
- Reponds de maniere structuree
- Donne des recommandations concretes
- Mentionne les trade-offs
- Cite des patterns reconnus

CONTRAINTES:
- Reste dans ton domaine d'expertise
- Si hors sujet, redirige poliment`;
```

## Output Formatting

### JSON Mode

```typescript
const prompt = `Analyse ce texte et retourne un JSON.

Texte: "${text}"

Retourne UNIQUEMENT un JSON valide avec cette structure:
{
  "summary": "resume en 1 phrase",
  "keywords": ["mot1", "mot2", "mot3"],
  "sentiment": "positif|negatif|neutre",
  "confidence": 0.0-1.0
}`;
```

### Markdown Structure

```typescript
const prompt = `Redige une analyse.

## Resume
[2-3 phrases]

## Points Cles
- Point 1
- Point 2
- Point 3

## Recommandations
1. Recommandation 1
2. Recommandation 2

## Conclusion
[1 phrase]`;
```

## Techniques Avancees

### Decomposition

```typescript
const prompt = `Decompose cette tache complexe en sous-taches:

Tache: ${complexTask}

Pour chaque sous-tache:
1. Description claire
2. Inputs necessaires
3. Output attendu
4. Dependances`;
```

### Critique et Amelioration

```typescript
const prompt = `Voici une premiere version:

${draft}

Critique cette version:
1. Points forts
2. Points faibles
3. Erreurs potentielles

Puis propose une version amelioree.`;
```

### Meta-Prompting

```typescript
const prompt = `Tu es un expert en prompt engineering.

Cree un prompt optimise pour cette tache:
${taskDescription}

Le prompt doit:
- Etre clair et specifique
- Inclure des exemples si utile
- Definir le format de sortie
- Anticiper les edge cases`;
```

## Anti-Patterns

| Anti-Pattern | Probleme | Solution |
|--------------|----------|----------|
| Prompt vague | Reponses inconsistantes | Etre specifique |
| Trop d'instructions | Confusion | Prioriser, simplifier |
| Pas d'exemples | Mauvais format | Few-shot |
| Ignorer le contexte | Hallucinations | Fournir le contexte |
| Pas de contraintes | Reponses trop longues | Limiter format/longueur |

## Voir Aussi

- `prompting/templates` pour gestion de templates
- `prompting/output-parsing` pour parsing
- `prompting/testing` pour evaluation
