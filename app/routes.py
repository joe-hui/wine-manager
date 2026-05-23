from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Winery as WineryModel, Wine as WineModel, TastingNote as TastingNoteModel
from app.schemas import (
    TastingNote as TastingNoteSchema,
    TastingNoteCreate,
    Winery as WinerySchema,
    WineryCreate,
    Wine as WineSchema,
    WineCreate,
    WineSummary,
)

router = APIRouter(tags=["wineries"])
wine_router = APIRouter(tags=["wines"])
note_router = APIRouter(tags=["tasting-notes"])


# ═══════════════════════════════════════
# Wineries
# ═══════════════════════════════════════

@router.post("/wineries", response_model=WinerySchema, status_code=status.HTTP_201_CREATED)
def create_winery(winery: WineryCreate, db: Session = Depends(get_db)):
    existing = db.query(WineryModel).filter(WineryModel.name == winery.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Winery already exists")
    db_winery = WineryModel(**winery.model_dump())
    db.add(db_winery)
    db.commit()
    db.refresh(db_winery)
    return db_winery


@router.get("/wineries", response_model=List[WinerySchema])
def list_wineries(db: Session = Depends(get_db)):
    return db.query(WineryModel).all()


@router.get("/wineries/{winery_id}", response_model=WinerySchema)
def get_winery(winery_id: int, db: Session = Depends(get_db)):
    winery = db.query(WineryModel).filter(WineryModel.id == winery_id).first()
    if not winery:
        raise HTTPException(status_code=404, detail="Winery not found")
    return winery


@router.delete("/wineries/{winery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_winery(winery_id: int, db: Session = Depends(get_db)):
    winery = db.query(WineryModel).filter(WineryModel.id == winery_id).first()
    if not winery:
        raise HTTPException(status_code=404, detail="Winery not found")
    db.delete(winery)
    db.commit()
    return None


# ═══════════════════════════════════════
# Wines
# ═══════════════════════════════════════

@wine_router.post("/wines", response_model=WineSchema, status_code=status.HTTP_201_CREATED)
def create_wine(wine: WineCreate, db: Session = Depends(get_db)):
    winery = db.query(WineryModel).filter(WineryModel.id == wine.winery_id).first()
    if not winery:
        raise HTTPException(status_code=404, detail="Winery not found")
    db_wine = WineModel(**wine.model_dump())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine


@wine_router.get("/wines", response_model=List[WineSchema])
def list_wines(
    type: str = None,
    winery_id: int = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db),
):
    query = db.query(WineModel)
    if type:
        query = query.filter(WineModel.type == type)
    if winery_id:
        query = query.filter(WineModel.winery_id == winery_id)
    if min_price is not None:
        query = query.filter(WineModel.price >= min_price)
    if max_price is not None:
        query = query.filter(WineModel.price <= max_price)
    return query.all()


@wine_router.get("/wines/{wine_id}", response_model=WineSchema)
def get_wine(wine_id: int, db: Session = Depends(get_db)):
    wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine


@wine_router.delete("/wines/{wine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wine(wine_id: int, db: Session = Depends(get_db)):
    wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    db.delete(wine)
    db.commit()
    return None


# ═══════════════════════════════════════
# Tasting Notes
# ═══════════════════════════════════════

@note_router.post("/notes", response_model=TastingNoteSchema, status_code=status.HTTP_201_CREATED)
def create_note(note: TastingNoteCreate, db: Session = Depends(get_db)):
    wine = db.query(WineModel).filter(WineModel.id == note.wine_id).first()
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    db_note = TastingNoteModel(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@note_router.get("/notes", response_model=List[TastingNoteSchema])
def list_notes(wine_id: int = None, db: Session = Depends(get_db)):
    query = db.query(TastingNoteModel)
    if wine_id:
        query = query.filter(TastingNoteModel.wine_id == wine_id)
    return query.all()


@note_router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(TastingNoteModel).filter(TastingNoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Tasting note not found")
    db.delete(note)
    db.commit()
    return None
