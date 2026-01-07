from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(String, primary_key=True)
    name = Column(String)
    
    # preliminary information -> can call to give additional information to robot
    primary_industry = Column(Text)
    secondary_industry = Column(Text)
    technology_background = Column(Text)
    research_background = Column(Text)
    commercialization_idea = Column(Text)
    marketability = Column(Text)
    ip_status = Column(Text)
    status = Column(String)

    # provide link to other tables
    hypotheses = relationship("Hypothesis", back_populates="team") # sync to hypotheses
    customers = relationship("Customers", back_populates="team") # sync to interviews
    interviews = relationship("Interview", back_populates="team") # sync to customers

