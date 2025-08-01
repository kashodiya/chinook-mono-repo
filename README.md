# Chinook Monorepo

This monorepo contains multiple projects related to the Chinook database system, demonstrating how to build a natural language interface to a database using the Model Context Protocol (MCP).

## Projects

### chinook-crud-api

A FastAPI-based CRUD API for the Chinook SQLite database, providing RESTful endpoints for database operations.

### chinook-crud-api-mcp

An MCP implementation that connects an LLM agent to the Chinook database API, enabling natural language interaction with the database.

> **Note**: While the repository metadata mentions Node.js, Express, and PostgreSQL, the current implementation uses Python, FastAPI, and SQLite.

## Architecture

The monorepo follows a layered architecture:

1. **Data Layer**: SQLite database with tables for artists, albums, tracks, etc.
2. **API Layer**: FastAPI server providing RESTful endpoints
3. **MCP Layer**: FastMCP server implementing the Model Context Protocol
4. **Agent Layer**: LangChain-based conversational agent using Claude 3

## Key Features

- **Natural Language Database Access**: Query, create, update, and delete records using conversational language
- **MCP Integration**: Standardized protocol for connecting LLMs to tools and data sources
- **LangGraph State Machine**: Sophisticated conversation flow management
- **Comprehensive Database Schema**: Digital media store with artists, albums, tracks, customers, and sales data

## Example Usage

```
You: Show me the top 5 artists with the most albums
Agent: Here are the top 5 artists with the most albums:

1. Iron Maiden - 21 albums
2. U2 - 10 albums
3. Led Zeppelin - 9 albums
4. Deep Purple - 8 albums
5. Metallica - 7 albums
```

## Getting Started

Each project has its own README with specific setup instructions. The general flow is:

1. Start the CRUD API server
2. Start the MCP server (depends on the CRUD API server being running)
3. Run the MCP agent for natural language interaction (depends on the MCP server being running)

**Important**: There are dependencies between these components:
- The MCP server depends on the CRUD API server to be running first
- The MCP agent depends on the MCP server to be running first

Make sure to start the services in the correct order to ensure proper functionality.

## Repository Structure

```
chinook-mono-repo/
├── chinook-crud-api/        # Core CRUD API
├── chinook-crud-api-mcp/    # MCP implementation
└── .openhands/              # Repository metadata
```

## Development

The monorepo uses coordinated versioning to ensure compatibility between projects. Each project can be developed and deployed independently or as part of a coordinated release.

## OpenHands

This project is primarily developed by OpenHands AI. The `.openhands/microagents/repo.md` file contains additional metadata.
