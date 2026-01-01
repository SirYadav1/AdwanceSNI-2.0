#!/usr/bin/env python3
import subprocess
import os
import time

# Colors
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    clear()
    print(f"{BOLD}{CYAN}=== SUBFINDER ==={RESET}")
    
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

    # 3. Read
    print(f"\n{CYAN}[*] Reading domains...{RESET}")
    try:
        with open(input_file, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[!] Error reading file: {e}{RESET}")
        input("Press Enter...")
        return

    if not domains:
        print(f"{RED}[!] No domains found in file.{RESET}")
        time.sleep(2)
        return

    print(f"{GREEN}[+] Found {len(domains)} domains. Starting scan...{RESET}")
    time.sleep(1)

    # 4. Scan
    count = 0
    total = len(domains)
    
    for i, domain in enumerate(domains, 1):
        print(f"\n{YELLOW}[{i}/{total}] Scanning: {domain}{RESET}")
        try:
            cmd = ["subfinder", "-d", domain, "-silent"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode == 0 and result.stdout:
                subs = [s.strip() for s in result.stdout.split('\n') if s.strip()]
                if subs:
                    with open(output_file, 'a') as f:
                        for s in subs:
                            f.write(s + '\n')
                    print(f"{GREEN}    -> Found: {len(subs)}{RESET}")
                    count += len(subs)
                else:
                    print(f"{RED}    -> No results{RESET}")
            else:
                 print(f"{RED}    -> No results{RESET}")

        except Exception as e:
            print(f"{RED}    -> Error: {e}{RESET}")
    
    print(f"\n{BOLD}{GREEN}=== SCAN COMPLETED ==={RESET}")
    print(f"{BOLD}Total Subdomains: {count}{RESET}")
    print(f"{BOLD}Saved to: {output_file}{RESET}")
    
    print(f"\n{BOLD}{YELLOW}[SYSTEM] Press Enter to return to menu...{RESET}")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter...")
