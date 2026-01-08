import os
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import DocumentChunk  # Importing your table blueprint
from database.pdf_to_chunk import process_file_to_chunks


def process_chunks(db: Session, interview_id: int):
    file = r"bt-icorps-2026\src\test_file\Chat w_ Bobby.docx.pdf"
    all_chunks = process_file_to_chunks(file)
    chunk_objects = [
        DocumentChunk(interview_id=interview_id, content=text) 
        for text in all_chunks
    ]

    # save to database
    try:
        db.add_all(chunk_objects)
        db.commit()
        print(f"Stored {len(chunk_objects)} text chunks for interview {interview_id}.")
    except Exception as e:
        # error checking
        db.rollback()
        print(f"Error: {e}")