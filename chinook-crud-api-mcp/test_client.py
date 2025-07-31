
import asyncio
from fastmcp import Client

async def main():
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
        
        # Test list_tables tool
        print("\nTesting list_tables tool:")
        result = await client.call_tool("list_tables")
        print(result)
        
        # Test get_all_records tool
        print("\nTesting get_all_records tool:")
        result = await client.call_tool("get_all_records", {"table_name": "Artist", "limit": 5})
        print(result)
        
        # Test get_record tool
        print("\nTesting get_record tool:")
        result = await client.call_tool("get_record", {"table_name": "Artist", "record_id": 1})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
