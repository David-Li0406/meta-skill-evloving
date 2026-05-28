#!/bin/bash
set -euo pipefail

# Generate secure JWT key pairs
# Supports both symmetric (HS256) and asymmetric (RS256) algorithms

ALGORITHM="${1:-RS256}"
OUTPUT_DIR="${2:-.}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔐 JWT Key Generator"
echo ""

case "$ALGORITHM" in
  HS256)
    echo "Generating symmetric key for HS256..."
    SECRET=$(openssl rand -base64 64 | tr -d '\n')

    echo "$SECRET" > "$OUTPUT_DIR/jwt-secret.key"
    chmod 600 "$OUTPUT_DIR/jwt-secret.key"

    echo -e "${GREEN}✅ Generated symmetric key${NC}"
    echo ""
    echo "Key saved to: $OUTPUT_DIR/jwt-secret.key"
    echo ""
    echo "Usage in your .env file:"
    echo "  JWT_SECRET=$SECRET"
    echo ""
    echo -e "${YELLOW}⚠️  Keep this secret secure and never commit it to version control!${NC}"
    ;;

  RS256)
    echo "Generating asymmetric key pair for RS256..."

    # Generate private key
    openssl genrsa -out "$OUTPUT_DIR/jwt-private.key" 4096 2>/dev/null
    chmod 600 "$OUTPUT_DIR/jwt-private.key"

    # Generate public key
    openssl rsa -in "$OUTPUT_DIR/jwt-private.key" -pubout -out "$OUTPUT_DIR/jwt-public.key" 2>/dev/null
    chmod 644 "$OUTPUT_DIR/jwt-public.key"

    echo -e "${GREEN}✅ Generated asymmetric key pair${NC}"
    echo ""
    echo "Private key (for signing): $OUTPUT_DIR/jwt-private.key"
    echo "Public key (for verification): $OUTPUT_DIR/jwt-public.key"
    echo ""
    echo "Usage in your application:"
    echo ""
    echo "Signing (private key):"
    echo "  const privateKey = fs.readFileSync('jwt-private.key', 'utf8');"
    echo "  const token = jwt.sign(payload, privateKey, { algorithm: 'RS256' });"
    echo ""
    echo "Verification (public key):"
    echo "  const publicKey = fs.readFileSync('jwt-public.key', 'utf8');"
    echo "  const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });"
    echo ""
    echo -e "${YELLOW}⚠️  Keep the private key secure and never commit it to version control!${NC}"
    echo -e "${YELLOW}⚠️  Add jwt-private.key to your .gitignore${NC}"
    ;;

  ES256)
    echo "Generating elliptic curve key pair for ES256..."

    # Generate private key
    openssl ecparam -name prime256v1 -genkey -noout -out "$OUTPUT_DIR/jwt-private.key"
    chmod 600 "$OUTPUT_DIR/jwt-private.key"

    # Generate public key
    openssl ec -in "$OUTPUT_DIR/jwt-private.key" -pubout -out "$OUTPUT_DIR/jwt-public.key" 2>/dev/null
    chmod 644 "$OUTPUT_DIR/jwt-public.key"

    echo -e "${GREEN}✅ Generated elliptic curve key pair${NC}"
    echo ""
    echo "Private key (for signing): $OUTPUT_DIR/jwt-private.key"
    echo "Public key (for verification): $OUTPUT_DIR/jwt-public.key"
    echo ""
    echo "ES256 provides similar security to RS256 with smaller key sizes."
    echo ""
    echo -e "${YELLOW}⚠️  Keep the private key secure and never commit it to version control!${NC}"
    ;;

  *)
    echo "Usage: $0 [ALGORITHM] [OUTPUT_DIR]"
    echo ""
    echo "Supported algorithms:"
    echo "  HS256  - HMAC with SHA-256 (symmetric)"
    echo "  RS256  - RSA with SHA-256 (asymmetric, default)"
    echo "  ES256  - ECDSA with SHA-256 (asymmetric)"
    echo ""
    echo "Examples:"
    echo "  $0 HS256 ./keys"
    echo "  $0 RS256 ./keys"
    echo "  $0 ES256 ./keys"
    exit 1
    ;;
esac

# Create .gitignore entry if git repo exists
if [[ -d "$OUTPUT_DIR/.git" ]] || git rev-parse --git-dir > /dev/null 2>&1; then
  GITIGNORE="$OUTPUT_DIR/.gitignore"

  if [[ ! -f "$GITIGNORE" ]] || ! grep -q "jwt-private.key" "$GITIGNORE"; then
    echo "" >> "$GITIGNORE"
    echo "# JWT keys" >> "$GITIGNORE"
    echo "jwt-private.key" >> "$GITIGNORE"
    echo "jwt-secret.key" >> "$GITIGNORE"
    echo ""
    echo -e "${GREEN}✅ Added keys to .gitignore${NC}"
  fi
fi

echo ""
echo "Next steps:"
echo "1. Store keys securely (use environment variables or secret management)"
echo "2. Configure your application to use these keys"
echo "3. Set appropriate token expiration times"
echo "4. Implement token refresh strategy"
