"""
Lab 3 — Build the agent loop by hand. No framework.

This is the most important 40 minutes of the workshop. Once you've written
this, smolagents / LangGraph / CrewAI stop being magic — they are all this
same while-loop with better error handling.

The loop:

    Thought      -> the model reasons about what to do
    Action       -> the model writes a tool call as TEXT
    Observation  -> YOUR code runs the tool and pastes the result back
    ...repeat until the model writes a Final Answer

    python day1/03_dummy_agent.py
"""

import os
import re

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")
MAX_STEPS = 6  # guard rail: without this, a confused agent bills you forever

client = InferenceClient(model=MODEL_ID, token=os.environ["HF_TOKEN"])

# ----------------------------------------------------------------------
# The tools. Same idea as Lab 2.
# ----------------------------------------------------------------------


def get_weather(city: str) -> str:
    fake = {"mumbai": "32C, humid", "pune": "27C, clear", "delhi": "38C, hazy"}
    return fake.get(city.lower().strip(), f"No weather data for {city}")


def calculate(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only numbers and + - * / ( ) allowed."
    try:
        return str(eval(expression))  # noqa: S307
    except Exception as exc:  # noqa: BLE001
        return f"Error: {exc}"


TOOLS = {"get_weather": get_weather, "calculate": calculate}

SYSTEM_PROMPT = """You solve tasks by reasoning step by step and using tools.

Available tools:
- get_weather(city): current weather for an Indian city. Use for any question \
about temperature, rain, or humidity.
- calculate(expression): evaluate arithmetic. Use for any maths.

You must reply in exactly this format, one step at a time:

Thought: <your reasoning about what to do next>
Action: <tool_name>(<single argument>)

After each Action you will be shown an Observation with the result.
Continue with more Thought/Action steps until you can answer.

When you are done, reply with exactly:

Thought: <why you are now able to answer>
Final Answer: <your answer to the user>

Never write an Observation yourself — that is given to you.
Never write more than one Action per reply."""


# ----------------------------------------------------------------------
# The loop. This is the entire "agent".
# ----------------------------------------------------------------------

ACTION_RE = re.compile(r"Action:\s*(\w+)\((.*?)\)", re.DOTALL)


def run(task: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]

    for step in range(1, MAX_STEPS + 1):
        print(f"\n{'-' * 60}\nSTEP {step}\n{'-' * 60}")

        response = client.chat.completions.create(
            messages=messages,
            max_tokens=400,
            # CRUCIAL: stop before the model hallucinates its own Observation.
            stop=["Observation:"],
        )
        output = response.choices[0].message.content.strip()
        print(output)

        messages.append({"role": "assistant", "content": output})

        # Done?
        if "Final Answer:" in output:
            return output.split("Final Answer:", 1)[1].strip()

        # Tool call?
        match = ACTION_RE.search(output)
        if not match:
            nudge = (
                "You did not produce a valid Action. Reply with either "
                "'Action: tool_name(arg)' or 'Final Answer: ...'."
            )
            print(f"\n[!] {nudge}")
            messages.append({"role": "user", "content": nudge})
            continue

        name, raw_arg = match.group(1), match.group(2).strip().strip("\"'")

        if name not in TOOLS:
            observation = f"Error: no tool named '{name}'. Available: {list(TOOLS)}"
        else:
            try:
                observation = TOOLS[name](raw_arg)
            except Exception as exc:  # noqa: BLE001
                observation = f"Error running {name}: {exc}"

        print(f"\nObservation: {observation}")
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "Gave up — hit MAX_STEPS without reaching a final answer."


if __name__ == "__main__":
    task = (
        "What's the weather in Pune right now, and if I add 5 degrees to the "
        "temperature, what do I get?"
    )
    print(f"TASK: {task}")
    answer = run(task)
    print(f"\n{'=' * 60}\nFINAL ANSWER: {answer}\n{'=' * 60}")

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Remove stop=["Observation:"]. Run again. The model will invent its own
#    observations and confidently hallucinate the weather. This single line
#    is the difference between an agent and a liar.
#
# 2. Set MAX_STEPS = 2 and ask a question needing 3 steps. See the failure.
#
# 3. Ask something with NO tool for it: "who won the 2019 cricket world cup?"
#    Does it answer from memory, or try to force a tool? What would you want?
#
# 4. Break the format on purpose: change "Action:" to "Act:" in SYSTEM_PROMPT
#    but leave the regex alone. Watch the nudge path kick in. Real agents
#    spend most of their code on exactly this kind of recovery.
