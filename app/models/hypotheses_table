from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Hypotheses(Base):
    __tablename__ = "hypotheses"
    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"))
    hypothesis_type = Column(String) # either ecosystem or customer
    hypothesis = Column(Text)
    evalulated = Column(Boolean)
    hypotheses_output = Column(Text) # store AI output
    hypotheses_output_score = Column(Integer)
    suggested_customer_profiles = Column(JSON)
    embedding = Column(Vector(1536)) # embedding of hypotheses for future comparison
    team = relationship("Team", back_populates="hypotheses")
