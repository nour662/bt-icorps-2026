from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(String, primary_key=True)
    industry = Column(Text)
    name = Column(String)
    password_hash = Column(String, nullable=False)
    
    #status = Column(String)

    # provide link to other tables

