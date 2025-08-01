
import asyncio
import subprocess
import sys
import time

def test_mcp_agent():
    print("Testing MCP Agent...")
    
    # Start the MCP agent process
    process = subprocess.Popen(
        ["python", "chinook-crud-api-mcp/mcp_agent.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Wait for the agent to start
    print("Waiting for MCP Agent to start...")
    time.sleep(5)
    
    # Check if the process is still running
    if process.poll() is not None:
        print("Error: MCP Agent failed to start")
        print(f"Error output: {process.stderr.read()}")
        return False
    
    # Send a command to the agent
    print("Sending command to MCP Agent: 'List all tables in the database'")
    process.stdin.write("List all tables in the database\n")
    process.stdin.flush()
    
    # Wait for response
    print("Waiting for response...")
    time.sleep(5)
    
    # Terminate the process
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    
    # Get output
    stdout = process.stdout.read()
    stderr = process.stderr.read()
    
    print("\nMCP Agent Output:")
    print(stdout)
    
    if stderr:
        print("\nMCP Agent Errors:")
        print(stderr)
    
    # Check if the output contains expected information
    if "tables" in stdout.lower() and "artist" in stdout.lower():
        print("\nMCP Agent test successful!")
        return True
    else:
        print("\nMCP Agent test failed: Expected output not found")
        return False

if __name__ == "__main__":
    success = test_mcp_agent()
    sys.exit(0 if success else 1)
