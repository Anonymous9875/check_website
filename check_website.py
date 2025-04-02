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
        encoded_url = quote(url)
        
        # URL de la API de check-host.net con max_nodes=47 como en el comando curl
        api_url = f"https://check-host.net/check-http?host={encoded_url}&max_nodes=47"
        
        # Headers necesarios para la solicitud, incluyendo el Accept del comando curl
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
            if data.get("ok") == 1:
                print(f"\nResultados para: {url}")
                nodes = data.get("nodes", {})
                
                if not nodes:
                    print("No se obtuvieron resultados de nodos. Puede que la verificación esté en proceso.")
                else:
                    online_count = 0
                    total_nodes = len(nodes)
                    for node, result in nodes.items():
                        if result[0] == 1:
                            print(f"[+] {node}: Online (Tiempo de respuesta: {result[2]}s)")
                            online_count += 1
                        else:
                            print(f"[-] {node}: Offline")
                    print(f"\nResumen: {online_count}/{total_nodes} nodos reportan el sitio como Online")
            else:
                print("Error en la verificación. Intenta de nuevo.")
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
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

    clear_screen()
    print("Herramienta para verificar si una página web está caída")
    print("Utilizando check-host.net con hasta 47 nodos")
    print("----------------------------------------")
    
    while True:
        # Solicitar URL al usuario
        website = input("Ingresa la URL a verificar (ejemplo: https://google.com) o 'exit' para terminar: ")
        
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
