
#!/bin/bash

# Script to run the Chinook MCP server

echo "Starting Chinook MCP server..."
cd "$(dirname "$0")/chinook-crud-api-mcp"

# Install dependencies if needed
pip install -q fastmcp requests

# Check if API server is running
if ! curl -s http://localhost:50514/ > /dev/null; then
    echo "Error: API server is not running or not accessible at http://localhost:50514/"
    echo "Please start the API server first using: ./run_api_server.sh"
    exit 1
fi

# Run the server
python mcp_server.py

