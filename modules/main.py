import subprocess
import os
import random
import platform
from datetime import datetime
import pytz
import sys


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

# List of colors for random selection
COLORS = [LIGHT_GREEN, RED, BLUE, YELLOW, GREEN, PURPLE, CYAN, WHITE, ORANGE, PINK]

def get_user_info_banner():
    # Gather system information
    os_info = platform.system()
    
    #current time and date
    current_time = datetime.now()
    date_str = current_time.strftime('%Y-%m-%d')
    time_str = current_time.strftime('%H:%M:%S')
    
    # Set timezone to India (Asia/Kolkata)
    timezone = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Z %z')
    formatted_timezone = timezone[:-2] + ":" + timezone[-2:]

    country = "India"
    
   
    color = random.choice(COLORS)
    banner = f"""
    {BOLD}{color}**************************************************{RESET}
    {BOLD}{color}*               USER INFORMATION                 *{RESET}
    {BOLD}{color}**************************************************{RESET}
    {BOLD}{color}* OS       : {os_info.ljust(16)}                   *{RESET}
    {BOLD}{color}* Date     : {date_str.ljust(16)}                    *{RESET}
    {BOLD}{color}* Time     : {time_str.ljust(16)}                    *{RESET}
    {BOLD}{color}* Timezone : {formatted_timezone.ljust(16)}                   *{RESET}
    {BOLD}{color}* Country  : {country.ljust(16)}                    *{RESET}
    {BOLD}{color}**************************************************{RESET}
    """
    print(banner)

def show_banner():
    
    banner = f"""
    **************************************************
    *                                                *
    *            AdwanceSNI - Main Menu              *
    *                  Version: 2.0.4                *
    *           Last Updated: 30 Dec 2025            *
    *                                                *
    **************************************************
    """
    color = random.choice(COLORS)
    print(f"{BOLD}{color}{banner}{RESET}")
    get_user_info_banner()

def clear_terminal():
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_banner()
    except Exception as e:
        print(f"{BOLD}{RED}[!] Clear failed: {e}{RESET}")

def show_menu():
    
    menu = f"""
    {BOLD}{LIGHT_GREEN}=============================={RESET}
    {BOLD}{YELLOW}[1]{RESET} - Find Subdomains
    {BOLD}{YELLOW}[2]{RESET} - Scan Hosts
    {BOLD}{YELLOW}[3]{RESET} - Extract IP/Domain
    {BOLD}{YELLOW}[4]{RESET} - Generate IPs
    {BOLD}{YELLOW}[5]{RESET} - Update Tool
    {BOLD}{YELLOW}[6]{RESET} - Split Files
    {BOLD}{YELLOW}[7]{RESET} - Help
    {BOLD}{RED}[8]{RESET} - Exit
    {BOLD}{LIGHT_GREEN}=============================={RESET}
    """
    print(menu)

def show_subdomain_menu():
    # Subdomain  options
    menu = f"""
    {BOLD}{LIGHT_GREEN}=============================={RESET}
    {BOLD}{YELLOW}[1]{RESET} - Use Subfinder (Fast)
    {BOLD}{YELLOW}[2]{RESET} - Use API Scanner (Deep)
    {BOLD}{LIGHT_GREEN}=============================={RESET}
    """
    print(menu)

def show_scan_host_menu():
    # Scanner options
    menu = f"""
    {BOLD}{LIGHT_GREEN}=============================={RESET}
    {BOLD}{YELLOW}[1]{RESET} - FlashScan (Recommended)
    {BOLD}{YELLOW}[2]{RESET} - Normal Scanner (Standard)
    {BOLD}{LIGHT_GREEN}=============================={RESET}
    """
    print(menu)

def update_scripts():
   
    clear_terminal()
    try:
        print(f"{BOLD}{BLUE}[*] Updating...{RESET}")
        command = "cd .. && git fetch --all && git reset --hard origin/main && git log -1"
        subprocess.run(command, shell=True, check=True)
        print(f"{BOLD}{GREEN}[+] Updated successfully!{RESET}")
    except subprocess.CalledProcessError:
        print(f"{BOLD}{RED}[!] Update failed.{RESET}")
    except Exception as e:
        print(f"{BOLD}{RED}[!] Error: {e}{RESET}")

def help_module():
   
    clear_terminal()
    try:
        print(f"{BOLD}{GREEN}[*] Opening help...{RESET}")
        subprocess.run(["bash", "help.sh"], check=True)
    except Exception as e:
        print(f"{BOLD}{RED}[!] Failed to open help: {e}{RESET}")

def main():
    # Main program loop
    clear_terminal()
    while True:
        show_menu()
        choice = input(f"{BOLD}{SKY_BLUE}Option (1-8): {RESET}").strip()

        if choice == "1":
            clear_terminal()
            show_subdomain_menu()
            sub_choice = input(f"{BOLD}{SKY_BLUE}Select (1-2): {RESET}").strip()

            if sub_choice == "1":
                clear_terminal()
                subprocess.run([sys.executable, "subfinder.py"])
            elif sub_choice == "2":
                clear_terminal()
                subprocess.run([sys.executable, "api_subd.py"])
            else:
                print(f"{BOLD}{RED}[!] Invalid choice.{RESET}")

        elif choice == "2":
            clear_terminal()
            show_scan_host_menu()
            sub_choice = input(f"{BOLD}{SKY_BLUE}Select (1-2): {RESET}").strip()

            if sub_choice == "1":
                clear_terminal()
                # Runs the FlashScan 
                subprocess.run([sys.executable, "flashscan_scanner.py"])
            elif sub_choice == "2":
                clear_terminal()
                subprocess.run([sys.executable, "normal_scanner.py"])
            else:
                print(f"{BOLD}{RED}[!] Invalid choice.{RESET}")

        elif choice == "3":
            clear_terminal()
            subprocess.run([sys.executable, "ip_domain_cleaner.py"])

        elif choice == "4":
            clear_terminal()
            subprocess.run([sys.executable, "ip_generator.py"])

        elif choice == "5":
            update_scripts()

        elif choice == "6":
            clear_terminal()
            subprocess.run([sys.executable, "file_splitter.py"])

        elif choice == "7":
            help_module()

        elif choice == "8":
            clear_terminal()
            print(f"{BOLD}{RED}Bye!{RESET}")
            break

        else:
            print(f"{BOLD}{RED}[!] Invalid option.{RESET}")

if __name__ == "__main__":
    main()
