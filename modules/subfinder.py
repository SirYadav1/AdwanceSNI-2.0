#!/usr/bin/env python3
import subprocess
import os
import threading
import asyncio
import random
import aiofiles
import platform
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
try:
    import psutil
except ImportError:
    psutil = None
import pytz
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# Color definitions
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

COLORS = [LIGHT_GREEN, RED, BLUE, YELLOW, GREEN, PURPLE, CYAN, WHITE, ORANGE, PINK]

write_lock = threading.Lock()

def show_banner():
    banner = """
    ****************************************************
╭━━━┳╮╱╭┳━━╮╭━━━┳━━┳━╮╱╭┳━━━┳━━━┳━━━╮
┃╭━╮┃┃╱┃┃╭╮┃┃╭━━┻┫┣┫┃╰╮┃┣╮╭╮┃╭━━┫╭━╮┃
┃╰━━┫┃╱┃┃╰╯╰┫╰━━╮┃┃┃╭╮╰╯┃┃┃┃┃╰━━┫╰━╯┃
╰━━╮┃┃╱┃┃╭━╮┃╭━━╯┃┃┃┃╰╮┃┃┃┃┃┃╭━━┫╭╮╭╯
┃╰━╯┃╰━╯┃╰━╯┃┃╱╱╭┫┣┫┃╱┃┃┣╯╰╯┃╰━━┫┃┃╰╮
╰━━━┻━━━┻━━━┻╯╱╱╰━━┻╯╱╰━┻━━━┻━━━┻╯╰━╯
    ****************************************************
    """
    print(f"{BOLD}{CYAN}{banner}{RESET}")
    print(f"{BOLD}{GREEN}Fastest Subdomains Finder{RESET}")

def print_banner():
    print(f"{BOLD}{CYAN}╔═══════════════════════════════╗{RESET}")
    print(f"{BOLD}{LIGHT_GREEN}║ System Resources Detected:    ║{RESET}")
    
    cpu_cores = os.cpu_count() or 2
    print(f"{BOLD}{YELLOW}║   - CPU Cores: {cpu_cores}              ║{RESET}")
    
    try:
        memory = psutil.virtual_memory().total / (1024**3) if psutil else 4.0
        print(f"{BOLD}{GREEN}║   - Memory: {memory:.2f} GB           ║{RESET}")
    except:
        print(f"{BOLD}{GREEN}║   - Memory: Unknown             ║{RESET}")

    print(f"{BOLD}{PURPLE}║ Optimized Configuration:      ║{RESET}")
    print(f"{BOLD}{BLUE}║   - Workers: 5                ║{RESET}")
    print(f"{BOLD}{RED}║   - Batch Size: 5             ║{RESET}")
    print(f"{BOLD}{CYAN}╚═══════════════════════════════╝{RESET}")

def get_system_resources():
    cpu_count = os.cpu_count() or 2
    try:
        memory = psutil.virtual_memory().total / (1024**3) if psutil else 4.0
    except:
        memory = 4.0
    return cpu_count, memory

def calculate_optimal_config(cpu_count, memory):
    workers = min(cpu_count * 2, 15)
    if memory < 4:
        workers = min(workers, 5)
    batch_size = 5 if memory < 4 else 10
    return workers, batch_size

async def read_domains(file_name):
    async with aiofiles.open(file_name, 'r') as file:
        domains = await file.readlines()
    return [domain.strip() for domain in domains if domain.strip()]

async def get_subdomains_subfinder(domain, output_file):
    try:
        print(f"{BOLD}{YELLOW}Fetching subdomains for: {BLUE}{domain}{RESET}")
        process = await asyncio.create_subprocess_exec(
            'subfinder', '-d', domain, '-silent',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            print(f"{BOLD}{RED}Error fetching subdomains for {domain}: {stderr.decode()}{RESET}")
            return 0
        else:
            subdomains = stdout.decode().splitlines()
            clean_subdomains = [line.strip() for line in subdomains if line.strip()]
            with write_lock:
                with open(output_file, 'a') as out_file:
                    for subdomain in clean_subdomains:
                        out_file.write(f"{subdomain}\n")
            print(f"{BOLD}{GREEN}Subdomains saved for: {domain}{RESET}")
            return len(clean_subdomains)
    except Exception as e:
        print(f"{BOLD}{RED}Error fetching subdomains for {domain}: {e}{RESET}")
        return 0

def batch_domains(domains, batch_size=20):
    total_domains = len(domains)
    for i in range(0, total_domains, batch_size):
        yield domains[i:i + batch_size]

def get_output_file_path(input_file, output_filename):
    input_dir = os.path.dirname(input_file)
    output_file_path = os.path.join(input_dir, output_filename)
    return output_file_path

async def main():
    print_banner()
    cpu_count, memory = get_system_resources()
    workers, batch_size = calculate_optimal_config(cpu_count, memory)

    # Use 5 workers default if psutil check failed logic
    if not psutil:
        workers = 5
        batch_size = 5

    input_file = input(f"{BOLD}{LIGHT_GREEN}Enter Domain File: {RESET}").strip()
    if not os.path.isfile(input_file):
        print(f"{BOLD}{RED}File not found. Please try again.{RESET}")
        return

    output_filename = input(f"{BOLD}{LIGHT_GREEN}Enter Output file name to Save Subdomain: {RESET}").strip()
    output_file = get_output_file_path(input_file, output_filename)

    with open(output_file, 'w') as f:
        pass

    domains = await read_domains(input_file)
    total_domains = len(domains)
    
    if total_domains == 0:
        print(f"{BOLD}{RED}No domains in file.{RESET}")
        return

    total_subdomains = 0
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("[progress.percentage]{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("[cyan]Processing Domains...", total=total_domains)
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for domain_batch in batch_domains(domains, batch_size):
                tasks = [get_subdomains_subfinder(domain, output_file) for domain in domain_batch]
                results = await asyncio.gather(*tasks)
                total_subdomains += sum(results)
                progress.update(task, advance=len(domain_batch))
    print(f"{BOLD}{LIGHT_GREEN}Subdomains have been saved in {output_file}.{RESET}")
    print(f"{BOLD}{GREEN}Total Subdomains Found: {total_subdomains}{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        input(f"\n{BOLD}{YELLOW}[SYSTEM] Press Enter to return to menu...{RESET}")
