"""
Lab 5 — Ship it. A Gradio app you can deploy to Hugging Face Spaces for free.

TO DEPLOY:
  1. huggingface.co -> your profile -> New Space
  2. SDK: Gradio. Hardware: CPU basic (free). Visibility: Public.
  3. Settings -> Variables and secrets -> New secret
        Name:  HF_TOKEN
        Value: your token
     (Never commit your token. Spaces are public — people WILL find it.)
  4. Upload app.py and requirements.txt from this folder.
  5. Wait for the build. Share the link.
"""

import os

import gradio as gr
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")


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
def days_until(event_date: str) -> str:
    """Count the days between today and a future date.

    Args:
        event_date: Target date in YYYY-MM-DD format, e.g. "2026-08-23".
    """
    from datetime import date

    try:
        y, m, d = (int(p) for p in event_date.split("-"))
        delta = (date(y, m, d) - date.today()).days
    except Exception as exc:  # noqa: BLE001
        return f"Could not parse '{event_date}': {exc}"
    if delta < 0:
        return f"{abs(delta)} days ago."
    return f"{delta} days from today."


def build_agent():
    model = InferenceClientModel(model_id=MODEL_ID, token=os.environ["HF_TOKEN"])
    return CodeAgent(
        tools=[get_weather, days_until, DuckDuckGoSearchTool()],
        model=model,
        max_steps=6,
    )


agent = build_agent()


def respond(message, history):
    if not message.strip():
        return "Ask me something."
    try:
        return str(agent.run(message))
    except Exception as exc:  # noqa: BLE001
        return f"The agent errored out: {type(exc).__name__}: {exc}"


demo = gr.ChatInterface(
    fn=respond,
    title="Alfred — a tool-using agent",
    description=(
        "Built at the S4DS AI Agents Workshop. Ask something that needs more "
        "than one step."
    ),
    examples=[
        "What's the weather in Pune and how many days until 2026-08-23?",
        "Search for the latest smolagents release and summarise it in 2 lines.",
    ],
)

if __name__ == "__main__":
    demo.launch()
