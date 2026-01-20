import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from config import DATA_FOLDER, VECTOR_DB_PATH

def load_documents():
    all_docs = []
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER, exist_ok=True)
    for filename in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(file_path)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            continue
        loaded = loader.load()
        for doc in loaded:
            doc.metadata = {"source": filename}
        all_docs.extend(loaded)
        print(f"[LOADER] Loaded {len(loaded)} pages from {filename}")
        with open("metrics_logs/test_log.txt", "a", encoding="utf-8") as logf:
            logf.write(f"[LOADER] Loaded {len(loaded)} pages from {filename}\n")
    return all_docs

def build_vector_db(all_docs):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_documents(all_docs)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_DB_PATH)

    print(f"[VECTOR DB] Total documents in vector store: {len(db.docstore._dict)}")
    with open("metrics_logs/test_log.txt", "a", encoding="utf-8") as logf:
        logf.write(f"[VECTOR DB] Total documents in vector store: {len(db.docstore._dict)}\n")
    
    return db

def embed_and_add_file(file_path, vectorstore, filename=None):
    if filename is None:
        filename = os.path.basename(file_path)
    if filename.endswith(".txt"):
        loader = TextLoader(file_path)
    elif filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    docs = loader.load()
    for doc in docs:
        doc.metadata = {"source": filename}
    chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    new_db = FAISS.from_documents(chunks, embeddings)
    vectorstore.merge_from(new_db)
    vectorstore.save_local(VECTOR_DB_PATH)
    return len(chunks)
