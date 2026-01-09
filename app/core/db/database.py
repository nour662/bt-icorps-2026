from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Import models so Base can see them for create_all
from app.models.team_table import Team
from app.models.customers_table import Customers
from app.models.hypotheses_table import Hypotheses
from app.models.interviews_table import Interviews
from app.models.document_chunk_table import DocumentChunk


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# creates a pipeline to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()