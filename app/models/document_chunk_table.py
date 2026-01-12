from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id")) # foreign key
    interview_id = Column(Integer, ForeignKey("interviews.id"))

    s3_key = Column(String) # s3 key for file access
    content = Column(Text)
    embedding = Column(Vector(1536)) 

    # python syntax, create direct connection to Interview class
    interviews = relationship("Interview", back_populates="chunks") 
