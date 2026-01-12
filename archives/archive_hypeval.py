from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser

#apparently this is the correct import path for vector store 
# when using langchain but it might be sequal algemy not sure DOUBLE CHECK 
from langchain_community.vectorstores import PGVector

#importing settings and prompt template
from app.core.config import settings

#imports file from system prompts
from app.systemprompts.hyp_evaluation_prompt import EVALUATION_PROMPT


#Step 1 loading data
loader = PyPDFLoader("PDF file path here")
data = loader.load()

#step 2 chunking data
rc_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=600, chunk_overlap=100
    )
docs = rc_splitter.split_documents(data)

#step 3 creating embeddings, vecorization, and retrieval
embeddings = OpenAIEmbeddings(
    api_key="The API Key for Embeddings here", model="text-embedding-3-small"
    )

vector_store = PGVector.from_documents(
    docs, embeddings,

    #not sure if I need these last 2 parameters DOUBLE CHECK
    collection_name="hypothesis_guidelines",
    connection_string=settings.DATABASE_URL
    )
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":4})

# Step 4: Chaining Components Together

def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

# This combines the Retrieval + The Prompt from File 1 + The LLM
rag_chain = (
    {
    "guidelines": retriever | format_docs, 
    "hypothesis": RunnablePassthrough()     
    }
    | EVALUATION_PROMPT                 # Uses the imported template
    | ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
    | StrOutputParser()
)

#celery route for tasks evaluate_hypothesis_task
# --- CELERY TASK ---
def evaluate_hypothesis_task(user_hypothesis: str):
    result = rag_chain.invoke(user_hypothesis)
    return result