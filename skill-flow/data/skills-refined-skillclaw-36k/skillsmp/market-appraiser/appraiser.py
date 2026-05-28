from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
import re
import os

def generar_query_inteligente(titulo_original):
    """
    Convierte un título largo de proveedor en una búsqueda efectiva de ML.
    """
    query = titulo_original.lower()
    
    palabras_basura = [
        " - ", "alta velocidad", "alto rendimiento", "ultra rápido", 
        "con carrete", "sin carrete", "original", "alto", "calidad", "premium",
        "español", "teclado numérico", "slim", "clase 10", "reusable",
        "con", "para", "compatible", "garantía", "rendimiento", "velocidad",
        "inalámbrico", "inalambrico", "diseño", "elegante", "compacto",
        "profesional", "máxima", "maxima", "eficiencia", "durabilidad",
        "superior", "excelente", "óptimo", "optimo", "innovador",
        "tecnología", "tecnologia", "sistema", "nuevo", "nueva"
    ]
    
    for basura in palabras_basura:
        query = query.replace(basura, " ")
    
    query = re.sub(r'\s+', ' ', query).strip()
    
    palabras = query.split()
    palabras_clave = [p for p in palabras if len(p) > 2 or p.isdigit() or any(c.isdigit() for c in p)]
    
    return " ".join(palabras_clave[:6])

def obtener_precio_ml(busqueda, filtro_palabras_clave=None):
    """
    Busca un producto en MercadoLibre Uruguay y devuelve el precio mínimo.
    """
    # Use context manager correctly
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            query = busqueda.replace(" ", "-").lower()
            url = f"https://listado.mercadolibre.com.uy/{query}"
            
            print(f"   Consultando ML: {busqueda[:60]}...")
            page.goto(url, timeout=15000)
            
            try:
                page.wait_for_selector('ol.ui-search-layout', timeout=8000)
            except:
                print(f"   Timeout o sin resultados")
                browser.close()
                return None

            items = page.query_selector_all('li.ui-search-layout__item')
            precios_encontrados = []

            for item in items[:8]:
                titulo_el = item.query_selector('.ui-search-item__title')
                if not titulo_el:
                    continue
                    
                titulo = titulo_el.inner_text().lower()
                
                if filtro_palabras_clave:
                    if not all(palabra.lower() in titulo for palabra in filtro_palabras_clave):
                        continue
                    
                    palabras_exclusion = ['aero', 'silk', 'seda', 'pro', 'plus', 'premium']
                    if any(excl in titulo for excl in palabras_exclusion):
                        continue
                
                precio_el = item.query_selector('.andes-money-amount__fraction')
                if precio_el:
                    try:
                        precio_texto = precio_el.inner_text().replace('.', '').replace(',', '.')
                        precio_num = float(precio_texto)
                        
                        if 5 < precio_num < 50000:
                            precios_encontrados.append(precio_num)
                    except:
                        continue

            browser.close()

            if precios_encontrados:
                precio_min = min(precios_encontrados)
                print(f"   Encontrados {len(precios_encontrados)} precios. Min: ${precio_min:.0f}")
                return precio_min
            else:
                return None
                
        except Exception as e:
            print(f"   Error: {e}")
            return None

def determinar_filtros(nombre_producto):
    nombre_lower = nombre_producto.lower()
    if 'basic' in nombre_lower: return ['basic']
    if 'aero' in nombre_lower: return ['aero']
    if 'silk' in nombre_lower or 'seda' in nombre_lower: return ['silk']
    
    palabras_clave = []
    marcas = ['bambu', 'apple', 'samsung', 'kingston', 'crucial', 'biostar', 
              'palit', 'lexar', 'hikvision', 'xiaomi', 'benq', 'deepcool']
    for marca in marcas:
        if marca in nombre_lower:
            palabras_clave.append(marca)
            break
            
    # Add simple heuristic for specific models if needed
    return palabras_clave if palabras_clave else None

def run_appraisal(input_csv, output_csv):
    print("\n========================================")
    print(" TASADOR v2 (Playwright + Filtros)")
    print("========================================\n")
    
    if not os.path.exists(input_csv):
        print(f"[ERROR] No se encontro {input_csv}")
        return

    try:
        df = pd.read_csv(input_csv, encoding='utf-8')
        print(f"[OK] Leidos {len(df)} productos\n")
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    
    resultados = []
    total_procesar = min(10, len(df)) # Keeping the strict limit from original for safety
    
    for index in range(total_procesar):
        row = df.iloc[index]
        nombre_producto = row['Nombre']
        precio_venta_nuestro = row['Precio_Venta']
        
        print(f"\n[{index+1}/{total_procesar}] {nombre_producto}")
        
        query_limpia = generar_query_inteligente(nombre_producto)
        filtros = determinar_filtros(nombre_producto)
        
        precio_ml = obtener_precio_ml(query_limpia, filtros)
        
        if not precio_ml:
            resultados.append({
                **row.to_dict(),
                'Precio_ML_Min': None,
                'Diferencia_Porcentaje': None,
                'Alerta': 'SIN_DATOS_ML'
            })
        else:
            diferencia = ((precio_venta_nuestro - precio_ml) / precio_ml) * 100
            
            if abs(diferencia) <= 15:
                alerta = 'OK'
            elif diferencia > 15:
                alerta = 'PRECIO_ALTO'
            else:
                alerta = 'OPORTUNIDAD'
            
            resultados.append({
                **row.to_dict(),
                'Precio_ML_Min': precio_ml,
                'Diferencia_Porcentaje': diferencia,
                'Alerta': alerta
            })
        
        if index < total_procesar - 1:
            delay = random.uniform(3, 6)
            time.sleep(delay)
    
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"\n[OK] Resultados: {output_csv}\n")
