# Chinook Mono Repo Testing Guide

This document provides instructions on how to start the services and run tests for the Chinook Mono Repo.

## Services Overview

The repository consists of two main services:

1. **Chinook CRUD API**: A RESTful API server that provides CRUD operations for the Chinook database.
2. **Chinook CRUD API MCP**: A Microservice Control Plane (MCP) server that provides tools for interacting with the Chinook Database API.

## Starting the Services

You can start the services using the provided run scripts or manually.

### Using Run Scripts

1. **Start the API Server**:
   ```bash
   ./run_api_server.sh
   ```

2. **Start the MCP Server**:
   ```bash
   ./run_mcp_server.sh
   ```

3. **Start the MCP Agent** (Optional):
   ```bash
   ./run_mcp_agent.sh
   ```

The run scripts will:
- Check if dependencies are installed
- Verify that prerequisite services are running
- Start the service in the correct directory

### Manual Start

If you prefer to start the services manually:

#### 1. Start the API Server

```bash
cd chinook-crud-api
python server.py
```

The API server will start on port 50514.

#### 2. Start the MCP Server

```bash
cd chinook-crud-api-mcp
python mcp_server.py
```

The MCP server will start on port 52796.

#### 3. Start the MCP Agent (Optional)

```bash
cd chinook-crud-api-mcp
python mcp_agent.py
```

Note: The MCP agent requires a valid OpenAI API key to run properly.

## Running Tests

The repository includes several test scripts to verify that the services are running correctly.

### 1. Basic API and MCP Server Test

```bash
python test_mcp.py
```

This test:
- Verifies that the API server is running and returns the list of available tables
- Creates and runs a test client that connects to the MCP server
- Lists the available tools from the MCP server
- Tests the `list_tables` tool

### 2. MCP Functionality Test

```bash
python test_mcp_functionality.py
```

This test:
- Connects directly to the MCP server
- Lists all available tools
- Tests the `list_tables` tool to get all database tables
- Tests the `get_all_records` tool to retrieve records from the Artist table

### 3. Manual MCP Agent Testing

The MCP agent provides a conversational interface for interacting with the Chinook Database. You can test it manually by running:

```bash
cd chinook-crud-api-mcp
python mcp_agent.py
```

Example commands you can try:
- "List all tables in the database"
- "Show me the first 5 artists"
- "Get details for artist with ID 1"
- "Create a new artist named 'New Band'"
- "Update artist 10 to have the name 'Updated Band Name'"
- "Delete artist with ID 15"

## Available MCP Tools

The MCP server provides the following tools:

1. `list_tables` - List all available tables in the database
2. `get_all_records` - Get all records from a specific table
3. `get_record` - Get a specific record by ID from a table
4. `create_record` - Create a new record in a table
5. `update_record` - Update an existing record in a table
6. `delete_record` - Delete a record from a table

## Troubleshooting

### API Server Issues

If the API server fails to start:
- Check if port 50514 is already in use
- Verify that the chinook.db file exists in the chinook-crud-api directory
- Ensure all dependencies are installed: `pip install fastapi uvicorn`

### MCP Server Issues

If the MCP server fails to start:
- Check if port 52796 is already in use
- Verify that the API server is running
- Ensure all dependencies are installed: `pip install fastmcp requests`

### MCP Agent Issues

If the MCP agent fails to start:
- Verify that the MCP server is running
- Ensure all dependencies are installed: `pip install langchain langchain-core langgraph litellm langchain_community`
- Make sure you have a valid OpenAI API key set in your environment
