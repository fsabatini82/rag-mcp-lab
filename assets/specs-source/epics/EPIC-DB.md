---
id: EPIC-DB
title: Database & Migrazioni — Project Tracker
status: in_progress
owner: data-team
---

# EPIC-DB — Database & Migrazioni

PostgreSQL 15. Migrazioni gestite con Alembic. Schema multi-tenant
(discriminato per `project_id`, no tenant_id separato in MVP).

## Stories
- US-301 — Schema tabella `tasks` con campi tipizzati
- US-302 — Indice composito su `tasks(project_id, status)`
- US-303 — FK con `ON DELETE CASCADE` da `tasks` a `projects`

## Linee guida (ADR-005)
- Migrazioni reversibili obbligatorie (`upgrade()` + `downgrade()`).
- Niente DDL inline negli endpoint — solo via Alembic.
- Indici su colonne usate in WHERE/ORDER BY ad alto volume. Documentare
  motivazione nel commento della migrazione, con riferimento al bug o
  alla storia che l'ha richiesto.
