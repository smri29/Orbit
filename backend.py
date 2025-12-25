import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

# --- CONFIGURATION ---
PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_vector_store():
    """Loads the existing Vector DB if it exists, otherwise returns None."""
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    if os.path.exists(PERSIST_DIRECTORY) and os.path.isdir(PERSIST_DIRECTORY):
        return Chroma(
            persist_directory=PERSIST_DIRECTORY, 
            embedding_function=embedding_function
        )
    return None

def update_knowledge_base(uploaded_files):
    """Processes uploaded PDFs and adds them to the persistent DB."""
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    all_splits = []
    
    for uploaded_file in uploaded_files:
        # Save temp file
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        loader = PyPDFLoader(uploaded_file.name)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        all_splits.extend(splits)
        
        # Cleanup
        os.remove(uploaded_file.name)

    # Save to Chroma
    vector_store = Chroma.from_documents(
        documents=all_splits,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    return vector_store

def get_rag_chain(vector_store):
    """Creates the RAG chain (Retrieval + Generation)."""
    retriever = vector_store.as_retriever()
    
    # SYSTEM PROMPT: Note I removed the "Say Hi" instruction here!
    system_prompt = (
        "You are Orbit, the AI assistant for CollabCircle. "
        "Your tone is helpful, professional, and encouraging. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer based on the context, say so politely. "
        "Context: {context}"
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Using the stable Flash model
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.3)
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain