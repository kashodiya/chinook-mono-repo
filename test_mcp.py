
import asyncio
import json
import requests

# Test the API server directly
def test_api_server():
    print("Testing API server...")
    try:
        response = requests.get("http://localhost:50514/")
        if response.status_code == 200:
            print("API server is running successfully!")
            print(f"Available tables: {response.json()['tables']}")
            return True
        else:
            print(f"API server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to API server: {e}")
        return False

# Test the MCP server directly using the FastMCP client
def test_mcp_server():
    print("\nTesting MCP server...")
    try:
        # Let's create a simple Python script that uses the FastMCP client
        print("Creating a test client script...")
        
        with open("test_mcp_client.py", "w") as f:
            f.write("""
import asyncio
from fastmcp import Client

async def main():
    print("Connecting to MCP server...")
    client = Client("http://localhost:52796/mcp")
    
    async with client:
        print("\\nListing available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
        
        print("\\nTesting list_tables tool:")
        result = await client.call_tool("list_tables", {})
        if result and len(result) > 0:
            print(f"Result: {result[0].text}")
        else:
            print("No result returned")

if __name__ == "__main__":
    asyncio.run(main())
""")
        
        # Run the test client
        print("\nRunning the test client...")
        import subprocess
        result = subprocess.run(["python", "test_mcp_client.py"], 
                               capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0 and "Result:" in result.stdout:
            print("MCP server test successful!")
            return True
        else:
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error testing MCP server: {e}")
        return False

# Run the tests
if __name__ == "__main__":
    api_success = test_api_server()
    mcp_success = test_mcp_server()
    
    if api_success and mcp_success:
        print("\nBoth servers are running successfully!")
    else:
        print("\nThere were issues with one or both servers.")
