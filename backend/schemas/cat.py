from pydantic import BaseModel, Field


class CatBase(BaseModel):
    name: str
    years_of_experience: int = Field(gt=0)
    breed: str
    salary: float = Field(gt=0)


class CatCreate(CatBase):
    pass


class CatUpdate(BaseModel):
    salary: float = Field(gt=0)


class CatResponse(CatBase):
    id: int

    class Config:
        from_attributes = True
