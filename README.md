# AI Agents Workshop — S4DS KJSIT

Two days, six hours, from "what even is an agent" to fine-tuning a model for function calling.

Based on the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course).

---

## Before you arrive (do this the night before)

You will lose 20 minutes of the workshop if you skip this.

1. **Create a Hugging Face account** — https://huggingface.co/join
2. **Create an access token** — https://huggingface.co/settings/tokens
   - Type: **Read** is enough for Day 1 (Labs 0–5)
   - Copy it somewhere safe, you only see it once
3. **Create a DeepSeek API key** — https://platform.deepseek.com/api_keys
   - Needed for the **Day 1 MCP agent labs** (`mcp_03`, `mcp_04`) and Project 2
   - Copy it into `.env` as `DEEPSEEK_API_KEY` (no quotes, no trailing spaces)
4. **Pick your environment** (see below)
5. **Run the setup check** — it must print `ALL CHECKS PASSED`

### Option A — Local (recommended if you have Python 3.10+)

```bash
git clone <this-repo-url>
cd ai-agents-workshop

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Open .env and set:
#   HF_TOKEN=...              (Day 1 Labs 0–5)
#   DEEPSEEK_API_KEY=sk-...   (Day 1 MCP agent labs)
python day1/00_setup_check.py
```


### Option B — Google Colab (fallback, works on any laptop)
day1_labs.ipynb
https://drive.google.com/file/d/1SoLxvw4vsnU4aRYcDEYHN3zeynvWHIuK/view?usp=sharing

day1_labs_gemini
https://drive.google.com/file/d/15QNSDrEQyiJdWp63AvpXF0oAjpQAbp2q/view?usp=sharing

day1_mcp_labs.ipynb
https://drive.google.com/file/d/1pz93SAJJRnmvSVzb8bhDffNoIWqxbwmg/view?usp=sharing

---

## Day 1 — Foundations + ship your first agent

| Lab | File | What you build |
|-----|------|----------------|
| 0 | `day1/00_setup_check.py` | Verify token + connectivity |
| 1 | `day1/01_messages_and_templates.py` | See the raw string the model actually receives |
| 2 | `day1/02_what_is_a_tool.py` | Turn a Python function into a tool description |
| 3 | `day1/03_dummy_agent.py` | **Hand-write the agent loop. No framework.** |
| 4 | `day1/04_first_smolagent.py` | Same thing in 10 lines with smolagents |
| 5 | `day1/05_space/` | Deploy it as a public Gradio Space |

Take-home: **[Project 1](projects/project-1.md)** — due before Day 2 starts.

## Day 1 — MCP (same day extension)

Plug into a real MCP server (Mindicator — Mumbai transit). Agent labs use **DeepSeek**
(`DEEPSEEK_API_KEY` in `.env`).

| Lab | File | What you build |
|-----|------|----------------|
| 0 | `day1/mcp_00_connect.py` | Connect to Mindicator, list tools, health check |
| 1 | `day1/mcp_01_tiny_server.py` | Tiny FastMCP server you create yourself |
| 2 | `day1/mcp_02_see_tools.py` | Print Mindicator tool descriptions |
| 3 | `day1/mcp_03_one_prompt.py` | One agent run over MCP tools (DeepSeek) |
| 4 | `day1/mcp_04_loop.py` | Interactive chat loop (DeepSeek) |
| — | `notebooks/day1_mcp_labs.ipynb` | Colab twin of the MCP labs |

Take-home: **[Project 2](projects/project-2.md)** — Mindicator MCP agent.

Hosted Mindicator URL: see `MINDICATOR_MCP_URL` in `.env.example`.

---

## Troubleshooting

**`401 Unauthorized` (Hugging Face)** — your `HF_TOKEN` is missing or wrong. Check `.env`
has no quotes around the value and no trailing spaces.

**`401 Unauthorized` / auth errors (DeepSeek / MCP agents)** — set `DEEPSEEK_API_KEY` in
`.env` (or Colab secret `DEEPSEEK_API_KEY`). Get a key at
https://platform.deepseek.com/api_keys

**Model 404 (DeepSeek)** — use `DEEPSEEK_MODEL=deepseek-chat`, not a Hugging Face-style
id like `deepseek-ai/...`.

**`Model too busy` / `503`** — free-tier Hugging Face inference is shared. Wait 30 seconds
and retry, or switch `MODEL_ID` in `.env` to a smaller model.

**Rate limited** — the free tier has a monthly credit cap. Once you hit it, use a
Colab runtime with a different account, or pair up with someone who hasn't.

**Agent loops forever** — this is normal and we cover why in Lab 3. Every script
here has a `max_steps` guard so it stops instead of burning your quota.

**MCP connection failed** — check `MINDICATOR_MCP_URL` in `.env` matches the hosted
Mindicator URL, and that transport is `streamable-http`
(see `day1/mcp_00_connect.py`). Wait and retry if the host is briefly unreachable.

---

## License

Teaching material, MIT. Course content adapted from Hugging Face's Agents Course
(Apache 2.0).
