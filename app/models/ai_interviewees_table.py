from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class Customer(Base):
    __tablename__ = "ai_interviewees"
    id = Column(Integer, primary_key=True) # primary key
    team_id = Column(String, ForeignKey("teams.id")) # foreign key, link a team with all generated personas
    team_id = Column(String, ForeignKey("hypotheses.id")) # foreign key, link hypothesis to generated personal

    ai_interviewee_name = Column(String) 
    ai_interviewee_industry = Column(String) 
    
    ai_output = Column(Text) # store AI output

    # link back to parents
    team = relationship("Team", back_populates="ai_personas")
    hypothesis = relationship("Hypothesis", back_populates="ai_personas")
