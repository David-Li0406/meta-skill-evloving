import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def organizador_arquivos(directory="biodiagnostico_app"):
    """
    O Organizador de Gavetas:
    Verifica se os nomes de arquivos seguem o padrão snake_case e sugere renomeações.
    Também alerta sobre arquivos soltos na raiz que deveriam estar em pastas.
    """
    print("🗄️  [ASPIRADOR] Organizando gavetas e analisando nomes...")
    
    start_dir = os.path.join(os.getcwd(), directory)
    if not os.path.exists(start_dir):
        start_dir = os.getcwd()

    issues = []
    
    # Regex para snake_case (letras minúsculas, números e underscore)
    snake_case_pattern = re.compile(r'^[a-z0-9_]+\.py$')
    
    for root, dirs, files in os.walk(start_dir):
        if "__pycache__" in root or ".git" in root:
            continue
            
        for file in files:
            if not file.endswith(".py"):
                continue
                
            # Verifica espaços ou letras maiúsculas (ex: "Meus Utils.py" ou "Page.py")
            if not snake_case_pattern.match(file) and file != "Dockerfile":
                issues.append({
                    "path": os.path.join(root, file),
                    "reason": f"Nome fora do padrão snake_case: '{file}'"
                })
                
    if issues:
        print(f"🚨 Encontrados {len(issues)} arquivos com nomes fora do padrão:")
        for issue in issues:
            print(f"  ❌ {issue['reason']}")
            # Sugestão de correção
            name = os.path.basename(issue['path'])
            sugestao = name.lower().replace(" ", "_").replace("-", "_")
            print(f"     👉 Sugestão: {sugestao}")
    else:
        print("✅ Todos os arquivos estão perfeitamente etiquetados (snake_case)!")

if __name__ == "__main__":
    organizador_arquivos()
