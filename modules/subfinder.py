#!/usr/bin/env python3
import subprocess
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    import psutil
except ImportError:
    psutil = None

# Colors
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

write_lock = threading.Lock()

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def get_optimal_config():
    """Dynamically calculate convenient worker count based on RAM."""
    try:
        ram_gb = psutil.virtual_memory().total / (1024**3) if psutil else 3
    except:
        ram_gb = 2 # Conservative default
    
    if ram_gb < 2:
        return 2, "Safe Mode (Low RAM)"
    elif ram_gb < 4:
        return 5, "Balanced Mode"
    elif ram_gb < 8:
        return 15, "Performance Mode"
    else:
        return 30, "Ultra Mode"

def scan_target(domain, output_file):
    """Scan a single target and append results thread-safely."""
    try:
        cmd = ["subfinder", "-d", domain, "-silent"]
        # Use simple subprocess, thread-safe due to OS isolation
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode == 0 and result.stdout:
            subs = [s.strip() for s in result.stdout.split('\n') if s.strip()]
            if subs:
                with write_lock:
                    with open(output_file, 'a') as f:
                        for s in subs:
                            f.write(s + '\n')
                return len(subs)
    except Exception:
        pass
    return 0

def main():
    clear()
    print(f"{BOLD}{CYAN}=== SUBFINDER (SMART PARALLEL) ==={RESET}")
    
    # 1. Input
    try:
        input_file = input(f"{YELLOW}[?] Enter Domain File: {RESET}").strip()
    except EOFError:
        return

    if not os.path.isfile(input_file):
        print(f"{RED}[!] File not found.{RESET}")
        time.sleep(2)
        return

    # 2. Output
    try:
        output_name = input(f"{YELLOW}[?] Enter Output Name: {RESET}").strip()
    except EOFError:
        return
        
    try:
        input_dir = os.path.dirname(os.path.abspath(input_file))
        output_file = os.path.join(input_dir, output_name)
    except:
        output_file = output_name

    # 3. Read & Config
    print(f"\n{CYAN}[*] Reading domains...{RESET}")
    try:
        with open(input_file, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
    except Exception:
        print(f"{RED}[!] Error reading file.{RESET}")
        return

    if not domains:
        print(f"{RED}[!] Empty file.{RESET}")
        return

    workers, mode_name = get_optimal_config()
    print(f"{GREEN}[*] System Analysis: {mode_name} | Threads: {workers}{RESET}")
    print(f"{GREEN}[*] Loaded {len(domains)} domains.{RESET}")
    time.sleep(1)

    print(f"\n{BOLD}Starting Scan...{RESET}")
    
    total = len(domains)
    completed = 0
    found_total = 0
    
    # 4. Parallel Execution
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_target, d, output_file): d for d in domains}
        
        for future in as_completed(futures):
            completed += 1
            domain = futures[future]
            try:
                count = future.result()
                found_total += count
                if count > 0:
                    print(f"{GREEN}[{completed}/{total}] {domain} -> Found {count}{RESET}")
                else:
                    print(f"{YELLOW}[{completed}/{total}] {domain} -> 0{RESET}")
            except:
                print(f"{RED}[{completed}/{total}] {domain} -> Error{RESET}")

    print(f"\n{BOLD}{GREEN}=== FINISHED ==={RESET}")
    print(f"{BOLD}Total Subdomains: {found_total}{RESET}")
    print(f"{BOLD}Saved to: {output_file}{RESET}")
    
    print(f"\n{BOLD}{YELLOW}[SYSTEM] Press Enter to return to menu...{RESET}")
    input() # Pause is critical

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter...")
