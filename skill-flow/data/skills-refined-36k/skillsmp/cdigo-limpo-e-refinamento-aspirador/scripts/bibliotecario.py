import os
import sys
import io
import subprocess

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def bibliotecario():
    """
    O Bibliotecário:
    Consulta o índice arcaico (pip) para ver se suas ferramentas estão obsoletas.
    """
    print("📚 [ASPIRADOR] O Bibliotecário está verificando suas dependências...")
    
    try:
        # Executa pip list --outdated
        # timeout para não travar se a internet estiver lenta
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            import json
            outdated = json.loads(result.stdout)
            
            if outdated:
                print(f"🚨 Atenção! {len(outdated)} livros na estante estão desatualizados:")
                print(f"{'Pacote':<20} | {'Atual':<10} | {'Nova':<10}")
                print("-" * 45)
                
                for pkg in outdated:
                    print(f"{pkg['name']:<20} | {pkg['version']:<10} | {pkg['latest_version']:<10}")
                    
                print("-" * 45)
                print("💡 Sugestão: Rode 'pip install --upgrade <pacote>' para atualizar.")
            else:
                print("✅ A Biblioteca está em dia! Nada obsoleto.")
        else:
            print("❌ O Bibliotecário não conseguiu acessar o catálogo (pip failed).")
            
    except subprocess.TimeoutExpired:
        print("⏳ O Bibliotecário demorou muito e desistiu. Verifique sua intenet.")
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")

if __name__ == "__main__":
    bibliotecario()
