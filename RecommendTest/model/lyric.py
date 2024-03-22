from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, TIMESTAMP, DECIMAL, Text, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from model.base import Base

class Lyric(Base):
    __tablename__ = 'lyric'
    lyric_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('track.track_id'), nullable=False)  # 수정된 부분
    start_time = Column(DECIMAL(10, 3), nullable=False)
    end_time = Column(DECIMAL(10, 3), nullable=False)
    en_text = Column(Text, nullable=False)
    kr_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    # tracks = relationship("Track", back_populates="lyric")

    def print(self):
        print(f"Lyric ID: {self.lyric_id}")
        print(f"Track ID: {self.track_id}")
        print(f"Start Time: {self.start_time}")
        print(f"End Time: {self.end_time}")
        print(f"English Text: {self.en_text}")
        print(f"Korean Text: {self.kr_text}")
        print(f"Created At: {self.created_at}")


