from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from typing import Optional
import numpy as np
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

app = FastAPI(title="Semantic Search Engine")

# --------------------------------
# MongoDB Connection
# --------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["semantic_search_db"]
collection = db["documents"]

# --------------------------------
# Load NLP Model (ONCE)
# --------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------------
# HOME ROUTE
# --------------------------------
@app.get("/")
def home():
    return {
        "message": "Semantic Search API is running",
        "endpoints": {
            "Add Document": "/add-document",
            "Semantic Search": "/search",
            "Stats": "/stats"
        }
    }

# --------------------------------
# ADD DOCUMENT API
# ADVANCEMENT 1: Validation + Metadata
# --------------------------------
@app.post("/add-document")
def add_document(doc: dict):
    if "title" not in doc or "content" not in doc:
        raise HTTPException(status_code=400, detail="Title and content required")

    # Prevent duplicates
    if collection.find_one({"content": doc["content"]}):
        raise HTTPException(status_code=409, detail="Duplicate document")

    embedding = model.encode(doc["content"]).tolist()

    document = {
        "title": doc["title"],
        "content": doc["content"],
        "embedding": embedding,
        "category": doc.get("category", "general"),
        "created_at": datetime.utcnow()
    }

    collection.insert_one(document)

    return {"message": "Document added successfully"}

# --------------------------------
# SEMANTIC SEARCH API
# ADVANCEMENT 2: top_k + threshold + category filter
# --------------------------------
@app.post("/search")
def search(data: dict):
    query = data.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    top_k: int = data.get("top_k", 5)
    threshold: float = data.get("threshold", 0.3)
    category: Optional[str] = data.get("category")

    query_embedding = model.encode(query)
    results = []

    mongo_filter = {}
    if category:
        mongo_filter["category"] = category

    for doc in collection.find(mongo_filter, {"_id": 0}):
        doc_embedding = np.array(doc["embedding"])
        similarity = np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
        )

        if similarity >= threshold:
            results.append({
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"],
                "score": round(float(similarity), 4)
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

# --------------------------------
# ADVANCEMENT 3: SEARCH STATISTICS
# --------------------------------
@app.get("/stats")
def stats():
    total_docs = collection.count_documents({})
    categories = collection.distinct("category")

    return {
        "total_documents": total_docs,
        "categories": categories
    }

# --------------------------------
# ADVANCEMENT 4: DELETE DOCUMENT
# --------------------------------
@app.delete("/delete")
def delete_document(title: str):
    result = collection.delete_one({"title": title})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": f"Document '{title}' deleted"}