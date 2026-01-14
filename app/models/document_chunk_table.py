from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id")) # foreign key
    # interview_id = Column(Integer, ForeignKey("interviews.id"), nullable = True)
    # past_data_id = Column(Integer, ForeignKey("past_data.id"), nullable = True)


    # __table_args__ = (
    #     # since interview id and past data id chunks both stored in same table, ensure
    #     # data in table corresponds with at oleast one entry
    #     CheckConstraint(
    #         "(interview_id IS NOT NULL) OR (past_data_id IS NOT NULL)",
    #         name="at_least_one_parent"
    #     ),
    # )
    
    s3_key = Column(String) # s3 key for file access
    content = Column(Text)
    embedding = Column(Vector(1536)) 

    # python syntax, create direct connection to Interview class
    #interviews = relationship("Interviews", back_populates="chunks") 
