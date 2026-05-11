"""Task service layer.

US-101 (create) is implemented. US-102 (list with filters) is TODO and
is the target of Demo 1 — GHCP will fill `list_tasks` guided by Mnemo.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sample_app.backend.common.sentinel import UNSET, _UnsetType
from sample_app.backend.schemas.task_schema import CreateTaskRequest, TaskOut, TaskStatus

# In a real service this would be a repository / DB session. Kept in-memory
# for the lab so the focus stays on the agent + MCP interplay.
_DB: list[TaskOut] = []


def create_task(req: CreateTaskRequest) -> TaskOut:
    """US-101 — Create a task. Already implemented."""
    now = datetime.now(timezone.utc)
    task = TaskOut(
        id=uuid4(),
        project_id=req.project_id,
        title=req.title,
        description=req.description,
        status=TaskStatus.OPEN,
        assignee_id=req.assignee_id,
        created_at=now,
        updated_at=now,
    )
    _DB.append(task)
    return task


def list_tasks(
    project_id: UUID,
    *,
    status: TaskStatus | None | _UnsetType = UNSET,
    assignee_id: UUID | None | _UnsetType = UNSET,
    label: str | None | _UnsetType = UNSET,
    page: int = 1,
    page_size: int = 25,
) -> tuple[list[TaskOut], int]:
    """US-102 — List tasks with optional filters.

    TODO(US-102): implement filtering and pagination.

    Critical requirements (see Mnemo: query_specs("US-102") and BUG-502):
    - Distinguish 'param not supplied' (UNSET) from 'param explicitly null' (None).
    - When `assignee_id is UNSET` → no filter on assignee.
    - When `assignee_id is None` → return only unassigned tasks.
    - When `assignee_id` is a UUID → return only tasks for that assignee.
    - Order by updated_at DESC, id ASC.
    - Pagination: 1-based `page`, `page_size` in [1, 100].
    """
    raise NotImplementedError("TODO: implement during Demo 1 (US-102)")
