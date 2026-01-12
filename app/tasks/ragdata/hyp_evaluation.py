from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser

#Add this to requirements.txt: langchain-postgres
from langchain_postgres import PGVector 
from app.core.config import settings
from app.systemprompts.hyp_evaluation_prompt import EVALUATION_PROMPT

# 1. Setup the Connection Tools
embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY, 
    model="text-embedding-3-small"
)

connection_url = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+psycopg://")

# 2. Connect to the "hypothesis_rules" Box we made in Phase 1
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="hypothesis_rules", # Must match Phase 1
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

#celery route for tasks evaluate_hypothesis_task
# --- CELERY TASK ---
def evaluate_hypothesis_task(user_hypothesis: str):
    result = rag_chain.invoke(user_hypothesis)
    return result