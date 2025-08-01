
import asyncio
import sys
from fastmcp import Client

async def test_mcp_functionality():
    print("Testing MCP functionality directly...")
    
    # Connect to the MCP server
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        # List available tools
        print("Listing available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
        
        # Test list_tables tool
        print("\nTesting list_tables tool:")
        result = await client.call_tool("list_tables", {})
        if result and len(result) > 0:
            print(f"Result: {result[0].text}")
            tables_result = True
        else:
            print("No result returned")
            tables_result = False
        
        # Test get_all_records tool
        print("\nTesting get_all_records tool:")
        result = await client.call_tool("get_all_records", {"table_name": "Artist", "limit": 5})
        if result and len(result) > 0:
            print(f"Result: {result[0].text}")
            records_result = True
        else:
            print("No result returned")
            records_result = False
        
        # Overall success
        if tables_result and records_result:
            print("\nMCP functionality test successful!")
            return True
        else:
            print("\nMCP functionality test failed")
            return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_functionality())
    sys.exit(0 if success else 1)
