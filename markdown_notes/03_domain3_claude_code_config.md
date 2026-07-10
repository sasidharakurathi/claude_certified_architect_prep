# Domain 3: Claude Code Configuration & Workflows (20%)

> 🟢 Rewritten directly from the official Exam Guide's 6 task statements for this domain.

---

## Task Statement 3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

**Hierarchy (as the guide defines it)**:
- **User-level**: `~/.claude/CLAUDE.md` — applies only to that user; **not shared with teammates via version control**
- **Project-level**: `.claude/CLAUDE.md` or root `CLAUDE.md`
- **Directory-level**: subdirectory `CLAUDE.md` files

**Diagnostic skill tested**: a new team member not receiving expected instructions is a classic symptom of instructions having been placed at **user-level** instead of **project-level** — since user-level settings never propagate via version control to teammates.

**Modularity tools**:
- **`@import` syntax** — reference external files to keep CLAUDE.md modular (e.g., importing only the standards files relevant to a specific package, based on that package's maintainer's domain knowledge)
- **`.claude/rules/`** directory — an alternative to one monolithic CLAUDE.md; split into topic-specific files (`testing.md`, `api-conventions.md`, `deployment.md`)
- **`/memory`** command — verify which memory files are actually loaded in the current session; use this to diagnose inconsistent behavior across sessions/environments

## Task Statement 3.2 — Create and configure custom slash commands and skills

**Scoping**:
- Commands: **project-scoped** `.claude/commands/` (shared via version control, team-wide) vs. **user-scoped** `~/.claude/commands/` (personal)
- Skills: `.claude/skills/` with `SKILL.md` files supporting frontmatter: **`context: fork`**, **`allowed-tools`**, **`argument-hint`**

**`context: fork`**: runs the skill in an **isolated sub-agent context** — prevents verbose or exploratory skill output (e.g., full codebase analysis, brainstorming alternatives) from polluting the main conversation.

**`allowed-tools`** in skill frontmatter: restricts tool access **during that skill's execution** — e.g., limiting a skill to file-write operations only, to prevent it from taking destructive actions outside its intended scope.

**`argument-hint`**: prompts the developer for required parameters when they invoke a skill without arguments.

**Personal customization**: create a personal variant in `~/.claude/skills/` under a **different name** so it doesn't affect teammates who might share the project-scoped skill.

**Judgment call**: choose **skills** for on-demand, task-specific workflows; choose **CLAUDE.md** for always-loaded universal standards.

## Task Statement 3.3 — Apply path-specific rules for conditional convention loading

**Mechanism**: `.claude/rules/` files with **YAML frontmatter `paths:`** field containing glob patterns — the rule loads into context **only** when Claude is working with a matching file, reducing irrelevant context/token usage.

**Why this beats subdirectory CLAUDE.md files**: conventions that span **multiple directories by file type** (e.g., test files scattered throughout a codebase alongside the code they test, like `Button.test.tsx` next to `Button.tsx`) can't cleanly be captured by directory-bound CLAUDE.md files — a glob pattern like `**/*.test.tsx` in a rules file applies regardless of where the file lives.

Example: `paths: ["terraform/**/*"]` scopes a rule to only load for Terraform files, wherever they are in the tree.

**Exam-confirmed wrong answers for this scenario type**: consolidating everything into root CLAUDE.md under headers (relies on inference, unreliable); putting conventions into skills (requires manual invocation, doesn't guarantee automatic loading by file path); per-subdirectory CLAUDE.md files (can't handle conventions for files spread across many directories).

## Task Statement 3.4 — Determine when to use plan mode vs. direct execution

**Plan mode** is for: large-scale changes, multiple valid approaches, architectural decisions, multi-file modifications. It enables safe exploration and design **before** committing to changes, avoiding costly rework.

**Direct execution** is for: simple, well-scoped changes with a clear single approach (e.g., adding one validation check to one function, a single-file bug fix with a clear stack trace).

**The `Explore` subagent**: used to isolate **verbose discovery output**, returning summaries to the main conversation instead of flooding it — this prevents context-window exhaustion during multi-phase investigation tasks.

**Exam-confirmed wrong answers**: "start with direct execution, let the natural boundaries emerge" (risks costly rework when dependencies surface late); "use direct execution with exhaustive upfront instructions" (assumes you already know the right structure without having explored); "start in direct execution, switch to plan mode only if surprised" (ignores that the complexity was already known upfront from the task description, not something that might emerge later). Correct pattern: use plan mode for investigation/architecture, then direct execution to implement the agreed plan.

## Task Statement 3.5 — Apply iterative refinement techniques for progressive improvement

**Techniques tested**:
- **Concrete input/output examples** (2–3 of them) — the most effective way to communicate an expected transformation when prose descriptions get interpreted inconsistently
- **Test-driven iteration** — write the test suite first (covering expected behavior, edge cases, performance requirements), then iterate by sharing test failures to guide progressive improvement
- **The interview pattern** — have Claude ask clarifying questions to surface considerations you may not have anticipated (e.g., cache invalidation strategy, failure modes) *before* implementing in an unfamiliar domain
- **Batch vs. sequential fixes** — provide all issues in a **single** detailed message when they **interact** with each other; fix **sequentially** when issues are **independent**

## Task Statement 3.6 — Integrate Claude Code into CI/CD pipelines

**CLI flags to know precisely**:
- **`-p`** (or `--print`) — non-interactive mode; prevents the job from hanging waiting for interactive input. (Wrong answers seen on the exam: a nonexistent `CLAUDE_HEADLESS` env var, a nonexistent `--batch` flag, or a `< /dev/null` stdin redirect hack — none of these are the documented mechanism.)
- **`--output-format json`** combined with **`--json-schema`** — enforces machine-parseable structured output so findings can be posted automatically as inline PR comments.

**CLAUDE.md's CI role**: the mechanism for giving CI-invoked Claude Code project context — testing standards, fixture conventions, review criteria.

**Session isolation fact**: the **same session** that generated code is **less effective at reviewing its own changes** than an independent review instance — because it retains its own generation reasoning and is less likely to question its own decisions (this connects directly to Domain 4's Task Statement 4.6 on multi-instance review).

**Practical CI skills**:
- Including **prior review findings** in context when re-running a review after new commits, instructing Claude to report only **new or still-unaddressed** issues — avoids duplicate PR comments
- Providing existing test files in context so generated tests don't duplicate already-covered scenarios
- Documenting testing standards, valuable test criteria, and available fixtures in CLAUDE.md to raise generated-test quality and cut low-value output

---

## Quick self-check

- [ ] I can list the CLAUDE.md hierarchy (user/project/directory) and diagnose the "new teammate missing instructions" symptom.
- [ ] I know `context: fork`, `allowed-tools`, and `argument-hint` as skill frontmatter options and what each does.
- [ ] I know why `.claude/rules/` with glob-pattern `paths:` beats subdirectory CLAUDE.md for conventions spread across directories (e.g., test files).
- [ ] I can pick plan mode vs. direct execution for a described task, and explain the `Explore` subagent's role.
- [ ] I know when to batch multiple issues into one message vs. fix them sequentially.
- [ ] I know `-p`/`--print`, `--output-format json`, and `--json-schema` for CI, and why a fresh review instance beats self-review.

Track these in the [progress tracker](tracker.html).
