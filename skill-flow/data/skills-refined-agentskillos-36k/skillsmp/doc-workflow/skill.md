---
name: doc-workflow
description: Starter dokumentasjonsarbeidsflyt for en GitHub issue. Setter opp todo-liste og verifiserer at verktøy er tilgjengelige.
---

# Dokumentasjonsarbeidsflyt

Starter en strukturert arbeidsflyt for å løse en GitHub issue som krever dokumentasjon.

## Bruk

```
/doc-workflow <github-issue-url>
```

Eksempel:
```
/doc-workflow https://github.com/Altinn/altinn-notifications/issues/1232
```

## Instruksjoner

Når brukeren starter denne skill-en:

### Steg 1: Hent issue-informasjon

```bash
gh issue view <issue-nummer> --repo <owner/repo>
```

Ekstraher:
- Tittel og beskrivelse
- Akseptkriterier
- Refererte issues (se etter `#nummer`)
- Labels (for å forstå type: dokumentasjon, feature, bug, etc.)

### Steg 2: Sjekk verktøy

Verifiser at nødvendige verktøy er tilgjengelige:

```bash
# Sjekk Borealis
python .claude/skills/refine-language/scripts/borealis.py --local --check
```

Rapporter status til brukeren. Hvis Borealis ikke er tilgjengelig, informer om at det steget vil bli hoppet over.

### Steg 3: Sett opp todo-liste

Bruk TodoWrite-verktøyet for å opprette følgende standardoppgaver:

1. **Analyser issue og eksisterende dokumentasjon** - Les issue, sjekk refererte issues, finn eksisterende docs
2. **Skriv norsk versjon** - Følg Diátaxis-modellen
3. **Kjør språkvask (language-editor-nb)** - Bruk Task med subagent_type="language-editor-nb"
4. **Kjør Borealis** (kun hvis tilgjengelig) - Bruk /refine-language skill
5. **Send norsk til review** - Bruk doc-review MCP-verktøyet FØR oversettelse
6. **Oversett til engelsk** - Etter godkjenning av norsk
7. **Send begge til review** - Sammenlign norsk og engelsk

### Steg 4: Start arbeidet

Etter oppsettet, start umiddelbart på første oppgave (analyser issue).

## Viktige prinsipper

1. **Norsk først** - Skriv alltid norsk versjon før engelsk
2. **Review før oversettelse** - Send norsk til menneskelig godkjenning FØR oversettelse
3. **Ikke blokker på verktøy** - Hvis Borealis er utilgjengelig, fortsett uten
4. **Oppdater todo-liste kontinuerlig** - Marker oppgaver som in_progress/completed underveis

## Tilpassing av oppgaver

Basert på issue-typen, tilpass todo-listen:

**Ny dokumentasjon:**
- Alle steg som beskrevet over

**Oppdatering av eksisterende:**
- Hopp over "Skriv norsk versjon", bruk "Oppdater norsk versjon"

**Oversettelse:**
- Hopp over skriving, fokuser på oversettelse og review

**Feilretting:**
- Enklere todo-liste med færre steg
