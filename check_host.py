import requests
import json
from urllib.parse import quote
import os
import sys
import time

# Códigos ANSI para colores
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_BOLD = "\033[1m"

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_color(text, color):
    """Imprime texto en el color especificado."""
    print(f"{color}{text}{COLOR_RESET}")

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
            
            # Procesar la respuesta inicial para obtener el request_id
            if "request_id" in data:
                request_id = data["request_id"]
                nodes = data["nodes"]
                
                print_color(f"\nVerificando: {url}", COLOR_CYAN)
                print_color("Esperando resultados de los servidores...", COLOR_YELLOW)
                
                # Esperar unos segundos para que los servidores completen las pruebas
                time.sleep(5)
                
                # Hacer una segunda solicitud para obtener los resultados
                result_url = f"https://check-host.net/check-result/{request_id}"
                result_response = requests.get(result_url, headers=headers, timeout=15)
                
                if result_response.status_code == 200:
                    results = result_response.json()
                    
                    if results:
                        print_color(f"\nResultados para: {url}", COLOR_CYAN)
                        for node in nodes:
                            if node in results and results[node] is not None:
                                node_result = results[node][0]
                                if isinstance(node_result, list):
                                    if node_result[0] is not None:
                                        if node_result[0] == 1:
                                            response_time = node_result[1] if len(node_result) > 1 else "N/A"
                                            print_color(f"[+] {node}: Online (Tiempo de respuesta: {response_time:.3f}s)", COLOR_GREEN)
                                        else:
                                            error_msg = node_result[1] if len(node_result) > 1 else "Error desconocido"
                                            print_color(f"[-] {node}: Offline (Error: {error_msg})", COLOR_RED)
                                    else:
                                        print_color(f"[?] {node}: No se pudo determinar el estado", COLOR_YELLOW)
                                else:
                                    print_color(f"[?] {node}: Formato de respuesta inesperado", COLOR_YELLOW)
                            else:
                                print_color(f"[?] {node}: No hay datos disponibles", COLOR_YELLOW)
                    else:
                        print_color("Los resultados aún no están disponibles. Intenta nuevamente más tarde.", COLOR_YELLOW)
                else:
                    print_color(f"Error al obtener resultados: Código {result_response.status_code}", COLOR_RED)
            else:
                print_color("Error: No se pudo iniciar la verificación. La respuesta del servidor no contiene request_id.", COLOR_RED)
        else:
            print_color(f"Error en la solicitud: Código {response.status_code}", COLOR_RED)
            
    except requests.exceptions.RequestException as e:
        print_color(f"Error de conexión: {str(e)}", COLOR_RED)
    except json.JSONDecodeError:
        print_color("Error al procesar la respuesta del servidor", COLOR_RED)

def main():
    # Verificar si requests está instalado
    try:
        import requests
    except ImportError:
        print_color("Error: La librería 'requests' no está instalada.", COLOR_RED)
        print_color("Instálala con: pip install requests", COLOR_YELLOW)
        print_color("En Termux, usa: pkg install python && pip install requests", COLOR_YELLOW)
        sys.exit(1)

    # Configurar codificación UTF-8
    if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
        sys.stdout.reconfigure(encoding='utf-8')

    clear_screen()
    print_color("Herramienta para verificar si una página web está caída", COLOR_BOLD + COLOR_CYAN)
    print_color("Utilizando check-host.net", COLOR_WHITE)
    print_color("----------------------------------------", COLOR_WHITE)
    
    while True:
        # Solicitar URL al usuario
        website = input(f"{COLOR_WHITE}Ingresa la URL a verificar (ejemplo: google.com) o 'salir' para terminar: {COLOR_RESET}").strip()
        
        if website.lower() == 'salir':
            print_color("¡Hasta luego!", COLOR_CYAN)
            break
            
        # Asegurarse de que la URL tenga el protocolo
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
            
        # Verificar el estado del sitio
        check_website_status(website)
        
        print_color("\n----------------------------------------", COLOR_WHITE)

if __name__ == "__main__":
    main()