from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(String, primary_key=True)
    name = Column(String)
    password_hash = Column(String, nullable=False)
    
    # preliminary information -> can call to give additional information to robot
    primary_industry = Column(Text)
    secondary_industry = Column(Text)
    # technology_background = Column(Text)
    # research_background = Column(Text)
    # commercialization_idea = Column(Text)
    # marketability = Column(Text)
    # ip_status = Column(Text)
    status = Column(String)

    # provide link to other tables
    hypotheses = relationship("Hypotheses", back_populates="team") # sync to hypotheses
    interviewees = relationship("Interviewees", back_populates="team") # sync to interviews
    interviews = relationship("Interviews", back_populates="team") # sync to customers
    ai_interviewees = relationship("AI_Interviewees", back_populates="team")

