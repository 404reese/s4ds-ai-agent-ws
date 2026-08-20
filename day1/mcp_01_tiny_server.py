"""
Lab MCP 1 — Create a tiny MCP server.

Day 1 Lab 2: @tool turns a function into something an agent can call.
MCP: @mcp.tool does the same thing — but on a server anyone can connect to.

This file is a complete mini server with 2 tools (hostel mess).
Run it in one terminal, then point an MCPClient at it from another.

Setup (.env — copy from .env.example):
  DEEPSEEK_API_KEY=...   # not required to run this server; needed when an
                         # agent (mcp_03 / mcp_04) talks to it

    Terminal A:
        python day1/mcp_01_tiny_server.py

    Terminal B (example):
        # url = http://127.0.0.1:8001/mcp
"""

from fastmcp import FastMCP

mcp = FastMCP("campus-mess")


@mcp.tool
def get_mess_menu(day: str) -> str:
    """Get the hostel mess menu for a weekday.

    Use this for food / mess / dining questions.

    Args:
        day: Day name, e.g. "Monday" or "Tuesday".
    """
    menu = {
        "monday": "Rajma chawal, salad, curd",
        "tuesday": "Pav bhaji, kheer",
        "wednesday": "Veg biryani, raita",
        "thursday": "Chole bhature",
        "friday": "Masala dosa, sambar",
    }
    return menu.get(day.lower().strip(), f"No menu listed for {day}")


@mcp.tool
def is_mess_open(time_str: str) -> str:
    """Check if the hostel mess is open at a given time.

    Args:
        time_str: Time in HH:MM 24h format, e.g. "13:30".
    """
    try:
        hour = int(time_str.split(":")[0])
    except Exception:  # noqa: BLE001
        return "Could not parse time. Use HH:MM, e.g. 13:30."

    if 7 <= hour < 10 or 12 <= hour < 15 or 19 <= hour < 22:
        return f"Mess is OPEN at {time_str}."
    return f"Mess is CLOSED at {time_str}."


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8001
    url = f"http://{host}:{port}/mcp"

    print("=" * 70)
    print("YOU CREATED YOUR MCP SERVER")
    print("=" * 70)
    print()
    print("Name:   campus-mess")
    print("Tools:")
    print("  - get_mess_menu(day)     → hostel mess menu for a weekday")
    print("  - is_mess_open(time_str) → whether mess is open at HH:MM")
    print()
    print(f"URL:    {url}")
    print("Transport: streamable-http")
    print()
    print("Plug this URL into an MCPClient (other terminal / notebook):")
    print()
    print("  from smolagents import MCPClient")
    print()
    print("  mcp_config = {")
    print(f'      "url": "{url}",')
    print('      "transport": "streamable-http",')
    print("  }")
    print()
    print("  with MCPClient(mcp_config, structured_output=True) as tools:")
    print("      for t in tools:")
    print("          print(t.name)")
    print()
    print("Keep THIS terminal running. Ctrl+C to stop the server.")
    print("=" * 70)
    print()
    mcp.run(transport="http", host=host, port=port)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Start this server. In another terminal, reuse mcp_00_connect.py but set
#    MINDICATOR_MCP_URL=http://127.0.0.1:8001/mcp and list tools.
# 2. Add a third tool, e.g. get_hostel_wifi_password(day).
# 3. Compare @mcp.tool here with @tool in day1/04_first_smolagent.py —
#    same idea, different place the function lives.
