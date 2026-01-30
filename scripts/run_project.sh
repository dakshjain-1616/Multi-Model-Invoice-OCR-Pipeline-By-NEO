#!/bin/bash
# run_project.sh - Entry point for Unix/Mac systems

set -e

# Change to the script directory
cd "$(dirname "$0")"

echo "=== Invoice Project Automator ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found. Please install Python 3."
    exit 1
fi

# Run the python setup/execution wrapper
python3 run_project.py