import json
import argparse
import requests
from urllib.parse import quote
import time
from typing import Dict, List, Optional

from src.script.method.ip_lookup import ip_lookup
from src.script.method.whois import whois
from src.script.method.ping import ping
from src.script.method.http import http
from src.script.method.tcp import tcp
from src.script.method.udp import udp
from src.script.method.dns import dns
from src.script.logs import logs

# Node data organized by continent
NODES_BY_CONTINENT = {
    "EU": ["bg1.node.check-host.net", "ch1.node.check-host.net", "cz1.node.check-host.net", ...],  # Lista completa del segundo script
    "AS": ["hk1.node.check-host.net", "il1.node.check-host.net", ...],
    "NA": ["us1.node.check-host.net", "us2.node.check-host.net", "us3.node.check-host.net"],
    "SA": ["br1.node.check-host.net"],
    "EU-EAST": ["ru1.node.check-host.net", "ru2.node.check-host.net", ...]
}

ALL_NODES = [node for nodes in NODES_BY_CONTINENT.values() for node in nodes]

NODE_DETAILS = {
    "bg1.node.check-host.net": {"country": "Bulgaria", "city": "Sofia", "continent": "EU"},
    "ch1.node.check-host.net": {"country": "Switzerland", "city": "Zurich", "continent": "EU"},
    # ... resto de los detalles de nodos del segundo script
}

class CheckHost:
    def __init__(self):
        self.ip_lookup_class = ip_lookup()
        self.whois_class = whois()
        self.ping_class = ping()
        self.http_class = http()
        self.tcp_class = tcp()
        self.udp_class = udp()
        self.dns_class = dns()
        self.logs_class = logs()

    def _check_host_config_file_open(self) -> Dict[str, Dict[str, str]]:
        with open("src/check-host-config.json", "r") as f:
            return json.load(f)

    def _check_host_config_access(self, func: str, attribute: str) -> str:
        return self._check_host_config_file_open()[func][attribute]

    def _check_host_logo(self) -> str:
        version = self._check_host_config_access("check-host", "version")
        return f"""
              __           __       __            __ 
         ____/ /  ___ ____/ /______/ /  ___  ___ / /_
        / __/ _ \/ -_) __/  '_/___/ _ \/ _ \(_-</ __/
        \__/_//_/\__/\__/_/\_\   /_//_/\___/___/\__/ v{version}
                            https://github.com/Anonymous9875
                            ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ
        """

    def _perform_network_check(self, method: str, target: str, max_nodes: Optional[int] = None) -> None:
        try:
            encoded_target = quote(target, safe='')
            api_urls = {
                "ping": f"https://check-host.net/check-ping?host={encoded_target}",
                "http": f"https://check-host.net/check-http?host={encoded_target}",
                "tcp": f"https://check-host.net/check-tcp?host={encoded_target}",
                "udp": f"https://check-host.net/check-udp?host={encoded_target}",
                "dns": f"https://check-host.net/check-dns?host={encoded_target}"
            }
            
            if max_nodes:
                api_urls[method] += f"&max_nodes={max_nodes}"

            headers = {"Accept": "application/json"}
            response = requests.get(api_urls[method], headers=headers, timeout=15)
            
            if response.status_code != 200:
                self.logs_class.logs_console_print("check-host/network", "error", 
                    f"Request failed with status: {response.status_code}")
                return

            data = response.json()
            request_id = data.get("request_id")
            if not request_id:
                self.logs_class.logs_console_print("check-host/network", "error", "No request_id received")
                return

            self.logs_class.logs_console_print("check-host/network", "info", 
                f"Checking {method} for {target}...")

            # Wait for results
            max_wait, wait_interval, elapsed = 50, 2, 0
            while elapsed < max_wait:
                result_response = requests.get(f"https://check-host.net/check-result/{request_id}", 
                                            headers=headers, timeout=15)
                if result_response.status_code == 200:
                    results = result_response.json()
                    if all(node in results for node in ALL_NODES[:max_nodes or len(ALL_NODES)]):
                        break
                time.sleep(wait_interval)
                elapsed += wait_interval

            self._display_results(method, target, results)
            
        except Exception as e:
            self.logs_class.logs_console_print("check-host/network", "error", str(e))

    def _display_results(self, method: str, target: str, results: Dict) -> None:
        self.logs_class.logs_console_print("check-host/results", "info", f"\nResults for {method} - {target}:")
        for node in ALL_NODES:
            if node not in results or results[node] is None:
                continue
                
            node_info = NODE_DETAILS.get(node, {"country": "Unknown", "city": "Unknown"})
            result = results[node]
            
            if method == "ping" and isinstance(result, list) and len(result) >= 2:
                avg_time = result[1]
                status = f"{node_info['country']}, {node_info['city']}: {avg_time:.2f}ms" if avg_time else "No response"
                self.logs_class.logs_console_print("check-host/results", "info", status)
            # Agregar más condiciones para otros métodos según sea necesario

    def _check_host_method(self, args: argparse.Namespace) -> None:
        method_dict = {
            "ip-lookup": self.ip_lookup_class.ip_lookup_run,
            "whois": self.whois_class.whois_run,
            "ping": lambda a: self._perform_network_check("ping", a.target, a.max_nodes),
            "http": lambda a: self._perform_network_check("http", a.target, a.max_nodes),
            "tcp": lambda a: self._perform_network_check("tcp", a.target, a.max_nodes),
            "udp": lambda a: self._perform_network_check("udp", a.target, a.max_nodes),
            "dns": lambda a: self._perform_network_check("dns", a.target, a.max_nodes)
        }
        method_dict[args.method](args)

    def _check_host_argparse(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Host checking tool",
            usage="python3 check-host.py -m {method} -t {target} [-mx {max_nodes}]"
        )
        parser.add_argument("-t", "--target", required=True, help="Target host (URL, IP, or domain)")
        parser.add_argument("-m", "--method", required=True, 
                          choices=["ip-lookup", "whois", "ping", "http", "tcp", "udp", "dns"],
                          help="Check method")
        parser.add_argument("-mx", "--max-nodes", type=int, help="Maximum number of nodes")
        return parser.parse_args()

    def check_host_run(self) -> None:
        self.logs_class.logs_logo_print(self._check_host_logo())
        args = self._check_host_argparse()
        self._check_host_method(args)

if __name__ == "__main__":
    try:
        check_host = CheckHost()
        check_host.check_host_run()
    except SystemExit:
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")