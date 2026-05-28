import os
import sys
import io
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Garante que a saída use UTF-8 para evitar erros com emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verificar_links(start_url="http://localhost:3000"):
    """
    O Verificador de Links (Crawler Simples):
    Busca links internos e verifica se respondem com sucesso.
    """
    print(f"🔗 [GUARDIÃO] Mapeando e verificando links a partir de {start_url}...")
    
    visited = set()
    to_visit = {start_url}
    broken_links = []
    base_domain = urlparse(start_url).netloc
    
    max_pages = 20 # Limite para não rodar infinito
    count = 0
    
    while to_visit and count < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
            
        try:
            res = requests.get(url, timeout=3)
            visited.add(url)
            count += 1
            
            status_icon = "✅" if res.status_code < 400 else "❌"
            print(f"{status_icon} [{res.status_code}] Verificando: {url}")
            
            if res.status_code >= 400:
                broken_links.append((url, res.status_code))
                continue
            
            # Se for interno, busca mais links
            if base_domain in url:
                soup = BeautifulSoup(res.text, "html.parser")
                for tag in soup.find_all("a", href=True):
                    href = tag["href"]
                    full_url = urljoin(url, href)
                    
                    # Filtra apenas http/https
                    if full_url.startswith("http"):
                        # Adiciona apenas se for do mesmo domínio para aprofundar a busca
                        if base_domain in urlparse(full_url).netloc:
                            if full_url not in visited:
                                to_visit.add(full_url)
                        # Se for externo, poderíamos só checar HEAD, mas aqui focamos no interno
                        
        except Exception as e:
            print(f"⚠️  Erro ao acessar {url}: {e}")
            broken_links.append((url, "Erro de Conexão"))
            
    print("-" * 30)
    print(f"🏁 Verificação concluída. {count} páginas analisadas.")
    
    if broken_links:
        print(f"🚨 Encontrados {len(broken_links)} links quebrados:")
        for link, status in broken_links:
            print(f"   - {link} (Status: {status})")
    else:
        print("🎉 Nenhum link quebrado encontrado! O site está sólido.")

if __name__ == "__main__":
    verificar_links()
