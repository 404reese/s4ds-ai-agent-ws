# Project 2 — Plug into MCP

**Due:** instructor will announce. This project is the MCP extension of Day 1:
connect to a real MCP server, inspect its tools, ask one good question, then
turn it into a loop.

---

## The task

Build a small agent around the **Mindicator MCP** server.

Your project should follow this exact flow:

1. **Connect** to the Mindicator MCP URL
2. **See the tools** and understand what each one does
3. **Run one good prompt** through an agent
4. **Turn it into a loop** so a user can keep asking questions

Optional stretch: also build a tiny MCP server like `day1/mcp_01_tiny_server.py`
and connect to it (bonus if you use Mindicator + your tiny server together).

Mindicator MCP URL:

```text
https://personal-mindicatormcp.qbegzg.easypanel.host/mcp
```

**API key:** copy `.env.example` → `.env` and set `DEEPSEEK_API_KEY` from
https://platform.deepseek.com/api_keys (same as the MCP labs). On Colab, add a
secret named exactly `DEEPSEEK_API_KEY`.

## Mindicator tools (what you should expect)

| Tool | Purpose |
|------|---------|
| `health_check` | Service + DB meta |
| `get_schema` | Full table/column catalog |
| `execute_sql` | Read-only `SELECT` / `WITH` (LIMIT capped) |
| `get_live_status` | Live running status for a train number |
| `search_stations` | Find stations by name |
| `find_train_path` | Path hints between two stations |
| `get_ticket_fare` | Suburban OD ticket fares |
| `search_bus_routes` | Find bus routes by code/agency |
| `get_bus_route_stops` | Ordered stops on a route |
| `get_auto_fare` | Auto rickshaw day/night fare by km |

Prefer the specialised tools (`find_train_path`, `get_ticket_fare`,
`get_auto_fare`, `get_bus_route_stops`, …). Use `execute_sql` only when no
specialised tool fits.

## Requirements

1. **Use MCPClient** to connect to the server.
2. **Show the available tools** before or during your demo.
3. **Use a real agent** (`ToolCallingAgent` or `CodeAgent`) with a `max_steps` guard.
4. **One task that genuinely needs tool use.** Good examples: route, fare, bus stops,
   live train status.
5. **A looped interface** at the end — terminal loop, Gradio chat, or similar.

## Deliverables

- Your code files
- A short `README.md` explaining the flow:

  ```
  1. Connect
  2. (Optional) tiny MCP server
  3. See tools
  4. One prompt
  5. Loop
  ```

- **3 example traces** in this shape:

  ```
  Question: <what you asked>
  Thought:  <what the agent reasoned>
  Action:   <tool it called>
  Observation: <what came back>
  ...
  Final Answer: <what it said>
  ```

- **3 sentences on what broke.** Which tool did it misuse? Did it pick the wrong
  tool? Did it loop? What did you change?

## Good prompt ideas

| Prompt | Likely tool |
|---|---|
| How do I get from Churchgate to Thane on the local? | `find_train_path` |
| Ticket fare from Churchgate to Thane | `get_ticket_fare` |
| Auto fare for 5 km at night | `get_auto_fare` |
| Stops on BEST bus route `1(Up)` | `get_bus_route_stops` |
| Is train `95338` running late right now? | `get_live_status` |
| Stations matching DADAR | `search_stations` |

## Rubric (20 marks)

| Criterion | Marks |
|---|---|
| Connects to MCP successfully | 4 |
| Clearly shows what tools exist | 4 |
| One good MCP-powered prompt works | 4 |
| Loop / chat interface works | 4 |
| Honest writeup of what broke and why | 4 |

**Bonus (+3):** add a second MCP server of your own and make the agent use both.

## Rules

- Keep `DEEPSEEK_API_KEY` out of committed code.
- Keep a `max_steps` guard.
- Vibe-coding is fine — but you must be able to explain each step of the flow.
- Pair submissions allowed (max 2 people), both names in the README.

## Getting unstuck

- `401` → bad DeepSeek API key
- MCP connection error → check the MCP URL and transport (`streamable-http`)
- Agent gives weak answers → ask a question that actually needs the tools
- Agent invents SQL for simple fare/path questions → tighten instructions to prefer specialised tools
- Agent loops → lower `max_steps` and inspect the tool descriptions
- Live train status empty → try another prompt that uses the offline DB tools instead
- Model 404 → use `DEEPSEEK_MODEL=deepseek-chat`, not a Hugging Face-style id
