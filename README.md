# 📄 Multi Document QA System (RAG-powered)

A Question Answering system that enables users to **upload their documents (any format)** and then **ask questions** of it.This application is powered by **Retrieval-Augmented Generation (RAG)** and a **language model** to provide intelligent, context-aware and **memory-based** responses.

---

## 🚀 Features

- 🧠 Ask any question about your uploaded documents
- 📄 Supports document in any format uploads
- 🔍 Embedding + Vector Store for fast information retrieval
- 🤖 Powered by a language model (mistral-small)
- 🧠 Remembers past question and history aware system
- 💬 Interactive and easy-to-use **Streamlit UI**

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **RAG Components**:
  - `LangChain`
  - `HuggingFaceEmbeddings`
  - `Semantic Chunking`
  - `ChromaDB` (Vector Store)
  - `MistralAI` (LLM)
  - `RunnableWithMessageHistory` (memory)
- **Parsing**: `marker`
- **Utilities**: `dotenv`, `os`, `datetime`, etc.

---

## 🧑‍💻 How It Works

1. **Upload documents** (`any format`)
2. documents are **parsed** using marker
3. Text is **split into chunks**
4. Each chunk is **embedded** using HuggingFace Embeddings
5. Chunks are stored in **ChromaDB vector store**
6. User selects:
   - **QA Mode**: Ask a question → relevant chunks are retrieved → MistralAI answers
   - **View Parsed text**: Allow users to view the textual format of the uploaded files
   - **View Chunk**: Allow viewing the chunks of parsed files

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/niskriti1/MultiDocRAG.git
```

# 2. (Optional) Create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

# 3. Install dependencies

```
pip install -r requirements.txt
```

# 4. Run the app

```
streamlit run app.py
```
