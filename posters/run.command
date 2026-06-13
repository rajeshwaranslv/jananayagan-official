#!/bin/bash
# Double-click this file to generate Jana Nayagan poster #1.
# Stays open so you can read the output.

cd "$(dirname "$0")" || exit 1
echo "==> Installing Python dependencies (one-time)…"
pip3 install --quiet --user -r requirements.txt
echo "==> Calling Nano Banana 2…"
python3 generate_posters.py 1
echo
echo "==> Done. Press any key to close this window."
read -n 1 -s
