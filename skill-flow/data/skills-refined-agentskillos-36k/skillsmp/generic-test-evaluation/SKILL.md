---
name: generic-test-evaluation
description: Document and evaluate tests using the generic test files, and explain why the match score was reached. Use when validating the app with `generic test files/` inputs or when recording test evidence.
---

# Skill: generic-test-evaluation

## Zweck
Fuehre reproduzierbare Tests mit den generischen Testdateien aus und dokumentiere, warum ein Match-Score zustande kommt.

## Wann anwenden
- Wenn die App mit den Beispieldateien validiert wird.
- Wenn eine nachvollziehbare Begruendung fuer den Match-Score benoetigt wird.

## Vorgehen (Schritt-fuer-Schritt)
1) Verwende die Dateien in `generic test files/` als Eingaben (CV und JD).
2) Fuehre die Core-Pipeline aus (`CVAnalyzer`, `SkillExtractor`, `ATSCriteriaExtractor`, `JDParser`, `BaselineMatcher`).
3) Notiere:
   - erkannte Abschnitte und Skills
   - fehlende ATS-Felder
   - erkannte JD-Felder
   - Match-Score und Breakdown
4) Erklaere den Score anhand des Breakdowns (welche Kriterien erfuellt/fehlend sind).
5) Lege einen Testbericht in `docs/04_evaluation/` ab (Timestamp oder Versionierung).

## Lernperspektive
- Warum so? Die generischen Testfiles sind deterministisch und liefern reproduzierbare Resultate.
- Alternativen: Ad-hoc manuelle Tests ohne Protokoll.
- Warum nicht hier? Ohne strukturiertes Protokoll ist der Score schwer nachvollziehbar.

## Repo-Referenzen
- `generic test files/`
- `src/core/`
- `tests/`
- `docs/04_evaluation/`

## Qualitaetscheck
- Eingaben stammen aus `generic test files/`.
- Score-Begruendung ist aus dem Breakdown ableitbar.
- Bericht nennt Dateipfade und Datum.
