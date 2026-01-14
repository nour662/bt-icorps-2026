from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class Interviews(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id")) # foreign key
    hypothesis_id = Column(Integer, ForeignKey("hypotheses.id"))

    s3_key = Column(String, unique=True) # s3 key for file access
    
    evaluated = Column(Boolean, default=False)
    
    interviews_summary = Column(Text)
    interviews_output = Column(Text) # store AI output

    # define relationships
    # team = relationship("Team", back_populates="interviews")
    # cleanup, delete data in DocumentChunk table if interview is deleted
    #chunks = relationship("DocumentChunk", back_populates="interviews", cascade="all, delete-orphan")
