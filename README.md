# Mnemo Lab — Sessione 6 (GHCP Advanced)

> Lab finale del corso **GHCP Advanced**. In 60 minuti vediamo come dare
> al coding agent dell'IDE una **memoria organizzativa** privata —
> specs di progetto e bug risolti — usando un server MCP e un RAG locale.
>
> Il lab è il **consumer**; il server MCP che usiamo è **[Mnemo](https://github.com/fsabatini82/mnemo)**, distribuito come asset riusabile in un repo separato.

---

## Cosa contiene questo repo

| Cartella | Contenuto |
| --- | --- |
| [`assets/specs-source/`](assets/specs-source/) | Mock di export Wiki — 3 epic, 4 user story, 1 ADR |
| [`assets/bugs-source/`](assets/bugs-source/) | Mock di export Azure DevOps Work Items — 5 bug risolti |
| [`sample_app/`](sample_app/) | Codice "in evoluzione" del Project Tracker (FastAPI + React) per i live edit |
| [`docs/RUNBOOK.md`](docs/RUNBOOK.md) | Cheat-sheet stampabile per la sessione live |
| [`scripts/setup-assets.ps1`](scripts/setup-assets.ps1) | Estrae gli asset al mirror esterno `%USERPROFILE%\mnemo-assets\` |
| [`scripts/generate_deck.py`](scripts/generate_deck.py) | Rigenera il deck dopo modifiche ai contenuti |
| [`.vscode/mcp.json`](.vscode/mcp.json) | Registra il server `mnemo` in VS Code (richiede mnemo installato) |
| [`.env.example`](.env.example) | Template di configurazione (vedi sotto) |

---

## Prerequisito: installare Mnemo

Questo lab dipende dal pacchetto Mnemo. Cloni i due repo come sibling e
installi Mnemo in editable:

```powershell
# Esempio di layout sul disco
git clone <mnemo-repo-url>            # → ./mnemo
git clone <lab-repo-url>              # → ./session-6-rag-mcp-lab

# Virtual env condiviso
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installa Mnemo (dal sibling)
cd mnemo
pip install -e .                      # oppure: pip install mnemo (da PyPI quando pubblicato)
cd ..
```

In alternativa, quando Mnemo sarà su PyPI:

```powershell
pip install mnemo
```

Dopo l'install, i comandi `mnemo-server` e `mnemo-ingest` sono nel PATH.

---

## Quick start del lab

```powershell
cd session-6-rag-mcp-lab

# 1. Estrai gli asset al mirror esterno (default: %USERPROFILE%\mnemo-assets)
.\scripts\setup-assets.ps1

# 2. Copia il template di config
Copy-Item .env.example .env
# (il .env punta già al mirror esterno generato sopra)

# 3. Popola le due collection di Mnemo dai mock
mnemo-ingest all

# 4. Apri VS Code — .vscode/mcp.json registra il server `mnemo` automaticamente
code .
```

Verifica in GHCP Chat (Agent mode): `@mnemo /mnemo_info` → deve restituire
2 collection popolate, store=chroma, sources puntate al mirror.

---

## Architettura del lab

```text
   ┌────────────────────────────────┐
   │  assets/specs-source/  (mock)  │ ─┐
   ├────────────────────────────────┤  │
   │  assets/bugs-source/   (mock)  │ ─┤
   └────────────────────────────────┘  │  read
                                       ▼
                            ┌────────────────────┐
                            │  mnemo-ingest      │   (esterno)
                            │  (pkg: mnemo)      │
                            └─────────┬──────────┘
                                      │ upsert
                                      ▼
                            ┌────────────────────┐
                            │   ./data/  (RAG)   │
                            │   specs · bugs     │
                            └─────────┬──────────┘
                                      │ MCP tools
                                      ▼
   ┌────────────────────────────────────────────────┐
   │  VS Code + GHCP Agent Mode                     │
   │  edita sample_app/ leggendo Mnemo via MCP      │
   └────────────────────────────────────────────────┘
```

- **Lab repo** (questo): asset, sample_app, materiali didattici, config.
- **Mnemo repo** (esterno): server MCP + CLI di ingestion.

---

## I 4 demo della sessione live

In sintesi (dettaglio completo in [docs/RUNBOOK.md](docs/RUNBOOK.md)):

| # | Tipo | Story / Bug | Cosa mostra |
| --- | --- | --- | --- |
| 1 | Implementazione | US-102 (list tasks con filtri) | GHCP scopre BUG-502 da solo e applica il pattern Sentinel |
| 2 | Implementazione | US-302 (DB index) | Codice che documenta la propria storia citando BUG-504 |
| 3 | Bug fix | Kanban revert (nuovo) | GHCP riconosce BUG-503 e propone il fix consolidato |
| 4 | Bug fix | Performance regression (nuovo) | Agentic reasoning: bug memory × stato del codice |

---

## Configurazione

Tutto via `.env` (prefix `MNEMO_`). Le variabili rilevanti per il lab:

```env
MNEMO_SPECS_SOURCE_DIR=%USERPROFILE%\mnemo-assets\specs
MNEMO_BUGS_SOURCE_DIR=%USERPROFILE%\mnemo-assets\bugs
MNEMO_TOP_K=5
```

Per la lista completa dei setting, vedi il [README di Mnemo](https://github.com/fsabatini82/mnemo).

---

## Materiali per il docente

- **Runbook**: [docs/RUNBOOK.md](docs/RUNBOOK.md) — pagina singola da stampare.
- **Speaker notes**: [docs/SPEAKER-NOTES.md](docs/SPEAKER-NOTES.md) — IT/EN per ogni slide, da copiare nelle note PowerPoint.
- **Deck**: [docs/Mnemo-Lab-Deck.pptx](docs/Mnemo-Lab-Deck.pptx) — 18 slide rigenerabili da [scripts/generate_deck.py](scripts/generate_deck.py).

Per modificare il deck dopo cambi di contenuto:

```powershell
pip install python-pptx
python scripts\generate_deck.py
```

---

## Licenza

MIT. Lab finale del corso GHCP Advanced. Usa [Mnemo](https://github.com/fsabatini82/mnemo) come asset MCP riusabile.
