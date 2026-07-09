# Practice Exam — 50 Original Questions + 12 Official Sample Questions

> 🟢 Updated against the official Exam Guide. A few of the original 50 referenced concepts the guide marks **out of scope** (a separate "Structured Outputs" feature, prompt-caching TTL/breakpoint mechanics) — those have been replaced with guide-aligned questions. Domain weights (27/18/20/20/15%) are now **confirmed exact**, not estimated.

**Section 1–5 (Q1–50)**: original questions I wrote to exercise the same judgment calls the exam tests — NOT leaked or recalled real exam questions. **Section 6**: the **12 official sample questions published in the Exam Guide itself**, reproduced verbatim with Anthropic's own explanations — these are the closest thing to "real exam calibration" available, since the guide explicitly provides them to help candidates learn the format and difficulty level.

⚠️ **Real exam format note**: some real exam items are **multiple-response** (select more than one correct answer; the item tells you how many to pick). This practice bank is single-answer for simplicity — don't let the real exam's multi-select format surprise you.

Instructions: Answer all questions in a section before checking the answer key. Time yourself — 60 questions in 120 minutes to simulate real conditions once you've studied all domains.

---

## Section 1: Agentic Architecture & Orchestration (Q1–14)

**Q1.** You're building a multi-agent research system: a coordinator dispatches to a search subagent, an analysis subagent, and a synthesis subagent, each reporting back. What topology is this, and why is it preferred over agents messaging each other directly?
A) Flat/mesh — it's simpler to implement
B) Hub-and-spoke — a single coordinator owns decomposition, integration, and failure handling
C) Peer-to-peer — subagents negotiate directly for lower latency
D) Round-robin — each subagent takes turns owning the conversation

**Q2.** A team wants to guarantee that Claude never runs `rm -rf` in production, no matter what a user asks. Which mechanism actually guarantees this?
A) A CLAUDE.md rule: "Never run destructive bash commands"
B) A strongly worded system prompt repeated at the top of every message
C) A `PreToolUse` hook that inspects the Bash command and denies matching patterns
D) Asking Claude to double-check with the user before running any Bash command

**Q3.** When should you delegate work to a subagent rather than handling it directly in the main agent loop?
A) Whenever a task involves more than one tool call
B) When the task is parallelizable, needs isolated context, or is an independent workstream
C) Always — subagents produce higher quality output than the main loop
D) Only when the user explicitly asks for "an agent"

**Q4.** You need an agent to autonomously read files, run tests, and edit code with minimal custom glue code, and you don't need to build your own tool-execution loop. Which should you build on?
A) The raw Anthropic Client SDK, implementing your own `while stop_reason == "tool_use"` loop
B) The Claude Agent SDK, which provides the agent loop and built-in tools (Read, Edit, Bash, etc.)
C) A custom REST wrapper around the Messages API with no tool use
D) The Batch API, scheduling tool calls asynchronously

**Q5.** A production agent needs to run inside your own infrastructure with full control over the filesystem it operates on, and you want to prototype quickly before scaling. What's the recommended progression?
A) Start with Managed Agents, then migrate to the Agent SDK once traffic grows
B) Prototype with the Agent SDK locally, then move to Managed Agents for production scale
C) Use the Client SDK exclusively at every stage
D) There is no recommended progression; pick one and never switch

**Q6.** Messages from a subagent's execution include a `parent_tool_use_id` field. What is this for?
A) Rate-limiting the subagent
B) Letting you attribute which messages/output belong to which delegated subagent call
C) Encrypting the subagent's output
D) Automatically retrying failed subagent calls

**Q7.** A coordinator dispatches a task to a "code-reviewer" subagent. Which `AgentDefinition` design best follows the least-privilege principle?
A) Give the code-reviewer subagent the full tool list, including Bash and Edit, in case it needs them
B) Give the code-reviewer subagent only Read, Glob, and Grep — tools it actually needs for a read-only review
C) Give the code-reviewer subagent no tools; require the coordinator to feed it all file contents inline
D) Give the code-reviewer subagent the Task tool so it can spawn its own subagents

**Q8.** You want to resume a specific prior Claude Code session by name, continuing the same investigation across separate work sessions. What's the correct mechanism?
A) `--resume <session-name>`
B) A brand-new session with the same prompt text repeated
C) `fork_session`, which always starts a blank session
D) Re-sending the entire prior conversation as a single new user message

**Q9.** What's the difference between `--resume <session-name>` and `fork_session`?
A) They are identical; "fork" is just older terminology for "resume"
B) Resume continues the same named session with full history; fork_session branches an independent copy from a shared analysis baseline to explore a divergent approach without mutating the original
C) Fork deletes the original session; resume preserves it
D) Resume only works with subagents; fork only works with the main agent

**Q10.** An engineer argues: "Since we told Claude in the CLAUDE.md file to always ask for confirmation before deleting files, we don't need any other safeguard." What's the flaw?
A) CLAUDE.md files are never loaded at session start
B) CLAUDE.md is context/guidance, not enforced configuration — nothing guarantees Claude follows it under all conditions
C) CLAUDE.md only applies to subagents, not the main agent
D) There is no flaw; this is sufficient

**Q11.** For a very long-running coding task spanning multiple context windows, which state-tracking combination is recommended?
A) Rely entirely on the model's memory of the conversation; do not write anything to disk
B) Structured JSON for machine-parsed state (e.g., `tests.json`) + freeform text for progress notes (`progress.txt`) + git commits as checkpoints
C) A single unstructured text file containing everything, updated at the end of each session
D) Store all state exclusively in the system prompt

**Q12.** Which scenario best justifies using **plan mode** instead of direct execution?
A) Renaming a single local variable in one file
B) A large refactor across a production codebase where a wrong first attempt would be costly to undo
C) Reading a file to answer a question
D) Running a linter that only reports issues without modifying files

**Q13.** A support-automation team wants each specialized agent (billing, returns, technical) to only access the tools relevant to its domain. What principle are they applying?
A) Separation of concerns for latency optimization only
B) Least privilege / tool scoping to reduce blast radius and avoid tool-selection confusion
C) Batch processing optimization
D) Prompt caching optimization

**Q14.** A multi-agent system has agents passing messages directly to each other with no central coordinator, and the team is struggling to figure out which agent is responsible when a task silently fails. What architectural issue does this describe?
A) Insufficient prompt caching
B) A flat/mesh topology anti-pattern — no single place owns integration and failure handling
C) Overuse of the Batch API
D) A missing JSON schema

---

## Section 2: Tool Design & MCP Integration (Q15–23)

**Q15.** Which is the strongest description for a custom tool named `get_weather`?
A) `"Gets weather."`
B) `"Weather tool."`
C) `"Get current weather conditions for a specified location. Use this when the user asks about current conditions, temperature, or forecasts for a specific place."`
D) No description is needed if the tool name is self-explanatory

**Q16.** A tool call fails because an upstream API returned a 500 error. Which tool_result is the best design?
A) Return an empty array `[]` so the agent doesn't get confused by error text
B) Return `{"isError": true, "isRetryable": true, "errorCategory": "upstream_unavailable", "message": "Order service returned 500; safe to retry"}`
C) Return the raw HTTP response with no structure
D) Silently retry three times internally and never inform the model an error occurred

**Q17.** What are the three core primitives an MCP **server** exposes to clients?
A) Tools, Resources, Prompts
B) Sessions, Tokens, Endpoints
C) Models, Datasets, Pipelines
D) Requests, Responses, Errors

**Q18.** Which transport is typically used for a **local**, single-client MCP server (e.g., a filesystem server launched by Claude Desktop)?
A) Streamable HTTP with OAuth
B) Stdio
C) WebSockets
D) gRPC

**Q19.** An MCP client sends an `initialize` request but the client and server cannot agree on a mutually compatible protocol version. What should happen?
A) The connection proceeds using the client's version regardless
B) The connection should be terminated
C) The server silently ignores version mismatches and returns tools anyway
D) The client retries indefinitely with the same version

**Q20.** You want Claude to be **guaranteed** to call a specific tool, not just likely to call it based on the prompt. What should you configure?
A) A stronger system prompt reminding Claude to use the tool
B) `tool_choice: {"type": "tool", "name": "your_tool"}`
C) Increase `max_tokens`
D) Enable prompt caching

**Q21.** Logs show the agent frequently calls the wrong one of two similar tools, both of which have minimal one-line descriptions and accept similar-looking identifiers. What's the most effective **first step**?
A) Add 5-8 few-shot examples showing correct tool selection
B) Expand each tool's description with input formats, example queries, and explicit boundaries explaining when to use it versus the similar tool
C) Build a keyword-based routing layer that pre-selects the tool before each turn
D) Immediately consolidate both tools into one generic tool that infers which backend to call

**Q22.** A company builds an internal Slack-notification tool used only by one specific internal agent, with no plan to reuse it elsewhere. What's the simplest appropriate design?
A) A full MCP server with its own transport layer
B) A plain custom tool with an `input_schema`, executed directly by the app — no need for the MCP abstraction for a single-consumer, single-app integration
C) A Batch API job
D) A subagent with no tools

**Q23.** Which built-in tool combination is most appropriate for "find where a specific bug might live in an unfamiliar 500-file codebase" without spawning unnecessary subagents?
A) Bash with a hand-written `find | xargs grep` pipeline
B) Glob + Grep + Read, used directly
C) Immediately spawn 10 subagents, one per top-level directory
D) WebSearch, since the answer might be documented online

---

## Section 3: Claude Code Configuration & Workflows (Q24–33)

**Q24.** Which CLAUDE.md location **cannot** be excluded by individual project or user settings?
A) `./CLAUDE.md`
B) `~/.claude/CLAUDE.md`
C) The managed-policy CLAUDE.md (e.g., `/etc/claude-code/CLAUDE.md`)
D) `./CLAUDE.local.md`

**Q25.** A CLAUDE.md file has grown to 600 lines and covers only frontend conventions, but frontend tasks are a small fraction of the repo's work. What's the recommended fix?
A) Leave it as-is; length has no effect on instruction-following
B) Move the frontend-specific content into a `.claude/rules/frontend.md` file scoped with `paths: ["src/frontend/**"]`
C) Delete the file entirely
D) Duplicate it into every subdirectory

**Q26.** What's the key difference between CLAUDE.md and auto memory?
A) They are the same mechanism with different names
B) CLAUDE.md is written by you (instructions/rules); auto memory is written by Claude itself (learnings/patterns it noticed)
C) Auto memory is loaded in full every session with no size limit; CLAUDE.md is capped at 200 lines by the system
D) CLAUDE.md only works for subagents

**Q27.** You need Claude Code to enforce that a specific tool is **never** available to a session, regardless of what the user or Claude decides. Where do you configure this?
A) In the CLAUDE.md file, as a strongly worded instruction
B) In managed/project settings, via `permissions.deny`
C) By asking Claude nicely in the first message
D) It cannot be configured; it's model behavior only

**Q28.** For packaging a repeatable, shareable team workflow like `/deploy-staging` going forward, what's the currently preferred mechanism over the legacy `.claude/commands/*.md` format?
A) Skills (`.claude/skills/*/SKILL.md`)
B) A new CLAUDE.md entry per invocation
C) A shell alias
D) An MCP resource

**Q29.** After a long session triggers `/compact`, which memory content is guaranteed to be re-injected automatically?
A) Everything said anywhere in the conversation, verbatim
B) The project-root CLAUDE.md (re-read from disk); nested subdirectory CLAUDE.md files reload only on next relevant file access
C) Nothing; all context is permanently lost
D) Only auto memory, never CLAUDE.md

**Q30.** Which flag runs Claude Code non-interactively, suitable for piping into CI/CD scripts?
A) `--interactive`
B) `-p`
C) `--batch-mode`
D) `--headless-only`

**Q31.** A GitHub Action needs Claude Code to post a PR review comment that a downstream bot will parse automatically. Which combination of domains' techniques is required?
A) Only Domain 3 (CI/CD integration) — structured output isn't relevant here
B) Domain 3 (non-interactive `-p` mode / GitHub Actions integration) AND Domain 4 (structured/schema-validated output so the downstream bot can parse it reliably)
C) Only Domain 4 — CI/CD mechanics are irrelevant
D) Domain 2 only, since this is fundamentally an MCP problem

**Q32.** When is **plan mode** the better choice over letting Claude execute directly?
A) When the requested change is trivial and fully unambiguous
B) When the blast radius of a wrong first attempt is high, or requirements are ambiguous, and you want a reviewed proposal before side-effecting tool calls run
C) Never — direct execution is always faster and preferred
D) Only for read-only tasks

**Q33.** What does `/init` do?
A) Deletes any existing CLAUDE.md and starts from a blank file every time
B) Analyzes the codebase and generates/suggests a starting CLAUDE.md with discovered build/test commands and conventions
C) Installs MCP servers automatically
D) Runs the full test suite

---

## Section 4: Prompt Engineering & Structured Output (Q34–43)

**Q34.** You need extraction output that is reliably valid JSON matching an exact schema, because a downstream system will crash on malformed input. Which mechanism should you use?
A) Ask nicely in the prompt for "valid JSON only"
B) `tool_use` with a JSON schema — this eliminates JSON syntax errors by construction
C) Prefill the assistant's response with `{`
D) Increase temperature to encourage more creative formatting

**Q35.** A team validates extracted output only against its JSON Schema and ships it directly to a billing system. A bug slips through where amounts are swapped between `subtotal` and `tax` fields, both correctly typed as numbers. What's missing?
A) Nothing — schema validation was sufficient
B) Programmatic/semantic validation layered on top of schema validation — schemas check syntax/types, not whether values are logically correct
C) A larger context window
D) The Batch API

**Q36.** Roughly how many examples does Anthropic recommend for effective few-shot/multishot prompting?
A) 1
B) 3–5
C) 50+
D) 0 — examples reduce reliability

**Q37.** Which technique is recommended for structuring a prompt that mixes instructions, background context, examples, and variable user input?
A) Concatenate everything as one undifferentiated block of prose
B) Wrap each content type in its own XML tag (`<instructions>`, `<context>`, `<example>`, `<input>`) so Claude can parse them unambiguously
C) Put everything in the system prompt and leave the user message empty
D) Use only bullet points, never tags

**Q38.** For a 40,000-token document analysis prompt, where should the document go relative to the query/instructions?
A) It doesn't matter — models are order-invariant
B) At the top of the prompt, with the query/instructions after it — improves response quality, especially for complex multi-document inputs
C) Always at the very end, right before the answer
D) Split evenly, half before and half after the query

**Q39.** A batch classification job over 2 million historical records, with no user waiting in real time, needs the lowest possible cost. What should you use?
A) Standard synchronous Messages API calls, one at a time
B) The Message Batches API — ~50% cost savings, acceptable given the up-to-24-hour latency and no real-time requirement
C) The Batch API for a live customer chat feature too, to save costs everywhere
D) Prompt caching alone, with no batching

**Q40.** Which is a stronger way to instruct Claude to avoid markdown bullet lists in long-form output?
A) "Do not use bullet points."
B) "Write in flowing prose paragraphs using complete sentences; reserve markdown for inline code and simple headings." (telling Claude what *to* do, not just what to avoid)
C) Leave it unspecified and hope for the best
D) Set `max_tokens` very low

**Q41.** What's the primary purpose of a validation/retry loop for structured output?
A) To silently discard failed generations without telling the model why
B) To validate output, and on failure feed the specific validation error back to Claude so the retry can correct the actual problem
C) To always retry with the exact same prompt regardless of the failure reason
D) To increase the temperature parameter until output validates by chance

**Q42.** A prompt says "NEVER use ellipses in your response." A more effective version adds:
A) Nothing — the instruction is already maximally clear
B) The reason: "your response is read by a text-to-speech engine that cannot pronounce ellipses" — context/motivation helps Claude generalize correctly
C) All-caps repeated five times for emphasis
D) A financial penalty clause

**Q43.** What does `tool_choice: "none"` do?
A) Forces Claude to call every available tool
B) Prevents Claude from calling any tool, forcing a direct text response
C) Deletes all tool definitions from the request
D) Is equivalent to `tool_choice: "auto"`

---

## Section 5: Context Management & Reliability (Q44–50)

**Q44.** During an extended codebase-exploration session, the model starts giving inconsistent answers and refers to "typical patterns" instead of the specific classes it identified earlier in the same session. What's the most effective mitigation?
A) Restart the task from scratch with no context at all
B) Have the agent maintain a scratchpad file recording key findings, and reference it explicitly for subsequent questions
C) Ignore it — this is expected and self-corrects
D) Switch to a completely different, unrelated task to "reset" the model

**Q45.** A coordinator needs to survive a crash mid-way through a long multi-agent exploration and resume where it left off. What's the recommended design?
A) Rely on the model's memory of the conversation with no external state
B) Have each agent export structured state to a known location; the coordinator loads a manifest on resume and re-injects it into agent prompts
C) Restart the entire exploration from the beginning every time
D) Store all state only in the system prompt of the next session

**Q46.** A team assumes that upgrading to a model with a much larger context window automatically fixes their agent's tendency to miss details buried in a huge input. What's the flaw in this reasoning?
A) There is no flaw; bigger windows always fix this
B) Larger windows don't prevent "lost in the middle" attention dilution — the fix is better context structuring (tags, quote-grounding, document-then-query ordering), not just more capacity
C) Larger context windows always cost less, so there's no tradeoff to consider
D) Context window size only affects output tokens, not input handling

**Q47.** A subagent's API call fails, and the subagent returns an empty result to the coordinator instead of an explicit error. What downstream risk does this create?
A) None — empty results are always interpreted correctly
B) The coordinator (or end user) may mistake "the call failed" for "there was genuinely nothing to find," producing a confidently wrong conclusion
C) It automatically triggers a retry with no side effects
D) It reduces token costs with no other consequences

**Q48.** What should trigger escalation of a task from an autonomous agent to a human reviewer?
A) The model self-reporting low confidence in its own answer
B) Objective, externally verifiable criteria — e.g., a validation check failing repeatedly, a specific error category, or a defined risk/monetary threshold being crossed
C) A random sampling of 1% of all requests, regardless of content
D) Whenever the response exceeds 500 tokens

**Q49.** Which combination best preserves information provenance when multiple subagents synthesize a final answer from several source documents?
A) Return only the final synthesized text, discarding which subagent found which fact
B) Ground each claim in an extracted quote tied to its specific source document, so a human reviewer can verify the synthesis against original sources
C) Merge all subagent outputs into one paragraph with no attribution
D) Provenance doesn't matter once synthesis is complete

**Q50.** Your extraction pipeline reports 97% overall accuracy, and the team wants to reduce human review to cut costs. What should you check before doing so?
A) Nothing — a 97% aggregate figure is sufficient justification on its own
B) Accuracy broken down by document type and field segment, plus stratified sampling of high-confidence extractions specifically, since an aggregate figure can mask poor performance on a specific segment
C) Only the extractions the model already flagged as low-confidence
D) Whether the batch job finished within its SLA window

---

# Answer Key & Explanations (Sections 1–5)

| Q | Answer | Why (Domain, Task Statement) |
|---|---|---|
| 1 | B | Hub-and-spoke: coordinator owns decomposition/integration/failure-handling — D1, TS 1.2 |
| 2 | C | Hooks are code-enforced, unlike prompts/CLAUDE.md — D1, TS 1.4/1.5 / anti-pattern #1 |
| 3 | B | Parallelizable / isolated / independent work is the delegation criterion — D1, TS 1.2/1.3 |
| 4 | B | Agent SDK gives you the loop + built-in tools out of the box — D1 overview |
| 5 | B | Prototype on Agent SDK, scale on Managed Agents — D1 overview |
| 6 | B | `parent_tool_use_id`-style attribution of subagent output — D1, TS 1.3 |
| 7 | B | Least privilege: only the tools the role needs — D1, TS 1.3; D2, TS 2.3; anti-pattern #5 |
| 8 | A | `--resume <session-name>` continues a specific named session — D1, TS 1.7 |
| 9 | B | Resume continues; fork_session branches without mutating original — D1, TS 1.7 |
| 10 | B | CLAUDE.md is guidance, not enforcement — anti-pattern #1 |
| 11 | B | Structured JSON + freeform notes + git checkpoints — D1, TS 1.6 |
| 12 | B | Large-scale/architectural/ambiguous → plan mode — D3, TS 3.4 |
| 13 | B | Least privilege / tool scoping per role — D2, TS 2.3 |
| 14 | B | Hub-and-spoke required for observability/failure-handling — D1, TS 1.2 |
| 15 | C | Description should say what AND when to use it — D2, TS 2.1 |
| 16 | B | Structured error with isError/isRetryable/errorCategory — D2, TS 2.2; anti-pattern #6 |
| 17 | A | Tools, Resources, Prompts — D2, TS 2.4 |
| 18 | B | Stdio for local, typically single-client — D2, TS 2.4 |
| 19 | B | Version mismatch → terminate connection (general MCP protocol knowledge) |
| 20 | B | `tool_choice` forced selection guarantees a specific tool call — D2, TS 2.3 |
| 21 | B | Expand descriptions first — the confirmed root-cause fix, not few-shot/routing/consolidation — D2, TS 2.1; anti-pattern #4 |
| 22 | B | Single-consumer integration doesn't need MCP overhead — D2, TS 2.4 |
| 23 | B | Narrowest correct built-in combo, no unnecessary subagents — D2, TS 2.5 |
| 24 | C | Managed policy CLAUDE.md can't be excluded — D3, TS 3.1 |
| 25 | B | Path-scoped `.claude/rules/` reduces noise & keeps files short — D3, TS 3.1/3.3 |
| 26 | B | You write CLAUDE.md; Claude writes auto memory — D3, TS 3.1 |
| 27 | B | `permissions.deny`-style hard enforcement, distinct from CLAUDE.md guidance — anti-pattern #1 |
| 28 | A | Skills are the modern preferred mechanism — D3, TS 3.2 |
| 29 | B | `/memory` verifies loaded files; general Claude Code memory knowledge — D3, TS 3.1 |
| 30 | B | `-p` = non-interactive/print mode — D3, TS 3.6 |
| 31 | B | CI/CD mechanics (D3, TS 3.6) + reliable structured output (D4, TS 4.3) together |
| 32 | B | Large-scale/architectural/ambiguous → plan mode — D3, TS 3.4; anti-pattern #18 |
| 33 | B | `/init` analyzes codebase, generates/suggests CLAUDE.md — D3, TS 3.1 |
| 34 | B | `tool_use` + JSON schema eliminates syntax errors by construction — D4, TS 4.3 |
| 35 | B | Schema = syntax only; need semantic validation too — D4, TS 4.3/4.4; anti-pattern #8 |
| 36 | B | 2–4 targeted examples for ambiguous scenarios — D4, TS 4.2 |
| 37 | B | XML tags disambiguate mixed content types (general prompt-structuring knowledge) |
| 38 | B | Long documents first, query last (general prompt-structuring knowledge) |
| 39 | B | Batch API for bulk/offline, not real-time — D4, TS 4.5; anti-pattern #9 |
| 40 | B | Explicit criteria beat vague/general instructions — D4, TS 4.1 |
| 41 | B | Feed the actual validation error back for a targeted retry — D4, TS 4.4 |
| 42 | B | Context/motivation improves generalization (general prompting knowledge) |
| 43 | B | `tool_choice: "none"` blocks all tool calls — D2, TS 2.3 |
| 44 | B | Scratchpad files counteract context degradation in long exploration — D5, TS 5.4 |
| 45 | B | Structured state exports + manifest for crash recovery — D5, TS 5.4 |
| 46 | B | "Lost in the middle" isn't fixed by a bigger window — D5, TS 5.1; anti-pattern #10 |
| 47 | B | Empty result masks failure as "nothing found" — D2, TS 2.2; D5, TS 5.3; anti-pattern #6 |
| 48 | B | Escalate on objective criteria, not self-reported confidence — D5, TS 5.2; anti-pattern #11 |
| 49 | B | Structured claim-source mappings preserved through synthesis — D5, TS 5.6 |
| 50 | B | Segment/stratified accuracy check before reducing review — D5, TS 5.5; anti-pattern #13 |

## Scoring guide
- Passing bar is **confirmed**: 720/1000 scaled score. On this 50-question set, treat **36/50 (72%)** as your rough "would-pass" floor, but aim well above it before booking the real thing.
- If you miss more than 2 questions in any one section, go back and re-read that domain file plus the matching anti-patterns before moving on.

---

# Section 6: Official Sample Questions (verbatim from the Exam Guide)

These 12 questions are reproduced directly from the official Exam Guide's own "Sample Questions" section (§9), including Anthropic's own correct answers and explanations. They're organized by the same scenario categories the real exam draws from, and are the single best calibration you have for real question difficulty and style.

### Scenario: Customer Support Resolution Agent

**Question 1.** Production data shows that in 12% of cases, your agent skips `get_customer` entirely and calls `lookup_order` using only the customer's stated name, occasionally leading to misidentified accounts and incorrect refunds. What change would most effectively address this reliability issue?
A. Add a programmatic prerequisite that blocks `lookup_order` and `process_refund` calls until `get_customer` has returned a verified customer ID.
B. Enhance the system prompt to state that customer verification via `get_customer` is mandatory before any order operations.
C. Add few-shot examples showing the agent always calling `get_customer` first, even when customers volunteer order details.
D. Implement a routing classifier that analyzes each request and enables only the subset of tools appropriate for that request type.
**Answer: A.** Programmatic enforcement provides deterministic guarantees that prompt-based approaches (B, C) cannot when errors have financial consequences. D addresses tool availability, not tool ordering — not the actual problem.

**Question 2.** Production logs show the agent frequently calls `get_customer` when users ask about orders (e.g., "check my order #12345"), instead of calling `lookup_order`. Both tools have minimal descriptions ("Retrieves customer information" / "Retrieves order details") and accept similar identifier formats. What's the most effective first step to improve tool selection reliability?
A. Add few-shot examples to the system prompt demonstrating correct tool selection patterns, with 5-8 examples showing order-related queries routing to `lookup_order`.
B. Expand each tool's description to include input formats it handles, example queries, edge cases, and boundaries explaining when to use it versus similar tools.
C. Implement a routing layer that parses user input before each turn and pre-selects the appropriate tool based on detected keywords and identifier patterns.
D. Consolidate both tools into a single `lookup_entity` tool that accepts any identifier and internally determines which backend to query.
**Answer: B.** Tool descriptions are the primary mechanism LLMs use for tool selection. This is a low-effort, high-leverage root-cause fix. A adds token overhead without fixing the underlying issue; C is over-engineered and bypasses the LLM's natural language understanding; D is a valid architectural choice but more effort than a "first step" warrants.

**Question 3.** Your agent achieves 55% first-contact resolution, well below the 80% target. Logs show it escalates straightforward cases (standard damage replacements with photo evidence) while attempting to autonomously handle complex situations requiring policy exceptions. What's the most effective way to improve escalation calibration?
A. Add explicit escalation criteria to your system prompt with few-shot examples demonstrating when to escalate versus resolve autonomously.
B. Have the agent self-report a confidence score (1-10) before each response and automatically route requests to humans when confidence falls below a threshold.
C. Deploy a separate classifier model trained on historical tickets to predict which requests need escalation before the main agent begins processing.
D. Implement sentiment analysis to detect customer frustration levels and automatically escalate when negative sentiment exceeds a threshold.
**Answer: A.** This directly addresses the root cause: unclear decision boundaries. B fails because LLM self-reported confidence is poorly calibrated. C is over-engineered given prompt optimization hasn't been tried. D solves a different problem — sentiment doesn't correlate with case complexity.

### Scenario: Code Generation with Claude Code

**Question 4.** You want to create a custom `/review` slash command that runs your team's standard code review checklist. This command should be available to every developer when they clone or pull the repository. Where should you create this command file?
A. In the `.claude/commands/` directory in the project repository
B. In `~/.claude/commands/` in each developer's home directory
C. In the CLAUDE.md file at the project root
D. In a `.claude/config.json` file with a commands array
**Answer: A.** Project-scoped custom slash commands live in `.claude/commands/`, version-controlled and automatically shared. B is for personal commands not shared via version control. C is for context, not command definitions. D doesn't exist in Claude Code.

**Question 5.** You've been assigned to restructure the team's monolithic application into microservices. This will involve changes across dozens of files and requires decisions about service boundaries and module dependencies. Which approach should you take?
A. Enter plan mode to explore the codebase, understand dependencies, and design an implementation approach before making changes.
B. Start with direct execution and make changes incrementally, letting the implementation reveal the natural service boundaries.
C. Use direct execution with comprehensive upfront instructions detailing exactly how each service should be structured.
D. Begin in direct execution mode and only switch to plan mode if you encounter unexpected complexity during implementation.
**Answer: A.** Plan mode is designed for exactly this: large-scale changes, multiple valid approaches, architectural decisions. B risks costly rework; C assumes you already know the right structure; D ignores that the complexity is already known upfront.

**Question 6.** Your codebase has distinct areas with different coding conventions: React components use functional style with hooks, API handlers use async/await with specific error handling, and database models follow a repository pattern. Test files are spread throughout the codebase alongside the code they test (e.g., `Button.test.tsx` next to `Button.tsx`), and you want all tests to follow the same conventions regardless of location. What's the most maintainable way to ensure Claude automatically applies the correct conventions when generating code?
A. Create rule files in `.claude/rules/` with YAML frontmatter specifying glob patterns to conditionally apply conventions based on file paths
B. Consolidate all conventions in the root CLAUDE.md file under headers for each area, relying on Claude to infer which section applies
C. Create skills in `.claude/skills/` for each code type that include the relevant conventions in their SKILL.md files
D. Place a separate CLAUDE.md file in each subdirectory containing that area's specific conventions
**Answer: A.** Glob patterns (e.g. `**/*.test.tsx`) apply based on file path regardless of directory location — essential for test files spread throughout. B relies on unreliable inference. C requires manual invocation. D can't handle files spread across many directories.

### Scenario: Multi-Agent Research System

**Question 7.** After running the system on the topic "impact of AI on creative industries," you observe that each subagent completes successfully: the web search agent finds relevant articles, the document analysis agent summarizes papers correctly, and the synthesis agent produces coherent output. However, the final reports cover only visual arts, completely missing music, writing, and film production. When you examine the coordinator's logs, you see it decomposed the topic into three subtasks: "AI in digital art creation," "AI in graphic design," and "AI in photography." What is the most likely root cause?
A. The synthesis agent lacks instructions for identifying coverage gaps in the findings it receives from other agents.
B. The coordinator agent's task decomposition is too narrow, resulting in subagent assignments that don't cover all relevant domains of the topic.
C. The web search agent's queries are not comprehensive enough and need to be expanded to cover more creative industry sectors.
D. The document analysis agent is filtering out sources related to non-visual creative industries due to overly restrictive relevance criteria.
**Answer: B.** The coordinator's logs reveal the root cause directly. The subagents executed their assigned tasks correctly — the problem is what they were assigned. A, C, D incorrectly blame downstream agents working correctly within their assigned scope.

**Question 8.** The web search subagent times out while researching a complex topic. You need to design how this failure information flows back to the coordinator agent. Which error propagation approach best enables intelligent recovery?
A. Return structured error context to the coordinator including the failure type, the attempted query, any partial results, and potential alternative approaches.
B. Implement automatic retry logic with exponential backoff within the subagent, returning a generic "search unavailable" status only after all retries are exhausted.
C. Catch the timeout within the subagent and return an empty result set marked as successful.
D. Propagate the timeout exception directly to a top-level handler that terminates the entire research workflow.
**Answer: A.** Structured error context gives the coordinator what it needs for intelligent recovery. B's generic status hides valuable context. C suppresses the error by marking failure as success. D terminates the whole workflow unnecessarily.

**Question 9.** During testing, you observe that the synthesis agent frequently needs to verify specific claims while combining findings. Currently, when verification is needed, the synthesis agent returns control to the coordinator, which invokes the web search agent, then re-invokes synthesis with results. This adds 2-3 round trips per task and increases latency by 40%. Your evaluation shows that 85% of these verifications are simple fact-checks (dates, names, statistics) while 15% require deeper investigation. What's the most effective approach to reduce overhead while maintaining system reliability?
A. Give the synthesis agent a scoped `verify_fact` tool for simple lookups, while complex verifications continue delegating to the web search agent through the coordinator.
B. Have the synthesis agent accumulate all verification needs and return them as a batch to the coordinator at the end of its pass, which then sends them all to the web search agent at once.
C. Give the synthesis agent access to all web search tools so it can handle any verification need directly without round-trips through the coordinator.
D. Have the web search agent proactively cache extra context around each source during initial research, anticipating what the synthesis agent might need to verify.
**Answer: A.** Applies least privilege: only what's needed for the 85% common case, while preserving coordination for complex cases. B creates blocking dependencies. C over-provisions, violating separation of concerns. D relies on unreliable speculative caching.

### Scenario: Claude Code for Continuous Integration

**Question 10.** Your pipeline script runs `claude "Analyze this pull request for security issues"` but the job hangs indefinitely. Logs indicate Claude Code is waiting for interactive input. What's the correct approach to run Claude Code in an automated pipeline?
A. Add the `-p` flag: `claude -p "Analyze this pull request for security issues"`
B. Set the environment variable `CLAUDE_HEADLESS=true` before running the command
C. Redirect stdin from `/dev/null`: `claude "Analyze this pull request for security issues" < /dev/null`
D. Add the `--batch` flag: `claude --batch "Analyze this pull request for security issues"`
**Answer: A.** `-p`/`--print` is the documented non-interactive mode. B and D reference non-existent features; C is an unreliable Unix workaround.

**Question 11.** Your team wants to reduce API costs for automated analysis. Currently, real-time Claude calls power two workflows: (1) a blocking pre-merge check that must complete before developers can merge, and (2) a technical debt report generated overnight for review the next morning. Your manager proposes switching both to the Message Batches API for its 50% cost savings. How should you evaluate this proposal?
A. Use batch processing for the technical debt reports only; keep real-time calls for pre-merge checks.
B. Switch both workflows to batch processing with status polling to check for completion.
C. Keep real-time calls for both workflows to avoid batch result ordering issues.
D. Switch both to batch processing with a timeout fallback to real-time if batches take too long.
**Answer: A.** Batch has no guaranteed latency SLA (up to 24h) — unsuitable for a blocking pre-merge check, ideal for the overnight report. B relies on unacceptable "often faster" completion for a blocking workflow. C reflects a misconception (results correlate via `custom_id`). D adds unneeded complexity.

**Question 12.** A pull request modifies 14 files across the stock tracking module. Your single-pass review analyzing all files together produces inconsistent results: detailed feedback for some files but superficial comments for others, obvious bugs missed, and contradictory feedback — flagging a pattern as problematic in one file while approving identical code elsewhere in the same PR. How should you restructure the review?
A. Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.
B. Require developers to split large PRs into smaller submissions of 3-4 files before the automated review runs.
C. Switch to a higher-tier model with a larger context window to give all 14 files adequate attention in one pass.
D. Run three independent review passes on the full PR and only flag issues that appear in at least two of the three runs.
**Answer: A.** Directly addresses attention dilution. B shifts burden to developers without improving the system. C misunderstands that larger windows don't solve attention-quality issues. D would suppress detection of real bugs caught only intermittently.

---

## Combined scoring guide

- **60-question mock**: take Sections 1–5 (50 Qs) plus a random 10 of the 12 official samples, timed to 120 minutes, to simulate the real exam's length exactly.
- Passing bar is confirmed at **720/1000** — on a percentage basis treat 72% as your floor, but push well past it before scheduling.
- Miss more than 2 in any section → re-read that domain file and the matching anti-patterns before moving on.
