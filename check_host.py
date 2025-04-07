#!/usr/bin/env python3
import requests
import json
import time
from typing import List, Dict, Optional, Union

class CheckHost:
    def __init__(self):
        self.headers = {
            "Accept": "application/json"
        }
        self.base_url = "https://check-host.net"
    
    def get_nodes(self) -> List[Dict]:
        """Obtiene la lista de nodos disponibles"""
        url = f"{self.base_url}/nodes/hosts"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            nodes_data = response.json()
            
            nodes_list = []
            for node_name, node_info in nodes_data['nodes'].items():
                nodes_list.append({
                    "server": node_name,
                    "address": node_info['ip'],
                    "location": node_info['location'][2] if len(node_info['location']) > 2 else ""
                })
            return nodes_list
        except Exception as e:
            print(f"Error getting nodes: {e}")
            return []
    
    def check_host(self, server: str, check_type: str, count: int = 5, node: Optional[str] = None) -> List[Dict]:
        """Realiza una comprobación en el host especificado"""
        nodes_list = self.get_nodes()
        if not nodes_list:
            print("No se pudo obtener la lista de nodos")
            return []
        
        url = f"{self.base_url}/check-{check_type}?host={server}&max_nodes={count}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            request_data = response.json()
            
            request_id = request_data['request_id']
            nodes = list(request_data['nodes'].keys())
            
            # Esperar a que los resultados estén listos
            url_result = f"{self.base_url}/check-result/{request_id}"
            while True:
                time.sleep(2)  # Esperar 2 segundos entre comprobaciones
                response = requests.get(url_result, headers=self.headers)
                response.raise_for_status()
                check_data = response.json()
                
                ready = all(check_data.get(node) is not None for node in nodes)
                if ready:
                    break
            
            # Procesar resultados según el tipo de comprobación
            results = []
            for node_name in nodes:
                node_result = check_data.get(node_name, {})
                node_info = next((n for n in nodes_list if n['server'] == node_name), {})
                
                if check_type == "ping":
                    for ping_result in node_result[0]:
                        results.append({
                            "server": node_name,
                            "location": node_info.get('location', ''),
                            "status": ping_result[0],
                            "time": ping_result[1]
                        })
                
                elif check_type == "http":
                    status = 'True' if node_result[0][0] == "1" else 'False'
                    results.append({
                        "server": node_name,
                        "location": node_info.get('location', ''),
                        "status": status,
                        "time": node_result[0][1]
                    })
                
                elif check_type == "dns":
                    results.append({
                        "server": node_name,
                        "location": node_info.get('location', ''),
                        "a_record": node_result.get('A', ''),
                        "ttl": node_result.get('TTL', '')
                    })
                
                elif check_type == "tcp":
                    if 'error' in node_result:
                        results.append({
                            "server": node_name,
                            "location": node_info.get('location', ''),
                            "status": node_result['error']
                        })
                    else:
                        results.append({
                            "server": node_name,
                            "location": node_info.get('location', ''),
                            "status": node_result.get('time', '')
                        })
                
                elif check_type == "udp":
                    results.append({
                        "server": node_name,
                        "location": node_info.get('location', ''),
                        "timeout": node_result.get('timeout', '')
                    })
            
            return results
        
        except Exception as e:
            print(f"Error checking host: {e}")
            return []

def print_results(results: List[Dict], check_type: str):
    """Muestra los resultados formateados"""
    if not results:
        print("No se obtuvieron resultados")
        return
    
    print("\nResultados:")
    if check_type == "ping":
        print(f"{'Servidor':<20} {'Ubicación':<25} {'Estado':<10} {'Tiempo (ms)':<10}")
        print("-" * 70)
        for r in results:
            print(f"{r['server']:<20} {r['location']:<25} {str(r['status']):<10} {str(r['time']):<10}")
    
    elif check_type == "http":
        print(f"{'Servidor':<20} {'Ubicación':<25} {'Estado':<10} {'Tiempo (ms)':<10}")
        print("-" * 70)
        for r in results:
            print(f"{r['server']:<20} {r['location']:<25} {r['status']:<10} {str(r['time']):<10}")
    
    elif check_type == "dns":
        print(f"{'Servidor':<20} {'Ubicación':<25} {'Registro A':<30} {'TTL':<10}")
        print("-" * 90)
        for r in results:
            a_records = r['a_record'] if isinstance(r['a_record'], list) else [r['a_record']]
            for a in a_records:
                print(f"{r['server']:<20} {r['location']:<25} {str(a):<30} {str(r['ttl']):<10}")
    
    elif check_type == "tcp":
        print(f"{'Servidor':<20} {'Ubicación':<25} {'Estado/Tiempo':<30}")
        print("-" * 70)
        for r in results:
            print(f"{r['server']:<20} {r['location']:<25} {str(r['status']):<30}")
    
    elif check_type == "udp":
        print(f"{'Servidor':<20} {'Ubicación':<25} {'Timeout':<10}")
        print("-" * 70)
        for r in results:
            print(f"{r['server']:<20} {r['location']:<25} {str(r['timeout']):<10}")

def main():
    checker = CheckHost()
    
    while True:
        print("\nOptions:")
        print("1. Ping test")
        print("2. HTTP test")
        print("3. TCP test")
        print("4. UDP test")
        print("5. DNS resolution test")
        print("6. List available nodes")
        print("0. Exit")
        
        try:
            choice = input("Select an option (0-6): ")
            
            if choice == "0":
                print("Saliendo...")
                break
            
            elif choice == "6":
                nodes = checker.get_nodes()
                print("\nAvailable nodes:")
                print(f"{'Server':<20} {'IP Address':<15} {'Location':<25}")
                print("-" * 60)
                for node in nodes:
                    print(f"{node['server']:<20} {node['address']:<15} {node['location']:<25}")
                continue
            
            elif choice in ("1", "2", "3", "4", "5"):
                server = input("Enter server/host to check (e.g., google.com or google.com:443): ").strip()
                if not server:
                    print("Server is required")
                    continue
                
                check_type = {
                    "1": "ping",
                    "2": "http",
                    "3": "tcp",
                    "4": "udp",
                    "5": "dns"
                }[choice]
                
                try:
                    count = int(input(f"Number of nodes to use (1-40, default 5): ") or "5")
                    if count < 1 or count > 40:
                        print("Number of nodes must be between 1 and 40")
                        continue
                except ValueError:
                    print("Invalid number, using default (5)")
                    count = 5
                
                results = checker.check_host(server, check_type, count)
                print_results(results, check_type)
            
            else:
                print("Invalid option, please try again")
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()