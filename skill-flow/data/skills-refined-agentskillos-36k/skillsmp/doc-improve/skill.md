---
name: doc-improve
description: Forbedrer eksisterende dokumentasjon basert på en URL. Analyserer innhold, kjører språkforbedring og får menneskelig godkjenning.
---

# Forbedre eksisterende dokumentasjon

## Bruk

```
/doc-improve <dokumentasjons-url>
```

Eksempel:
```
/doc-improve https://docs.altinn.studio/nb/notifications/explanation/recipient-lookup/
```

## Instruksjoner

### Steg 1: Parse URL og finn fil

URL-til-fil-mapping:
- URL: `https://docs.altinn.studio/{lang}/{path}/`
- Fil: `repos/altinn-studio-docs/content/{path}/_index.{lang}.md`

**Mapping-tabell:**

| URL-del | Fil-del |
|---------|---------|
| `https://docs.altinn.studio/` | (fjernes) |
| `nb/` eller `en/` | `_index.nb.md` eller `_index.en.md` |
| `notifications/explanation/recipient-lookup/` | `content/notifications/explanation/recipient-lookup/` |

**Eksempel:**
- Input: `https://docs.altinn.studio/nb/notifications/explanation/recipient-lookup/`
- Output: `repos/altinn-studio-docs/content/notifications/explanation/recipient-lookup/_index.nb.md`

Verifiser at repo er klonet:
```bash
ls repos/altinn-studio-docs/content/
```

Hvis ikke klonet:
```bash
cd repos && gh repo clone Altinn/altinn-studio-docs
```

Verifiser at filene eksisterer før du fortsetter.

### Steg 2: Les og analyser innhold

Les begge språkversjoner og analyser for:

1. **Klarhet og struktur**
   - Tydelige overskrifter og logisk hierarki
   - Passende avsnittslengde
   - Riktig Diátaxis-type (tutorial/guide/explanation/reference)

2. **Språk og tone**
   - Aktiv form framfor passiv
   - Konsise setninger uten unødvendige ord
   - Korrekt terminologi (sjekk TERMINOLOGY.md)

3. **Manglende kontekst**
   - Uforklarte begreper eller forkortelser
   - Forutsetninger som ikke er nevnt
   - Manglende bakgrunnsinformasjon

4. **Kryssreferansemuligheter**
   - Relaterte sider som bør lenkes til
   - Manglende lenker til forutsetningsdokumentasjon

### Steg 3: Finn relaterte sider

Søk etter relaterte sider i samme produktområde:

```bash
# Finn andre sider i samme område
ls repos/altinn-studio-docs/content/{produktområde}/

# Søk etter relaterte begreper
grep -r "relevant-begrep" repos/altinn-studio-docs/content/{produktområde}/
```

Noter potensielle kryssreferanser for brukerintervjuet.

### Steg 4: Intervju bruker

Bruk AskUserQuestion-verktøyet for å stille følgende spørsmål:

**Spørsmål 1: Målgruppe**
- Utviklere som integrerer mot API
- Tjenesteeiere som konfigurerer løsninger
- Sluttbrukere
- Annet

**Spørsmål 2: Hva utløste behovet for forbedring?**
- Tilbakemelding fra brukere
- Utdatert innhold
- Manglende informasjon
- Uklart språk
- Annet

**Spørsmål 3: Ønsket omfang**
- Mindre justeringer (språk, formatering)
- Moderat omskriving (struktur, klarhet)
- Omfattende revisjon (nytt innhold, restrukturering)

**Spørsmål 4: Prioriteringer** (multi-select)
- Forbedre klarhet
- Legge til eksempler
- Oppdatere utdatert info
- Legge til kryssreferanser
- Forenkle språk

**Spørsmål 5: Kryssreferanser**
Vis listen over potensielle kryssreferanser fra Steg 3 og spør hvilke som bør inkluderes.

### Steg 5: Forbedre norsk versjon

Basert på analysen og brukerintervjuet:

1. Forbedre klarhet og struktur
2. Legg til manglende kontekst
3. Oppdater terminologi (sjekk TERMINOLOGY.md)
4. Legg til godkjente kryssreferanser
5. Bevar eksisterende innhold som fungerer godt

**Viktig:** Gjør endringer inkrementelt og dokumenter hva du endrer.

### Steg 6: Kjør language-editor-nb

Bruk language-editor-nb agenten for språkvask:

```
Task med subagent_type: "language-editor-nb"
Prompt: "Gjør språkvask av følgende dokumentasjon. Sjekk mot WRITING-GUIDE.md og TERMINOLOGY.md."
```

Implementer forbedringsforslag.

### Steg 7: Kjør Borealis (hvis tilgjengelig)

Sjekk tilgjengelighet:
```bash
python .claude/skills/refine-language/scripts/borealis.py --local --check
```

Hvis tilgjengelig, kjør språkforbedring på nøkkelavsnitt:
```bash
python .claude/skills/refine-language/scripts/borealis.py --local "<avsnitt>"
```

**Viktig:** Hvis Borealis ikke er tilgjengelig, fortsett uten. Språkvask fra language-editor-nb er tilstrekkelig.

### Steg 8: Sjekkpunkt 1 - Norsk review

Send norsk versjon til menneskelig godkjenning:

```
mcp__doc-review__review_documentation med:
- nb_file: <sti til norsk fil>
```

Revieweren kan:
- Se endringer med diff-markering
- Redigere innhold direkte
- Legge til kommentarer
- Godkjenne eller avslå

**Iterer basert på tilbakemeldinger til den norske teksten er godkjent.**

Hvis avslått, hent tilbakemelding:
```
mcp__doc-review__get_review_feedback med:
- nb_file: <sti til norsk fil>
```

### Steg 9: Oppdater engelsk versjon

Overfør endringer fra norsk til engelsk:

1. Les oppdatert norsk versjon
2. Identifiser alle endringer som ble gjort
3. Overfør tilsvarende endringer til engelsk versjon
4. Bytt `/nb/` til `/en/` i alle interne lenker
5. Tilpass til engelsk idiomatikk

Bruk godkjent terminologi fra TERMINOLOGY.md for oversettelser.

### Steg 10: Sjekkpunkt 2 - Begge versjoner

Send begge versjoner til sammenlignende review:

```
mcp__doc-review__review_documentation med:
- nb_file: <sti til norsk fil>
- en_file: <sti til engelsk fil>
```

Revieweren kan sammenligne norsk og engelsk side-by-side.

**Iterer basert på tilbakemeldinger til begge versjoner er godkjent.**

## Todo-liste mal

Bruk TodoWrite-verktøyet for å opprette følgende liste:

1. Parse URL og finn filer
2. Les og analyser innhold
3. Finn relaterte sider for kryssreferanser
4. Intervju bruker om behov og prioriteringer
5. Forbedre norsk versjon
6. Kjør språkvask (language-editor-nb)
7. Kjør Borealis (kun hvis tilgjengelig)
8. Send norsk til review - iterer til godkjent
9. Oppdater engelsk versjon
10. Send begge til review - iterer til godkjent

## Viktige prinsipper

### 1. Norsk først
Gjør alltid endringer i norsk versjon først. Norsk er kildeteksten som engelsk oversettes fra.

### 2. Spør først, gjør endringer etterpå
Brukerintervjuet sikrer at endringene treffer riktig. Ikke gjett hva som trengs.

### 3. Review før oversettelse
Den norske teksten må være godkjent før oversettelse starter. Dette sikrer at oversettelsen starter fra et kvalitetssikret utgangspunkt.

### 4. Bevar eksisterende innhold
Forbedring betyr ikke omskriving fra scratch. Behold det som fungerer og forbedre det som trenger det.

### 5. Ikke blokker på verktøy
Hvis Borealis eller andre verktøy ikke er tilgjengelige, fortsett arbeidsflyten. Språkvask fra language-editor-nb er tilstrekkelig.

## Forskjeller fra doc-workflow

| Aspekt | doc-workflow | doc-improve |
|--------|--------------|-------------|
| Input | GitHub issue URL | Dokumentasjons-URL |
| Formål | Skrive ny dokumentasjon | Forbedre eksisterende |
| Steg 1 | Hent issue-info | Parse URL, finn fil |
| Brukerintervju | Ikke formalisert | Formalisert steg |
| Fokus | Skriving | Analyse og forbedring |
