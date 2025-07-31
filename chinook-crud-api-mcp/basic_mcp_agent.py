

#!/usr/bin/env python3

import asyncio
import json
import sys
from typing import Dict, List, Any, Optional

from fastmcp import Client

# MCP client setup
MCP_URL = "http://localhost:52796/mcp"

# Function to get available MCP tools
async def get_mcp_tools():
    client = Client(MCP_URL)
    tools = []
    
    async with client:
        tools = await client.list_tools()
    
    return [{"name": tool.name, "description": tool.description} for tool in tools]

# Function to execute MCP tool
async def execute_mcp_tool(tool_name: str, args: Dict = None):
    if args is None:
        args = {}
    
    client = Client(MCP_URL)
    result = None
    
    async with client:
        result = await client.call_tool(tool_name, args)
    
    if result and len(result) > 0:
        return result[0].text
    return "No result returned"

# Function to parse user input and determine tool and arguments
def parse_user_input(user_input, available_tools):
    user_input = user_input.lower()
    
    # Check for list tables command
    if "list tables" in user_input or "show tables" in user_input:
        return "list_tables", {}
    
    # Check for get all records command
    if "all" in user_input and ("records" in user_input or "rows" in user_input):
        for tool in available_tools:
            if tool["name"] == "get_all_records":
                # Extract table name
                table_name = None
                limit = 10  # Default limit
                
                # Check for table names
                tables = ["album", "artist", "customer", "employee", "genre", 
                          "invoice", "invoiceline", "mediatype", "playlist", 
                          "playlisttrack", "track"]
                
                for table in tables:
                    if table in user_input:
                        table_name = table.capitalize()
                        break
                
                # Check for limit
                if "limit" in user_input:
                    try:
                        limit_idx = user_input.index("limit")
                        limit_str = user_input[limit_idx:].split()[1]
                        limit = int(limit_str)
                    except (ValueError, IndexError):
                        pass
                
                if table_name:
                    return "get_all_records", {"table_name": table_name, "limit": limit}
    
    # Check for get record command
    if "get" in user_input and "record" in user_input and "id" in user_input:
        for tool in available_tools:
            if tool["name"] == "get_record":
                # Extract table name and ID
                table_name = None
                record_id = None
                
                # Check for table names
                tables = ["album", "artist", "customer", "employee", "genre", 
                          "invoice", "invoiceline", "mediatype", "playlist", 
                          "playlisttrack", "track"]
                
                for table in tables:
                    if table in user_input:
                        table_name = table.capitalize()
                        break
                
                # Extract ID
                try:
                    id_idx = user_input.index("id")
                    id_parts = user_input[id_idx:].split()
                    for part in id_parts:
                        if part.isdigit():
                            record_id = int(part)
                            break
                except (ValueError, IndexError):
                    pass
                
                if table_name and record_id:
                    return "get_record", {"table_name": table_name, "record_id": record_id}
    
    # Check for create record command
    if ("create" in user_input or "add" in user_input) and "record" in user_input:
        for tool in available_tools:
            if tool["name"] == "create_record":
                # Extract table name and data
                table_name = None
                data = {}
                
                # Check for table names
                tables = ["album", "artist", "customer", "employee", "genre", 
                          "invoice", "invoiceline", "mediatype", "playlist", 
                          "playlisttrack", "track"]
                
                for table in tables:
                    if table in user_input:
                        table_name = table.capitalize()
                        break
                
                # Extract data (simple key-value pairs)
                if "name" in user_input and ":" in user_input:
                    try:
                        name_idx = user_input.index("name")
                        name_parts = user_input[name_idx:].split(":", 1)
                        if len(name_parts) > 1:
                            name_value = name_parts[1].strip().strip('"\'')
                            data["Name"] = name_value
                    except (ValueError, IndexError):
                        pass
                
                if table_name and data:
                    return "create_record", {"table_name": table_name, "data": data}
    
    # Check for update record command
    if "update" in user_input and "record" in user_input:
        for tool in available_tools:
            if tool["name"] == "update_record":
                # Extract table name, ID, and data
                table_name = None
                record_id = None
                data = {}
                
                # Check for table names
                tables = ["album", "artist", "customer", "employee", "genre", 
                          "invoice", "invoiceline", "mediatype", "playlist", 
                          "playlisttrack", "track"]
                
                for table in tables:
                    if table in user_input:
                        table_name = table.capitalize()
                        break
                
                # Extract ID
                try:
                    id_idx = user_input.index("id")
                    id_parts = user_input[id_idx:].split()
                    for part in id_parts:
                        if part.isdigit():
                            record_id = int(part)
                            break
                except (ValueError, IndexError):
                    pass
                
                # Extract data (simple key-value pairs)
                if "name" in user_input and ":" in user_input:
                    try:
                        name_idx = user_input.index("name")
                        name_parts = user_input[name_idx:].split(":", 1)
                        if len(name_parts) > 1:
                            name_value = name_parts[1].strip().strip('"\'')
                            data["Name"] = name_value
                    except (ValueError, IndexError):
                        pass
                
                if table_name and record_id and data:
                    return "update_record", {"table_name": table_name, "record_id": record_id, "data": data}
    
    # Check for delete record command
    if ("delete" in user_input or "remove" in user_input) and "record" in user_input:
        for tool in available_tools:
            if tool["name"] == "delete_record":
                # Extract table name and ID
                table_name = None
                record_id = None
                
                # Check for table names
                tables = ["album", "artist", "customer", "employee", "genre", 
                          "invoice", "invoiceline", "mediatype", "playlist", 
                          "playlisttrack", "track"]
                
                for table in tables:
                    if table in user_input:
                        table_name = table.capitalize()
                        break
                
                # Extract ID
                try:
                    id_idx = user_input.index("id")
                    id_parts = user_input[id_idx:].split()
                    for part in id_parts:
                        if part.isdigit():
                            record_id = int(part)
                            break
                except (ValueError, IndexError):
                    pass
                
                if table_name and record_id:
                    return "delete_record", {"table_name": table_name, "record_id": record_id}
    
    # If no tool matches, return None
    return None, None

# Main function
async def main():
    print("Starting Basic MCP Agent...")
    print("Connecting to MCP server at", MCP_URL)
    
    # Get available tools
    try:
        mcp_tools = await get_mcp_tools()
        print(f"Connected to MCP server. Found {len(mcp_tools)} tools.")
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        sys.exit(1)
    
    # Print available tools
    print("\nAvailable tools:")
    for tool in mcp_tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    print("\nAvailable tables:")
    print("- Album\n- Artist\n- Customer\n- Employee\n- Genre")
    print("- Invoice\n- InvoiceLine\n- MediaType\n- Playlist\n- PlaylistTrack\n- Track")
    
    print("\nBasic MCP Agent is ready! Type 'exit' to quit.\n")
    print("Example commands:")
    print("- List all tables")
    print("- Get all records from Artist limit 5")
    print("- Get record from Artist with id 1")
    print("- Create record in Artist with name: 'New Artist'")
    print("- Update record in Artist with id 1 name: 'Updated Artist'")
    print("- Delete record from Artist with id 1")
    print()
    
    # Main loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Parse user input
        tool_name, tool_args = parse_user_input(user_input, mcp_tools)
        
        if tool_name:
            print(f"\nAgent: I'll use the '{tool_name}' tool with these arguments: {json.dumps(tool_args, indent=2)}")
            
            # Execute the tool
            try:
                tool_result = await execute_mcp_tool(tool_name, tool_args)
                
                # Format the tool result
                try:
                    result_json = json.loads(tool_result)
                    formatted_result = json.dumps(result_json, indent=2)
                except:
                    formatted_result = tool_result
                
                print(f"\nResult:\n{formatted_result}\n")
            except Exception as e:
                print(f"\nError executing tool: {str(e)}\n")
        else:
            print("\nAgent: I couldn't determine which tool to use. Please try one of the example commands.\n")

if __name__ == "__main__":
    asyncio.run(main())

