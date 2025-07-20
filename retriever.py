import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain.vectorstores import Chroma
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.schema import Document
from langchain.retrievers import MultiQueryRetriever
from langchain.memory.chat_message_histories import FileChatMessageHistory

def chunk_newly_parsed_grouped(newly_parsed, output_dir="./output"):
    splitter = SemanticChunker(
		embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
	)
    
    grouped_chunks = {}

    for base in newly_parsed:
        md_path = os.path.join(output_dir, base, f"{base}.md")

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        chunks = splitter.split_text(md_text)
        doc_chunks = []
        for i, chunk in enumerate(chunks):
            doc_chunks.append(Document(page_content=chunk, metadata={"source": base, "chunk_id": i}))
        
        grouped_chunks[base] = doc_chunks

    return grouped_chunks
  
def initialize_retriever(api_key,newly_parsed):
  
  grouped_chunks = chunk_newly_parsed_grouped(newly_parsed)
  
  all_docs = []
  for chunks in grouped_chunks.values():
    all_docs.extend(chunks)
  if not all_docs:
    raise ValueError("❌ No documents to add to vectorstore.")

  #initialize llm model
  llm = ChatMistralAI(
    model="mistral-small",
    temperature=0.2,
    api_key=api_key
  )

  #initialize vectorstore
  vectorstore=Chroma.from_documents(
    documents=all_docs,
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
  )

  #Create base retriever
  base_retriever = vectorstore.as_retriever(search_kwargs={'k':3})


  #Setup Retriever
  retriever =  MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm,
    include_original=True
  )
  
  return retriever

def format_docs(docs):
    if isinstance(docs, list):
        return "\n\n".join(doc.page_content for doc in docs)
    raise ValueError("Expected a list of Document objects.")
  
  

def get_history_file(session_id: str) -> FileChatMessageHistory:
    os.makedirs("memory", exist_ok=True)
    
    file_path = f"memory/{session_id}.json"
    return FileChatMessageHistory(file_path=file_path)