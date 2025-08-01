#!/bin/bash

# Script to run the Chinook CRUD API server

echo "Starting Chinook CRUD API server..."
cd "$(dirname "$0")/chinook-crud-api"

# Check if the database file exists
if [ ! -f "chinook.db" ]; then
    echo "Error: chinook.db not found!"
    exit 1
fi

# Install dependencies if needed
pip install -q fastapi uvicorn

# Run the server
python server.py
