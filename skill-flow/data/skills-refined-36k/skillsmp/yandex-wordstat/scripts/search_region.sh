#!/bin/bash
# Search for region by name

SEARCH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --name|-n) SEARCH="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$SEARCH" ]]; then
    echo "Usage: search_region.sh --name \"city name\""
    echo ""
    echo "Examples:"
    echo "  bash scripts/search_region.sh --name \"Москва\""
    echo "  bash scripts/search_region.sh --name \"Казань\""
    exit 1
fi

echo "Searching for: $SEARCH"
echo ""

# Hardcoded common regions
REGIONS="
225|Россия
159|Казахстан
187|Украина
149|Беларусь
3|Центральный ФО
17|Северо-Западный ФО
40|Приволжский ФО
52|Уральский ФО
59|Сибирский ФО
73|Южный ФО
26|Дальневосточный ФО
1|Москва и область
213|Москва
10716|Московская область
2|Санкт-Петербург
54|Екатеринбург
65|Новосибирск
43|Казань
35|Краснодар
47|Нижний Новгород
39|Ростов-на-Дону
51|Самара
172|Уфа
56|Челябинск
66|Омск
11|Пермь
14|Воронеж
38|Волгоград
37|Саратов
195|Тюмень
"

# Search (case-insensitive)
matches=$(echo "$REGIONS" | grep -i "$SEARCH" || true)

if [[ -z "$matches" ]]; then
    echo "No regions found matching \"$SEARCH\""
    echo ""
    echo "Try running regions_tree.sh to see all common regions"
else
    echo "Found:"
    echo ""
    echo "| ID | Name |"
    echo "|----|------|"
    echo "$matches" | while IFS='|' read -r id name; do
        [[ -n "$id" ]] && echo "| $id | $name |"
    done
fi
