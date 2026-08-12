# Project 1 — Ship an Agent

**Due:** before Day 2 begins. We open Day 2 by debugging real submissions, so
a broken agent you can explain is worth more than no submission.

---

## The task

Build a tool-using agent and deploy it publicly on Hugging Face Spaces.

## Requirements

1. **At least 2 custom tools** you wrote yourself. At least one must hit a real
   API or read real data — not a hardcoded dictionary like the ones in the labs.
2. **A task that genuinely needs 2+ steps.** If a single tool call answers it,
   you've built a wrapper, not an agent. Good test: could a plain chatbot with
   one API do this? If yes, make it harder.
3. **Deployed and public** on HF Spaces, with your token stored as a *secret*.
4. **A `max_steps` guard.** Non-negotiable.

## Deliverables

- Link to your Space (must be running, not "Build error")
- Link to the repo/Space files
- A `README.md` containing **3 example traces** in this shape:

  ```
  Question: <what you asked>
  Thought:  <what the agent reasoned>
  Action:   <tool it called, with args>
  Observation: <what came back>
  ... (more steps)
  Final Answer: <what it said>
  ```

- **3 sentences on what broke.** Which tool did it misuse? Where did it loop?
  What did you change in the docstring to fix it? This section is worth as much
  as the working demo.

## Ideas (pick one or bring your own)

| Idea | Why it's a good fit |
|---|---|
| Campus event finder | Needs search + date filtering + formatting |
| PDF → quiz generator | Needs file reading + generation + validation |
| GitHub repo explainer | Real API, multi-step: fetch → read files → summarise |
| "Should I order out?" | Combines weather + mess menu + a judgement call |
| Placement prep helper | Search a topic, pull questions, rank by difficulty |
| Bus/train time + weather | Two real APIs, genuine multi-step reasoning |

## Rubric (20 marks)

| Criterion | Marks |
|---|---|
| Space is live and responds | 4 |
| 2+ custom tools, one hitting real data | 4 |
| Task genuinely requires multiple steps | 4 |
| 3 traces documented, showing real reasoning | 4 |
| Honest writeup of what broke and why | 4 |

**Bonus (+3):** handle a failure gracefully — a tool that returns an error and
an agent that recovers instead of crashing or looping.

## Rules

- Token in a Space secret, never in `app.py`. We will check.
- Vibe-coding the whole thing is fine — but you must be able to explain every
  line on Day 2. We will ask.
- Pair submissions allowed (max 2 people), both names in the README.

## Getting unstuck

- Space stuck on "Building" → check `requirements.txt` versions
- `401` in Space logs → secret is named wrong; it must be exactly `HF_TOKEN`
- Agent loops → your tool descriptions are ambiguous. Read them as if you were
  the model with no other context.
- Free-tier quota gone → drop `MODEL_ID` to a smaller model, or borrow a
  teammate's token for the demo
