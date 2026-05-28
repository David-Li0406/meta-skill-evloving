#!/bin/bash
# env-audit.sh
# Genera un reporte completo del estado de sincronización de variables de entorno

set -e

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Cargar funciones compartidas
source "$SKILL_DIR/lib/env-functions.sh"

# Variables
OUTPUT_FORMAT="table"  # table | json
ENVIRONMENTS=("production" "preview" "development")

# Parsear argumentos
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      OUTPUT_FORMAT="json"
      shift
      ;;
    --env)
      ENVIRONMENTS=("$2")
      shift 2
      ;;
    --help)
      cat << EOF
Uso: $0 [opciones]

Opciones:
  --json            Generar reporte en formato JSON
  --env <env>       Auditar solo un entorno
  --help            Mostrar esta ayuda

Ejemplos:
  $0                # Auditoría completa en formato tabla
  $0 --json         # Auditoría en formato JSON
  $0 --env production  # Solo production

EOF
      exit 0
      ;;
    *)
      echo -e "${RED}Argumento desconocido: $1${NC}"
      exit 1
      ;;
  esac
done

# Si es JSON, suprimir output de colores
if [[ "$OUTPUT_FORMAT" == "json" ]]; then
  RED=''
  GREEN=''
  YELLOW=''
  BLUE=''
  NC=''
fi

echo -e "${BLUE}🔍 Auditoría de Variables de Entorno${NC}"
echo -e "${BLUE}═══════════════════════════════════${NC}"
echo ""

# 1. Health check
echo "1️⃣  Verificando configuración..."
if ! vercel::env::health_check; then
  exit 1
fi
echo ""

# 2. Obtener variables locales
echo "2️⃣  Analizando archivos locales..."
LOCAL_VARS=$(vercel::env::get_local_vars)
LOCAL_VAR_COUNT=$(echo "$LOCAL_VARS" | wc -l)
echo -e "   ${GREEN}✓${NC} Encontradas $LOCAL_VAR_COUNT variables en .env.example"
echo ""

# 3. Obtener variables de Vercel
echo "3️⃣  Consultando variables en Vercel..."

declare -A VERCEL_VARS

for env in "${ENVIRONMENTS[@]}"; do
  VERCEL_VARS[$env]=$(vercel env ls "$env" 2>/dev/null | tail -n +4 | awk '{print $1}' | sort | uniq || echo "")
  count=$(echo "${VERCEL_VARS[$env]}" | wc -l)
  echo -e "   ${GREEN}✓${NC} $env: $count variables"
done
echo ""

# 4. Generar reporte
echo "4️⃣  Generando reporte..."
echo ""

if [[ "$OUTPUT_FORMAT" == "json" ]]; then
  # Reporte JSON
  echo "{"
  echo "  \"timestamp\": \"$(date -Iseconds)\","
  echo "  \"project\": \"$(vercel::get_project_id)\","
  echo "  \"local_vars\": ["
  
  first=true
  for var in $LOCAL_VARS; do
    [[ "$first" == false ]] && echo ","
    first=false
    echo -n "    {\"name\": \"$var\", \"environments\": {"
    
    env_first=true
    for env in "${ENVIRONMENTS[@]}"; do
      [[ "$env_first" == false ]] && echo -n ", "
      env_first=false
      
      if echo "${VERCEL_VARS[$env]}" | grep -q "^$var$"; then
        echo -n "\"$env\": true"
      else
        echo -n "\"$env\": false"
      fi
    done
    echo -n "}}"
  done
  
  echo ""
  echo "  ]"
  echo "}"
  
else
  # Reporte tabla
  echo -e "${BLUE}┌─────────────────────────────────────────────────────────────────┐${NC}"
  echo -e "${BLUE}│                      REPORTE DE ESTADO                          │${NC}"
  echo -e "${BLUE}└─────────────────────────────────────────────────────────────────┘${NC}"
  echo ""
  
  # Header
  printf "%-35s" "Variable"
  for env in "${ENVIRONMENTS[@]}"; do
    printf " %-15s" "$env"
  done
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # Contadores por entorno
  declare -A MISSING
  for env in "${ENVIRONMENTS[@]}"; do
    MISSING[$env]=0
  done
  
  # Filas
  for var in $LOCAL_VARS; do
    printf "%-35s" "$var"
    
    for env in "${ENVIRONMENTS[@]}"; do
      if echo "${VERCEL_VARS[$env]}" | grep -q "^$var$"; then
        printf " ${GREEN}%-15s${NC}" "✓ Existe"
      else
        printf " ${RED}%-15s${NC}" "✗ Falta"
        MISSING[$env]=$((MISSING[$env] + 1))
      fi
    done
    echo ""
  done
  
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  # Resumen
  echo -e "${BLUE}📊 RESUMEN${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Variables locales (.env.example): $LOCAL_VAR_COUNT"
  echo ""
  
  TOTAL_MISSING=0
  for env in "${ENVIRONMENTS[@]}"; do
    echo "  Faltantes en $env: ${MISSING[$env]}"
    TOTAL_MISSING=$((TOTAL_MISSING + MISSING[$env]))
  done
  echo ""
  
  if [[ $TOTAL_MISSING -eq 0 ]]; then
    echo -e "${GREEN}✅ Todos los entornos están correctamente configurados${NC}"
    echo ""
    exit 0
  else
    echo -e "${YELLOW}⚠️  Hay $TOTAL_MISSING variable(s) faltante(s). Sincroniza con:${NC}"
    echo ""
    echo "  # Todos los entornos"
    echo "  $SKILL_DIR/scripts/env-push.sh --all-envs"
    echo ""
    echo "  # Solo faltantes (sin --force)"
    echo "  $SKILL_DIR/scripts/env-push.sh --all-envs"
    echo ""
    exit 1
  fi
fi
