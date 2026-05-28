#!/usr/bin/env bash
set -e

echo "Init Devcontainer"

VSCODE_CWD=${VSCODE_CWD:-$PWD}

mkdir -p "${VSCODE_CWD}/config"

# Create .env file if it doesn't exist
if [ ! -f "${VSCODE_CWD}/.env" ]; then
  echo "Creating .env file with DUPLO credentials..."
  cat > "${VSCODE_CWD}/.env" << EOF
DUPLO_HOST=${DUPLO_HOST}
DUPLO_TOKEN=${DUPLO_TOKEN}
EOF
  echo ".env file created"
else
  echo ".env file already exists"
fi
