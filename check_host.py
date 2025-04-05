#!/usr/bin/env python3
"""
Network Diagnostic Tool

A comprehensive network testing tool that performs:
- Ping tests
- HTTP/HTTPS availability and speed tests
- TCP port checks
- UDP checks
- DNS resolution tests

Works on both Linux and Termux environments.
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

class NetworkTester:
    def __init__(self):
        self.ping_path = self._find_ping_binary()
        self.timeout = DEFAULT_TIMEOUT
        self.max_threads = MAX_THREADS

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

    def ping(self, host: str, count: int = PING_COUNT) -> Dict[str, Union[float, bool, str]]:
        """
        Perform a ping test to the specified host.
        
        Args:
            host: Hostname or IP address to ping
            count: Number of pings to send
            
        Returns:
            Dictionary with ping results including:
            - success: bool
            - packet_loss: float
            - avg_latency: float (in ms)
            - min_latency: float (in ms)
            - max_latency: float (in ms)
            - raw_output: str
        """
        try:
            # Validate host
            ipaddress.ip_address(host)
            target = host
        except ValueError:
            target = host.split(':')[0]  # Remove port if present

        result = {
            'success': False,
            'packet_loss': 100.0,
            'avg_latency': 0.0,
            'min_latency': 0.0,
            'max_latency': 0.0,
            'raw_output': ''
        }

        try:
            # Different ping options for different systems
            if 'termux' in self.ping_path.lower():
                cmd = [self.ping_path, '-c', str(count), '-W', str(self.timeout), target]
            else:
                cmd = [self.ping_path, '-c', str(count), '-w', str(self.timeout), target]

            output = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout + 2
            )

            result['raw_output'] = output.stdout

            if output.returncode == 0:
                result['success'] = True

            # Parse ping output
            lines = output.stdout.split('\n')
            stats_line = None

            for line in lines:
                if 'packets transmitted' in line and 'received' in line:
                    stats_line = line
                    break

            if stats_line:
                parts = stats_line.split(',')
                if len(parts) >= 3:
                    # Packet loss
                    transmitted = int(parts[0].split()[0])
                    received = int(parts[1].split()[0])
                    loss = 100.0 - (received / transmitted * 100)
                    result['packet_loss'] = loss

                    # Latency stats (if available)
                    if 'min/avg/max' in parts[2]:
                        latency_parts = parts[2].split('=')[1].split('/')
                        result['min_latency'] = float(latency_parts[0])
                        result['avg_latency'] = float(latency_parts[1])
                        result['max_latency'] = float(latency_parts[2])

        except subprocess.TimeoutExpired:
            result['raw_output'] = "Ping timed out"
        except Exception as e:
            result['raw_output'] = f"Ping error: {str(e)}"

        return result

    def http_check(self, url: str) -> Dict[str, Union[float, bool, int, str]]:
        """
        Perform an HTTP/HTTPS check to the specified URL.
        
        Args:
            url: URL to check (must include http:// or https://)
            
        Returns:
            Dictionary with HTTP results including:
            - success: bool
            - status_code: int
            - response_time: float (in seconds)
            - error: str (if any)
        """
        result = {
            'success': False,
            'status_code': 0,
            'response_time': 0.0,
            'error': None
        }

        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'

        try:
            start_time = time.time()
            response = requests.get(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                headers={'User-Agent': 'NetworkTester/1.0'}
            )
            end_time = time.time()

            result['status_code'] = response.status_code
            result['response_time'] = (end_time - start_time) * 1000  # Convert to ms
            result['success'] = response.ok

        except requests.exceptions.RequestException as e:
            result['error'] = str(e)
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"

        return result

    def tcp_check(self, host: str, port: int) -> Dict[str, Union[bool, float, str]]:
        """
        Perform a TCP connection check to the specified host and port.
        
        Args:
            host: Hostname or IP address
            port: TCP port number
            
        Returns:
            Dictionary with TCP results including:
            - success: bool
            - connect_time: float (in seconds)
            - error: str (if any)
        """
        result = {
            'success': False,
            'connect_time': 0.0,
            'error': None
        }

        try:
            start_time = time.time()
            with socket.create_connection((host, port), timeout=self.timeout):
                end_time = time.time()
                result['connect_time'] = (end_time - start_time) * 1000  # Convert to ms
                result['success'] = True
        except socket.timeout:
            result['error'] = "Connection timed out"
        except ConnectionRefusedError:
            result['error'] = "Connection refused"
        except Exception as e:
            result['error'] = f"TCP error: {str(e)}"

        return result

    def udp_check(self, host: str, port: int) -> Dict[str, Union[bool, float, str]]:
        """
        Perform a UDP check to the specified host and port.
        
        Args:
            host: Hostname or IP address
            port: UDP port number
            
        Returns:
            Dictionary with UDP results including:
            - success: bool
            - error: str (if any)
        """
        result = {
            'success': False,
            'error': None
        }

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            # Send a simple message
            message = b'PING'
            start_time = time.time()
            sock.sendto(message, (host, port))
            
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
            sock.close()

        return result

    def dns_check(self, domain: str, dns_server: str = '8.8.8.8') -> Dict[str, Union[bool, float, str, list]]:
        """
        Perform a DNS resolution check for the specified domain.
        
        Args:
            domain: Domain name to resolve
            dns_server: DNS server to use (default: 8.8.8.8)
            
        Returns:
            Dictionary with DNS results including:
            - success: bool
            - resolution_time: float (in seconds)
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

    def check_global_availability(self, host: str, check_type: str = 'ping', 
                                port: Optional[int] = None) -> Dict[str, Dict[str, Dict]]:
        """
        Check global availability by testing from multiple locations.
        
        Args:
            host: Host to check
            check_type: Type of check (ping, http, tcp, udp, dns)
            port: Port number (required for tcp/udp checks)
            
        Returns:
            Dictionary with results from different regions
        """
        # This is a simplified version. In a real implementation, you would:
        # 1. Use a service with global nodes (like the original script)
        # 2. Or deploy your own nodes in different regions
        # 3. Or use cloud provider APIs
        
        # For this example, we'll simulate different regions by using different DNS servers
        regions = {
            'North America': {'dns': '8.8.8.8'},  # Google DNS
            'Europe': {'dns': '1.1.1.1'},        # Cloudflare DNS
            'Asia': {'dns': '114.114.114.114'},  # China DNS
            'South America': {'dns': '200.160.0.29'},  # Brazil DNS
            'Oceania': {'dns': '203.50.2.71'}    # Australia DNS
        }

        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {}
            
            for region, config in regions.items():
                if check_type == 'dns':
                    futures[executor.submit(self.dns_check, host, config['dns'])] = region
                elif check_type == 'ping':
                    futures[executor.submit(self.ping, host)] = region
                elif check_type == 'http':
                    futures[executor.submit(self.http_check, host)] = region
                elif check_type == 'tcp' and port:
                    futures[executor.submit(self.tcp_check, host, port)] = region
                elif check_type == 'udp' and port:
                    futures[executor.submit(self.udp_check, host, port)] = region
            
            for future in concurrent.futures.as_completed(futures):
                region = futures[future]
                try:
                    results[region] = future.result()
                except Exception as e:
                    results[region] = {'error': str(e), 'success': False}

        return results


def display_ping_results(results: Dict) -> None:
    """Display ping results in a formatted way."""
    print(f"\n{Fore.CYAN}PING RESULTS:{Style.RESET_ALL}")
    print(f"{'Region':<20} {'Status':<10} {'Packet Loss':<15} {'Latency (min/avg/max)':<25}")
    print("-" * 70)
    
    for region, data in results.items():
        status = f"{Fore.GREEN}UP{Style.RESET_ALL}" if data.get('success') else f"{Fore.RED}DOWN{Style.RESET_ALL}"
        packet_loss = f"{data.get('packet_loss', 0):.1f}%"
        
        if data.get('success'):
            latency = f"{data.get('min_latency', 0):.1f}/{data.get('avg_latency', 0):.1f}/{data.get('max_latency', 0):.1f} ms"
        else:
            latency = "N/A"
        
        print(f"{region:<20} {status:<10} {packet_loss:<15} {latency:<25}")


def display_http_results(results: Dict) -> None:
    """Display HTTP results in a formatted way."""
    print(f"\n{Fore.CYAN}HTTP RESULTS:{Style.RESET_ALL}")
    print(f"{'Region':<20} {'Status':<10} {'Response Code':<15} {'Response Time':<15}")
    print("-" * 70)
    
    for region, data in results.items():
        if data.get('success'):
            status = f"{Fore.GREEN}UP{Style.RESET_ALL}"
            code = str(data.get('status_code', 'N/A'))
            time_ms = f"{data.get('response_time', 0):.1f} ms"
        else:
            status = f"{Fore.RED}DOWN{Style.RESET_ALL}"
            code = "N/A"
            time_ms = "N/A"
        
        print(f"{region:<20} {status:<10} {code:<15} {time_ms:<15}")


def display_tcp_results(results: Dict, port: int) -> None:
    """Display TCP results in a formatted way."""
    print(f"\n{Fore.CYAN}TCP PORT {port} RESULTS:{Style.RESET_ALL}")
    print(f"{'Region':<20} {'Status':<10} {'Connect Time':<15}")
    print("-" * 70)
    
    for region, data in results.items():
        if data.get('success'):
            status = f"{Fore.GREEN}OPEN{Style.RESET_ALL}"
            time_ms = f"{data.get('connect_time', 0):.1f} ms"
        else:
            status = f"{Fore.RED}CLOSED{Style.RESET_ALL}"
            time_ms = "N/A"
        
        print(f"{region:<20} {status:<10} {time_ms:<15}")


def display_udp_results(results: Dict, port: int) -> None:
    """Display UDP results in a formatted way."""
    print(f"\n{Fore.CYAN}UDP PORT {port} RESULTS:{Style.RESET_ALL}")
    print(f"{'Region':<20} {'Status':<10} {'Response Time':<15}")
    print("-" * 70)
    
    for region, data in results.items():
        if data.get('success'):
            status = f"{Fore.GREEN}UP{Style.RESET_ALL}"
            time_ms = f"{data.get('response_time', 0):.1f} ms" if 'response_time' in data else "No response"
        else:
            status = f"{Fore.RED}DOWN{Style.RESET_ALL}"
            time_ms = "N/A"
        
        print(f"{region:<20} {status:<10} {time_ms:<15}")


def display_dns_results(results: Dict) -> None:
    """Display DNS results in a formatted way."""
    print(f"\n{Fore.CYAN}DNS RESULTS:{Style.RESET_ALL}")
    print(f"{'Region':<20} {'Status':<10} {'Resolution Time':<20} {'Addresses':<30}")
    print("-" * 70)
    
    for region, data in results.items():
        if data.get('success'):
            status = f"{Fore.GREEN}OK{Style.RESET_ALL}"
            time_ms = f"{data.get('resolution_time', 0):.1f} ms"
            addresses = ", ".join(data.get('addresses', []))[:30]
        else:
            status = f"{Fore.RED}FAIL{Style.RESET_ALL}"
            time_ms = "N/A"
            addresses = data.get('error', 'Unknown error')
        
        print(f"{region:<20} {status:<10} {time_ms:<20} {addresses:<30}")


def save_results(results: Dict, filename: str, format: str = 'json') -> None:
    """Save results to a file in the specified format."""
    try:
        with open(filename, 'w') as f:
            if format == 'json':
                json.dump(results, f, indent=2)
            else:  # text
                for region, data in results.items():
                    f.write(f"Region: {region}\n")
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
        print("6. Global availability test")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '0':
            break
        
        if choice == '1':
            host = input("Enter host to ping: ")
            results = tester.ping(host)
            print("\nResults:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Packet Loss: {results['packet_loss']:.1f}%")
            print(f"Latency (min/avg/max): {results['min_latency']:.1f}/{results['avg_latency']:.1f}/{results['max_latency']:.1f} ms")
            
        elif choice == '2':
            url = input("Enter URL to test (include http:// or https://): ")
            results = tester.http_check(url)
            print("\nResults:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Status Code: {results.get('status_code', 'N/A')}")
            print(f"Response Time: {results['response_time']:.1f} ms")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif choice == '3':
            host = input("Enter host: ")
            port = int(input("Enter TCP port: "))
            results = tester.tcp_check(host, port)
            print("\nResults:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Connect Time: {results['connect_time']:.1f} ms")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif choice == '4':
            host = input("Enter host: ")
            port = int(input("Enter UDP port: "))
            results = tester.udp_check(host, port)
            print("\nResults:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            if 'response_time' in results:
                print(f"Response Time: {results['response_time']:.1f} ms")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif choice == '5':
            domain = input("Enter domain to resolve: ")
            dns_server = input("Enter DNS server (leave empty for default): ") or '8.8.8.8'
            results = tester.dns_check(domain, dns_server)
            print("\nResults:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Resolution Time: {results['resolution_time']:.1f} ms")
            print(f"Addresses: {', '.join(results['addresses'])}")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif choice == '6':
            print("\nGlobal Availability Test")
            host = input("Enter host/domain to test: ")
            print("\nTest types:")
            print("1. Ping")
            print("2. HTTP")
            print("3. TCP Port")
            print("4. UDP Port")
            print("5. DNS")
            
            test_choice = input("Select test type: ")
            
            if test_choice == '1':
                results = tester.check_global_availability(host, 'ping')
                display_ping_results(results)
            elif test_choice == '2':
                results = tester.check_global_availability(host, 'http')
                display_http_results(results)
            elif test_choice == '3':
                port = int(input("Enter TCP port: "))
                results = tester.check_global_availability(host, 'tcp', port)
                display_tcp_results(results, port)
            elif test_choice == '4':
                port = int(input("Enter UDP port: "))
                results = tester.check_global_availability(host, 'udp', port)
                display_udp_results(results, port)
            elif test_choice == '5':
                results = tester.check_global_availability(host, 'dns')
                display_dns_results(results)
                
            # Ask to save results
            save = input("\nSave results to file? (y/n): ").lower()
            if save == 'y':
                filename = input("Enter filename: ")
                format = input("Format (json/text): ").lower() or 'json'
                save_results(results, filename, format)
                
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Network Diagnostic Tool')
    subparsers = parser.add_subparsers(dest='command', required=False)

    # Ping command
    ping_parser = subparsers.add_parser('ping', help='Perform ping test')
    ping_parser.add_argument('host', help='Host to ping')
    ping_parser.add_argument('-c', '--count', type=int, default=PING_COUNT, 
                           help='Number of pings to send')
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
    dns_parser.add_argument('-s', '--server', default='8.8.8.8', 
                           help='DNS server to use (default: 8.8.8.8)')
    dns_parser.add_argument('-o', '--output', help='Output file to save results')
    dns_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                           help='Output format')

    # Global command
    global_parser = subparsers.add_parser('global', help='Perform global availability test')
    global_parser.add_argument('host', help='Host to test')
    global_parser.add_argument('type', choices=['ping', 'http', 'tcp', 'udp', 'dns'],
                             help='Type of test to perform')
    global_parser.add_argument('-p', '--port', type=int, 
                             help='Port number (required for tcp/udp tests)')
    global_parser.add_argument('-o', '--output', help='Output file to save results')
    global_parser.add_argument('-f', '--format', choices=['json', 'text'], default='json',
                             help='Output format')

    args = parser.parse_args()

    tester = NetworkTester()

    if not args.command:
        interactive_mode()
        return

    try:
        if args.command == 'ping':
            results = tester.ping(args.host, args.count)
            print("\nPing Results:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Packet Loss: {results['packet_loss']:.1f}%")
            print(f"Latency (min/avg/max): {results['min_latency']:.1f}/{results['avg_latency']:.1f}/{results['max_latency']:.1f} ms")
            
        elif args.command == 'http':
            results = tester.http_check(args.url)
            print("\nHTTP Results:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Status Code: {results.get('status_code', 'N/A')}")
            print(f"Response Time: {results['response_time']:.1f} ms")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif args.command == 'tcp':
            results = tester.tcp_check(args.host, args.port)
            print("\nTCP Results:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Connect Time: {results['connect_time']:.1f} ms")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif args.command == 'udp':
            results = tester.udp_check(args.host, args.port)
            print("\nUDP Results:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            if 'response_time' in results:
                print(f"Response Time: {results['response_time']:.1f} ms")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif args.command == 'dns':
            results = tester.dns_check(args.domain, args.server)
            print("\nDNS Results:")
            print(f"Success: {'Yes' if results['success'] else 'No'}")
            print(f"Resolution Time: {results['resolution_time']:.1f} ms")
            print(f"Addresses: {', '.join(results['addresses'])}")
            if results['error']:
                print(f"Error: {results['error']}")
                
        elif args.command == 'global':
            if args.type in ['tcp', 'udp'] and not args.port:
                print(f"{Fore.RED}Error: Port number is required for TCP/UDP tests{Style.RESET_ALL}")
                return
                
            results = tester.check_global_availability(args.host, args.type, args.port)
            
            if args.type == 'ping':
                display_ping_results(results)
            elif args.type == 'http':
                display_http_results(results)
            elif args.type == 'tcp':
                display_tcp_results(results, args.port)
            elif args.type == 'udp':
                display_udp_results(results, args.port)
            elif args.type == 'dns':
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