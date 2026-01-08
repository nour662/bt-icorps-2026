from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

#apparently this is the correct import path for vector store 
# when using langchain but it might be sequal algemy not sure DOUBLE CHECK 
from langchain_community.vectorstores import PGVector

#importing settings and prompt template
from app.core.config import settings

#not sure if this is the correct import path DOUBLE CHECK
from app.core import EVALUATION_PROMPT_TEMPLATE

#Step 1 loading data
loader = PyPDFLoader("PDF file path here")
data = loader.load()

#step 2 chunking data
rc_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=600, chunk_overlap=100
    )
docs = rc_splitter.split_documents(data)

#step 3 creating embeddings and retrieval
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
#step 4 building a prompt template for evaluation

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("user", "Evaluate the following hypothesis: {hypothesis}")
])
system_instruction = 

#step 5 chaining it all together NOT DONE YET

rag_chain = ({
    "guidelines": retriever, 
})

#celery route for tasks evaluate_hypothesis_task
# --- CELERY TASK ---
def evaluate_hypothesis_task(user_hypothesis: str):
    chain = get_rag_chain()
    result = chain.invoke(user_hypothesis)
    return result