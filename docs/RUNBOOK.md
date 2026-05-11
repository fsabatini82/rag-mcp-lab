# Mnemo Lab — Runbook 60 min

> Cheat-sheet stampabile da tenere accanto durante la live. Una pagina A4.

## Setup (3 min, pre-live)

Prerequisito: il pacchetto **Mnemo** deve essere installato nel venv
(`pip install -e ../mnemo` se cloni come sibling, oppure `pip install mnemo`).

```powershell
.\scripts\setup-assets.ps1                # asset → %USERPROFILE%\mnemo-assets
.\.venv\Scripts\Activate.ps1
mnemo-ingest all                          # popola le due collection
code .                                    # VS Code carica .vscode/mcp.json
```

Verifica: in GHCP Chat (Agent) → `@mnemo /mnemo_info` → 2 collection, store=chroma.

---

## Demo 1 — Implementare US-102 (8 min)

**Prompt**: *"Implementa US-102. Usa la nostra memoria di progetto per allinearti a convenzioni e bug passati."*

| GHCP chiama | Recupera |
| --- | --- |
| `query_specs("US-102")` | Acceptance criteria, scenari BDD, riferimenti |
| `get_spec("ADR-002")` | Pattern Sentinel + response shape |
| `query_bugs("filter assignee null query parameter")` | BUG-502 (filtro perso su null) |

**Output GHCP**: endpoint `GET /api/v1/tasks` con response shape ADR-002, `_UNSET` sentinel nel service, test per 3 casi (assente/null/valore), commento che cita ADR-002 + BUG-502.

**WOW**: GHCP scopre da solo BUG-502 e applica il pattern. Senza Mnemo: BUG-602.

---

## Demo 2 — Implementare US-302 (7 min)

**Prompt**: *"Genera la migrazione Alembic per US-302. Commento SQL che spieghi il perché."*

| GHCP chiama | Recupera |
| --- | --- |
| `query_specs("US-302")` | AC indice composito parziale + CONCURRENTLY |
| `query_bugs("slow query tasks performance")` | BUG-504 con metriche (2.3s → 50ms) |
| `get_spec("ADR-005")` | Convenzione "commenta il perché" |

**Output GHCP**: migrazione Alembic con docstring che riferisce BUG-504, SLO e dataset.

**WOW**: il codice generato documenta la propria storia per il futuro maintainer.

---

## Demo 3 — Bug nuovo: kanban revert (8 min)

**Prompt**: *"Card del kanban tornano a colonna origine dopo qualche secondo, no errori. Cerca casi simili."*

| GHCP chiama | Recupera |
| --- | --- |
| `query_bugs("kanban card revert drag drop")` | BUG-503 (top hit) |
| `get_bug("BUG-503")` | Root cause, fix, files_touched, PR #312 |
| `get_spec("US-203")` | Cross-ref ADR-004 "no fire-and-forget" |

**Output GHCP**: "è BUG-503 ripetuto altrove. Probabilmente nuova mutation senza `onError`. Ispeziono `useTaskMutation.ts`." → apre file, trova mutation incriminata, propone patch.

**WOW**: bug riconosciuto via memoria del team, non via Google/Stack Overflow.

---

## Demo 4 — Performance regression /tasks (7 min)

**Prompt**: *"P99 di `/api/v1/tasks` schizzato a 3.5s su tenant da 200k task. Cosa abbiamo già visto?"*

| GHCP chiama | Recupera | Poi |
| --- | --- | --- |
| `query_bugs("slow tasks endpoint")` | BUG-504 | Legge `migrations/versions/` per verificare se l'indice esiste |

**Output GHCP**: due rami —

- **Indice esiste**: suggerisce EXPLAIN + `pg_stat_user_indexes`.
- **Indice assente**: genera la migrazione (stesso codice di Demo 2).

**WOW**: agentic reasoning = bug memory ⨯ stato attuale del codice.

---

## Backup tips

- **Se il MCP non si connette**: `mnemo-server` da terminale → vedi log stdio.
- **Se il retrieval è povero**: aumenta `MNEMO_TOP_K=10` nel `.env`.
- **Se serve resettare**: cancella `./data/` e ri-esegui `mnemo-ingest all`.
- **Se Chroma fallisce su Windows path con spazi**: sposta `MNEMO_PERSIST_DIR` in path senza spazi.

---

## Wrap-up (5 min)

1. **Pattern shown**: PEP 544 Protocols, Factory + lazy imports, multi-collection RAG, adapter pattern.
2. **In production**: cambia solo l'adapter (`specs_loader.iter_spec_files`, `bugs_loader.iter_bug_files`) → ADO Wiki, Confluence, Jira, GitHub Issues.
3. **Generalizzato a N domini**: incident DB, compliance, runbook, OnCall…
