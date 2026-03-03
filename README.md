# 🔍 Semantic Search Engine for MongoDB Documents

An AI-powered **Semantic Search Engine** that enables intelligent and context-aware document retrieval from MongoDB using **Natural Language Processing (NLP)** and **sentence embeddings**.

---

## 📌 Project Summary

Traditional keyword-based search fails to understand the *meaning* of user queries.  
This project solves that problem using **semantic embeddings**, allowing users to search documents based on intent and context.

The application is a complete **full-stack AI system** consisting of:
- FastAPI backend
- MongoDB database
- NLP embedding model
- Streamlit user interface

---

## ✨ Features

- 🔎 Semantic (context-based) search
- ➕ Add documents dynamically
- 🧠 NLP-based embeddings using MiniLM
- 📊 Cosine similarity ranking
- 🗄️ MongoDB document storage
- 🌐 REST API with FastAPI
- 🎨 User-friendly Streamlit frontend
- 📄 Sample document loader

---

## 🧠 Technologies Used

### Backend
- Python
- FastAPI
- Sentence-Transformers (all-MiniLM-L6-v2)
- MongoDB
- NumPy

### Frontend
- Streamlit

### Tools & Libraries
- requests
- pymongo
- uvicorn

---

## 🗂️ Project Structure

Semantic-Search-Engine-for-MongoDB-Documents/
│
├── python_service/
│   └── app.py              # FastAPI backend
│
├── streamlitapp.py         # Streamlit frontend
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignored files (venv, cache, etc.)
└── README.md               # Project documentation

---

## ⚙️ How It Works

1. Documents are added through API or Streamlit UI  
2. Text is converted into embeddings using Sentence Transformers  
3. Embeddings are stored in MongoDB  
4. User query is embedded and compared using cosine similarity  
5. Top relevant documents are returned and ranked  

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository
Streamlit UI:
- http://localhost:8501

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/` | API health check |
| POST | `/add-document` | Add document |
| POST | `/search` | Semantic search |
| GET | `/stats` | Database statistics |

---

## 📄 Sample Documents

- AI Basics – Introduction to Artificial Intelligence  
- Deep Learning – Neural networks and representation learning  
- NLP Concepts – Natural language understanding  

---

## 🎯 Use Cases

- Academic research search
- Knowledge base systems
- Enterprise document retrieval
- Educational platforms

---

## 🏆 Hackathon Highlights

- End-to-end AI application
- Real-world NLP implementation
- Clean backend–frontend separation
- Scalable and modular design
