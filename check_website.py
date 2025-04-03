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

def initiate_check(url: str) -> str:
    """Inicia una verificación en check-host.net y retorna el ID del resultado."""
    try:
        encoded_url = quote(url, safe=':/')
        api_url = f"https://check-host.net/check-http?host={encoded_url}"
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get("request_id")
        else:
            print(f"Error al iniciar verificación: Código HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al iniciar verificación: {str(e)}")
        return None

def check_website_status(url: str) -> None:
    """
    Verifica el estado de un sitio web usando check-host.net y mide tiempos de respuesta.
    """
    try:
        # Iniciar la verificación
        request_id = initiate_check(url)
        if not request_id:
            return

        # URL para obtener resultados
        api_url = f"https://check-host.net/check-result/{request_id}"
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # Esperar un momento para que los nodos procesen
        time.sleep(2)
        
        # Medir tiempo de inicio
        start_time = time.time()
        
        # Realizar la solicitud
        response = requests.get(api_url, headers=headers, timeout=90)
        request_time = round(time.time() - start_time, 3)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                print(f"\nResultados para: {url}")
                print(f"Tiempo de solicitud inicial: {request_time}s")
                
                nodes: Dict[str, Any] = data or {}
                if not nodes:
                    print("No se obtuvieron resultados de nodos. Verificación en proceso...")
                    return
                
                online_count = 0
                total_nodes = len(nodes)
                
                # Procesar y mostrar resultados por nodo
                for node, result in sorted(nodes.items()):
                    if result and isinstance(result, list) and len(result) > 0:
                        status = result[0].get('status', 0) if result[0] else 0
                        response_time = result[0].get('time', 'N/A') if result[0] else 'N/A'
                        
                        if status == 1:
                            status_str = f"[+] {node}: Online"
                            online_count += 1
                            time_str = f"{response_time}s" if isinstance(response_time, (int, float)) else "Tiempo no disponible"
                            print(f"{status_str} (Respuesta: {time_str})")
                        else:
                            error = result[0].get('error', 'Offline') if result[0] else 'Offline'
                            print(f"[-] {node}: {error}")
                    else:
                        print(f"[-] {node}: No responde")
                
                # Mostrar resumen
                percentage = (online_count / total_nodes) * 100
                print(f"\nResumen: {online_count}/{total_nodes} nodos online ({percentage:.1f}%)")
                
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
    print("Powered by check-host.net")
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
