from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST"],
    allow_headers=["*"],
)

# Load the embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

class SimilarityRequest(BaseModel):
    docs: list[str]
    query: str

class SimilarityResponse(BaseModel):
    matches: list[str]

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

@app.post("/similarity", response_model=SimilarityResponse)
async def calculate_similarity(request: SimilarityRequest):
    if not request.docs or not request.query:
        raise HTTPException(status_code=400, detail="Docs and query must be provided.")

    # Generate embeddings for documents and query
    doc_embeddings = model.encode(request.docs)
    query_embedding = model.encode(request.query)

    # Calculate similarities
    similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]

    # Rank documents by similarity
    ranked_docs = [doc for _, doc in sorted(zip(similarities, request.docs), reverse=True)]

    # Return top 3 matches
    return SimilarityResponse(matches=ranked_docs[:3])