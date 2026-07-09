# Exam Overview — Claude Certified Architect: Foundations (CCAR-F)

> 🟢 **High confidence** — this file is now built directly from the official **Exam Guide v1.0** (effective July 2026), which the user obtained and provided in full. Where earlier drafts of this kit guessed or relied on third-party blogs, those guesses are now replaced with the authoritative source. Exam code: **CCAR-F**. The guide states it is "subject to change without notice" — re-check before sitting if a lot of time has passed.

## What it validates

Per the official guide: the exam validates that a practitioner can **make informed decisions about tradeoffs when implementing real-world solutions with Claude**, tested across Claude Code, the Claude Agent SDK, the Claude API, and MCP. Questions are grounded in **realistic scenarios drawn from actual customer use cases**. Candidates must show practical judgment about architecture, configuration, and tradeoffs — not just definitions.

**Intended candidate**: a solution architect with **6+ months** of hands-on experience building with Claude APIs, the Agent SDK, Claude Code, and MCP, who understands both the capabilities and limitations of LLMs in production.

## Format — official, confirmed

| Attribute | Value |
|---|---|
| Exam code | **CCAR-F** |
| Number of items | 60 |
| Item format | **Multiple-choice AND multiple-response** — some items require selecting more than one answer; each item states how many responses to select |
| Exam structure | **4 scenarios presented, drawn at random from a bank of 6** (see below) |
| Time limit | 120 minutes |
| Delivery | Proctored — online proctored or Pearson VUE test center |
| Passing score | Scaled score of **720** on a 100–1,000 scale (criterion-referenced, not curved — set via a formal standard-setting study with subject-matter experts) |
| Exam fee | $125 USD (fee applies per attempt) |
| Validity period | 12 months from the date awarded |
| Result reporting | Pass/fail + scaled score + **percent-correct by domain** (domain breakdown is informational only, not used to determine pass/fail — only the total scaled score decides that) |

⚠️ **Correction from earlier drafts of this kit**: the item format is NOT pure single-answer multiple-choice — some items are **multiple-response** (select N of the options). Read each question's instruction carefully for how many to select.

## The 5 domains — confirmed exact weights

| # | Domain | Weight |
|---|---|---|
| 1 | Agentic Architecture & Orchestration | **27%** |
| 2 | Tool Design & MCP Integration | **18%** |
| 3 | Claude Code Configuration & Workflows | **20%** |
| 4 | Prompt Engineering & Structured Output | **20%** |
| 5 | Context Management & Reliability | **15%** |

## The 6 scenarios (4 are randomly presented each sitting) — confirmed exact wording

Each scenario frames a set of questions around a realistic production context, with an explicit list of "primary domains" it draws from:

1. **Customer Support Resolution Agent** — Claude Agent SDK agent handling high-ambiguity returns/billing/account issues via custom MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`); target 80%+ first-contact resolution.
   Primary domains: **1, 2, 5**
2. **Code Generation with Claude Code** — team uses Claude Code for generation/refactoring/debugging/docs; needs custom slash commands, CLAUDE.md, and plan-mode-vs-direct-execution judgment.
   Primary domains: **3, 5**
3. **Multi-Agent Research System** — coordinator delegates to search/document-analysis/synthesis/report-generation subagents; produces comprehensive cited reports.
   Primary domains: **1, 2, 5**
4. **Developer Productivity with Claude** — Agent SDK agent helps explore unfamiliar codebases/legacy systems using built-in tools (Read, Write, Bash, Grep, Glob) + MCP servers.
   Primary domains: **2, 3, 1**
5. **Claude Code for Continuous Integration** — Claude Code in CI/CD running automated code review, test generation, PR feedback; must minimize false positives.
   Primary domains: **3, 4**
6. **Structured Data Extraction** — extracting info from unstructured documents, validating with JSON schemas, handling edge cases, integrating downstream.
   Primary domains: **4, 5**

**Study tip**: since only 4 of 6 appear per sitting, you can't skip any — but you now know exactly which domains each scenario will pull questions from. Cross-reference this when studying: if you're weak on Domain 5, scenarios 1, 3, and 6 are where it'll bite you.

## Out-of-scope topics — confirmed, don't over-study these

The guide explicitly lists topics that will **not** appear on the exam. This matters because earlier drafts of this kit spent real effort on some of these (notably prompt caching mechanics and a separate "Structured Outputs" API feature) that turn out to be out of scope:

- Fine-tuning or training custom models
- Claude API authentication, billing, or account management
- Deep programming-language/framework implementation details (beyond tool/schema config)
- Deploying/hosting MCP servers (infra, networking, container orchestration)
- Claude's internal architecture, training process, or model weights
- Constitutional AI, RLHF, or safety training methodologies
- Embedding models or vector database implementation
- Computer use (browser/desktop automation) or vision/image analysis
- Streaming API implementation or server-sent events
- Rate limiting, quotas, or API pricing calculations
- OAuth, API key rotation, or auth protocol details
- Specific cloud provider configs (AWS/GCP/Azure)
- Performance benchmarking or model comparison metrics
- **Prompt caching implementation details (beyond knowing it exists)**
- Token counting algorithms or tokenization specifics

## Registration & scheduling — official process

Handled through **Anthropic Partner Academy + Pearson VUE**:
1. Review the certification page on Anthropic Partner Academy.
2. Download the Exam Guide, read the Certification Terms & Conditions and the Certification Exam Policy.
3. Register and complete checkout ($125, adjusted for partner-tier discounts if applicable).
4. Create a Pearson VUE account via the confirmation instructions, sign in to schedule.
5. Pick a date + online proctoring or a Pearson test center.
6. You can cancel/reschedule up to **24 hours before** your appointment penalty-free; inside 24 hours forfeits the fee.

## Retake policy — confirmed

If you don't pass: waiting periods **increase with each attempt** — 14 days after the 1st fail, 30 days after the 2nd, 90 days after the 3rd. Max **4 attempts per rolling 12-month period**, per exam (failing CCAR-F doesn't block registering for a different Anthropic exam). The $125 fee applies **every attempt**.

## Recertification

The credential lasts 12 months. To renew **on time**: review what changed and complete a **free, non-proctored** renewal assessment on Partner Academy. If it lapses, you must retake the full proctored exam at full fee. If Anthropic decides content changed significantly, they may require a full retake instead of the lighter renewal path even for on-time renewals.

## Exam-day conduct (know this before you sit down)

- Valid, unexpired **government-issued photo ID**, name must exactly match your registration (fix mismatches via `certifications-support@anthropic.com` *before* scheduling).
- Online: stay on webcam for the entire session, clear workspace (no notes/phones/second monitor), no talking to anyone, no recording/reproducing exam content.
- You'll accept an **NDA** before starting — declining ends the session with no refund.
- Misconduct → result invalidated, credential revoked, banned from future exams.
- Appeals: within **14 days** of notification (or of your exam date, for a result concern) via Pearson VUE support. Standard-setting outcomes and individual item content are **not** appealable.

## Prerequisites & required reading

No formal prerequisite course is enforced, but read before sitting: the **Exam Guide** itself (now fully incorporated into this kit), the **Certification Terms and Conditions**, and the **Anthropic Certification Exam Policy**.

## Recommended free official courses (still a good idea, not exam-mandated)

All hosted on `anthropic.skilljar.com`, free, no partner login needed — useful for hands-on practice even though the exam guide's own "How to Prepare" section (see `01`–`05` domain files) is now the primary syllabus:

1. Claude 101, Claude Platform 101
2. Building with the Claude API
3. Introduction to Model Context Protocol / Advanced Topics
4. Claude Code 101, Claude Code in Action
5. Introduction to Agent Skills, Introduction to Subagents
