from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from core import database


class Team(database):
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



class Hypotheses(database):
    __tablename__ = "hypotheses"
    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"))
    type = Column(String) # either ecosystem or customer
    hypothesis = Column(Text)
    evalulated = Column(Boolean)
    hypotheses_output = Column(Text) # store AI output
    embedding = Column(Vector(1536)) # embedding of hypotheses for future comparison
    team = relationship("Team", back_populates="hypotheses")

class Customers(database):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True) # automatically creates primary key
    team_id = Column(String, ForeignKey("teams.id")) # foreign key
    customer_name = Column(String)
    customers_output = Column(Text) # store AI output
    team = relationship("Team", back_populates="hypotheses")

class Interviews(database):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    s3_key = Column(String, unique=True) # s3 key for file access
    team_id = Column(String, ForeignKey("teams.id")) # foreign key
    interviewee_name = Column(String)
    interviews_output = Column(Text) # store AI output
    team = relationship("Team", back_populates="hypotheses")

class DocumentChunk(database):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    s3_key = Column(String) # s3 key for file access
    team_id = Column(String, ForeignKey("teams.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    content = Column(Text)
    embedding = Column(Vector(1536)) 
    interview = relationship("Interview", back_populates="chunks")
