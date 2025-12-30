#!/bin/bash

# AdwanceSNI 2.0.4Installer
# (Termux, Linux, WSL)

BOLD="\033[1m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
CYAN="\033[1;36m"
RESET="\033[0m"

REPO_DIR="$HOME/AdwanceSNI-2.0"
REPO_URL="https://github.com/SirYadav1/AdwanceSNI-2.0"

echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${GREEN}   AdwanceSNI 2.0.4Installer   ${RESET}"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${YELLOW}[*] Checking System...${RESET}"
sleep 1

# 0. Clone Repo (One-line support)
if [ ! -f "run.sh" ]; then
    echo -e "${BOLD}${YELLOW}[*] Downloading...${RESET}"
    if [ -d "$REPO_DIR" ]; then
        echo -e "${BOLD}${YELLOW}[*] Updating Repo...${RESET}"
        cd "$REPO_DIR" && git pull
    else
        echo -e "${BOLD}${YELLOW}[*] Cloning Repo...${RESET}"
        git clone "$REPO_URL" "$REPO_DIR"
        cd "$REPO_DIR" || { echo -e "${BOLD}${RED}[!] Clone Failed!${RESET}"; exit 1; }
    fi
fi

# 1. System Setup
if [ -d "/data/data/com.termux/files/home" ]; then
    echo -e "${BOLD}${GREEN}[+] Termux Detected.${RESET}"
    echo -e "${BOLD}${YELLOW}[*] Updating Packages...${RESET}"
    pkg update -y 
    
    echo -e "${BOLD}${YELLOW}[*] Installing Deps...${RESET}"
    pkg install git python golang -y
else
    echo -e "${BOLD}${GREEN}[+] Linux detected.${RESET}"
    if [ -f /etc/debian_version ]; then
        echo -e "${BOLD}${YELLOW}[*] Installing Deps...${RESET}"
        sudo apt-get update -y
        sudo apt-get install git python3 python3-pip golang -y
    fi
fi

# 2. Set Permissions
chmod +x run.sh
chmod +x modules/*.py 2>/dev/null

# 3. Python Libs
echo -e "${BOLD}${YELLOW}[*] Installing Python Libs...${RESET}"
PIP_PACKAGES="requests beautifulsoup4 rich colorama tqdm aiohttp aiofiles psutil pytz"

# Attempt install with break-system-packages flag for newer envs
if pip3 install $PIP_PACKAGES --break-system-packages > /dev/null 2>&1; then
    echo -e "${BOLD}${GREEN}[+] Libs Installed.${RESET}"
else
    pip3 install $PIP_PACKAGES
fi

# 4. Go Setup
echo -e "${BOLD}${YELLOW}[*] Setting up Go...${RESET}"
export GOPATH=$HOME/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin

if ! grep -q "export PATH=\$PATH:\$GOPATH/bin" ~/.bashrc; then
    echo 'export GOPATH=$HOME/go' >> ~/.bashrc
    echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> ~/.bashrc
fi

# 5. Tools Install
install_tool() {
    NAME=$1
    PKG_URL=$2
    CMD=$3
    
    if ! command -v "$CMD" &>/dev/null; then
        echo -e "${BOLD}${YELLOW}[*] Installing ${NAME}...${RESET}"
        if [ "$NAME" == "FlashScan-Go" ]; then
            GOPROXY=direct go install github.com/SirYadav1/flashscan-go/v2@v2.0.1
        else
            go install -v "$PKG_URL"
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${BOLD}${GREEN}[+] ${NAME} OK!${RESET}"
        else
            echo -e "${BOLD}${RED}[!] ${NAME} Failed.${RESET}"
        fi
    else
        echo -e "${BOLD}${GREEN}[OK] ${NAME} found.${RESET}"
    fi
}

install_tool "FlashScan-Go" "github.com/SirYadav1/flashscan-go/v2@latest" "flashscan-go"
install_tool "Subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest" "subfinder"

# 6. Finish
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${GREEN}   Done!   ${RESET}"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"

echo -e "${BOLD}${YELLOW}Run:${RESET} ./run.sh"

# Auto Alias
if ! grep -q "alias adwance=" ~/.bashrc; then
    echo -e "${BOLD}${YELLOW}[*] Adding shortcut...${RESET}"
    PWD=$(pwd)
    ALIAS_CMD="alias adwance='cd $PWD && ./run.sh'"
    
    # Add to .bashrc
    if [ -f "$HOME/.bashrc" ]; then
        if ! grep -q "alias adwance=" "$HOME/.bashrc"; then
            echo "$ALIAS_CMD" >> "$HOME/.bashrc"
        fi
    else
        echo "$ALIAS_CMD" >> "$HOME/.bashrc"
    fi

    # Add to .zshrc (if exists)
    if [ -f "$HOME/.zshrc" ]; then
        if ! grep -q "alias adwance=" "$HOME/.zshrc"; then
            echo "$ALIAS_CMD" >> "$HOME/.zshrc"
        fi
    fi
    
    echo -e "${BOLD}${GREEN}[+] Shortcut added!${RESET}"
    echo -e "${BOLD}${CYAN}Please restart Termux or type 'source ~/.bashrc' to use 'adwance' command.${RESET}"
fi
