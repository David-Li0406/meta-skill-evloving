#!/bin/bash
# env-functions.sh
# Funciones compartidas para gestión de variables de entorno de Vercel

# Colores
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

# Variables sensibles que deben marcarse con --sensitive
SENSITIVE_VARS=(
  "DATABASE_URL"
  "BETTER_AUTH_SECRET"
  "NEON_API_KEY"
  "GITHUB_TOKEN"
  "VERCEL_TOKEN"
  "NEXTAUTH_SECRET"
  "API_KEY"
  "API_SECRET"
  "PRIVATE_KEY"
  "SECRET_KEY"
)

# Verificar si Vercel CLI está instalado
vercel::check_cli() {
  if ! command -v vercel &> /dev/null; then
    echo -e "${RED}❌ Vercel CLI no está instalado${NC}"
    echo ""
    echo "Instalar con uno de estos comandos:"
    echo "  pnpm add -g vercel"
    echo "  npm install -g vercel"
    echo "  yarn global add vercel"
    return 1
  fi
  return 0
}

# Verificar autenticación
vercel::authenticated() {
  vercel whoami &>/dev/null
  return $?
}

# Verificar proyecto vinculado
vercel::project_linked() {
  [[ -f .vercel/project.json ]]
  return $?
}

# Obtener project ID
vercel::get_project_id() {
  if vercel::project_linked; then
    grep -o '"projectId":"[^"]*' .vercel/project.json | cut -d '"' -f 4
  fi
}

# Obtener org ID
vercel::get_org_id() {
  if vercel::project_linked; then
    grep -o '"orgId":"[^"]*' .vercel/project.json | cut -d '"' -f 4
  fi
}

# Leer valor de variable de .env.local (con fallback a .env)
vercel::env::get_local_value() {
  local var_name=$1
  local value=""
  
  # Intentar leer de .env.local primero
  if [[ -f .env.local ]]; then
    value=$(grep "^${var_name}=" .env.local 2>/dev/null | cut -d '=' -f 2- | sed 's/^["'\'']//' | sed 's/["'\'']$//' || echo "")
  fi
  
  # Fallback a .env
  if [[ -z "$value" ]] && [[ -f .env ]]; then
    value=$(grep "^${var_name}=" .env 2>/dev/null | cut -d '=' -f 2- | sed 's/^["'\'']//' | sed 's/["'\'']$//' || echo "")
  fi
  
  echo "$value"
}

# Obtener lista de variables de .env.example
vercel::env::get_local_vars() {
  if [[ ! -f .env.example ]]; then
    echo -e "${RED}❌ No se encontró .env.example${NC}" >&2
    return 1
  fi
  
  grep -v '^#' .env.example | grep -v '^$' | cut -d '=' -f 1 | sort | uniq
}

# Verificar si variable existe en Vercel
vercel::env::exists() {
  local var_name=$1
  local env=$2
  
  vercel env ls "$env" 2>/dev/null | tail -n +4 | awk '{print $1}' | grep -q "^${var_name}$"
  return $?
}

# Verificar si variable es sensible
vercel::env::is_sensitive() {
  local var_name=$1
  
  # Verificar si está en la lista de sensibles
  for sensitive_var in "${SENSITIVE_VARS[@]}"; do
    if [[ "$var_name" == "$sensitive_var" ]]; then
      return 0
    fi
  done
  
  # Verificar patrones comunes
  if [[ "$var_name" =~ SECRET|PASSWORD|KEY|TOKEN|PRIVATE ]]; then
    return 0
  fi
  
  return 1
}

# Validar valor según tipo de variable
vercel::env::validate_value() {
  local var_name=$1
  local value=$2
  
  # Verificar que no sea placeholder
  if [[ "$value" =~ ^your-|^changeme|^placeholder|^example ]]; then
    echo -e "${RED}❌ $var_name contiene valor placeholder${NC}" >&2
    return 1
  fi
  
  # Validaciones específicas
  case $var_name in
    BETTER_AUTH_SECRET|NEXTAUTH_SECRET|*_SECRET)
      if [[ ${#value} -lt 32 ]]; then
        echo -e "${RED}❌ $var_name debe tener al menos 32 caracteres${NC}" >&2
        return 1
      fi
      ;;
    *_URL|*_ENDPOINT)
      if [[ ! "$value" =~ ^https?:// ]]; then
        echo -e "${YELLOW}⚠️  $var_name debería ser una URL válida (http:// o https://)${NC}" >&2
      fi
      ;;
    DATABASE_URL)
      if [[ ! "$value" =~ ^postgresql:// ]]; then
        echo -e "${RED}❌ DATABASE_URL debe ser una conexión PostgreSQL válida${NC}" >&2
        return 1
      fi
      ;;
  esac
  
  return 0
}

# Crear/actualizar variable en Vercel
vercel::env::set() {
  local var_name=$1
  local value=$2
  local env=$3
  local force=${4:-false}
  
  # Validar valor
  if ! vercel::env::validate_value "$var_name" "$value"; then
    return 1
  fi
  
  # Determinar si es sensible
  local sensitive_flag=""
  if vercel::env::is_sensitive "$var_name"; then
    sensitive_flag="--sensitive"
  fi
  
  # Verificar si existe
  if vercel::env::exists "$var_name" "$env"; then
    if [[ "$force" == true ]]; then
      # Usar update en lugar de rm + add
      echo -e "${YELLOW}🔄 Actualizando $var_name en $env...${NC}"
      printf "%s\n" "$value" | vercel env update "$var_name" "$env" $sensitive_flag --yes 2>&1 | grep -v "Vercel CLI" || true
    else
      echo -e "${YELLOW}⚠️  $var_name ya existe en $env (usa --force para actualizar)${NC}"
      return 0
    fi
  else
    # Crear nueva variable
    echo -e "${BLUE}📝 Creando $var_name en $env...${NC}"
    printf "%s\n" "$value" | vercel env add "$var_name" "$env" $sensitive_flag --force 2>&1 | grep -v "Vercel CLI" || true
  fi
  
  return 0
}

# Remover variable de Vercel
vercel::env::remove() {
  local var_name=$1
  local env=$2
  
  if vercel::env::exists "$var_name" "$env"; then
    echo -e "${RED}🗑  Removiendo $var_name de $env...${NC}"
    vercel env rm "$var_name" "$env" --yes 2>&1 | grep -v "Vercel CLI" || true
  else
    echo -e "${YELLOW}⚠️  $var_name no existe en $env${NC}"
  fi
}

# Pull variables desde Vercel
vercel::env::pull() {
  local output_file=${1:-.env.local}
  local env=${2:-development}
  local git_branch=${3:-}
  
  local cmd="vercel env pull \"$output_file\" --environment=\"$env\" --yes"
  
  if [[ -n "$git_branch" ]]; then
    cmd="$cmd --git-branch=\"$git_branch\""
  fi
  
  echo -e "${BLUE}⬇️  Descargando variables de $env a $output_file...${NC}"
  eval $cmd
}

# Comparar variables locales vs Vercel
vercel::env::diff() {
  local env=${1:-production}
  
  # Obtener variables locales
  local local_vars=$(vercel::env::get_local_vars)
  
  # Obtener variables de Vercel
  local vercel_vars=$(vercel env ls "$env" 2>/dev/null | tail -n +4 | awk '{print $1}' | sort | uniq)
  
  # Encontrar faltantes
  local missing=()
  for var in $local_vars; do
    if ! echo "$vercel_vars" | grep -q "^$var$"; then
      missing+=("$var")
    fi
  done
  
  # Encontrar extra
  local extra=()
  for var in $vercel_vars; do
    if ! echo "$local_vars" | grep -q "^$var$"; then
      extra+=("$var")
    fi
  done
  
  # Resultado
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo -e "${RED}Faltantes en $env:${NC}"
    printf '  - %s\n' "${missing[@]}"
  fi
  
  if [[ ${#extra[@]} -gt 0 ]]; then
    echo -e "${YELLOW}Extra en $env:${NC}"
    printf '  - %s\n' "${extra[@]}"
  fi
  
  if [[ ${#missing[@]} -eq 0 ]] && [[ ${#extra[@]} -eq 0 ]]; then
    echo -e "${GREEN}✓ Sincronizado${NC}"
    return 0
  fi
  
  return 1
}

# Crear backup de variables actuales
vercel::env::backup() {
  local env=${1:-production}
  local timestamp=$(date +%Y%m%d_%H%M%S)
  local backup_file=".env.backup.${env}.${timestamp}"
  
  echo -e "${BLUE}💾 Creando backup de $env...${NC}"
  vercel env pull "$backup_file" --environment="$env" --yes
  
  echo -e "${GREEN}✓ Backup guardado en $backup_file${NC}"
  echo "$backup_file"
}

# Verificar configuración completa
vercel::env::health_check() {
  local errors=0
  
  echo -e "${BLUE}🏥 Verificación de salud...${NC}"
  echo ""
  
  # 1. Vercel CLI instalado
  if vercel::check_cli; then
    echo -e "  ${GREEN}✓${NC} Vercel CLI instalado"
  else
    ((errors++))
  fi
  
  # 2. Autenticación
  if vercel::authenticated; then
    local user=$(vercel whoami)
    echo -e "  ${GREEN}✓${NC} Autenticado como: $user"
  else
    echo -e "  ${RED}✗${NC} No autenticado"
    ((errors++))
  fi
  
  # 3. Proyecto vinculado
  if vercel::project_linked; then
    local project=$(vercel::get_project_id)
    echo -e "  ${GREEN}✓${NC} Proyecto vinculado: $project"
  else
    echo -e "  ${RED}✗${NC} Proyecto no vinculado"
    ((errors++))
  fi
  
  # 4. Archivo .env.example
  if [[ -f .env.example ]]; then
    local count=$(vercel::env::get_local_vars | wc -l)
    echo -e "  ${GREEN}✓${NC} .env.example existe ($count variables)"
  else
    echo -e "  ${RED}✗${NC} .env.example no encontrado"
    ((errors++))
  fi
  
  echo ""
  
  if [[ $errors -eq 0 ]]; then
    echo -e "${GREEN}✅ Configuración OK${NC}"
    return 0
  else
    echo -e "${RED}❌ $errors error(es) encontrado(s)${NC}"
    return 1
  fi
}

# Exportar funciones
export -f vercel::check_cli
export -f vercel::authenticated
export -f vercel::project_linked
export -f vercel::get_project_id
export -f vercel::get_org_id
export -f vercel::env::get_local_value
export -f vercel::env::get_local_vars
export -f vercel::env::exists
export -f vercel::env::is_sensitive
export -f vercel::env::validate_value
export -f vercel::env::set
export -f vercel::env::remove
export -f vercel::env::pull
export -f vercel::env::diff
export -f vercel::env::backup
export -f vercel::env::health_check
