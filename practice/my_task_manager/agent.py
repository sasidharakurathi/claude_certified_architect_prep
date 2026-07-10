import asyncio
import hashlib
import os
from pathlib import Path

from claude_agent_sdk import (
    AgentDefinition,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    TextBlock,
    query,
)

from dotenv import load_dotenv
load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

TASKS_FILE     = Path(__file__).parent / "tasks.md"
MAIN_MODEL     = "claude-haiku-4-5-20251001"
RESEARCH_MODEL = "claude-haiku-4-5-20251001"

# ── Research Subagent ─────────────────────────────────────────────────────────

RESEARCH_SUBAGENT = AgentDefinition(
    description=(
        "Software development research specialist. "
        "Invoke this agent when the user asks HOW to implement something, "
        "wants to understand a technology or concept, needs best practices, "
        "asks for suggestions on approaching a task, or uses words like "
        "'research', 'how do I', 'what is', 'how to', 'help me understand', "
        "'suggest', 'guide me', 'steps to', 'tutorial'. "
        "Do NOT invoke for listing tasks, adding tasks, or marking tasks done."
    ),
    prompt="""You are a senior software development research assistant.

Your job: Given a task or topic, produce a concise but actionable research brief.

Structure your response EXACTLY like this:

## 🔍 Research Brief: <topic>

### What it is
One paragraph — plain explanation, no jargon.

### Why it matters / When to use it
2-3 bullet points.

### Recommended approach (step-by-step)
Numbered steps a developer can follow right now.

### Key tools / libraries / frameworks
A short table or bullet list with one-line descriptions.

### Gotchas & best practices
3-5 bullet points of things that trip people up.

### Useful resources
2-3 links you actually fetched and verified exist.

---
Rules:
- Always run WebSearch FIRST before writing anything
- Fetch at least one page to verify recommendations are current
- Keep total length under 600 words
- Only include URLs you actually fetched — no hallucinated links
""",
    tools=["WebSearch", "WebFetch"],
    model=RESEARCH_MODEL,
    maxTurns=8,
)

# ── Main Agent System Prompt ──────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are a smart Task Manager Agent for a software developer.

You manage a Markdown task file at: {TASKS_FILE}

FILE FORMAT (maintain this exactly):
# My Tasks

## TODO
- [ ] task description

## IN PROGRESS
- [ ] task description

## DONE
- [x] task description

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT YOU CAN DO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. LIST TASKS
   → Always re-read tasks.md fresh before answering.

2. ADD A TASK
   → Re-read tasks.md, then append under ## TODO as `- [ ] description`

3. MARK DONE
   → Re-read tasks.md, find the task, change `- [ ]` to `- [x]`, move to ## DONE

4. RESEARCH A TASK / TOPIC
   → Delegate to the research-assistant subagent.
   → The subagent's output is already shown to the user directly.
   → Your ONLY job after research: ask "Would you like me to add this as a task?"
   → Do NOT repeat, reprint, or summarize the research brief.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Always re-read tasks.md before listing or modifying
- Never delete tasks — only move to DONE
- After research: ask the add-task question ONLY — nothing else
"""

# ── Options ───────────────────────────────────────────────────────────────────

def make_options(session_id: str | None) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        model=MAIN_MODEL,
        permission_mode="bypassPermissions",
        allowed_tools=["Read", "Write", "Edit", "Agent"],
        system_prompt=SYSTEM_PROMPT,
        agents={"research-assistant": RESEARCH_SUBAGENT},
        resume=session_id,
    )

# ── Render + dedup ────────────────────────────────────────────────────────────

def make_renderer():
    """
    Returns a render function that tracks already-printed content hashes
    to suppress duplicate blocks (subagent brief printed twice).
    """
    seen: set[str] = set()

    def render(message) -> str | None:
        if isinstance(message, AssistantMessage):
            parts = []
            for block in message.content:
                if isinstance(block, TextBlock) and block.text.strip():
                    # Hash the first 300 chars — enough to catch reprints
                    key = hashlib.md5(block.text[:300].encode()).hexdigest()
                    if key in seen:
                        continue  # already printed this block — skip
                    seen.add(key)
                    parts.append(block.text)
                elif hasattr(block, "name") and block.name in ("Agent", "Task"):
                    subagent = getattr(block, "input", {}).get("subagent_type", "research-assistant")
                    parts.append(
                        f"\n🔬 Spawning research subagent ({subagent})...\n"
                        f"   Searching the web — this takes 30–60s\n"
                    )
            return "\n".join(parts).strip() or None

        if isinstance(message, ResultMessage):
            if message.subtype == "error_during_execution":
                return "[Agent error — check your API key and tasks.md]"
        return None

    return render

# ── Single turn ───────────────────────────────────────────────────────────────

async def run_turn(session_id: str | None, user_input: str) -> str | None:
    new_session_id = session_id
    render = make_renderer()  # fresh dedup tracker per turn

    async for message in query(prompt=user_input, options=make_options(session_id)):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            data = getattr(message, "data", {}) or {}
            new_session_id = data.get("session_id", session_id)

        if isinstance(message, ResultMessage):
            sid = getattr(message, "session_id", None)
            if sid:
                new_session_id = sid

        text = render(message)
        if text:
            print(text)

    return new_session_id

# ── CLI loop ──────────────────────────────────────────────────────────────────

async def run_agent():
    print("\n╔══════════════════════════════════════════════╗")
    print("║       Task Manager Agent  (Claude SDK)       ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  • list tasks                                ║")
    print("║  • add task: <description>                   ║")
    print("║  • mark done: <task>                         ║")
    print("║  • how do I implement <topic>?               ║")
    print("║  • research: <topic or task name>            ║")
    print("║  • exit                                      ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"\nTasks file: {TASKS_FILE}\n")

    if not TASKS_FILE.exists():
        print(f"[Error] tasks.md not found at {TASKS_FILE}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[Error] ANTHROPIC_API_KEY not set.")
        print("Set it: export ANTHROPIC_API_KEY=sk-ant-...\n")
        return

    session_id: str | None = None

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        print("\nAgent:\n")
        session_id = await run_turn(session_id, user_input)
        print()


if __name__ == "__main__":
    asyncio.run(run_agent())