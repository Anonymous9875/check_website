import requests
import json
from urllib.parse import quote
import os
import sys
import time

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system('clear' if os.name == 'posix' else 'cls')

def check_website_status(url):
    try:
        # Codificar la URL para que sea segura en la solicitud
        encoded_url = quote(url)
        
        # URL inicial de la API
        api_url = f"https://check-host.net/check-http?host={encoded_url}"
        
        # Headers necesarios
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # Primera solicitud para obtener el enlace del reporte
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            request_id = data.get("request_id")
            if not request_id:
                print("No se pudo obtener el ID de la solicitud")
                return
                
            # Obtener el enlace del resultado
            result_url = f"https://check-host.net/check-result/{request_id}"
            
            # Esperar y verificar el resultado
            print(f"\nVerificando {url} en tiempo real...")
            max_attempts = 10
            attempt = 0
            
            while attempt < max_attempts:
                result_response = requests.get(result_url, headers=headers, timeout=10)
                if result_response.status_code == 200:
                    result_data = result_response.json()
                    
                    # Verificar si hay resultados disponibles
                    nodes = result_data.items()
                    if len(nodes) > 0 and any(node[1] is not None for node in nodes):
                        print(f"\nResultados para: {url}")
                        online_count = 0
                        total_nodes = 0
                        
                        for node, result in nodes:
                            total_nodes += 1
                            if result and isinstance(result, list) and len(result) > 0:
                                if result[0] == 1:  # 1 significa online
                                    online_count += 1
                                    print(f"[+] {node}: Online (Tiempo de respuesta: {result[2]}s)")
                                else:
                                    print(f"[-] {node}: Offline")
                        
                        # Mostrar resumen
                        print(f"\nResumen: {online_count}/{total_nodes} nodos reportan el sitio como Online")
                        return
                        
                # Esperar antes del próximo intento
                time.sleep(2)
                attempt += 1
            
            print("No se obtuvieron resultados completos después de varios intentos")
        else:
            print(f"Error en la solicitud inicial: Código {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
    except json.JSONDecodeError:
        print("Error al procesar la respuesta del servidor")

def main():
    try:
        import requests
    except ImportError:
        print("Error: La librería 'requests' no está instalada.")
        print("Instálala con: pip install requests")
        print("En Termux, usa: pkg install python && pip install requests")
        sys.exit(1)

    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

    clear_screen()
    print("Herramienta para verificar si una página web está caída")
    print("Utilizando check-host.net - Verificación en tiempo real")
    print("----------------------------------------")
    
    while True:
        website = input("Ingresa la URL a verificar (ejemplo: https://google.com) o 'salir' para terminar: ")
        
        if website.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
            
        check_website_status(website)
        print("\n----------------------------------------")

if __name__ == "__main__":
    main() 
