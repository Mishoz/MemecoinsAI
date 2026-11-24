#!/bin/bash
set -e
echo "Running sync at $(date)"
cd /home/NikiPC/Documents/MemecoinsAI
/home/NikiPC/.local/bin/gh repo sync
# git push is handled by /home/NikiPC/.local/bin/gh repo sync if needed
echo "Sync completed at $(date)"
