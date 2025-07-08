import faiss
import numpy as np
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class VectorStore:
    def __init__(self, dim):
        """
        Args:
            dim (int): Dimension of the embeddings.
        """
        self.index = faiss.IndexFlatL2(dim)  # L2 = Euclidean distance
        self.metadata = []  # List of dicts storing info per vector

    def add_embeddings(self, embedded_chunks):
        """
        Adds a list of embedded chunks to the index.

        Each element in embedded_chunks must be:
        {
            "embedding": [...],
            "text": ...,
            "start_time": ...,
            "sentences": [...],
            "chunk_id": ...
        }
        """
        vectors = np.array([ec["embedding"] for ec in embedded_chunks]).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(embedded_chunks)

    def search(self, query_text, top_k=5, model="text-embedding-3-small"):
        """
        Embeds the query text, searches the index, and returns top_k matches.

        Returns:
            List of dicts: [{
                "text": ...,
                "chunk_id": ...,
                "start_time": ...,
                "score": ...,
                "sentences": [...]
            }]
        """
        query_embedding = openai.embeddings.create(input=[query_text], model=model).data[0].embedding
        query_vec = np.array(query_embedding).reshape(1, -1).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i < len(self.metadata):
                meta = self.metadata[i]
                results.append({
                    "text": meta["text"],
                    "chunk_id": meta["chunk_id"],
                    "start_time": meta.get("start_time", ""),
                    "sentences": meta.get("sentences", []),
                    "score": float(dist)
                })
        return results
