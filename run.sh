#!/bin/bash
# AdwanceSNI 2.0 - Simplified Launcher
# This script is kept for backward compatibility
# You can also run directly: python main.py

BOLD="\033[1m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"
echo -e "${BOLD}${GREEN}      🚀 Starting AdwanceSNI 2.0 🚀          ${RESET}"
echo -e "${BOLD}${CYAN}-------------------------------------------${RESET}"

# Detect python command
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo -e "${BOLD}${YELLOW}[ERROR] Python is not installed. Please install Python to proceed.${RESET}"
    exit 1
fi

# Run main.py from root directory
"$PYTHON_CMD" main.py
