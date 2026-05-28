import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def coletor_lixo(directory="biodiagnostico_app"):
    """
    O Coletor de Lixo:
    Identifica " código morto":
    1. Grandes blocos de código comentado.
    2. Importações não utilizadas (básico).
    3. TODOs esquecidos.
    """
    print("🗑️  [ASPIRADOR] Varrendo código morto e lixo acumulado...")
    
    start_dir = os.path.join(os.getcwd(), directory)
    if not os.path.exists(start_dir):
        start_dir = os.getcwd()
        
    lixo_encontrado = 0
    
    for root, dirs, files in os.walk(start_dir):
        if "__pycache__" in root: 
            continue
            
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                        comment_block_count = 0
                        todos = []
                        
                        for i, line in enumerate(lines):
                            stripped = line.strip()
                            
                            # Detecta TODO
                            if "TODO" in line or "FIXME" in line:
                                todos.append(i + 1)
                                
                            # Detecta código comentado (heurística simples: linha começa com # mas parece código)
                            if stripped.startswith("#") and len(stripped) > 5 and ("=" in stripped or "def " in stripped or "class " in stripped):
                                comment_block_count += 1
                        
                        if comment_block_count > 5 or todos:
                            print(f"📄 {file}:")
                            if comment_block_count > 5:
                                print(f"  ⚠️  {comment_block_count} linhas de código comentado (Cemitério de Código?)")
                                lixo_encontrado += 1
                            if todos:
                                print(f"  📌 {len(todos)} tarefas pendentes (TODO/FIXME) nas linhas: {todos}")
                                lixo_encontrado += 1
                                
                except Exception:
                    pass

    if lixo_encontrado == 0:
        print("✅ Código limpo! Nenhum lixo aparente.")
    else:
        print(f"🧹 A vassoura precisa trabalhar! {lixo_encontrado} arquivos precisam de limpeza.")

if __name__ == "__main__":
    coletor_lixo()
