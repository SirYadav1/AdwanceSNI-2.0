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

# 6. Global Shortcut (Permanent)
echo -e "${BOLD}${YELLOW}[*] Setting up global command...${RESET}"
PWD_DIR=$(pwd)
BIN_PATH="/usr/local/bin/adwance"

# Detect Termux Bin
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    BIN_PATH="/data/data/com.termux/files/usr/bin/adwance"
fi

# Create Wrapper
cat <<EOF > adwance
#!/bin/bash
cd $PWD_DIR && bash run.sh
EOF
chmod +x adwance

# Try to move to bin
if mv adwance "$BIN_PATH" 2>/dev/null || sudo mv adwance "$BIN_PATH" 2>/dev/null; then
    echo -e "${BOLD}${GREEN}[+] Global command 'adwance' created successfully!${RESET}"
    echo -e "${BOLD}${CYAN}[!] Now you can type 'adwance' from anywhere.${RESET}"
else
    # Fallback to Alias if BIN fails
    rm -f adwance
    echo -e "${BOLD}${YELLOW}[!] Could not create bin command, using alias instead...${RESET}"
    ALIAS_CMD="alias adwance='cd $PWD_DIR && ./run.sh'"
    
    [ -f "$HOME/.bashrc" ] && echo "$ALIAS_CMD" >> "$HOME/.bashrc"
    [ -f "$HOME/.zshrc" ] && echo "$ALIAS_CMD" >> "$HOME/.zshrc"
    echo -e "${BOLD}${GREEN}[+] Alias 'adwance' added to shell profile.${RESET}"
fi

echo
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${GREEN}   INSTALLATION COMPLETE!   ${RESET}"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${YELLOW}Type 'adwance' to start the tool from anywhere!${RESET}"
echo
echo -e "${BOLD}${WHITE}Press [ENTER] to restart Termux session...${RESET}"
read -r
kill -9 $PPID 2>/dev/null || exit
