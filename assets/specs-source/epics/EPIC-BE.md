---
id: EPIC-BE
title: Backend API — Project Tracker
status: in_progress
owner: backend-team
---

# EPIC-BE — Backend API

Service REST per la gestione di progetti, task, assegnazioni. Linguaggio
Python 3.11 + FastAPI + SQLAlchemy. Esposto su `/api/v1/...`. Auth via JWT
(out of scope per questa epica, gestita da gateway).

## Obiettivi
- CRUD task con regole di dominio (assegnatari, stati, transizioni)
- Notifiche outbound (webhook) sui cambi di stato
- Validazione cross-entità (assegnatario ∈ membri progetto)

## Stories
- US-101 — Creare un task
- US-102 — Listare task con filtri
- US-103 — Aggiornare lo stato di un task
- US-104 — Validare assegnatario
- US-105 — Webhook al cambio di stato

## Vincoli architetturali
- Tutte le response seguono lo schema `{ data, error, meta }` (ADR-002)
- Tutte le query con filtri opzionali devono distinguere "param assente"
  da "param esplicitamente nullo" (ADR-002)
- Errori 4xx con `error.code` machine-readable + `error.message` human-readable
