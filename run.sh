#!/bin/bash
BOLD="\033[1m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
CYAN="\033[1;36m"
RESET="\033[0m"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${GREEN}      🚀 Starting AdwanceSNI 2.0 🚀          ${RESET}"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
sleep 1

echo -e "${BOLD}${YELLOW}[INFO] Navigating to the modules folder...${RESET}"
cd modules || { 
    echo -e "${BOLD}${RED}[ERROR] Failed to navigate to 'modules'. Exiting.${RESET}"
    exit 1
}


if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo -e "${BOLD}${RED}[ERROR] Python is not installed. Please install Python to proceed.${RESET}"
    exit 1
fi

# Detect python command
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo -e "${BOLD}${YELLOW}[INFO] Launching the main application...${RESET}"
sleep 1

"$PYTHON_CMD" main.py

# Completion Message
if [ $? -eq 0 ]; then
    echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
    echo -e "${BOLD}${GREEN}🎉 AdwanceSNI 2.0 has successfully finished! 🎉${RESET}"
    echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
else
    echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
    echo -e "${BOLD}${RED}❌ Oops! Something went wrong with AdwanceSNI 2.0 ❌${RESET}"
    echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
fi
