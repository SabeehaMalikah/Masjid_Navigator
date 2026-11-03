from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix= '/review',
    tags = ["Reviews"] # for fastapi docs
)

# get reviews for one mosque
@router.get("/{google_places_id}", response_model=List[schemas.Review])
def get_reviews(google_places_id : str, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.google_places_id == google_places_id).all()

    if not reviews:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"reviews for mosque with gpid {google_places_id} was not found")
    return reviews