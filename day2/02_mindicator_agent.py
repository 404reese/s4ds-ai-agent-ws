"""
Lab 2 — A real agent over Mindicator MCP.

Same smolagents loop as Day 1 Lab 4 — but every tool comes from the hosted
Mindicator server (Mumbai locals, buses, fares, live train status).

The big idea: execute_sql is retrieval-as-a-tool. The model decides what to
fetch from the DB. That is agentic RAG without a vector store lecture.

    python day2/02_mindicator_agent.py
"""

import os
import sys

from dotenv import load_dotenv
from smolagents import InferenceClientModel, MCPClient, ToolCallingAgent

load_dotenv()

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")
DEFAULT_URL = "https://personal-mindicatormcp.qbegzg.easypanel.host/mcp"
MCP_URL = os.environ.get("MINDICATOR_MCP_URL", DEFAULT_URL)
MAX_STEPS = 8

token = os.environ.get("HF_TOKEN")
if not token:
    print("HF_TOKEN missing. Copy .env.example → .env and paste your token.")
    sys.exit(1)

mcp_config = {"url": MCP_URL, "transport": "streamable-http"}

TASK = (
    "How do I get from Churchgate to Thane on the local train? "
    "Also give a rough ticket fare if the data has it. "
    "Answer in a few short sentences."
)

print("=" * 70)
print("MINDICATOR AGENT")
print("=" * 70)
print(f"MCP:   {MCP_URL}")
print(f"MODEL: {MODEL_ID}")
print(f"TASK:  {TASK}")
print()

model = InferenceClientModel(model_id=MODEL_ID, token=token)

try:
    with MCPClient(mcp_config, structured_output=True) as tools:
        print("Tools loaded:")
        for t in tools:
            print(f"  - {t.name}")
        print()

        agent = ToolCallingAgent(
            tools=tools,
            model=model,
            max_steps=MAX_STEPS,
        )
        answer = agent.run(TASK)
except Exception as exc:  # noqa: BLE001
    print(f"FAILED: {type(exc).__name__}: {exc}")
    print(
        "\nTips:\n"
        "  - 401 → bad HF_TOKEN\n"
        "  - connection error → check MINDICATOR_MCP_URL; wait and retry\n"
        "  - model busy → change MODEL_ID in .env\n"
        "  - agent loops → max_steps already caps it; try a narrower question"
    )
    sys.exit(1)

print()
print("=" * 70)
print("FINAL ANSWER")
print("=" * 70)
print(answer)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Swap TASK to: "What is the auto rickshaw fare for about 5 km at night?"
# 2. Swap TASK to: "Is train 95338 running late right now?"
#    (uses get_live_status — live HTTP, may be slow or empty off-peak)
# 3. Add verbosity_level=2 to ToolCallingAgent. Watch it call get_schema
#    and/or execute_sql. That SQL is the model choosing what to retrieve.
# 4. Ask something the DB cannot answer ("who won the 2019 world cup?").
#    Does it invent SQL, or admit it can't help?
