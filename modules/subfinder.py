#!/usr/bin/env python3
import subprocess
import os
import platform
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
    print(f"{BOLD}{CYAN}=== SUBFINDER (STABLE MODE) ==={RESET}")
    
    # 1. Input
    try:
        input_file = input(f"{YELLOW}Enter Domain File: {RESET}").strip()
    except EOFError:
        print("Input Error (EOF).")
        return

    if not os.path.isfile(input_file):
        print(f"{RED}File not found.{RESET}")
        time.sleep(2)
        return

    # 2. Output
    try:
        output_name = input(f"{YELLOW}Enter Output Name: {RESET}").strip()
    except EOFError:
        return
        
    output_file = os.path.join(os.path.dirname(os.path.abspath(input_file)), output_name)

    # 3. Read
    print(f"{CYAN}Reading domains...{RESET}")
    try:
        with open(input_file, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}Error reading file: {e}{RESET}")
        input("Press Enter...")
        return

    print(f"{GREEN}Found {len(domains)} domains. Starting scan...{RESET}")
    time.sleep(1)

    # 4. Scan (Sequential)
    count = 0
    for domain in domains:
        print(f"\n{YELLOW}>> Scanning: {domain}{RESET}")
        try:
            # Direct subprocess writing to file via appending in python
            # Use 'subfinder' command directly
            cmd = ["subfinder", "-d", domain, "-silent"]
            
            # Run
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode == 0 and result.stdout:
                subs = result.stdout.strip().split('\n')
                valid_subs = [s for s in subs if s.strip()]
                if valid_subs:
                    with open(output_file, 'a') as f:
                        for s in valid_subs:
                            f.write(s + '\n')
                    print(f"{GREEN}[+] Found {len(valid_subs)} subdomains{RESET}")
                    count += len(valid_subs)
                else:
                    print(f"{RED}[-] No results{RESET}")
            else:
                 print(f"{RED}[-] Failed or No Output{RESET}")
                 if result.stderr:
                     print(f"Error: {result.stderr.strip()}")

        except Exception as e:
            print(f"{RED}Error scanning {domain}: {e}{RESET}")
    
    print(f"\n{BOLD}{GREEN}=== COMPLETED ==={RESET}")
    print(f"Total Subdomains: {count}")
    print(f"Saved to: {output_file}")
    
    # FINAL PAUSE
    print(f"\n{BOLD}{YELLOW}[SYSTEM] Press Enter to return to menu...{RESET}")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press Enter...")
