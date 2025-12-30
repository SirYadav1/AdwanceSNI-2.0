import os

# Terminal Colors
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
BOLD = '\033[1m'
RESET = '\033[0m'

CONFIG_FILE = os.path.expanduser("~/.domainsplitter_config")

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

def print_banner():
    # Clears screen and prints header
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
    print(f"{BLUE}{BOLD}")
    print("AdwanceSNI - File Splitter")
    print(f"{RESET}")

def get_file_path():
    # Asks user for file path
    print(f"{YELLOW}Input File:{RESET}")
    return input("» Path: ")

def check_file(file_path):
    # Validates file existence
    if os.path.isfile(file_path):
        print(f"{GREEN}✔ File Found{RESET}")
        return True
    else:
        print(f"{RED}✘ File Not Found{RESET}")
        return False

def calculate_parts(file_path):
    # Analyzes file size and suggests split count
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        line_count = len(lines)
        file_size = os.path.getsize(file_path) / (1024 * 1024) 
        
        print(f"{BLUE}Lines: {line_count} | Size: {file_size:.2f} MB{RESET}")
        suggested_parts = (line_count // 50000) + 1 # Suggest large chunks
        print(f"{YELLOW}Suggestion: {suggested_parts} parts.{RESET}")
        return line_count
    except Exception as e:
        print(f"{RED}Error reading file: {e}{RESET}")
        return None

def get_num_parts():
    # Asks for split count
    while True:
        try:
            num_parts = int(input(f"{YELLOW}Split into how many parts?: {RESET}"))
            if num_parts > 0:
                return num_parts
        except ValueError:
            print(f"{RED}Enter a number.{RESET}")

def get_config_value(index):
    # helper to read config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                lines = f.readlines()
                if len(lines) > index:
                    return lines[index].strip().split('=')[1]
        except:
            pass
    return None

def get_file_prefix():
    # Asks for output prefix
    default = get_config_value(0)
    if default: print(f"{YELLOW}Last Prefix: {default}{RESET}")
    
    prefix = input(f"{YELLOW}Prefix (default: 'part'): {RESET}") or "part"
    return prefix

def get_output_path():
    # Asks for output directory
    default = get_config_value(1) or get_files_dir()
    if default: print(f"{YELLOW}Last Path: {default}{RESET}")
    
    path = input(f"{YELLOW}Save Path (Enter for default): {RESET}") or default
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return path

def split_file(file_path, num_parts, file_prefix, output_path, line_count):
    # Splits the file
    try:
        lines_per_part = (line_count + num_parts - 1) // num_parts

        print(f"{BLUE}Splitting...{RESET}")
        
        with open(file_path, 'r') as file:
            lines = file.readlines()

        part_number = 1
        for i in range(0, line_count, lines_per_part):
            part_filename = os.path.join(output_path, f"{file_prefix}_{part_number}.txt")
            with open(part_filename, 'w') as part_file:
                part_file.writelines(lines[i:i + lines_per_part])
            part_number += 1

        print(f"{GREEN}✔ success! Split into {num_parts} files at {output_path}{RESET}")

    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

def save_config(file_prefix, output_path):
    # Saves prefs
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(f"prefix={file_prefix}\npath={output_path}\n")
    except:
        pass

def main():
    print_banner()
    file_path = get_file_path()
    
    if not check_file(file_path): return
    
    line_count = calculate_parts(file_path)
    if not line_count: return
    
    num_parts = get_num_parts()
    file_prefix = get_file_prefix()
    output_path = get_output_path()
    
    save_config(file_prefix, output_path)
    split_file(file_path, num_parts, file_prefix, output_path, line_count)

if __name__ == "__main__":
    main()