from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class WineryBase(BaseModel):
    name: str
    country: str
    region: Optional[str] = None


class WineryCreate(WineryBase):
    pass


class Winery(WineryBase):
    id: int

    class Config:
        from_attributes = True


class WineBase(BaseModel):
    name: str
    winery_id: int
    type: str = Field(description="red, white, rose, sparkling, dessert, or fortified")
    vintage: Optional[int] = None
    price: Optional[float] = None
    abv: Optional[float] = None
    description: Optional[str] = None


class WineCreate(WineBase):
    pass


class Wine(WineBase):
    id: int
    winery: Optional[Winery] = None

    class Config:
        from_attributes = True


class TastingNoteBase(BaseModel):
    wine_id: int
    rating: int = Field(ge=1, le=100)
    notes: Optional[str] = None
    tasted_on: date = date.today
    reviewer: Optional[str] = None


class TastingNoteCreate(TastingNoteBase):
    pass


class TastingNote(TastingNoteBase):
    id: int

    class Config:
        from_attributes = True
