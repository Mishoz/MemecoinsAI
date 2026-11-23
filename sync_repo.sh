#!/bin/bash
set -e
echo "Running sync at $(date)"
cd /home/NikiPC/Documents/MemecoinsAI
gh repo sync
# git push is handled by gh repo sync if needed
echo "Sync completed at $(date)"
