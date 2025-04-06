#!/usr/bin/env python3
"""
Network Diagnostic Tool

A comprehensive network testing tool that performs:
- Ping tests
- HTTP/HTTPS availability and speed tests
- TCP port checks
- UDP checks
- DNS resolution tests

Uses Check-Host.net nodes for global testing.
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
DEFAULT_TIMEOUT = 5  # seconds
MAX_THREADS = 10
PING_COUNT = 4  # Number of pings to send

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
    """Client for the Check-Host API, focused on ping and HTTP checks."""
    
    BASE_URL = "https://check-host.net"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NetworkTester/1.0',
            'Accept': 'application/json'
        })
    
    def check_ping(self, host: str, nodes: List[str] = None) -> Dict:
        """Perform ping check from multiple nodes."""
        if nodes is None:
            nodes = list(NODE_DETAILS.keys())
        
        params = {
            'host': host,
            'node': nodes
        }
        
        try:
            # Request new check
            response = self.session.get(
                f"{self.BASE_URL}/check-ping",
                params=params,
                timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            
            # Get check ID and wait for results
            check_id = response.json().get('request_id')
            if not check_id:
                return {'error': 'No check ID received'}
            
            # Wait and get results
            time.sleep(5)  # Wait for nodes to respond
            result_url = f"{self.BASE_URL}/check-result/{check_id}"
            result_response = self.session.get(result_url, timeout=DEFAULT_TIMEOUT)
            result_response.raise_for_status()
            
            return result_response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def check_http(self, url: str, nodes: List[str] = None) -> Dict:
        """Perform HTTP check from multiple nodes."""
        if nodes is None:
            nodes = list(NODE_DETAILS.keys())
        
        params = {
            'host': url,
            'node': nodes
        }
        
        try:
            # Request new check
            response = self.session.get(
                f"{self.BASE_URL}/check-http",
                params=params,
                timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            
            # Get check ID and wait for results
            check_id = response.json().get('request_id')
            if not check_id:
                return {'error': 'No check ID received'}
            
            # Wait and get results
            time.sleep(5)  # Wait for nodes to respond
            result_url = f"{self.BASE_URL}/check-result/{check_id}"
            result_response = self.session.get(result_url, timeout=DEFAULT_TIMEOUT)
            result_response.raise_for_status()
            
            return result_response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def check_tcp(self, host: str, port: int, nodes: List[str] = None) -> Dict:
        """Perform TCP check from multiple nodes."""
        if nodes is None:
            nodes = list(NODE_DETAILS.keys())
        
        params = {
            'host': f"{host}:{port}",
            'node': nodes
        }
        
        try:
            # Request new check
            response = self.session.get(
                f"{self.BASE_URL}/check-tcp",
                params=params,
                timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            
            # Get check ID and wait for results
            check_id = response.json().get('request_id')
            if not check_id:
                return {'error': 'No check ID received'}
            
            # Wait and get results
            time.sleep(5)  # Wait for nodes to respond
            result_url = f"{self.BASE_URL}/check-result/{check_id}"
            result_response = self.session.get(result_url, timeout=DEFAULT_TIMEOUT)
            result_response.raise_for_status()
            
            return result_response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

class NetworkTester:
    def __init__(self):
        self.ping_path = self._find_ping_binary()
        self.timeout = DEFAULT_TIMEOUT
        self.max_threads = MAX_THREADS
        self.check_host_api = CheckHostAPI()

    def _find_ping_binary(self) -> str:
        """Find the appropriate ping binary for the system."""
        possible_paths = [
            '/bin/ping',
            '/usr/bin/ping',
            '/system/bin/ping',
            '/data/data/com.termux/files/usr/bin/ping'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Fallback to just 'ping' if none found (relying on PATH)
        return 'ping'

    def ping(self, host: str, count: int = PING_COUNT) -> Dict[str, Dict]:
        """
        Perform a global ping test to the specified host using all Check-Host nodes.
        
        Args:
            host: Hostname or IP address to ping
            count: Number of pings to send (not used in API check)
            
        Returns:
            Dictionary with ping results from all nodes
        """
        api_result = self.check_host_api.check_ping(host)
        
        if 'error' in api_result:
            return {'error': api_result['error']}
        
        results = {}
        for node, node_result in api_result.items():
            if node in NODE_DETAILS:
                region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                
                if node_result and isinstance(node_result, list) and len(node_result) > 0:
                    ping_result = node_result[0]
                    if isinstance(ping_result, dict) and 'rtt' in ping_result:
                        results[region] = {
                            'success': True,
                            'avg_latency': ping_result['rtt'],
                            'min_latency': ping_result['rtt'],
                            'max_latency': ping_result['rtt'],
                            'packet_loss': 0.0
                        }
                    else:
                        results[region] = {
                            'success': False,
                            'error': 'Invalid ping response'
                        }
                else:
                    results[region] = {
                        'success': False,
                        'error': 'No ping data'
                    }
        
        return results

    def http_check(self, url: str) -> Dict[str, Dict]:
        """
        Perform a global HTTP check to the specified URL using all Check-Host nodes.
        
        Args:
            url: URL to check (must include http:// or https://)
            
        Returns:
            Dictionary with HTTP results from all nodes
        """
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'

        api_result = self.check_host_api.check_http(url)
        
        if 'error' in api_result:
            return {'error': api_result['error']}
        
        results = {}
        for node, node_result in api_result.items():
            if node in NODE_DETAILS:
                region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                
                if node_result and isinstance(node_result, dict):
                    results[region] = {
                        'success': node_result.get('status', '').startswith('OK'),
                        'status_code': node_result.get('response_code', 0),
                        'response_time': node_result.get('time', 0)
                    }
                else:
                    results[region] = {
                        'success': False,
                        'error': 'No HTTP data'
                    }
        
        return results

    def tcp_check(self, host: str, port: int) -> Dict[str, Dict]:
        """
        Perform a global TCP check to the specified host and port using all Check-Host nodes.
        
        Args:
            host: Hostname or IP address
            port: TCP port number
            
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
                    if isinstance(tcp_result, dict) and 'time' in tcp_result:
                        results[region] = {
                            'success': True,
                            'connect_time': tcp_result['time']
                        }
                    else:
                        results[region] = {
                            'success': False,
                            'error': 'Invalid TCP response'
                        }
                else:
                    results[region] = {
                        'success': False,
                        'error': 'No TCP data'
                    }
        
        return results

    def udp_check(self, host: str, port: int) -> Dict[str, Dict]:
        """
        Perform a UDP check to the specified host and port from multiple locations.
        
        Args:
            host: Hostname or IP address
            port: UDP port number
            
        Returns:
            Dictionary with UDP results from multiple locations
        """
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {}
            
            for node in NODE_DETAILS:
                region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                futures[executor.submit(self._single_udp_check, host, port, node)] = region
            
            for future in concurrent.futures.as_completed(futures):
                region = futures[future]
                try:
                    results[region] = future.result()
                except Exception as e:
                    results[region] = {'error': str(e), 'success': False}

        return results

    def _single_udp_check(self, host: str, port: int, dns_server: str = None) -> Dict[str, Union[bool, float, str]]:
        """
        Perform a single UDP check to the specified host and port.
        
        Args:
            host: Hostname or IP address
            port: UDP port number
            dns_server: DNS server to use for host resolution
            
        Returns:
            Dictionary with UDP results including:
            - success: bool
            - response_time: float (in ms, if available)
            - error: str (if any)
        """
        result = {
            'success': False,
            'error': None
        }

        try:
            # Resolve host if needed
            if dns_server:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                resolver.timeout = self.timeout
                resolver.lifetime = self.timeout
                answers = resolver.resolve(host, 'A')
                target_ip = str(answers[0])
            else:
                target_ip = host

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            # Send a simple message
            message = b'PING'
            start_time = time.time()
            sock.sendto(message, (target_ip, port))
            
            # Try to receive (though UDP is connectionless)
            try:
                data, addr = sock.recvfrom(1024)
                end_time = time.time()
                result['success'] = True
                result['response_time'] = (end_time - start_time) * 1000  # Convert to ms
            except socket.timeout:
                # UDP is connectionless, so timeout doesn't necessarily mean failure
                result['success'] = True
                result['error'] = "No response (UDP is connectionless)"
                
        except Exception as e:
            result['error'] = f"UDP error: {str(e)}"
        finally:
            if 'sock' in locals():
                sock.close()

        return result

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
            # Single DNS check if server is specified
            return self._single_dns_check(domain, dns_server)
        else:
            # Global DNS check using Check-Host nodes
            results = {}
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = {}
                
                for node in NODE_DETAILS:
                    region = f"{NODE_DETAILS[node]['country']} ({NODE_DETAILS[node]['city']})"
                    futures[executor.submit(self._single_dns_check, domain, node)] = region
                
                for future in concurrent.futures.as_completed(futures):
                    region = futures[future]
                    try:
                        results[region] = future.result()
                    except Exception as e:
                        results[region] = {'error': str(e), 'success': False}

            return results

    def _single_dns_check(self, domain: str, dns_server: str) -> Dict[str, Union[bool, float, str, list]]:
        """
        Perform a single DNS resolution check for the specified domain.
        
        Args:
            domain: Domain name to resolve
            dns_server: DNS server to use
            
        Returns:
            Dictionary with DNS results including:
            - success: bool
            - resolution_time: float (in ms)
            - addresses: list of resolved IPs
            - error: str (if any)
        """
        result = {
            'success': False,
            'resolution_time': 0.0,
            'addresses': [],
            'error': None
        }

        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server]
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

        return result


def display_ping_results(results: Dict) -> None:
    """Display ping results in a formatted way."""
    print(f"\n{Fore.CYAN}PING RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Packet Loss':<15} {'Latency (min/avg/max)':<25}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in data:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            packet_loss = "N/A"
            latency = data['error']
        else:
            status = f"{Fore.GREEN}UP{Style.RESET_ALL}" if data.get('success') else f"{Fore.RED}DOWN{Style.RESET_ALL}"
            packet_loss = f"{data.get('packet_loss', 0):.1f}%"
            
            if data.get('success'):
                latency = f"{data.get('min_latency', 0):.1f}/{data.get('avg_latency', 0):.1f}/{data.get('max_latency', 0):.1f} ms"
            else:
                latency = "N/A"
        
        print(f"{location:<30} {status:<10} {packet_loss:<15} {latency:<25}")


def display_http_results(results: Dict) -> None:
    """Display HTTP results in a formatted way."""
    print(f"\n{Fore.CYAN}HTTP RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Response Code':<15} {'Response Time':<15}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in data:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            code = "N/A"
            time_ms = data['error']
        else:
            if data.get('success'):
                status = f"{Fore.GREEN}UP{Style.RESET_ALL}"
                code = str(data.get('status_code', 'N/A'))
                time_ms = f"{data.get('response_time', 0):.1f} ms"
            else:
                status = f"{Fore.RED}DOWN{Style.RESET_ALL}"
                code = "N/A"
                time_ms = "N/A"
        
        print(f"{location:<30} {status:<10} {code:<15} {time_ms:<15}")


def display_tcp_results(results: Dict, port: int) -> None:
    """Display TCP results in a formatted way."""
    print(f"\n{Fore.CYAN}TCP PORT {port} RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Connect Time':<15}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in data:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            time_ms = data['error']
        else:
            if data.get('success'):
                status = f"{Fore.GREEN}OPEN{Style.RESET_ALL}"
                time_ms = f"{data.get('connect_time', 0):.1f} ms"
            else:
                status = f"{Fore.RED}CLOSED{Style.RESET_ALL}"
                time_ms = "N/A"
        
        print(f"{location:<30} {status:<10} {time_ms:<15}")


def display_udp_results(results: Dict, port: int) -> None:
    """Display UDP results in a formatted way."""
    print(f"\n{Fore.CYAN}UDP PORT {port} RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Response Time':<15}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in data:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            time_ms = data['error']
        else:
            if data.get('success'):
                status = f"{Fore.GREEN}UP{Style.RESET_ALL}"
                time_ms = f"{data.get('response_time', 0):.1f} ms" if 'response_time' in data else "No response"
            else:
                status = f"{Fore.RED}DOWN{Style.RESET_ALL}"
                time_ms = "N/A"
        
        print(f"{location:<30} {status:<10} {time_ms:<15}")


def display_dns_results(results: Dict) -> None:
    """Display DNS results in a formatted way."""
    print(f"\n{Fore.CYAN}DNS RESULTS:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<10} {'Resolution Time':<20} {'Addresses':<30}")
    print("-" * 80)
    
    for location, data in results.items():
        if 'error' in data:
            status = f"{Fore.RED}ERROR{Style.RESET_ALL}"
            time_ms = "N/A"
            addresses = data['error']
        else:
            if data.get('success'):
                status = f"{Fore.GREEN}OK{Style.RESET_ALL}"
                time_ms = f"{data.get('resolution_time', 0):.1f} ms"
                addresses = ", ".join(data.get('addresses', []))[:30]
            else:
                status = f"{Fore.RED}FAIL{Style.RESET_ALL}"
                time_ms = "N/A"
                addresses = data.get('error', 'Unknown error')
        
        print(f"{location:<30} {status:<10} {time_ms:<20} {addresses:<30}")


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


def interactive_mode():
    """Run in interactive mode."""
    tester = NetworkTester()
    
    print(f"{Fore.CYAN}=== Network Diagnostic Tool ==={Style.RESET_ALL}")
    
    while True:
        print("\nOptions:")
        print("1. Ping test")
        print("2. HTTP/HTTPS test")
        print("3. TCP port test")
        print("4. UDP port test")
        print("5. DNS resolution test")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '0':
            break
        
        if choice == '1':
            host = input("Enter host to ping: ")
            results = tester.ping(host)
            display_ping_results(results)
            
        elif choice == '2':
            url = input("Enter URL to test (include http:// or https://): ")
            results = tester.http_check(url)
            display_http_results(results)
                
        elif choice == '3':
            host = input("Enter host: ")
            port = int(input("Enter TCP port: "))
            results = tester.tcp_check(host, port)
            display_tcp_results(results, port)
                
        elif choice == '4':
            host = input("Enter host: ")
            port = int(input("Enter UDP port: "))
            results = tester.udp_check(host, port)
            display_udp_results(results, port)
                
        elif choice == '5':
            domain = input("Enter domain to resolve: ")
            dns_server = input("Enter DNS server (leave empty for global check): ") or None
            results = tester.dns_check(domain, dns_server)
            display_dns_results(results)
                
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        
        # Ask to save results
        save = input("\nSave results to file? (y/n): ").lower()
        if save == 'y':
            filename = input("Enter filename: ")
            format = input("Format (json/text): ").lower() or 'json'
            save_results(results, filename, format)


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Network Diagnostic Tool')
    subparsers = parser.add_subparsers(dest='command', required=False)

    # Ping command
    ping_parser = subparsers.add_parser('ping', help='Perform ping test')
    ping_parser.add_argument('host', help='Host to ping')
    ping_parser.add_argument('-c', '--count', type=int, default=PING_COUNT, 
                           help='Number of pings to send (not used in API check)')
    ping_parser.add_argument('-o', '--output', help='Output file to save results')
    ping_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    # HTTP command
    http_parser = subparsers.add_parser('http', help='Perform HTTP test')
    http_parser.add_argument('url', help='URL to test')
    http_parser.add_argument('-o', '--output', help='Output file to save results')
    http_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    # TCP command
    tcp_parser = subparsers.add_parser('tcp', help='Perform TCP port test')
    tcp_parser.add_argument('host', help='Host to test')
    tcp_parser.add_argument('port', type=int, help='TCP port to test')
    tcp_parser.add_argument('-o', '--output', help='Output file to save results')
    tcp_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    # UDP command
    udp_parser = subparsers.add_parser('udp', help='Perform UDP port test')
    udp_parser.add_argument('host', help='Host to test')
    udp_parser.add_argument('port', type=int, help='UDP port to test')
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
        if args.command == 'ping':
            results = tester.ping(args.host, args.count)
            display_ping_results(results)
            
        elif args.command == 'http':
            results = tester.http_check(args.url)
            display_http_results(results)
                
        elif args.command == 'tcp':
            results = tester.tcp_check(args.host, args.port)
            display_tcp_results(results, args.port)
                
        elif args.command == 'udp':
            results = tester.udp_check(args.host, args.port)
            display_udp_results(results, args.port)
                
        elif args.command == 'dns':
            results = tester.dns_check(args.domain, args.server)
            display_dns_results(results)
        
        # Save results if requested
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