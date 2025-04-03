#!/usr/bin/env python3
"""
Check-Host Ping & HTTP Tester (Multiplataforma)
"""

# ... (todo el código anterior se mantiene igual hasta la función interactive_mode())

def interactive_mode() -> None:
    """Run the program in interactive mode, prompting for inputs."""
    print(f"{Fore.CYAN}=== Check-Host Ping & HTTP Tester - Interactive Mode ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Escribe 'exit' en cualquier momento para salir.{Style.RESET_ALL}\n")
    
    # Get host to check
    while True:
        host = input(f"{Fore.YELLOW}Enter host to check (domain or IP): {Style.RESET_ALL}")
        if host.lower() == 'exit':
            sys.exit(0)
        try:
            host = validate_host(host)
            break
        except ValueError as e:
            print(f"{Fore.RED}{e}. Please try again.{Style.RESET_ALL}")
    
    # Get check type
    check_type = ""
    while check_type not in ["ping", "http"]:
        check_type = input(f"{Fore.YELLOW}Enter check type (ping/http) [default: ping]: {Style.RESET_ALL}").lower() or "ping"
        if check_type.lower() == 'exit':
            sys.exit(0)
        if check_type not in ["ping", "http"]:
            print(f"{Fore.RED}Invalid check type. Please enter 'ping' or 'http'.{Style.RESET_ALL}")
    
    # Get nodes selection
    print(f"\n{Fore.CYAN}Available continent options:{Style.RESET_ALL}")
    print("  ALL   - All available nodes")
    print("  EU    - European nodes")
    print("  NA    - North American nodes")
    print("  AS    - Asian nodes")
    print("  SA    - South American nodes")
    print("  EU+NA - European and North American nodes")
    
    continent = input(f"\n{Fore.YELLOW}Select nodes by continent [default: ALL]: {Style.RESET_ALL}").upper() or "ALL"
    if continent.lower() == 'exit':
        sys.exit(0)
    nodes = get_nodes_selection(continent)
    
    print(f"\n{Fore.CYAN}Selected {len(nodes)} nodes from {continent or 'ALL'}{Style.RESET_ALL}")
    
    # Ask about saving results
    save_option = input(f"{Fore.YELLOW}Save results to file? (y/n) [default: n]: {Style.RESET_ALL}").lower() or "n"
    if save_option == 'exit':
        sys.exit(0)
    save_to_file = save_option in ["y", "yes"]
    
    if save_to_file:
        format_type = input(f"{Fore.YELLOW}Save format (json/txt) [default: json]: {Style.RESET_ALL}").lower() or "json"
        if format_type == 'exit':
            sys.exit(0)
        if format_type not in ["json", "txt"]:
            format_type = "json"
            print(f"{Fore.YELLOW}Invalid format. Using json instead.{Style.RESET_ALL}")
        
        filename = input(f"{Fore.YELLOW}Filename [leave empty for auto-generated]: {Style.RESET_ALL}")
        if filename.lower() == 'exit':
            sys.exit(0)
    else:
        format_type = "json"
        filename = None
    
    # Run the check
    run_check_and_display(check_type, host, nodes, save_to_file, filename, format_type)

# ... (el resto del código se mantiene igual)

def main():
    """Main function to parse command line arguments or start interactive mode."""
    parser = argparse.ArgumentParser(
        description='Check host availability and response times using the Check-Host API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_host.py                             # Start interactive mode
  python check_host.py 1.1.1.1                     # Ping check with all nodes
  python check_host.py google.com --type http      # HTTP check with all nodes
  python check_host.py 1.1.1.1 --nodes EU          # Ping check with European nodes
  python check_host.py example.com --save          # Save results to auto-generated file
  python check_host.py 1.1.1.1 --output ping.json  # Save results to specific file
"""
    )
    
    parser.add_argument('host', nargs='?', help='Host to check (domain or IP)')
    parser.add_argument('--type', choices=['ping', 'http'], default='ping',
                      help='Type of check to perform (default: ping)')
    parser.add_argument('--nodes', default='ALL',
                      help='Nodes to use (ALL, EU, NA, AS, SA, EU+NA)')
    parser.add_argument('--save', action='store_true',
                      help='Save results to file')
    parser.add_argument('--output', help='Output file name')
    parser.add_argument('--format', choices=['json', 'txt'], default='json',
                      help='Output format (default: json)')
    parser.add_argument('--exit', action='store_true',  # Nueva opción
                      help='Exit immediately (for script integration)')
    
    args = parser.parse_args()
    
    if args.exit:  # Salir inmediatamente si se usa --exit
        sys.exit(0)
    
    # ... (resto del main() original)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operación cancelada por el usuario{Style.RESET_ALL}")
        sys.exit(0)
