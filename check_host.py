#!/usr/bin/env python3
"""
Network Diagnostic Tool

A comprehensive network testing utility that performs:
- Ping tests
- HTTP checks
- TCP port checks
- UDP port checks
- DNS resolution tests
Using both local system checks and the Check-Host API for global testing.
"""

import os
import sys
import time
import socket
import subprocess
import requests
import dns.resolver
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
import concurrent.futures
import json
import ipaddress
import colorama
from colorama import Fore, Style, Back

# Initialize colorama
colorama.init(autoreset=True)

# Global configuration
DEFAULT_TIMEOUT = 10  # seconds
MAX_THREADS = 10
PING_COUNT = 4  # Number of pings to send
MAX_RETRIES = 3  # Max retries for API checks
RESULT_WAIT_TIME = 10  # Initial wait time for results
MAX_WAIT_TIME = 30  # Max total wait time for results

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

class CheckHostAPI:
    """Client for the Check-Host API, supporting multiple check types."""
    
    BASE_URL = "https://check-host.net"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NetworkTester/1.0',
            'Accept': 'application/json'
        })
    
    def _get_check_results(self, check_id: str) -> Dict:
        """Wait for and retrieve check results with retries."""
        result_url = f"{self.BASE_URL}/check-result/{check_id}"
        start_time = time.time()
        elapsed = 0
        
        while elapsed < MAX_WAIT_TIME:
            try:
                time.sleep(RESULT_WAIT_TIME)
                response = self.session.get(result_url, timeout=DEFAULT_TIMEOUT)
                response.raise_for_status()
                
                result_data = response.json()
                
                # Check if all nodes have responded
                if all(v is not None for v in result_data.values()):
                    return result_data
                
                elapsed = time.time() - start_time
                
            except requests.exceptions.RequestException as e:
                elapsed = time.time() - start_time
                if elapsed >= MAX_WAIT_TIME:
                    return {'error': f"Timeout waiting for results: {str(e)}"}
                
        return {'error': 'Timeout waiting for all nodes to respond'}
    
    def check_tcp(self, host: str, port: int = 80, nodes: List[str] = None) -> Dict:
        """Perform TCP check from multiple nodes."""
        if nodes is None:
            nodes = list(NODE_DETAILS.keys())
        
        params = {
            'host': f"{host}:{port}",
            'node': ','.join(nodes)
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(
                    f"{self.BASE_URL}/check-tcp",
                    params=params,
                    timeout=DEFAULT_TIMEOUT
                )
                response.raise_for_status()
                
                check_id = response.json().get('request_id')
                if not check_id:
                    if attempt == MAX_RETRIES - 1:
                        return {'error': 'No check ID received after retries'}
                    continue
                
                return self._get_check_results(check_id)
                
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return {'error': f"API request failed after retries: {str(e)}"}
                time.sleep(2)
    
    def check_udp(self, host: str, port: int = 53, nodes: List[str] = None) -> Dict:
        """Perform UDP check from multiple nodes."""
        if nodes is None:
            nodes = list(NODE_DETAILS.keys())
        
        params = {
            'host': f"{host}:{port}",
            'node': ','.join(nodes)
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(
                    f"{self.BASE_URL}/check-udp",
                    params=params,
                    timeout=DEFAULT_TIMEOUT
                )
                response.raise_for_status()
                
                check_id = response.json().get('request_id')
                if not check_id:
                    if attempt == MAX_RETRIES - 1:
                        return {'error': 'No check ID received after retries'}
                    continue
                
                return self._get_check_results(check_id)
                
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return {'error': f"API request failed after retries: {str(e)}"}
                time.sleep(2)
    
    def check_dns(self, domain: str, nodes: List[str] = None) -> Dict:
        """Perform DNS check from multiple nodes."""
        if nodes is None:
            nodes = list(NODE_DETAILS.keys())
        
        params = {
            'host': domain,
            'node': ','.join(nodes)
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(
                    f"{self.BASE_URL}/check-dns",
                    params=params,
                    timeout=DEFAULT_TIMEOUT
                )
                response.raise_for_status()
                
                check_id = response.json().get('request_id')
                if not check_id:
                    if attempt == MAX_RETRIES - 1:
                        return {'error': 'No check ID received after retries'}
                    continue
                
                return self._get_check_results(check_id)
                
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return {'error': f"API request failed after retries: {str(e)}"}
                time.sleep(2)

class NetworkTester:
    def __init__(self):
        self.timeout = DEFAULT_TIMEOUT
        self.max_threads = MAX_THREADS
        self.check_host_api = CheckHostAPI()

    def tcp_check(self, host: str, port: int = 80) -> Dict[str, Dict]:
        """
        Perform a global TCP check to the specified host and port using all Check-Host nodes.
        
        Args:
            host: Hostname or IP address
            port: Port number to check (default: 80)
            
        Returns:
            Dictionary with TCP results from all nodes
        """
        api_result = self.check_host_api.check_tcp(host, port)
        
        if 'error' in api_result:
            return {'error': api_result['error']}
        
        results = {}
        for node, node_result in api_result.items():
            if node in NODE_DETAILS:
                region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                
                if node_result and isinstance(node_result, list) and len(node_result) > 0:
                    tcp_result = node_result[0]
                    if isinstance(tcp_result, list) and len(tcp_result) >= 2:
                        success = tcp_result[0] == 1
                        connect_time = float(tcp_result[1]) * 1000  # Convert to ms
                        ip = tcp_result[2] if len(tcp_result) > 2 else None
                        
                        results[region] = {
                            'success': success,
                            'connect_time': connect_time,
                            'ip': ip,
                            'port': port
                        }
                    else:
                        results[region] = {
                            'success': False,
                            'connect_time': 0.0,
                            'ip': None,
                            'port': port,
                            'error': 'Invalid TCP response format'
                        }
                else:
                    results[region] = {
                        'success': False,
                        'connect_time': 0.0,
                        'ip': None,
                        'port': port,
                        'error': 'No TCP data received'
                    }
        
        return results

    def udp_check(self, host: str, port: int = 53) -> Dict[str, Dict]:
        """
        Perform a UDP check to the specified host and port from multiple locations.
        
        Args:
            host: Hostname or IP address
            port: Port number to check (default: 53)
            
        Returns:
            Dictionary with UDP results from multiple locations
        """
        api_result = self.check_host_api.check_udp(host, port)
        
        if 'error' in api_result:
            return {'error': api_result['error']}
        
        results = {}
        for node, node_result in api_result.items():
            if node in NODE_DETAILS:
                region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                
                if node_result and isinstance(node_result, list) and len(node_result) > 0:
                    udp_result = node_result[0]
                    if isinstance(udp_result, list) and len(udp_result) >= 2:
                        success = udp_result[0] == 1
                        response_time = float(udp_result[1]) * 1000  # Convert to ms
                        ip = udp_result[2] if len(udp_result) > 2 else None
                        
                        results[region] = {
                            'success': success,
                            'response_time': response_time,
                            'ip': ip,
                            'port': port
                        }
                    else:
                        results[region] = {
                            'success': False,
                            'response_time': 0.0,
                            'ip': None,
                            'port': port,
                            'error': 'Invalid UDP response format'
                        }
                else:
                    results[region] = {
                        'success': False,
                        'response_time': 0.0,
                        'ip': None,
                        'port': port,
                        'error': 'No UDP data received'
                    }
        
        return results

    def dns_check(self, domain: str, dns_server: str = None) -> Dict[str, Dict]:
        """
        Perform a DNS resolution check for the specified domain from multiple locations.
        
        Args:
            domain: Domain name to resolve
            dns_server: DNS server to use (if None, will use Check-Host nodes)
            
        Returns:
            Dictionary with DNS results from multiple locations
        """
        if dns_server:
            return self._single_dns_check(domain, dns_server)
        else:
            api_result = self.check_host_api.check_dns(domain)
            
            if 'error' in api_result:
                return {'error': api_result['error']}
            
            results = {}
            for node, node_result in api_result.items():
                if node in NODE_DETAILS:
                    region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                    
                    if node_result and isinstance(node_result, list) and len(node_result) > 0:
                        dns_result = node_result[0]
                        if isinstance(dns_result, list) and len(dns_result) >= 2:
                            success = dns_result[0] == 1
                            resolution_time = float(dns_result[1]) * 1000  # Convert to ms
                            addresses = dns_result[2] if len(dns_result) > 2 else []
                            
                            results[region] = {
                                'success': success,
                                'resolution_time': resolution_time,
                                'addresses': addresses,
                                'error': None
                            }
                        else:
                            results[region] = {
                                'success': False,
                                'resolution_time': 0.0,
                                'addresses': [],
                                'error': 'Invalid DNS response format'
                            }
                    else:
                        results[region] = {
                            'success': False,
                            'resolution_time': 0.0,
                            'addresses': [],
                            'error': 'No DNS data received'
                        }
            
            return results

    def _single_dns_check(self, domain: str, dns_server: str) -> Dict[str, Union[bool, float, str, list]]:
        """Perform a single DNS resolution check."""
        result = {
            'success': False,
            'resolution_time': 0.0,
            'addresses': [],
            'error': None
        }

        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [socket.gethostbyname(dns_server)]
            resolver.timeout = self.timeout
            resolver.lifetime = self.timeout

            start_time = time.time()
            answers = resolver.resolve(domain, 'A')
            end_time = time.time()

            result['resolution_time'] = (end_time - start_time) * 1000  # Convert to ms
            result['addresses'] = [str(r) for r in answers]
            result['success'] = True

        except dns.resolver.NXDOMAIN:
            result['error'] = "Domain does not exist"
        except dns.resolver.Timeout:
            result['error'] = "DNS resolution timed out"
        except dns.resolver.NoNameservers:
            result['error'] = "No nameservers available"
        except Exception as e:
            result['error'] = f"DNS error: {str(e)}"

        return {f"DNS Server ({dns_server})": result}

def display_tcp_results(results: Dict) -> None:
    """Display TCP results in a formatted way."""
    print(f"\n{Fore.CYAN}TCP RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Port':<8} {'Connect Time':<15} {'IP':<15}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in results:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            port = "N/A"
            time_ms = results['error']
            ip = "N/A"
        else:
            status = f"{Fore.GREEN}OPEN{Style.RESET_ALL}" if data['success'] else f"{Fore.RED}CLOSED{Style.RESET_ALL}"
            port = str(data.get('port', 'N/A'))
            time_ms = f"{data.get('connect_time', 0):.1f} ms" if data['success'] else "N/A"
            ip = data.get('ip', 'N/A') if data['success'] else "N/A"
        
        print(f"{location:<30} {status:<10} {port:<8} {time_ms:<15} {ip:<15}")

def display_udp_results(results: Dict) -> None:
    """Display UDP results in a formatted way."""
    print(f"\n{Fore.CYAN}UDP RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Port':<8} {'Response Time':<15} {'IP':<15}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in results:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            port = "N/A"
            time_ms = results['error']
            ip = "N/A"
        else:
            status = f"{Fore.GREEN}UP{Style.RESET_ALL}" if data['success'] else f"{Fore.RED}DOWN{Style.RESET_ALL}"
            port = str(data.get('port', 'N/A'))
            time_ms = f"{data.get('response_time', 0):.1f} ms" if data['success'] else "N/A"
            ip = data.get('ip', 'N/A') if data['success'] else "N/A"
        
        print(f"{location:<30} {status:<10} {port:<8} {time_ms:<15} {ip:<15}")

def display_dns_results(results: Dict) -> None:
    """Display DNS results in a formatted way."""
    print(f"\n{Fore.CYAN}DNS RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Resolution Time':<20} {'Addresses':<30}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in results:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            time_ms = "N/A"
            addresses = results['error']
        else:
            status = f"{Fore.GREEN}OK{Style.RESET_ALL}" if data['success'] else f"{Fore.RED}FAIL{Style.RESET_ALL}"
            time_ms = f"{data.get('resolution_time', 0):.1f} ms" if data['success'] else "N/A"
            addresses = ", ".join(data.get('addresses', []))[:30] if data['success'] else data.get('error', 'N/A')
        
        print(f"{location:<30} {status:<10} {time_ms:<20} {addresses:<30}")

def interactive_mode():
    """Run in interactive mode."""
    tester = NetworkTester()
    
    print(f"{Fore.CYAN}=== Network Diagnostic Tool ==={Style.RESET_ALL}")
    
    while True:
        print("\nOptions:")
        print("1. TCP port test")
        print("2. UDP port test")
        print("3. DNS resolution test")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '0':
            break
        
        if choice == '1':
            host = input("Enter host: ")
            port = int(input("Enter port (default 80): ") or 80)
            results = tester.tcp_check(host, port)
            display_tcp_results(results)
                
        elif choice == '2':
            host = input("Enter host: ")
            port = int(input("Enter port (default 53): ") or 53)
            results = tester.udp_check(host, port)
            display_udp_results(results)
                
        elif choice == '3':
            domain = input("Enter domain to resolve: ")
            dns_server = input("Enter DNS server (leave empty for global check): ") or None
            results = tester.dns_check(domain, dns_server)
            display_dns_results(results)
                
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        
        save = input("\nSave results to file? (y/n): ").lower()
        if save == 'y':
            filename = input("Enter filename: ")
            format = input("Format (json/text): ").lower() or 'json'
            save_results(results, filename, format)

def save_results(results: Dict, filename: str, format: str = 'json') -> None:
    """Save results to a file in the specified format."""
    try:
        with open(filename, 'w') as f:
            if format == 'json':
                json.dump(results, f, indent=2)
            else:  # text
                for region, data in results.items():
                    f.write(f"Location: {region}\n")
                    for key, value in data.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
        
        print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving results: {e}{Style.RESET_ALL}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Network Diagnostic Tool')
    subparsers = parser.add_subparsers(dest='command', required=False)

    # TCP command
    tcp_parser = subparsers.add_parser('tcp', help='Perform TCP test')
    tcp_parser.add_argument('host', help='Host to test')
    tcp_parser.add_argument('-p', '--port', type=int, default=80, help='Port to test')
    tcp_parser.add_argument('-o', '--output', help='Output file to save results')
    tcp_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    # UDP command
    udp_parser = subparsers.add_parser('udp', help='Perform UDP test')
    udp_parser.add_argument('host', help='Host to test')
    udp_parser.add_argument('-p', '--port', type=int, default=53, help='Port to test')
    udp_parser.add_argument('-o', '--output', help='Output file to save results')
    udp_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    # DNS command
    dns_parser = subparsers.add_parser('dns', help='Perform DNS resolution test')
    dns_parser.add_argument('domain', help='Domain to resolve')
    dns_parser.add_argument('-s', '--server', 
                           help='DNS server to use (leave empty for global check)')
    dns_parser.add_argument('-o', '--output', help='Output file to save results')
    dns_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    args = parser.parse_args()

    tester = NetworkTester()

    if not args.command:
        interactive_mode()
        return

    try:
        if args.command == 'tcp':
            results = tester.tcp_check(args.host, args.port)
            display_tcp_results(results)
                
        elif args.command == 'udp':
            results = tester.udp_check(args.host, args.port)
            display_udp_results(results)
                
        elif args.command == 'dns':
            results = tester.dns_check(args.domain, args.server)
            display_dns_results(results)
        
        if hasattr(args, 'output') and args.output:
            save_results(results, args.output, args.format)
            
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)