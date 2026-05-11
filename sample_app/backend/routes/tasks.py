"""HTTP routes for the Task API.

Built on FastAPI. Mounts under `/api/v1/tasks`.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from sample_app.backend.common.sentinel import UNSET
from sample_app.backend.schemas.task_schema import CreateTaskRequest, TaskStatus
from sample_app.backend.services import task_service

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.post("", status_code=201)
def create_task(req: CreateTaskRequest) -> dict[str, Any]:
    """POST /api/v1/tasks — US-101. Response shape per ADR-002."""
    task = task_service.create_task(req)
    return {"data": task.model_dump(mode="json"), "error": None, "meta": None}


@router.get("")
def list_tasks(
    project_id: UUID = Query(...),
    status: TaskStatus | None = Query(default=None),
    # FIXME(US-102): the current binding cannot distinguish 'absent' from
    # 'explicitly null'. Demo 1 (with Mnemo) fixes this using the Sentinel
    # pattern from ADR-002 — see also BUG-502.
    assignee_id: str | None = Query(default=None),
    label: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
) -> dict[str, Any]:
    """GET /api/v1/tasks — US-102. TODO during Demo 1."""
    raise HTTPException(status_code=501, detail="Not implemented — Demo 1 target")
