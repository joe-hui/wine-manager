import enum
from datetime import date

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship

from app.database import Base


class WineType(str, enum.Enum):
    RED = "red"
    WHITE = "white"
    ROSE = "rose"
    SPARKLING = "sparkling"
    DESSERT = "dessert"
    FORTIFIED = "fortified"


class Winery(Base):
    __tablename__ = "wineries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    country = Column(String, nullable=False)
    region = Column(String, nullable=True)

    wines = relationship("Wine", back_populates="winery", cascade="all, delete-orphan")


class Wine(Base):
    __tablename__ = "wines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    winery_id = Column(Integer, ForeignKey("wineries.id"), nullable=False)
    type = Column(Enum(WineType), nullable=False)
    vintage = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    abv = Column(Float, nullable=True)
    description = Column(Text, nullable=True)

    winery = relationship("Winery", back_populates="wines")
    tasting_notes = relationship("TastingNote", back_populates="wine", cascade="all, delete-orphan")


class TastingNote(Base):
    __tablename__ = "tasting_notes"

    id = Column(Integer, primary_key=True, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    tasted_on = Column(Date, default=date.today, nullable=False)
    reviewer = Column(String, nullable=True)

    wine = relationship("Wine", back_populates="tasting_notes")
