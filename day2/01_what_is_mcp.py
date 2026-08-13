"""
Lab 1 — What MCP actually is.

Day 1: a tool was a Python function + a docstring, living in YOUR process.
Day 2: the same idea, but the function runs on a SERVER and your agent only
sees the description over HTTP.

MCP = Model Context Protocol. Think USB-for-AI-tools: any MCP client can
plug into any MCP server without custom glue code.

    python day2/01_what_is_mcp.py
"""

import inspect
import os

from dotenv import load_dotenv
from smolagents import MCPClient

load_dotenv()

DEFAULT_URL = "https://personal-mindicatormcp.qbegzg.easypanel.host/mcp"
MCP_URL = os.environ.get("MINDICATOR_MCP_URL", DEFAULT_URL)


# ----------------------------------------------------------------------
# STYLE A — Day 1: tool lives in this file
# ----------------------------------------------------------------------


def get_weather(city: str) -> str:
    """Get the current weather for an Indian city.

    Use whenever the user asks about temperature, rain, or humidity.

    Args:
        city: Name of the city, e.g. "Pune".
    """
    fake = {"mumbai": "32C, humid", "pune": "27C, clear"}
    return fake.get(city.lower().strip(), f"No data for {city}")


def describe_local(func) -> str:
    sig = inspect.signature(func)
    doc = (func.__doc__ or "").strip().split("\n")[0]
    return f"- {func.__name__}{sig}: {doc}"


print("=" * 70)
print("STYLE A — Day 1: in-process tool (function in THIS file)")
print("=" * 70)
print(describe_local(get_weather))
print("  where it runs: your Python process")
print("  how the agent gets it: import + pass to ToolCallingAgent(tools=[...])")
print()

# ----------------------------------------------------------------------
# STYLE B — Day 2: tool lives behind a URL (MCP)
# ----------------------------------------------------------------------

print("=" * 70)
print("STYLE B — Day 2: MCP tool (function on a remote server)")
print("=" * 70)
print(f"  server URL: {MCP_URL}")
print("  where it runs: Mindicator host (SQLite + live train API)")
print("  how the agent gets it: MCPClient → get_tools()")
print()

mcp_config = {"url": MCP_URL, "transport": "streamable-http"}

with MCPClient(mcp_config, structured_output=True) as tools:
    print("  tools this server exposes:")
    for t in tools:
        desc = (t.description or "").strip().split("\n")[0]
        print(f"    - {t.name}: {desc}")

print()
print("=" * 70)
print("THE POINT")
print("=" * 70)
print(
    "Same ReAct loop as Day 1. Same max_steps guard.\n"
    "The only change: tool *implementations* can live anywhere MCP reaches.\n"
    "Your docstring (or the server's tool description) is STILL the prompt\n"
    "the model uses to decide which tool to call.\n"
    "\n"
    "Mindicator wraps Mumbai transit data as four tools:\n"
    "  health_check, get_schema, execute_sql, get_live_status\n"
    "execute_sql is agentic retrieval — the MODEL decides what to query,\n"
    "not a hand-stuffed RAG prompt."
)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Without looking at the server code, read only the tool descriptions.
#    Could you pick the right tool for "is train 95338 late?"
# 2. Compare get_weather's docstring to execute_sql's description. Which is
#    more specific about WHEN to use it?
# 3. Sketch (on paper) a second MCP server you might build for campus mess
#    menus. What 2 tools would it expose? (Project 2 asks for 2+ servers.)
