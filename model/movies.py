from pydantic import BaseModel, Field
from typing import Optional


class Movies(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1800, le=2100)
    gender: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True


