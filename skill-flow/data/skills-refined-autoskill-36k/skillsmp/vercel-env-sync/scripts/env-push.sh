#!/bin/bash
# env-push.sh
# Sincroniza variables de entorno desde archivos locales a Vercel
# Uso: ./env-push.sh [--env production|preview|development] [--all-envs] [--force] [--dry-run]

set -e

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Cargar funciones compartidas
source "$SKILL_DIR/lib/env-functions.sh"

# Variables
DRY_RUN=false
ENVIRONMENTS=("production")  # Default: solo production
FORCE=false
BACKUP_BEFORE=true

# Función principal de sincronización
sync_var() {
  local var_name=$1
  local env=$2
  
  # Obtener valor local
  local value=$(vercel::env::get_local_value "$var_name")
  
  if [[ -z "$value" ]]; then
    echo -e "${YELLOW}⚠️  $var_name no tiene valor en archivos locales (.env/.env.local)${NC}"
    return 0  # No es un error crítico, solo skip
  fi
  
  # Dry run mode
  if [[ "$DRY_RUN" == true ]]; then
    local action="crear"
    if vercel::env::exists "$var_name" "$env"; then
      action="actualizar"
    fi
    
    local sensitive_mark=""
    if vercel::env::is_sensitive "$var_name"; then
      sensitive_mark=" [SENSITIVE]"
    fi
    
    echo -e "${BLUE}[DRY RUN]${NC} $action $var_name en $env$sensitive_mark"
    return 0
  fi
  
  # Sincronizar
  vercel::env::set "$var_name" "$value" "$env" "$FORCE"
}

# Parsear argumentos
while [[ $# -gt 0 ]]; do
  case $1 in
    --env)
      ENVIRONMENTS=("$2")
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --all-envs)
      ENVIRONMENTS=("production" "preview" "development")
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --no-backup)
      BACKUP_BEFORE=false
      shift
      ;;
    --help)
      cat << EOF
Uso: $0 [opciones]

Opciones:
  --env <env>        Sincronizar solo un entorno (production|preview|development)
  --all-envs         Sincronizar todos los entornos
  --force            Forzar actualización de variables existentes
  --dry-run          Simular cambios sin aplicarlos
  --no-backup        No crear backup antes de sincronizar
  --help             Mostrar esta ayuda

Ejemplos:
  $0                          # Sincronizar solo production
  $0 --env preview            # Sincronizar solo preview
  $0 --all-envs               # Sincronizar todos los entornos
  $0 --all-envs --force       # Forzar actualización en todos
  $0 --dry-run                # Ver qué cambios se harían

Variables de entorno:
  VERCEL_TOKEN               Token de autenticación (opcional)

EOF
      exit 0
      ;;
    *)
      echo -e "${RED}Argumento desconocido: $1${NC}"
      echo "Usa --help para ver las opciones disponibles"
      exit 1
      ;;
  esac
done

# Main script
echo -e "${BLUE}🚀 Sincronizando variables de entorno con Vercel...${NC}"
echo ""

# Health check
if ! vercel::env::health_check; then
  exit 1
fi

echo ""

# Mostrar configuración
echo "🎯 Configuración:"
echo "  Entornos: ${ENVIRONMENTS[*]}"
echo "  Forzar actualización: $FORCE"
echo "  Dry run: $DRY_RUN"
echo "  Backup automático: $BACKUP_BEFORE"
echo ""

# Obtener variables a sincronizar
VARS=$(vercel::env::get_local_vars)
if [[ -z "$VARS" ]]; then
  echo -e "${RED}❌ No se encontraron variables en .env.example${NC}"
  exit 1
fi

# Verificar archivos de valores
if [[ ! -f .env.local ]] && [[ ! -f .env ]]; then
  echo -e "${YELLOW}⚠️  No se encontró .env.local ni .env${NC}"
  echo -e "${YELLOW}   Las variables sin valor en estos archivos serán omitidas${NC}"
  echo ""
fi

# Crear backups si no es dry-run
if [[ "$BACKUP_BEFORE" == true ]] && [[ "$DRY_RUN" == false ]]; then
  echo -e "${BLUE}💾 Creando backups...${NC}"
  for env in "${ENVIRONMENTS[@]}"; do
    vercel::env::backup "$env"
  done
  echo ""
fi

# Sincronizar cada variable en cada entorno
TOTAL=0
SUCCESS=0
SKIPPED=0
FAILED=0

for env in "${ENVIRONMENTS[@]}"; do
  echo -e "\n${BLUE}📦 Procesando entorno: $env${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  for var in $VARS; do
    TOTAL=$((TOTAL + 1))
    
    # Obtener valor para determinar si skip
    value=$(vercel::env::get_local_value "$var")
    
    if sync_var "$var" "$env"; then
      if [[ -n "$value" ]]; then
        SUCCESS=$((SUCCESS + 1))
      else
        SKIPPED=$((SKIPPED + 1))
      fi
    else
      FAILED=$((FAILED + 1))
    fi
  done
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [[ "$DRY_RUN" == true ]]; then
  echo -e "${YELLOW}🔍 Dry Run Completado${NC}"
else
  echo -e "${GREEN}✓ Completado${NC}"
fi

echo "  Total: $TOTAL operaciones"
echo "  Exitosas: $SUCCESS"
echo "  Omitidas: $SKIPPED (sin valor local)"
echo "  Fallidas: $FAILED"

if [[ $FAILED -gt 0 ]]; then
  exit 1
fi

echo ""

if [[ "$DRY_RUN" == false ]]; then
  echo -e "${GREEN}✅ Sincronización completada exitosamente${NC}"
  echo ""
  echo "💡 Próximos pasos:"
  echo "   1. Verificar: $SKILL_DIR/scripts/env-audit.sh"
  echo "   2. Pull local: vercel env pull .env.local"
  echo "   3. Deploy: vercel --prod"
else
  echo ""
  echo "💡 Para aplicar cambios, ejecuta sin --dry-run:"
  echo "   $0 ${ENVIRONMENTS[*]/#/--env }"
fi
