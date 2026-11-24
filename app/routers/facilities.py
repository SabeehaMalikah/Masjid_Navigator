from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix= '/facilities',
    tags = ["Facilities"] # for fastapi docs
)

@router.get("/{google_places_id}", response_model=List[schemas.Facilities])
def get_facilities(google_places_id : str, db: Session = Depends(get_db)):
    facilities = db.query(models.Facilities).filter(models.Facilities.google_places_id == google_places_id).all()

    if not facilities:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"facilities for mosque with gpid {google_places_id} were not found")
    return facilities