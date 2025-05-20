# backend/app/schemas.py

from pydantic import BaseModel

class FunctionBase(BaseModel):
    name: str
    route: str
    language: str
    timeout: float = 5.0

class FunctionCreate(FunctionBase):
    pass

class FunctionOut(FunctionBase):
    id: int

    class Config:
        orm_mode = True
