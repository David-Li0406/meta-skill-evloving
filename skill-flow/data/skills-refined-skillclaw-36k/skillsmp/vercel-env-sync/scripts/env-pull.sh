#!/bin/bash
# env-pull.sh
# Descarga variables de entorno desde Vercel a archivo local
# Uso: ./env-pull.sh [--env production|preview|development] [--output .env.local] [--branch feature-x]

set -e

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Cargar funciones compartidas
source "$SKILL_DIR/lib/env-functions.sh"

# Variables
OUTPUT_FILE=".env.local"
ENVIRONMENT="development"
GIT_BRANCH=""
OVERWRITE=false

# Parsear argumentos
while [[ $# -gt 0 ]]; do
  case $1 in
    --env|--environment)
      ENVIRONMENT="$2"
      shift 2
      ;;
    --output|-o)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --branch|--git-branch)
      GIT_BRANCH="$2"
      shift 2
      ;;
    --yes|-y|--overwrite)
      OVERWRITE=true
      shift
      ;;
    --help)
      cat << EOF
Uso: $0 [opciones]

Opciones:
  --env <env>            Entorno de Vercel (production|preview|development)
                         Default: development
  --output <file>        Archivo de salida
                         Default: .env.local
  --branch <branch>      Git branch específico (solo preview/development)
  --yes                  Sobrescribir archivo existente sin confirmar
  --help                 Mostrar esta ayuda

Ejemplos:
  $0                                    # Pull development a .env.local
  $0 --env production                   # Pull production a .env.local
  $0 --env preview --branch feature-x   # Pull preview del branch feature-x
  $0 --output .env.ci --env preview     # Pull preview a .env.ci

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
echo -e "${BLUE}⬇️  Descargando variables de entorno desde Vercel...${NC}"
echo ""

# Health check básico
if ! vercel::check_cli; then
  exit 1
fi

if ! vercel::authenticated; then
  echo -e "${RED}❌ No estás autenticado en Vercel${NC}"
  echo "Ejecuta: vercel login"
  exit 1
fi

# Verificar si archivo existe
if [[ -f "$OUTPUT_FILE" ]] && [[ "$OVERWRITE" == false ]]; then
  echo -e "${YELLOW}⚠️  El archivo $OUTPUT_FILE ya existe${NC}"
  read -p "¿Sobrescribir? (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operación cancelada"
    exit 0
  fi
fi

# Configuración
echo "🎯 Configuración:"
echo "  Entorno: $ENVIRONMENT"
echo "  Archivo: $OUTPUT_FILE"
[[ -n "$GIT_BRANCH" ]] && echo "  Branch: $GIT_BRANCH"
echo ""

# Pull variables
vercel::env::pull "$OUTPUT_FILE" "$ENVIRONMENT" "$GIT_BRANCH"

echo ""
echo -e "${GREEN}✅ Variables descargadas exitosamente${NC}"
echo ""
echo "📁 Archivo: $OUTPUT_FILE"

# Mostrar count de variables
if [[ -f "$OUTPUT_FILE" ]]; then
  local var_count=$(grep -c '^[A-Z]' "$OUTPUT_FILE" || echo "0")
  echo "📊 Variables: $var_count"
fi

echo ""
echo "💡 Próximos pasos:"
echo "   1. Revisar: cat $OUTPUT_FILE"
echo "   2. Iniciar dev: vercel env run -- pnpm dev"
