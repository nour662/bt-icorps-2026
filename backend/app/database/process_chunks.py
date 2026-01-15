import os
#from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from pypdf import PdfReader
import io
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv #dotenv to read from env
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.past_document_chunk_table import PastDocumentChunk
from app.models.interview_document_chunk_table import DocumentChunk

# def process_chunks(interview_id: int, file_bytes : bytes, key: str):
#     all_chunks = process_file_to_chunks(file_bytes)
#     all_vectors = process_chunks_to_vectors(all_chunks)


def process_file_to_chunks(file_bytes, size):
    # compatibility with various file types
    # file_type = os.path.splitext(file)[1].lower() # determine file type

    # if file_type == ".pdf":
    #     loader = PyPDFLoader(file)
    # elif file_type == ".docx" or file_type == ".doc":
    #     loader = Docx2txtLoader(file)
    # pages = loader.load()

    # extracting the text: 
    reader = PdfReader(io.BytesIO(file_bytes))
    texts = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if (page_text != None):
            texts.append(f"\n\n-- Page {i + 1} --\n{page_text}")
    text = "".join(texts)

    # chunk text based on paragraph, then sentence, then character
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size, # determine optimal chunk size later
        chunk_overlap=100, # preserves context if awkward split
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # split documents
    chunks = text_splitter.split_text(text)
    return chunks

def process_chunks_to_vectors(chunks):
    # will require openai key, skeleton for now
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small") 

    # loader creates list of document objects which contain page_content and metadata
    # texts = [chunk.page_content for chunk in chunks] # extract text from chunks

    # generate vectors via openai -> 1536 numbers per chunk
    vectors = embeddings_model.embed_documents(chunks)

    return vectors

def add_past_data_chunks_to_db(all_chunks, all_vectors, past_data_id, db):
    chunk_objects = []
    for chunk, vector in zip(all_chunks, all_vectors):
        # use zip to pair all_chunks and all_vectors 
        obj = PastDocumentChunk(
            content=chunk,
            embedding=vector,       
            past_data_id=interview_id,
        )
        chunk_objects.append(obj)
    # save to database
    try:
        db.add_all(chunk_objects)
        db.commit()
        print(f"Stored {len(chunk_objects)} text chunks for past data.")
    except Exception as e:
        # error checking
        db.rollback() # if error, remove all chunks added to database
        print(f"Error: {e}")
    
def add_interview_data_chunks_to_db(all_chunks, all_vectors, interview_id, db):
    chunk_objects = []
    for chunk, vector in zip(all_chunks, all_vectors):
        # use zip to pair all_chunks and all_vectors 
        obj = DocumentChunk(
            content=chunk,
            embedding=vector,       
            interview_id=interview_id,
        )
        chunk_objects.append(obj)
    # save to database
    try:
        db.add_all(chunk_objects)
        db.commit()
        print(f"Stored {len(chunk_objects)} text chunks for past data.")
    except Exception as e:
        # error checking
        db.rollback() # if error, remove all chunks added to database
        print(f"Error: {e}")