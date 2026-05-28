Dette er info til menneske-brukeren, ikke Claude/AI-agenter

Skill-et er ment for å benyttes med en "norsk" språkmodell, f.eks https://huggingface.co/NbAiLab/borealis-4b-instruct-preview
 
- .env.example - mal med dokumentasjon som brukere kan kopiere og sette opp med egne/ønskede endepunkt
- .gitignore - sikrer at .env ikke committes
- borealis.py (wrapper som kaller modellen med riktig konfigurasjon)

Prioritetsrekkefølge for konfigurasjon:
1. Miljøvariabler (BOREALIS_API_URL, BOREALIS_MODEL)
2. .env-fil i scripts-mappen
3. Innebygde standardverdier (localhost:1234, borealis-4b-instruct-preview)

For å bruke lokalt LM Studio kan en bruker lage .env med:
BOREALIS_API_URL=http://min-ai-server.example.com/v1/chat/completions
BOREALIS_MODEL=borealis-4b-instruct-preview


Se også [SKILL.md](../SKILL.md) for funksjonell forklaring