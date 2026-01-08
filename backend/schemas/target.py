from pydantic import BaseModel
from typing import Optional


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None


class TargetResponse(TargetBase):
    id: int
    mission_id: int
    is_complete: bool

    class Config:
        from_attributes = True
