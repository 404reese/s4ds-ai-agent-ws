"""
Lab MCP 2 — See what an MCP server exposes.

Day 1 taught: a tool is a function + a description.
MCP keeps the same idea, but the function lives on a server.

This script asks one question only:
    what tools does the Mindicator MCP server expose?

Expect specialised Mumbai-transit tools such as find_train_path,
get_ticket_fare, get_auto_fare, get_bus_route_stops, get_live_status,
plus get_schema / execute_sql as a fallback.

Setup (.env — copy from .env.example):
  DEEPSEEK_API_KEY=...   # needed from mcp_03 onward (agent labs)
  MINDICATOR_MCP_URL=... # optional; default hosted URL is fine

    python day1/mcp_02_see_tools.py
"""

import os

from dotenv import load_dotenv
from smolagents import MCPClient

load_dotenv()

MCP_URL = os.environ.get(
    "MINDICATOR_MCP_URL",
    "https://personal-mindicatormcp.qbegzg.easypanel.host/mcp",
)

mcp_config = {
    "url": MCP_URL,
    "transport": "streamable-http",
}

print("=" * 70)
print("MINDICATOR MCP — WHAT TOOLS EXIST?")
print("=" * 70)

with MCPClient(mcp_config, structured_output=True) as tools:
    for tool in tools:
        print(f"\n{tool.name}")
        print("-" * len(tool.name))
        print((tool.description or "(no description)").strip())

print()
print("The point:")
print(
    "The model never sees your Python implementation. It only sees these names\n"
    "and descriptions. MCP changes WHERE the function lives, not what the model\n"
    "needs in order to choose it."
)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Which tool for "Is train 95338 late?"          -> get_live_status
# 2. Which tool for "Churchgate to Thane path?"      -> find_train_path
# 3. Which tool for "Auto fare for 5 km at night?"   -> get_auto_fare
# 4. Which tool for "Stops on BEST bus route 1(Up)?" -> get_bus_route_stops
# 5. When would you still use execute_sql?

