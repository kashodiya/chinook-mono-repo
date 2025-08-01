

#!/bin/bash

# Script to run the Chinook MCP agent

echo "Starting Chinook MCP agent..."
cd "$(dirname "$0")/chinook-crud-api-mcp"

# Install dependencies if needed
pip install -q langchain langchain-core langgraph litellm langchain_community

# Check if MCP server is running
if ! curl -s -H "Accept: text/event-stream" http://localhost:52796/mcp > /dev/null; then
    echo "Error: MCP server is not running or not accessible at http://localhost:52796/mcp"
    echo "Please start the MCP server first using: ./run_mcp_server.sh"
    exit 1
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY environment variable is not set."
    echo "The MCP agent requires an OpenAI API key to function properly."
    echo "You can set it using: export OPENAI_API_KEY=your_api_key"
    echo ""
    echo "Continuing with a dummy key for testing purposes..."
    export OPENAI_API_KEY="sk-dummy"
fi

# Run the agent
python mcp_agent.py


