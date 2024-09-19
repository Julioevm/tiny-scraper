#!/bin/bash

. /mnt/mod/ctrl/configs/functions &>/dev/null 2>&1
progdir=$(cd $(dirname "$0"); pwd)

program="python3 ${progdir}/tiny_scraper/main.py"
log_file="${progdir}/tiny_scraper/log.txt"

$program > "$log_file" 2>&1