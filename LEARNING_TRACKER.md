# Learning Tracker — Claude Certified Architect: Foundations (CCAR-F)

> 🟢 Updated against the official Exam Guide. A few hands-on items below (prompt caching, "Structured Outputs") have been swapped for guide-confirmed exercises instead.
>
> Every "hands-on" item below has a matching free resource link and expanded step-by-step version in **`08_resources_and_practicals.md`** (or the Resources page in `index.html`) — open that alongside this tracker.

Check items off by changing `[ ]` to `[x]` as you complete them. Most markdown editors (VS Code, Obsidian, Typora) render these as clickable checkboxes.

**My start date:** _______________ **My target exam date:** _______________

---

## At-a-glance progress

- [ ] Domain 1 — Agentic Architecture & Orchestration (27%) studied
- [ ] Domain 2 — Tool Design & MCP Integration (18%) studied
- [ ] Domain 3 — Claude Code Configuration & Workflows (20%) studied
- [ ] Domain 4 — Prompt Engineering & Structured Output (20%) studied
- [ ] Domain 5 — Context Management & Reliability (15%) studied
- [ ] Anti-patterns doc read and internalized
- [ ] Practice exam attempted once per domain (as I finish each)
- [ ] Full 50-question mock exam completed cold, scoring ≥ 36/50 (72%)
- [ ] Full 50-question mock exam re-attempted, scoring ≥ 45/50 (90%)
- [ ] All 12 official sample questions (Section 6) attempted and understood
- [x] **Official Exam Guide PDF reviewed** ✅ — obtained and fully incorporated into this kit
- [ ] Certification Terms & Conditions PDF reviewed
- [ ] Anthropic Certification Exam Policy PDF reviewed
- [ ] Exam scheduled via Pearson VUE
- [ ] **Exam passed** 🎉

---

## Week 1 — Foundations + Claude API core concepts

**Goal:** baseline product literacy + how the API actually works under the hood.

- [ ] Take **Claude 101** (anthropic.skilljar.com)
- [ ] Take **Claude Platform 101**
- [ ] Start **Building with the Claude API** (flagship course — budget 8+ hrs total; this week just get through streaming, auth, and basic requests)
- [ ] Read `00_exam_overview.md` in this kit fully
- [ ] Read `04_domain4_prompt_engineering_structured_output.md` Task Statements 4.1–4.2 (precision criteria + few-shot) — pairs naturally with the API course
- [ ] Set up a real API key and run at least 3 hands-on API calls yourself (a basic message, a `tool_use` call, a streaming call)

## Week 2 — Claude Code hands-on

**Goal:** live in Claude Code daily; make Domain 3 muscle memory, not theory.

- [ ] Take **Claude Code 101**
- [ ] Take **Claude Code in Action**
- [ ] Take **Introduction to Agent Skills**
- [ ] Take **Introduction to Subagents**
- [ ] Read `03_domain3_claude_code_config.md` fully
- [ ] In a real (or scratch) repo: write your own CLAUDE.md, add a `.claude/rules/` file with `paths:` frontmatter, create one custom Skill using `context: fork`, `allowed-tools`, and `argument-hint`
- [ ] Configure at least one hook (e.g., a tool-call interception hook blocking a specific Bash pattern) and verify it actually blocks the action
- [ ] Run Claude Code once with `-p` (non-interactive mode) piping in real input, and once more with `--output-format json --json-schema`

## Week 3 — Model Context Protocol & tool design

**Goal:** understand MCP mechanics well enough to answer protocol-level questions, not just "MCP connects tools."

- [ ] Take **Introduction to Model Context Protocol** (build a server + client from scratch in Python)
- [ ] Take **Model Context Protocol: Advanced Topics**
- [ ] Read `02_domain2_tool_design_mcp.md` fully
- [ ] Build one toy MCP server exposing at least one tool, one resource, and one prompt
- [ ] Configure it in project-scoped `.mcp.json` with an env-var-expanded credential, and separately in user-scoped `~/.claude.json`
- [ ] Write one structured tool error response by hand (`isError`/`isRetryable`/`errorCategory`) and trace how it would change agent behavior vs. an empty result
- [ ] Do practice questions Q15–23 in `07_practice_exam.md`; review any misses against `06_anti_patterns.md`

## Week 4 — Prompt engineering & structured output deep dive

**Goal:** go from "knows the techniques" to "can pick the right one under a constraint."

- [ ] Re-read `04_domain4_prompt_engineering_structured_output.md` fully (you started it Week 1 — now finish it end to end)
- [ ] Hands-on: write 2–4 few-shot examples for an ambiguous extraction/classification scenario, showing the reasoning for the chosen answer
- [ ] Hands-on: implement a `tool_use` + JSON-schema extraction with nullable/optional fields and an `"other"` + detail enum pattern
- [ ] Hands-on: implement a validation/retry loop that feeds a real validation error back to Claude, and add a `detected_pattern` field to track false-positive patterns
- [ ] Do practice questions Q34–43; review any misses

## Week 5 — Multi-agent systems & context management

**Goal:** the two biggest-weight areas (Domain 1 = 27%, plus Domain 5) — don't shortchange this week.

- [ ] Read `01_domain1_agentic_architecture.md` fully
- [ ] Read `05_domain5_context_management_reliability.md` fully
- [ ] Hands-on: build a hub-and-spoke system — one coordinator (with `"Task"` in `allowedTools`), two subagents with distinct scoped tool lists, spawned in parallel via multiple `Task` calls in one response
- [ ] Hands-on: simulate a subagent timeout and verify the coordinator receives structured error context (failure type, attempted query, partial results) rather than a suppressed/empty result
- [ ] Hands-on: have an agent maintain a scratchpad file during a long exploration task and reference it on a later question
- [ ] Do practice questions Q1–14 and Q44–50; review any misses

## Week 6 — Anti-patterns, mock exams, and gap closing

**Goal:** convert domain knowledge into exam-taking speed and accuracy.

- [ ] Read `06_anti_patterns.md` fully — all 18 patterns
- [ ] Do the full 50-question mock in `07_practice_exam.md` cold, timed (aim ≤ 100 minutes to leave buffer vs. the real 120)
- [ ] Do all 12 official sample questions (Section 6) cold
- [ ] Score it; for any domain with >2 misses, re-read that domain file same day
- [ ] Re-take the mock 48+ hours later; target ≥ 90%
- [ ] Read the **Certification Terms & Conditions PDF** and **Anthropic Certification Exam Policy PDF** (the Exam Guide itself is already fully incorporated into this kit)
- [ ] Book the proctored exam via Pearson VUE
- [ ] Day before exam: skim `06_anti_patterns.md` + `glossary.md` only — no new material
- [ ] Confirm your government-issued photo ID name **exactly matches** your registration
- [ ] **Sit the exam**

---

## The Exam Guide's own 4 preparation exercises

Straight from the official guide's "Preparation Exercises" section — hands-on, cross-domain, and worth doing verbatim if you have the time:

- [ ] **Exercise 1 — Multi-Tool Agent with Escalation Logic**: define 3–4 MCP tools (two deliberately similar, to test description quality); implement an agentic loop keyed on `stop_reason`; add structured errors (`errorCategory`, `isRetryable`); add a tool-call-interception hook enforcing a threshold rule; test with a multi-concern message. *(Domains 1, 2, 5)*
- [ ] **Exercise 2 — Claude Code for a Team Workflow**: project-level CLAUDE.md; `.claude/rules/` with glob-scoped conventions; a skill with `context: fork` + `allowed-tools`; an MCP server in `.mcp.json` plus a personal one in `~/.claude.json`; compare plan mode vs. direct execution across a single-file fix, a multi-file migration, and a multi-approach feature. *(Domains 3, 2)*
- [ ] **Exercise 3 — Structured Data Extraction Pipeline**: a JSON schema with required/optional/nullable fields and an enum "other"+detail pattern; a validation-retry loop; few-shot examples across varied document formats; a 100-document Message Batches API run with `custom_id`-based failure resubmission; a confidence-based human-review router. *(Domains 4, 5)*
- [ ] **Exercise 4 — Multi-Agent Research Pipeline**: a coordinator delegating to ≥2 subagents via parallel `Task` calls; structured findings separating content from metadata (claim/excerpt/source/date); a simulated subagent timeout propagating structured error context; a test with conflicting source statistics verifying both are preserved with attribution rather than one being silently picked. *(Domains 1, 2, 5)*

---

## Post-exam (optional)

- [ ] Note anything that surprised you vs. this kit (for your own future reference, or to help others)
- [ ] Consider the follow-on **Claude Certified Architect – Professional** track once Foundations is passed
- [ ] Set a reminder ~11 months out to complete the free on-time renewal assessment before the 12-month credential expires
