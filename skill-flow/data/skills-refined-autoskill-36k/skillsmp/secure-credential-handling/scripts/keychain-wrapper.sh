#!/bin/bash
# Keychain Wrapper for Secure Credential Storage
# Supports: macOS Keychain, Linux Secret Service, Windows Credential Manager

set -e

ACTION="$1"
SERVICE="$2"
TYPE="$3"
VALUE="$4"

detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

store_credential() {
    local service="$1"
    local type="$2"
    local value="$3"

    case "$OS" in
        macos)
            security add-generic-password -a "$USER" -s "$service" -w "$value" -U 2>/dev/null || \
            security delete-generic-password -s "$service" 2>/dev/null && \
            security add-generic-password -a "$USER" -s "$service" -w "$value"
            ;;
        linux)
            if command -v secret-tool &> /dev/null; then
                echo -n "$value" | secret-tool store --label="$service" service "$service" type "$type" username "$USER"
            else
                mkdir -p ~/.local/share/claude-code/credentials
                echo -n "$value" | openssl enc -aes-256-cbc -salt -pbkdf2 -out ~/.local/share/claude-code/credentials/"${service}.enc" -pass pass:"$(hostname)-$(whoami)"
                chmod 600 ~/.local/share/claude-code/credentials/"${service}.enc"
            fi
            ;;
        windows)
            echo "$value" | cmdkey /generic:"$service" /user:"$USER" /pass
            ;;
    esac
}

get_credential() {
    local service="$1"

    case "$OS" in
        macos)
            security find-generic-password -a "$USER" -s "$service" -w 2>/dev/null
            ;;
        linux)
            if command -v secret-tool &> /dev/null; then
                secret-tool lookup service "$service" username "$USER" 2>/dev/null
            else
                if [ -f ~/.local/share/claude-code/credentials/"${service}.enc" ]; then
                    openssl enc -aes-256-cbc -d -in ~/.local/share/claude-code/credentials/"${service}.enc" -pass pass:"$(hostname)-$(whoami)" 2>/dev/null
                fi
            fi
            ;;
    esac
}

delete_credential() {
    local service="$1"

    case "$OS" in
        macos)
            security delete-generic-password -s "$service" 2>/dev/null
            ;;
        linux)
            if command -v secret-tool &> /dev/null; then
                secret-tool clear service "$service" username "$USER" 2>/dev/null
            else
                rm -f ~/.local/share/claude-code/credentials/"${service}.enc"
            fi
            ;;
    esac
}

list_credentials() {
    local prefix="$1"

    case "$OS" in
        macos)
            security dump-keychain 2>/dev/null | grep "^keychain" -A 10 | grep "\"$prefix" | sed 's/.*"\(.*\)".*/\1/'
            ;;
        linux)
            if command -v secret-tool &> /dev/null; then
                secret-tool search --all username "$USER" 2>/dev/null | grep "^attribute.service" | grep "$prefix" | cut -d= -f2 | tr -d ' '
            else
                ls ~/.local/share/claude-code/credentials/*.enc 2>/dev/null | xargs -n1 basename | sed 's/\.enc$//' | grep "^$prefix" || true
            fi
            ;;
    esac
}

case "$ACTION" in
    store)
        store_credential "$SERVICE" "$TYPE" "$VALUE"
        echo "✓ Credential stored successfully"
        ;;
    get)
        get_credential "$SERVICE"
        ;;
    delete)
        delete_credential "$SERVICE"
        echo "✓ Credential deleted"
        ;;
    list)
        list_credentials "$SERVICE"
        ;;
    *)
        echo "Usage: $0 {store|get|delete|list} <service> [type] [value]"
        exit 1
        ;;
esac
