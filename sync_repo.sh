#!/bin/bash
set -e
echo "Running sync at $(date)"
cd /home/NikiPC/Documents/MemecoinsAI
git pull origin main
git push origin main
echo "Sync completed at $(date)"
