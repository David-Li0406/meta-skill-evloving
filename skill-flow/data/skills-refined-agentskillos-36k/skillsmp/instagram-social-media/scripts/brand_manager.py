#!/usr/bin/env python3
"""
Brand Manager - Manages persistent brand profiles for the Instagram Skill.
Stores profiles as JSON files in the ../profiles/ directory.
"""

import sys
import json
import os
from pathlib import Path

# Define profiles directory relative to this script
BASE_DIR = Path(__file__).parent.parent
PROFILES_DIR = BASE_DIR / 'profiles'

def ensure_profiles_dir():
    """Ensure the profiles directory exists."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

def list_brands():
    """List all available brand profiles."""
    ensure_profiles_dir()
    files = list(PROFILES_DIR.glob('*.json'))
    if not files:
        print("Nenhuma marca encontrada.")
        return
    
    print("Marcas disponíveis:")
    for f in files:
        print(f"- {f.stem}")

def read_brand(brand_slug):
    """Read and print a brand profile."""
    ensure_profiles_dir()
    file_path = PROFILES_DIR / f"{brand_slug}.json"
    
    if not file_path.exists():
        print(f"Erro: Marca '{brand_slug}' não encontrada.")
        sys.exit(1)
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro ao ler perfil: {e}")
        sys.exit(1)

def create_brand(brand_slug, json_data):
    """Create or update a brand profile."""
    ensure_profiles_dir()
    file_path = PROFILES_DIR / f"{brand_slug}.json"
    
    try:
        # Validate JSON
        data = json.loads(json_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Sucesso: Perfil da marca '{brand_slug}' salvo em {file_path}")
    except json.JSONDecodeError:
        print("Erro: Dados fornecidos não são um JSON válido.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao salvar perfil: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Uso: brand_manager.py <list|read|create> [args...]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == 'list':
        list_brands()
    elif command == 'read':
        if len(sys.argv) < 3:
            print("Uso: brand_manager.py read <brand_slug>")
            sys.exit(1)
        read_brand(sys.argv[2])
    elif command == 'create' or command == 'update':
        if len(sys.argv) < 4:
            print("Uso: brand_manager.py create <brand_slug> <json_data>")
            sys.exit(1)
        create_brand(sys.argv[2], sys.argv[3])
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
