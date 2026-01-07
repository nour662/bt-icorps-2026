import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    file = r"bt-icorps-2026\src\test_file\Chat w_ Bobby.docx.pdf"
    
    all_chunks = process_file_to_chunks(file)

    # Display results
    print(f"Total chunks created: {len(all_chunks)}")
    print("-" * 30)

    for i, chunk in enumerate(all_chunks[:5]):
        print(f"CHUNK {i+1} (Source: Page {chunk.metadata.get('page', 'N/A')}):")
        print(chunk.page_content)
        print("-" * 30)

def process_file_to_chunks(file):
    # compatibility with various file types
    file_type = os.path.splitext(file)[1].lower() # determine file type

    if file_type == ".pdf":
        loader = PyPDFLoader(file)
    elif file_type == ".docx" or file_type == ".doc":
        loader = Docx2txtLoader(file)
    loader = PyPDFLoader(file) # library function
    pages = loader.load()

    # chunk text based on paragraph, then sentence, then character
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # determine optimal chunk size later
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # split documents
    chunks = text_splitter.split_documents(pages)
    return chunks

if __name__ == "__main__":
    main()