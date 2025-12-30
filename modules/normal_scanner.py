from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from pathlib import Path
import socket
import threading
import time
from colorama import Fore, Style
import requests


DEFAULT_TIMEOUT = 5
# Locations to handle as false positives
EXCLUDE_LOCATIONS = ["https://jio.com/BalanceExhaust", "http://filter.ncell.com.np/nc"]


file_write_lock = threading.Lock()

def get_files_dir():
    # Returns the 'files' directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == 'modules':
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
    
    files_dir = os.path.join(project_root, "files")
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
    return files_dir

def get_input(prompt, default=None):
   
    user_input = input(prompt).strip()
    return user_input if user_input else default

def clear_screen():
  
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hosts_from_file(file_path):
    # Reads hosts from file, ignoring empty lines
    path = Path(file_path)
    if path.is_file():
        try:
            return [line.strip() for line in path.read_text().splitlines() if line.strip()]
        except Exception:
            print(Fore.RED + f"Error reading file.")
    return []

def get_http_method():
    # Asks user for HTTP method
    methods = ['GET', 'POST', 'HEAD']
    print(Fore.CYAN + "\nMethods: " + ", ".join(methods))
    method = get_input(Fore.YELLOW + " » Select Method (default: GET): " + Fore.RESET, "GET").upper()
    return method if method in methods else "GET"

def format_row(code, server, port, ip_address, host, use_colors=True):
    # Formats the result row
    bold = "\033[1m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""
    
    return (f"{bold}{Fore.GREEN if use_colors else ''}{code:<4}{reset} " +
            f"{bold}{Fore.CYAN if use_colors else ''}{server:<20}{reset} " +
            f"{bold}{Fore.YELLOW if use_colors else ''}{port:<5}{reset} " +
            f"{bold}{Fore.MAGENTA if use_colors else ''}{ip_address:<15}{reset} " +
            f"{bold}{Fore.LIGHTBLUE_EX if use_colors else ''}{host}{reset}")

def check_http_response(host, port, method):
    # Performs the HTTP request
    url = f"{'https' if port in ['443', '8443'] else 'http'}://{host}:{port}"
    try:
        response = requests.request(method, url, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
        # Check against exclude list
        if any(exclude in response.headers.get('Location', '') for exclude in EXCLUDE_LOCATIONS):
            return None
            
        status_code = response.status_code
        server_header = response.headers.get('Server', 'N/A')
        ip_address = get_ip_from_host(host) or 'N/A'
        return (status_code, server_header, port, ip_address, host)
    except requests.exceptions.RequestException:
        return None

def get_ip_from_host(host):
    # Resolves hostname to IP
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return "N/A"

def format_time(elapsed_time):
    # Formats seconds into M m S s
    return f"{int(elapsed_time // 60)}m {int(elapsed_time % 60)}s" if elapsed_time >= 60 else f"{elapsed_time:.2f}s"

def perform_scan(hosts, ports, output_file, threads, method):
    clear_screen()
    print(Fore.GREEN + f"Scanning ({method})...")

    headers = (Fore.GREEN + "Code  " + Fore.CYAN + "Server               " +
              Fore.YELLOW + "Port   " + Fore.MAGENTA + "IP Address     " + Fore.LIGHTBLUE_EX + "Host" + Style.RESET_ALL)
    separator = "-" * 65

    # Write headers to file
    try:
        with open(output_file, 'a') as file:
            file.write(f"Code  Server               Port   IP Address     Host\n{separator}\n")
    except Exception:
        pass

    print(headers, separator, sep='\n')

    start_time = time.time()
    total_hosts, scanned_hosts, responded_hosts = len(hosts) * len(ports), 0, 0

    # Start ThreadPool
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_http_response, host, port, method) for host in hosts for port in ports]
        for future in as_completed(futures):
            scanned_hosts += 1
            try:
                result = future.result(timeout=DEFAULT_TIMEOUT + 1)
                if result:
                    responded_hosts += 1
                    row = format_row(*result)
                    print(row)
                    with file_write_lock:
                        with open(output_file, 'a') as file:
                            file.write(format_row(*result, use_colors=False) + "\n")
            except Exception:
                pass

            elapsed_time = time.time() - start_time
            print(f"Progress: {scanned_hosts}/{total_hosts} | Found: {responded_hosts} | Time: {format_time(elapsed_time)}", end='\r')

    print(f"\n\n{Fore.GREEN}[+] Scan Complete! {responded_hosts} responsive.")
    print(f"{Fore.GREEN}[+] Saved to: {output_file}{Style.RESET_ALL}")

def main():
    # Input File
    file_path = get_input(Fore.GREEN + "» Host File Path: " + Fore.YELLOW, "/storage/emulated/0/domain.txt")
    hosts = get_hosts_from_file(file_path)
    if not hosts:
        print(Fore.RED + "No hosts found.")
        return

    #Ports
    ports_input = get_input(Fore.GREEN + "» Ports (default: 80): " + Fore.YELLOW, "80").strip()
    ports = [port.strip() for port in ports_input.split(',')] if ports_input else ["80"]

    #Output File
    out_name = get_input(Fore.GREEN + "» Output Filename: " + Fore.YELLOW, "scan_results.txt")
    output_file_path = os.path.join(get_files_dir(), out_name)

    #Threads
    threads = int(get_input(Fore.GREEN + "» Threads (default: 50): " + Fore.YELLOW, "50") or "50")
    
    #Method
    http_method = get_http_method()

    perform_scan(hosts, ports, output_file_path, threads, http_method)

if __name__ == "__main__":
    main()
