---
name: vw-bank-statement-processor
description: Process Volkswagen Bank CSV exports into a single merged CSV file. Use when converting VW Bank statements from the source directory into a format that can be uploaded to Lexoffice.
---

# VW Bank Statement Processor

Process Volkswagen Bank CSV exports into a single merged file, suitable to be uploaded to Lexoffice.

## Source Directory

```
/Users/manuel/Library/CloudStorage/GoogleDrive-manuel@uplink.tech/Meine Ablage/Firma/Kontoauszüge/Volkswagen Bank/
```

## Input Format

VW Bank CSV exports are UTF-16 encoded with tab delimiters. Each file has this structure:

```
"Umsätze vom DD.MM.YYYY bis DD.MM.YYYY"
""
"Saldo DD.MM.YYYY: EUR XX.XXX,XX H"
"Saldo DD.MM.YYYY: EUR XX.XXX,XX H"
""
"Nr."	"Buchungsdatum"	"Verwendungszweck"	"Wertstellung"	"Soll"	"Haben"
"1"	"DD.MM.YYYY"	"Description"	"DD.MM.YYYY"	"amount"	""
...
```

## Processing Steps

1. **Read files from source directory** - Do not copy files, read them into memory
2. **Convert encoding** - Convert from UTF-16 to UTF-8
3. **Remove header lines** - Skip the first 5 lines (title, empty, balances, empty) and keep only from the "Nr." header row onwards
4. **Add column** - Add "Auftraggeber/Empfänger" as a new column with value "VW Bank" in each data row
5. **Merge files** - Combine all files, keeping only one header row
6. **Change delimiter** - Convert from tab-separated to semicolon-separated
7. **Write output** - Save merged file to `~/Downloads/`

## Output Format

Single merged CSV file with semicolon delimiters:

```
"Nr.";"Buchungsdatum";"Verwendungszweck";"Wertstellung";"Soll";"Haben";"Auftraggeber/Empfänger"
"1";"31.07.2025";"Description";"30.07.2025";"18,45";"";"VW Bank"
...
```

## Usage

When invoked, ask the user:
1. Which months/files to process (e.g., "last 6 months", "2025-07 to 2025-12", "all files")
2. Output filename (default: `vw-bank-merged.csv`)

## Example Command

```bash
# Process files in memory and output merged result
for file in 2025-07.csv 2025-08.csv ...; do
  iconv -f UTF-16 -t UTF-8 "$SOURCE_DIR/$file" | tail -n +6
done | awk 'NR==1 || !/^"Nr\."/' | sed 's/$/\t"VW Bank"/' | sed 's/\t/;/g' > ~/Downloads/vw-bank-merged.csv
```

## Notes

- Files are named by month: `2025-01.csv`, `2025-02.csv`, etc.
- The "Nr." column restarts at 1 for each monthly file
- Soll = Debit, Haben = Credit
