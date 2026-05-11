"""Pydantic schemas for the Task API."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


class CreateTaskRequest(BaseModel):
    """Body for POST /api/v1/tasks (US-101)."""

    project_id: UUID
    title: str = Field(min_length=3, max_length=200)
    # description defaults to empty string — see BUG-501.
    description: str = Field(default="", max_length=5000)
    assignee_id: UUID | None = None


class TaskOut(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    description: str
    status: TaskStatus
    assignee_id: UUID | None
    created_at: datetime
    updated_at: datetime
