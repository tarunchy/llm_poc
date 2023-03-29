#!/bin/bash

# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Install required packages
pip install -r requirements.txt

# Run the application using run.sh
chmod +x run.sh
./run.sh

