import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def alinhador_automatico(directory="biodiagnostico_app"):
    """
    O Alinhador Automático:
    Verifica se espaçamentos e margens estão usando os tokens do sistema (Spacing.SM, etc)
    ou se estão usando valores hardcoded ("10px", "15px").
    """
    print("📐 [UI PREMIUM] Verificando alinhamento e respiro visual...")
    
    # Padrão para encontrar pixels soltos, ex: "10px", '15px'
    # Evita 0px ou 100% que as vezes são ok, mas foca em valores arbitrários
    pixel_pattern = r'["\']\d+px["\']'
    
    violations = []
    
    start_dir = os.path.join(os.getcwd(), directory)
    if not os.path.exists(start_dir):
        start_dir = os.getcwd()

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".py") and "styles.py" not in file:
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    for i, line in enumerate(lines):
                        # Verifica propriedades de espaçamento
                        if any(prop in line for prop in ["padding", "margin", "gap", "spacing"]):
                            matches = re.finditer(pixel_pattern, line)
                            for match in matches:
                                val = match.group(0)
                                # Ignora valores comuns de CSS global se necessário, mas em Reflex idealmente é Token
                                violations.append({
                                    "file": file,
                                    "line": i + 1,
                                    "value": val,
                                    "content": line.strip()
                                })
                except Exception as e:
                    pass

    if violations:
        print(f"⚠️  Atenção: Encontrados {len(violations)} espaçamentos manuais (Hardcoded).")
        print("👉 Prefira usar Spacing.SM, Spacing.MD, Spacing.LG para consistência.")
        print("-" * 50)
        # Mostra apenas os 10 primeiros para não poluir
        for v in violations[:10]:
            print(f"📏 {v['file']} (Linha {v['line']}): {v['value']} -> {v['content'][:50]}...")
        if len(violations) > 10:
            print(f"... e mais {len(violations) - 10} ocorrências.")
    else:
        print("✅ Alinhamento Perfeito! Todos os espaçamentos parecem seguir o padrão.")

if __name__ == "__main__":
    alinhador_automatico()
