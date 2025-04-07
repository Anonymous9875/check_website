#!/usr/bin/env python3

import requests
import json
import time
import sys
import re

def check_nodes():
    try:
        response = requests.get("https://check-host.net/nodes/hosts", headers={"Accept": "application/json"})
        nodes_data = response.json()
        nodes = nodes_data.get("nodes", {})
        
        result = []
        for hostname, info in nodes.items():
            location = info.get("location", [])
            if len(location) >= 3:
                result.append({"hostname": hostname, "location": location[2]})
        return result
    except Exception as e:
        print(f"Error fetching nodes: {e}")
        return None

def perform_check(check_type, host, count=1, node=None):
    try:
        # Build the request URL
        url = f"https://check-host.net/check-{check_type}?host={host}&max_nodes={count}"
        if node:
            url += f"&node={node}"
        
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
        
        return result_data
    except Exception as e:
        print(f"Error performing check: {e}")
        return None

def print_menu():
    print("\nOptions:")
    print("1. Ping test")
    print("2. HTTP test")
    print("3. TCP test")
    print("4. UDP test")
    print("5. DNS resolution test")
    print("6. List available nodes")
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
            count = 1
            node = None
            
            if len(sys.argv) > 4:
                # Check if 4th argument is a count or node
                if sys.argv[4].isdigit():
                    count = int(sys.argv[4])
                    if len(sys.argv) > 5:
                        node = sys.argv[5]
                else:
                    node = sys.argv[4]
            
            result = perform_check(check_type, host, count, node)
            if result:
                print(json.dumps(result, indent=2))
                
        elif sys.argv[1] in ("-n", "--nodes"):
            nodes = check_nodes()
            if nodes:
                for node in nodes:
                    print(f"Hostname: {node['hostname']}")
                    print(f"Location: {node['location']}")
                    print("-" * 40)
        else:
            print("Invalid parameter.\nUse parameters: <-t|--type>, <-n|--nodes>")
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
                count = input("Enter number of nodes (default 1): ")
                node = input("Enter specific node (leave blank for any): ")
                
                count = int(count) if count.isdigit() else 1
                node = node if node else None
                
                result = perform_check("ping", host, count, node)
                if result:
                    print(json.dumps(result, indent=2))
            elif choice == "2":
                host = input("Enter URL to test (include http:// or https://): ")
                count = input("Enter number of nodes (default 1): ")
                node = input("Enter specific node (leave blank for any): ")
                
                count = int(count) if count.isdigit() else 1
                node = node if node else None
                
                result = perform_check("http", host, count, node)
                if result:
                    print(json.dumps(result, indent=2))
            elif choice == "3":
                host = input("Enter host:port (e.g., example.com:443): ")
                count = input("Enter number of nodes (default 1): ")
                node = input("Enter specific node (leave blank for any): ")
                
                count = int(count) if count.isdigit() else 1
                node = node if node else None
                
                result = perform_check("tcp", host, count, node)
                if result:
                    print(json.dumps(result, indent=2))
            elif choice == "4":
                host = input("Enter host:port (e.g., example.com:443): ")
                count = input("Enter number of nodes (default 1): ")
                node = input("Enter specific node (leave blank for any): ")
                
                count = int(count) if count.isdigit() else 1
                node = node if node else None
                
                result = perform_check("udp", host, count, node)
                if result:
                    print(json.dumps(result, indent=2))
            elif choice == "5":
                host = input("Enter domain name to resolve: ")
                count = input("Enter number of nodes (default 1): ")
                node = input("Enter specific node (leave blank for any): ")
                
                count = int(count) if count.isdigit() else 1
                node = node if node else None
                
                result = perform_check("dns", host, count, node)
                if result:
                    print(json.dumps(result, indent=2))
            elif choice == "6":
                nodes = check_nodes()
                if nodes:
                    for node in nodes:
                        print(f"Hostname: {node['hostname']}")
                        print(f"Location: {node['location']}")
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