import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import sys
import io
from dotenv import load_dotenv

# Fix UTF-8 for Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load Environment
load_dotenv()
COOKIE_VALOR = os.getenv("CDR_FULL_COOKIE")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': COOKIE_VALOR if COOKIE_VALOR else "",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.cdrmedios.com/'
}

BASE_URL = "https://www.cdrmedios.com"

productos_totales = []

def extraer_productos_de_pagina(soup, categoria_nombre):
    """
    Extrae productos de una página de listado de CDR.
    """
    articulos = soup.find_all('article')
    
    if not articulos:
        return 0
    
    count = 0
    for art in articulos:
        try:
            link_tag = art.find('a', href=True)
            if not link_tag:
                continue
            
            href = link_tag['href']
            if href.startswith('/'):
                full_url = BASE_URL + href
            elif not href.startswith('http'):
                full_url = BASE_URL + '/' + href
            else:
                full_url = href
            
            if '/catalogo/' not in full_url:
                continue
            
            nombre = "Sin nombre"
            nombre_tag = (
                art.find('h2') or 
                art.find('h3') or 
                art.find('span', class_='name') or
                art.find('div', class_='name') or
                link_tag 
            )
            if nombre_tag:
                nombre = nombre_tag.get_text(strip=True)
            
            precio_cdr = 0.0
            precio_tag = (
                art.find('span', class_='price') or
                art.find('div', class_='price') or
                art.find('span', class_='precio')
            )
            
            if precio_tag:
                precio_texto = precio_tag.get_text(strip=True)
                precio_texto = (
                    precio_texto
                    .replace('U$S', '')
                    .replace('USD', '')
                    .replace('$', '')
                    .replace('.', '')
                    .replace(',', '.')
                    .strip()
                )
                try:
                    precio_cdr = float(precio_texto)
                except:
                    precio_cdr = 0.0
            
            stock = "Disponible"
            stock_tag = art.find('span', class_='stock')
            if stock_tag:
                stock = stock_tag.get_text(strip=True)
            
            productos_totales.append({
                'Categoria': categoria_nombre,
                'Nombre': nombre,
                'Precio_CDR_USD': precio_cdr,
                'Stock': stock,
                'URL': full_url
            })
            count += 1
            
        except Exception as e:
            print(f"      Advertencia: Error en un producto: {e}")
            continue
    
    return count

def minar_categoria_completa(url_base, nombre_cat):
    """
    Mina una categoría completa siguiendo la paginación.
    """
    print(f"\n[Categoria] {nombre_cat}")
    print(f"   URL: {url_base}")
    
    pagina = 1
    productos_categoria = 0
    
    while True:
        if '?' in url_base:
            url_actual = f"{url_base}&pag={pagina}"
        else:
            url_actual = f"{url_base}?pag={pagina}"
        
        print(f"   [Pagina {pagina}] Scrapeando...")
        
        try:
            r = requests.get(url_actual, headers=HEADERS, timeout=15)
            
            if r.status_code != 200:
                print(f"   [STOP] Status {r.status_code} - Fin de categoria")
                break
            
            soup = BeautifulSoup(r.text, 'html.parser')
            cantidad = extraer_productos_de_pagina(soup, nombre_cat)
            
            if cantidad == 0:
                print(f"   [STOP] No se encontraron productos - Fin de categoria")
                break
            
            productos_categoria += cantidad
            print(f"   [OK] {cantidad} productos extraidos")
            
            pagina += 1
            time.sleep(random.uniform(1.5, 3.0))
            
        except Exception as e:
            print(f"   [ERROR] {e}")
            break
    
    print(f"   [TOTAL] {productos_categoria} productos en {nombre_cat}")
    return productos_categoria

def exportar_csv(filename="CDR_MASTER_DB.csv"):
    if productos_totales:
        df = pd.DataFrame(productos_totales)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"   Archivo generado: {filename}")
        return True
    return False

if __name__ == "__main__":
    # Test run
    pass
