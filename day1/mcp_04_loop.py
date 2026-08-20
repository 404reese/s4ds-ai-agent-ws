"""
Lab MCP 4 — Put the MCP agent in a loop.

One prompt is useful, but a chatbot is just that same agent called again and
again. This script gives you a tiny REPL over the Mindicator MCP tools.

Type 'quit' to stop.

Setup (.env — copy from .env.example):
  DEEPSEEK_API_KEY=sk-...     # required — https://platform.deepseek.com/api_keys
  DEEPSEEK_MODEL=deepseek-chat  # optional; default is deepseek-chat
  MINDICATOR_MCP_URL=...        # optional; default hosted URL is fine

    python day1/mcp_04_loop.py
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

print("=" * 70)
print("MINDICATOR CHAT LOOP")
print("=" * 70)
print("Ask about Mumbai trains, buses, fares, or a live train number.")
print("Type 'quit' to stop.")
print()

try:
    with MCPClient(mcp_config, structured_output=True) as tools:
        agent = ToolCallingAgent(
            tools=tools,
            model=model,
            max_steps=MAX_STEPS,
            instructions=INSTRUCTIONS,
        )

        while True:
            question = input("You: ").strip()
            if question.lower() in {"quit", "exit", "q"}:
                print("Bye.")
                break
            if not question:
                continue

            print()
            print("Agent:")
            print(agent.run(question))
            print()
except KeyboardInterrupt:
    print("\nStopped.")
except Exception as exc:  # noqa: BLE001
    print(f"FAILED: {type(exc).__name__}: {exc}")
    sys.exit(1)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Ask one train path, one auto fare, and one bus-stops question.
# 2. Ask something the server cannot answer. Does it admit that limitation?
# 3. Lower MAX_STEPS to 2. What kinds of questions start failing?
