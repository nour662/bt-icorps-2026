from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class Interviewees(Base):
    __tablename__ = "interviewees"
    id = Column(Integer, primary_key=True) # automatically creates primary key
    team_id = Column(String, ForeignKey("teams.id")) # foreign key

    customer_industry = Column(Text)
    customer_experience = Column(Text)
    customer_occupation = Column(Text)
    customer_checked = Column(Boolean, default=False)
    
    customers_output = Column(Text) # store AI output
    customers_output_score = Column(Integer)

    # team = relationship("Team", back_populates="interviewees")
