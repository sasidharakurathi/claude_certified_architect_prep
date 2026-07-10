"""
main.py - Entry point that loads .env then starts the agent.
Run this instead of agent.py directly so your API key is picked up from .env
"""

import os
import asyncio
from pathlib import Path

# Load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[Loaded .env from {env_path}]")
except ImportError:
    pass  # dotenv not installed — rely on shell env variable

# Validate key before importing agent (gives clearer error)
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("\n[Error] ANTHROPIC_API_KEY is not set.")
    print("Either:")
    print("  1. Add it to .env:  ANTHROPIC_API_KEY=sk-ant-...")
    print("  2. Export it:       export ANTHROPIC_API_KEY=sk-ant-...\n")
    exit(1)

from agent import run_agent

if __name__ == "__main__":
    asyncio.run(run_agent())
