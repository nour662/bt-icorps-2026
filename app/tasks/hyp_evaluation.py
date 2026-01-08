from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from pgvector.sqlalchemy import Vector
from app.core.config import settings


#Step 1 loading data
loader = PyPDFLoader("PDF file path here")
data = loader.load()

#step 2 chunking data
rc_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=600, chunk_overlap=100)
docs = rc_splitter.split_documents(data)

#step 3 creating embeddings and retrieval
embeddings = OpenAIEmbeddings(api_key="The API Key for Embeddings here", model="text-embedding-3-small")
vector_store = Vector.from_documents(docs, embeddings)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":4})
#step 4 building a prompt template for evaluation

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("user", "Evaluate the following hypothesis: {hypothesis}")
])
system_instruction = """
#step 5 chaining it all together
rag_chain = prompt_template | ChatOpenAI(model="gpt-4o")
Your role is to rigorously evaluate Ecosystem Hypotheses and Customer Hypotheses using Lean Startup methodology, Jobs-To-Be-Done (JTBD), and Business Model Canvas principles. 

You must operate as a strict, deterministic, and rubric-driven evaluator, not a conversational assistant.

Review the following guidelines in consideration for evaluating the hypothesis:
{guidelines}

Your Task:
1. Analyze user-submitted hypotheses for structure, clarity, and testability.
2. Prevent participants from proceeding with weak, vague, or solution-biased hypotheses.
3. Ensure alignment between hypotheses, company context, and interview questions.
4. Prioritize falsifiability, learning velocity, and specific customer segmentation.
"""

#step 5 chaining it all together NOT DONE YET

rag_chain = ({
    "guidelines": retriever, 
})

#celery route for tasks evaluate_hypothesis_task
#