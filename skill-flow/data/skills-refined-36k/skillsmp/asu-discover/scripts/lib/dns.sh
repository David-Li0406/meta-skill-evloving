#!/usr/bin/env bash
# ==============================================================================
# DNS Validation and Scaffolding Library
# ==============================================================================
# Functions for validating domains and generating Terraform scaffolding
# for Infoblox (*.asu.edu) and Cloudflare (external) DNS configurations.

# Get the template directory relative to this script
DNS_TEMPLATE_DIR="${SCRIPT_DIR}/../templates/dns"

# ==============================================================================
# Domain Validation Functions
# ==============================================================================

# Validate domain and return provider recommendation
# Usage: validate_domain <domain>
# Returns: infoblox | cloudflare
validate_domain() {
    local domain="$1"
    
    if [[ "$domain" =~ \.asu\.edu$ ]]; then
        echo "infoblox"
    else
        echo "cloudflare"
    fi
}

# Check if domain exists in DNS using dig
# Usage: check_dns_exists <domain>
# Returns: 0 if exists, 1 if not found
check_dns_exists() {
    local domain="$1"
    local result
    
    # Try to resolve the domain
    result=$(dig +short "$domain" 2>/dev/null)
    
    if [[ -n "$result" ]]; then
        return 0
    else
        return 1
    fi
}

# Get current DNS records for a domain
# Usage: get_dns_records <domain>
get_dns_records() {
    local domain="$1"
    local record_type="${2:-ANY}"
    
    echo "=== DNS Records for $domain ==="
    
    # A records
    local a_records=$(dig +short A "$domain" 2>/dev/null)
    if [[ -n "$a_records" ]]; then
        echo "A Records:"
        echo "$a_records" | sed 's/^/  /'
    fi
    
    # CNAME records
    local cname_records=$(dig +short CNAME "$domain" 2>/dev/null)
    if [[ -n "$cname_records" ]]; then
        echo "CNAME Records:"
        echo "$cname_records" | sed 's/^/  /'
    fi
    
    # Check if no records found
    if [[ -z "$a_records" && -z "$cname_records" ]]; then
        echo "No A or CNAME records found"
    fi
}

# Get DNS views for Infoblox domains
# Returns space-separated list of views
get_infoblox_views() {
    echo "default external"
}

# ==============================================================================
# Scaffolding Functions
# ==============================================================================

# Scaffold Infoblox A record
# Usage: scaffold_infoblox_a <name> <domain> <ip> [view] [comment]
scaffold_infoblox_a() {
    local name="$1"
    local domain="$2"
    local ip="$3"
    local view="${4:-default}"
    local comment="${5:-Managed by Terraform}"
    
    if [[ ! -f "${DNS_TEMPLATE_DIR}/infoblox-a.tf.tpl" ]]; then
        echo "Error: Template not found: ${DNS_TEMPLATE_DIR}/infoblox-a.tf.tpl" >&2
        return 1
    fi
    
    sed -e "s/{{name}}/${name}/g" \
        -e "s/{{domain}}/${domain}/g" \
        -e "s/{{ip}}/${ip}/g" \
        -e "s/{{view}}/${view}/g" \
        -e "s/{{comment}}/${comment}/g" \
        "${DNS_TEMPLATE_DIR}/infoblox-a.tf.tpl"
}

# Scaffold Infoblox CNAME record
# Usage: scaffold_infoblox_cname <name> <domain> <target> [view] [comment]
scaffold_infoblox_cname() {
    local name="$1"
    local domain="$2"
    local target="$3"
    local view="${4:-default}"
    local comment="${5:-Managed by Terraform}"
    
    if [[ ! -f "${DNS_TEMPLATE_DIR}/infoblox-cname.tf.tpl" ]]; then
        echo "Error: Template not found: ${DNS_TEMPLATE_DIR}/infoblox-cname.tf.tpl" >&2
        return 1
    fi
    
    sed -e "s/{{name}}/${name}/g" \
        -e "s/{{domain}}/${domain}/g" \
        -e "s/{{target}}/${target}/g" \
        -e "s/{{view}}/${view}/g" \
        -e "s/{{comment}}/${comment}/g" \
        "${DNS_TEMPLATE_DIR}/infoblox-cname.tf.tpl"
}

# Scaffold Cloudflare A record
# Usage: scaffold_cloudflare_a <name> <subdomain> <value> [proxied]
scaffold_cloudflare_a() {
    local name="$1"
    local subdomain="$2"
    local value="$3"
    local proxied="${4:-true}"
    
    if [[ ! -f "${DNS_TEMPLATE_DIR}/cloudflare-a.tf.tpl" ]]; then
        echo "Error: Template not found: ${DNS_TEMPLATE_DIR}/cloudflare-a.tf.tpl" >&2
        return 1
    fi
    
    sed -e "s/{{name}}/${name}/g" \
        -e "s/{{subdomain}}/${subdomain}/g" \
        -e "s/{{value}}/${value}/g" \
        -e "s/{{proxied}}/${proxied}/g" \
        "${DNS_TEMPLATE_DIR}/cloudflare-a.tf.tpl"
}

# Scaffold Cloudflare CNAME record
# Usage: scaffold_cloudflare_cname <name> <subdomain> <value> [proxied]
scaffold_cloudflare_cname() {
    local name="$1"
    local subdomain="$2"
    local value="$3"
    local proxied="${4:-true}"
    
    if [[ ! -f "${DNS_TEMPLATE_DIR}/cloudflare-cname.tf.tpl" ]]; then
        echo "Error: Template not found: ${DNS_TEMPLATE_DIR}/cloudflare-cname.tf.tpl" >&2
        return 1
    fi
    
    sed -e "s/{{name}}/${name}/g" \
        -e "s/{{subdomain}}/${subdomain}/g" \
        -e "s/{{value}}/${value}/g" \
        -e "s/{{proxied}}/${proxied}/g" \
        "${DNS_TEMPLATE_DIR}/cloudflare-cname.tf.tpl"
}

# Scaffold hybrid pattern (Infoblox -> Cloudflare CDN -> Origin)
# Usage: scaffold_hybrid <name> <subdomain> <origin>
scaffold_hybrid() {
    local name="$1"
    local subdomain="$2"
    local origin="$3"
    
    if [[ ! -f "${DNS_TEMPLATE_DIR}/hybrid-pattern.tf.tpl" ]]; then
        echo "Error: Template not found: ${DNS_TEMPLATE_DIR}/hybrid-pattern.tf.tpl" >&2
        return 1
    fi
    
    sed -e "s/{{name}}/${name}/g" \
        -e "s/{{subdomain}}/${subdomain}/g" \
        -e "s/{{origin}}/${origin}/g" \
        "${DNS_TEMPLATE_DIR}/hybrid-pattern.tf.tpl"
}

# Generate Vault secrets data source for a provider
# Usage: scaffold_vault_secrets <provider>
# provider: infoblox | cloudflare | both
scaffold_vault_secrets() {
    local provider="$1"
    
    if [[ ! -f "${DNS_TEMPLATE_DIR}/vault-secrets.tf.tpl" ]]; then
        echo "Error: Template not found: ${DNS_TEMPLATE_DIR}/vault-secrets.tf.tpl" >&2
        return 1
    fi
    
    case "$provider" in
        infoblox)
            sed -n '/^# infoblox$/,/^# cloudflare$/{ /^# cloudflare$/d; p; }' "${DNS_TEMPLATE_DIR}/vault-secrets.tf.tpl"
            ;;
        cloudflare)
            sed -n '/^# cloudflare$/,/^$/p' "${DNS_TEMPLATE_DIR}/vault-secrets.tf.tpl"
            ;;
        both|hybrid)
            cat "${DNS_TEMPLATE_DIR}/vault-secrets.tf.tpl"
            ;;
        *)
            echo "Unknown provider: $provider" >&2
            return 1
            ;;
    esac
}

# ==============================================================================
# Display Functions
# ==============================================================================

# Show provider recommendation with details
# Usage: show_recommendation <domain> [check_dns]
show_recommendation() {
    local domain="$1"
    local check_dns="${2:-false}"
    local provider
    
    provider=$(validate_domain "$domain")
    
    echo "Domain: $domain"
    echo "Provider: $provider"
    echo ""
    
    case "$provider" in
        infoblox)
            echo "Configuration:"
            echo "  Server: dnsadmin.asu.edu"
            echo "  Views: default, external"
            echo "  Vault Path: secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app"
            echo ""
            echo "Resources:"
            echo "  - infoblox_a_record"
            echo "  - infoblox_cname_record"
            ;;
        cloudflare)
            echo "Configuration:"
            echo "  Action: Register domain + configure DNS"
            echo "  Vault Path: secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops"
            echo ""
            echo "Resources:"
            echo "  - cloudflare_record"
            echo "  - cloudflare_zone"
            echo ""
            echo "Available Modules:"
            echo "  - cloudflare-tunnel"
            echo "  - cloudflare-tunnel-route53-dns"
            echo "  - cloudflare-access-app"
            echo "  - cloudflare-origin-ca-certificate"
            ;;
    esac
    
    # Check if domain already exists in DNS
    if [[ "$check_dns" == "true" ]]; then
        echo ""
        if check_dns_exists "$domain"; then
            echo "DNS Status: EXISTS"
            get_dns_records "$domain"
        else
            echo "DNS Status: NOT FOUND (domain does not resolve)"
        fi
    fi
}

# Show example repos for DNS patterns
# Usage: show_dns_examples [pattern]
show_dns_examples() {
    local pattern="${1:-all}"
    
    echo "=== Example Repos for DNS Pattern: $pattern ==="
    echo ""
    
    case "$pattern" in
        infoblox)
            echo "Infoblox DNS Examples:"
            echo "  ASU/sso-shibboleth      - Hybrid Infoblox+Cloudflare pattern"
            echo "  ASU/hosting-fse         - Infoblox CNAME with for_each"
            echo "  ASU/ewp-www-farm-acquia - Infoblox A and CNAME records"
            echo "  ASU/hosting-cronkite    - infoblox-cname-record module"
            echo "  ASU/xreal-xr-at-asu-portal - Infoblox integration"
            echo ""
            echo "Module Source:"
            echo "  ASU/dns-infoblox        - Infoblox Terraform configurations"
            ;;
        cloudflare)
            echo "Cloudflare DNS Examples:"
            echo "  ASU/sso-shibboleth      - Cloudflare proxied records"
            echo ""
            echo "Available Cloudflare Modules:"
            echo "  - cloudflare-tunnel"
            echo "  - cloudflare-tunnel-route53-dns"
            echo "  - cloudflare-access-app"
            echo "  - cloudflare-origin-ca-certificate"
            ;;
        hybrid)
            echo "Hybrid Pattern Examples (Infoblox -> Cloudflare CDN -> Origin):"
            echo "  ASU/sso-shibboleth      - Full hybrid pattern implementation"
            echo ""
            echo "Pattern Flow:"
            echo "  1. Infoblox CNAME (default + external views) -> Cloudflare CDN"
            echo "  2. Cloudflare proxied record -> Origin server"
            ;;
        all|*)
            echo "All DNS Patterns:"
            echo ""
            echo "Infoblox (*.asu.edu):"
            echo "  ASU/hosting-fse, ASU/ewp-www-farm-acquia, ASU/hosting-cronkite"
            echo ""
            echo "Cloudflare (external domains):"
            echo "  ASU/sso-shibboleth"
            echo ""
            echo "Hybrid (ASU domain + Cloudflare CDN):"
            echo "  ASU/sso-shibboleth"
            echo ""
            echo "Module Sources:"
            echo "  ASU/dns-infoblox"
            ;;
    esac
}
