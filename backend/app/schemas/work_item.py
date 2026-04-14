from datetime import date, datetime

from pydantic import BaseModel, Field


class WorkItemCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"
    priority: str = "medium"
    due_date: date | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    project_id: int
    assignee_id: int | None = None
    metadata_jsonb: dict = Field(default_factory=dict)


class WorkItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: date | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    assignee_id: int | None = None
    metadata_jsonb: dict | None = None


class WorkItemOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    due_date: date | None
    estimated_hours: float | None
    actual_hours: float | None
    project_id: int
    assignee_id: int | None
    reporter_id: int
    metadata_jsonb: dict
    is_deleted: bool
    created_at: datetime

    model_config = {"from_attributes": True}
