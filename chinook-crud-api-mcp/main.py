import requests
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional

# API base URL
API_BASE_URL = "http://host.docker.internal:8000"

# Get available tables
def get_tables() -> List[str]:
    response = requests.get(f"{API_BASE_URL}/")
    return response.json()["tables"]

# Create MCP server
mcp = FastMCP("Chinook Database MCP Server")

# Tool to list all available tables
@mcp.tool(
    name="list_tables",
    description="List all available tables in the database"
)
def list_tables() -> Dict[str, Any]:
    """List all available tables in the Chinook database."""
    response = requests.get(f"{API_BASE_URL}/")
    return response.json()

# Tool to get all records from a table
@mcp.tool(
    name="get_all_records",
    description="Get all records from a specific table"
)
def get_all_records(
    table_name: str,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get all records from a specific table.
    
    Args:
        table_name: Name of the table to query
        limit: Maximum number of records to return (default: 100)
        offset: Number of records to skip (default: 0)
    """
    response = requests.get(f"{API_BASE_URL}/{table_name}", params={"limit": limit, "offset": offset})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get records: {response.status_code}", "details": response.text}

# Tool to get a specific record by ID
@mcp.tool(
    name="get_record",
    description="Get a specific record by ID from a table"
)
def get_record(
    table_name: str,
    record_id: int
) -> Dict[str, Any]:
    """
    Get a specific record by ID from a table.
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to retrieve
    """
    response = requests.get(f"{API_BASE_URL}/{table_name}/{record_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get record: {response.status_code}", "details": response.text}

# Tool to create a new record
@mcp.tool(
    name="create_record",
    description="Create a new record in a table"
)
def create_record(
    table_name: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new record in a table.
    
    Args:
        table_name: Name of the table
        data: Data for the new record as a dictionary
    """
    response = requests.post(f"{API_BASE_URL}/{table_name}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to create record: {response.status_code}", "details": response.text}

# Tool to update an existing record
@mcp.tool(
    name="update_record",
    description="Update an existing record in a table"
)
def update_record(
    table_name: str,
    record_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update an existing record in a table.
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to update
        data: Updated data for the record as a dictionary
    """
    response = requests.put(f"{API_BASE_URL}/{table_name}/{record_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to update record: {response.status_code}", "details": response.text}

# Tool to delete a record
@mcp.tool(
    name="delete_record",
    description="Delete a record from a table"
)
def delete_record(
    table_name: str,
    record_id: int
) -> Dict[str, Any]:
    """
    Delete a record from a table.
    
    Args:
        table_name: Name of the table
        record_id: ID of the record to delete
    """
    response = requests.delete(f"{API_BASE_URL}/{table_name}/{record_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to delete record: {response.status_code}", "details": response.text}

def main():
    print("Starting Chinook Database MCP Server...")
    # Start the MCP server
    mcp.run(transport="streamable-http", port=52796, host="0.0.0.0")

if __name__ == "__main__":
    main()
