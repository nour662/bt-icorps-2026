from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class PastData(Base):
    __tablename__ = "past_data"
    id = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id")) # foreign key, link a team with all generated personas

    hypothesis = Column(Text)
    hypothesis_embedding = Column(Vector(1536))
    hypothesis_evaluation = Column(Text)
    hypothesis_score = Column(Integer)
    
    user_personas = Column(JSON) # maybe store in seperate tables?
    
    # past interview information
    s3_key = Column(String)
    interview_evaulation = Column(Text)
    
    hypotheses_output = Column(Text) # store AI output
    hypotheses_output_score = Column(Integer)
    
    
    team = relationship("Team", back_populates="past_data")
    chunks = relationship("DocumentChunk", back_populates="interviews", cascade="all, delete-orphan")

