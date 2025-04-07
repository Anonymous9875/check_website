#!/usr/bin/env python3

import requests
import json
import time
import sys
import re

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

# Node details mapping
NODE_DETAILS = {
    "bg1.node.check-host.net": {"country": "Bulgaria", "city": "Sofia", "continent": "EU"},
    "br1.node.check-host.net": {"country": "Brazil", "city": "Sao Paulo", "continent": "SA"},
    "ch1.node.check-host.net": {"country": "Switzerland", "city": "Zurich", "continent": "EU"},
    "cz1.node.check-host.net": {"country": "Czechia", "city": "C.Budejovice", "continent": "EU"},
    "de1.node.check-host.net": {"country": "Germany", "city": "Nuremberg", "continent": "EU"},
    "de4.node.check-host.net": {"country": "Germany", "city": "Frankfurt", "continent": "EU"},
    "es1.node.check-host.net": {"country": "Spain", "city": "Barcelona", "continent": "EU"},
    "fi1.node.check-host.net": {"country": "Finland", "city": "Helsinki", "continent": "EU"},
    "fr1.node.check-host.net": {"country": "France", "city": "Roubaix", "continent": "EU"},
    "fr2.node.check-host.net": {"country": "France", "city": "Paris", "continent": "EU"},
    "hk1.node.check-host.net": {"country": "Hong Kong", "city": "Hong Kong", "continent": "AS"},
    "hu1.node.check-host.net": {"country": "Hungary", "city": "Nyiregyhaza", "continent": "EU"},
    "il1.node.check-host.net": {"country": "Israel", "city": "Tel Aviv", "continent": "AS"},
    "il2.node.check-host.net": {"country": "Israel", "city": "Netanya", "continent": "AS"},
    "in1.node.check-host.net": {"country": "India", "city": "Mumbai", "continent": "AS"},
    "in2.node.check-host.net": {"country": "India", "city": "Chennai", "continent": "AS"},
    "ir1.node.check-host.net": {"country": "Iran", "city": "Tehran", "continent": "AS"},
    "ir3.node.check-host.net": {"country": "Iran", "city": "Mashhad", "continent": "AS"},
    "ir5.node.check-host.net": {"country": "Iran", "city": "Esfahan", "continent": "AS"},
    "ir6.node.check-host.net": {"country": "Iran", "city": "Karaj", "continent": "AS"},
    "it2.node.check-host.net": {"country": "Italy", "city": "Milan", "continent": "EU"},
    "jp1.node.check-host.net": {"country": "Japan", "city": "Tokyo", "continent": "AS"},
    "kz1.node.check-host.net": {"country": "Kazakhstan", "city": "Karaganda", "continent": "AS"},
    "lt1.node.check-host.net": {"country": "Lithuania", "city": "Vilnius", "continent": "EU"},
    "md1.node.check-host.net": {"country": "Moldova", "city": "Chisinau", "continent": "EU"},
    "nl1.node.check-host.net": {"country": "Netherlands", "city": "Amsterdam", "continent": "EU"},
    "nl2.node.check-host.net": {"country": "Netherlands", "city": "Meppel", "continent": "EU"},
    "pl1.node.check-host.net": {"country": "Poland", "city": "Poznan", "continent": "EU"},
    "pl2.node.check-host.net": {"country": "Poland", "city": "Warsaw", "continent": "EU"},
    "pt1.node.check-host.net": {"country": "Portugal", "city": "Viana", "continent": "EU"},
    "rs1.node.check-host.net": {"country": "Serbia", "city": "Belgrade", "continent": "EU"},
    "ru1.node.check-host.net": {"country": "Russia", "city": "Moscow", "continent": "EU-EAST"},
    "ru2.node.check-host.net": {"country": "Russia", "city": "Moscow", "continent": "EU-EAST"},
    "ru3.node.check-host.net": {"country": "Russia", "city": "Saint Petersburg", "continent": "EU-EAST"},
    "ru4.node.check-host.net": {"country": "Russia", "city": "Ekaterinburg", "continent": "EU-EAST"},
    "se1.node.check-host.net": {"country": "Sweden", "city": "Tallberg", "continent": "EU"},
    "tr1.node.check-host.net": {"country": "Turkey", "city": "Istanbul", "continent": "AS"},
    "tr2.node.check-host.net": {"country": "Turkey", "city": "Gebze", "continent": "AS"},
    "ua1.node.check-host.net": {"country": "Ukraine", "city": "Khmelnytskyi", "continent": "EU-EAST"},
    "ua2.node.check-host.net": {"country": "Ukraine", "city": "Kyiv", "continent": "EU-EAST"},
    "ua3.node.check-host.net": {"country": "Ukraine", "city": "SpaceX Starlink", "continent": "EU-EAST"},
    "uk1.node.check-host.net": {"country": "UK", "city": "Coventry", "continent": "EU"},
    "us1.node.check-host.net": {"country": "USA", "city": "Los Angeles", "continent": "NA"},
    "us2.node.check-host.net": {"country": "USA", "city": "Dallas", "continent": "NA"},
    "us3.node.check-host.net": {"country": "USA", "city": "Atlanta", "continent": "NA"},
    "vn1.node.check-host.net": {"country": "Vietnam", "city": "Ho Chi Minh City", "continent": "AS"}
}

def get_all_nodes():
    """Return all available nodes from our predefined list"""
    return [node for continent in NODES_BY_CONTINENT.values() for node in continent]

def perform_check(check_type, host):
    try:
        # Get all available nodes
        all_nodes = get_all_nodes()
        
        # Build the request URL with all nodes
        url = f"https://check-host.net/check-{check_type}?host={host}"
        
        # Make the initial request
        response = requests.get(url, headers={"Accept": "application/json"})
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
            
        data = response.json()
        request_id = data.get("request_id")
        if not request_id:
            print("Error: No request_id received")
            return None
        
        # Poll for results
        result_url = f"https://check-host.net/check-result/{request_id}"
        while True:
            result_response = requests.get(result_url, headers={"Accept": "application/json"})
            if result_response.status_code != 200:
                print(f"Error: Received status code {result_response.status_code} while polling results")
                return None
                
            result_data = result_response.json()
            if all(value is not None for value in result_data.values()):
                break
            time.sleep(0.1)
        
        # Process and format the results
        formatted_results = {}
        for node, node_result in result_data.items():
            if node in NODE_DETAILS:
                node_info = NODE_DETAILS[node]
                location = f"{node_info['country']}, {node_info['city']}"
                
                if isinstance(node_result, list):
                    node_result = node_result[0] if node_result else {}
                
                if node_result.get('success'):
                    status = "OK"
                    latency = f"{node_result.get('min_latency', 0):.1f}/{node_result.get('avg_latency', 0):.1f}/{node_result.get('max_latency', 0):.1f} ms"
                    ip = node_result.get('ip', 'N/A')
                else:
                    status = "DOWN"
                    latency = "N/A"
                    ip = "N/A"
                
                formatted_results[node] = {
                    "location": location,
                    "status": status,
                    "latency": latency,
                    "ip": ip
                }
        
        return formatted_results
        
    except Exception as e:
        print(f"Error performing check: {e}")
        return None

def print_menu():
    print("\nOptions:\n")
    print("1. Ping test")
    print("2. HTTP test")
    print("3. TCP test")
    print("4. UDP test")
    print("5. DNS test")
    print("0. Exit")

def main():
    if len(sys.argv) > 1:
        # Command-line mode
        if sys.argv[1] in ("-t", "--type"):
            if len(sys.argv) < 3:
                print("Invalid type.\nUse type: ping, dns, http, tcp, udp")
                return
                
            check_type = sys.argv[2]
            if check_type not in ("ping", "dns", "http", "tcp", "udp"):
                print("Invalid type.\nUse type: ping, dns, http, tcp, udp")
                return
                
            if len(sys.argv) < 4:
                print("Invalid hostname.")
                return
                
            host = sys.argv[3]
            
            result = perform_check(check_type, host)
            if result:
                print("\nTest Results:")
                for node, info in result.items():
                    print(f"\nNode: {node}")
                    print(f"Location: {info['location']}")
                    print(f"Status: {info['status']}")
                    print(f"Latency: {info['latency']}")
                    print(f"IP: {info['ip']}")
                    print("-" * 40)
                
        else:
            print("Invalid parameter.\nUse parameters: <-t|--type>")
    else:
        # Interactive menu mode
        while True:
            print_menu()
            choice = input("Enter your choice: ")
            
            if choice == "0":
                print("Exiting...")
                break
            elif choice == "1":
                host = input("Enter host to ping: ")
                result = perform_check("ping", host)
                if result:
                    print("\nPing Test Results:")
                    for node, info in result.items():
                        print(f"\nNode: {node}")
                        print(f"Location: {info['location']}")
                        print(f"Status: {info['status']}")
                        print(f"Latency: {info['latency']}")
                        print(f"IP: {info['ip']}")
                        print("-" * 40)
            elif choice == "2":
                host = input("Enter URL to test (include http:// or https://): ")
                result = perform_check("http", host)
                if result:
                    print("\nHTTP Test Results:")
                    for node, info in result.items():
                        print(f"\nNode: {node}")
                        print(f"Location: {info['location']}")
                        print(f"Status: {info['status']}")
                        print(f"Latency: {info['latency']}")
                        print(f"IP: {info['ip']}")
                        print("-" * 40)
            elif choice == "3":
                host = input("Enter host:port (e.g., example.com:443): ")
                result = perform_check("tcp", host)
                if result:
                    print("\nTCP Test Results:")
                    for node, info in result.items():
                        print(f"\nNode: {node}")
                        print(f"Location: {info['location']}")
                        print(f"Status: {info['status']}")
                        print(f"Latency: {info['latency']}")
                        print(f"IP: {info['ip']}")
                        print("-" * 40)
            elif choice == "4":
                host = input("Enter host:port (e.g., example.com:443): ")
                result = perform_check("udp", host)
                if result:
                    print("\nUDP Test Results:")
                    for node, info in result.items():
                        print(f"\nNode: {node}")
                        print(f"Location: {info['location']}")
                        print(f"Status: {info['status']}")
                        print(f"Latency: {info['latency']}")
                        print(f"IP: {info['ip']}")
                        print("-" * 40)
            elif choice == "5":
                host = input("Enter domain name to resolve: ")
                result = perform_check("dns", host)
                if result:
                    print("\nDNS Test Results:")
                    for node, info in result.items():
                        print(f"\nNode: {node}")
                        print(f"Location: {info['location']}")
                        print(f"Status: {info['status']}")
                        print(f"IP: {info['ip']}")
                        print("-" * 40)
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Check if required packages are installed
    try:
        import requests
        import json
    except ImportError:
        print("Error: Required packages not found. Please install them with:")
        print("pip install requests")
        sys.exit(1)
    
    main()