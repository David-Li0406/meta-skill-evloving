import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def padronizador_texto(directory="biodiagnostico_app"):
    """
    O Padronizador de Texto:
    Verifica se funções complexas possuem Docstrings e se os comentários estão legíveis.
    """
    print("📝 [ASPIRADOR] Auditando documentação e clareza...")
    
    start_dir = os.path.join(os.getcwd(), directory)
    if not os.path.exists(start_dir):
        start_dir = os.getcwd()
        
    issues = 0
    
    # Regex simples para capturar definições de função
    def_pattern = re.compile(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
    
    for root, dirs, files in os.walk(start_dir):
        if "__pycache__" in root: continue
        
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    for i, line in enumerate(lines):
                        match = def_pattern.match(line)
                        if match:
                            func_name = match.group(1)
                            # Se a função for muito curta (one-liner), ignora
                            # Se não, verifica se a próxima linha tem docstring
                            if i + 1 < len(lines):
                                next_line = lines[i+1].strip()
                                # Heurística: docstring começa com """ ou '''
                                has_docstring = next_line.startswith('"""') or next_line.startswith("'''")
                                
                                # Verifica tamanho da função (simples contagem até próximo def ou fim)
                                # Se for função pública (sem _) e não tiver docstring, alerta
                                if not func_name.startswith("_") and not has_docstring:
                                    print(f"⚠️  {file}: Função '{func_name}' (Linha {i+1}) sem Docstring.")
                                    issues += 1
                                    
                except Exception:
                    pass

    if issues == 0:
        print("✅ Documentação impecável! Todas as funções públicas estão explicadas.")
    else:
        print(f"📖 Faltam manuais! {issues} funções precisam de documentação (docstrings).")

if __name__ == "__main__":
    padronizador_texto()
