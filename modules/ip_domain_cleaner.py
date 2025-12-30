import os
import re
from colorama import Fore, Style, init

init(autoreset=True)

BOLD = "\033[1m"

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

def ask(msg):
    return input(f"{Fore.GREEN}{msg}{Style.RESET_ALL}: ").strip()

def process_text(file_location, destination_name):
    try:
        with open(file_location, 'r') as source:
            lines = source.readlines()
    except Exception as e:
        print(Fore.RED + f"Error reading file: {e}")
        return

    print(Fore.CYAN + "Processing...")


    domain_regex = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')
    ip_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    domains, ips = set(), set()

    for line in lines:
        domains.update(domain_regex.findall(line))
        ips.update(ip_regex.findall(line))

    if not domains and not ips:
        print(Fore.YELLOW + "No IP or Domain found.")
        return

    
    if not destination_name.endswith('.txt'):
        destination_name += ".txt"
    final_path = os.path.join(get_files_dir(), destination_name)

    try:
        with open(final_path, 'w') as target:
            if domains:
                target.write('\n'.join(sorted(domains)) + "\n\n")
            if ips:
                target.write('\n'.join(sorted(ips)) + "\n")
        
        print(Fore.GREEN + f"✔ Saved to: {final_path}")
        print(f"  - Domains: {len(domains)}")
        print(f"  - IPs: {len(ips)}\n")

    except Exception as e:
        print(Fore.RED + f"Write Error: {e}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + BOLD + "AdwanceSNI - Extractor" + Style.RESET_ALL)
    
    path = ask("Input File Path")
    if not os.path.exists(path):
        print(Fore.RED + "File not found.")
        return
    
    out_name = ask("Output Filename (default: result.txt)") or "result.txt"
    
    process_text(path, out_name)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
