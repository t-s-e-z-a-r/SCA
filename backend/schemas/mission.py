from pydantic import BaseModel, Field
from typing import Optional, List
from .target import TargetCreate, TargetResponse


class MissionBase(BaseModel):
    pass


class MissionCreate(BaseModel):
    cat_id: Optional[int] = None
    targets: List[TargetCreate] = Field(..., min_length=1, max_length=3)


class MissionUpdate(BaseModel):
    cat_id: Optional[int] = None


class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_complete: bool
    targets: List[TargetResponse]

    class Config:
        from_attributes = True


class MissionListResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_complete: bool

    class Config:
        from_attributes = True
