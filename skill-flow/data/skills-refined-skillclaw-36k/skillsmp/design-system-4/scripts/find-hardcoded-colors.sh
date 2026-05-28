#!/bin/bash
# find-hardcoded-colors.sh
# 
# Finds hardcoded Tailwind color classes that should use CSS variables instead.
# Part of the design-system skill.
#
# Usage: ./scripts/find-hardcoded-colors.sh [directory]

DIR="${1:-src}"

echo "🔍 Searching for hardcoded color violations in $DIR..."
echo ""

echo "=== Background Colors (bg-slate, bg-gray, bg-zinc) ==="
grep -rn "bg-slate\|bg-gray\|bg-zinc" "$DIR" --include="*.tsx" --include="*.ts" || echo "  ✅ No violations found"
echo ""

echo "=== Text Colors (text-slate, text-gray, text-zinc) ==="
grep -rn "text-slate\|text-gray\|text-zinc" "$DIR" --include="*.tsx" --include="*.ts" || echo "  ✅ No violations found"
echo ""

echo "=== Border Colors (border-slate, border-gray, border-zinc) ==="
grep -rn "border-slate\|border-gray\|border-zinc" "$DIR" --include="*.tsx" --include="*.ts" || echo "  ✅ No violations found"
echo ""

echo "=== Hex Colors (inline styles) ==="
grep -rn "#[0-9a-fA-F]\{6\}\|#[0-9a-fA-F]\{3\}\b" "$DIR" --include="*.tsx" --include="*.ts" | grep -v "node_modules" || echo "  ✅ No violations found"
echo ""

echo "=== dark: Prefix (should use data-theme instead) ==="
grep -rn "dark:" "$DIR" --include="*.tsx" --include="*.ts" || echo "  ✅ No violations found"
echo ""

echo "---"
echo "If violations found, replace with semantic CSS variables."
echo "See: .agent/skills/design-system/SKILL.md"
