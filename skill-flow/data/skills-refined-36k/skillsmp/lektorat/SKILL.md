---
name: lektorat
description: Lektoriere Workshop-Lektionen in `content/` (MDX) nach Korrektheit, Vollständigkeit, Nachvollziehbarkeit und Didaktik. Nutze bei Anfragen wie "lektoriere Abschnitt 3 in Programmieren", "lektoriere sec 2 in praesi" oder "lektoriere React Native in Apps". Liefere eine kurze Liste von Befunden mit Dateiverweisen.
---

# Lektorat

## Ziele

- Fokussiere auf Korrektheit, Vollständigkeit, Nachvollziehbarkeit, Didaktik.
- Prüfe nur MDX-Dateien unter `content/`.
- Liefere kurze, umsetzbare Befunde; keine Voll-Redrafts.
- Ändere keine Inhalte selbst. 

## Bestimme den Abschnitt

- Interpretiere die Nutzerangabe (Bereich wie `prog/`, `web-prog/`, `mobile/`, `praesi/`, Abschnittsnummer oder Thema).
- Nutze `_meta.js` im Zielordner, um Struktur und Reihenfolge zu verstehen.
- Stelle eine Rückfrage, wenn Abschnitt oder Thema mehrdeutig ist.

## Sammle die Dateien

- Erfasse alle MDX-Dateien im Abschnittsordner. 
- `index.mdx` kann ignoriert werden.
- Halte die Reihenfolge gemäß `_meta.js`, falls mehrere Lektionen vorhanden sind.
- Notiere Dateipfade für Referenzen in den Befunden.

## Prüfe die Inhalte

- Prüfe Korrektheit: Fakten, Begriffe, Code-Behauptungen, Versionsangaben, Syntax der Code-Beispiele, Rechtschreibung, Markdown/MDX-Fehler, interne Links und externe URLs.
- Prüfe Vollständigkeit: Fehlen zentrale Schritte, Definitionen, Konzepte, Beispiele? Decken die Lektionen alles Wesentliche zum Thema ab?
- Prüfe Nachvollziehbarkeit: Sprünge, unklare Anweisungen, fehlende Übergänge. Das vorausgesetzte Vorwissen aus den vorigen Abschnitten beachten.
- Prüfe Didaktik: Lernfluss, steigende Komplexität, passende Aufgaben/Beispiele.

## Berichte die Befunde

- Schreibe auf Deutsch.
- Nutze eine kurze Liste; priorisiere Korrektheit, dann Vollständigkeit, Nachvollziehbarkeit, Didaktik.
- Vergebe für jeden Befund eine eindeutige Nummer.
- Formatiere jeden Befund mit Kategorie und Dateipfad.
- Formuliere Unsicherheiten als Frage.
- Antworte mit "Keine Auffälligkeiten gefunden.", falls keine Befunde für eine Lektion oder einen Abschnittvorliegen.

Nutze dieses Format:

```markdown
**[Lektionsname] (`content/.../lektion.mdx`)**

*Korrektheit*

- [K01] Kurzer Befund. (`Abschnitt/Zeile`)
- [K02]Kurzer Befund. (`Abschnitt/Zeile`)

*Vollständigkeit*

Keine Auffälligkeiten gefunden.

*Nachvollziehbarkeit*

- [N01] Kurzer Befund. (`Abschnitt/Zeile`)
- [N02] Kurzer Befund. (`Abschnitt/Zeile`)

*Didaktik*

- [D01] Kurzer Befund. (`Abschnitt/Zeile`)
- [D02] Kurzer Befund. (`Abschnitt/Zeile`)
```