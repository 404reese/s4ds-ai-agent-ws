"""
Lab 1 — Messages, chat templates, and special tokens.

The big idea: an LLM does not see a list of messages. It sees ONE STRING.
Everything else — roles, tools, agents — is a convention layered on top of
that string. If you understand this, nothing later is magic.

    python day1/01_messages_and_templates.py
"""

import os

from dotenv import load_dotenv
from transformers import AutoTokenizer

load_dotenv()

# We use a small model's tokenizer just to SEE the template.
# You don't need a GPU or the weights for this — only the tokenizer config.
TOKENIZER_ID = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)

messages = [
    {"role": "system", "content": "You are a terse assistant."},
    {"role": "user", "content": "What is the capital of Maharashtra?"},
    {"role": "assistant", "content": "Mumbai."},
    {"role": "user", "content": "And its population?"},
]

print("=" * 70)
print("WHAT YOU WROTE (a list of dicts):")
print("=" * 70)
for m in messages:
    print(f"  {m['role']:>9} | {m['content']}")

print()
print("=" * 70)
print("WHAT THE MODEL ACTUALLY RECEIVES (one flat string):")
print("=" * 70)
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,  # appends the "your turn now" marker
)
print(repr(prompt))

print()
print("=" * 70)
print("SAME THING, RENDERED:")
print("=" * 70)
print(prompt)

print("=" * 70)
print("AS TOKEN IDS:")
print("=" * 70)
ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
print(f"  {len(ids)} tokens")
print(f"  first 20: {ids[:20]}")

print()
print("Special tokens this model uses:")
for name, tok in tokenizer.special_tokens_map.items():
    print(f"  {name:>20} = {tok!r}")

# ----------------------------------------------------------------------
# TRY IT YOURSELF
# ----------------------------------------------------------------------
# 1. Change TOKENIZER_ID to "meta-llama/Llama-3.2-1B-Instruct" and compare.
#    The template is COMPLETELY different. This is why you can't just paste
#    a prompt from one model into another and expect the same behaviour.
#
# 2. Set add_generation_prompt=False. What disappears? Why does the model
#    need that marker?
#
# 3. Add a 5th message with role "tool". Does the template handle it?
#    (Foreshadowing: this is exactly how tool results get back into the model.)
