# Project 2 — Compose MCP servers

**Due:** after Day 2 (instructor will set the exact deadline). Day 2 class time
covers *using* Mindicator MCP and fine-tuning — building / combining servers
is this take-home.

---

## The task

Build a tool-using agent that talks to **at least two MCP servers** at once.

One of them **may** be the workshop Mindicator server:

```text
https://personal-mindicatormcp.qbegzg.easypanel.host/mcp
```

(transport: `streamable-http`)

The second can be:

- a **FastMCP server you write** (campus mess, weather, calculator, GitHub, …), or
- another **public / local MCP** you did not write

Wire both into one smolagents agent (`MCPClient` accepts a **list** of configs).

## Requirements

1. **2+ MCP servers** in a single agent run. Tools from both must be loadable.
2. **A task that needs both.** If one server alone can answer, make the question
  harder. Good test: would Mindicator alone finish it? If yes, add a second
   dependency.
3. **A** `max_steps` **guard.** Non-negotiable.
4. **3 example traces** in README (Thought → Action → Observation → … → Final Answer).
5. **3 sentences on what broke** when combining servers — name collisions, bad
  SQL, wrong tool pick, timeouts. Worth as much as the demo.



## Deliverables

- Link to a runnable demo (local instructions OK; Space / public MCP URL is a bonus)
- Repo or folder with agent code + (if any) your FastMCP server code
- `README.md` with the 3 traces + failure writeup
- List of MCP URLs / how to start each server



## Ideas


| Idea                             | Why it needs 2 servers                              |
| -------------------------------- | --------------------------------------------------- |
| Mindicator + campus mess MCP     | Transit + “should I eat out vs mess?”               |
| Mindicator + weather MCP         | Local + rain → leave early or not                   |
| Mindicator + tiny calculator MCP | Fare lookup + arithmetic / split bill               |
| Mindicator + docs/GitHub MCP     | Live train Q + “explain this API”                   |
| Two of your own MCPs             | e.g. mess + placement prep — no Mindicator required |




## Minimal multi-MCP sketch

```python
from smolagents import MCPClient, ToolCallingAgent, InferenceClientModel

servers = [
    {"url": "https://personal-mindicatormcp.qbegzg.easypanel.host/mcp",
     "transport": "streamable-http"},
    {"url": "http://127.0.0.1:8001/mcp", "transport": "streamable-http"},
]

with MCPClient(servers, structured_output=True) as tools:
    agent = ToolCallingAgent(tools=tools, model=model, max_steps=10)
    print(agent.run("...question that needs BOTH servers..."))
```

Building a tiny FastMCP server (homework tip, not required in Day 2 class):

```python
from fastmcp import FastMCP

mcp = FastMCP("campus-mess")

@mcp.tool
def get_mess_menu(day: str) -> str:
    """Hostel mess menu for a weekday. Use for food / mess questions."""
    ...

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)
```





