import subprocess
import os
import threading
import sys
import platform
import shutil

def setup_environment():
    # Add Go binary paths to the current process PATH
    home = os.path.expanduser("~")
    go_paths = [
        os.path.join(home, "go", "bin"),
        os.path.join(home, ".go", "bin"),
        "/usr/local/go/bin",
        "/data/data/com.termux/files/usr/bin"
    ]
    
    current_path = os.environ.get('PATH', '')
    for path in go_paths:
        if os.path.exists(path) and path not in current_path:
            current_path += os.pathsep + path
    
    os.environ['PATH'] = current_path

# UI Colors
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
GREEN = "\033[32m"
CYAN = "\033[96m"
ORANGE = "\033[38;5;208m"

# Lock for thread-safe operations if needed
write_lock = threading.Lock()

def get_files_dir():
    # Returns the 'files' directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path if we are inside 'modules'
    if os.path.basename(current_dir) == 'modules':
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
    
    files_dir = os.path.join(project_root, "files")
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
    return files_dir

def display_banner():
    
    banner = f"""
{BOLD}{CYAN}
  FlashScan-Go Wrapper
  v2.0
{RESET}
    """
    print(banner)

def scan_subdomains_with_flashscan(input_file, output_file, threads):
    # Locate flashscan binary (flashscan-go or flashscan) using PATH
    binary = shutil.which('flashscan-go')
    if not binary:
        binary = shutil.which('flashscan')
    if not binary:
        print(f"\n{BOLD}{RED}[!] Error: flashscan-go/flashscan not installed.{RESET}")
        print(f"{BOLD}{YELLOW}Run: go install github.com/SirYadav1/flashscan-go/v2@latest{RESET}")
        return
    try:
        print(f"{BOLD}{YELLOW}[*] Scanning: {BLUE}{input_file}{RESET}")
        cmd = [
            binary, 'direct',
            '-f', input_file,
            '-o', output_file,
            '-t', str(threads)
        ]
        subprocess.run(cmd, check=True)
        print(f"\n{BOLD}{GREEN}[+] Done! Saved to: {output_file}{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"\n{BOLD}{RED}[!] Scan Error: {e}{RESET}")

def main():
    setup_environment()
    display_banner()
    
    # Get input file
    input_file = input(f"{BOLD}{LIGHT_GREEN}[?] Input File (e.g. subs.txt): {RESET}").strip()
    if not os.path.isfile(input_file):
        print(f"{BOLD}{RED}[!] File not found.{RESET}")
        return

    # Get output filename (default if empty)
    output_filename = input(f"{BOLD}{LIGHT_GREEN}[?] Output File (default: Scanned.txt): {RESET}").strip() or "Scanned.txt"
    output_file = os.path.join(get_files_dir(), output_filename)

    # Get thread count
    threads = input(f"{BOLD}{LIGHT_GREEN}[?] Threads (default: 64): {RESET}").strip() or "64"

    try:
        threads = int(threads)
    except ValueError:
        print(f"{BOLD}{RED}[!] Invalid number. Using 64.{RESET}")
        threads = 64

    scan_subdomains_with_flashscan(input_file, output_file, threads)

    print(f"\n{BOLD}{YELLOW}[SYSTEM] Press Enter to return to menu...{RESET}")
    input()

if __name__ == "__main__":
    main()
