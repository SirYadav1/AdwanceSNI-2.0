#!/usr/bin/env python3
import os
import threading
import asyncio
import random
import aiofiles
import platform
import pytz
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
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

# Debug mode
DEBUG = True

def debug_print(message):
    """Print debug messages if DEBUG is True"""
    if DEBUG:
        print(f"{BOLD}{CYAN}[DEBUG]{RESET} {message}")

def get_user_info_banner():
    try:
        os_info = platform.system()
        
        current_time = datetime.now()
        date_str = current_time.strftime('%Y-%m-%d')
        time_str = current_time.strftime('%H:%M:%S')
        
        try:
            timezone = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Z %z')
            formatted_timezone = timezone[:-2] + ":" + timezone[-2:]
        except:
            formatted_timezone = "IST +05:30"

        country = "India"
        total_width = 36

        color = random.choice(COLORS)
        banner = f"""
    {BOLD}{color}╔{'═' * total_width}╗{RESET}
    {BOLD}{color}║        USER INFORMATION            ║{RESET}
    {BOLD}{color}╠{'═' * total_width}╣{RESET}
    {BOLD}{color}║ OS       : {os_info.ljust(16)}        ║{RESET}
    {BOLD}{color}║ Date     : {date_str.ljust(16)}        ║{RESET}
    {BOLD}{color}║ Time     : {time_str.ljust(16)}        ║{RESET}
    {BOLD}{color}║ Timezone : {formatted_timezone.ljust(16)}        ║{RESET}
    {BOLD}{color}║ Country  : {country.ljust(16)}        ║{RESET}
    {BOLD}{color}╚{'═' * total_width}╝{RESET}
        """
        print(banner)
    except Exception as e:
        debug_print(f"Banner error: {e}")

def show_banner():
    banner = f"""
    ╔══════════════════════════════════╗
    ║  Subdomain Finder & Scanner Tool ║
    ╠══════════════════════════════════╣
    ║ Coded by    : YADAV              ║
    ║ Design by   : SONU               ║
    ║ Telegram    : @SirYadav          ║
    ║ Version     : 2.0.5              ║
    ╚══════════════════════════════════╝
    """
    color = random.choice(COLORS)
    print(f"{BOLD}{color}{banner}{RESET}")
    get_user_info_banner()

def clear_terminal():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_banner()
    except Exception as e:
        print(f"{BOLD}{RED}[WARNING]{RESET} Unable to clear terminal. {e}")

async def read_domains(file_name):
    debug_print(f"Reading domains from: {file_name}")
    try:
        async with aiofiles.open(file_name, 'r') as file:
            domains = await file.readlines()
        return [domain.strip() for domain in domains if domain.strip()]
    except Exception as e:
        print(f"{BOLD}{RED}[ERROR] Failed to read file: {e}{RESET}")
        return []

async def get_subdomains_subfinder(domain, output_file):
    try:
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
            return len(clean_subdomains)
    except Exception as e:
        print(f"{BOLD}{RED}Error fetching subdomains for {BLUE}{domain}: {e}{RESET}")
        return 0

def batch_domains(domains, batch_size=20):
    total_domains = len(domains)
    for i in range(0, total_domains, batch_size):
        yield domains[i:i + batch_size]

def get_output_file_path(input_file, output_filename):
    input_dir = os.path.dirname(os.path.abspath(input_file))
    output_file_path = os.path.join(input_dir, output_filename)
    return output_file_path

async def main():
    clear_terminal()
    
    # Input File
    input_file = input(f"{BOLD}{LIGHT_GREEN}Enter Domain File: {RESET}").strip()
    if not os.path.isfile(input_file):
        print(f"{BOLD}{RED}File not found. Please try again.{RESET}")
        input(f"\n{BOLD}{YELLOW}Press Enter to exit...{RESET}")
        return

    # Output File
    output_filename = input(f"{BOLD}{LIGHT_GREEN}Enter Output file name (default: Subdomains.txt): {RESET}").strip() or "Subdomains.txt"
    output_file = get_output_file_path(input_file, output_filename)
    
    debug_print(f"Output Path: {output_file}")

    # Initialize output file
    try:
        with open(output_file, 'w') as f:
            pass
    except Exception as e:
        print(f"{BOLD}{RED}Cannot create output file: {e}{RESET}")
        input(f"\n{BOLD}{YELLOW}Press Enter to exit...{RESET}")
        return

    domains = await read_domains(input_file)
    total_domains = len(domains)
    
    if total_domains == 0:
        print(f"{BOLD}{RED}No domains found in file.{RESET}")
        input(f"\n{BOLD}{YELLOW}Press Enter to exit...{RESET}")
        return

    total_subdomains = 0
    debug_print(f"Starting scan for {total_domains} domains")
    
    try:
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[progress.percentage]{task.completed}/{task.total} Domains"),
        ) as progress:
            task = progress.add_task("[cyan]Processing Domains...", total=total_domains)
            
            with ProcessPoolExecutor(max_workers=5) as executor:
                for domain_batch in batch_domains(domains, batch_size=5):
                    tasks = [get_subdomains_subfinder(domain, output_file) for domain in domain_batch]
                    results = await asyncio.gather(*tasks)
                    total_subdomains += sum(results)
                    progress.update(task, advance=len(domain_batch))
        
        print(f"\n{BOLD}{LIGHT_GREEN}Subdomains have been saved in {output_file}.{RESET}")
        print(f"{BOLD}{GREEN}Total Subdomains Found: {total_subdomains}{RESET}")
        
    except Exception as e:
        print(f"{BOLD}{RED}Fatal Error During Scan: {e}{RESET}")
        debug_print(f"Exception: {e}")

    # CRITICAL: Pause before returning to menu
    input(f"\n{BOLD}{YELLOW}Scan complete. Press Enter to exit and return to menu...{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{BOLD}{RED}Interrupted by user.{RESET}")
    except Exception as e:
        print(f"\n{BOLD}{RED}Unexpected error: {e}{RESET}")
        input(f"\n{BOLD}{YELLOW}Press Enter to exit...{RESET}")
