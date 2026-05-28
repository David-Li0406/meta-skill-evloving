#!/bin/bash
# Script de validation du fichier mcp.json
# Usage: ./validate-mcp-config.sh [chemin-vers-mcp.json]

set -e

MCP_FILE="${1:-$HOME/.cursor/mcp.json}"

echo "🔍 Validation du fichier MCP: $MCP_FILE"

# Vérifier que le fichier existe
if [ ! -f "$MCP_FILE" ]; then
    echo "❌ Erreur: Le fichier $MCP_FILE n'existe pas"
    exit 1
fi

# Vérifier que le JSON est valide
if ! jq empty "$MCP_FILE" 2>/dev/null; then
    echo "❌ Erreur: Le fichier JSON n'est pas valide"
    echo "Vérifiez la syntaxe JSON avec: jq . $MCP_FILE"
    exit 1
fi

echo "✅ JSON valide"

# Vérifier la structure de base
if ! jq -e '.mcpServers' "$MCP_FILE" > /dev/null 2>&1; then
    echo "❌ Erreur: La clé 'mcpServers' est manquante"
    exit 1
fi

echo "✅ Structure de base correcte"

# Lister les serveurs configurés
SERVERS=$(jq -r '.mcpServers | keys[]' "$MCP_FILE" 2>/dev/null || echo "")

if [ -z "$SERVERS" ]; then
    echo "⚠️  Aucun serveur configuré"
    exit 0
fi

echo ""
echo "📋 Serveurs configurés:"
echo "$SERVERS" | while read -r server; do
    echo "  - $server"
    
    # Vérifier le type de configuration
    TYPE=$(jq -r ".mcpServers[\"$server\"].type // \"url\"" "$MCP_FILE" 2>/dev/null)
    
    if [ "$TYPE" = "url" ] || [ -z "$TYPE" ]; then
        URL=$(jq -r ".mcpServers[\"$server\"].url // \"\"" "$MCP_FILE" 2>/dev/null)
        if [ -n "$URL" ]; then
            echo "    Type: URL"
            echo "    URL: $URL"
        else
            echo "    ⚠️  URL manquante"
        fi
    elif [ "$TYPE" = "streamable-http" ]; then
        URL=$(jq -r ".mcpServers[\"$server\"].url // \"\"" "$MCP_FILE" 2>/dev/null)
        echo "    Type: Streamable HTTP"
        echo "    URL: $URL"
    else
        COMMAND=$(jq -r ".mcpServers[\"$server\"].command // \"\"" "$MCP_FILE" 2>/dev/null)
        if [ -n "$COMMAND" ]; then
            echo "    Type: Command ($COMMAND)"
        else
            echo "    ⚠️  Configuration incomplète"
        fi
    fi
done

echo ""
echo "✅ Validation terminée"

# Vérifier les tokens secrets (avertissement seulement)
if grep -q "YOUR_.*_TOKEN\|Bearer.*token\|sbp_" "$MCP_FILE" 2>/dev/null; then
    echo ""
    echo "⚠️  ATTENTION: Des tokens ou placeholders sont présents dans le fichier"
    echo "   Assurez-vous de ne pas commiter ce fichier avec des secrets"
fi
