import os
import ipaddress
import random
from tqdm import tqdm
import logging
import subprocess


logging.basicConfig(filename='ip_generator.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def log_event(message):
    logging.info(message)

def get_files_dir():
    # Returns 'files' directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == 'modules':
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
    
    files_dir = os.path.join(project_root, "files")
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
    return files_dir

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner = r"""
   IP Generator
    """
    print(f"\033[1;36m{banner}\033[0m")

def save_ips_to_file(ip_list, file_name):
    try:
        directory = os.path.dirname(file_name)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_name, "w") as f:
            for ip in ip_list:
                f.write(f"{ip}\n")
        print(f"\033[1;32m[+] Saved IPs to {file_name}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Error writing file: {e}\033[0m")

def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False

def get_valid_ip(prompt):
    # Loops until valid IP is entered
    while True:
        ip = input(prompt)
        if is_valid_ip(ip):
            return ip
        else:
            print("\033[1;31mInvalid IP. Try again.\033[0m")

def generate_ips_from_range(start_ip, end_ip, file_name):
    # Generates IP list between start and end
    try:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)

        if start > end:
            print("\033[1;31mStart IP must be smaller than End IP.\033[0m")
            return

        ip_list = [ipaddress.IPv4Address(ip) for ip in range(int(start), int(end) + 1)]
        total_ips = len(ip_list)
        print(f"\033[1;34mGenerating {total_ips} IPs...\033[0m")

        with tqdm(total=total_ips, desc="Progress", ncols=75) as pbar:
            save_ips_to_file(ip_list, file_name)
            pbar.update(total_ips)
    except Exception as e:
        print(f"\033[1;31mError: {e}\033[0m")

def generate_ips_from_cidr(cidr, file_name):
    # Generates IPs from CIDR 
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
        total_ips = len(ip_list)
        print(f"\033[1;34mGenerating IPs from CIDR...\033[0m")

        with tqdm(total=total_ips, desc="Progress", ncols=75) as pbar:
            save_ips_to_file(ip_list, file_name)
            pbar.update(total_ips)
    except Exception as e:
        print(f"\033[1;31mError: {e}\033[0m")

def parse_file_for_cidr(file_name, output_file):
    # Reads CIDRs from file and generates IPs
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if '/' in line:
                generate_ips_from_cidr(line, output_file)
    except FileNotFoundError:
        print(f"\033[1;31mFile not found.\033[0m")

def main():
    while True:
        clear_terminal()
        display_banner()
        print("\n\033[1;34mOptions:\033[0m")
        print("1. Range (Start IP - End IP)")
        print("2. CIDR (e.g., 10.0.0.0/24)")
        print("3. File with CIDRs")
        print("4. Back to Main Menu")
        choice = input("\033[1;34mSelection: \033[0m")

        if choice == "1":
            start_ip = get_valid_ip("Start IP: ")
            end_ip = get_valid_ip("End IP: ")
            out_name = input("Output Filename (default: Range_IPs.txt): ").strip() or "Range_IPs.txt"
            file_name = os.path.join(get_files_dir(), out_name)
            generate_ips_from_range(start_ip, end_ip, file_name)

        elif choice == "2":
            cidr = input("CIDR: ")
            out_name = input("Output Filename (default: CIDR_IPs.txt): ").strip() or "CIDR_IPs.txt"
            file_name = os.path.join(get_files_dir(), out_name)
            generate_ips_from_cidr(cidr, file_name)

        elif choice == "3":
            file_name = input("Input File Path: ")
            out_name = input("Output Filename (default: File_IPs.txt): ").strip() or "File_IPs.txt"
            output_file = os.path.join(get_files_dir(), out_name)
            parse_file_for_cidr(file_name, output_file)

        elif choice == "4":
             break

        else:
            print("\033[1;31mInvalid option.\033[0m")
            input("Press Enter...")

if __name__ == "__main__":
    main()