# Flexibel CSV-import - Användarguide

## 🎯 Översikt

Den flexibla importen är den **enklaste** och **mest kraftfulla** importfunktionen i TheHUB. Den låter dig importera deltagardata från vilken CSV-källa som helst, oavsett kolumnordning eller format.

## ✨ Nyckelfunktioner

### 1. **Kolumnordning spelar ingen roll**
Du kan ha kolumnerna i **vilken ordning som helst** - systemet känner automatiskt igen dem!

**Exempel 1:**
```csv
Förnamn,Efternamn,Email,Klubb
Lars,Nordenson,lars@example.com,Ringmurens CK
```

**Exempel 2 (samma data, annan ordning):**
```csv
Email,Klubb,Efternamn,Förnamn
lars@example.com,Ringmurens CK,Nordenson,Lars
```

Båda fungerar perfekt! ✅

### 2. **Okända kolumner ignoreras automatiskt**
Har din CSV extra kolumner som inte behövs? Inga problem - de ignoreras bara!

```csv
Förnamn,Efternamn,Intern ID,Medlemsnummer,Klubb,Glöm denna
Lars,Nordenson,12345,ABC123,Ringmurens CK,Data vi inte vill ha
```

Systemet plockar ut `Förnamn`, `Efternamn` och `Klubb` - resten ignoreras. ✅

### 3. **Automatisk separatordetektering**
Fungerar med:
- Komma (`,`)
- Semikolon (`;`)
- Tabulator (`\t`)

Systemet upptäcker automatiskt vilken separator din fil använder!

### 4. **Förhandsgranska innan import**
Klicka på "Förhandsgranska" för att se:
- Vilka kolumner systemet känner igen
- Vilka kolumner som ignoreras
- Hur mappningen ser ut

Detta ger dig **full kontroll** innan du importerar!

### 5. **Flexibla kolumnnamn**
Systemet känner igen kolumner på **både svenska och engelska**, med eller utan mellanslag/understreck:

| Du skriver | Systemet känner igen som |
|------------|-------------------------|
| `Förnamn` | firstname |
| `First Name` | firstname |
| `first_name` | firstname |
| `FirstName` | firstname |
| `Födelsedatum` | personnummer |
| `Date of Birth` | personnummer |
| `UCI Kod` | ucicode |
| `UCI ID` | ucicode |
| `uci_code` | ucicode |

## 🚀 Snabbstart

### Steg 1: Förbered din CSV
Du behöver **minst** dessa kolumner:
- `Förnamn` (eller `First Name`, `Firstname`, etc.)
- `Efternamn` (eller `Last Name`, `Lastname`, etc.)

Allt annat är valfritt!

### Steg 2: Exportera från ditt system
- **Excel**: Spara som → CSV (kommaseparerad)
- **Google Sheets**: Fil → Ladda ner → CSV
- **Numbers**: Exportera → CSV

### Steg 3: Ladda upp
1. Gå till `/admin/import-riders-flexible.php`
2. Välj din CSV-fil
3. Klicka "Förhandsgranska" (rekommenderat!)
4. Granska kolumnmappningen
5. Klicka "Importera"

Klart! 🎉

## 📋 Exempel

### Exempel 1: Minimal CSV (kommaseparerad)
```csv
Förnamn,Efternamn,Email,Klubb
Lars,Nordenson,lars@example.com,Ringmurens CK
Anna,Karlsson,anna@example.com,CK Olympia
```

### Exempel 2: Utökad CSV med extra kolumner (semikolonseparerad)
```csv
Efternamn;Förnamn;Internt ID;Medlemsnummer;Email;Telefon;Klubb;Status
Nordenson;Lars;12345;M001;lars@example.com;070-1111111;Ringmurens CK;Aktiv
Karlsson;Anna;12346;M002;anna@example.com;070-2222222;CK Olympia;Aktiv
```

Kolumnerna "Internt ID", "Medlemsnummer" och "Status" ignoreras automatiskt.

### Exempel 3: Engelska kolumnnamn (tabulator-separerad)
```csv
First Name	Last Name	City	Birth Year	Gender	Club Name	License Number
Lars	Nordenson	Stånga	1940	M	Ringmurens CK	101 637 581 11
Anna	Karlsson	Stockholm	1985	F	CK Olympia	101 234 567 89
```

### Exempel 4: Komplett med grenar
```csv
Förnamn,Efternamn,Klubb,UCI Kod,Road,MTB,Gravel,Track,BMX
Lars,Nordenson,Ringmurens CK,101 637 581 11,Road,,Gravel,,
Anna,Karlsson,CK Olympia,101 234 567 89,Road,MTB,Gravel,,
```

Markera grenar genom att fylla i kolumnen (tomt = ingen, valfritt värde = ja).

## 🎓 Igenkända Kolumnnamn

### Obligatoriska
- **Förnamn**: `Förnamn`, `Fornamn`, `First Name`, `Firstname`, `fname`
- **Efternamn**: `Efternamn`, `Last Name`, `Lastname`, `Surname`

### Personuppgifter
- **Personnummer**: `Födelsedatum`, `Personnummer`, `PNR`, `SSN`, `Date of Birth` — **Note: Parsed to extract birth_year only, NOT stored in database**
- **Födelseår**: `Födelseår`, `Birth Year`, `Year`, `Ålder`, `Age`
- **Kön**: `Kön`, `Gender`, `Sex`

### Kontakt (PRIVAT)
- **Email**: `Epost`, `Email`, `E-post`, `Mail`
- **Telefon**: `Telefon`, `Phone`, `Tel`, `Mobile`
- **Nödkontakt**: `Emergency Contact`, `Nödkontakt`

### Adress (PRIVAT)
- **Adress**: `Postadress`, `Address`, `Street Address`
- **Postnummer**: `Postnummer`, `Postal Code`, `Zip Code`, `Zip`
- **Ort**: `Ort`, `Stad`, `City`
- **Land**: `Land`, `Country`

### Organisation
- **Klubb**: `Klubb`, `Club`, `Huvudförening`, `Club Name`
- **Team**: `Team`, `Lag`
- **Distrikt**: `Distrikt`, `District`, `Region`

### Licens
- **UCI Kod**: `UCI Kod`, `UCI ID`, `UCI Code`, `License Number`, `Licens`
- **Licenstyp**: `Licenstyp`, `License Type`
- **Kategori**: `Kategori`, `Category`
- **Licensår**: `Licensår`, `License Year`

### Grenar
- **Road**: `Road`, `Landsväg`
- **MTB**: `MTB`, `Mountain Bike`
- **Gravel**: `Gravel`
- **CX**: `CX`, `Cyclocross`
- **Track**: `Track`, `Bana`
- **BMX**: `BMX`
- **Trial**: `Trial`
- **Para**: `Para`
- **E-cycling**: `E-cycling`

## 🔒 Sekretess

Följande fält är **PRIVATA** och visas ALDRIG publikt:
- Adress
- Postnummer
- Telefon
- Nödkontakt

**Obs:** Personnummer lagras INTE i databasen. Det används endast vid import för att extrahera födelseår.

Dessa fält används endast för:
- Intern administration
- Autofyll vid bokning (för deltagaren själv)

## ❓ FAQ

### Varför känner systemet inte igen min kolumn?
1. Kontrollera stavningen
2. Kolla "Igenkända Kolumnnamn" ovan
3. Använd "Förhandsgranska" för att se vad systemet känner igen

### Kan jag ha svenska och engelska kolumnnamn i samma fil?
Ja! Systemet känner igen båda språken samtidigt.

### Vad händer om jag har flera kolumner som mappas till samma fält?
Den första kolumnen används. Exempel: Om du har både `Förnamn` och `First Name` används `Förnamn` (den som kommer först).

### Kan jag importera samma fil flera gånger?
Ja! Systemet uppdaterar befintliga deltagare baserat på:
1. UCI-kod (om finns)
2. Namn + födelseår (fallback)

### Vad händer med tomma fält?
Tomma fält sätts till `NULL` i databasen och påverkar inte befintliga data vid uppdatering.

## 📁 Testfiler

Se `docs/` för exempel:
- `example_flexible_1.csv` - Kommaseparerad, blandad ordning
- `example_flexible_2.csv` - Semikolonseparerad, extra kolumner

## 🆘 Support

Problem? Kontrollera:
1. Att filen är sparad som CSV (inte Excel)
2. Att den har kolumnerna `Förnamn` och `Efternamn`
3. Att encoding är UTF-8 för svenska tecken

För mer hjälp, se `/docs/EXTENDED_IMPORT_GUIDE.md`

---

**Last Updated:** 2025-12-01
**Version:** 1.1

### Changelog
- 2025-12-01: Updated to clarify personnummer is NOT stored (only birth_year is extracted)
