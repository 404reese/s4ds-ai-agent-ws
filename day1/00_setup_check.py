"""
Lab 0 — Setup check.

Run this BEFORE the workshop. It should print ALL CHECKS PASSED.
If it doesn't, fix it before Day 1 starts — we won't have time in the room.

    python day1/00_setup_check.py
"""

import os
import sys

FAILURES = []


def check(label, condition, fix):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")
    if not condition:
        FAILURES.append((label, fix))
    return condition


print("=" * 60)
print("AI Agents Workshop — setup check")
print("=" * 60)

# --- 1. Python version -------------------------------------------------
check(
    f"Python {sys.version_info.major}.{sys.version_info.minor} (need 3.10+)",
    sys.version_info >= (3, 10),
    "Install Python 3.10 or newer, then recreate your venv.",
)

# --- 2. Packages -------------------------------------------------------
try:
    import huggingface_hub  # noqa: F401

    have_hub = True
except ImportError:
    have_hub = False

check(
    "huggingface_hub installed",
    have_hub,
    "pip install -r requirements.txt",
)

try:
    import smolagents  # noqa: F401

    have_smol = True
except ImportError:
    have_smol = False

check("smolagents installed", have_smol, "pip install -r requirements.txt")

# --- 3. Token ----------------------------------------------------------
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # Colab users set secrets a different way

token = os.environ.get("HF_TOKEN")

check(
    "HF_TOKEN found in environment",
    bool(token),
    "Copy .env.example to .env and paste your token from "
    "https://huggingface.co/settings/tokens",
)

check(
    "HF_TOKEN looks like a real token",
    bool(token) and token.startswith("hf_") and len(token) > 20,
    "Tokens start with 'hf_'. Check for quotes or stray spaces in .env.",
)

# --- 4. Can we actually reach a model? ---------------------------------
if have_hub and token:
    from huggingface_hub import InferenceClient

    model_id = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")
    try:
        client = InferenceClient(model=model_id, token=token)
        reply = client.chat.completions.create(
            messages=[{"role": "user", "content": "Reply with exactly: pong"}],
            max_tokens=10,
        )
        text = reply.choices[0].message.content.strip()
        check(f"Inference call to {model_id}", "pong" in text.lower(), "")
        print(f"       model said: {text!r}")
    except Exception as exc:  # noqa: BLE001
        check(
            f"Inference call to {model_id}",
            False,
            f"Got: {type(exc).__name__}: {exc}\n"
            "       401 -> bad token. 503 -> model busy, try again or change "
            "MODEL_ID in .env.",
        )

# --- Result ------------------------------------------------------------
print("=" * 60)
if FAILURES:
    print(f"{len(FAILURES)} CHECK(S) FAILED\n")
    for label, fix in FAILURES:
        print(f"  * {label}")
        if fix:
            print(f"    fix: {fix}")
    sys.exit(1)

print("ALL CHECKS PASSED — you're ready for Day 1.")
