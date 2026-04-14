from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    code: str
    description: str | None = None
    status: str = "active"


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None


class ProjectOut(BaseModel):
    id: int
    name: str
    code: str
    description: str | None
    status: str
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
