import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def detetive_erros(log_dir="."):
    """
    O Detetive de Bugs:
    Procura por arquivos de log (.log) e varre em busca de palavras-chave de erro.
    """
    print("🕵️  [GUARDIÃO] Investigando logs em busca de crimes (bugs)...")
    
    keywords = ["Error", "Exception", "Traceback", "Fail", "Critical"]
    crimes_found = 0
    
    # Procura recursivamente ou apenas no dir atual (ajustar conforme estrutura de logs)
    # Por padrão, vamos olhar no diretório atual e subpastas próximas
    
    for root, dirs, files in os.walk(log_dir):
        if "node_modules" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".log") or file.endswith(".txt") or file == "reflex_output.txt": # Exemplo de arquivo
                filepath = os.path.join(root, file)
                print(f"📄 Analisando evidências em: {file}...")
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                        # Pega as ultimas 100 linhas apenas para ser relevante
                        recent_lines = lines[-100:] if len(lines) > 100 else lines
                        
                        for i, line in enumerate(recent_lines):
                            for kw in keywords:
                                if kw.lower() in line.lower():
                                    print(f"   🚨 Pista encontrada (Linha {len(lines) - 100 + i}): {line.strip()[:100]}...")
                                    crimes_found += 1
                except Exception as e:
                    print(f"⚠️  Não consegui ler o arquivo {file}: {e}")

    if crimes_found == 0:
        print("✅ Nenhuma evidência de erro encontrada nos logs recentes. Caso encerrado.")
    else:
        print(f"🚓 O Detetive encontrou {crimes_found} indicativos de problemas. Investigação necessária!")

if __name__ == "__main__":
    # Foca apenas no diretório do app para evitar logs do sistema/vscode
    target_dir = os.path.join(os.getcwd(), "biodiagnostico_app")
    if not os.path.exists(target_dir):
        target_dir = os.getcwd() # Fallback
        
    detetive_erros(target_dir)
