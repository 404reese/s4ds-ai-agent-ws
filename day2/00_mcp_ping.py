"""
Lab 0 — Ping the Mindicator MCP server.

Day 1 tools lived inside your Python file. Day 2 tools live behind a URL.
This script only checks that the plug works: connect, list tools, health_check.

    python day2/00_mcp_ping.py
"""

import os
import sys

from dotenv import load_dotenv
from smolagents import MCPClient

load_dotenv()

DEFAULT_URL = "https://personal-mindicatormcp.qbegzg.easypanel.host/mcp"
MCP_URL = os.environ.get("MINDICATOR_MCP_URL", DEFAULT_URL)

mcp_config = {
    "url": MCP_URL,
    "transport": "streamable-http",  # FastMCP HTTP — do not use "sse"
}

print("=" * 70)
print("MINDICATOR MCP — ping")
print("=" * 70)
print(f"URL: {MCP_URL}")
print()

try:
    with MCPClient(mcp_config, structured_output=True) as tools:
        print(f"Connected. {len(tools)} tool(s):\n")
        for t in tools:
            desc = (t.description or "").strip().split("\n")[0]
            print(f"  - {t.name}: {desc}")

        by_name = {t.name: t for t in tools}
        if "health_check" not in by_name:
            print("\n[!] No health_check tool — unexpected server?")
            sys.exit(1)

        print("\nCalling health_check ...")
        result = by_name["health_check"]()
        print(result)
except Exception as exc:  # noqa: BLE001
    print(f"\nFAILED: {type(exc).__name__}: {exc}")
    print(
        "\nFix:\n"
        "  - Check MINDICATOR_MCP_URL in .env (hosted Mindicator URL).\n"
        "  - Transport must be streamable-http for FastMCP HTTP.\n"
        "  - pip install -r requirements.txt  (needs smolagents[mcp])\n"
        "  - Host briefly unreachable? Wait and retry."
    )
    sys.exit(1)

print()
print("=" * 70)
print("PING OK — ready for Lab 1 / Lab 2.")
print("=" * 70)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Typo the host in MINDICATOR_MCP_URL. What error do you get?
# 2. Call get_schema instead of health_check. How big is the catalog?
# 3. Open the URL in a browser — MCP is not a website. 406 / odd responses
#    are normal; the client speaks the MCP protocol, not plain GET HTML.
