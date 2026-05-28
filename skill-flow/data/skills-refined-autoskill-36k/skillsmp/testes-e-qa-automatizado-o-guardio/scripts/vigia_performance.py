import os
import sys
import io
import time
import requests

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def vigiar_performance(url="http://localhost:3000"):
    """
    O Vigia de Performance:
    Mede o Time to First Byte (TTFB) e o tempo total de resposta.
    """
    print(f"⏱️ [GUARDIÃO] Iniciando patrulha de performance em {url}...")
    
    limite_ideal = 0.5 # segundos
    limite_medio = 1.5
    
    try:
        # Aquecimento (primeira req pode ser lenta devido a cold start/caches)
        requests.get(url, timeout=5) 
        
        tempos = []
        for i in range(5):
            start = time.time()
            requests.get(url, timeout=5)
            end = time.time()
            duration = end - start
            tempos.append(duration)
            print(f"  - Medição {i+1}: {duration:.3f}s")
            time.sleep(0.5)
            
        media = sum(tempos) / len(tempos)
        
        print("-" * 30)
        print(f"📊 Média de Tempo de Resposta: {media:.3f}s")
        
        if media < limite_ideal:
            print(f"🚀 Status: VELOCIDADE DA LUZ! O site está voando. (Abaixo de {limite_ideal}s)")
        elif media < limite_medio:
            print(f"✅ Status: BOM. Performance aceitável. (Entre {limite_ideal}s e {limite_medio}s)")
        else:
            print(f"🐢 Status: PREGUIÇOSO. Atenção necessária! (Acima de {limite_medio}s)")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: O servidor parece desligado.")
    except Exception as e:
        print(f"❌ Erro na medição: {e}")

if __name__ == "__main__":
    vigiar_performance()
