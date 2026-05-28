import os
import re

def aspirar_dívidas(directory):
    files_to_refactor = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                points = 0
                reasons = []
                
                # Check Size
                size = os.path.getsize(path) / 1024 # KB
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    
                    if lines > 500:
                        points += 3
                        reasons.append(f"Arquivo Gigante ({lines} linhas)")
                    
                    # Check Hardcoded hex colors
                    if re.search(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', content) and "styles.py" not in file:
                        points += 2
                        reasons.append("Cores Hex manuais detectadas")
                    
                    # Check for mixing logic and UI
                    if "rx.vstack" in content and ("import supabase" in content or "import cloudinary" in content):
                        points += 2
                        reasons.append("Lógica de Infra/DB misturada com UI")
                        
                    if points > 0:
                        files_to_refactor.append({
                            "path": path,
                            "points": points,
                            "reasons": reasons
                        })

    # Sort by priority
    files_to_refactor.sort(key=lambda x: x['points'], reverse=True)
    
    print("=== RELATORIO DO ASPIRADOR DE CODIGO ===")
    for item in files_to_refactor:
        print(f"\n[PRIO {item['points']}] {item['path']}")
        for reason in item['reasons']:
            print(f"  - {reason}")

if __name__ == "__main__":
    aspirar_dívidas("biodiagnostico_app/biodiagnostico_app")
