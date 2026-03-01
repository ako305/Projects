from fastapi import FastAPI
from qdrant_client import QdrantClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaLLM


app = FastAPI()

client = QdrantClient(url="http://qdrant:6333")

# This is the "Safety Net"
COLLECTION_NAME = "test_cases"
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"size": 3072, "distance": "Cosine"} # Adjust size to your model
    )

# Configuration for our Docker network
EMBEDDINGS_MODEL = "phi3"
OLLAMA_URL = "http://ollama:11434"
QDRANT_URL = "http://qdrant:6333"


# This turns text into mathematical vectors
embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)

class IngestRequest(BaseModel):
    file_path: str

@app.post("/ingest")
async def ingest_pdf(request: IngestRequest):
    try:
        # 1. Load PDF from the path provided
        loader = PyPDFLoader(request.file_path)
        pages = loader.load()

        # 2. Split into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(pages)

        # 3. Upload to Vector DB
        QdrantVectorStore.from_documents(
            docs,
            embeddings,
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME,
        )

        return {"status": "success", "chunks": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_pdf(request: QueryRequest):
    try:
        # 1. Connect to our existing 'Vault' in Qdrant
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            url=QDRANT_URL
        )

        # 2. Search for the top 3 most relevant snippets from the PDF
        docs = vector_store.similarity_search(request.question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # 3. Feed that context into the LLM
        llm = OllamaLLM(model="phi3", base_url=OLLAMA_URL)
        
        # This is the "Secret Sauce" - a prompt that forces the AI to use your data
        prompt = f"""
        Answer the question strictly using the provided context. 
        If the answer isn't in the context, say "I don't know."
        
        Context: {context}
        
        Question: {request.question}
        """
        
        response = llm.invoke(prompt)
        return {"answer": response, "source_documents": len(docs)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))