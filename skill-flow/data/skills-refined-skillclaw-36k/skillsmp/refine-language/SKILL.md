---
name: refine-language
description: Forbedrer norske tekster ved hjelp av den norske språkmodellen Borealis (via LM Studio)
---

# Forbedre tekst med Borealis

Forbedrer norske tekster ved hjelp av den norske språkmodellen Borealis (via LM Studio eller ekstern server).

## Instruksjoner

### Steg 1: Sjekk tilgjengelighet først

**Før du forsøker å forbedre tekst**, verifiser at tjenesten er tilgjengelig:

```bash
python .claude/skills/refine-language/scripts/borealis.py --check
```

Hvis dette feiler, informer brukeren og hopp over Borealis-steget i arbeidsflyten. Ikke bruk tid på å feilsøke - gå videre til neste steg.

### Steg 2: Forbedre tekst

Hvis tilkoblingssjekken er OK, kjør:

```bash
python .claude/skills/refine-language/scripts/borealis.py "<teksten som skal forbedres>"
```

### Steg 3: Vurder og implementer

1. Vurder forslagene kritisk
2. Vis resultatet til brukeren
3. Implementer forbedringene i dokumentasjonen

## Kommandolinje-alternativer

| Alternativ | Beskrivelse |
|------------|-------------|
| `--check` | Sjekk om tjenesten er tilgjengelig (kjør dette først!) |
| `--local` | Bruk lokal LM Studio (ignorerer .env-fil) |
| `--api-url URL` | Overstyr API-endepunkt |
| `--model NAVN` | Overstyr modellnavn |
| `--show-config` | Vis gjeldende konfigurasjon |

## Konfigurasjonsprioritet

1. CLI-argumenter (høyest prioritet)
2. Miljøvariabler (`BOREALIS_API_URL`, `BOREALIS_MODEL`)
3. `.env`-fil i scripts-mappen
4. Standardverdier (lokal LM Studio)

## Bruk i dokumentasjonsarbeidsflyten

Denne skill-en brukes i fase 2 av dokumentasjonsarbeidsflyten:
1. Etter at første utkast på norsk er skrevet
2. Etter language-editor-nb agenten har gjort språkvask
3. Før menneskelig godkjenning (sjekkpunkt 1)

**Viktig:** Hvis Borealis ikke er tilgjengelig, skal arbeidsflyten fortsette uten den. Språkvask fra language-editor-nb agenten er tilstrekkelig for å gå videre til review.

## Feilhåndtering

Hvis `--check` feiler:
- Lokal: Start LM Studio og last inn modellen `borealis-4b-instruct-preview`
- Ekstern: Sjekk at serveren kjører og at .env-filen har riktig URL

**Ikke bruk tid på feilsøking** - gå videre til neste steg i arbeidsflyten.
