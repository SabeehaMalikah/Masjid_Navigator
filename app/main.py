from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
import os
from . import models
from .database import engine
from .routers import mosque, review, facilities

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://127.0.0.1:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


app.include_router(mosque.router) # see requests in routers/mosque.py
app.include_router(review.router) # see requests in routers/review.py
app.include_router(facilities.router) # see requests in routers/facilities.py

@app.get("/")
def root():
    return {"message" : "Welcome to the Masjid Navigator API!"}


