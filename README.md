# Claude Certified Architect – Foundations (CCAR-F) — Prep Kit

This folder is your complete, self-contained study kit for the **Claude Certified Architect – Foundations** certification (exam code **CCAR-F**) from Anthropic's Partner Academy.

## ✅ Update: now built from the official Exam Guide (v1.0, effective July 2026)

The user obtained and provided the official **Claude Certified Architect – Foundations Exam Guide** PDF directly from Anthropic (exam code **CCAR-F**). Every file in this kit has been rewritten against it. Confidence is now uniformly high:

| Content type | Confidence | Why |
|---|---|---|
| **Exam logistics** (domains, weights, format, scoring, registration, retake/recert policy) | 🟢 **High — official** | Taken directly from the Exam Guide PDF, section by section. No more third-party estimates. |
| **Domain content** (the 5 domains' task statements, knowledge/skills tested) | 🟢 **High — official** | The domain files (`01`–`05`) are now organized around the guide's own numbered Task Statements (e.g., 1.1–1.7 for Domain 1), not a generic product-docs summary. |
| **Anti-patterns** (`06_anti_patterns.md`) | 🟢 Mostly official | Patterns marked ✅ are directly named in the guide's task statements or sample questions; a few marked 🔹 are reasonable extensions of its stated principles. |
| **Practice questions in `07_practice_exam.md`** | 🟢 Mixed, clearly labeled | Sections 1–5 are original questions (not real/leaked exam items), corrected to match the guide. **Section 6 is the guide's own 12 official sample questions**, reproduced verbatim with Anthropic's explanations. |

**Two corrections worth knowing about**, since earlier drafts of this kit got these wrong before the official guide was available:
- **Prompt-caching mechanics** (TTL, `cache_control` breakpoints, pricing) are explicitly **out of scope** for the exam — see the "Out-of-scope topics" list in `00_exam_overview.md`.
- There is **no separate "Structured Outputs" API feature** tested — the exam's actual model of reliable structured output is **`tool_use` with a JSON schema**, full stop.

**Item format correction**: some real exam items are **multiple-response** (select more than one correct answer — the item states how many to pick), not purely single-answer multiple-choice.

The guide is subject to change without notice per its own cover page — if you have a newer version, re-check `00_exam_overview.md` against it.

## 🌐 Prefer a website to markdown files? Open `index.html`

Double-click **`index.html`** in this folder (or right-click → Open with → your browser) for a proper study-guide website: sidebar navigation, styled tables and callouts instead of raw markdown, and an interactive 50-question practice exam where clicking an answer instantly shows right/wrong plus the explanation. It's a single self-contained file — works offline, no server needed.

Double-click **`tracker.html`** for the companion progress tracker: domain-mastery gauges, the six-week plan, and an exam-readiness checklist, all clickable. Both pages link to each other. Progress is saved locally in your browser (per-browser, not synced) — the markdown files remain the permanent, editable source of truth if you want to tweak content.

## Folder contents

| File | Purpose |
|---|---|
| `index.html` | 🌐 The study-guide website — open this first |
| `tracker.html` | 🌐 The interactive progress tracker |
| `00_exam_overview.md` | Exam format, cost, domains & weights, policies, registration |
| `01_domain1_agentic_architecture.md` | Domain 1 (27%): Agentic Architecture & Orchestration |
| `02_domain2_tool_design_mcp.md` | Domain 2 (18%): Tool Design & MCP Integration |
| `03_domain3_claude_code_config.md` | Domain 3 (20%): Claude Code Configuration & Workflows |
| `04_domain4_prompt_engineering_structured_output.md` | Domain 4 (20%): Prompt Engineering & Structured Output |
| `05_domain5_context_management_reliability.md` | Domain 5 (15%): Context Management & Reliability |
| `06_anti_patterns.md` | The recurring "wrong answer" architectural mistakes the exam tests for |
| `07_practice_exam.md` | 50 original practice questions + the 12 official sample questions from the Exam Guide, all with explanations |
| `glossary.md` | Quick-reference term definitions |
| `LEARNING_TRACKER.md` | Checkbox-based 6-week study plan — check items off as you go |

## How to use this kit

1. Open `index.html` (or start with `00_exam_overview.md` if you prefer plain markdown) so you know the shape of the test.
2. Work through domains **in weight order**: Domain 1 → 3/4 (tied) → 2 → 5. Heavier domains deserve more study hours.
3. After each domain, read the matching section of `06_anti_patterns.md` — most wrong-answer choices on scenario questions are one of these patterns.
4. Do `07_practice_exam.md` domain-by-domain as you finish each section, then do it cold as a full mock once you've covered everything.
5. Check off progress in `LEARNING_TRACKER.md` (or the web tracker) as you go.
6. Book the real exam once you're consistently scoring well above the passing bar on your own mock run.

## Recommended external resources (official, free)

All free, no partner access required, hosted on Anthropic Academy (`anthropic.skilljar.com`):

- Claude 101
- Claude Platform 101
- Building with the Claude API
- Introduction to Model Context Protocol
- Model Context Protocol: Advanced Topics
- Claude Code 101
- Claude Code in Action
- Introduction to Agent Skills
- Introduction to Subagents

These are folded into the weekly plan in `LEARNING_TRACKER.md`.
