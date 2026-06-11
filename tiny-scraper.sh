#!/bin/bash

progdir="$(cd "$(dirname "$0")" || exit; pwd)"/tiny_scraper
log_file="${progdir}/log.txt"

# --- Pre-flight checks ---
echo "[DEBUG] progdir: ${progdir}" > "$log_file"

if ! command -v python3 > /dev/null 2>&1; then
    echo "[ERROR] python3 not found on PATH" >> "$log_file"
    exit 1
fi
echo "[DEBUG] python3: $(command -v python3)" >> "$log_file"

if [ ! -f "${progdir}/main.py" ]; then
    echo "[ERROR] ${progdir}/main.py not found" >> "$log_file"
    exit 1
fi

if [ ! -f "${progdir}/config.json" ]; then
    echo "[ERROR] ${progdir}/config.json not found" >> "$log_file"
    exit 1
fi

export PYSDL2_DLL_PATH="/usr/lib"

# --- Start volume control daemon if available ---
VOL_PID=""
if [ -f /mnt/mod/ctrl/volumeCtrl.dge ]; then
    /mnt/mod/ctrl/volumeCtrl.dge &
    VOL_PID=$!
fi

# --- Launch the scraper ---
echo "[DEBUG] Launching Tiny Scraper..." >> "$log_file"
python3 "${progdir}/main.py" "${progdir}/config.json" >> "$log_file" 2>&1
exit_code=$?
echo "[DEBUG] Python exited with code: ${exit_code}" >> "$log_file"

# --- Cleanup volume daemon ---
if [ -n "$VOL_PID" ]; then
    kill -9 "$VOL_PID" 2>/dev/null
fi

exit ${exit_code}
