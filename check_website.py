import requests
import json
from urllib.parse import quote

def check_website_status(url):
    try:
        # Codificar la URL para que sea segura en la solicitud
        encoded_url = quote(url)
        
        # URL de la API de check-host.net
        api_url = f"https://check-host.net/check-http?host={encoded_url}"
        
        # Headers necesarios para la solicitud
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
                
                for node, result in nodes.items():
                    if result[0] == 1:
                        print(f"✓ {node}: Online (Tiempo de respuesta: {result[2]}s)")
                    else:
                        print(f"✗ {node}: Offline")
            else:
                print("Error en la verificación. Intenta de nuevo.")
        else:
            print(f"Error en la solicitud: Código {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
    except json.JSONDecodeError:
        print("Error al procesar la respuesta del servidor")

def main():
    print("Herramienta para verificar si una página web está caída")
    print("Utilizando check-host.net")
    print("----------------------------------------")
    
    while True:
        # Solicitar URL al usuario
        website = input("Ingresa la URL a verificar (ejemplo: https://google.com) o 'salir' para terminar: ")
        
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
