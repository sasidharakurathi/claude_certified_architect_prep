# Glossary — Quick Reference

> 🟢 Rewritten against the official Exam Guide. Terms confirmed to be out of exam scope (prompt-caching mechanics, the separate "Structured Outputs" constrained-decoding feature) have been removed — see `00_exam_overview.md`'s out-of-scope list.

**Agent loop** — send request → check `stop_reason` → if `"tool_use"`, execute tool(s) and append results to conversation history → repeat → if `"end_turn"`, stop. The fundamental control flow of any tool-using Claude system. (Domain 1, TS 1.1)

**AgentDefinition** — Config object defining a subagent: description, system prompt, and its own restricted tool list. (Domain 1, TS 1.3)

**`allowed-tools`** — Skill frontmatter field restricting which tools are available while that skill executes. (Domain 3, TS 3.2)

**`argument-hint`** — Skill frontmatter field that prompts the developer for required parameters when a skill is invoked without arguments. (Domain 3, TS 3.2)

**Auto memory / `/memory`** — `/memory` is the command to verify which CLAUDE.md/memory files are actually loaded in a session — used to diagnose inconsistent behavior across environments. (Domain 3, TS 3.1)

**Claim-source mapping** — Structured pairing of a claim with its source (URL, document name, excerpt) that must be preserved through summarization/synthesis steps to avoid losing provenance. (Domain 5, TS 5.6)

**CLAUDE.md** — Markdown file(s) giving Claude persistent, human-written instructions. Hierarchy: user-level (`~/.claude/CLAUDE.md`, personal, not shared via VCS), project-level (`.claude/CLAUDE.md` or root `CLAUDE.md`), directory-level (subdirectory files). (Domain 3, TS 3.1)

**`context: fork`** — Skill frontmatter option that runs the skill in an isolated sub-agent context, keeping its (possibly verbose) output from polluting the main conversation. (Domain 3, TS 3.2)

**Coordinator / hub-and-spoke** — Orchestration pattern where one coordinator agent owns all inter-subagent communication, error handling, and information routing; subagents don't talk to each other directly. (Domain 1, TS 1.2)

**`custom_id`** — Field on a Message Batches API request used to correlate it with its corresponding response, including for identifying and resubmitting failed items. (Domain 4, TS 4.5)

**Escalation** — Routing a task/decision to a human. Correct triggers: explicit customer request, a genuine policy gap/exception, inability to make progress. Wrong triggers: self-reported model confidence, sentiment analysis. (Domain 5, TS 5.2)

**`Explore` subagent** — A subagent used to isolate verbose codebase-discovery output, returning summaries to the main conversation to prevent context-window exhaustion during multi-phase tasks. (Domain 3, TS 3.4)

**`fork_session`** — Creates an independent session branch from a shared analysis baseline, to explore a divergent approach without mutating the original session. Contrast with `--resume`. (Domain 1, TS 1.7)

**Hooks** — Code that runs at defined agent-lifecycle points. Exam-tested examples: `PostToolUse` (normalize heterogeneous tool-result data formats) and tool-call interception hooks (block a policy-violating action before it executes). Code-enforced, unlike prompts. (Domain 1, TS 1.5)

**`isError` / `isRetryable` / `errorCategory`** — MCP structured error-response pattern. `errorCategory` distinguishes transient/validation/business/permission errors; `isRetryable` tells the agent whether retrying could help. (Domain 2, TS 2.2)

**"Lost in the middle"** — Models reliably process information at the beginning and end of a long input but may omit findings buried in the middle. (Domain 5, TS 5.1)

**Manifest (crash recovery)** — A structured export of an agent's state to a known location; the coordinator loads the manifest on resume and re-injects it into agent prompts. (Domain 5, TS 5.4)

**MCP (Model Context Protocol)** — Standard connecting AI hosts to external servers exposing **tools** (actions), **resources** (content catalogs, e.g. issue summaries or schemas), and **prompts** (templates).

**MCP server scoping** — **Project-level** `.mcp.json` (shared team tooling, version-controlled, supports `${ENV_VAR}` expansion for credentials) vs. **user-level** `~/.claude.json` (personal/experimental servers). (Domain 2, TS 2.4)

**Message Batches API** — Asynchronous bulk API: ~50% cheaper, up to 24-hour window, **no guaranteed latency SLA**, and **no multi-turn tool calling within a single request**. Never for blocking/user-facing workflows. (Domain 4, TS 4.5)

**Multishot / few-shot prompting** — Providing 2–4 targeted, relevant examples (per the guide's own range for ambiguous-scenario prompts) to steer output format, demonstrate ambiguous-case handling, and reduce hallucination. (Domain 4, TS 4.2)

**Plan mode** — Claude proposes and lets you review an approach before executing side-effecting tools. Right for large-scale/architectural/multi-file/ambiguous tasks; direct execution is right for small well-scoped ones. (Domain 3, TS 3.4)

**`Task` tool** — The mechanism for spawning subagents. A coordinator's `allowedTools` must include `"Task"` to invoke them. (Domain 1, TS 1.3)

**`--resume <session-name>`** — CLI flag to continue a specific named prior session with its full history. Contrast with `fork_session`. (Domain 1, TS 1.7)

**Scratchpad files** — Files where an agent records key findings during long exploration, referenced on later questions to counteract context degradation in extended sessions. (Domain 5, TS 5.4)

**Stratified random sampling** — Sampling *high-confidence* extractions specifically (not just low-confidence ones) to measure true error rates and catch novel error patterns before reducing human review. (Domain 5, TS 5.5)

**Subagent** — A specialized agent spawned via the `Task` tool, with its own scoped tool list (`AgentDefinition`) and isolated context — it does not automatically inherit the coordinator's conversation history.

**Tool choice (`tool_choice`)** — `"auto"` (model decides), `"any"` (must call a tool, but chooses which), or forced `{"type": "tool", "name": "..."}` (must call this specific tool). (Domain 2, TS 2.3; Domain 4, TS 4.3)

**`tool_use` + JSON schema** — The exam's actual mechanism for reliable structured output: eliminates JSON syntax errors by construction, but does **not** prevent semantic errors (e.g., values in the wrong field). (Domain 4, TS 4.3)

**`.claude/rules/`** — Directory of modular instruction files, optionally scoped via YAML frontmatter `paths:` glob patterns so a rule loads only when Claude touches a matching file. (Domain 3, TS 3.3)

## Out of scope — don't build glossary entries around these

Per the official guide, these are explicitly **not** tested: prompt-caching implementation details (TTL, `cache_control` breakpoints, pricing), a separate "Structured Outputs"/constrained-decoding API feature, fine-tuning, API auth/billing, streaming/SSE, rate limits/quotas, OAuth/key rotation, cloud-provider-specific config, tokenization internals, and Claude's internal architecture/training.
