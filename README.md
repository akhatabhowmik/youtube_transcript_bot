# 🎬 YouTube Transcript RAG Bot

A powerful Retrieval-Augmented Generation (RAG) application that allows you to chat with any YouTube video using its transcript. Built with FastAPI, Streamlit, and LangChain, this bot leverages Mistral AI to provide accurate answers based solely on video content.

## 🚀 Features

- **Transcript Extraction**: Automatically fetches transcripts from YouTube videos.
- **RAG Pipeline**: Efficiently chunks text, generates embeddings, and stores them in a FAISS vector store.
- **Context-Aware QA**: Answers questions specifically using the video transcript as context.
- **Interactive UI**: A clean, chat-like interface for seamless interaction.

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **Streamlit** | Frontend UI and chat interface |
| **FastAPI** | Backend API service |
| **LangChain** | RAG orchestration and chain management |
| **Mistral AI** | Large Language Model (mistral-large-latest) |
| **FAISS** | High-performance vector database |
| **HuggingFace** | Text embeddings (all-MiniLM-L6-v2) |
| **YouTube Transcript API** | Automated transcript retrieval |

## 📂 Project Structure

```text
youtube_transcript_rag/
├── backend/
│   ├── main.py       # FastAPI application & endpoints
│   └── rag.py        # RAG pipeline logic (Transcripts -> Embeddings -> QA)
├── frontend/
│   └── app.py        # Streamlit user interface
├── .env              # Environment variables (Internal)
├── .gitignore        # Git ignore rules
└── requirements.txt  # Python dependencies
```

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/akhatabhowmik/youtube_transcript_bot.git
cd youtube_transcript_bot
```

### 2. Set up Virtual Environment (Optional but recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory and add your Mistral API key:
```env
MISTRAL_API_KEY=your_api_key_here
```

## 🏃 Running the Application

You need to run both the backend and the frontend simultaneously.

### Step 1: Start the Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
The backend will be available at `http://localhost:8000`.

### Step 2: Start the Frontend (Streamlit)
Open a new terminal and run:
```bash
streamlit run frontend/app.py
```
The application will open in your browser at `http://localhost:8501`.

## 🛠️ How it Works

1.  **Load Video**: When you enter a URL, the backend fetches the transcript and splits it into searchable chunks.
2.  **Indexing**: These chunks are converted into vectors using HuggingFace embeddings and stored in a FAISS index.
3.  **Querying**: When you ask a question, the system retrieves the most relevant chunks from the FAISS index and passes them to Mistral AI to generate a precise answer based on that context.

---
Built with ❤️ by [Akshata Bhowmik](https://github.com/akhatabhowmik)
