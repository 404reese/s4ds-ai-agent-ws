"""
Lab 4 — The same agent, in 15 lines, with smolagents.

Everything you wrote by hand in Lab 3 is here:
  - the system prompt with tool descriptions  -> generated from @tool
  - the parse-the-output regex                -> built in
  - the observation feedback loop             -> built in
  - the MAX_STEPS guard                       -> max_steps=

The difference between CodeAgent and ToolCallingAgent is only HOW the model
writes its action:

    ToolCallingAgent  ->  {"name": "get_weather", "arguments": {"city": "Pune"}}
    CodeAgent         ->  weather = get_weather("Pune")
                          print(weather + 5)

CodeAgent is usually stronger for multi-step work — one block of Python can do
what three JSON tool calls would, and LLMs are very good at writing Python.

    python day1/04_first_smolagent.py
"""

import os

from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, ToolCallingAgent, tool

load_dotenv()

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")


# ----------------------------------------------------------------------
# Tools. The docstring and type hints ARE the spec sent to the model.
# Write them like you're writing a prompt, because you are.
# ----------------------------------------------------------------------


@tool
def get_weather(city: str) -> str:
    """Get the current weather for an Indian city.

    Use this whenever the user asks about temperature, rain, or humidity.

    Args:
        city: Name of the city, e.g. "Pune".
    """
    fake = {"mumbai": "32C, humid", "pune": "27C, clear", "delhi": "38C, hazy"}
    return fake.get(city.lower().strip(), f"No weather data for {city}")


@tool
def get_mess_menu(day: str) -> str:
    """Get the hostel mess menu for a given day of the week.

    Args:
        day: Day name, e.g. "Monday".
    """
    menu = {
        "monday": "Rajma chawal, salad, curd",
        "tuesday": "Pav bhaji, kheer",
        "wednesday": "Veg biryani, raita",
    }
    return menu.get(day.lower().strip(), f"No menu listed for {day}")


model = InferenceClientModel(model_id=MODEL_ID, token=os.environ["HF_TOKEN"])

TASK = (
    "What's the weather in Pune, and what's on the mess menu for Tuesday? "
    "Tell me in one sentence whether it's a good day to eat outside."
)

# ----------------------------------------------------------------------
print("#" * 70)
print("# ToolCallingAgent — writes actions as JSON")
print("#" * 70)

json_agent = ToolCallingAgent(
    tools=[get_weather, get_mess_menu],
    model=model,
    max_steps=5,
)
print(json_agent.run(TASK))

# ----------------------------------------------------------------------
print()
print("#" * 70)
print("# CodeAgent — writes actions as Python")
print("#" * 70)

code_agent = CodeAgent(
    tools=[get_weather, get_mess_menu],
    model=model,
    max_steps=5,
)
print(code_agent.run(TASK))

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Add verbosity_level=2 to either agent. You'll see the full system prompt
#    smolagents built for you — compare it to the one you wrote in Lab 3.
#
# 2. Delete the "Use this whenever..." line from get_weather's docstring and
#    ask a vaguer question ("should I carry an umbrella in Pune?"). Does the
#    agent still pick the tool?
#
# 3. Give CodeAgent a task that needs real computation:
#    "If Pune is 27C, convert that to Fahrenheit and tell me if it's above 80."
#    Watch it write actual Python instead of chaining tool calls.
#
# 4. Add DuckDuckGoSearchTool() from smolagents to the tools list and ask
#    something current. Now your agent has the internet.
