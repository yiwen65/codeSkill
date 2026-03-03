# AI-Assisted Development Best Practices (Newbie-First)

## 1) Reduce decision load
- Prefer sensible defaults over repeated confirmation prompts.
- Ask only blocking questions; cap to 1–3 at a time.
- Show assumptions explicitly so users can correct quickly.

## 2) Keep work deterministic
- Convert natural-language plans into machine-readable tasks (`docs/PLAN.yaml`).
- Use scripts for repetitive operations (`scripts/*.sh`, `scripts/*.py`).
- Track task state in a resumable file (`.agent_state/backlog.json`).

## 3) Enforce quality gates every task
Run in order and stop on failures:
1. format
2. lint
3. type check
4. unit tests
5. smoke/integration tests

If a gate is unavailable, log skip reason and continue with remaining gates.

## 4) Keep iteration small and observable
- Prefer small, testable tasks with explicit acceptance criteria.
- For each task: implement → test → record runlog → update resume context.
- Keep commits focused (single task, single intent).

## 5) Safe autonomy
- Never run destructive commands without explicit confirmation.
- When blocked, provide: failing command, root-cause hypothesis, and 1–3 concrete fixes.

## 6) Newbie UX quality bar
- Always include:
  - what was changed,
  - what command validated it,
  - what to do next.
- Avoid jargon where possible; use concise explanations.
