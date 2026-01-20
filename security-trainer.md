#### **Project Title**  
**Security Trainer Chatbot for the Lecture on Secure Programming (SECTRAIN)**  

---

#### **Objective**  
Develop a context-aware, locally operable chatbot using **fine-tuning** and **Retrieval-Augmented Generation (RAG)** to enhance cybersecurity education. The chatbot will support students in mastering secure programming concepts, terminal/Kali Linux usage, and preparation for advanced offensive security courses. It aims to integrate into an existing **CTF-based self-learning platform** while operating without external API dependencies.  

---

#### **Key Components**  
1. **Research & Framework Selection**  
   - Comparative analysis of open-source LLMs (e.g., WhiteRabbitNeo, SecureFalcon) and frameworks (Langchain, LlamaIndex).  
   - Evaluation of vector databases (e.g., FAISS, Chroma) for local RAG workflows.  

2. **Domain-Specific Knowledge Integration**  
   - Data sources: (Lecture slides), OWASP Secure Code Review Guide, CVE/NVD databases, and curated code examples (good/bad practices).  
   - Web scraping for OWASP and cybersecurity literature.  

3. **Chatbot Architecture**  
   - Local inference optimization (CPU-only compatibility, no GPU dependency).  
   - User progress tracking and contextual history retention.  

(4. **Integration with Existing Systems**) 
   - Compatibility with the **CTF-based self-learning course** platform developed in prior work.  

---

#### **Methodology**  
1. **Comprehensive Literature Review**  

2. **Prototyping & Testing**  
   - Implement RAG pipelines using Langchain/LlamaIndex and evaluate LLMs like Mistral-7B or CodeLlama.  
   - Develop metrics:  
     - **Accuracy**: F1-score, BERTScore(?).  
     - **User Engagement**: Response time, satisfaction surveys.  
     - **Context Retention**: Custom benchmarks for multi-session interactions.  

3. **Iterative Refinement**  
   - Validate with students and if possible compare results against baseline models.  

---

#### **Technical Challenges**  
- **Resource Constraints**: Balancing model performance (e.g., 7B-parameter LLMs) with CPU-only inference latency.  
- **License Compliance**: Ensuring all components (LLMs, frameworks) are open-source and commercially usable.  
- **Data Privacy**: Secure local storage of user interaction histories and training data.  
- **Knowledge Freshness**: Regular updates to CVE/NVD databases and OWASP guidelines.  

---

#### **Expected Contributions**  
1. **Educational Tool**: Address the lack of tutoring resources for secure programming and Kali Linux training.  
2. **LLM Best Practices**: Insights into fine-tuning vs. RAG trade-offs for domain-specific education.  
3. **Open-Source Framework**: Reusable codebase for academic and industry cybersecurity training.  
4. **Research Validation**: Empirical evaluation of LLMs in technical education, supported by metrics like BERTScore.  

---

#### **Relevant Research Insights**  
- Fine-tuned LLMs might outperform general models in domain-specific tasks (e.g., SecureFalcon’s code analysis).  
- RAG might enhance factual accuracy in educational chatbots compared to base LLMs.  
- Hybrid approaches (RAG + light fine-tuning) might reduce hallucination rates in technical Q&A systems.  
