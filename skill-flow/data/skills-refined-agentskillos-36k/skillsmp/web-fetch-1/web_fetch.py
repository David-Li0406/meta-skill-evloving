#!/usr/bin/env python3
"""
Web Fetch - Realiza peticiones HTTP y devuelve el contenido
"""

import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Any


def fetch_url(url: str, method: str = "GET", headers: Dict[str, str] = None, 
              data: str = None, timeout: int = 10) -> Dict[str, Any]:
    """
    Realiza una petición HTTP y devuelve la respuesta
    
    Args:
        url: URL a consultar
        method: Método HTTP (GET, POST, PUT, DELETE, etc.)
        headers: Headers adicionales
        data: Datos para POST/PUT (JSON string)
        timeout: Timeout en segundos
    
    Returns:
        Dict con status, headers y content
    """
    result = {
        "url": url,
        "method": method,
        "success": False,
        "status_code": None,
        "headers": {},
        "content": None,
        "error": None
    }
    
    try:
        # Preparar headers
        req_headers = {
            'User-Agent': 'Mozilla/5.0 (Web-Fetch-Skill/1.0)'
        }
        if headers:
            req_headers.update(headers)
        
        # Preparar datos
        req_data = None
        if data:
            req_data = data.encode('utf-8')
            if 'Content-Type' not in req_headers:
                req_headers['Content-Type'] = 'application/json'
        
        # Crear request
        request = urllib.request.Request(
            url,
            data=req_data,
            headers=req_headers,
            method=method
        )
        
        # Realizar petición
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result["success"] = True
            result["status_code"] = response.getcode()
            result["headers"] = dict(response.headers)
            
            # Leer contenido
            content = response.read().decode('utf-8')
            
            # Intentar parsear como JSON
            try:
                result["content"] = json.loads(content)
                result["content_type"] = "json"
            except json.JSONDecodeError:
                result["content"] = content
                result["content_type"] = "text"
    
    except urllib.error.HTTPError as e:
        result["status_code"] = e.code
        result["error"] = f"HTTP Error {e.code}: {e.reason}"
        try:
            result["content"] = e.read().decode('utf-8')
        except:
            pass
    
    except urllib.error.URLError as e:
        result["error"] = f"URL Error: {e.reason}"
    
    except Exception as e:
        result["error"] = f"Error: {str(e)}"
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Realiza peticiones HTTP y devuelve el contenido"
    )
    parser.add_argument("url", help="URL a consultar")
    parser.add_argument("--method", "-m", default="GET",
                        choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
                        help="Método HTTP (default: GET)")
    parser.add_argument("--header", "-H", action="append", dest="headers",
                        help="Header adicional (formato: 'Key: Value')")
    parser.add_argument("--data", "-d", help="Datos para POST/PUT (JSON)")
    parser.add_argument("--timeout", "-t", type=int, default=10,
                        help="Timeout en segundos (default: 10)")
    parser.add_argument("--pretty", "-p", action="store_true",
                        help="Formatear JSON de forma legible")
    
    args = parser.parse_args()
    
    # Parsear headers
    headers = {}
    if args.headers:
        for header in args.headers:
            if ':' in header:
                key, value = header.split(':', 1)
                headers[key.strip()] = value.strip()
    
    # Realizar petición
    result = fetch_url(
        url=args.url,
        method=args.method,
        headers=headers if headers else None,
        data=args.data,
        timeout=args.timeout
    )
    
    # Output
    if args.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
