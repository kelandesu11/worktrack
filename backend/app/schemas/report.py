from datetime import datetime

from pydantic import BaseModel


class DashboardSummaryRow(BaseModel):
    project_id: int
    project_name: str
    total_work_items: int
    open_work_items: int
    done_work_items: int
    high_priority_items: int


class StatusReportRow(BaseModel):
    status: str
    total: int


class ProjectLoadRow(BaseModel):
    project_name: str
    total_work_items: int


class RecentActivityRow(BaseModel):
    id: int
    event_type: str
    created_at: datetime
