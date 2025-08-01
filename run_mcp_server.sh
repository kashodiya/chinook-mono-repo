
#!/bin/bash

# Script to run the Chinook MCP server

echo "Starting Chinook MCP server..."
cd "$(dirname "$0")/chinook-crud-api-mcp"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package installer..."
    pip install -q uv
fi

# Install dependencies if needed
uv pip install -q fastmcp requests

# Check if API server is running
if ! curl -s http://localhost:50514/ > /dev/null; then
    echo "Error: API server is not running or not accessible at http://localhost:50514/"
    echo "Please start the API server first using: ./run_api_server.sh"
    exit 1
fi

# Run the server
uv run mcp_server.py

