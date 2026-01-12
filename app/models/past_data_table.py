from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class PastData(Base):
    __tablename__ = "past_data"
    id = Column(Integer, primary_key=True)

    # past interview information
    s3_key = Column(String)
    embeddings = Column(Vector(1536))
    interview_evaulation = Column(Text)    
    
    # team = relationship("Team", back_populates="past_data")
    # chunks = relationship("DocumentChunk", back_populates="interviews", cascade="all, delete-orphan")

