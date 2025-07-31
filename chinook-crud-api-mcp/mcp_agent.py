
#!/usr/bin/env python3

import asyncio
import json
import sys
from typing import Dict, List, Any, Optional, TypedDict, Annotated

from fastmcp import Client
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END

# Configure LLM
llm = ChatAnthropic(
    model="claude-3-7-sonnet-20240229",
    anthropic_api_key="not-needed",  # Will be overridden by base_url
    base_url="https://ec2-3-224-104-215.compute-1.amazonaws.com:7105/v1",
    temperature=0.1,
    max_tokens=4000,
    model_kwargs={"verify_ssl": False}  # For self-signed certificates
)

# MCP client setup
MCP_URL = "http://localhost:52796/mcp"

# Define state
class AgentState(TypedDict):
    messages: List[Any]
    current_tool: Optional[str]
    tool_args: Optional[Dict]
    tool_result: Optional[str]
    mcp_tools: Optional[List[Dict]]

# System prompt
SYSTEM_PROMPT = """
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

When the user asks you to perform an operation, you should:
1. Understand what the user wants to do
2. Select the appropriate tool
3. Provide the necessary arguments for the tool
4. Execute the tool and return the results in a user-friendly format

Always be helpful, clear, and concise in your responses.
"""

# Tool descriptions
TOOL_DESCRIPTIONS = {
    "list_tables": "Lists all available tables in the database",
    "get_all_records": "Gets all records from a specific table (params: table_name, limit)",
    "get_record": "Gets a specific record by ID from a table (params: table_name, record_id)",
    "create_record": "Creates a new record in a table (params: table_name, data)",
    "update_record": "Updates an existing record in a table (params: table_name, record_id, data)",
    "delete_record": "Deletes a record from a table (params: table_name, record_id)"
}

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

# Define the agent nodes
def agent_prompt(state: AgentState):
    """Generate agent prompt based on the current state."""
    messages = state["messages"]
    
    # Add tool information if available
    if state.get("mcp_tools"):
        tools_info = "Available tools:\n"
        for tool in state["mcp_tools"]:
            tools_info += f"- {tool['name']}: {tool['description']}\n"
        
        # Add tools info to the system message
        system_message = SystemMessage(content=SYSTEM_PROMPT + "\n\n" + tools_info)
    else:
        system_message = SystemMessage(content=SYSTEM_PROMPT)
    
    # Add tool result if available
    if state.get("tool_result"):
        tool_name = state.get("current_tool", "unknown")
        tool_args = state.get("tool_args", {})
        
        # Format the tool result in a readable way
        try:
            result_json = json.loads(state["tool_result"])
            formatted_result = json.dumps(result_json, indent=2)
        except:
            formatted_result = state["tool_result"]
        
        tool_message = AIMessage(content=f"I executed the '{tool_name}' tool with arguments: {json.dumps(tool_args, indent=2)}\n\nResult:\n```json\n{formatted_result}\n```")
        
        # Add the tool message before generating the response
        all_messages = [system_message] + messages + [tool_message]
    else:
        all_messages = [system_message] + messages
    
    return {"messages": all_messages}

def should_use_tool(state: AgentState) -> str:
    """Determine if a tool should be used based on the last message."""
    last_message = state["messages"][-1]
    
    if last_message.type == "human":
        # Check if the user is asking for data or performing an operation
        content = last_message.content.lower()
        data_keywords = ["list", "show", "get", "find", "search", "query", "display", "fetch"]
        modify_keywords = ["create", "add", "insert", "update", "modify", "change", "delete", "remove"]
        
        if any(keyword in content for keyword in data_keywords + modify_keywords):
            return "select_tool"
    
    # If there's a tool result, we should format the response
    if state.get("tool_result"):
        return "format_response"
    
    # Default to direct response
    return "respond"

def select_tool(state: AgentState):
    """Select the appropriate tool based on user input."""
    messages = state["messages"]
    mcp_tools = state.get("mcp_tools", [])
    
    # Create a prompt to select the tool
    tool_selection_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=f"""
You are an assistant that helps select the appropriate tool based on user input.
Available tools:
{json.dumps(mcp_tools, indent=2)}

Your task is to:
1. Analyze the user's request
2. Select the most appropriate tool from the available tools
3. Provide the necessary arguments for the tool in JSON format

Respond with a JSON object containing:
{{
  "tool": "tool_name",
  "args": {{
    "arg1": "value1",
    "arg2": "value2"
  }}
}}
"""),
        MessagesPlaceholder(variable_name="messages"),
        HumanMessage(content="Based on the conversation above, which tool should I use and what arguments should I provide? Respond in JSON format only.")
    ])
    
    # Create a chain to select the tool
    chain = tool_selection_prompt | llm | StrOutputParser()
    
    # Run the chain
    result = chain.invoke({"messages": messages})
    
    try:
        # Parse the result
        tool_selection = json.loads(result)
        
        # Update the state with the selected tool and arguments
        return {
            "current_tool": tool_selection.get("tool"),
            "tool_args": tool_selection.get("args", {})
        }
    except json.JSONDecodeError:
        # If the result is not valid JSON, return an error
        return {
            "current_tool": None,
            "tool_args": None,
            "tool_result": "Error: Could not parse tool selection"
        }

async def execute_tool(state: AgentState):
    """Execute the selected tool with the provided arguments."""
    tool_name = state.get("current_tool")
    tool_args = state.get("tool_args", {})
    
    if not tool_name:
        return {"tool_result": "Error: No tool selected"}
    
    try:
        # Execute the tool
        result = await execute_mcp_tool(tool_name, tool_args)
        
        # Update the state with the tool result
        return {"tool_result": result}
    except Exception as e:
        # If there's an error, return the error message
        return {"tool_result": f"Error executing tool: {str(e)}"}

def format_response(state: AgentState):
    """Format the response based on the tool result."""
    # The agent_prompt function already adds the tool result to the messages
    # So we just need to generate a response
    
    response_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="messages"),
        HumanMessage(content="Please provide a helpful response based on the tool execution result.")
    ])
    
    # Create a chain to generate the response
    chain = response_prompt | llm | StrOutputParser()
    
    # Run the chain
    result = chain.invoke({"messages": state["messages"]})
    
    # Add the response to the messages
    return {
        "messages": state["messages"] + [AIMessage(content=result)],
        "current_tool": None,
        "tool_args": None,
        "tool_result": None
    }

def respond(state: AgentState):
    """Generate a direct response without using tools."""
    response_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    # Create a chain to generate the response
    chain = response_prompt | llm | StrOutputParser()
    
    # Run the chain
    result = chain.invoke({"messages": state["messages"]})
    
    # Add the response to the messages
    return {
        "messages": state["messages"] + [AIMessage(content=result)]
    }

# Create the graph
def create_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent_prompt", agent_prompt)
    workflow.add_node("select_tool", select_tool)
    workflow.add_node("execute_tool", execute_tool)
    workflow.add_node("format_response", format_response)
    workflow.add_node("respond", respond)
    
    # Add edges
    workflow.add_conditional_edges(
        "agent_prompt",
        should_use_tool,
        {
            "select_tool": "select_tool",
            "format_response": "format_response",
            "respond": "respond"
        }
    )
    workflow.add_edge("select_tool", "execute_tool")
    workflow.add_edge("execute_tool", "format_response")
    workflow.add_edge("format_response", END)
    workflow.add_edge("respond", END)
    
    # Set the entry point
    workflow.set_entry_point("agent_prompt")
    
    return workflow.compile()

# Main function
async def main():
    print("Starting MCP Agent...")
    print("Connecting to MCP server at", MCP_URL)
    
    # Get available tools
    try:
        mcp_tools = await get_mcp_tools()
        print(f"Connected to MCP server. Found {len(mcp_tools)} tools.")
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        sys.exit(1)
    
    # Create the agent
    agent = create_agent_graph()
    
    # Initialize the state
    state = {
        "messages": [],
        "current_tool": None,
        "tool_args": None,
        "tool_result": None,
        "mcp_tools": mcp_tools
    }
    
    print("\nMCP Agent is ready! Type 'exit' to quit.\n")
    
    # Main loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Add the user message to the state
        state["messages"].append(HumanMessage(content=user_input))
        
        # Run the agent
        result = await agent.ainvoke(state)
        
        # Update the state
        state = result
        
        # Print the agent's response
        if state["messages"] and state["messages"][-1].type == "ai":
            print("\nAgent:", state["messages"][-1].content)
            print()

if __name__ == "__main__":
    asyncio.run(main())
