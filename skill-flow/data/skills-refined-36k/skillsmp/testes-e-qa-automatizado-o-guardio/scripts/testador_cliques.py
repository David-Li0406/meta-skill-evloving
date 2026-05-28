import os
import sys
import io
import time
import requests
from bs4 import BeautifulSoup

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def testar_cliques(url_base="http://localhost:3000"):
    """
    O Testador de Cliques:
    Simula a navegação básica, buscando botões e links na página inicial
    e verificando se eles são acessíveis (status 200).
    Nota: Para cliques reais de UI (JS), seria necessário Playwright/Selenium.
    Esta versão é um "smoke test" leve.
    """
    print(f"🖱️ [GUARDIÃO] Testando acessibilidade de links/botões em {url_base}...")
    
    try:
        start_time = time.time()
        response = requests.get(url_base, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Página inicial carregada com sucesso ({response.elapsed.total_seconds():.2f}s).")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca links (a href)
            links = soup.find_all('a', href=True)
            print(f"🔎 Encontrados {len(links)} links navegáveis.")
            
            error_count = 0
            for i, link in enumerate(links[:10]): # Testa os primeiros 10 para não demorar
                href = link['href']
                if href.startswith("/"):
                    target = url_base + href
                elif href.startswith("http"):
                    target = href
                else:
                    continue # Ignora links js ou âncoras #
                
                try:
                    res = requests.head(target, timeout=3)
                    if res.status_code < 400:
                        print(f"  [{i+1}] ✅ Link funcional: {href}")
                    else:
                        print(f"  [{i+1}] ❌ Link quebrado ({res.status_code}): {href}")
                        error_count += 1
                except Exception:
                    print(f"  [{i+1}] ⚠️  Erro ao acessar: {href}")
                    error_count += 1
            
            # Busca botões
            buttons = soup.find_all('button')
            print(f"🔎 Encontrados {len(buttons)} botões renderizados (sem teste de ação JS nesta versão leve).")
            
            if error_count == 0:
                print("🎉 Teste de cliques (estático) concluído sem erros de requisição!")
            else:
                print(f"⚠️ Teste concluído com {error_count} problemas de link.")
                
        else:
            print(f"❌ Falha ao acessar página inicial. Status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor. O app está rodando?")
    except Exception as e:
        print(f"❌ O Testador tropeçou: {e}")

if __name__ == "__main__":
    testar_cliques()
