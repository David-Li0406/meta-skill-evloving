#!/bin/bash
# THEhub CSS Auto-Fix Script
# Automatisk ersättning av vanliga inline-styles med utility-klasser

set -e  # Exit on error

# Färger
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}THEhub CSS AUTO-FIX SCRIPT${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Kontrollera att vi är i rätt directory
if [ ! -f "config.php" ]; then
    echo -e "${RED}Fel: Kör detta script från projekt-roten (där config.php finns)${NC}"
    exit 1
fi

# Funktion för att räkna styles i en fil
count_styles() {
    local file=$1
    if [ -f "$file" ]; then
        grep -o 'style="[^"]*"' "$file" 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# Funktion för att fixa en fil
fix_file() {
    local file=$1
    echo -e "${YELLOW}Fixar: ${file}${NC}"

    # Räkna före
    local before=$(count_styles "$file")
    echo -e "  Styles före: ${RED}${before}${NC}"

    # Backup
    cp "$file" "${file}.bak"

    # === SPACING FIXES ===

    # margin-bottom
    sed -i 's/ style="margin-bottom: var(--space-xs);"/ class="mb-xs"/g' "$file"
    sed -i 's/ style="margin-bottom: var(--space-sm);"/ class="mb-sm"/g' "$file"
    sed -i 's/ style="margin-bottom: var(--space-md);"/ class="mb-md"/g' "$file"
    sed -i 's/ style="margin-bottom: var(--space-lg);"/ class="mb-lg"/g' "$file"
    sed -i 's/ style="margin-bottom: var(--space-xl);"/ class="mb-xl"/g' "$file"
    sed -i 's/ style="margin-bottom: 8px;"/ class="mb-xs"/g' "$file"
    sed -i 's/ style="margin-bottom: 16px;"/ class="mb-md"/g' "$file"
    sed -i 's/ style="margin-bottom: 24px;"/ class="mb-lg"/g' "$file"
    sed -i 's/ style="margin-bottom: 32px;"/ class="mb-xl"/g' "$file"

    # margin-top
    sed -i 's/ style="margin-top: var(--space-xs);"/ class="mt-xs"/g' "$file"
    sed -i 's/ style="margin-top: var(--space-sm);"/ class="mt-sm"/g' "$file"
    sed -i 's/ style="margin-top: var(--space-md);"/ class="mt-md"/g' "$file"
    sed -i 's/ style="margin-top: var(--space-lg);"/ class="mt-lg"/g' "$file"
    sed -i 's/ style="margin-top: 12px;"/ class="mt-sm"/g' "$file"
    sed -i 's/ style="margin-top: 24px;"/ class="mt-lg"/g' "$file"

    # margin: 0
    sed -i 's/ style="margin: 0;"/ class="m-0"/g' "$file"
    sed -i 's/ style="margin: 0 0 8px 0;"/ class="mb-xs"/g' "$file"
    sed -i 's/ style="margin: 0 0 24px 0;"/ class="mb-lg"/g' "$file"

    # padding-top
    sed -i 's/ style="padding-top: var(--space-md);"/ class="pt-md"/g' "$file"
    sed -i 's/ style="padding-top: var(--space-lg);"/ class="pt-lg"/g' "$file"

    # === DISPLAY FIXES ===

    # display: none
    sed -i 's/ style="display: none;"/ class="hidden"/g' "$file"

    # text-align
    sed -i 's/ style="text-align: center;"/ class="text-center"/g' "$file"
    sed -i 's/ style="text-align: right;"/ class="text-right"/g' "$file"
    sed -i 's/ style="text-align: left;"/ class="text-left"/g' "$file"

    # === FLEX FIXES ===

    # align-items: center (single property)
    sed -i 's/ style="align-items: center;"/ class="items-center"/g' "$file"

    # === WIDTH FIXES ===

    # width: auto
    sed -i 's/ style="width: auto;"/ class="w-auto"/g' "$file"

    # === COLOR FIXES ===

    # color: var(--color-text-muted)
    sed -i 's/ style="color: var(--color-text-muted);"/ class="text-muted"/g' "$file"
    sed -i 's/ style="color: var(--color-text-secondary);"/ class="text-secondary"/g' "$file"

    # === KOMBINERADE STYLES (vanliga mönster) ===

    # text-center + margin
    sed -i 's/ style="text-align: center; margin: 0 0 24px 0;"/ class="text-center mb-lg"/g' "$file"
    sed -i 's/ style="text-align: center; margin-bottom: 24px;"/ class="text-center mb-lg"/g' "$file"
    sed -i 's/ style="text-align: center; margin-bottom: 16px;"/ class="text-center mb-md"/g' "$file"

    # Räkna efter
    local after=$(count_styles "$file")
    local diff=$((before - after))
    local pct=0
    if [ $before -gt 0 ]; then
        pct=$((100 * diff / before))
    fi

    echo -e "  Styles efter: ${GREEN}${after}${NC}"
    echo -e "  Borttagna: ${GREEN}${diff}${NC} (${pct}%)"

    # Ta bort backup om inga ändringar gjordes
    if [ $before -eq $after ]; then
        rm "${file}.bak"
        echo -e "  ${YELLOW}Inga ändringar${NC}"
    else
        echo -e "  ${GREEN}✓ Backup sparad: ${file}.bak${NC}"
    fi

    echo ""
}

# Funktion för att visa statistik
show_stats() {
    echo -e "${BLUE}=== STATISTIK ===${NC}"
    local total=$(grep -r 'style="' --include="*.php" . 2>/dev/null | wc -l)
    echo -e "Totalt antal kvarvarande styles: ${RED}${total}${NC}"
    echo ""

    echo -e "${BLUE}Top 10 filer med flest styles:${NC}"
    grep -r "style=" --include="*.php" . -l 2>/dev/null | while read file; do
        count=$(grep "style=" "$file" 2>/dev/null | wc -l)
        echo "$count $file"
    done | sort -rn | head -10
    echo ""
}

# === HUVUDMENY ===

if [ "$1" = "auto" ]; then
    # Auto-läge: fixa top 3 filerna
    echo -e "${GREEN}AUTO-LÄGE: Fixar de 3 värsta filerna${NC}"
    echo ""

    # Hitta top 3
    files=$(grep -r "style=" --include="*.php" . -l 2>/dev/null | while read file; do
        count=$(grep "style=" "$file" 2>/dev/null | wc -l)
        echo "$count $file"
    done | sort -rn | head -3 | awk '{print $2}')

    for file in $files; do
        fix_file "$file"
    done

    show_stats

elif [ "$1" = "file" ] && [ -n "$2" ]; then
    # Fixa specifik fil
    if [ ! -f "$2" ]; then
        echo -e "${RED}Fel: Filen $2 finns inte${NC}"
        exit 1
    fi

    fix_file "$2"

elif [ "$1" = "stats" ]; then
    # Visa bara statistik
    show_stats

elif [ "$1" = "batch" ]; then
    # Batch-läge: fixa flera filer
    echo -e "${GREEN}BATCH-LÄGE: Ange filer att fixa${NC}"
    echo "Format: ./css-auto-fix.sh batch file1.php file2.php file3.php"
    echo ""

    shift  # Ta bort "batch" argumentet

    for file in "$@"; do
        if [ -f "$file" ]; then
            fix_file "$file"
        else
            echo -e "${RED}Hoppar över: $file (finns inte)${NC}"
        fi
    done

    show_stats

else
    # Visa hjälp
    echo "Användning:"
    echo "  $0 auto              Fixa de 3 värsta filerna automatiskt"
    echo "  $0 file <filnamn>    Fixa en specifik fil"
    echo "  $0 batch file1 file2 Fixa flera filer"
    echo "  $0 stats             Visa statistik"
    echo ""
    echo "Exempel:"
    echo "  $0 auto"
    echo "  $0 file admin/event-map.php"
    echo "  $0 batch admin/event-map.php organizer/register.php"
    echo "  $0 stats"
    echo ""

    # Visa nuvarande stats
    show_stats
fi

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}Klart!${NC}"
echo -e "${BLUE}================================================${NC}"
