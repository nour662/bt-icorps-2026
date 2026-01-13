import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv #dotenv to read from env
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.document_chunk_table import DocumentChunk 

def process_chunks(db: Session, interview_id: int, key: str):
    file = "src/test_file/Chat w_ Bobby.docx.pdf" # hardcode file to test :P

    all_chunks = process_file_to_chunks(file)
    all_vectors = process_chunks_to_vectors(all_chunks)

    chunk_objects = []
    for chunk, vector in zip(all_chunks, all_vectors):
        # use zip to pair all_chunks and all_vectors 
        obj = DocumentChunk(
            content=chunk.page_content,
            embedding=vector,       
            interview_id=interview_id,
            s3_key=None
        )
        chunk_objects.append(obj)

    # save to database
    try:
        db.add_all(chunk_objects)
        db.commit()
        print(f"Stored {len(chunk_objects)} text chunks for interview.")
    except Exception as e:
        # error checking
        db.rollback() # if error, remove all chunks added to database
        print(f"Error: {e}")

def process_file_to_chunks(file):
    # compatibility with various file types
    file_type = os.path.splitext(file)[1].lower() # determine file type

    if file_type == ".pdf":
        loader = PyPDFLoader(file)
    elif file_type == ".docx" or file_type == ".doc":
        loader = Docx2txtLoader(file)
    pages = loader.load()

    # chunk text based on paragraph, then sentence, then character
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, # determine optimal chunk size later
        chunk_overlap=100, # preserves context if awkward split
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # split documents
    chunks = text_splitter.split_documents(pages)
    return chunks

def process_chunks_to_vectors(chunks):
    # will require openai key, skeleton for now
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small") 

    # loader creates list of document objects which contain page_content and metadata
    texts = [chunk.page_content for chunk in chunks] # extract text from chunks

    # generate vectors via openai -> 1536 numbers per chunk
    vectors = embeddings_model.embed_documents(texts)

    return vectors
