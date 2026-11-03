from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import os
from . import models
from .database import engine
from .routers import mosque, review, facilities

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(mosque.router) # see requests in routers/mosque.py
app.include_router(review.router) # see requests in routers/review.py
app.include_router(facilities.router) # see requests in routers/facilities.py

@app.get("/")
def root():
    return {"message" : "Welcome to the Masjid Navigator API!"}


