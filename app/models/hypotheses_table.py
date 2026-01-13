from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class Hypotheses(Base):
    __tablename__ = "hypotheses"
    id = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"))
    hypothesis_type = Column(String)
    hypothesis = Column(Text)
    
    evaluated = Column(Boolean, default=False)
    
    hypotheses_output = Column(Text) # store AI output
    hypotheses_output_score = Column(Integer)
    
    hypothesis_embedding = Column(Vector(1536)) # embedding of hypotheses for future comparison
    
    # team = relationship("Team", back_populates="hypotheses")
    # ai_interviewees = relationship("AI_Interviewees", back_populates="hypotheses")
