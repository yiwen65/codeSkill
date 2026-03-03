---
name: codeSkill
description: Structured Spec→Docs→Plan→implementation workflow for software projects. Use when users want interactive requirements interview, generation of PRD/DESIGN/PLAN docs, machine-readable PLAN.yaml, and resumable task-by-task implementation with tests and backlog/runlog state.
---

# codeSkill

Execute a deterministic, resumable workflow that converts requirements into docs and then into iterative implementation.

## Invocation and modes

- Use explicit invocation only (do not auto-invoke in normal chat).
- Accept optional argument: `init`, `resume`, `safe`, or `dev` (default `dev`).
  - `safe`: write/update docs and state only; do not edit product code.
  - `dev`: full loop including code edits, tests, and git commits.
- Newbie-first default behavior (unless user overrides):
  - Keep each turn low-cognitive-load: provide a short plan, execute, then summarize next action.
  - Ask questions only when truly blocking; otherwise choose sensible defaults and continue.
  - Prefer deterministic scripts in `scripts/` over ad-hoc manual steps.

## Project root

- Treat repository root (`codeSkill`) as the project root.
- Resolve all relative paths from repository root.

## Required outputs

Always ensure these files exist and are updated when relevant:

- `docs/INTERVIEW.md`
- `docs/PRD.md`
- `docs/DESIGN.md`
- `docs/PLAN.md`
- `docs/PLAN.yaml`
- `.agent_state/backlog.json`
- `.agent_state/runlog.md`
- `.agent_state/last_context.md`

Use templates from `assets/templates/` as the initial scaffold.

## Workflow state machine

### 1) Bootstrap

1. Detect repository status and stack.
2. Load existing docs/state if present.
3. Choose mode (`safe` or `dev`), default `dev`.
4. If `docs/PLAN.yaml` and `.agent_state/backlog.json` exist and user requested resume, jump to Execute Loop.
5. For beginner users, explicitly state defaults/assumptions before generating docs.

### 2) Interview

Ask only decision-critical questions; cap each round to concise bullets.

- Round 1: problem, users, platform, constraints, non-goals.
- Round 2: happy path, I/O, edge/error cases.
- Round 3: MVP acceptance and testing constraints.

Write distilled Q&A and decisions to `docs/INTERVIEW.md`.

### 3) Write Docs

Produce/update:

1. `docs/PRD.md`
2. `docs/DESIGN.md`
3. `docs/PLAN.md`
4. `docs/PLAN.yaml` with structured tasks

Every task in `PLAN.yaml` must include:

- `id`
- `title`
- `goal`
- `files_touched` (array, can be empty)
- `acceptance` (array, testable)
- `test_plan` (array of commands)
- `dependencies` (array, can be empty)
- `risk` (string, can be empty)

### 4) Gate / Approval

After creating or significantly changing PLAN, stop and request user confirmation before implementing code.

If confirmation is denied or pending, only refine docs and state.

### 5) Execute Loop

Convert plan to backlog using:

```bash
python3 .agents/skills/codeSkill/scripts/plan_to_backlog.py docs/PLAN.yaml .agent_state/backlog.json
```

Then iterate first actionable task (`todo` or `blocked` that is now unblocked):

1. Mark task `doing` in `.agent_state/backlog.json`.
2. Implement minimal change set for task scope.
3. Run task tests from `test_plan`; then run repository gates via `scripts/run_tests.sh` when available.
4. Retry fix+retest up to 3 cycles when failing.
5. Mark `done` or `blocked` with reason and concrete unblock options.
6. Append summary to `.agent_state/runlog.md`.
7. Write short resume note to `.agent_state/last_context.md`.

Prefer small commits per completed task.

### 6) Finish

When all tasks are done:

1. Summarize delivered scope vs plan.
2. List deferred items and risks.
3. Propose next iteration tasks.

## Quality and safety gates

- Load `references/QUALITY_GATES.md` before execution loop.
- If user asks to optimize workflow quality/autonomy, also load `references/BEST_PRACTICES.md`.
- Never run destructive actions without explicit user confirmation:
  - `rm -rf`, `git reset --hard`, dropping databases, production deploys.
- Never exfiltrate secrets or customer data.

## Bundled resources

- Templates: `assets/templates/`
- Questions: `references/QUESTION_BANK.md`
- Quality gates: `references/QUALITY_GATES.md`
- Best practices: `references/BEST_PRACTICES.md`
- Scripts:
  - `scripts/detect_stack.py`
  - `scripts/plan_to_backlog.py`
  - `scripts/run_tests.sh`
  - `scripts/update_progress.py`

## Determinism rules

- Keep tasks small and testable (prefer ≤1 hour execution chunks).
- Do not start code edits until PLAN approval is received.
- If key inputs are missing, ask at most 3 blocking questions at once.
- Default to automation: if a repeatable command exists, run it instead of describing it manually.
- If blocked after retries, provide: failure summary, minimal repro, and 1–3 concrete unblock options.
