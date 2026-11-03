from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix= '/mosques',
    tags = ["Mosques"] # for fastapi docs
)

# get all mosques
@router.get("/", response_model=List[schemas.Mosque])
def get_mosques(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    mosques = db.query(models.Mosque).filter(models.Mosque.name.contains(search)).limit(limit).offset(skip).all()

    return mosques

# get one mosque
@router.get("/{google_places_id}", response_model=schemas.Mosque)
def get_mosque(google_places_id : str, db: Session = Depends(get_db)):
    mosque = db.query(models.Mosque).filter(models.Mosque.google_places_id == google_places_id).first()

    if not mosque:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"mosque with gpid {google_places_id} was not found")
    return mosque