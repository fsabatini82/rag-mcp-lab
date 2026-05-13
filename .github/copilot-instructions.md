# Project Instructions — Mnemo-Aware Coding

This workspace is equipped with **Mnemo**, a local MCP server exposing
two collections of private organizational knowledge:

- **`specs`** — user stories, ADRs, epics, BDD scenarios
  (tools: `query_specs`, `get_spec`)
- **`bug_memory`** — resolved bugs with root cause + fix + files touched
  (tools: `query_bugs`, `get_bug`)

Plus `mnemo_info()` for diagnostics.

Treat Mnemo as the **source of truth** for project conventions and
historical lessons. The Internet doesn't know our specs or our bugs;
Mnemo does.

## Core mandate

**Consult Mnemo before writing code.** When the user asks you to:

- implement a user story, feature, or endpoint
- modify a sensitive area (data layer, auth, error handling, UI mutations)
- fix a bug or investigate an incident
- refactor anything touching public API contracts

your first action is **not** to open files — it's to query Mnemo.

The minimum useful chain:

1. `query_specs("<topic or story ID>")` — surface acceptance criteria, conventions
2. `query_bugs("<area or symptom keywords>")` — surface lessons from past incidents
3. Follow up with `get_spec` / `get_bug` on any cross-reference

Only then read the local code. Reading code first and Mnemo second is
a defect: you might re-invent a pattern Mnemo already has cataloged.

## Two operating modes

### Mode A — Implementing a feature ("implement US-xxx")

1. **Plan first, code second.** Produce a structured plan in markdown:

   ```
   ## Plan for <STORY-ID>
   - Spec hits: [<id>: <one-line summary>]
   - ADR hits: [<id>: <constraint that applies>]
   - Bug hits (defensive): [<id>: <pitfall to avoid in this area>]
   - Files to modify: [<path>: <what changes>]
   - Tests to add: [<path>: <case>]
   ```

2. Wait for the user's confirmation.
3. Apply the plan with minimal scope. Every change influenced by a
   Mnemo hit gets a code comment citing the ID:

   ```python
   # Sentinel pattern — see ADR-002 (response shape) and BUG-502 (filter bypass).
   ```

### Mode B — Investigating a bug or regression ("I see this error / P99 spike")

1. **Triage first, fix second.** Produce a triage report:

   ```
   ## Triage: <one-line problem summary>
   - Closest past pattern: <BUG-id> (score: high|medium|low)
   - Same root cause? yes | partial | no — <reasoning>
   - Where the pattern lives now: [<path>: <suspect symbol>]
   - Proposed fix shape: <reuse historical | adapt | fresh diagnosis>
   ```

2. Wait for confirmation.
3. **Bug memory × current code**: for perf / regression issues, before
   proposing a fix, check whether the historical fix's artifacts
   (migration, hook, middleware) still exist on this branch. If they
   do, the answer isn't "re-apply" — it's "investigate why the fix
   isn't effective anymore". If they don't, generate the consolidated
   fix from the past bug.

## Citation rule

When generating code influenced by a Mnemo entry, **cite the exact ID**
in a comment. Do not paraphrase or copy the spec/bug text verbatim;
the ID lets the reader call `get_spec(...)` / `get_bug(...)` for the
full source.

Examples that follow the rule:

```python
"""Add composite index on tasks(project_id, status).

Why: BUG-504 — P99 regressed to 2.3s on tenants > 100k rows
(Seq Scan in EXPLAIN). Fix verified at ~50ms post-index.
See ADR-005 for migration conventions.
"""
```

```ts
// Mirror of the fix in BUG-503 (PR #312): no fire-and-forget mutation.
// onError reverts optimistic UI + shows retry toast.
```

## Hard rules

- **Don't invent IDs.** If you reference `BUG-XYZ` or `US-XYZ`, that ID
  must have come from an actual Mnemo response in this conversation.
- **Don't ask the user about project conventions** — query Mnemo
  first. Ask only when Mnemo returns nothing relevant; say so
  explicitly: "Mnemo has no prior context on this — proceed with
  general best practices, or pause to add a spec?"
- **Don't skip the Plan / Triage phase** unless the change is < 10
  lines and purely mechanical (rename, format, no logic).
- **Don't swallow Mnemo errors silently.** If a tool call fails,
  surface it with `mnemo_info()` output and a suggested next step.

## Style

- Plans and triage reports are bullet lists, not essays.
- Code comments referencing Mnemo IDs are short and inline at the
  relevant line, not piled at the top of the file.
- File paths use repo-relative form.
- Prefer pre-fix diagnostics (EXPLAIN, grep, log inspection) over
  speculative edits.
