# Node data organized by continent
NODES_BY_CONTINENT = {
    "EU": [
        "bg1.node.check-host.net", "ch1.node.check-host.net", "cz1.node.check-host.net",
        "de1.node.check-host.net", "de4.node.check-host.net", "es1.node.check-host.net",
        "fi1.node.check-host.net", "fr1.node.check-host.net", "fr2.node.check-host.net",
        "hu1.node.check-host.net", "it2.node.check-host.net", "lt1.node.check-host.net",
        "md1.node.check-host.net", "nl1.node.check-host.net", "nl2.node.check-host.net",
        "pl1.node.check-host.net", "pl2.node.check-host.net", "pt1.node.check-host.net",
        "rs1.node.check-host.net", "se1.node.check-host.net", "uk1.node.check-host.net"
    ],
    "AS": [
        "hk1.node.check-host.net", "il1.node.check-host.net", "il2.node.check-host.net",
        "in1.node.check-host.net", "in2.node.check-host.net", "ir1.node.check-host.net",
        "ir3.node.check-host.net", "ir5.node.check-host.net", "ir6.node.check-host.net",
        "jp1.node.check-host.net", "kz1.node.check-host.net", "tr1.node.check-host.net",
        "tr2.node.check-host.net", "vn1.node.check-host.net"
    ],
    "NA": [
        "us1.node.check-host.net", "us2.node.check-host.net", "us3.node.check-host.net"
    ],
    "SA": [
        "br1.node.check-host.net"
    ],
    "EU-EAST": [
        "ru1.node.check-host.net", "ru2.node.check-host.net", "ru3.node.check-host.net",
        "ru4.node.check-host.net", "ua1.node.check-host.net", "ua2.node.check-host.net",
        "ua3.node.check-host.net"
    ]
}

# All nodes combined
ALL_NODES = []
for nodes in NODES_BY_CONTINENT.values():
    ALL_NODES.extend(nodes)

# Node details mapping with country organization
NODE_DETAILS = {
    # Europe (EU)
    "bg1.node.check-host.net": {"country": "Bulgaria", "city": "Sofia", "continent": "EU"},
    "ch1.node.check-host.net": {"country": "Switzerland", "city": "Zurich", "continent": "EU"},
    "cz1.node.check-host.net": {"country": "Czechia", "city": "C.Budejovice", "continent": "EU"},
    "de1.node.check-host.net": {"country": "Germany", "city": "Nuremberg", "continent": "EU"},
    "de4.node.check-host.net": {"country": "Germany", "city": "Frankfurt", "continent": "EU"},
    "es1.node.check-host.net": {"country": "Spain", "city": "Barcelona", "continent": "EU"},
    "fi1.node.check-host.net": {"country": "Finland", "city": "Helsinki", "continent": "EU"},
    "fr1.node.check-host.net": {"country": "France", "city": "Roubaix", "continent": "EU"},
    "fr2.node.check-host.net": {"country": "France", "city": "Paris", "continent": "EU"},
    "hu1.node.check-host.net": {"country": "Hungary", "city": "Nyiregyhaza", "continent": "EU"},
    "it2.node.check-host.net": {"country": "Italy", "city": "Milan", "continent": "EU"},
    "lt1.node.check-host.net": {"country": "Lithuania", "city": "Vilnius", "continent": "EU"},
    "md1.node.check-host.net": {"country": "Moldova", "city": "Chisinau", "continent": "EU"},
    "nl1.node.check-host.net": {"country": "Netherlands", "city": "Amsterdam", "continent": "EU"},
    "nl2.node.check-host.net": {"country": "Netherlands", "city": "Meppel", "continent": "EU"},
    "pl1.node.check-host.net": {"country": "Poland", "city": "Poznan", "continent": "EU"},
    "pl2.node.check-host.net": {"country": "Poland", "city": "Warsaw", "continent": "EU"},
    "pt1.node.check-host.net": {"country": "Portugal", "city": "Viana", "continent": "EU"},
    "rs1.node.check-host.net": {"country": "Serbia", "city": "Belgrade", "continent": "EU"},
    "se1.node.check-host.net": {"country": "Sweden", "city": "Tallberg", "continent": "EU"},
    "uk1.node.check-host.net": {"country": "UK", "city": "Coventry", "continent": "EU"},
    
    # Asia (AS)
    "hk1.node.check-host.net": {"country": "Hong Kong", "city": "Hong Kong", "continent": "AS"},
    "il1.node.check-host.net": {"country": "Israel", "city": "Tel Aviv", "continent": "AS"},
    "il2.node.check-host.net": {"country": "Israel", "city": "Netanya", "continent": "AS"},
    "in1.node.check-host.net": {"country": "India", "city": "Mumbai", "continent": "AS"},
    "in2.node.check-host.net": {"country": "India", "city": "Chennai", "continent": "AS"},
    "ir1.node.check-host.net": {"country": "Iran", "city": "Tehran", "continent": "AS"},
    "ir3.node.check-host.net": {"country": "Iran", "city": "Mashhad", "continent": "AS"},
    "ir5.node.check-host.net": {"country": "Iran", "city": "Esfahan", "continent": "AS"},
    "ir6.node.check-host.net": {"country": "Iran", "city": "Karaj", "continent": "AS"},
    "jp1.node.check-host.net": {"country": "Japan", "city": "Tokyo", "continent": "AS"},
    "kz1.node.check-host.net": {"country": "Kazakhstan", "city": "Karaganda", "continent": "AS"},
    "tr1.node.check-host.net": {"country": "Turkey", "city": "Istanbul", "continent": "AS"},
    "tr2.node.check-host.net": {"country": "Turkey", "city": "Gebze", "continent": "AS"},
    "vn1.node.check-host.net": {"country": "Vietnam", "city": "Ho Chi Minh City", "continent": "AS"},
    
    # North America (NA)
    "us1.node.check-host.net": {"country": "USA", "city": "Los Angeles", "continent": "NA"},
    "us2.node.check-host.net": {"country": "USA", "city": "Dallas", "continent": "NA"},
    "us3.node.check-host.net": {"country": "USA", "city": "Atlanta", "continent": "NA"},
    
    # South America (SA)
    "br1.node.check-host.net": {"country": "Brazil", "city": "Sao Paulo", "continent": "SA"},
    
    # Eastern Europe (EU-EAST)
    "ru1.node.check-host.net": {"country": "Russia", "city": "Moscow", "continent": "EU-EAST"},
    "ru2.node.check-host.net": {"country": "Russia", "city": "Moscow", "continent": "EU-EAST"},
    "ru3.node.check-host.net": {"country": "Russia", "city": "Saint Petersburg", "continent": "EU-EAST"},
    "ru4.node.check-host.net": {"country": "Russia", "city": "Ekaterinburg", "continent": "EU-EAST"},
    "ua1.node.check-host.net": {"country": "Ukraine", "city": "Khmelnytskyi", "continent": "EU-EAST"},
    "ua2.node.check-host.net": {"country": "Ukraine", "city": "Kyiv", "continent": "EU-EAST"},
    "ua3.node.check-host.net": {"country": "Ukraine", "city": "SpaceX Starlink", "continent": "EU-EAST"}
}

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

def perform_check(method, target):
    try:
        # Codificar el objetivo para que sea segura en la solicitud
        encoded_target = quote(target, safe='')
        
        # URL de la API de check-host.net según el método
        if method == "ip-info":
            api_url = f"https://check-host.net/ip-info?host={encoded_target}"
        elif method == "ping":
            api_url = f"https://check-host.net/check-ping?host={encoded_target}"
        elif method == "http":
            api_url = f"https://check-host.net/check-http?host={encoded_target}"
        elif method == "tcp":
            api_url = f"https://check-host.net/check-tcp?host={encoded_target}"
        elif method == "udp":
            api_url = f"https://check-host.net/check-udp?host={encoded_target}"
        elif method == "dns":
            api_url = f"https://check-host.net/check-dns?host={encoded_target}"
        else:
            print_color("Método no válido", COLOR_RED)
            return
        
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
                
                print_color(f"\nRealizando {method} en: {target}", COLOR_CYAN)
                print_color("Esperando resultados de los servidores...", COLOR_YELLOW)
                
                # Esperar unos segundos para que los servidores completen las pruebas
                time.sleep(5)
                
                # Hacer una segunda solicitud para obtener los resultados
                result_url = f"https://check-host.net/check-result/{request_id}"
                result_response = requests.get(result_url, headers=headers, timeout=15)
                
                if result_response.status_code == 200:
                    results = result_response.json()
                    
                    if results:
                        print_color(f"\nResultados de {method} para: {target}", COLOR_CYAN)
                        for node in nodes:
                            if node in results and results[node] is not None:
                                node_result = results[node]
                                if isinstance(node_result, list):
                                    node_result = node_result[0]  # Tomar el primer resultado si es una lista
                                
                                country_info = NODE_DETAILS.get(node, {}).get("country", "Unknown")
                                city_info = NODE_DETAILS.get(node, {}).get("city", "Unknown")
                                
                                if method == "ping":
                                    if isinstance(node_result, dict) and "error" in node_result:
                                        print_color(f"[-] ({country_info}, {city_info}): Error - {node_result['error']}", COLOR_RED)
                                    elif isinstance(node_result, list) and len(node_result) > 0:
                                        ping_time = sum(node_result) / len(node_result)
                                        print_color(f"[+] ({country_info}, {city_info}): Ping promedio: {ping_time:.2f} ms", COLOR_GREEN)
                                elif method == "http":
                                    if isinstance(node_result, list) and len(node_result) > 0:
                                        if node_result[0] == 1:
                                            response_time = node_result[1] if len(node_result) > 1 else "N/A"
                                            print_color(f"[+] ({country_info}, {city_info}): Online (Tiempo de respuesta: {response_time:.3f}s)", COLOR_GREEN)
                                        else:
                                            error_msg = node_result[1] if len(node_result) > 1 else "Error desconocido"
                                            print_color(f"[-] ({country_info}, {city_info}): Offline (Error: {error_msg})", COLOR_RED)
                                elif method in ["tcp", "udp"]:
                                    if node_result == 1:
                                        print_color(f"[+] ({country_info}, {city_info}): Puerto accesible", COLOR_GREEN)
                                    elif node_result == 0:
                                        print_color(f"[-] ({country_info}, {city_info}): Puerto inaccesible", COLOR_RED)
                                    else:
                                        print_color(f"[?] ({country_info}, {city_info}): Resultado desconocido", COLOR_YELLOW)
                                elif method == "dns":
                                    if isinstance(node_result, list) and len(node_result) > 0:
                                        print_color(f"[+] ({country_info}, {city_info}): Registros DNS encontrados", COLOR_GREEN)
                                        for record in node_result:
                                            print_color(f"    {record}", COLOR_WHITE)
                                    else:
                                        print_color(f"[-] ({country_info}, {city_info}): No se encontraron registros DNS", COLOR_RED)
                                elif method == "ip-info":
                                    if isinstance(node_result, dict):
                                        print_color(f"[+] ({country_info}, {city_info}): Información encontrada", COLOR_GREEN)
                                        for key, value in node_result.items():
                                            print_color(f"    {key}: {value}", COLOR_WHITE)
                                    else:
                                        print_color(f"[?] ({country_info}, {city_info}): Formato de respuesta inesperado", COLOR_YELLOW)
                            else:
                                country_info = NODE_DETAILS.get(node, {}).get("country", "Unknown")
                                city_info = NODE_DETAILS.get(node, {}).get("city", "Unknown")
                                print_color(f"[?] ({country_info}, {city_info}): No hay datos disponibles", COLOR_YELLOW)
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
    print_color("Herramienta para verificar hosts usando check-host.net", COLOR_BOLD + COLOR_CYAN)
    print_color("Métodos disponibles: ip-info, ping, http, tcp, udp, dns", COLOR_YELLOW)
    print_color("----------------------------------------", COLOR_WHITE)
    
    while True:
        # Solicitar método al usuario
        method = input(f"{COLOR_GREEN}Selecciona el método (ip-info, ping, http, tcp, udp, dns) o 'exit' para terminar: {COLOR_RESET}").strip().lower()
        
        if method == 'exit':
            print_color("¡Hasta luego!", COLOR_CYAN)
            break
            
        if method not in ['ip-info', 'ping', 'http', 'tcp', 'udp', 'dns']:
            print_color("Método no válido. Por favor selecciona uno de los métodos disponibles.", COLOR_RED)
            continue
            
        # Solicitar objetivo al usuario
        target = input(f"{COLOR_GREEN}Ingresa el objetivo (URL, IP o dominio) a verificar: {COLOR_RESET}").strip()
        
        if not target:
            print_color("Debes ingresar un objetivo válido.", COLOR_RED)
            continue
            
        # Realizar la verificación
        perform_check(method, target)
        
        print_color("\n----------------------------------------", COLOR_WHITE)

if __name__ == "__main__":
    main()