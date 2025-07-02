#!/bin/bash


BOLD="\033[1m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
CYAN="\033[1;36m"
RESET="\033[0m"


echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${GREEN}      🚀 Installation Script 🚀           ${RESET}"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
sleep 1

chmod +x run.sh

# List of required modules
REQUIRED_MODULES=("requests" "beautifulsoup4" "rich" "colorama" "tqdm" "aiohttp" "aiofiles" "psutil" "pytz")


check_and_install_modules() {
    echo -e "${BOLD}${YELLOW}[INFO] Checking for required Python modules...${RESET}"
    
    
    INSTALLED_MODULES=$(pip freeze | cut -d "=" -f 1)

    
    MISSING_MODULES=()
    for module in "${REQUIRED_MODULES[@]}"; do
        if ! echo "$INSTALLED_MODULES" | grep -qw "$module"; then
            MISSING_MODULES+=("$module")
        fi
    done

    
    if [ ${#MISSING_MODULES[@]} -ne 0 ]; then
        echo -e "${BOLD}${YELLOW}[INFO] Installing missing modules...${RESET}"
        for module in "${MISSING_MODULES[@]}"; do
            echo -e "${BOLD}${YELLOW}[INSTALLING] Installing ${module}...${RESET}"
            pip install "$module" --quiet
            if [ $? -eq 0 ]; then
                echo -e "${BOLD}${GREEN}[SUCCESS] ${module} installed.${RESET}"
            else
                echo -e "${BOLD}${RED}[ERROR] Failed to install ${module}.${RESET}"
                exit 1
            fi
        done
    else
        echo -e "${BOLD}${GREEN}[INFO] All required modules are already installed.${RESET}"
    fi
}


check_tool() {
    TOOL=$1
    if ! command -v "$TOOL" &>/dev/null; then
        echo -e "${BOLD}${RED}[ERROR] ${TOOL} is not installed. Please install ${TOOL} to proceed.${RESET}"
    else
        echo -e "${BOLD}${GREEN}[OK] ${TOOL} is installed.${RESET}"
    fi
}

# Install modules
check_and_install_modules


echo -e "${BOLD}${YELLOW}[INFO] Checking for required tools...${RESET}"
check_tool "bugscanx-go"
check_tool "subfinder"

echo -e "${BOLD}${GREEN}[INFO] Installation script completed successfully!${RESET}"
