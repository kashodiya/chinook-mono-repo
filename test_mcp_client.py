
import asyncio
from fastmcp import Client

async def main():
    print("Connecting to MCP server...")
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        print("\nListing available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
        
        print("\nTesting list_tables tool:")
        result = await client.call_tool("list_tables", {})
        if result and len(result) > 0:
            print(f"Result: {result[0].text}")
        else:
            print("No result returned")

if __name__ == "__main__":
    asyncio.run(main())
