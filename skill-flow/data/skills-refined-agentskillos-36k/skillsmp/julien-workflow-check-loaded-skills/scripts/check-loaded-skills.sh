#!/bin/bash
# Script pour vérifier les skills chargés dans le projet

echo "═══════════════════════════════════════════════════════"
echo "🔍 SKILLS CHARGÉS - Projet Hostinger"
echo "═══════════════════════════════════════════════════════"
echo ""

# Skills globaux
echo "📦 SKILLS GLOBAUX (~/.claude/skills/)"
echo "───────────────────────────────────────────────────────"
GLOBAL_COUNT=$(ls -1 ~/.claude/skills/ 2>/dev/null | wc -l)
echo "Total: $GLOBAL_COUNT skills"
echo ""

# Skills Hostinger
echo "🏢 Skills Hostinger-specific:"
ls -1 ~/.claude/skills/ 2>/dev/null | grep hostinger | sed 's/^/  ✓ /'
echo ""

# Skills Anthropic
ANTHROPIC_COUNT=$(ls -1 ~/.claude/skills/ 2>/dev/null | grep anthropic | wc -l)
echo "🤖 Skills Anthropic: $ANTHROPIC_COUNT"
ls -1 ~/.claude/skills/ 2>/dev/null | grep anthropic | sed 's/^/  ✓ /'
echo ""

# Skills project-level
echo "📁 SKILLS PROJECT-LEVEL (.claude/skills/)"
echo "───────────────────────────────────────────────────────"
if [ -d ".claude/skills" ] && [ "$(ls -A .claude/skills 2>/dev/null)" ]; then
    PROJECT_COUNT=$(ls -1 .claude/skills/ 2>/dev/null | wc -l)
    echo "Total: $PROJECT_COUNT skills"
    ls -1 .claude/skills/ | sed 's/^/  ✓ /'
else
    echo "✅ Aucun skill project-level"
    echo "   → Utilise uniquement les skills globaux"
fi
echo ""

echo "═══════════════════════════════════════════════════════"
echo "✅ Vérification terminée"
echo "═══════════════════════════════════════════════════════"
