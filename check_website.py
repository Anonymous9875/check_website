import requests
import json
from urllib.parse import quote
import os
import sys
import time
from typing import Dict, Any

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system('clear' if os.name == 'posix' else 'cls')

def check_website_status(url: str) -> None:
    """
    Verifica el estado de un sitio web usando check-host.net y mide tiempos de respuesta.
    """
    try:
        # Codificar la URL para la solicitud
        encoded_url = quote(url, safe=':/')
        
        # URL de la API con parámetros optimizados
        api_url = f"https://check-host.net/check-http?host={encoded_url}&max_nodes=47"
        
        headers = {
            curl -H "Accept: application/json" \
            https://check-host.net/check-result/806dfa,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # Medir tiempo de inicio
        start_time = time.time()
        
        # Realizar la solicitud
        response = requests.get(api_url, headers=headers, timeout=90)
        request_time = round(time.time() - start_time, 3)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                if data.get("ok") == 1:
                    print(f"\nResultados para: {url}")
                    print(f"Tiempo de solicitud inicial: {request_time}s")
                    
                    nodes: Dict[str, Any] = data.get("nodes", {})
                    if not nodes:
                        print("No se obtuvieron resultados de nodos. Verificación en proceso...")
                        return
                    
                    online_count = 0
                    total_nodes = len(nodes)
                    
                    # Procesar y mostrar resultados por nodo
                    for node, result in sorted(nodes.items()):
                        status = result[0] if result else 0
                        response_time = result[2] if result and len(result) > 2 and result[2] is not None else "N/A"
                        
                        if status == 1:
                            status_str = f"[+] {node}: Online"
                            online_count += 1
                            if isinstance(response_time, (int, float)):
                                time_str = f"{response_time:.3f}s"
                            else:
                                time_str = "Tiempo no disponible"
                            print(f"{status_str} (Respuesta: {time_str})")
                        else:
                            print(f"[-] {node}: Offline")
                    
                    # Mostrar resumen
                    percentage = (online_count / total_nodes) * 100
                    print(f"\nResumen: {online_count}/{total_nodes} nodos online ({percentage:.1f}%)")
                    
                else:
                    print("Error en la verificación del servidor.")
            except json.JSONDecodeError:
                print("Error: Respuesta del servidor no válida (JSON corrupto)")
        else:
            print(f"Error en la solicitud: Código HTTP {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("Error: Tiempo de espera agotado (timeout)")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

def main():
    # Verificar dependencias
    try:
        import requests
    except ImportError:
        print("Error: La librería 'requests' no está instalada.")
        print("Instálala con: pip install requests")
        sys.exit(1)

    # Configurar codificación
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    clear_screen()
    print("Herramienta de verificación de sitios web")
    print("Powered by check-host.net (max 47 nodos)")
    print("----------------------------------------")
    
    while True:
        website = input("Ingresa la URL (ej: https://google.com) o 'exit' para salir: ").strip()
        
        if website.lower() == 'exit':
            print("¡Programa terminado!")
            break
            
        if not website:
            print("Por favor, ingresa una URL válida")
            continue
            
        # Añadir protocolo si falta
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
            
        check_website_status(website)
        print("\n----------------------------------------")

if __name__ == "__main__":
    main()
