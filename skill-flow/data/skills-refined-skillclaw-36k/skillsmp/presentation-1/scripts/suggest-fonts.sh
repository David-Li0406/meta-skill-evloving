#!/bin/bash
# Suggest Google Fonts by language
# Usage: ./suggest-fonts.sh [hebrew|arabic|latin|all]

LANG="${1:-all}"

echo "=== Google Fonts by Language ==="
echo ""

if [[ "$LANG" == "hebrew" || "$LANG" == "all" ]]; then
  echo "HEBREW:"
  echo "-------"
  echo "1. Heebo        - Modern, clean, excellent for UI (recommended)"
  echo "   CSS: family=Heebo:wght@300;400;500;600;700;800;900"
  echo ""
  echo "2. Rubik        - Rounded, friendly, good readability"
  echo "   CSS: family=Rubik:wght@300;400;500;600;700;800;900"
  echo ""
  echo "3. Assistant    - Professional, versatile"
  echo "   CSS: family=Assistant:wght@300;400;500;600;700;800"
  echo ""
  echo "4. Noto Sans Hebrew - Most complete coverage"
  echo "   CSS: family=Noto+Sans+Hebrew:wght@300;400;500;600;700;800;900"
  echo ""
  echo "5. Alef         - Classic, elegant"
  echo "   CSS: family=Alef:wght@400;700"
  echo ""
fi

if [[ "$LANG" == "arabic" || "$LANG" == "all" ]]; then
  echo "ARABIC:"
  echo "-------"
  echo "1. Noto Sans Arabic - Most complete, modern (recommended)"
  echo "   CSS: family=Noto+Sans+Arabic:wght@300;400;500;600;700;800;900"
  echo ""
  echo "2. Cairo        - Clean, contemporary"
  echo "   CSS: family=Cairo:wght@300;400;500;600;700;800;900"
  echo ""
  echo "3. Tajawal      - Modern, rounded"
  echo "   CSS: family=Tajawal:wght@300;400;500;700;800;900"
  echo ""
  echo "4. Amiri        - Traditional, elegant"
  echo "   CSS: family=Amiri:wght@400;700"
  echo ""
fi

if [[ "$LANG" == "latin" || "$LANG" == "all" ]]; then
  echo "LATIN (English, European):"
  echo "--------------------------"
  echo "1. Inter        - Modern, clean, excellent for UI (recommended)"
  echo "   CSS: family=Inter:wght@300;400;500;600;700;800;900"
  echo ""
  echo "2. Roboto       - Google's standard, versatile"
  echo "   CSS: family=Roboto:wght@300;400;500;700;900"
  echo ""
  echo "3. Open Sans    - Friendly, highly readable"
  echo "   CSS: family=Open+Sans:wght@300;400;500;600;700;800"
  echo ""
  echo "4. Poppins      - Geometric, modern"
  echo "   CSS: family=Poppins:wght@300;400;500;600;700;800;900"
  echo ""
  echo "5. Montserrat   - Bold, stylish"
  echo "   CSS: family=Montserrat:wght@300;400;500;600;700;800;900"
  echo ""
fi

echo "=== MONOSPACE (all languages) ==="
echo ""
echo "1. Noto Sans Mono - Best multilingual monospace"
echo "   CSS: family=Noto+Sans+Mono:wght@400;500;600;700"
echo ""
echo "2. JetBrains Mono - Developer favorite"
echo "   CSS: family=JetBrains+Mono:wght@400;500;600;700"
echo ""

echo "=== RECOMMENDATION ==="
echo "Hebrew: Heebo"
echo "Arabic: Noto Sans Arabic"
echo "Latin:  Inter"
echo "Code:   JetBrains Mono or Noto Sans Mono"
