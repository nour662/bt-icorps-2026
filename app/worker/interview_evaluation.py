from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser

# db models: 
from app.models.interviews_table import Interviews
from app.models.hypotheses_table import Hypotheses
from app.models.document_chunk_table import DocumentChunk
from app.models.team_table import Team

# file imports: 
from app.storage.s3 import load_pdf_from_s3
from app.database.process_chunks import process_chunks

# rag usage
from .rag_functions import top_k_chunks_interview_data, format_rows_for_prompt
#importing settings and prompt template
from app.core.config import settings

#imports file from system prompts
from app.systemprompts.interview_evaluation_prompt import INTERVIEW_EVALUATION_PROMPT

@celery_app.task(name="evaluate_interview_task", bind=True)
def evaluate_interview_task(self, hypothesis_id : int, team_id : str, interview_id : int):
    db = SessionLocal()

    interview = db.query(Interviews).filter(Interviews.id == interview_id)
    s3_key = interview.s3_key
    file_bytes = load_pdf_from_s3(s3_key)
    process_chunks(db, interview_id, file_bytes, s3_key)

    hypothesis = db.query(Hypotheses).filter(Hypotheses.id == hypothesis_id)
    team = db.query(Team).filter(Team.id == team_id)
    hypothesis_embedding = hypothesis.hypothesis_embedding
    hypothesis_text = hypothesis.hypothesis

    rag_rows = top_k_chunks_interview_data(db, hypothesis_embedding, 5, interview_id)

    llm = ChatOpenAI(
       model="gpt-4o", 
       api_key=settings.OPENAI_API_KEY,
       base_url=settings.OPENAI_BASE_URL
    )
    rag_excerpts = format_rows_for_prompt(rag_rows)
    try: # need to still update prompt to match these guidelines
        prompt_inpupts = {
            "industry" : team.idustry,
            "hypothesis" : hypothesis_text,
            "rag_excerpts" : rag_excerpts
        }
        prompt = INTERVIEW_EVALUATION_PROMPT.format_messages(**prompt_inputs)
        response = llm.invoke(prompt)
        response = response.content
        response_json = json.loads(response)
        summary = response_json["summary"]
        evaluation = response_json["evaluation"]
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
        














