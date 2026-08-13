# AI Agents Workshop — S4DS KJSIT

Two days, six hours, from "what even is an agent" to fine-tuning a model for function calling.

Based on the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course).

---

## Before you arrive (do this the night before)

You will lose 20 minutes of the workshop if you skip this.

1. **Create a Hugging Face account** — https://huggingface.co/join
2. **Create an access token** — https://huggingface.co/settings/tokens
   - Type: **Read** is enough for Day 1
   - Copy it somewhere safe, you only see it once
3. **Pick your environment** (see below)
4. **Run the setup check** — it must print `ALL CHECKS PASSED`

### Option A — Local (recommended if you have Python 3.10+)

```bash
git clone <this-repo-url>
cd ai-agents-workshop

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env             # then open .env and paste your token
python day1/00_setup_check.py
```

### Option B — Google Colab (fallback, works on any laptop)

Open `notebooks/day1_labs.ipynb` in Colab and run the first cell. Add your token
via the key icon in the left sidebar (Secrets → name it `HF_TOKEN` → toggle
notebook access on).

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

## Day 2 — MCP (use) then fine-tuning

First half: plug into a real MCP server (Mindicator — Mumbai transit). Second half:
why fine-tune, LoRA intuition, and a Colab LoRA SFT lab.

| Lab | File | What you build |
|-----|------|----------------|
| 0 | `day2/00_mcp_ping.py` | Connect to Mindicator MCP, list tools, health check |
| 1 | `day2/01_what_is_mcp.py` | Day-1 in-process tool vs MCP tool over HTTP |
| 2 | `day2/02_mindicator_agent.py` | smolagents agent over Mindicator (agentic SQL) |
| — | `notebooks/day2_labs.ipynb` | Colab twin of the MCP labs |
| — | `notebooks/day2_lora.ipynb` | Post-break Colab: LoRA SFT with TRL |

Take-home: **[Project 2](projects/project-2.md)** — compose 2+ MCP servers.

Hosted Mindicator URL: see `MINDICATOR_MCP_URL` in `.env.example`.

LoRA notebook installs its own training deps inside Colab (`trl`, `peft`, etc.) —
you do not need a GPU for the MCP labs.

---

## Troubleshooting

**`401 Unauthorized`** — your token is missing or wrong. Check `.env` has no
quotes around the value and no trailing spaces.

**`Model too busy` / `503`** — free-tier inference is shared. Wait 30 seconds and
retry, or switch `MODEL_ID` in `.env` to a smaller model.

**Rate limited** — the free tier has a monthly credit cap. Once you hit it, use a
Colab runtime with a different account, or pair up with someone who hasn't.

**Agent loops forever** — this is normal and we cover why in Lab 3. Every script
here has a `max_steps` guard so it stops instead of burning your quota.

**MCP connection failed (Day 2)** — check `MINDICATOR_MCP_URL` in `.env` matches
the hosted Mindicator URL, and that transport is `streamable-http`
(see `day2/00_mcp_ping.py`). Wait and retry if the host is briefly unreachable.

---

## License

Teaching material, MIT. Course content adapted from Hugging Face's Agents Course
(Apache 2.0).
