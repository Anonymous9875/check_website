import requests
import json
from urllib.parse import quote
import os
import sys

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system('clear' if os.name == 'posix' else 'cls')

def check_website_status(url):
    try:
        # Codificar la URL para que sea segura en la solicitud
        encoded_url = quote(url, safe='')
        
        # URL de la API de check-host.net
        api_url = f"https://check-host.net/check-http?host={encoded_url}"
        
        # Headers necesarios para la solicitud
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # Hacer la solicitud GET a la API
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            
            # Procesar la respuesta
            if "nodes" in data and "result" in data:
                print(f"\nResultados para: {url}")
                request_id = data["request_id"]
                nodes = data["nodes"]
                results = data["result"]
                
                for node in nodes:
                    if node in results and results[node]:
                        result = results[node][0]
                        if isinstance(result, list) and len(result) >= 3:
                            if result[0] == 1:
                                print(f"[+] {node}: Online (Tiempo de respuesta: {result[1]:.2f}s)")
                            else:
                                print(f"[-] {node}: Offline (Error: {result[1]})")
                        else:
                            print(f"[?] {node}: Respuesta inesperada del servidor")
                    else:
                        print(f"[?] {node}: No hay datos disponibles")
            else:
                print("Error en la verificación. La respuesta del servidor no contiene los datos esperados.")
        else:
            print(f"Error en la solicitud: Código {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
    except json.JSONDecodeError:
        print("Error al procesar la respuesta del servidor")

def main():
    # Verificar si requests está instalado
    try:
        import requests
    except ImportError:
        print("Error: La librería 'requests' no está instalada.")
        print("Instálala con: pip install requests")
        print("En Termux, usa: pkg install python && pip install requests")
        sys.exit(1)

    # Configurar codificación UTF-8
    if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
        sys.stdout.reconfigure(encoding='utf-8')

    clear_screen()
    print("Herramienta para verificar si una página web está caída")
    print("Utilizando check-host.net")
    print("----------------------------------------")
    
    while True:
        # Solicitar URL al usuario
        website = input("Ingresa la URL a verificar (ejemplo: google.com) o 'salir' para terminar: ").strip()
        
        if website.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        # Asegurarse de que la URL tenga el protocolo
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
            
        # Verificar el estado del sitio
        check_website_status(website)
        
        print("\n----------------------------------------")

if __name__ == "__main__":
    main()