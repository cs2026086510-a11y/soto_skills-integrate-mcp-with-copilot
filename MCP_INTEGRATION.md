# GitHub Copilot MCP Integration Guide

This project integrates the Model Context Protocol (MCP) to give GitHub Copilot access to the Mergington High School activities management system.

## Overview

The MCP server (`src/mcp_server.py`) exposes the school activities API as tools that GitHub Copilot can use to:
- List all available activities
- View activity details
- Manage student activity registrations
- Check activity availability

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Running the Services

**Option A: Run the FastAPI server**
```bash
cd src
python app.py
```
This starts the REST API on http://localhost:8000

**Option B: Run the MCP server**
```bash
cd src
python mcp_server.py
```
This starts the MCP server for Copilot integration

## Available MCP Tools

The MCP server exposes the following tools to GitHub Copilot:

### 1. `list_activities`
Lists all available extracurricular activities with their details and current enrollment.

**Usage**: Ask Copilot to "Show me all available activities at Mergington High School"

### 2. `get_activity_details`
Retrieves detailed information about a specific activity.

**Parameters**:
- `activity_name` (string): Name of the activity

**Usage**: Ask Copilot to "Tell me about the Chess Club"

### 3. `signup_for_activity`
Signs up a student for an activity.

**Parameters**:
- `activity_name` (string): Name of the activity
- `email` (string): Student's email address

**Usage**: Ask Copilot to "Sign up john@mergington.edu for Programming Class"

### 4. `unregister_from_activity`
Unregisters a student from an activity.

**Parameters**:
- `activity_name` (string): Name of the activity
- `email` (string): Student's email address

**Usage**: Ask Copilot to "Unregister john@mergington.edu from Programming Class"

### 5. `get_activity_availability`
Checks how many spots are available in a specific activity.

**Parameters**:
- `activity_name` (string): Name of the activity

**Usage**: Ask Copilot to "How many spots are available in the Basketball Team?"

## Configuring Copilot in VS Code

To use the MCP server with GitHub Copilot in VS Code:

1. Open VS Code settings (Cmd/Ctrl + ,)
2. Search for "Copilot" settings
3. Look for MCP server configuration options
4. Configure the MCP server path to point to `src/mcp_server.py`

Alternatively, you can set environment variable:
```bash
export MCP_SERVER_PATH=/path/to/src/mcp_server.py
```

## Example Copilot Interactions

Here are some natural language queries you can use with Copilot now:

- "What activities are available at Mergington High School?"
- "Show me all activities with available spots"
- "Sign emma@mergington.edu up for Art Club"
- "How many students are in Chess Club?"
- "Remove michael@mergington.edu from Soccer Team"
- "Which activities are full?"

## Architecture

```
┌─────────────────────┐
│ GitHub Copilot      │
│ (VS Code)           │
└──────────┬──────────┘
           │
           │ MCP Protocol
           │
┌──────────▼──────────┐
│ MCP Server          │
│ (mcp_server.py)     │
└──────────┬──────────┘
           │
           │ Direct API calls
           │
┌──────────▼──────────┐
│ FastAPI Server      │
│ (app.py)            │
└─────────────────────┘
```

## Data Model

Activities are stored in-memory and contain:
- **name**: Activity identifier
- **description**: What the activity is about
- **schedule**: When the activity meets
- **max_participants**: Maximum number of students allowed
- **participants**: List of emails of registered students

## Note

This demonstration uses in-memory storage. In a production environment, you would connect to a persistent database for data storage.