from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True) # automatically creates primary key
    team_id = Column(String, ForeignKey("teams.id")) # foreign key

    customer_name = Column(String)
    customer_industry = Column(Text)
    customer_experience = Column(Text)

    customers_output = Column(Text) # store AI output

    team = relationship("Team", back_populates="hypotheses")
