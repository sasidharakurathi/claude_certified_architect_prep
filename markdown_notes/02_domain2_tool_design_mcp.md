# Domain 2: Tool Design & MCP Integration (18%)

> 🟢 Rewritten directly from the official Exam Guide's 5 task statements for this domain.

---

## Task Statement 2.1 — Design effective tool interfaces with clear descriptions and boundaries

**Core fact**: tool descriptions are the **primary mechanism** LLMs use for tool selection. Minimal descriptions ("Retrieves customer information") lead to unreliable selection among similar tools — this is the single most common root cause the exam tests for tool-misrouting scenarios.

**What a good description includes**: input formats, example queries, edge cases, and explicit boundary explanations (when to use this tool vs. a similar one).

**Named failure mode**: ambiguous/overlapping descriptions cause misrouting — e.g., `analyze_content` vs. `analyze_document` with near-identical wording. Also watch for **system-prompt wording that creates unintended tool associations** through keyword sensitivity (a system prompt emphasizing certain keywords can override otherwise well-written tool descriptions).

**Skills tested**:
- Writing descriptions that clearly differentiate purpose, inputs/outputs, and "when to use this vs. that"
- **Renaming** tools and updating descriptions to eliminate overlap (e.g., `analyze_content` → `extract_web_results` with a web-specific description)
- **Splitting** an overly generic tool into purpose-specific tools with defined contracts (e.g., splitting `analyze_document` into `extract_data_points`, `summarize_content`, `verify_claim_against_source`)
- Auditing system prompts for keyword-sensitive instructions that might silently override tool descriptions

**Exam-confirmed judgment call**: when misrouting is caused by *thin descriptions*, the correct **first step** is improving the descriptions themselves — not adding few-shot examples (adds token overhead without fixing the root cause), not a hand-rolled routing/classifier layer (over-engineered, bypasses the model's own reasoning), and not immediately consolidating tools (a valid architecture change, but more effort than a "first step" warrants).

## Task Statement 2.2 — Implement structured error responses for MCP tools

**The MCP `isError` flag** is the pattern for signaling tool failure back to the agent.

**Error taxonomy tested**: transient (timeouts, service unavailable), validation (bad input), business (policy violation), permission errors — each needs different downstream handling.

**Recommended structured error metadata**:
- `errorCategory` (transient / validation / permission / business)
- `isRetryable` boolean
- Human-readable description
- For business-rule violations specifically: a `retriable: false` flag plus a customer-friendly explanation the agent can relay

**Named anti-patterns**:
- **Uniform/generic error responses** ("Operation failed") — prevent the agent from making an appropriate recovery decision
- Confusing an **access failure** (needs a retry decision) with a **valid empty result** (a successful query that legitimately found nothing) — these must be distinguishable in the response

**Error propagation skill**: implement **local error recovery within subagents** for transient failures; propagate to the coordinator **only** errors that couldn't be resolved locally, along with partial results and a note on what was attempted.

## Task Statement 2.3 — Distribute tools appropriately across agents and configure tool choice

**Named principle with specific numbers**: giving an agent access to **too many tools (e.g., 18 instead of 4–5)** degrades tool-selection reliability by increasing decision complexity. Agents given tools **outside their specialization** tend to misuse them (a synthesis agent attempting web searches it wasn't meant to run).

**Scoped tool access**: give each agent only the tools its role needs, with **limited cross-role tools reserved for specific high-frequency needs** (e.g., a narrow `verify_fact` tool available to a synthesis agent for the common case, while complex verification still routes through the coordinator to the full web-search agent).

**`tool_choice` options tested**:
- `"auto"` — model decides whether/which tool to call
- `"any"` — model **must** call a tool, but chooses which; guarantees a tool call instead of conversational text
- Forced selection — `{"type": "tool", "name": "..."}` — guarantees a **specific named** tool is called first (e.g., forcing `extract_metadata` before enrichment tools run in a later turn)

**Skill**: replacing an overly generic tool with a constrained alternative (e.g., `fetch_url` → `load_document` that validates the URL is actually a document) to reduce misuse surface area.

## Task Statement 2.4 — Integrate MCP servers into Claude Code and agent workflows

**MCP server scoping** — memorize this distinction exactly:
- **Project-level**: `.mcp.json` — shared team tooling, checked into version control
- **User-level**: `~/.claude.json` — personal/experimental servers, not shared

**Environment variable expansion** in `.mcp.json` (e.g., `${GITHUB_TOKEN}`) lets you reference credentials without committing secrets to the repo.

**Discovery fact**: tools from **all** configured MCP servers are discovered at connection time and become simultaneously available to the agent — there's no lazy/on-demand loading described in the guide's scope.

**MCP resources**: expose **content catalogs** (issue summaries, documentation hierarchies, database schemas) to reduce exploratory tool calls — the agent can look at a resource instead of making a chain of speculative tool calls to figure out what's available.

**Skills tested**:
- Configuring shared servers in project-scoped `.mcp.json` with env-var expansion for auth tokens; personal/experimental servers in user-scoped `~/.claude.json`
- Enhancing MCP tool descriptions in enough detail that the agent doesn't default to a less-capable built-in tool (e.g., preferring `Grep` over a more capable MCP tool because the MCP tool's description undersold it)
- **Preferring existing community MCP servers** over custom implementations for standard integrations (e.g., Jira) — reserve custom servers for genuinely team-specific workflows
- Exposing content catalogs as MCP **resources** rather than requiring exploratory tool calls to discover what's available

## Task Statement 2.5 — Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

| Tool | Use for |
|---|---|
| **Grep** | Content search — function names, error messages, import statements |
| **Glob** | File **path** pattern matching — finding files by name/extension pattern (`**/*.test.tsx`) |
| **Read / Write** | Full file operations |
| **Edit** | Targeted modification via **unique text matching** |
| **Bash** | Commands/scripts/git |

**Key fallback rule**: when `Edit` fails because the anchor text isn't unique in the file, fall back to **Read + Write** for a reliable full-file replace.

**Codebase-exploration skill tested repeatedly**: build understanding **incrementally** — start with `Grep` to find entry points, then `Read` to follow imports and trace flow, rather than reading everything upfront. For tracing a function's usage across wrapper modules: first identify all exported names, then search for each name across the codebase (a two-step search, not a single grep).

---

## Quick self-check

- [ ] I can explain why thin tool descriptions are the most common root cause of tool misrouting, and why "improve the descriptions" beats few-shot examples or a routing layer as the *first* fix.
- [ ] I can write a structured MCP error response distinguishing transient/validation/business/permission categories.
- [ ] I know the "18 tools vs. 4–5" framing for why over-provisioning degrades selection reliability.
- [ ] I can explain all three `tool_choice` modes (`auto`, `any`, forced `{"type":"tool","name":...}`) and when each is the right answer.
- [ ] I know `.mcp.json` (project) vs. `~/.claude.json` (user) MCP server scoping and env-var expansion for credentials.
- [ ] I know MCP resources are for exposing catalogs, distinct from tools (for actions).
- [ ] I can pick the right built-in tool (Grep vs. Glob vs. Edit vs. Read+Write fallback) for a described scenario.

Track these in the [progress tracker](tracker.html).
