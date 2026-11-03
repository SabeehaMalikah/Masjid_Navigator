from .database import Base
from sqlalchemy import Column, BigInteger, FLOAT, VARCHAR, JSON, TEXT, TIMESTAMP, Boolean, ForeignKey

class Mosque(Base):
    __tablename__ = 'mosque'

    id = Column(BigInteger, primary_key=True, nullable=False)
    google_places_id = Column(VARCHAR(50))
    name = Column(VARCHAR(250))
    address = Column(VARCHAR(250))
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    rating = Column(FLOAT)
    reviews = Column(JSON)

class Review(Base):
    __tablename__ = 'review'

    id  = Column(BigInteger, primary_key=True)
    google_places_id = Column(VARCHAR(50), ForeignKey('mosque.google_places_id'))
    author = Column(VARCHAR(100))
    rating = Column(FLOAT)
    review_text = Column(TEXT)
    review_date = Column(TIMESTAMP)

class Facilities(Base):
    __tablename__ = 'facilities'

    id = Column(BigInteger, primary_key= True)
    google_places_id = Column(VARCHAR(50), ForeignKey('mosque.google_places_id'))
    has_womens_section = Column(Boolean)
    nlp_verified = Column(Boolean)
