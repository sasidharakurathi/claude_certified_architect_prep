# Domain 4: Prompt Engineering & Structured Output (20%)

> 🟢 Rewritten directly from the official Exam Guide's 6 task statements for this domain.
>
> ⚠️ **Correction from the earlier draft of this kit**: I had previously given significant space to a separate "Structured Outputs" API feature (`output_config.format`, `strict: true`, constrained decoding) and to prompt-caching mechanics. **The official exam guide does not mention a separate Structured Outputs/constrained-decoding feature at all**, and explicitly lists "prompt caching implementation details (beyond knowing it exists)" as **out of scope**. The exam's actual model of "reliable structured output" is **`tool_use` with JSON schemas** — full stop. That's what's below now.

---

## Task Statement 4.1 — Design prompts with explicit criteria to improve precision and reduce false positives

**Core principle**: explicit, categorical criteria beat vague instructions. "Flag comments only when the claimed behavior contradicts actual code behavior" works; "check that comments are accurate" doesn't.

**Named anti-pattern**: general instructions like "be conservative" or "only report high-confidence findings" **fail to improve precision** compared to specific categorical criteria — confidence-based filtering is not a substitute for defining what to report vs. skip.

**Trust dynamics fact worth remembering**: a high false-positive rate in **one category** undermines developer trust in **all** categories, even accurate ones — so a practical fix when one category is noisy is to **temporarily disable** that category while you improve its prompt, rather than let it poison trust in the whole review.

**Skills tested**: writing specific criteria for what to report (bugs, security) vs. skip (minor style, local patterns); defining explicit severity levels with concrete code examples for each level to get consistent classification.

## Task Statement 4.2 — Apply few-shot prompting to improve output consistency and quality

Few-shot examples are the **most effective technique** for consistent, actionable output when detailed prose instructions alone produce inconsistent results.

**What few-shot examples are good for, specifically** (per the guide):
- Demonstrating **ambiguous-case handling** (e.g., which tool to pick for an ambiguous request, what counts as a test-coverage gap)
- Enabling **generalization** to novel patterns, not just matching the exact cases shown
- **Reducing hallucination** in extraction tasks — e.g., correctly handling informal measurements or varied document structures instead of guessing

**Skills tested**:
- **2–4 targeted examples** for ambiguous scenarios, showing the *reasoning* for choosing one action over plausible alternatives
- Examples demonstrating the desired output format itself (e.g., location/issue/severity/suggested-fix fields)
- Examples distinguishing acceptable patterns from genuine issues (reduces false positives while still generalizing)
- Examples covering varied document structures (inline citations vs. bibliographies; methodology sections vs. embedded details) to fix empty/null extraction of required fields

## Task Statement 4.3 — Enforce structured output using tool use and JSON schemas

**This is the exam's actual "how do you get reliable structured output" answer**: `tool_use` with a JSON schema is the most reliable approach for **guaranteed schema-compliant** structured output — it **eliminates JSON syntax errors** by construction.

**`tool_choice` for structured output** (same three modes as Domain 2, applied here):
- `"auto"` — model may return plain text instead of calling a tool (not what you want when you need structured output)
- `"any"` — model **must** call a tool but may pick among several extraction schemas — right choice when the document type is unknown and multiple extraction tools exist
- Forced named tool (`{"type": "tool", "name": "extract_metadata"}`) — guarantees a **specific** extraction runs first, before enrichment steps in later turns

**Critical limitation to remember**: strict JSON schemas via `tool_use` eliminate **syntax** errors but do **not** prevent **semantic** errors — e.g., line items that don't sum to the stated total, or a value placed in the wrong field. Schema conformance ≠ correctness.

**Schema design skills**:
- **Optional/nullable fields** when the source document may simply not contain that information — this prevents the model from **fabricating** values just to satisfy a required field
- **Enum + "other" + detail-string pattern** for extensible categorization, and an explicit `"unclear"` enum value for genuinely ambiguous cases
- Include **format normalization rules** in the prompt alongside the strict schema, to handle inconsistent source formatting before it hits the schema

## Task Statement 4.4 — Implement validation, retry, and feedback loops for extraction quality

**Retry-with-error-feedback**: on a validation failure, the follow-up request should include the **original document**, the **failed extraction**, and the **specific validation error** — this is what lets the model self-correct.

**The limit of retries** (memorize this distinction): retries work for **format/structural** errors, but are **ineffective** when the required information is simply **absent from the source document** — no amount of retrying recovers information that was never there.

**Feedback-loop design**:
- A `detected_pattern` field on structured findings lets you analyze **which code constructs trigger findings** — useful for spotting systematic false-positive patterns when developers dismiss findings
- Self-correction validation flows: extract both `calculated_total` and `stated_total` to flag discrepancies; add a `conflict_detected` boolean for inconsistent source data — this converts a *semantic* error into something a schema-plus-logic check can actually catch

## Task Statement 4.5 — Design efficient batch processing strategies

**Message Batches API facts** (the exam's exact framing):
- **50% cost savings**
- **Up to 24-hour processing window**, with **no guaranteed latency SLA**
- **Does not support multi-turn tool calling within a single request** — you cannot execute a tool mid-request and get results back within that same batched call
- **`custom_id`** fields correlate each request/response pair

**Appropriateness rule**: batch is right for **non-blocking, latency-tolerant** workloads (overnight reports, weekly audits, nightly test generation) and **wrong** for **blocking** workflows (pre-merge checks a developer is waiting on).

**Practical skills**:
- Calculating submission frequency against an SLA (e.g., submitting every 4 hours to guarantee a 30-hour SLA against a 24-hour max batch window)
- Handling batch failures by **resubmitting only the failed documents** (identified via `custom_id`) with fixes (e.g., chunking documents that exceeded context limits) — not resubmitting the whole batch
- **Refining the prompt on a small sample first**, before batch-processing a large volume, to maximize first-pass success and avoid expensive iterative resubmission

**Exam-confirmed wrong answers**: switching a *blocking* pre-merge check to batch (unacceptable latency for a workflow someone is waiting on); a "timeout fallback to real-time" hybrid for both workflows (unnecessary complexity — just match each workflow to the right API).

## Task Statement 4.6 — Design multi-instance and multi-pass review architectures

**Self-review limitation**: a model that generated code **retains its own generation reasoning** in the same session, making it **less likely to question its own decisions** — self-review instructions or extended thinking don't fully overcome this.

**The fix**: an **independent review instance**, without the generator's prior reasoning context, catches subtle issues more reliably than asking the same session to review itself.

**Multi-pass review**: split a large review into **per-file local-analysis passes** plus a **separate cross-file integration pass** — this avoids attention dilution and the contradictory-findings problem described under Task Statement 1.6.

**Skill**: running verification passes where the model **self-reports a confidence score alongside each finding**, enabling calibrated routing of review attention (connects to Domain 5's human-review/confidence-calibration content).

---

## Quick self-check

- [ ] I know `tool_use` + JSON schema is the exam's actual answer for "reliable structured output" — not a separate constrained-decoding feature.
- [ ] I can explain why schema conformance doesn't guarantee semantic correctness, and name an example (line items not summing to total).
- [ ] I can design a schema with nullable/optional fields and an enum "other"+detail pattern to avoid fabricated values.
- [ ] I know when retries help (format/structural errors) vs. when they can't (information genuinely absent from source).
- [ ] I know the Message Batches API's exact tradeoffs: 50% savings, up to 24h, no SLA, no multi-turn tool calling, `custom_id` correlation.
- [ ] I can explain why an independent review instance beats self-review, and why per-file + integration passes beat one big pass.
- [ ] I know 2–4 few-shot examples is the target range for ambiguous-case handling, and why "be conservative" instructions don't work as well as explicit criteria.

Track these in the [progress tracker](tracker.html).
