from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    
    content = Column(Text)
    embedding = Column(Vector(1536)) 

    # python syntax, create direct connection to Interview class
    #interviews = relationship("Interviews", back_populates="chunks") 
