# chinook-crud-api-mcp

This project consists of two main components:

1. **MCP Server**: A FastMCP server that provides tools for interacting with the Chinook Database API.
2. **MCP Agent**: A CLI agent that uses LLM to understand user requests and execute the appropriate MCP tools.

## Installation

```bash
uv pip install -e .
pip install langchain langchain-core langgraph litellm
```

## Usage

### Running the MCP Server

Start the MCP server:

```bash
python mcp_server.py
```

The server will start on port 52796.

### Running the MCP Agent

Start the MCP agent:

```bash
python mcp_agent.py
```

The agent will connect to the MCP server and provide a conversational interface for interacting with the Chinook Database.

Example commands:
- "List all tables in the database"
- "Show me the first 5 artists"
- "Get details for artist with ID 1"
- "Create a new artist named 'New Band'"
- "Update artist 10 to have the name 'Updated Band Name'"
- "Delete artist with ID 15"

## Available Tools

The MCP server provides the following tools:

1. `list_tables` - List all available tables in the database
2. `get_all_records` - Get all records from a specific table
3. `get_record` - Get a specific record by ID from a table
4. `create_record` - Create a new record in a table
5. `update_record` - Update an existing record in a table
6. `delete_record` - Delete a record from a table

## Example Usage

### List Tables

```json
{
  "tool": "list_tables",
  "params": {}
}
```

### Get All Records

```json
{
  "tool": "get_all_records",
  "params": {
    "table_name": "Artist",
    "limit": 10,
    "offset": 0
  }
}
```

### Get Record

```json
{
  "tool": "get_record",
  "params": {
    "table_name": "Artist",
    "record_id": 1
  }
}
```

### Create Record

```json
{
  "tool": "create_record",
  "params": {
    "table_name": "Artist",
    "data": {
      "Name": "New Artist"
    }
  }
}
```

### Update Record

```json
{
  "tool": "update_record",
  "params": {
    "table_name": "Artist",
    "record_id": 1,
    "data": {
      "Name": "Updated Artist Name"
    }
  }
}
```

### Delete Record

```json
{
  "tool": "delete_record",
  "params": {
    "table_name": "Artist",
    "record_id": 1
  }
}
```
