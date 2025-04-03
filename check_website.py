import requests
import time
import os
import sys

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    # Para Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Para Linux, Mac, Termux
    else:
        _ = os.system('clear')

def check_website_status(url):
    """Verifica el estado de una URL usando check-host.net."""
    check_url = f"https://check-host.net/check-http?host={url}"
    
    try:
        headers = {"Accept": "application/json"}
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"Error al iniciar la verificación: {response.status_code}"
        
        result_data = response.json()
        request_id = result_data.get("request_id")
        
        if not request_id:
            return "No se pudo obtener el ID de la solicitud"
        
        time.sleep(3)
        
        result_url = f"https://check-host.net/check-result/{request_id}"
        result_response = requests.get(result_url, headers=headers, timeout=10)
        
        if result_response.status_code != 200:
            return f"Error al obtener resultados: {result_response.status_code}"
        
        results = result_response.json()
        
        status_summary = []
        for node, result in results.items():
            if result and isinstance(result, list) and len(result) > 0:
                status = result[0]
                if isinstance(status, list) and len(status) >= 2:
                    response_time = status[0]  # Tiempo de respuesta
                    status_code = status[1]   # Código de estado HTTP
                    
                    if status_code == 200:
                        status_summary.append(f"Nodo {node}: Online (Tiempo: {response_time}s)")
                    else:
                        status_summary.append(f"Nodo {node}: Problema (Código: {status_code})")
        
        if not status_summary:
            return "No se obtuvieron resultados válidos"
        
        return "\n".join(status_summary)
    
    except requests.exceptions.Timeout:
        return "Tiempo de espera agotado al conectar con el servidor"
    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

if __name__ == "__main__":
    # Asegurar codificación UTF-8 para todos los sistemas
    if sys.stdout.encoding != 'UTF-8':
        if sys.version_info >= (3, 7):
            sys.stdout.reconfigure(encoding='utf-8')
        else:
            # Para versiones antiguas de Python en Windows
            sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

    while True:
        clear_screen()  # Limpiar pantalla al inicio de cada iteración
        print("=== Verificador de Estado de Sitios Web ===")
        website = input("Introduce la URL a verificar (ejemplo: google.com) o 'exit' para salir: ")
        
        if website.lower() == "exit":
            clear_screen()
            print("Saliendo del programa...")
            time.sleep(1)  # Pequeña pausa antes de salir
            break
        
        if not website.startswith("http"):
            website = "http://" + website
        
        print(f"\nVerificando {website}...")
        result = check_website_status(website)
        print(result)
        input("\nPresiona Enter para continuar...")  # Pausa para ver resultados
