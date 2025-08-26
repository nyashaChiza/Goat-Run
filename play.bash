#!/bin/bash

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python3 to run the game."
    exit
fi

# Check if loguru is installed
if ! python3 -c "import loguru" &> /dev/null
then
    echo "Installing required Python packages..."
    pip3 install -r requirements.txt
fi

# Run the game
python3 game.py
