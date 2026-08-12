"""
Lab 2 — What a tool actually is.

A "tool" is two things glued together:

    1. A Python function.          <- the part YOU call
    2. A text description of it.   <- the part the MODEL sees

The model never touches your function. It only ever reads the description and
writes text. Your code does the calling. That's the whole trick.

    python day1/02_what_is_a_tool.py
"""

import inspect
import json

# ----------------------------------------------------------------------
# 1. Plain Python functions. Nothing special about them.
# ----------------------------------------------------------------------


def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: Name of the city, e.g. "Mumbai" or "Pune".
    """
    fake = {"mumbai": "32C, humid", "pune": "27C, clear", "delhi": "38C, hazy"}
    return fake.get(city.lower(), f"No data for {city}")


def calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression.

    Args:
        expression: A maths expression like "17 * 3 + 2".
    """
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        return str(eval(expression))  # noqa: S307 - guarded by the check above
    except Exception as exc:  # noqa: BLE001
        return f"Error: {exc}"


# ----------------------------------------------------------------------
# 2. Turn a function into something a model can read.
# ----------------------------------------------------------------------


def describe(func) -> str:
    """Render a function as a one-line spec for the system prompt."""
    sig = inspect.signature(func)
    doc = (func.__doc__ or "").strip().split("\n")[0]
    return f"- {func.__name__}{sig}: {doc}"


def as_json_schema(func) -> dict:
    """Render a function the way the OpenAI/HF tool-calling API expects."""
    sig = inspect.signature(func)
    props = {
        name: {"type": "string", "description": f"The {name}"}
        for name in sig.parameters
    }
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip().split("\n")[0],
            "parameters": {
                "type": "object",
                "properties": props,
                "required": list(sig.parameters),
            },
        },
    }


TOOLS = [get_weather, calculate]

print("=" * 70)
print("STYLE A — tools described in plain text inside the system prompt")
print("=" * 70)
system_prompt = (
    "You have access to these tools:\n"
    + "\n".join(describe(f) for f in TOOLS)
    + "\n\nTo use one, reply with exactly:\nAction: <tool_name>(<arg>)"
)
print(system_prompt)

print()
print("=" * 70)
print("STYLE B — the same tools as JSON schema (native tool calling)")
print("=" * 70)
print(json.dumps([as_json_schema(f) for f in TOOLS], indent=2))

print()
print("=" * 70)
print("THE POINT")
print("=" * 70)
print(
    "Both are just text prepended to the prompt.\n"
    "The model reads it, writes a string back, and YOUR code decides whether\n"
    "that string looks like a tool call. There is no wire connecting the\n"
    "model to your function."
)

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Delete the docstring from get_weather and re-run. Look at how useless
#    the description becomes. Your docstring IS your prompt.
#
# 2. Rewrite get_weather's docstring as: "gets weather". Then as:
#    "Get current temperature and conditions for one Indian city. Use this
#    whenever the user asks about weather, temperature, rain, or humidity."
#    Which one would you pick if you were the model?
#
# 3. Write a third tool. Bad tool descriptions are the #1 reason agents fail,
#    so make yours specific about WHEN to use it, not just what it does.
