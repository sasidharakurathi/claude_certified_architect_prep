# Task Manager Agent

A CLI-based AI agent built with the **Claude Agent SDK** that manages your `tasks.md` file through natural language.

## What it does

| Command | Example |
|---|---|
| List tasks | `list my tasks` / `show all tasks` |
| Add task | `add task: write unit tests for login` |
| Mark done | `mark done: review PR #42` |

The agent remembers context within a session — so you can say things like:
- `"add two tasks: fix the navbar bug and update the README"`
- `"mark the first TODO as done"`
- `"what's left in progress?"`

---

## Setup

### 1. Clone / create the folder
```bash
mkdir task-manager-agent && cd task-manager-agent
# copy all files here
```

### 2. Run setup script
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Add your API key
Get your key from [console.anthropic.com](https://console.anthropic.com) → API Keys

```bash
# Edit .env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 4. Activate venv and run
```bash
source .venv/bin/activate
python agent.py
```

---

## Manual setup (if setup.sh doesn't work)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install claude-agent-sdk python-dotenv
export ANTHROPIC_API_KEY=your-key  # Windows: set ANTHROPIC_API_KEY=your-key
python agent.py
```

---

## Project structure

```
task-manager-agent/
├── agent.py      # Core agent logic — read this to learn the SDK
├── tasks.md      # Your task file — the agent reads/writes this
├── setup.sh      # One-time setup script
├── .env          # Your API key (never commit this)
└── README.md
```

---

## Key concepts used (mapped to Google ADK)

| Google ADK | Claude Agent SDK |
|---|---|
| `Agent(tools=[...])` | `ClaudeAgentOptions(allowed_tools=[...])` |
| `Runner.run()` | `async for msg in query(...)` |
| `SessionService` | `ClaudeSDKClient` (auto-manages session) |
| Callbacks | `hooks` (PostToolUse, PreToolUse) |

---

## Cost

Uses `claude-haiku-4-5` — the cheapest model. Each session costs roughly **$0.01–$0.03**. You can safely run 30–50 sessions on a $10 budget.

---

## Next steps to explore

- [ ] Add `WebSearch` tool to let the agent research tasks
- [ ] Add a `PostToolUse` hook to log every file change
- [ ] Use `resume=session_id` to continue a session after process restart
- [ ] Add a `priority` field to tasks using structured output
