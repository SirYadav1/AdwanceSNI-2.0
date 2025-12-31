import subprocess
import os
import threading
import asyncio
import random
import aiofiles
import platform
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
import psutil
import pytz
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# --- UI COLORS (NEW UI) ---
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
SKY_BLUE = "\033[1;36m"
YELLOW = "\033[93m"
GREEN = "\033[32m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
ORANGE = "\033[38;5;208m"
PINK = "\033[38;5;206m"

# Thread lock for safe file writing
write_lock = threading.Lock()

def get_files_dir():
    # Returns the path to the 'files' directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == 'modules':
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
    
    files_dir = os.path.join(project_root, "files")
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
    return files_dir

# --- BANNER (NEW UI) ---
def print_banner():
    print(f"{BOLD}{CYAN}╔═══════════════════════════════╗{RESET}")
    print(f"{BOLD}{LIGHT_GREEN}║ System Stats:                 ║{RESET}")
    print(f"{BOLD}{YELLOW}║   - CPU: {os.cpu_count()} Cores               ║{RESET}")
    memory = psutil.virtual_memory().total / (1024**3)  # GB
    print(f"{BOLD}{GREEN}║   - RAM: {memory:.2f} GB              ║{RESET}")
    print(f"{BOLD}{PURPLE}║ Config:                       ║{RESET}")
    print(f"{BOLD}{BLUE}║   - Workers: 5                ║{RESET}")
    print(f"{BOLD}{RED}║   - Batch: 5                  ║{RESET}")
    print(f"{BOLD}{CYAN}╚═══════════════════════════════╝{RESET}")

def get_system_resources():
    # Checks CPU and Memory
    cpu_count = os.cpu_count() or 2
    memory = psutil.virtual_memory().total / (1024**3)
    return cpu_count, memory

def calculate_optimal_config(cpu_count, memory):
    # Adjust performance based on system specs
    workers = min(cpu_count * 2, 15)
    if memory < 4:
        workers = min(workers, 5)
    batch_size = 5 if memory < 4 else 10
    return workers, batch_size

async def read_domains(file_name):
    # Reads domains from  file 
    async with aiofiles.open(file_name, 'r') as file:
        domains = await file.readlines()
    return [domain.strip() for domain in domains]

# --- OLD LOGIC (No Binary Path Argument) ---
async def get_subdomains_subfinder(domain, output_file):
    # Runs subfinder for  single domain - REVERTED TO OLD LOGIC
    try:
        print(f"{BOLD}{YELLOW}[*] Fetching: {BLUE}{domain}{RESET}")
        # OLD LOGIC: Direct call to 'subfinder' without path resolution
        process = await asyncio.create_subprocess_exec(
            'subfinder', '-d', domain, '-silent',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"{BOLD}{RED}[!] Error: {stderr.decode()}{RESET}")
            return 0
        else:
            subdomains = stdout.decode().splitlines()
            clean_subdomains = [line.strip() for line in subdomains if line.strip()]
            
            # Save results thread-safely
            with write_lock:
                with open(output_file, 'a') as out_file:
                    for subdomain in clean_subdomains:
                        out_file.write(f"{subdomain}\n")
            
            print(f"{BOLD}{GREEN}[+] Saved results for: {domain}{RESET}")
            return len(clean_subdomains)
    except Exception as e:
        print(f"{BOLD}{RED}[!] Exception: {e}{RESET}")
        return 0

def batch_domains(domains, batch_size=20):
    # Generator for domain batches
    total_domains = len(domains)
    for i in range(0, total_domains, batch_size):
        yield domains[i:i + batch_size]

async def main():
    # --- NO setup_environment() CALL HERE ---
    print_banner()
    cpu_count, memory = get_system_resources()
    workers, batch_size = calculate_optimal_config(cpu_count, memory)

    # --- NO Binary Resolution Logic Here ---

    # Get Input File
    input_file = input(f"{BOLD}{LIGHT_GREEN}[?] Domain File: {RESET}").strip()
    if not os.path.isfile(input_file):
        print(f"{BOLD}{RED}[!] File not found.{RESET}")
        return

    # Get Output File
    output_filename = input(f"{BOLD}{LIGHT_GREEN}[?] Output Filename (default: Subfinder_Results.txt): {RESET}").strip() or "Subfinder_Results.txt"
    output_file = os.path.join(get_files_dir(), output_filename)

    # Initialize output file
    with open(output_file, 'w') as f:
        pass

    domains = await read_domains(input_file)
    total_domains = len(domains)
    total_subdomains = 0
    
    # Show progress bar (NEW UI)
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("[progress.percentage]{task.completed}/{task.total} Domains"),
    ) as progress:
        task = progress.add_task("[cyan]Scanning...", total=total_domains)
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for domain_batch in batch_domains(domains, batch_size):
                # Call without binary_path
                tasks = [get_subdomains_subfinder(domain, output_file) for domain in domain_batch]
                results = await asyncio.gather(*tasks)
                total_subdomains += sum(results)
                progress.update(task, advance=len(domain_batch))
                
    print(f"{BOLD}{LIGHT_GREEN}[+] Saved to: {output_file}{RESET}")
    print(f"{BOLD}{GREEN}[+] Total Subdomains: {total_subdomains}{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
