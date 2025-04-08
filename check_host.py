#!/usr/bin/env python3

import requests
import json
import time
import argparse
from collections import defaultdict

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

def get_nodes():
    """Get and display all available nodes organized by country and continent"""
    # Group nodes by country first
    nodes_by_country = defaultdict(list)
    for node, details in NODE_DETAILS.items():
        country = details["country"]
        nodes_by_country[country].append({
            "hostname": node,
            "city": details["city"],
            "continent": details["continent"]
        })
    
    # Sort countries alphabetically
    sorted_countries = sorted(nodes_by_country.items(), key=lambda x: x[0])
    
    # Print nodes organized by continent and country
    for continent in sorted(NODES_BY_CONTINENT.keys()):
        print(f"\n=== {continent} ===")
        continent_nodes = []
        
        # Get all countries in this continent
        continent_countries = []
        for country, nodes in sorted_countries:
            if nodes[0]["continent"] == continent:
                continent_countries.append((country, nodes))
        
        # Sort countries in continent alphabetically
        continent_countries.sort(key=lambda x: x[0])
        
        for country, nodes in continent_countries:
            print(f"\n{country}:")
            for node in sorted(nodes, key=lambda x: x["hostname"]):
                print(f"  {node['hostname']} ({node['city']})")

def perform_check(check_type, host, count=1, node=None):
    """Perform network check using check-host.net API"""
    if not host:
        print("Invalid hostname.")
        return
    
    try:
        count = int(count)
    except ValueError:
        count = 1
    
    url = f"https://check-host.net/check-{check_type}?host={host}&max_nodes={count}"
    if node:
        url += f"&node={node}"
    
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        request_id = data["request_id"]
        
        # Wait for results
        result_url = f"https://check-host.net/check-result/{request_id}"
        while True:
            result_response = requests.get(result_url, headers=headers)
            result_response.raise_for_status()
            result = result_response.json()
            
            if not any(v is None for v in result.values()):
                break
            
            time.sleep(0.1)
        
        # Format and print results
        formatted_result = json.dumps(result, indent=2)
        print(formatted_result)
        
    except requests.exceptions.RequestException as e:
        print(f"Error performing check: {e}")

def main():
    parser = argparse.ArgumentParser(description="Network checking tool using check-host.net API")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Nodes command
    nodes_parser = subparsers.add_parser('nodes', aliases=['n'], help='List all available nodes')
    
    # Check command
    check_parser = subparsers.add_parser('check', aliases=['t'], help='Perform network check')
    check_parser.add_argument('type', choices=['ping', 'dns', 'http', 'tcp', 'udp'], 
                            help='Type of check to perform')
    check_parser.add_argument('host', help='Host to check')
    check_parser.add_argument('count', nargs='?', default=1, 
                            help='Number of nodes to use (default: 1)')
    check_parser.add_argument('node', nargs='?', 
                            help='Specific node to use for the check')
    
    args = parser.parse_args()
    
    if args.command in ('nodes', 'n'):
        get_nodes()
    elif args.command in ('check', 't'):
        perform_check(args.type, args.host, args.count, args.node)

if __name__ == "__main__":
    main()