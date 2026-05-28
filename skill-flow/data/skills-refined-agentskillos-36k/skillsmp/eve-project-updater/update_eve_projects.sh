#!/bin/bash
# ============================================================================
# EVE Project Master Updater
# ============================================================================
# Updates all EVE projects with ESI integration, compliance fixes, and assets.
#
# Usage:
#   ./update_eve_projects.sh                    # Interactive mode
#   ./update_eve_projects.sh --audit            # Audit only
#   ./update_eve_projects.sh --apply            # Apply all updates
#   ./update_eve_projects.sh --assets           # Download assets only
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - Update these paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="${HOME}/projects"
ASSET_DIR="${HOME}/.eve_assets"

# Project paths - Update these to match your setup
PROJECTS=(
    "${PROJECTS_DIR}/EVE_Rebellion"
    "${PROJECTS_DIR}/EVE_Gatekeeper"
    "${PROJECTS_DIR}/EVE_Ships"
    # Add more projects here
)

# ============================================================================
# Functions
# ============================================================================

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check for required packages
    python3 -c "import httpx" 2>/dev/null || {
        print_warning "Installing required Python packages..."
        pip3 install httpx --quiet
    }
}

audit_projects() {
    print_header "Auditing All Projects"
    
    for project in "${PROJECTS[@]}"; do
        if [[ -d "$project" ]]; then
            echo -e "\n📁 ${project##*/}"
            python3 "${SCRIPT_DIR}/scripts/project_auditor.py" "$project" 2>/dev/null || {
                print_warning "Could not audit $project"
            }
        else
            print_warning "Project not found: $project"
        fi
    done
}

update_projects() {
    print_header "Updating All Projects"
    
    for project in "${PROJECTS[@]}"; do
        if [[ -d "$project" ]]; then
            echo -e "\n📁 Updating: ${project##*/}"
            python3 "${SCRIPT_DIR}/scripts/project_updater.py" "$project" --apply 2>/dev/null && {
                print_success "Updated ${project##*/}"
            } || {
                print_warning "Could not update $project"
            }
        fi
    done
}

download_assets() {
    print_header "Downloading EVE Assets"
    
    echo "📥 Downloading ship renders to: $ASSET_DIR"
    python3 "${SCRIPT_DIR}/scripts/asset_manager.py" \
        --asset-dir "$ASSET_DIR" \
        --sync-all
    
    print_success "Assets downloaded!"
}

link_assets() {
    print_header "Linking Assets to Projects"
    
    for project in "${PROJECTS[@]}"; do
        if [[ -d "$project" ]]; then
            echo "🔗 Linking to: ${project##*/}"
            python3 "${SCRIPT_DIR}/scripts/asset_manager.py" \
                --asset-dir "$ASSET_DIR" \
                --link-to-project "$project" 2>/dev/null && {
                print_success "Linked to ${project##*/}"
            } || {
                print_warning "Could not link to $project"
            }
        fi
    done
}

generate_report() {
    print_header "Generating Compliance Report"
    
    REPORT_FILE="${SCRIPT_DIR}/compliance_report_$(date +%Y%m%d).json"
    
    python3 "${SCRIPT_DIR}/scripts/project_auditor.py" \
        "${PROJECTS[@]}" \
        --json > "$REPORT_FILE" 2>/dev/null
    
    print_success "Report saved to: $REPORT_FILE"
}

interactive_menu() {
    print_header "EVE Project Master Updater"
    
    echo "Select an option:"
    echo ""
    echo "  1) Audit all projects (show current status)"
    echo "  2) Update all projects (apply ESI integration)"
    echo "  3) Download assets (ship renders from Image Server)"
    echo "  4) Link assets to all projects"
    echo "  5) Generate compliance report"
    echo "  6) Full update (all of the above)"
    echo "  7) Exit"
    echo ""
    read -p "Enter choice [1-7]: " choice
    
    case $choice in
        1) audit_projects ;;
        2) update_projects ;;
        3) download_assets ;;
        4) link_assets ;;
        5) generate_report ;;
        6)
            audit_projects
            update_projects
            download_assets
            link_assets
            generate_report
            print_header "Complete!"
            print_success "All projects have been updated."
            ;;
        7) exit 0 ;;
        *) print_error "Invalid choice" && exit 1 ;;
    esac
}

# ============================================================================
# Main
# ============================================================================

check_python

case "${1:-}" in
    --audit)
        audit_projects
        ;;
    --apply)
        update_projects
        ;;
    --assets)
        download_assets
        ;;
    --link)
        link_assets
        ;;
    --report)
        generate_report
        ;;
    --full)
        audit_projects
        update_projects
        download_assets
        link_assets
        generate_report
        ;;
    --help|-h)
        echo "Usage: $0 [OPTION]"
        echo ""
        echo "Options:"
        echo "  --audit    Audit all projects"
        echo "  --apply    Apply updates to all projects"
        echo "  --assets   Download EVE assets"
        echo "  --link     Link assets to projects"
        echo "  --report   Generate compliance report"
        echo "  --full     Do everything"
        echo "  --help     Show this help"
        echo ""
        echo "Without options, runs interactive menu."
        ;;
    *)
        interactive_menu
        ;;
esac
