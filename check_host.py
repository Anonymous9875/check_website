#!/usr/bin/env python3
import subprocess
import socket
import time
import requests
import dns.resolver
import threading
from concurrent.futures import ThreadPoolExecutor
from statistics import mean

class NetworkTester:
    def __init__(self, target="google.com", timeout=5):
        self.target = target
        self.timeout = timeout
        self.results = {}

    def ping(self, count=4):
        """Realiza un test de ping y mide latencia"""
        try:
            # Comando ping diferente para Linux/Termux
            cmd = f"ping -c {count} {self.target}"
            start_time = time.time()
            output = subprocess.check_output(cmd, shell=True, text=True)
            end_time = time.time()
            
            # Extraer tiempos de respuesta
            times = [float(line.split('time=')[1].split(' ')[0]) 
                    for line in output.split('\n') if 'time=' in line]
            
            if times:
                avg_latency = mean(times)
                self.results['ping'] = {
                    'status': 'online',
                    'avg_latency': f"{avg_latency:.2f} ms",
                    'speed': f"{(end_time - start_time)*1000/count:.2f} ms/packet"
                }
            else:
                self.results['ping'] = {'status': 'offline'}
                
        except subprocess.CalledProcessError:
            self.results['ping'] = {'status': 'offline'}

    def http(self):
        """Prueba conexión HTTP y mide velocidad de respuesta"""
        try:
            url = f"http://{self.target}"
            start_time = time.time()
            response = requests.get(url, timeout=self.timeout)
            end_time = time.time()
            
            self.results['http'] = {
                'status': 'online',
                'response_time': f"{(end_time - start_time)*1000:.2f} ms",
                'status_code': response.status_code
            }
        except requests.RequestException:
            self.results['http'] = {'status': 'offline'}

    def tcp(self, port=80):
        """Prueba conexión TCP en el puerto especificado"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            end_time = time.time()
            
            if result == 0:
                self.results['tcp'] = {
                    'status': 'online',
                    'port': port,
                    'response_time': f"{(end_time - start_time)*1000:.2f} ms"
                }
            else:
                self.results['tcp'] = {'status': 'offline'}
            sock.close()
            
        except socket.error:
            self.results['tcp'] = {'status': 'offline'}

    def udp(self, port=53):
        """Prueba conexión UDP en el puerto especificado"""
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.sendto(b"test", (self.target, port))
            data, _ = sock.recvfrom(1024)
            end_time = time.time()
            
            self.results['udp'] = {
                'status': 'online',
                'port': port,
                'response_time': f"{(end_time - start_time)*1000:.2f} ms"
            }
            sock.close()
            
        except socket.error:
            self.results['udp'] = {'status': 'offline'}

    def dns(self):
        """Prueba resolución DNS"""
        try:
            start_time = time.time()
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(self.target, 'A')
            end_time = time.time()
            
            ips = [answer.address for answer in answers]
            self.results['dns'] = {
                'status': 'online',
                'ips': ips,
                'resolution_time': f"{(end_time - start_time)*1000:.2f} ms"
            }
            
        except dns.resolver.NXDOMAIN:
            self.results['dns'] = {'status': 'offline'}
        except Exception as e:
            self.results['dns'] = {'status': f'error: {str(e)}'}

    def run_all_tests(self):
        """Ejecuta todos los tests en paralelo"""
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(self.ping)
            executor.submit(self.http)
            executor.submit(self.tcp)
            executor.submit(self.udp)
            executor.submit(self.dns)

    def display_results(self):
        """Muestra los resultados de las pruebas"""
        print(f"\nResultados para {self.target}:")
        print("-" * 50)
        for test, result in self.results.items():
            print(f"{test.upper()} Test:")
            for key, value in result.items():
                print(f"  {key}: {value}")
            print()

def test_multiple_countries(target):
    """Prueba el target desde diferentes servidores DNS por país"""
    countries = {
        'US': '8.8.8.8',    # Google DNS
        'EU': '1.1.1.1',    # Cloudflare DNS
        'RU': '77.88.8.8',  # Yandex DNS
        'CN': '223.5.5.5'   # AliDNS
    }
    
    for country, dns_server in countries.items():
        print(f"\nTesting from {country}:")
        tester = NetworkTester(target)
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        tester.run_all_tests()
        tester.display_results()

if __name__ == "__main__":
    # Lista de sitios web para probar
    targets = ["google.com", "facebook.com", "twitter.com"]
    
    for target in targets:
        print(f"\n{'='*50}\nTesting {target}\n{'='*50}")
        test_multiple_countries(target)