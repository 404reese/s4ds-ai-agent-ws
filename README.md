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

## Day 2 — Better agents + fine-tuning

Added after Day 1. Covers custom tools, agentic RAG, and LoRA fine-tuning for
function calling.

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

---

## License

Teaching material, MIT. Course content adapted from Hugging Face's Agents Course
(Apache 2.0).
