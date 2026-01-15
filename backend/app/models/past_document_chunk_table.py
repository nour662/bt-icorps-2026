from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class PastDocumentChunk(Base):
    __tablename__ = "past_document_chunks"
    id = Column(Integer, primary_key=True)
    past_data_id = Column(Integer, ForeignKey("past_data.id"))
    
    content = Column(Text)
    embedding = Column(Vector(1536)) 