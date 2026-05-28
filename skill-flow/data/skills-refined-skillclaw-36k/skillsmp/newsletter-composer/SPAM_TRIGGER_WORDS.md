# Spam Trigger Words - Vermeiden!

## Übersicht

Spam-Filter analysieren Subject Lines und Email-Body. Bestimmte Wörter, Phrasen und Muster erhöhen das Spam-Risiko. Diese Liste hilft, sie zu vermeiden.

**Wichtig:** Ein einzelnes Wort löst selten Spam aus. Die Kombination mehrerer Trigger erhöht das Risiko.

---

## Hochrisiko-Wörter

### Geld & Finanzen
```
❌ Kostenlos / Gratis (übermäßig)
❌ €€€ / $$$
❌ Geld verdienen
❌ Reich werden
❌ Schnell Geld
❌ Kredit / Darlehen
❌ Schulden
❌ Einkommen
❌ Bargeld
❌ Gewinn
❌ Provision
❌ Ohne Kosten
❌ Ohne Investition
❌ Finanzielle Freiheit
```

### Dringlichkeit (übertrieben)
```
❌ JETZT!!!
❌ Sofort handeln
❌ Nur heute
❌ Letzte Warnung
❌ Dringend
❌ Begrenzte Zeit
❌ Läuft ab
❌ Nicht verpassen
❌ Einmalige Chance
❌ Nur noch X übrig
```

### Garantien & Versprechen
```
❌ Garantiert
❌ 100% sicher
❌ Risikofrei
❌ Ohne Risiko
❌ Versprochen
❌ Kein Haken
❌ Keine Verpflichtung
❌ Kein Risiko
❌ Erfolg garantiert
```

### Marketing-Buzzwords
```
❌ Unglaublich
❌ Sensationell
❌ Revolutionär
❌ Durchbruch
❌ Geheimnis
❌ Exklusiv (übermäßig)
❌ Limitiert (ohne echte Limitierung)
❌ Einzigartig
❌ Fantastisch
❌ Unschlagbar
```

### Verkaufs-Sprache
```
❌ Kaufen / Jetzt kaufen
❌ Bestellen
❌ Angebot
❌ Rabatt / % Rabatt
❌ Sale
❌ Schnäppchen
❌ Billig
❌ Preiswert
❌ Sonderangebot
❌ Nur heute X% günstiger
```

### Gesundheit & Pharma
```
❌ Abnehmen
❌ Gewichtsverlust
❌ Wundermittel
❌ Heilung
❌ Medikament
❌ Rezeptfrei
❌ Natürlich (im Gesundheitskontext)
❌ Anti-Aging
```

---

## Formatierungs-Trigger

### Überschriften
```
❌ ALLES IN GROSSBUCHSTABEN
❌ Übermäßige Ausrufezeichen!!!
❌ $$$ Symbole $$$
❌ Übermäßige Emojis 🔥🔥🔥🔥🔥
❌ Seltsame Zeichenfolgen: *** FREE ***
```

### Email-Body
```
❌ Nur Bilder, kein Text
❌ Zu viele Links
❌ Versteckte Links
❌ Winziger/unsichtbarer Text
❌ Viele verschiedene Schriftfarben
❌ Übermäßige Formatierung
```

---

## Alternativen zu Spam-Wörtern

| Statt... | Besser... |
|----------|-----------|
| KOSTENLOS | Ohne Kosten für dich / Inklusive |
| Jetzt kaufen! | Mehr erfahren / Entdecken |
| Garantiert | Unsere Erfahrung zeigt... |
| Geheimnis | Was die wenigsten wissen |
| Unglaublich | Bemerkenswert / Interessant |
| Einmalige Chance | Zeitlich begrenzt |
| Geld verdienen | Einnahmen steigern |
| Schnell | Effizient / In kurzer Zeit |
| 100% | Sehr hohe Wahrscheinlichkeit |
| Nur noch heute | Verfügbar bis [Datum] |

---

## Kontextabhängige Wörter

Diese Wörter sind nicht per se Spam, aber im falschen Kontext:

### "Kostenlos"
```
❌ "KOSTENLOS!!! Hol dir jetzt..."
✅ "Dein kostenloser Guide wartet"
✅ "Inklusive: Kostenlose Checkliste"
```

### "Angebot"
```
❌ "MEGA ANGEBOT nur HEUTE!!!"
✅ "Unser neues Angebot für Teams"
✅ "Angebot für Newsletter-Abonnenten"
```

### "Exklusiv"
```
❌ "EXKLUSIV!!! Nur für dich!!!"
✅ "Exklusiver Einblick für unsere Community"
```

---

## Technische Spam-Faktoren

### Absender
- Verifizierte Domain (SPF, DKIM, DMARC)
- Konsistenter "From" Name
- Reply-to Email funktioniert

### Empfängerliste
- Nur Opt-in Kontakte
- Regelmäßige Listen-Hygiene
- Bounces entfernen

### Email-Struktur
- Text-Version vorhanden
- Ausgewogenes Bild-zu-Text-Verhältnis
- Unsubscribe-Link vorhanden
- Physische Adresse im Footer

### Versandverhalten
- Nicht zu viele Emails auf einmal
- Konsistente Versandzeiten
- Warm-up bei neuen Domains

---

## Spam-Score Selbsttest

Vor dem Versand prüfen:

### Subject Line
- [ ] Keine GROSSBUCHSTABEN?
- [ ] Max 1 Ausrufezeichen?
- [ ] Keine €/$ Symbole?
- [ ] Keine hochrisiko Wörter?

### Email Body
- [ ] Text-zu-Bild Verhältnis ok (60/40)?
- [ ] Nicht zu viele Links (<5)?
- [ ] Unsubscribe Link vorhanden?
- [ ] Keine versteckten Elemente?

### Technisch
- [ ] SPF/DKIM konfiguriert?
- [ ] Von vertrauenswürdiger Domain?
- [ ] Reply-to funktioniert?

---

## Tools zum Testen

1. **Mail-Tester.com** - Kostenloses Spam-Score-Tool
2. **GlockApps** - Deliverability Testing
3. **Litmus** - Email Testing Suite
4. **SendForensics** - Spam Analysis

---

## Branchen-spezifische Hinweise

### B2B / SaaS
- "Demo", "Trial", "Pricing" sind okay
- Vorsicht bei "kostenlos" in Kombination

### E-Commerce
- "Sale", "Rabatt" sparsam verwenden
- Preisnennungen okay, aber nicht schreien

### Finanzbranche
- Extra vorsichtig mit Geld-Begriffen
- Compliance-Prüfung empfohlen
