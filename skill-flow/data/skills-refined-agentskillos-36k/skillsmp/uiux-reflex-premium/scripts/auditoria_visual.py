import os
import sys
import io
import re

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def caçar_cores_estranhas(directory="biodiagnostico_app"):
    """
    O Caçador de Cores:
    Varre o código em busca de cores hardcoded (hexadecimais) que violam o Design System.
    """
    print("🎨 [UI PREMIUM] Iniciando auditoria visual (Caça às Cores)...")
    
    # Padrão para encontrar hexadecimais: #FFF ou #FFFFFF
    hex_pattern = r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\b'
    
    # Cores permitidas (exceções, se houver) ou ignorar styles.py onde elas são definidas
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
                        content = f.read()
                        
                        matches = re.finditer(hex_pattern, content)
                        for match in matches:
                            # Ignora se estiver dentro de um comentário (simplificado)
                            # Para uma análise robusta, precisaria de um parser autêntico
                            violations.append({
                                "file": file,
                                "path": filepath,
                                "color": f"#{match.group(1)}",
                                "line": content[:match.start()].count('\n') + 1
                            })
                except Exception as e:
                    print(f"⚠️ Erro ao ler {file}: {e}")

    if violations:
        print(f"🚨 Encontradas {len(violations)} violações do Design System!")
        print("👉 Use os tokens de cor (Color.PRIMARY, Color.TEXT, etc) em vez de códigos hex.")
        print("-" * 50)
        for v in violations:
            print(f"❌ {v['file']} (Linha {v['line']}): Usou {v['color']}")
    else:
        print("✅ Design System respeitado! Nenhuma cor 'clandestina' encontrada.")

if __name__ == "__main__":
    caçar_cores_estranhas()
