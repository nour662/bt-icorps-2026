from langchain_community_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv

#Loads the future api key from the .env file
load_dotenv()

#Step 1 loading data
loader = PyPDFLoader("PDF file path here")
data = loader.load()

#step 2 splitting data
rc_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=600, chunk_overlap=100)
docs = rc_splitter.split_documents(data)

#step 3 creating embeddings
embeddings = OpenAIEmbeddings(api_key="The API Key for Embeddings here", model="text-embedding-3-small")
vector_store = Vector.from_documents(docs, embeddings)

#step 4 building a prompt template for evaluation



#celery route for tasks evaluate_hypothesis_task
#