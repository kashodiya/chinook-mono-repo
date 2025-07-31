

#!/usr/bin/env python3

import asyncio
import json
import sys
import requests
import urllib3
from typing import Dict, List, Any, Optional

from fastmcp import Client

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MCP client setup
MCP_URL = "http://localhost:52796/mcp"
LLM_URL = "https://ec2-3-224-104-215.compute-1.amazonaws.com:7105/messages"

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

# Function to call the LLM API
def call_llm(messages, system=None):
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "claude-3-7-sonnet-20240229",
        "max_tokens": 4000,
        "temperature": 0.1,
        "messages": []
    }
    
    # Add system message if provided
    if system:
        payload["messages"].append({"role": "system", "content": system})
    
    # Add user and assistant messages
    for msg in messages:
        payload["messages"].append(msg)
    
    try:
        response = requests.post(
            LLM_URL,
            headers=headers,
            json=payload,
            verify=False  # Skip SSL verification
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return f"Error: {str(e)}"

# Main function
async def main():
    print("Starting Simple MCP Agent...")
    print("Connecting to MCP server at", MCP_URL)
    
    # Get available tools
    try:
        mcp_tools = await get_mcp_tools()
        print(f"Connected to MCP server. Found {len(mcp_tools)} tools.")
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        sys.exit(1)
    
    # Create system message with tools information
    tools_info = "Available tools:\n"
    for tool in mcp_tools:
        tools_info += f"- {tool['name']}: {tool['description']}\n"
    
    system_message = f"""
You are an MCP Agent that helps users interact with a Chinook Database through an MCP server.
You can perform various operations on the database tables using the available tools.

Available tables in the database:
- Album
- Artist
- Customer
- Employee
- Genre
- Invoice
- InvoiceLine
- MediaType
- Playlist
- PlaylistTrack
- Track

{tools_info}

When the user asks you to perform an operation, you should:
1. Understand what the user wants to do
2. Select the appropriate tool
3. Provide the necessary arguments for the tool
4. Execute the tool and return the results in a user-friendly format

Always be helpful, clear, and concise in your responses.

IMPORTANT: When selecting a tool, respond with a JSON object containing:
{{
  "tool": "tool_name",
  "args": {{
    "arg1": "value1",
    "arg2": "value2"
  }}
}}
"""
    
    # Initialize conversation history
    conversation = []
    
    print("\nSimple MCP Agent is ready! Type 'exit' to quit.\n")
    
    # Main loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Add user message to conversation
        conversation.append({"role": "user", "content": user_input})
        
        # Ask LLM to select a tool
        tool_selection_prompt = "Based on the user's request, which tool should I use and what arguments should I provide? Respond in JSON format only."
        conversation.append({"role": "user", "content": tool_selection_prompt})
        
        # Get tool selection from LLM
        tool_selection_response = call_llm(conversation, system_message)
        conversation.pop()  # Remove the tool selection prompt
        
        try:
            # Extract JSON from the response
            tool_selection_text = tool_selection_response
            
            # Find JSON in the response
            start_idx = tool_selection_text.find('{')
            end_idx = tool_selection_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = tool_selection_text[start_idx:end_idx]
                tool_selection = json.loads(json_str)
                
                tool_name = tool_selection.get("tool")
                tool_args = tool_selection.get("args", {})
                
                print(f"\nAgent: I'll use the '{tool_name}' tool with these arguments: {json.dumps(tool_args, indent=2)}")
                
                # Execute the tool
                tool_result = await execute_mcp_tool(tool_name, tool_args)
                
                # Format the tool result
                try:
                    result_json = json.loads(tool_result)
                    formatted_result = json.dumps(result_json, indent=2)
                except:
                    formatted_result = tool_result
                
                print(f"\nTool result:\n{formatted_result}")
                
                # Add tool execution to conversation
                conversation.append({"role": "assistant", "content": f"I executed the '{tool_name}' tool with arguments: {json.dumps(tool_args, indent=2)}\n\nResult:\n```json\n{formatted_result}\n```"})
                
                # Ask LLM to interpret the result
                response = call_llm(conversation, system_message)
                
                # Add assistant response to conversation
                conversation.append({"role": "assistant", "content": response})
                
                # Print the response
                print(f"\nAgent: {response}\n")
            else:
                print("\nAgent: I couldn't determine which tool to use. Could you please rephrase your request?\n")
                conversation.append({"role": "assistant", "content": "I couldn't determine which tool to use. Could you please rephrase your request?"})
        except Exception as e:
            print(f"\nAgent: I encountered an error: {str(e)}. Could you please rephrase your request?\n")
            conversation.append({"role": "assistant", "content": f"I encountered an error: {str(e)}. Could you please rephrase your request?"})

if __name__ == "__main__":
    asyncio.run(main())

