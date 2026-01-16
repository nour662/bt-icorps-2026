from app.core.celery_app import celery_app
import json
# from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
# from langchain.prompts.chat import ChatPromptTemplate
#from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser


# db models: 
from app.models.interviews_table import Interviews
from app.models.hypotheses_table import Hypotheses
from app.models.interview_document_chunk_table import DocumentChunk
from app.models.team_table import Team
from app.core.db.database import SessionLocal

# file imports: 
from app.storage.s3 import load_pdf_from_s3
from app.database.process_chunks import process_file_to_chunks, process_chunks_to_vectors, add_interview_data_chunks_to_db

# rag usage
from .rag_functions import top_k_chunks_interview_data, format_rows_for_prompt
#importing settings and prompt template
from app.core.config import settings

#imports file from system prompts
from app.systemprompts.interview_evaluation_prompt import INTERVIEW_EVALUATION_PROMPT

@celery_app.task(name="evaluate_interview_task", bind=True)
def evaluate_interview_task(self, hypothesis_id : int, team_id : str, interview_id : int):
    db = SessionLocal()

    interview = db.query(Interviews).filter(Interviews.id == interview_id).first()

    # extracting the bytes from the interview transcript in s3
    s3_key = interview.s3_key
    file_bytes = load_pdf_from_s3(s3_key)

    # chunking and embedding the file and inserting it into db
    text_chunks = process_file_to_chunks(file_bytes, 600)
    vector_chunks = process_chunks_to_vectors(text_chunks)
    add_interview_data_chunks_to_db(text_chunks, vector_chunks, interview_id, db)

    # gets the hypothesis embedding and text and runs RAG on the embedding to find the most similar portions of the transcript
    hypothesis = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id).first()
    team = db.query(Team).filter(Team.id == team_id).first()
    hypothesis_embedding = hypothesis.embedding
    hypothesis_text = hypothesis.hypothesis

    rag_rows = top_k_chunks_interview_data(db, hypothesis_embedding, 5, interview_id)

    # sets up the llm using langchain
    llm = ChatOpenAI(
       model="gpt-4o", 
       api_key=settings.OPENAI_API_KEY,
       base_url=settings.OPENAI_BASE_URL
    )
    rag_excerpts = format_rows_for_prompt(rag_rows)

    try: 
        print("\nTASK STARTED\n")
        prompt_inputs = {
            "industry" : team.industry,
            "hypothesis" : hypothesis_text,
            "rag_excerpts" : rag_excerpts
        }
        prompt = INTERVIEW_EVALUATION_PROMPT.format_messages(**prompt_inputs)
        response = llm.invoke(prompt)
        response = response.content
        # extracts information in json format
        response_json = json.loads(response)
        summary = response_json["summary"]
        evaluation = response_json["output"]
        # adds evauation information to db under the interview_id
        interview.interviews_output = evaluation
        interview.interviews_summary = summary
        interview.evaluated = True
        db.commit()
    except Exception as e: 
        print(f"Interview evaluation worker failed: {e}")
        db.rollback()
    finally:
        db.close()
    return "Interview Evaluation Task Finished"
        














