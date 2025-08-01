#!/bin/bash

# Script to run the Chinook CRUD API server

echo "Starting Chinook CRUD API server..."
cd "$(dirname "$0")/chinook-crud-api"

# Check if the database file exists
if [ ! -f "chinook.db" ]; then
    echo "Error: chinook.db not found!"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package installer..."
    pip install -q uv
fi

# Install dependencies if needed
uv pip install -q fastapi uvicorn

# Run the server
uv run server.py
