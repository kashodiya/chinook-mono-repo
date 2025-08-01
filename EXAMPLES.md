
# Chinook MCP Examples

This document provides examples of how to use the Chinook MCP server to interact with the Chinook database.

## Prerequisites

Before running these examples, make sure you have:

1. Started the API server:
   ```bash
   ./run_api_server.sh
   ```

2. Started the MCP server:
   ```bash
   ./run_mcp_server.sh
   ```

3. Installed the required dependencies:
   ```bash
   pip install fastmcp requests
   ```

## Example Scripts

### 1. Basic MCP Client Demo (`mcp_client_demo.py`)

This script demonstrates basic CRUD operations using the MCP server:
- Listing all tables
- Getting records from a table
- Getting a specific record by ID
- Creating a new record
- Updating a record
- Deleting a record

Run the example:
```bash
python mcp_client_demo.py
```

### 2. Complex Queries (`mcp_complex_queries.py`)

This script demonstrates more complex operations:
- Finding all tracks by a specific artist
- Finding the top 5 genres by number of tracks
- Calculating the total duration of all tracks by an artist

Run the example:
```bash
python mcp_complex_queries.py
```

### 3. Customer Analysis (`mcp_customer_analysis.py`)

This script demonstrates how to analyze customer data:
- Finding customers who purchased tracks from a specific artist
- Counting purchases per customer
- Analyzing customer distribution by country

Run the example:
```bash
python mcp_customer_analysis.py
```

## Using the MCP Client

Here's a basic template for creating your own MCP client:

```python
import asyncio
import json
from fastmcp import Client

async def my_mcp_client():
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
        
        # Call a tool
        result = await client.call_tool("tool_name", {"param1": "value1", "param2": "value2"})
        if result and len(result) > 0:
            data = json.loads(result[0].text)
            print(f"Result: {json.dumps(data, indent=2)}")

if __name__ == "__main__":
    asyncio.run(my_mcp_client())
```

## Available MCP Tools

The Chinook MCP server provides the following tools:

1. `list_tables`: List all available tables in the database
   - Parameters: None

2. `get_all_records`: Get all records from a specific table
   - Parameters:
     - `table_name` (string): Name of the table
     - `limit` (integer, optional): Maximum number of records to return (default: 100)
     - `offset` (integer, optional): Number of records to skip (default: 0)

3. `get_record`: Get a specific record by ID from a table
   - Parameters:
     - `table_name` (string): Name of the table
     - `record_id` (integer): ID of the record to retrieve

4. `create_record`: Create a new record in a table
   - Parameters:
     - `table_name` (string): Name of the table
     - `data` (object): Data for the new record as a dictionary

5. `update_record`: Update an existing record in a table
   - Parameters:
     - `table_name` (string): Name of the table
     - `record_id` (integer): ID of the record to update
     - `data` (object): Updated data for the record as a dictionary

6. `delete_record`: Delete a record from a table
   - Parameters:
     - `table_name` (string): Name of the table
     - `record_id` (integer): ID of the record to delete

## Database Schema

The Chinook database contains the following tables:

- `Album`: Albums in the music store
- `Artist`: Artists who created the albums
- `Customer`: Customers who made purchases
- `Employee`: Employees of the store
- `Genre`: Music genres
- `Invoice`: Sales invoices
- `InvoiceLine`: Individual line items on an invoice
- `MediaType`: Types of media (e.g., MPEG audio file)
- `Playlist`: Playlists of tracks
- `PlaylistTrack`: Tracks included in a playlist
- `Track`: Individual songs/tracks

For more information about the database schema, you can use the `list_tables` tool and explore the tables using the `get_all_records` tool.
