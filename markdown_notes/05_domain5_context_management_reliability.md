# Domain 5: Context Management & Reliability (15%)

> 🟢 Rewritten directly from the official Exam Guide's 6 task statements for this domain.
>
> ⚠️ **Correction from the earlier draft**: prompt-caching mechanics (TTL, `cache_control` breakpoints, pricing multipliers) are **explicitly out of scope** per the official guide ("beyond knowing it exists"). This domain is actually about **information management and reliability judgment**, not caching internals. Rewritten accordingly.

---

## Task Statement 5.1 — Manage conversation context to preserve critical information across long interactions

**Progressive summarization risk**: numerical values, percentages, dates, and customer-stated expectations get **condensed into vague summaries** as a conversation is compressed — precisely the details that matter most for a correct outcome.

**"Lost in the middle"**: models reliably process information at the **beginning and end** of long inputs but may **omit findings from middle sections**. This is the exam's core context-structuring concept for this domain (distinct from, but related to, Domain 1's attention-dilution point about splitting large reviews into passes).

**Token-cost-vs-relevance mismatch**: tool results accumulate in context **disproportionately to their relevance** — e.g., an order lookup returning 40+ fields when only 5 are relevant to the task at hand.

**Skills tested**:
- Extracting **transactional facts** (amounts, dates, order numbers, statuses) into a persistent **"case facts" block** included in every prompt, kept **outside** the summarized/compressible history
- **Trimming verbose tool outputs** to only the relevant fields *before* they accumulate in context
- **Placing key findings summaries at the beginning** of aggregated inputs, with explicit section headers organizing detail — mitigating the position effect
- Requiring subagents to include **metadata** (dates, source locations, methodological context) in structured outputs to support accurate downstream synthesis
- When a downstream agent has a **limited context budget**, have the upstream agent return **structured data** (key facts, citations, relevance scores) instead of verbose prose and reasoning chains

## Task Statement 5.2 — Design effective escalation and ambiguity resolution patterns

**Correct escalation triggers**: an explicit customer request for a human, a genuine **policy exception or gap** (not just "this case is complex"), or inability to make meaningful progress.

**Named anti-patterns** (both explicitly called out in the guide):
- **Sentiment-based escalation** — detecting frustration and auto-escalating on that basis doesn't correlate with actual case complexity
- **Self-reported confidence scores** as an escalation proxy — same unreliability problem as sentiment

**Nuance the exam tests**: honor an **explicit** request for a human **immediately**, without first attempting investigation. But if a customer is merely frustrated and the issue is within the agent's capability, **acknowledge the frustration while still offering to resolve it** — only escalate if they reiterate their preference for a human after that.

**Policy-gap escalation example**: if policy addresses own-site price adjustments but is silent on **competitor** price matching, that silence is itself a reason to escalate — not a reason to improvise.

**Multiple-match handling**: when a tool call returns multiple candidate matches (e.g., several customers with a similar name), the correct behavior is to **ask for an additional identifier** — never pick one via heuristic guessing.

## Task Statement 5.3 — Implement error propagation strategies across multi-agent systems

**Structured error context** — failure type, the query that was attempted, any partial results, and possible alternative approaches — is what lets a **coordinator** make an intelligent recovery decision (retry differently, try an alternate approach, or proceed with partial results and flag the gap).

**Two named anti-patterns, memorize both**:
- **Silently suppressing errors** — returning an empty result and marking it as success
- **Terminating the entire workflow** on a single subagent failure

Both are wrong for the same underlying reason: they throw away the coordinator's ability to make an informed decision — one by hiding the failure, the other by overreacting to it.

**Distinguish precisely**: an **access failure** (e.g., a timeout) needs a retry decision; a **valid empty result** (a query that succeeded and legitimately found nothing) does not — conflating the two, in either direction, breaks downstream reasoning.

**Skill**: structuring synthesis output with **coverage annotations** — explicitly marking which findings are well-supported vs. which topic areas have gaps because a source was unavailable.

## Task Statement 5.4 — Manage context effectively in large codebase exploration

**Context degradation symptom**: in long sessions, a model starts giving **inconsistent answers** and referencing "typical patterns" instead of the **specific classes it actually discovered earlier** — a sign context has degraded and needs active management, not just more tokens.

**Mitigations tested**:
- **Subagent delegation** to isolate verbose exploration output while the main agent keeps only high-level coordination in its own context
- **Scratchpad files** — have agents record key findings to a file and reference it for later questions, directly counteracting degradation
- **Summarize before spawning the next phase** — summarize key findings from one exploration phase, then inject that summary into the next phase's initial context rather than carrying the full raw exploration forward
- **Structured state persistence for crash recovery** — each agent exports state to a known location; the coordinator loads a **manifest** on resume and re-injects it into agent prompts
- **`/compact`** — reduces context usage during extended exploration sessions once verbose discovery output has filled the window

## Task Statement 5.5 — Design human review workflows and confidence calibration

**The masking risk**: an aggregate accuracy figure (e.g., "97% overall") can **mask poor performance on specific document types or fields** — a segment could be far worse than the headline number suggests.

**Techniques tested**:
- **Stratified random sampling** of *high-confidence* extractions specifically — to measure real error rates and catch novel error patterns that a naive "check the low-confidence ones" approach would miss
- **Field-level confidence scores**, calibrated against a **labeled validation set**, used to route review attention
- Validate accuracy **by document type and field segment** before reducing/automating away human review for high-confidence cases
- Route extractions with **low confidence or ambiguous/contradictory source documents** to human review, prioritizing scarce reviewer capacity toward the cases that need it most

## Task Statement 5.6 — Preserve information provenance and handle uncertainty in multi-source synthesis

**Root failure mode**: source attribution gets **lost during summarization** when findings are compressed without preserving the claim-to-source mapping.

**Fix**: require subagents to output **structured claim-source mappings** (source URL, document name, relevant excerpt) that downstream synthesis **preserves and merges** rather than discarding.

**Conflicting-source handling**: when two credible sources give **different statistics**, the correct behavior is to **include both values with source attribution explicitly annotated** — not arbitrarily pick one. Let the coordinator (or a human) decide how to reconcile before final synthesis, rather than silently resolving the conflict for them.

**Temporal data**: require **publication/collection dates** in structured outputs — otherwise a genuine **time-based** difference between two sources can be misread as a **contradiction**.

**Presentation skill**: render different content types appropriately in the final synthesis — financial data as tables, news as prose, technical findings as structured lists — rather than flattening everything into one uniform format.

---

## Quick self-check

- [ ] I can explain "lost in the middle" and name at least two mitigations (case-facts block, summary-first ordering).
- [ ] I know sentiment-based escalation and self-reported confidence are both named anti-patterns for escalation triggers.
- [ ] I can distinguish an access failure (needs retry decision) from a valid empty result, and explain why suppressing errors and terminating the whole workflow are both wrong.
- [ ] I know scratchpad files, phase-summarization, and crash-recovery manifests as context-degradation mitigations for long codebase exploration.
- [ ] I can explain why a 97%-aggregate accuracy figure can still hide a bad segment, and what stratified sampling of high-confidence cases is for.
- [ ] I know why conflicting source statistics should be preserved with attribution, not arbitrarily resolved — and why publication dates matter for that.

Track these in the [progress tracker](tracker.html).
