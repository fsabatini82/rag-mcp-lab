---
id: EPIC-FE
title: Frontend SPA — Project Tracker
status: in_progress
owner: frontend-team
---

# EPIC-FE — Frontend SPA

Single-page app React + TypeScript. Consuma l'API descritta in EPIC-BE.
Stato UI gestito con TanStack Query (cache + invalidation).

## Stories
- US-201 — Vista Kanban del progetto
- US-202 — Filtri sui task (status, assignee, label)
- US-203 — Drag-and-drop fra colonne per cambio status
- US-204 — Toast di conferma e gestione errori utente-visibile

## Convenzioni
- Nessuna chiamata API in modalità fire-and-forget. Ogni mutazione che
  modifica UI ottimisticamente DEVE avere un `onError` con revert + toast
  (vedi ADR-004 + storia bug BUG-503).
- Form state e server state separati: form locale, server via TanStack Query.
- Componenti shareable in `src/frontend/components/`, viste in `src/frontend/views/`.
