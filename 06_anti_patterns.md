# Anti-Patterns & Common Pitfalls — The Exam's "Wrong Answer" Playbook

> 🟢 Rewritten against the official Exam Guide. Every pattern below is either **directly named** in the guide's task statements/sample questions (marked ✅ Confirmed) or a reasonable engineering-judgment extension consistent with the guide's stated principles (marked 🔹 Supplementary). Read this after finishing all 5 domain files.

Scenario exams give you 3–4 plausible options where only one is sound. These patterns are what usually makes the others wrong.

---

### 1. ✅ Relying on prompts instead of programmatic enforcement for critical rules
**Trap**: "We told Claude in the system prompt that customer verification is mandatory before any order operation."
**Why it's wrong**: The guide's own phrasing — prompt instructions alone have a **non-zero failure rate**. When deterministic compliance matters (e.g., identity verification before a financial operation), probabilistic compliance isn't good enough.
**Fix**: Programmatic prerequisites/hooks — e.g., a gate that blocks `process_refund` until `get_customer` has returned a verified ID. *(Domain 1, Task Statement 1.4/1.5)*

### 2. ✅ Loop termination via natural-language parsing, arbitrary iteration caps, or text-presence checks
**Trap**: Deciding an agentic loop is "done" by scanning the assistant's text for phrases like "I'm finished," or by capping iterations at a fixed number as the primary stop mechanism, or by checking whether any text content was returned.
**Why it's wrong**: None of these are the actual signal the API gives you. The loop should be governed by `stop_reason`.
**Fix**: Continue while `stop_reason == "tool_use"`, stop at `"end_turn"`. *(Domain 1, Task Statement 1.1)*

### 3. ✅ Overly narrow task decomposition by a coordinator
**Trap**: A coordinator asked to research "AI's impact on creative industries" spins up subtasks only for digital art, graphic design, and photography — completely missing music, writing, and film.
**Why it's wrong**: Every subagent can execute its assigned task perfectly and the system still fails, because the **coordinator** defined too narrow a scope. This is a decomposition failure, not an execution failure — don't blame downstream agents that did exactly what they were asked.
**Fix**: Coordinator scope review — does the decomposition actually cover the full breadth of the request? *(Domain 1, Task Statement 1.2 — this is the exact scenario behind the guide's own Sample Question 7)*

### 4. ✅ Ambiguous or overlapping tool descriptions causing misrouting
**Trap**: Two tools like `analyze_content` and `analyze_document` with near-identical minimal descriptions ("Retrieves customer information" / "Retrieves order details") cause the model to pick the wrong one.
**Why it's wrong**: Tool descriptions are the **primary mechanism** models use for tool selection — thin or overlapping descriptions remove the only signal the model has.
**Fix**: Expand descriptions with input formats, example queries, edge cases, and explicit "use this vs. that" boundaries — this is the correct **first step**, ahead of few-shot examples, a routing layer, or consolidating tools. *(Domain 2, Task Statement 2.1 — behind the guide's own Sample Question 2)*

### 5. ✅ Giving one agent too many tools, or tools outside its specialization
**Trap**: An agent has 18 tools available "just in case," including ones (like web search) that belong to a different agent's role.
**Why it's wrong**: More tools increases decision complexity and degrades selection reliability; agents given tools outside their specialization tend to misuse them.
**Fix**: Scope tools tightly per role (the guide's own example: 4–5, not 18), with narrow cross-role tools reserved only for specific high-frequency needs. *(Domain 2, Task Statement 2.3)*

### 6. ✅ Uniform/generic error responses, and confusing access failures with valid empty results
**Trap**: Every tool failure returns `"Operation failed"`; or an empty result set is treated the same whether the query legitimately found nothing or the call actually broke.
**Why it's wrong**: Generic errors hide the context a coordinator needs to recover intelligently. Access failures (timeouts) need a retry decision; valid empty results (a successful query with no matches) do not — conflating them in either direction breaks downstream reasoning.
**Fix**: Structured error metadata — `errorCategory`, `isRetryable`, human-readable description — and a clear distinction between "failed" and "succeeded with nothing found." *(Domain 2, Task Statement 2.2; Domain 5, Task Statement 5.3)*

### 7. ✅ Silently suppressing subagent errors, or terminating the whole workflow on one failure
**Trap**: A failing subagent either quietly returns an empty result marked "success," or its failure kills the entire multi-agent run.
**Why it's wrong**: These are opposite overcorrections to the same underlying problem — both throw away the coordinator's ability to make an informed recovery decision, one by hiding the failure, the other by overreacting to it.
**Fix**: Structured error context (failure type, what was attempted, partial results, alternatives) propagated to the coordinator, which can then retry, try an alternative, or proceed with partial results and annotate the gap. *(Domain 5, Task Statement 5.3)*

### 8. ✅ Schema validation mistaken for semantic correctness
**Trap**: Assuming a `tool_use` call that matches its JSON schema is necessarily a *correct* extraction.
**Why it's wrong**: Strict schemas eliminate **syntax** errors but not **semantic** ones — line items that don't sum to the stated total, or a value in the wrong field, can still pass schema validation cleanly.
**Fix**: Add semantic checks alongside schema validation — e.g., extract both `calculated_total` and `stated_total` and flag discrepancies. *(Domain 4, Task Statement 4.3/4.4)*

### 9. ✅ Routing a blocking, user-facing workflow through the Message Batches API
**Trap**: Switching a pre-merge check (developers are waiting) to Batch because it's 50% cheaper.
**Why it's wrong**: Batch has **no guaranteed latency SLA** (up to 24 hours) and **doesn't support multi-turn tool calling** in a single request — both disqualifying for a blocking workflow.
**Fix**: Match the API to the latency tolerance: synchronous for blocking checks, Batch for overnight/weekly non-blocking analysis. *(Domain 4, Task Statement 4.5 — behind the guide's own Sample Question 11)*

### 10. ✅ Assuming a bigger context window fixes attention dilution
**Trap**: "Upgrade to a model with a larger context window so all 14 files get equal attention in one review pass."
**Why it's wrong**: A single pass over many files produces inconsistent depth and even contradictory findings (approving a pattern in one file, flagging it in another) — that's an attention-dilution problem, not a capacity problem, and a bigger window doesn't fix it.
**Fix**: Split into per-file local-analysis passes plus a separate cross-file integration pass. *(Domain 1, Task Statement 1.6; Domain 4, Task Statement 4.6 — behind the guide's own Sample Question 12)*

### 11. ✅ Self-reported model confidence, or customer sentiment, as an escalation trigger
**Trap**: "Escalate to a human whenever the model's self-reported confidence drops below N," or "escalate whenever sentiment analysis detects frustration."
**Why it's wrong**: Both are named in the guide as **unreliable proxies for actual case complexity** — a model can be confidently wrong on a hard case, and frustration doesn't correlate with whether the case is actually hard.
**Fix**: Escalate on explicit customer request, genuine policy gaps/exceptions, or demonstrated inability to progress — not on a self-assessed or sentiment score. *(Domain 5, Task Statement 5.2 — behind the guide's own Sample Question 3)*

### 12. ✅ Heuristic selection among multiple ambiguous matches
**Trap**: A lookup returns several customers with a similar name, and the agent picks one based on a guess (most recent order, first alphabetically, etc.).
**Why it's wrong**: Guessing risks acting on the wrong person's data — in a support/financial context that's a real-harm mistake, not just an inconvenience.
**Fix**: Ask the customer for an additional identifier to disambiguate. *(Domain 5, Task Statement 5.2)*

### 13. ✅ Aggregate accuracy metrics masking segment-level failure
**Trap**: "Our extraction pipeline is 97% accurate overall, so we're fine to reduce human review."
**Why it's wrong**: A single aggregate number can hide much worse performance on a specific document type or field.
**Fix**: Validate accuracy by document type and field segment, and use stratified random sampling of *high-confidence* extractions specifically to catch novel error patterns before scaling back review. *(Domain 5, Task Statement 5.5)*

### 14. ✅ Arbitrarily resolving conflicting source data instead of preserving both
**Trap**: Two credible sources give different statistics, and the synthesis step picks one and moves on.
**Why it's wrong**: Silently discarding one value hides a real disagreement in the source material from anyone downstream who might need to judge it.
**Fix**: Include both values, explicitly annotated with source attribution, and let the coordinator/human decide how to reconcile. Also require publication/collection dates so a genuine time-based difference isn't misread as a contradiction. *(Domain 5, Task Statement 5.6)*

### 15. 🔹 Treating self-review as equivalent to independent review
**Trap**: Asking the same Claude session that generated code to also review it for bugs.
**Why it's wrong**: The guide states a session retains its own generation reasoning, making it less likely to question its own decisions — even with explicit self-review instructions or extended thinking.
**Fix**: Use a second, independent instance with no prior reasoning context for the review pass. *(Domain 3, Task Statement 3.6; Domain 4, Task Statement 4.6)*

### 16. 🔹 Session resumption without informing the agent what changed
**Trap**: Resuming a named session after code has been modified, assuming the agent will notice the drift on its own.
**Why it's wrong**: Resumption doesn't auto-detect file changes; stale tool results can silently mislead subsequent reasoning.
**Fix**: Explicitly tell a resumed session which files changed for targeted re-analysis; if prior tool results are too stale to trust, start a fresh session with a structured summary injected instead of resuming. *(Domain 1, Task Statement 1.7)*

### 17. 🔹 Consolidating all conventions into one root CLAUDE.md and relying on inference
**Trap**: Putting React, API, and database conventions all in one CLAUDE.md under separate headers, trusting Claude to apply the right section.
**Why it's wrong**: This relies on inference rather than deterministic matching — especially fragile for conventions (like test-file rules) that need to apply based on file path/type regardless of directory.
**Fix**: `.claude/rules/` files with YAML frontmatter `paths:` glob patterns, so the right convention loads automatically based on which file Claude is actually touching. *(Domain 3, Task Statement 3.3 — behind the guide's own Sample Question 6)*

### 18. 🔹 Choosing plan mode or direct execution based on when complexity is discovered, not what's already known
**Trap**: "Start in direct execution and only switch to plan mode if something unexpected comes up" — for a task that was described as a large-scale, multi-file, architecturally-significant change from the outset.
**Why it's wrong**: The complexity here isn't something that might emerge later — it's already known from the task description, so the safe-exploration value of plan mode should be used upfront, not reactively.
**Fix**: Use plan mode for investigation/design on tasks already known to be architecturally significant; reserve direct execution for well-scoped, well-understood changes. *(Domain 3, Task Statement 3.4 — behind the guide's own Sample Question 5)*

---

## How to use this list on exam day

When a scenario gives you 3–4 plausible options, check each one against this list: does it quietly commit one of these mistakes? In a well-written scenario item, exactly one option avoids all of them. Patterns marked ✅ are directly evidenced in the official guide's task statements or sample questions — weight those most heavily in your final review pass.
