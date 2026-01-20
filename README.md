#  SECTRAIN — Security Trainer Chatbot for Secure Programming

**SECTRAIN** is a local, AI-powered chatbot designed to help students and developers learn about **secure programming**, **OWASP**, **CVE vulnerabilities**, and **cybersecurity practices** using natural language.  
It uses a **Retrieval-Augmented Generation (RAG)** pipeline and runs fully **offline** — no internet or external API required.

---

##  Get Started

###  Clone the Repository

```bash
git clone https://github.com/kevinsangani988/sectrain.git
cd sectrain
```

---

##  Download the Model

You must manually download the **Mistral 7B (v0.8 or higher)** GGUF model 

 Download from Hugging Face:  
[TheBloke/Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

 Recommended file:
```
mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

 **Update the path in `config.py`**:
Make sure your model path is correctly set in the `config.py` file, for example:

```python
MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
```

---

we have implemented two codes one with fallback and one without , please remove comments to use whatever you want to use and do comment which you are not using. it is in main.py and looks like :

```
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
.....

```

we have wrote comments which is with fallback and which one is not.

##  Installation

###  Requirements

- Python **3.9+**
- pip (Python package manager)

###  Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Run the Chatbot

Launch the Streamlit chatbot interface:

```bash
streamlit run main.py
```
Now UI will be available on port

---

##  How to Use

-  Ask questions related to **security**, **OWASP**, **CVE**, **Kali Linux**, and more.
-  Upload your **own PDFs** (cheat sheets, research papers, etc.) — the chatbot will use their content for answers.
-  Click **"Clear"** to reset the conversation context anytime.
-  No internet needed — **runs completely offline**.

---

##  Features

-  **Offline-first**: No external APIs or internet required  
-  Knowledgeable in **OWASP**, **CVEs**, **secure coding**, **Kali Linux**, and more  
-  **Upload PDFs** to enhance context (e.g., notes, research, whitepapers)  
-  Uses **RAG** pipeline for smart, accurate answers  
-  Powered by a **locally loaded language model (Mistral 7B)**  
-  Perfect for **universities**, **cybersecurity workshops**, and **self-learners**

---
