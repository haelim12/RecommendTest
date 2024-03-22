from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, TIMESTAMP, DECIMAL, Text, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from model.base import Base


class Artist(Base):
    __tablename__ = 'artist'
    artist_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    genres = Column(String(255), nullable=True)
    spotify_id = Column(String(255), nullable=False)
    spotify_popularity = Column(Integer, nullable=True)
    image = Column(String(512))
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    albums = relationship('Album', secondary='artist_album', back_populates='artists')
    tracks = relationship('Track', secondary='artist_track', back_populates='artists')


