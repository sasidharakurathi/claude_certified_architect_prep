# Free Resources & Practicals — by Domain

> 🟢 Every link below was checked live during research for this kit — no guessed URLs. Free Anthropic Academy courses require no partner account. Practicals are hands-on exercises tied to specific Task Statements; do them, don't just read them.

---

## Domain 1: Agentic Architecture & Orchestration (27%)

### Free resources
- **[Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)** — the agent loop, built-in tools, hooks, subagents, sessions, MCP, all in one page
- **[Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents)** — official deep-dive: `AgentDefinition`, the `Task`/`Agent` tool, context isolation, parallel spawning, resuming subagents
- **[Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)** — every hook event, matcher patterns, blocking/allowing, async hooks, full worked examples
- **[Example agents (GitHub)](https://github.com/anthropics/claude-agent-sdk-demos)** — real reference agents built on the SDK (email assistant, research agent, etc.) — read the source
- **[Introduction to Subagents](https://anthropic.skilljar.com/introduction-to-subagents)** — free Anthropic Academy course
- **[Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api)** — free course covering the underlying `stop_reason`/tool-loop mechanics

### Practicals
1. Implement a bare agentic loop by hand against the raw Messages API: send a request, branch on `stop_reason`, execute a tool, append the result, repeat. Deliberately test what happens if you check for text-content presence instead of `stop_reason` — see the anti-pattern break.
2. Using the Agent SDK, build a coordinator with 2 subagents (different `AgentDefinition`s, different tool sets). Confirm `"Task"` (or `"Agent"`, per your SDK version) is in the coordinator's `allowedTools` and that removing it blocks delegation.
3. Spawn two subagents in a single response (parallel) vs. two separate turns (sequential) and time the difference.
4. Implement a `PostToolUse` hook that normalizes two different date formats coming from two mock tools into one consistent shape.
5. Implement a tool-call interception hook that blocks a mock `process_refund` call above a threshold and redirects to a logged "escalate" path.
6. Capture a session ID, then use `--resume <session-name>` (CLI) or the SDK's resume option to continue it; separately, branch with `fork_session` and confirm the original session is untouched.

---

## Domain 2: Tool Design & MCP Integration (18%)

### Free resources
- **[Model Context Protocol — Introduction](https://modelcontextprotocol.io/introduction)** — what MCP is, in plain terms
- **[MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)** — hosts/clients/servers, data vs. transport layer, the three primitives, a full worked JSON-RPC example
- **[MCP reference servers (GitHub)](https://github.com/modelcontextprotocol/servers)** — real, production-quality MCP servers to read and run (filesystem, Git, etc.)
- **[MCP Inspector (GitHub)](https://github.com/modelcontextprotocol/inspector)** — a dev tool for poking at any MCP server's tools/resources/prompts interactively
- **[Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)** — official guide to writing tool descriptions, `input_schema`, `tool_choice`, with a good-vs-bad description example
- **[Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)** — client vs. server tools, the full tool-use loop
- **[Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol)** — free course: build an MCP server + client from scratch in Python
- **[Model Context Protocol: Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)** — free course: sampling, notifications, transports

### Practicals
1. Write two tool descriptions for genuinely similar tools (e.g., `get_customer` vs. `lookup_order`) — first as one-liners, then expanded per the official "good vs. bad" example. Test both against ambiguous prompts and observe the selection difference.
2. Build a toy MCP server (Python, using the free MCP course as a guide) exposing one tool, one resource, and one prompt. Run the MCP Inspector against it.
3. Configure that server once in project-scoped `.mcp.json` with an `${ENV_VAR}`-expanded credential, and once in user-scoped `~/.claude.json`.
4. Write a structured MCP error response (`isError`, `errorCategory`, `isRetryable`) for a deliberately-broken tool call, and trace how an agent's next action differs from receiving a bare `"Error: failed"` string.
5. Experiment with all three `tool_choice` modes (`auto`, `any`, forced `{"type":"tool","name":...}`) against the same prompt and compare the responses.

---

## Domain 3: Claude Code Configuration & Workflows (20%)

### Free resources
- **[Claude Code overview](https://code.claude.com/docs/en/overview)** — installation, everything Claude Code can do, links to CLAUDE.md/skills/hooks/CI docs
- **[How Claude remembers your project (CLAUDE.md)](https://code.claude.com/docs/en/memory)** — the full hierarchy, `@import`, `.claude/rules/`, `/memory`, auto memory — the single best page for this domain
- **[Claude Code 101](https://anthropic.skilljar.com/claude-code-101)** — free course, daily-workflow basics
- **[Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action)** — free course, integrating into a real dev workflow
- **[Introduction to Agent Skills](https://anthropic.skilljar.com/introduction-to-agent-skills)** — free course on building/sharing Skills

### Practicals
1. In a real (or scratch) repo, run `/init` and inspect the generated CLAUDE.md. Then deliberately write a conflicting instruction in `~/.claude/CLAUDE.md` (user-level) vs. the project file, and observe/reason about which one a teammate would actually receive.
2. Create a `.claude/rules/testing.md` with YAML frontmatter `paths: ["**/*.test.*"]` and confirm it only loads when you touch a matching file (not on unrelated edits).
3. Build a custom Skill with `context: fork`, `allowed-tools` restricted to file-write only, and `argument-hint` — invoke it with and without arguments and observe the prompts.
4. Run the exact same non-trivial, multi-file task twice: once in plan mode, once with direct execution. Compare the outcomes.
5. Run Claude Code with `-p "<prompt>" --output-format json --json-schema <your-schema>` and confirm you get machine-parseable output suitable for a CI step.

---

## Domain 4: Prompt Engineering & Structured Output (20%)

### Free resources
- **[Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)** — Anthropic's living reference: clarity, examples, XML structuring, thinking, agentic systems
- **[Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)** — covers `tool_choice`, forcing tool use, and the tool-use system prompt mechanics behind Domain 4's structured-output content
- **[GitHub prompting tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)** — hands-on, example-filled interactive tutorial covering the same concepts as the docs
- **[Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api)** — free course, covers streaming, structured output, production patterns end to end

### Practicals
1. Write 2-4 few-shot examples for one genuinely ambiguous classification/extraction task, each showing the *reasoning* for the chosen label — not just the label. Test with and without the examples and compare consistency across 5 runs.
2. Define a `tool_use` extraction tool with a JSON schema containing a required field, an optional/nullable field, and an enum with an `"other"` + detail-string pattern. Feed it a document missing the optional field and confirm the model returns `null` rather than fabricating a value.
3. Build a validation-retry loop: deliberately fail a validation check, then send a follow-up request containing the original input, the failed output, and the specific error — confirm the retry actually uses that feedback.
4. Submit a small (5-10 item) batch via the Message Batches API with `custom_id` per item; simulate a failure on one item and resubmit only that one.
5. Generate code with one Claude session, then review it with a **second, independent** session that has no prior reasoning context — compare what each one catches.

---

## Domain 5: Context Management & Reliability (15%)

### Free resources
- **[Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)** — how the context window works, context awareness, compaction, overflow behavior (background reading — remember the exam itself doesn't test caching internals, but this page explains the surrounding concepts like "context rot" and compaction that the exam's Domain 5 judgment calls are built on)
- **[Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents)** — the "what subagents inherit" table is directly relevant to error propagation and context-passing judgment calls
- **[Claude Code memory](https://code.claude.com/docs/en/memory)** — relevant again here for how state persists (or doesn't) across long sessions

### Practicals
1. Deliberately run a long exploration task in Claude Code until you notice it start referencing "typical patterns" instead of specifics it found earlier — then have it write a scratchpad file and observe whether re-grounding on that file fixes the drift.
2. Build a 2-subagent pipeline where one simulates a timeout (raise an error deliberately). Compare a version that returns a structured error context vs. one that silently returns an empty result — trace how the coordinator's next action differs.
3. Feed a synthesis task two "sources" with deliberately conflicting numbers and see whether your prompt design preserves both with attribution or collapses them into one silently-chosen value.
4. Simulate an escalation-worthy scenario three ways: (a) customer explicitly asks for a human, (b) policy is silent on the exact request, (c) the model just reports "I'm not confident." Confirm your system correctly escalates on (a) and (b) but does *not* treat (c) alone as a valid trigger.
5. Build a tiny crash-recovery test: have an agent write its state to a file mid-task, kill the session, then have a fresh session load that file as a "manifest" and continue.

---

## General / cross-domain

- **[Claude 101](https://anthropic.skilljar.com/claude-101)** — free course, baseline product literacy
- **[Claude Platform 101](https://anthropic.skilljar.com/claude-platform-101)** — free course, building on the Claude Developer Platform
- **[Anthropic Partner Academy — CCAR-F certification page](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)** — official cert page, exam guide, T&Cs, exam policy

### Reference only — confirmed out of scope for the exam, but useful to know exist
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — real API feature, not tested on CCAR-F
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — real API feature, exam only expects you to know it exists, not its mechanics
