import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scanner_seguranca(directory="."):
    """
    O Scanner de Segurança:
    Procura por segredos (API Keys, Passwords) expostos no código.
    """
    print("🔐 [ASPIRADOR] Varredura de segurança iniciada...")
    
    # Padrões perigosos
    patterns = {
        "Supabase Key": r"ey[A-Za-z0-9-_=]{20,}", # JWT like
        "Generic Secret": r"(?i)(secret|password|api_key|token)\s*=\s*['\"][^'\"]+['\"]"
    }
    
    issues = 0
    
    # Excluir arquivos de configuração legítimos
    ignored_diles = [".env", "package-lock.json", ".git"]
    
    targets = []
    # Foca no app se existir
    if os.path.exists("biodiagnostico_app"):
        start_dir = "biodiagnostico_app"
    else:
        start_dir = directory

    for root, dirs, files in os.walk(start_dir):
        if "__pycache__" in root or ".git" in root: continue
        
        for file in files:
            if file in ignored_diles: continue
            if file.endswith(".py") or file.endswith(".js") or file.endswith(".sql"):
                targets.append(os.path.join(root, file))
                
    for filepath in targets:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for name, pattern in patterns.items():
                matches = re.finditer(pattern, content)
                for match in matches:
                    # Verifica se não é uma leitura de env, ex: os.getenv("SECRET")
                    matched_str = match.group(0)
                    if "os.getenv" in matched_str or "os.environ" in matched_str:
                        continue
                        
                    # Verifica se é muito curto (falso positivo)
                    if len(matched_str) < 10:
                        continue

                    display_str = matched_str[:20] + "..." if len(matched_str) > 20 else matched_str
                    print(f"🛑 PERIGO em {os.path.basename(filepath)}: Possível {name} exposta!")
                    print(f"   Trecho: {display_str}")
                    issues += 1
                    
        except Exception:
            pass

    if issues == 0:
        print("✅ Cofre seguro! Nenhuma chave secreta encontrada exposta no código.")
    else:
        print(f"🚨 ALERTA: Encontrados {issues} potenciais vazamentos de segurança!")
        print("👉 Mova essas chaves para o arquivo .env IMEDIATAMENTE.")

if __name__ == "__main__":
    scanner_seguranca()
