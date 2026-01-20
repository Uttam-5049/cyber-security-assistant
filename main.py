import os
import streamlit as st
from config import DATA_FOLDER, VECTOR_DB_PATH, HISTORY_FILE, TEST_LOG_FILE
from vectorstore_utils import load_documents, build_vector_db, embed_and_add_file
from llm_utils import load_llm_and_chain
from chat_history_utils import load_chat_history, save_chat_history
from cve_utils import fetch_cve_docs, fetch_cve_from_nvd_by_id
from owasp_utils import fetch_owasp_cheatsheets
from langchain.docstore.document import Document
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from feedback_logger import log_feedback
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

if not os.path.exists(os.path.dirname(TEST_LOG_FILE)):
    os.makedirs(os.path.dirname(TEST_LOG_FILE))
with open(TEST_LOG_FILE, "a") as f:
    f.write("Streamlit is running and has write access.\n")

st.set_page_config(page_title="SECTRAIN Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 SECTRAIN Chatbot")
st.caption("Your AI assistant for Secure Programming and Cybersecurity questions.")
st.markdown("---")

if 'vectorstore' not in st.session_state:
    all_docs = load_documents() + [Document(page_content=doc) for doc in fetch_cve_docs()] + fetch_owasp_cheatsheets()
    st.session_state.vectorstore = build_vector_db(all_docs)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = load_chat_history()
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = load_llm_and_chain(st.session_state.vectorstore, st.session_state.chat_history)

for pair in st.session_state.chat_history:
    if isinstance(pair, HumanMessage):
        with st.chat_message("user"):
            st.markdown(pair.content)
    elif isinstance(pair, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(pair.content)

user_input = st.chat_input("Ask SECTRAIN a question:")

# not using strong fallback but still effective

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            system_prompt = f"give well structured and meaningful answer of :  {user_input} "
            st.session_state.qa_chain.memory.chat_memory.add_message(SystemMessage(content=system_prompt))
            response = st.session_state.qa_chain.invoke(user_input)
            answer = response.get("answer", str(response))
            try:
                retrieved_docs = st.session_state.qa_chain.retriever.get_relevant_documents(user_input)
                with open(TEST_LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n--- QUERY: {user_input} ---\n")
                    for i, doc in enumerate(retrieved_docs, 1):
                        preview = doc.page_content[:300].replace("\n", " ")
                        source = doc.metadata.get("source", "N/A") if doc.metadata else "N/A"
                        f.write(f"{i}. Source: {source}\n   Preview: {preview}...\n")
            except Exception as e:
                pass
            st.markdown(answer)
            feedback_key = f"feedback_{len(st.session_state.chat_history)}"
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍 Correct", key=f"{feedback_key}_correct"):
                    log_feedback(user_input, answer, True)
                    st.success("✅ Thanks! Marked as correct.")
            with col2:
                if st.button("👎 Incorrect", key=f"{feedback_key}_incorrect"):
                    log_feedback(user_input, answer, False)
                    st.warning("❌ Got it. Marked as incorrect.")
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=answer))
    save_chat_history(st.session_state.chat_history)

# strong fallback with using keywords also

# if user_input:
#     with st.chat_message("user"):
#         st.markdown(user_input)
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             system_prompt = (
#                 f"give a well-structured, clear and meaningfull answer of this question :  {user_input} "
#             )
#             st.session_state.qa_chain.memory.chat_memory.add_message(SystemMessage(content=system_prompt))
#             try:
#                 retrieved_docs = st.session_state.qa_chain.retriever.get_relevant_documents(user_input)
                
#                 def is_relevant_doc(doc, query, min_length=50):
#                     if not doc.page_content or len(doc.page_content.strip()) < min_length:
#                         return False
                    
#                     query_words = set(query.lower().split())
#                     doc_words = set(doc.page_content.lower().split())
#                     overlap = len(query_words & doc_words)
                    
#                     security_terms = ['security', 'vulnerability', 'attack', 'injection', 'xss', 'sql', 'owasp', 'cve']
#                     has_security_terms = any(term in doc.page_content.lower() for term in security_terms)
                    
#                     return overlap >= 2 or has_security_terms
                
#                 kb_match = any(is_relevant_doc(doc, user_input) for doc in retrieved_docs)
                
#                 if kb_match:
#                     response = st.session_state.qa_chain.invoke(user_input)
#                     answer = response.get("answer", str(response))
#                     with open(TEST_LOG_FILE, "a", encoding="utf-8") as f:
#                         f.write(f"\n--- QUERY: {user_input} ---\n")
#                         f.write("[KB MATCH] Answered from knowledge base.\n")
#                         for i, doc in enumerate(retrieved_docs[:3], 1):
#                             if is_relevant_doc(doc, user_input):
#                                 preview = doc.page_content[:200].replace("\n", " ")
#                                 source = doc.metadata.get("source", "N/A") if doc.metadata else "N/A"
#                                 f.write(f"{i}. Source: {source}\n   Preview: {preview}...\n")
#                 else:
#                     contextual_prompt = (
#                         f"give a well-structured, clear and meaningfull answer of this question :  {user_input} "
#                     )
                    
#                     response = st.session_state.qa_chain.llm.invoke(contextual_prompt) if hasattr(st.session_state.qa_chain, 'llm') else {'answer': 'Sorry, I could not find relevant security information for your question in the knowledge base.'}
#                     answer = response.get("answer", str(response)) if isinstance(response, dict) else str(response)
#                     with open(TEST_LOG_FILE, "a", encoding="utf-8") as f:
#                         f.write(f"\n--- QUERY: {user_input} ---\n")
#                         f.write("[NO KB MATCH] Answered from general LLM knowledge with contextual fallback.\n")
                
#                 user_msg = HumanMessage(content=user_input)
#                 ai_msg = AIMessage(content=answer)
#                 st.session_state.qa_chain.memory.chat_memory.add_message(user_msg)
#                 st.session_state.qa_chain.memory.chat_memory.add_message(ai_msg)
                
#             except Exception as e:
#                 answer = f"An error occurred: {str(e)}"
#             st.markdown(answer)
#             feedback_key = f"feedback_{len(st.session_state.chat_history)}"
#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 if st.button("👍 Correct", key=f"{feedback_key}_correct"):
#                     log_feedback(user_input, answer, True)
#                     st.success("✅ Thanks! Marked as correct.")
#             with col2:
#                 if st.button("👎 Incorrect", key=f"{feedback_key}_incorrect"):
#                     log_feedback(user_input, answer, False)
#                     st.warning("❌ Got it. Marked as incorrect.")
#     st.session_state.chat_history.append(HumanMessage(content=user_input))
#     st.session_state.chat_history.append(AIMessage(content=answer))
#     save_chat_history(st.session_state.chat_history)


with st.sidebar:
    st.header("🛠️ Controls")
    st.subheader("📤 Upload Knowledge File")
    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"], key="file_uploader")
    if uploaded_file is not None and not st.session_state.get("file_uploaded", False):
        file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Uploaded {uploaded_file.name} to knowledge base.")
        try:
            num_chunks = embed_and_add_file(file_path, st.session_state.vectorstore, uploaded_file.name)
            st.session_state.qa_chain = load_llm_and_chain(st.session_state.vectorstore, st.session_state.chat_history)
            with open(TEST_LOG_FILE, "a", encoding="utf-8") as logf:
                logf.write(f"[DEBUG] Uploaded file {uploaded_file.name} added to vector DB with {num_chunks} chunks.\n")
            st.session_state.file_uploaded = True
            st.success("✅ New document embedded and added to knowledge base.")
        except Exception as e:
            st.error(f"❌ Failed to add file: {e}")
    elif uploaded_file is None:
        st.session_state.file_uploaded = False
    st.subheader("🧹 Chat Session")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        save_chat_history([])
        st.rerun()
    st.markdown("---")
    st.subheader("📚 Knowledge Base")
    if st.button("🔄 Reload Vector DB"):
        with st.spinner("Reloading knowledge base..."):
            all_docs = load_documents() + [Document(page_content=doc) for doc in fetch_cve_docs()] + fetch_owasp_cheatsheets()
            st.session_state.vectorstore = build_vector_db(all_docs)
            st.session_state.qa_chain = load_llm_and_chain(st.session_state.vectorstore, st.session_state.chat_history)
        st.success("✅ Vector DB and chat chain reloaded.")
    st.markdown("---")
    st.subheader("🕵️‍♂️ Add CVE by ID")
    cve_input = st.text_input("Enter CVE ID (e.g., CVE-2023-29357)", key="cve_input")
    if st.button("➕ Add CVE"):
        if not cve_input.strip():
            st.warning("⚠️ Please enter a valid CVE ID.")
        else:
            with st.spinner("Fetching CVE details..."):
                cve_data = fetch_cve_from_nvd_by_id(cve_input.strip())
                if cve_data["description"] == "Not found or failed to fetch.":
                    st.error("❌ CVE not found or failed to fetch.")
                else:
                    if cve_data and 'cve_id' in cve_data:
                        doc_text = (
                            f"CVE ID: {cve_data['cve_id']}\n"
                            f"Severity: {cve_data.get('severity', 'N/A')}\n"
                            f"Score: {cve_data.get('score', 'N/A')}\n"
                            f"Description: {cve_data.get('description', 'N/A')}\n"
                        )
                    else:
                        doc_text = "No valid CVE data available."
                    new_doc = Document(page_content=doc_text)
                    try:
                        num_chunks = embed_and_add_file(None, st.session_state.vectorstore, filename=None)
                        chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_documents([new_doc])
                        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                        new_db = FAISS.from_documents(chunks, embeddings)
                        st.session_state.vectorstore.merge_from(new_db)
                        st.session_state.vectorstore.save_local(VECTOR_DB_PATH)
                        st.session_state.qa_chain = load_llm_and_chain(st.session_state.vectorstore, st.session_state.chat_history)
                        st.success(f"✅ CVE {cve_data['cve_id']} added to knowledge base.")
                    except Exception as e:
                        st.error(f"❌ Failed to add CVE: {e}")
