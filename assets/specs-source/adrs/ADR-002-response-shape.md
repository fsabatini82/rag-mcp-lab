---
id: ADR-002
title: Response shape e gestione param "esplicitamente nullo"
status: accepted
date: 2025-06-14
---

# ADR-002 — Response shape uniforme e Sentinel per param nulli

## Decisione

1. **Response shape unificato** per tutti gli endpoint API:
   ```json
   {
     "data": <payload | null>,
     "error": { "code": "...", "message": "..." } | null,
     "meta": { ... } | null
   }
   ```
   Mai response "nude" (es. array direttamente).

2. **Distinzione param assente vs param nullo** nelle query string:
   - Parametro assente → nessun filtro applicato.
   - Parametro `=null` → filtro `IS NULL` applicato.
   - Usare un Sentinel value (`_UNSET = object()`) nei service layer per
     distinguere "non passato" da `None` durante la chiamata interna.

## Motivazione

Il punto 2 nasce da BUG-502 (filtri ignorati su `assignee_id=null`).
Senza Sentinel il caso "esplicitamente nullo" è indistinguibile dal caso
"non passato" lungo la catena di chiamate, e il filtro viene perso.

## Conseguenze

- Ogni nuovo endpoint deve seguire questo shape (linter + check in CI).
- I service layer non possono usare `Optional[T] = None` come default per
  param di filtro opzionali: serve un Sentinel esplicito.
