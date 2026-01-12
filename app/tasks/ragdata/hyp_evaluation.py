import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.core.celery_app import celery_app

from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser

#Add this to requirements.txt: langchain-postgres
from langchain_postgres import PGVector 
from app.core.config import settings
from app.systemprompts.hyp_evaluation_prompt import EVALUATION_PROMPT
from app.core.config import settings
from database.process_input_hypothesis import embed_hypothesis
from sqlalchemy.orm import Session
from app.models.hypotheses_table import Hypotheses

# 1. The reason why we are embedding is because yes we are receving the vectors from the DB
# But when you receive vectors they are just numbers. We need to embed the vectors inorder for 
# the LLM to understand them and use them for searching and matching.
embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY, 
    model="text-embedding-3-small"
)

# Create the DB connection URL but not sure if the .replace is needed or correct
connection_url = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+psycopg://")

# 2. Connect to the "hypothesis_rules" DB collection
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="hypothesis_rules", #Match the name of the table in the DB
    connection=connection_url,
    use_jsonb=True,
)

# 3. Create the Search Engine
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 4. Define the Chain
# Input expected: { "hypothesis": "...", "team_id": "...", "type": "..." }
rag_chain = (
    {
        # SEARCH STEP: Take the hypothesis text, find matching rules in DB
        "guidelines": itemgetter("hypothesis") | retriever | format_docs,
        
        # PASSTHROUGH: Pass the raw data to the prompt
        "hypothesis": itemgetter("hypothesis"),
        "team_id": itemgetter("team_id"),
        "hypothesis_type": itemgetter("hypothesis_type")
    }
    | EVALUATION_PROMPT
    | ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
    | StrOutputParser()
)

@celery_app.task(name="evaluate_hypothesis_task")

def evaluate_hypothesis_task(hypothesis_id:int, hypothesis:str, hypothesis_type: str, 
db: Session):
    # if ecosystem, evaluate with PGVector
    hypothesis_embedding = embed_hypothesis(hypothesis)


        # RAG logic here - make sure to sort by ecosystem
    # make OpenAI call - can define a request body baseed on the type r can make two separate calls

    # store results in the output and score section of the hypothesis table
    # return 


    #after you finish the openai call, set the score in the results variable 
    #This is in the hypothesis output and score 