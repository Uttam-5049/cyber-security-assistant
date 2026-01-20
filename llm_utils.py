from langchain_community.llms import LlamaCpp
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import MODEL_PATH

def load_llm_and_chain(vectorstore, chat_history):
    llm = LlamaCpp(
        model_path=MODEL_PATH,
        n_ctx=8192,
        n_batch=128,
        f16_kv=False,
        use_mlock=True,
        n_gpu_layers=0,
        verbose=True,
        max_tokens=2048
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    for msg in chat_history:
        memory.chat_memory.add_message(msg)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return qa_chain
