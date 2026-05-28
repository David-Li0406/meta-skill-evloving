import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

# Configurações
BASE_URL = "http://localhost:3000"
OUTPUT_DIR = ".agent/artifacts/mobile_screenshots"
DEVICES = {
    "iPhone 12": {"width": 390, "height": 844},
    "Samsung Galaxy S8": {"width": 360, "height": 740},
    "iPad Mini": {"width": 768, "height": 1024}
}
PAGES = ["/", "/dashboard", "/conversor", "/analise"]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run_simulation():
    """Roda a simulação de acesso mobile e tira screenshots."""
    print("[INFO] Iniciando Simulador de Celular (O Guardiao)...")
    ensure_dir(OUTPUT_DIR)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for device_name, viewport in DEVICES.items():
            print(f"   [TEST] Testando em: {device_name} ({viewport['width']}x{viewport['height']})...")
            # Configura um contexto com o viewport do dispositivo
            context = browser.new_context(
                viewport=viewport,
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1" # Fake UA
            )
            page = context.new_page()
            
            for route in PAGES:
                url = f"{BASE_URL}{route}"
                try:
                    print(f"      [LINK] Visitando: {url}")
                    page.goto(url, wait_until="networkidle", timeout=10000)
                    # Espera animações
                    time.sleep(1) 
                    
                    # Nome do arquivo de screenshot
                    safe_route = route.replace("/", "_") or "_home"
                    filename = f"{device_name.replace(' ', '_')}{safe_route}.png"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    page.screenshot(path=filepath, full_page=True)
                    print(f"      [FOTO] Screenshot salvo: {filepath}")
                    
                except Exception as e:
                    print(f"      [ERRO] Erro ao acessar {url}: {e}")
            
            context.close()
        
        browser.close()
    
    print(f"\n[SUCESSO] Simulacao concluida! Screenshots salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        print(f"[FALHA] Falha critica no simulador: {e}")
        print("[DICA] Verifique se o app esta rodando na porta 3000.")
