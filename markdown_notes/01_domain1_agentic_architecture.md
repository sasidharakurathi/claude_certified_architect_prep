# Domain 1: Agentic Architecture & Orchestration (27% — the biggest domain)

> 🟢 Rewritten directly from the official Exam Guide's 7 task statements for this domain. This is now the authoritative structure — study it task statement by task statement.

---

## Task Statement 1.1 — Design and implement agentic loops for autonomous task execution

**The loop, precisely as the guide defines it**: send a request to Claude → inspect `stop_reason` → if `"tool_use"`, execute the requested tool(s) and return results, appending them to conversation history, then repeat → if `"end_turn"`, stop.

Key distinction: **model-driven decision-making** (Claude reasons about which tool to call next based on context) vs. **pre-configured decision trees** — the exam wants you to recognize the agent loop as inherently model-driven, not scripted.

**Named anti-patterns for loop termination** (these are exam-favorite wrong answers):
- Parsing natural-language signals in the assistant's text to decide when to stop
- Setting an arbitrary iteration cap as the *primary* stopping mechanism
- Checking for the presence of assistant text content as a "done" indicator

**Correct implementation**: control flow keyed strictly off `stop_reason` ("tool_use" continues, "end_turn" terminates), with tool results appended to conversation history between iterations so Claude can reason about new information on the next turn.

## Task Statement 1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns

**Hub-and-spoke** is the architecture: a coordinator manages *all* inter-subagent communication, error handling, and information routing — subagents don't talk to each other directly. Subagents run with **isolated context** — they do not automatically inherit the coordinator's conversation history.

The coordinator's job: task decomposition, delegation, result aggregation, and deciding *which* subagents to invoke based on query complexity (not always routing through a fixed full pipeline).

**Named anti-pattern**: **overly narrow task decomposition** — e.g., a coordinator asked to research "AI's impact on creative industries" that only spins up subtasks for "digital art," "graphic design," and "photography" completely misses music, writing, and film. This is a coordinator problem, not a subagent execution problem — the sample exam question built around exactly this scenario has the correct answer identifying the coordinator's decomposition as too narrow, explicitly rejecting answers that blame the (correctly-functioning) downstream subagents.

**Skills tested**:
- Dynamically selecting which subagents to invoke rather than always running the full pipeline
- Partitioning scope across subagents to minimize duplication (distinct subtopics/source types per agent)
- **Iterative refinement loops**: coordinator evaluates synthesis output for gaps, re-delegates to search/analysis with targeted queries, re-invokes synthesis until coverage is sufficient
- Routing all subagent communication through the coordinator for observability and consistent error handling

## Task Statement 1.3 — Configure subagent invocation, context passing, and spawning

⚠️ **Terminology correction**: the mechanism for spawning subagents is the **`Task` tool** — a coordinator's `allowedTools` **must include `"Task"`** to invoke subagents. (Earlier drafts of this kit used "Agent" tool terminology from generic SDK docs; the exam guide is explicit that it's called the **Task tool**.)

Key facts:
- Subagent context is **not** automatically inherited — you must **explicitly include** what the subagent needs directly in its prompt (e.g., passing prior web-search results and document-analysis outputs into the synthesis subagent's prompt).
- **`AgentDefinition`** configuration includes: description, system prompt, and tool restrictions per subagent type.
- **Fork-based session management** (`fork_session`) lets you explore divergent approaches from a shared analysis baseline.
- Use **structured data formats** to separate content from metadata (source URLs, document names, page numbers) when passing context between agents — this preserves attribution.
- **Spawn parallel subagents by emitting multiple `Task` tool calls in a single coordinator response**, not across separate turns — this is how you get true parallelism rather than sequential round-trips.
- Design coordinator prompts around **goals and quality criteria**, not step-by-step procedural instructions — this gives subagents room to adapt.

## Task Statement 1.4 — Implement multi-step workflows with enforcement and handoff patterns

**Programmatic enforcement (hooks, prerequisite gates) vs. prompt-based guidance**: when deterministic compliance is required (e.g., identity verification before a financial operation), prompt instructions alone have a **non-zero failure rate** — this is the guide's own phrasing, worth memorizing verbatim since it captures exactly why hooks exist.

**Skills tested**:
- Programmatic prerequisites that **block** downstream tool calls until a prerequisite has completed — e.g., blocking `process_refund` until `get_customer` has returned a verified customer ID
- Decomposing multi-concern requests (a customer message with several distinct issues) into separate items, investigating each in parallel with shared context, then synthesizing one unified resolution
- **Structured handoff summaries** when escalating to a human who lacks the conversation transcript: customer ID, root cause, refund amount, recommended action

## Task Statement 1.5 — Apply Agent SDK hooks for tool call interception and data normalization

Two hook use cases the exam tests specifically:
1. **`PostToolUse`** to **normalize heterogeneous data formats** coming back from different MCP tools — e.g., one tool returns Unix timestamps, another ISO 8601, another numeric status codes; a `PostToolUse` hook reconciles these into one consistent shape before Claude reasons over them.
2. **Tool call interception hooks** on outgoing calls to **enforce compliance rules** — e.g., blocking a refund above $500 and redirecting to human escalation instead.

**The core judgment call**: choose hooks over prompt-based enforcement whenever a business rule requires a **guaranteed**, not probabilistic, outcome.

## Task Statement 1.6 — Design task decomposition strategies for complex workflows

Two decomposition modes:
- **Prompt chaining** (fixed sequential pipeline) — right for **predictable, multi-aspect reviews**: e.g., analyze each file individually, then run one cross-file integration pass.
- **Dynamic/adaptive decomposition** — right for **open-ended investigation**: generate subtasks based on what's discovered at each step (e.g., "add comprehensive tests to a legacy codebase" → first map structure, identify high-impact areas, then build a prioritized plan that adapts as dependencies surface).

**Named anti-pattern / exam scenario**: splitting a large code review into **per-file passes plus a separate cross-file integration pass** avoids **attention dilution** — a single pass over many files at once produces inconsistent depth and even contradictory findings (flagging a pattern in one file while approving identical code in another). The wrong answers here include "upgrade to a bigger context window" (doesn't fix attention dilution) and "require majority consensus across repeated full-context runs" (suppresses real findings that only surface intermittently).

## Task Statement 1.7 — Manage session state, resumption, and forking

⚠️ **Terminology correction**: named session resumption uses **`--resume <session-name>`** to continue a specific prior conversation. Branching uses **`fork_session`** to create an independent branch from a shared analysis baseline (e.g., comparing two refactoring approaches from the same codebase analysis).

**Key judgment call**: when resuming a session after code has changed, you must **explicitly inform the agent about which files changed** — resuming doesn't auto-detect drift. And when prior tool results are **stale**, starting a **new session with a structured summary injected** is more reliable than resuming and trusting outdated tool outputs. Prefer targeted re-analysis of specifically-changed files over full re-exploration when resuming.

---

## Quick self-check

- [ ] I can state the agentic loop's control-flow rule using `stop_reason` and name the three loop-termination anti-patterns.
- [ ] I can explain hub-and-spoke and why subagents don't inherit coordinator context automatically.
- [ ] I know the `Task` tool is the subagent-spawning mechanism and that `allowedTools` must include `"Task"`.
- [ ] I can explain `fork_session` vs. `--resume <session-name>` and when to start fresh with an injected summary instead of either.
- [ ] I know when to choose hooks (`PostToolUse`, tool-call interception) over prompt-based enforcement, and can give the "non-zero failure rate" reasoning.
- [ ] I can distinguish prompt chaining (predictable, sequential) from dynamic decomposition (open-ended, adaptive).
- [ ] I can explain why splitting a large review into per-file + integration passes beats one big pass, and why a bigger context window doesn't fix that.
- [ ] I can recognize "overly narrow task decomposition by the coordinator" as a root-cause answer distinct from blaming a correctly-functioning subagent.

Track these in the [progress tracker](tracker.html).
