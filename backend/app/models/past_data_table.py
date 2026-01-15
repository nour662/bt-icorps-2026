from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class PastData(Base):
    __tablename__ = "past_data"
    id = Column(Integer, primary_key=True)

    # content (ex hypothesis or file)
    content = Column(Text)
    s3_key = Column(String)
    
    # ex past_hypothesis, past_interviews
    data_type = Column(String)
    
    # outcomes
    embedding = Column(Vector(1536))
    
    # tags -> store industry for more information
    #industry = Column(String)
    
    #225 chunk size!
    