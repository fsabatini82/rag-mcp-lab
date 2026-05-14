# Guida — Mnemo Lab

> Guida step-by-step per eseguire il lab da zero: dai prerequisiti
> all'esecuzione dei 4 use case in VS Code con GitHub Copilot.

---

## Sommario

1. [Prerequisiti](#1-prerequisiti)
2. [Installazione runtime e tool](#2-installazione-runtime-e-tool)
3. [Clone repo Mnemo + Lab](#3-clone-repo-mnemo--lab)
   - [Setup alternativo per macOS](#setup-alternativo-per-macos) — varianti dei §4–§7 per zsh / bash
4. [Installazione Mnemo](#4-installazione-mnemo)
5. [Configurazione delle sorgenti (specs + bugs)](#5-configurazione-delle-sorgenti-specs--bugs)
6. [Alimentazione del RAG](#6-alimentazione-del-rag)
   - [6.1 Modalità deterministica (default)](#61-modalità-deterministica-default)
   - [6.2 Modalità agentica via Copilot CLI (opt-in)](#62-modalità-agentica-via-copilot-cli-opt-in)
7. [Configurazione MCP in VS Code](#7-configurazione-mcp-in-vs-code)
8. [Strategia LLM: Plan + Execute](#8-strategia-llm-plan--execute)
9. [I 4 use case con prompt copia-incolla](#9-i-4-use-case)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisiti

| Item | Versione minima | Verifica |
| --- | --- | --- |
| OS | Windows 10/11, macOS 12+, Linux | — |
| RAM | 8 GB consigliati | — |
| Disco libero | ~600 MB | — |
| Internet | Solo per il primo install | — |
| Account GitHub | Con licenza GitHub Copilot attiva | [github.com/settings/copilot](https://github.com/settings/copilot) |

### Check rapido in PowerShell

```powershell
# Versione PowerShell (richiede 5.1+ o pwsh 7+)
$PSVersionTable.PSVersion
```

---

## 2. Installazione runtime e tool

### 2.1 Python 3.10+

```powershell
python --version
# Atteso: Python 3.10.x o superiore
```

Se manca o è troppo vecchio, scarica da [python.org/downloads](https://www.python.org/downloads/)
e durante l'install spunta **"Add python.exe to PATH"**.

```powershell
pip --version
# Atteso: pip 23.x+ (se manca, su Linux: sudo apt install python3-pip)
```

Soluzione
python -m pip install --upgrade pip

### 2.2 Git

```powershell
git --version
# Atteso: git version 2.40+ (qualunque 2.x recente va bene)
```

Se manca: [git-scm.com/download/win](https://git-scm.com/download/win).

### 2.3 VS Code

```powershell
code --version
# Atteso: 1.95+ (consigliato 1.97+ per pieno supporto MCP)
```

Se manca: [code.visualstudio.com](https://code.visualstudio.com/).

### 2.4 Estensioni VS Code richieste

Da VS Code → Extensions, installa:

- **GitHub Copilot** (`GitHub.copilot`)
- **GitHub Copilot Chat** (`GitHub.copilot-chat`)
- **Python** (`ms-python.python`) — utile per debug del sample_app
- **ESLint** + **Prettier** — opzionali per il frontend del sample_app

Da terminale equivalente:

```powershell
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension ms-python.python
```

Dopo l'install, in VS Code: apri Copilot Chat, fai sign-in al tuo account GitHub.

### 2.5 Verifica supporto MCP in GHCP

VS Code 1.97+ con GHCP Chat ha il supporto MCP nativo. Verifica aprendo
la palette comandi (Ctrl+Shift+P) e cercando **"MCP"** — devi vedere
voci come `MCP: List Servers`. Se non le vedi, aggiorna VS Code.

---

## 3. Clone repo Mnemo + Lab

Clona i due repo come sibling nella stessa cartella padre (es. `c:\dev\`):

```powershell
cd c:\dev
git clone https://github.com/fsabatini82/mnemo.git
git clone https://github.com/fsabatini82/rag-mcp-lab.git
```

Struttura risultante:

```text
c:\dev\
├── mnemo\                         # asset MCP riusabile
└── rag-mcp-lab\                   # materiali del lab
```

---

## Setup alternativo per macOS

> Mac è pienamente supportato (Intel x64 e Apple Silicon arm64). I §1–§3
> valgono identici (Python da python.org o `brew install python@3.12`,
> Git solitamente già presente, VS Code dal sito ufficiale). I §4–§7
> cambiano solo per la sintassi shell. I §8–§10 sono OS-agnostici e
> non hanno bisogno di adattamento.
>
> Assumo zsh (default su macOS 10.15+). Per bash i comandi sono identici
> tranne l'attivazione del venv.

### §4 Installazione Mnemo (macOS)

```bash
cd ~/dev/rag-mcp-lab                  # path dove hai clonato il repo del lab
python3 -m venv .venv
source .venv/bin/activate             # bash/zsh equivalente di Activate.ps1
pip install --upgrade pip             # opzionale ma riduce noise
pip install -e ../mnemo
which mnemo-server                    # deve puntare a ...../.venv/bin/mnemo-server
mnemo-ingest --help                   # subcommand: specs / bugs / all
```

### §5 Configurazione delle sorgenti (macOS)

Su Mac non c'è `setup-assets.ps1` (è PowerShell-only). Equivalente inline:

```bash
mkdir -p ~/mnemo-assets/specs ~/mnemo-assets/bugs
cp -R assets/specs-source/. ~/mnemo-assets/specs/
cp -R assets/bugs-source/.  ~/mnemo-assets/bugs/
echo "Done. Asset mirror at: $HOME/mnemo-assets"
```

Poi:

```bash
cp .env.example .env
```

Edita `.env` con `code .env` (o `nano`, `vim`) e imposta i due path al
mirror **con percorso assoluto** (pydantic-settings non espande `~` o
`$HOME`):

```env
MNEMO_SPECS_SOURCE_DIR=/Users/<tuo-username>/mnemo-assets/specs
MNEMO_BUGS_SOURCE_DIR=/Users/<tuo-username>/mnemo-assets/bugs
```

Per ottenere il path esatto già pronto da copiare:

```bash
echo "MNEMO_SPECS_SOURCE_DIR=$HOME/mnemo-assets/specs"
echo "MNEMO_BUGS_SOURCE_DIR=$HOME/mnemo-assets/bugs"
```

### §6 Alimentazione del RAG (macOS)

```bash
mnemo-ingest all
```

Tempo atteso ~30s la prima volta (download fastembed in
`~/.cache/fastembed/`, ~80MB), ~5–10s dalle successive.

Verifica:

```bash
ls -la data
```

Reset in caso di stato sqlite incoerente:

```bash
rm -rf data
mnemo-ingest all
```

### §7 Configurazione MCP in VS Code (macOS)

`.vscode/mcp.json` è OS-agnostico, **ma** su Mac il PATH che vede VS
Code non sempre include il venv. Due opzioni:

**Opzione A — Usa path assoluto (più robusto, consigliato):**

```json
{
  "servers": {
    "mnemo": {
      "type": "stdio",
      "command": "/Users/<tuo-user>/dev/rag-mcp-lab/.venv/bin/mnemo-server"
    }
  }
}
```

**Opzione B — Attiva il venv prima di lanciare VS Code:**

```bash
source .venv/bin/activate
code .
```

Per la prima volta usa l'Opzione A: non dipende dallo stato della shell.

Se `code` non è disponibile da terminale: in VS Code → `Cmd+Shift+P` →
`Shell Command: Install 'code' command in PATH`.

Smoke test in GHCP Chat (Agent mode), modello a scelta:

```
Usa il tool mnemo_info di Mnemo e mostrami la configurazione attiva.
```

### Differenze comandi: cheat-sheet

Quando incontri i §8–§10 (e i §4–§7 originali) usa questa mappatura:

| Windows / cmd / PowerShell | macOS / zsh / bash |
| --- | --- |
| `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| `Copy-Item src dst` / `copy src dst` | `cp src dst` |
| `Remove-Item -Recurse dir` / `rmdir /S /Q dir` | `rm -rf dir` |
| `where.exe mnemo-server` | `which mnemo-server` |
| `%USERPROFILE%\mnemo-assets` | `$HOME/mnemo-assets` o `~/mnemo-assets` |
| `notepad .env` | `code .env` (o `nano`, `vim`) |
| `.\scripts\setup-assets.ps1` | comandi inline §5 sopra |

### Specifico Apple Silicon (M1 / M2 / M3 / M4)

Tutto lo stack ha wheel native arm64 (`chromadb` ≥ 1.0, `fastembed`,
`tantivy` opzionale). Verifica che il tuo Python sia arm64:

```bash
python3 -c "import platform; print(platform.machine())"
# Atteso: arm64
```

Se stampa `x86_64` su Apple Silicon → Python Intel sotto Rosetta.
Reinstalla con `brew install python@3.12` (la formula Homebrew è
arm64 nativa) e ricrea il venv.

---

## 4. Installazione Mnemo

### 4.1 Virtual environment condiviso

```powershell
cd c:\dev\rag-mcp-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1      ### \
```

Verifica che il prompt mostri `(.venv)` all'inizio.

### 4.2 Install Mnemo in editable mode

```powershell
pip install -e ..\mnemo
```

Tempo atteso: **2–4 minuti** (scarica `chromadb`, `fastembed`,
`langchain-text-splitters`, `mcp`, ~250 MB di wheel).

### 4.3 Verifica installazione

```powershell
mnemo-server --help     # se non c'è --help, esce subito → installato OK
mnemo-ingest --help     # mostra i subcommand: specs, bugs, all
```

Se i comandi non sono trovati, riattiva il venv: `.\.venv\Scripts\Activate.ps1`.   ### .venv\Scripts\activate.bat   da cmd

---

## 5. Configurazione delle sorgenti (specs + bugs)

### 5.1 Estrazione asset al mirror esterno

```powershell
.\scripts\setup-assets.ps1
```

cd C:\Dev\demo-sdd-lab\rag-mcp-lab\live\rag-mcp-lab
powershell -ExecutionPolicy Bypass -File scripts\setup-assets.ps1

Lo script copia gli asset (mock di export ADO/Wiki) in:

- `%USERPROFILE%\mnemo-assets\specs\` (5 file Markdown)
- `%USERPROFILE%\mnemo-assets\bugs\`  (5 file JSON)

Output atteso:

```text
Mnemo asset setup
  Source (specs): c:\dev\session-6-rag-mcp-lab\assets\specs-source
  Source (bugs):  c:\dev\session-6-rag-mcp-lab\assets\bugs-source
  Target root:    C:\Users\<tu>\mnemo-assets
Done. Now point your .env at the mirror:
  MNEMO_SPECS_SOURCE_DIR=C:\Users\<tu>\mnemo-assets\specs
  MNEMO_BUGS_SOURCE_DIR=C:\Users\<tu>\mnemo-assets\bugs
```

Done. Now point your .env at the mirror:
  MNEMO_SPECS_SOURCE_DIR=C:\Users\fabio.sabatini\mnemo-assets\specs
  MNEMO_BUGS_SOURCE_DIR=C:\Users\fabio.sabatini\mnemo-assets\bugs

### 5.2 File .env

```powershell
Copy-Item .env.example .env         # copy .env.example .env   (da cmd)
```

Apri `.env` e verifica che i path puntino al mirror esterno (o lasciali
relativi, funziona comunque per il lab):

```env
MNEMO_STORE=chroma
MNEMO_PIPELINE=default
MNEMO_EMBED_MODEL=BAAI/bge-small-en-v1.5

MNEMO_PERSIST_DIR=./data
MNEMO_SPECS_COLLECTION=specs
MNEMO_BUGS_COLLECTION=bug_memory

MNEMO_SPECS_SOURCE_DIR=C:\Users\<tuo-user>\mnemo-assets\specs
MNEMO_BUGS_SOURCE_DIR=C:\Users\<tuo-user>\mnemo-assets\bugs

MNEMO_CHUNK_SIZE=512
MNEMO_CHUNK_OVERLAP=64
MNEMO_TOP_K=5
```

---

## 6. Alimentazione del RAG

Due modalità, scelte per invocazione: **deterministica** (default, sempre
disponibile) e **agentica via Copilot CLI** (opt-in, richiede prerequisiti
sotto). Stesso output finale, internals diversi — la seconda usa un LLM per
estrarre/normalizzare/classificare ogni item.

### 6.1 Modalità deterministica (default)

```powershell
mnemo-ingest all
```

Tempo atteso: **~30 secondi** alla prima esecuzione (scarica il modello
fastembed `BAAI/bge-small-en-v1.5`, ~80 MB). Dalle volte successive,
~5–10 secondi.

Output atteso:

```text
Ingesting 5 specs document(s)...
Done — specs collection refreshed.
Ingesting 5 bugs document(s)...
Done — bugs collection refreshed.
```

Verifica che la cartella `./data/` sia stata popolata:

```powershell
Get-ChildItem .\data
# Deve contenere chroma.sqlite3 + qualche cartella UUID
```

### 6.2 Modalità agentica via Copilot CLI (opt-in)

Invece di parsare i file in modo meccanico, due agent specializzati
(uno per le spec, uno per i bug) usano il LLM di GitHub Copilot via CLI
per: estrarre metadati strutturati, classificare ogni item come
*indexable* o *noise*, e arricchire i cross-reference. Output finale
identico (`Document[]` indicizzati nelle stesse collection), valore
aggiunto = qualità della classificazione.

#### Prerequisiti

1. **Subscription GitHub Copilot attiva** sul tuo account GitHub
   (Pro, Business, o Enterprise). Verifica:
   <https://github.com/settings/copilot>.

2. **GitHub CLI installato e autenticato.** Su Windows:

   ```powershell
   winget install --id GitHub.cli
   gh auth login                       # OAuth device flow, ~30s
   gh auth status                      # deve mostrare "Logged in to github.com"
   ```

   Su macOS:

   ```bash
   brew install gh
   gh auth login
   gh auth status
   ```

3. **Estensione Copilot CLI installata.** Due varianti supportate:

   **Variante A — `gh copilot` (estensione GitHub CLI, più diffusa):**

   ```powershell
   gh extension install github/gh-copilot
   gh copilot --version                 # smoke test
   ```

   **Variante B — `copilot` standalone (più recente, più adatto a uso
   headless agentic):** segui le istruzioni di installazione di
   <https://github.com/github/copilot-cli> (o equivalente per la
   tua organizzazione). Poi:

   ```bash
   copilot --version
   ```

4. **Token / auth disponibile in modalità headless.** L'auth OAuth di
   `gh` viene cachata localmente dopo il primo login interattivo; le
   esecuzioni successive (anche schedulate) la riusano in automatico.
   **Non c'è un'API key esplicita da settare in env** — Copilot usa il
   token OAuth caricato sotto `~/.config/gh/hosts.yml` (macOS/Linux) o
   `%APPDATA%\GitHub CLI\hosts.yml` (Windows).

   Se devi fare l'auth in CI/runner non-interattivo, usa `GH_TOKEN` (o
   `GITHUB_TOKEN`) come fallback con PAT che abbia gli scope di Copilot:

   ```powershell
   $env:GH_TOKEN = "<personal access token>"
   ```

#### Configurazione `.env` per il runner

Decommenta nel `.env` queste variabili (sono lette dal `CopilotRunner`):

```env
# Quale eseguibile invocare (default: "copilot" standalone)
MNEMO_COPILOT_BIN=copilot
MNEMO_COPILOT_ARGS=--no-stream
MNEMO_COPILOT_STDIN=1
MNEMO_COPILOT_TIMEOUT=180
```

**Se usi la Variante A (`gh copilot`)**, la config equivalente è:

```env
MNEMO_COPILOT_BIN=gh
MNEMO_COPILOT_ARGS=copilot suggest -t shell
MNEMO_COPILOT_STDIN=0
MNEMO_COPILOT_TIMEOUT=180
```

(Il sub-comando esatto di `gh copilot` può variare in base alla
versione dell'estensione — controlla con `gh copilot --help` qual è il
sub-comando che accetta un prompt in input.)

#### Esecuzione

Stesso `mnemo-ingest`, flag in più:

```powershell
mnemo-ingest specs --agentic copilot       # solo specs
mnemo-ingest bugs  --agentic copilot       # solo bugs
mnemo-ingest all   --agentic copilot       # entrambi
```

Tempo atteso: **~5–10 secondi per item** (round-trip LLM). Per il
corpus del lab (~10 file) → ~1-2 minuti totali. Per produzione con
centinaia di item, conviene schedulare di notte.

Output atteso (verbose):

```text
Using agentic ingestion: CopilotRunner(binary='copilot', ...)
Agent classified scratch.md as noise — skipping
Ingesting 7 specs document(s)...
Done — specs collection refreshed.
Agent classified BUG-typo.json as noise — skipping
Ingesting 4 bugs document(s)...
Done — bugs collection refreshed.
```

Nota le righe "classified ... as noise — skipping": è la classificazione
che il LLM fa per ogni item. Il loader deterministico ingurgita tutto;
l'agent filtra il rumore.

#### Verifica preliminare (raccomandata)

Prima del primo run reale, controlla che la CLI risponda:

```powershell
echo "Say hello in JSON: {\"msg\": \"hi\"}" | copilot --no-stream
```

Deve restituire qualcosa che contiene `{"msg": "hi"}` o simile. Se
ricevi errori di auth/quota/timeout, sistema prima questi prima di
invocare `mnemo-ingest --agentic`.

#### Schedulazione (Windows Task Scheduler)

```cmd
schtasks /Create /TN "Mnemo Ingest Agentic" /SC DAILY /ST 02:00 /TR ^
"cmd /c c:\dev\rag-mcp-lab\.venv\Scripts\activate.bat && mnemo-ingest all --agentic copilot"
```

Su macOS / Linux via cron:

```bash
crontab -e
# Aggiungi:
# 0 2 * * * cd ~/dev/rag-mcp-lab && source .venv/bin/activate && mnemo-ingest all --agentic copilot
```

#### Fallback in caso di problemi

Se l'invocazione agentica fallisce (CLI non installata, quota esaurita,
timeout di rete), `mnemo-ingest` mostra un messaggio chiaro ed esce
con codice ≠ 0 **senza toccare il RAG**. Riprova con la modalità
deterministica:

```powershell
mnemo-ingest all                          # senza --agentic, default
```

Il deterministico è 100% offline e privo di dipendenze esterne — è la
modalità da usare per il lab live se preferisci ridurre i rischi.

---

## 7. Configurazione MCP in VS Code

### 7.1 Verifica `.vscode/mcp.json`

Il file è già nel repo:

```json
{
  "servers": {
    "mnemo": {
      "type": "stdio",
      "command": "mnemo-server"
    }
  }
}
```

> Nota: `mnemo-server` deve essere risolvibile dal PATH. Con il venv
> attivato (`.\.venv\Scripts\Activate.ps1`) lo è. Se apri VS Code dal
> menu di Windows e il venv non è attivo, sostituisci `"command"` con il
> path assoluto: `c:\dev\session-6-rag-mcp-lab\.venv\Scripts\mnemo-server.exe`.

### 7.2 Apri VS Code dal venv attivo

```powershell
code .
```

VS Code rileva `.vscode/mcp.json` e ti chiede conferma per registrare
il server `mnemo`. Accetta.

### 7.3 Test che MCP risponde

In **GHCP Chat → Agent mode**:

```text
@mnemo /mnemo_info
```

Output atteso (estratto):

```json
{
  "store": "chroma",
  "pipeline": "default",
  "embed_model": "BAAI/bge-small-en-v1.5",
  "collections": { "specs": "specs", "bugs": "bug_memory" },
  ...
}
```

Se vedi questo, **MCP è collegato e funzionante**. Procedi.


## Smoke test prima dei demo
Apri Copilot Chat, modalità Agent, e prova:


@mnemo /mnemo_info
Risposta attesa: JSON con due collection (specs, bug_memory), store: chroma, source path. Se vedi questo, il giro è chiuso end-to-end (IDE → MCP → Mnemo → RAG → ritorno).

## Poi una query reale per validare il retrieval:

@mnemo cerca la spec US-102 e mostrami gli acceptance criteria principali
Copilot dovrebbe chiamare query_specs("US-102") o get_spec("US-102") e tornare con il contenuto della story.


## ULTIMO TEST:

Cerca con query_bugs il bug più rilevante che riguarda il kanban.
Poi, con get_bug, recupera il record completo del top hit e dimmi:
- bug_id
- root_cause
- files_touched
- l'ID della spec correlata (related_spec nel metadata)

Per ultimo, fai get_spec di quell'ID e dimmi solo titolo ed epic.

Niente codice, niente piani — solo retrieval + reporting.

---

## 8. Strategia LLM: Plan + Execute

GHCP supporta lo switch di modello per turno in Agent mode. Useremo
**due modelli diversi** per ottimizzare costo/qualità:

| Fase | Modello consigliato | Perché |
| --- | --- | --- |
| **Plan** | Claude Opus 4 (o 4.7) | Reasoning multi-step, gestione di chain di tool MCP, scelte architetturali |
| **Execute** | GPT 5.4 (o GPT-5) | Generazione codice ampia, edit multi-file, velocità |

### 8.1 Come cambiare modello in GHCP Chat

In fondo alla chat, accanto al bottone "Send", c'è un picker del modello.
Cliccaci sopra e seleziona quello desiderato. Lo switch è effettivo dal
turno successivo.

Se nella tua organizzazione GHCP non espone Opus o GPT-5.4, usa:

- **Plan**: `Claude Sonnet 4.6` (alternativa solida) o il top model disponibile
- **Execute**: `GPT-5 Mini` o `Claude Haiku 4.5`

### 8.2 Pattern di lavoro

Per ogni use case eseguiamo **due turni**:

1. **Turno Plan** (modello: Opus) — l'agent chiama i tool Mnemo, analizza
   il codice, propone un piano. **Non scrive ancora codice.**
2. **Turno Execute** (modello: GPT 5.4) — l'agent applica il piano,
   modifica i file, cita le fonti Mnemo nei commenti.

Tra i due turni, **review veloce del piano** — se ti convince, procedi;
altrimenti chiedi di rivederlo prima di passare a Execute.

---

## 9. I 4 use case

> Tutti i prompt sono **copia-incolla** ready. Modifica solo gli ID di
> story/bug se vuoi provarne altri.

### Use case 1 — Implementare US-102 (list tasks con filtri)

**Modello consigliato Plan**: Claude Opus 4

#### Prompt 1A — Plan

```text
Sto per implementare la user story US-102 nel sample_app. Prima di scrivere
codice, voglio che tu analizzi la situazione usando Mnemo.

Passi:
1. Usa il tool query_specs per recuperare la spec completa di US-102.
2. Identifica gli ADR correlati e usali via get_spec.
3. Usa query_bugs per cercare lezioni passate su "filter query parameter
   null assignee". Riferisci qualsiasi BUG- rilevante.
4. Apri ed esamina sample_app/backend/routes/tasks.py e
   sample_app/backend/services/task_service.py — capisci lo stato attuale.
5. Produci un piano di implementazione step-by-step, citando esplicitamente
   le fonti Mnemo (US-102, ADR-xxx, BUG-xxx) che giustificano ogni scelta.

NON scrivere codice ancora. Solo il piano, in markdown.
```

**Switcha modello a GPT 5.4 prima di proseguire.**

#### Prompt 1B — Execute

```text
Il piano va bene. Procedi con l'implementazione.

File da modificare:
- sample_app/backend/services/task_service.py — implementa list_tasks
  rispettando il pattern Sentinel UNSET (vedi ADR-002 e BUG-502).
- sample_app/backend/routes/tasks.py — rimuovi lo stub 501 e collega
  list_tasks; rispetta il response shape ADR-002.

Vincoli:
- Aggiungi commenti che citino le fonti Mnemo (ADR-002, BUG-502) ai
  punti chiave.
- Aggiungi anche i test di regressione per i 3 casi (param assente / null
  esplicito / valore concreto) in tests/backend/test_list_tasks_filters.py.
```

**Wow atteso**: il codice usa `_UNSET` correttamente, ha un commento
tipo `# Sentinel pattern — see ADR-002 / BUG-502` esattamente dove
serve.

---

### Use case 2 — Implementare US-302 (DB index)

**Modello consigliato Plan**: Claude Opus 4

#### Prompt 2A — Plan

```text
Devo implementare US-302 — aggiunta di un indice composito sulla tabella
tasks. Prima di scrivere la migrazione, ragiona usando Mnemo:

1. query_specs per recuperare US-302 con i suoi acceptance criteria.
2. query_bugs per cercare incident di performance correlati a /tasks o
   query lente — devi trovare almeno un BUG- pertinente.
3. get_spec sull'ADR correlato (probabilmente ADR-005) per le convenzioni
   di documentazione delle migrazioni.
4. Verifica il codice in sample_app/backend/db/migrations/versions/ —
   confermami che la baseline esiste e che US-302 non è ancora applicata.
5. Proponi un piano per la nuova migrazione, includendo:
   - Nome del file e revision id
   - Strategia (CONCURRENTLY, partial index, ecc.)
   - Cosa scriverai nel commento/docstring (deve spiegare il "perché",
     riferendosi a BUG-xxx e SLO).

NON scrivere codice. Solo piano.
```

**Switcha modello a GPT 5.4.**

#### Prompt 2B — Execute

```text
Procedi. Crea il file della migrazione in
sample_app/backend/db/migrations/versions/ seguendo il piano.

Requisiti chiave:
- CREATE INDEX CONCURRENTLY (no lock prolungato in prod)
- Indice parziale: WHERE archived_at IS NULL
- Migrazione reversibile (downgrade dropa l'indice)
- Docstring che cita BUG-504, descrive il SLO violato e il dataset, e il
  beneficio atteso (~50ms post-fix)
```

**Wow atteso**: la docstring della migrazione racconta la storia del
bug — chi la leggerà fra 2 anni capisce subito perché esiste l'indice.

---

### Use case 3 — Bug nuovo: kanban revert

**Modello consigliato Plan**: Claude Opus 4

#### Prompt 3A — Plan (diagnostica)

```text
Bug report (staging): "Trascino una card del kanban da una colonna all'altra
e a volte dopo 2-3 secondi torna alla colonna di partenza. Nessun errore
in console, nessun toast."

Usa Mnemo per capire se l'abbiamo già visto:

1. query_bugs con sintomo simile — cerca termini come "kanban revert drag
   drop status silent fail". Identifica il top hit.
2. get_bug sul bug più simile e mostrami symptom, root cause, fix_summary,
   files_touched.
3. get_spec sulla user story correlata e l'eventuale ADR.
4. Esamina sample_app/frontend/hooks/useTaskMutation.ts e
   sample_app/frontend/components/KanbanBoard.tsx — cerca pattern simili
   a quello del bug storico (in particolare: mutation senza onError /
   fire-and-forget).
5. Produci diagnosi e piano di fix che riproduca lo shape del fix storico.

NON modificare il codice ancora.
```

**Switcha modello a GPT 5.4.**

#### Prompt 3B — Execute (fix)

```text
Conferma diagnosi: applica il fix.

File da modificare:
- sample_app/frontend/hooks/useTaskMutation.ts — refactor di
  useQuickStatusChange affinché deleghi al hook canonico
  useTaskStatusMutation (no fire-and-forget, error handler con revert
  + toast).
- sample_app/frontend/components/KanbanBoard.tsx — verifica che
  onContextMenuMarkDone usi il pattern corretto.

Aggiungi un commento sopra useQuickStatusChange che riferisca BUG-503
("see BUG-503 — fire-and-forget was the original root cause").
```

**Wow atteso**: il fix replica esattamente lo shape del fix di BUG-503;
nessuna re-invenzione, solo applicazione di lessons del team.

---

### Use case 4 — Performance regression /tasks

**Modello consigliato Plan**: Claude Opus 4

#### Prompt 4A — Plan (root cause)

```text
Bug report (production monitor): "P99 di GET /api/v1/tasks è schizzato a
3.5s sul tenant ACME (~200k task). Locale era veloce."

Usa Mnemo per capire:

1. query_bugs su "slow tasks endpoint performance large tenant" — trova
   il bug storico.
2. get_bug sul match: leggi root cause, fix e files_touched.
3. Verifica nel codice attuale (sample_app/backend/db/migrations/versions/)
   se la migrazione del fix storico esiste già in questo branch.
4. Output diagnostico:
   - Se l'indice c'è: suggerisci cosa controllare (bloat, uso effettivo
     via pg_stat_user_indexes, parametri planner).
   - Se l'indice manca: proponi di rieseguire il fix di BUG-504 (cita la
     migrazione mancante).

NON modificare il codice.
```

**Switcha modello a GPT 5.4.**

#### Prompt 4B — Execute (fix se necessario)

```text
Se la diagnosi indica che la migrazione manca, generala ora seguendo lo
stesso template di Use case 2 (US-302), e cita BUG-504 nella docstring.

Se invece l'indice è presente, scrivi un breve report
sample_app/docs/perf-investigation-tasks.md con:
- Hypothesis (bloat, statistics, planner, parametri)
- Comandi diagnostici suggeriti (EXPLAIN ANALYZE, pg_stat_user_indexes,
  VACUUM ANALYZE)
- Riferimenti a BUG-504 come precedente storico
```

**Wow atteso**: l'agent **legge il filesystem** per capire la situazione
attuale prima di proporre un fix. Questo è agentic reasoning, non
retrieval cieco.

---

## 10. Troubleshooting

| Problema | Causa probabile | Soluzione |
| --- | --- | --- |
| `mnemo-server` non trovato | Venv non attivo o install fallito | `pip install -e ..\mnemo` con venv attivo |
| `@mnemo /mnemo_info` non risponde in Chat | Server non registrato | Riavvia VS Code; verifica `.vscode/mcp.json` |
| Ingestion lento la prima volta | Download modello fastembed | Aspetta ~80MB di download, è normale |
| Retrieval povero (hit sbagliati) | Query troppo astratta o `top_k` basso | Imposta `MNEMO_TOP_K=10` e riformula la query |
| Permission denied su `data/` | Path con caratteri speciali o spazi | Sposta `MNEMO_PERSIST_DIR` in un path semplice |
| VS Code non vede MCP | Versione < 1.97 | Aggiorna VS Code |
| Errore "fastembed" su Windows | Build tools mancanti per onnxruntime | `pip install --upgrade pip wheel` e riprova |
| GHCP non mostra il picker modello | Account senza piano Pro/Business | Solo Sonnet 4.5 / GPT-5 disponibili — usa quelli |

### Reset completo

```powershell
# Cancella RAG locale e ripopola da zero
Remove-Item -Recurse -Force .\data
mnemo-ingest all
```

### Verifica integrità

```powershell
# Smoke test della pipeline
python -c "from mnemo.factory import build_system; from mnemo.config import load_settings; s=build_system(load_settings()); print(s.specs.query('US-102').hits[0].text[:200])"
```

Se questo stampa testo coerente con la spec US-102, il sistema è
funzionante end-to-end.

---

## Riferimenti

- **Mnemo repo**: <https://github.com/fsabatini82/mnemo>
- **Lab repo**: questo
- **MCP spec**: <https://modelcontextprotocol.io>
- **GHCP MCP docs**: <https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp>
- **Anthropic MCP servers**: <https://github.com/modelcontextprotocol/servers>

Per i dettagli architetturali e i pattern adottati: [README.md](README.md).
Per la live: [docs/RUNBOOK.md](docs/RUNBOOK.md) e [docs/SPEAKER-NOTES.md](docs/SPEAKER-NOTES.md).
