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

# Configuración de colores (la misma que tenías)

def perform_check(method, target):
    try:
        encoded_target = quote(target, safe='')
        
        # URL base actualizada
        base_url = "https://check-host.net"
        
        # Endpoints actualizados según la documentación reciente
        endpoints = {
            "ip-lookup": "/ip-info",
            "whois": "/check-whois",
            "ping": "/check-ping",
            "http": "/check-http",
            "tcp": "/check-tcp",
            "udp": "/check-udp",
            "dns": "/check-dns"
        }
        
        if method not in endpoints:
            print_color("Método no válido", COLOR_RED)
            return None
            
        # Construir URL con parámetros correctos
        api_url = f"{base_url}{endpoints[method]}?host={encoded_target}"
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # 1. Hacer la solicitud inicial
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print_color(f"Error en la solicitud inicial: Código {response.status_code}", COLOR_RED)
            print_color(f"URL intentada: {api_url}", COLOR_YELLOW)
            return None
            
        data = response.json()
        
        if "request_id" not in data:
            print_color("La respuesta no contiene request_id", COLOR_RED)
            print_color("Respuesta completa del servidor:", COLOR_YELLOW)
            print(data)
            return None
            
        request_id = data["request_id"]
        nodes = list(data["nodes"].keys()) if isinstance(data["nodes"], dict) else data["nodes"]
        
        print_color(f"\nRealizando {method} en: {target}", COLOR_CYAN)
        print_color(f"Request ID: {request_id}", COLOR_WHITE)
        print_color("Esperando resultados... (esto puede tomar hasta 30 segundos)", COLOR_YELLOW)
        
        # 2. Esperar y obtener resultados
        max_attempts = 6
        attempt = 0
        results = None
        
        while attempt < max_attempts:
            time.sleep(5)  # Esperar 5 segundos entre intentos
            attempt += 1
            
            result_url = f"{base_url}/check-result/{request_id}"
            result_response = requests.get(result_url, headers=headers, timeout=15)
            
            if result_response.status_code == 200:
                results = result_response.json()
                if results and any(results.values()):  # Verificar que hay datos reales
                    break
            elif result_response.status_code == 404:
                print_color(f"Intento {attempt}: Resultados no disponibles aún...", COLOR_YELLOW)
                continue
            else:
                print_color(f"Error al obtener resultados: Código {result_response.status_code}", COLOR_RED)
                return None
                
        if not results:
            print_color("No se pudieron obtener resultados después de varios intentos", COLOR_RED)
            return None
            
        # 3. Procesar resultados
        print_color(f"\nResultados de {method} para: {target}", COLOR_CYAN)
        
        for node in nodes:
            if node in results and results[node] is not None:
                node_result = results[node]
                if isinstance(node_result, list) and len(node_result) > 0:
                    node_result = node_result[0]  # Tomar primer resultado si es lista
                
                country_info = NODE_DETAILS.get(node, {}).get("country", "Unknown")
                city_info = NODE_DETAILS.get(node, {}).get("city", "Unknown")
                
                # ... (mantén tu lógica de procesamiento de resultados según el método)
                
            else:
                country_info = NODE_DETAILS.get(node, {}).get("country", "Unknown")
                city_info = NODE_DETAILS.get(node, {}).get("city", "Unknown")
                print_color(f"[?] ({country_info}, {city_info}): Sin respuesta del nodo", COLOR_YELLOW)
                
        return results
        
    except requests.exceptions.RequestException as e:
        print_color(f"Error de conexión: {str(e)}", COLOR_RED)
        return None
    except json.JSONDecodeError:
        print_color("Error al procesar la respuesta JSON", COLOR_RED)
        return None

# ... (mantén el resto de tus funciones como main(), clear_screen(), etc.)

if __name__ == "__main__":
    main()