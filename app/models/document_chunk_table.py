from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
<<<<<<< HEAD
    #team_id = Column(String, ForeignKey("teams.id")) # foreign key
    #interview_id = Column(Integer, ForeignKey("interviews.id"))

    s3_key = Column(String) # s3 key for file access
   # team_id = Column(String, ForeignKey("teams.id"))
    #interview_id = Column(Integer, ForeignKey("interviews.id"))
    content = Column(Text)
    embedding = Column(Vector(1536)) 

    #interview = relationship("Interview", back_populates="chunks")
=======
    team_id = Column(String, ForeignKey("teams.id")) # foreign key
    interview_id = Column(Integer, ForeignKey("interviews.id"))

    s3_key = Column(String) # s3 key for file access
    team_id = Column(String, ForeignKey("teams.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    content = Column(Text)
    embedding = Column(Vector(1536)) 

    interview = relationship("Interview", back_populates="chunks")
>>>>>>> origin/main
