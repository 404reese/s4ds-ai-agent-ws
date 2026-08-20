"""
Lab MCP 3 — One prompt, one agent, MCP tools.

This is the same ToolCallingAgent pattern as Day 1 Lab 4.
The difference is only where the tools come from.

Day 1 Lab 4:
    tools=[get_weather, get_mess_menu]

This lab:
    tools come from MCPClient(...)

Setup (.env — copy from .env.example):
  DEEPSEEK_API_KEY=sk-...     # required — https://platform.deepseek.com/api_keys
  DEEPSEEK_MODEL=deepseek-chat  # optional; default is deepseek-chat
  MINDICATOR_MCP_URL=...        # optional; default hosted URL is fine

    python day1/mcp_03_one_prompt.py
"""

import os
import sys

from dotenv import load_dotenv
from smolagents import MCPClient, OpenAIModel, ToolCallingAgent

load_dotenv()

MCP_URL = os.environ.get(
    "MINDICATOR_MCP_URL",
    "https://personal-mindicatormcp.qbegzg.easypanel.host/mcp",
)
MAX_STEPS = 8

# DeepSeek OpenAI-compatible API.
# Valid model ids: deepseek-chat , deepseek-reasoner
# NOT Hugging Face ids like deepseek-ai/...
api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("DEEPSEEK_API_KEY missing. Add it to .env")
    sys.exit(1)

MODEL_ID = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
model = OpenAIModel(
    model_id=MODEL_ID,
    api_base="https://api.deepseek.com/v1",
    api_key=api_key,
)

mcp_config = {
    "url": MCP_URL,
    "transport": "streamable-http",
}

# Extra guidance for the agent — tool *descriptions* come from MCP;
# this tells it HOW to use them for Mumbai transit questions.
INSTRUCTIONS = """
You are a Mumbai transit helper using Mindicator MCP tools.

Prefer the specialised tools first. Use execute_sql only when no specialised
tool fits.

How to choose tools:
- health_check: confirm the server + DB are up
- get_schema: list tables/columns before writing custom SQL
- execute_sql: read-only SELECT/WITH fallback for odd queries (LIMIT capped)
- get_live_status: live running status for a suburban train number (e.g. 95338)
- search_stations: find stations by name
- find_train_path: path hints between two stations (e.g. Churchgate → Thane)
- get_ticket_fare: suburban OD ticket fares between two stations
- search_bus_routes: find bus routes by code/agency
- get_bus_route_stops: ordered stops on a bus route (e.g. BEST 1(Up))
- get_auto_fare: auto rickshaw day/night fare by km

Rules:
- Prefer real tool results over guessing.
- Prefer find_train_path / get_ticket_fare / get_auto_fare / get_bus_route_stops
  over inventing SQL when those tools exist.
- Keep any SQL simple. Use LIMIT. Station names are often UPPERCASE in the DB
  (e.g. CHURCHGATE, THANE, DADAR).
- Answer in a few short sentences for a student.
- If the tools cannot answer, say so clearly.
""".strip()

TASK = "How do I get from Churchgate to Thane on the local train?"

print("=" * 70)
print("ONE PROMPT WITH MINDICATOR MCP")
print("=" * 70)
print(f"MODEL: {MODEL_ID}")
print(f"TASK:  {TASK}")
print()

try:
    with MCPClient(mcp_config, structured_output=True) as tools:
        agent = ToolCallingAgent(
            tools=tools,
            model=model,
            max_steps=MAX_STEPS,
            instructions=INSTRUCTIONS,
        )
        print(agent.run(TASK))
except Exception as exc:  # noqa: BLE001
    print(f"FAILED: {type(exc).__name__}: {exc}")
    print()
    print("Check:")
    print("  - DEEPSEEK_API_KEY in .env")
    print("  - DEEPSEEK_MODEL=deepseek-chat (not a Hugging Face id)")
    print("  - MINDICATOR_MCP_URL is correct")
    print("  - the hosted MCP server is reachable")
    sys.exit(1)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Ask: "Auto fare for 5 km at night."  (get_auto_fare)
# 2. Ask: "Stops on BEST bus route 1(Up)."  (get_bus_route_stops)
# 3. Ask: "Ticket fare from Churchgate to Thane."  (get_ticket_fare)
# 4. Add verbosity_level=2. Watch which specialised tools it picks.
