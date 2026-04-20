"""
MCP (Model Context Protocol) Server for Mergington High School Activities API

Exposes school activities as tools that GitHub Copilot can use to:
- View available activities
- Sign up students for activities
- Unregister students from activities
"""

import asyncio
import json
from typing import Any
from mcp.server import Server, ErrorCode
from mcp.types import (
    TextContent,
    Tool,
    ToolResult,
)

# Import the activities data from the FastAPI app
# In production, these would be fetched from the API
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


# Create the MCP server
server = Server("mergington-activities")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for managing school activities"""
    return [
        Tool(
            name="list_activities",
            description="Get a list of all available extracurricular activities at Mergington High School with their details and current participant counts",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_activity_details",
            description="Get detailed information about a specific activity including participants, schedule, and availability",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "The name of the activity (e.g., 'Chess Club', 'Programming Class')"
                    }
                },
                "required": ["activity_name"]
            }
        ),
        Tool(
            name="signup_for_activity",
            description="Sign up a student for an extracurricular activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "The name of the activity to sign up for"
                    },
                    "email": {
                        "type": "string",
                        "description": "The student's email address (must be @mergington.edu)"
                    }
                },
                "required": ["activity_name", "email"]
            }
        ),
        Tool(
            name="unregister_from_activity",
            description="Unregister a student from an extracurricular activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "The name of the activity to unregister from"
                    },
                    "email": {
                        "type": "string",
                        "description": "The student's email address"
                    }
                },
                "required": ["activity_name", "email"]
            }
        ),
        Tool(
            name="get_activity_availability",
            description="Check how many spots are available in a specific activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_name": {
                        "type": "string",
                        "description": "The name of the activity to check"
                    }
                },
                "required": ["activity_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from Copilot"""
    
    if name == "list_activities":
        activity_list = []
        for activity_name, activity_data in activities.items():
            participants = len(activity_data["participants"])
            max_participants = activity_data["max_participants"]
            availability = max_participants - participants
            activity_list.append(
                f"• {activity_name}: {activity_data['description']} "
                f"(Schedule: {activity_data['schedule']}, "
                f"Participants: {participants}/{max_participants}, "
                f"Available spots: {availability})"
            )
        
        result = "Available Activities at Mergington High School:\n\n" + "\n".join(activity_list)
        return [TextContent(type="text", text=result)]
    
    elif name == "get_activity_details":
        activity_name = arguments.get("activity_name")
        if activity_name not in activities:
            return [TextContent(
                type="text",
                text=f"Error: Activity '{activity_name}' not found."
            )]
        
        activity = activities[activity_name]
        participants_count = len(activity["participants"])
        available_spots = activity["max_participants"] - participants_count
        
        details = f"""
Activity: {activity_name}
Description: {activity['description']}
Schedule: {activity['schedule']}
Max Participants: {activity['max_participants']}
Current Participants: {participants_count}
Available Spots: {available_spots}
Registered Students:
{chr(10).join(['  - ' + p for p in activity['participants']])}
"""
        return [TextContent(type="text", text=details)]
    
    elif name == "signup_for_activity":
        activity_name = arguments.get("activity_name")
        email = arguments.get("email")
        
        if activity_name not in activities:
            return [TextContent(type="text", text=f"Error: Activity '{activity_name}' not found.")]
        
        activity = activities[activity_name]
        
        if email in activity["participants"]:
            return [TextContent(type="text", text=f"Error: {email} is already signed up for {activity_name}."))
        
        if len(activity["participants"]) >= activity["max_participants"]:
            return [TextContent(type="text", text=f"Error: {activity_name} is full. Maximum participants ({activity['max_participants']}) reached.")]
        
        activity["participants"].append(email)
        return [TextContent(
            type="text",
            text=f"Success: {email} has been signed up for {activity_name}."
        )]
    
    elif name == "unregister_from_activity":
        activity_name = arguments.get("activity_name")
        email = arguments.get("email")
        
        if activity_name not in activities:
            return [TextContent(type="text", text=f"Error: Activity '{activity_name}' not found.")]
        
        activity = activities[activity_name]
        
        if email not in activity["participants"]:
            return [TextContent(type="text", text=f"Error: {email} is not signed up for {activity_name}."))
        
        activity["participants"].remove(email)
        return [TextContent(
            type="text",
            text=f"Success: {email} has been unregistered from {activity_name}."
        )]
    
    elif name == "get_activity_availability":
        activity_name = arguments.get("activity_name")
        
        if activity_name not in activities:
            return [TextContent(type="text", text=f"Error: Activity '{activity_name}' not found.")]
        
        activity = activities[activity_name]
        participants = len(activity["participants"])
        max_participants = activity["max_participants"]
        available = max_participants - participants
        
        status = "FULL" if available == 0 else f"{available} spots available"
        
        return [TextContent(
            type="text",
            text=f"{activity_name}: {participants}/{max_participants} participants ({status})"
        )]
    
    return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def main():
    """Run the MCP server"""
    async with server:
        print("Mergington High School Activities MCP Server started")
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())