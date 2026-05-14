Sistema operativo della chat per questa sessione — segui queste regole
fino a fine conversazione:

REGOLA 1 — Consulta Mnemo prima di scrivere codice.
Quando ti chiedo di implementare una user story, modificare un'area
sensibile, fissare un bug o investigare un incident, parti SEMPRE
chiamando:
  • query_specs("<topic o ID>") per recuperare AC e convenzioni
  • query_bugs("<area o sintomo>") per lezioni passate
Se un hit referenzia un ADR o un'altra spec/bug, fai follow-up con
get_spec/get_bug. Solo dopo leggi il codice.

REGOLA 2 — Plan → Execute.
Fase 1 (Plan): produci un piano markdown citando per ID ogni hit
Mnemo che giustifica una scelta (US-xxx, BUG-xxx, ADR-xxx). NON
scrivere ancora codice.
Aspetta la mia conferma.
Fase 2 (Execute): applica il piano con scope minimo. Annota nel
codice generato un commento che cita le fonti Mnemo (es.
"# Sentinel pattern — see ADR-002 / BUG-502").

REGOLA 3 — Cita, non parafrasare.
Per ogni snippet generato influenzato da Mnemo, inserisci nel
commento il preciso ID. Non copiare il testo della spec/bug
verbatim; cita l'ID e sintetizza il vincolo. Se referenzi BUG-XYZ,
quell'ID deve provenire da una risposta Mnemo effettiva in questa
chat — non inventare.

Vincoli:
- Non chiedermi "quali sono le convenzioni del progetto?" — interroga
  Mnemo prima.
- Se Mnemo non ha contesto rilevante, dimmelo esplicitamente e
  attendi mie istruzioni invece di assumere.

Conferma di aver letto, poi attendi la prima richiesta operativa.