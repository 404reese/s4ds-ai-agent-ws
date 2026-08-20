"""
Lab MCP 0 — Connect to an MCP server.

Day 1 tools lived inside your Python file. Here the tools live on a server and
you load them through a client.

This first script does only three things:
  1. connect
  2. list the tools
  3. call health_check

Setup (.env — copy from .env.example):
  DEEPSEEK_API_KEY=...   # needed from mcp_03 onward (agent labs)
  MINDICATOR_MCP_URL=... # optional; default hosted URL is fine

    python day1/mcp_00_connect.py
"""

import os
import sys

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
print("MCP CONNECT")
print("=" * 70)
print(f"URL: {MCP_URL}")
print()

try:
    with MCPClient(mcp_config, structured_output=True) as tools:
        print(f"Connected. {len(tools)} tool(s):\n")
        for tool in tools:
            first_line = (tool.description or "").strip().split("\n")[0]
            print(f"  - {tool.name}: {first_line}")

        by_name = {tool.name: tool for tool in tools}
        print("\nhealth_check:")
        print(by_name["health_check"]())
except Exception as exc:  # noqa: BLE001
    print(f"FAILED: {type(exc).__name__}: {exc}")
    print()
    print("Check:")
    print("  - pip install -r requirements.txt")
    print("  - MINDICATOR_MCP_URL points at a working MCP URL")
    print("  - transport is streamable-http")
    print("  - you can reach the host from this machine")
    sys.exit(1)

print()
print("=" * 70)
print("READY — next: build a tiny MCP server (mcp_01_tiny_server.py).")
print("=" * 70)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Call get_schema() too. How big is the catalog?
# 2. Call search_stations with a partial name like "DADAR".
# 3. Change the URL to something wrong. What error do you get?
# 4. Open the MCP URL in a browser. Why doesn't it look like a normal site?
