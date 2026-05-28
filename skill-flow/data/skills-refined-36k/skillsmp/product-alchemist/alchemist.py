import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
MODELO_LOCAL = os.getenv("MODELO_LOCAL", "qwen2.5-coder-7b-instruct")

def mejorar_producto(titulo_crudo, specs_cruda, precio_usd):
    """
    Toma datos crudos y devuelve JSON bonito usando LM Studio.
    """
    print(f"IA Local Procesando: {titulo_crudo}...")

    prompt = f"""
    Eres un experto en Hardware y E-commerce.
    Convierte estos datos crudos en una ficha de producto vendedora (JSON).
    
    DATOS:
    - Título original: {titulo_crudo}
    - Specs: {specs_cruda}
    - Precio: {precio_usd} USD
    
    REQUISITOS JSON:
    {{
        "titulo_nuevo": "Título SEO optimizado (max 60 chars)",
        "frase_gancho": "Una frase corta impactante para vender el beneficio",
        "html_descripcion": "HTML limpio (<h2>, <ul>, <p>) describiendo el producto. Enfócate en beneficios (Velocidad, FPS). No uses markdown ```html.",
        "tags": ["tag1", "tag2", "tag3"]
    }}
    
    Responde SOLO con el JSON.
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODELO_LOCAL,
        "messages": [
            {"role": "system", "content": "Eres un experto en hardware que solo responde en formato JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(LM_STUDIO_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            texto_respuesta = result['choices'][0]['message']['content']
            texto_limpio = texto_respuesta.replace('```json', '').replace('```', '').strip()
            return json.loads(texto_limpio)
        else:
            print(f"Error en LM Studio: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error conectando con la IA Local: {e}")
        return None

if __name__ == "__main__":
    # Test
    pass
