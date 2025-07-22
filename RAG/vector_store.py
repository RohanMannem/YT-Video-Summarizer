import faiss
import numpy as np
import openai
import os
from dotenv import load_dotenv
import pickle
from RAG.embeddings.openai_embeddings import OpenAIEmbeddings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class VectorStore:
    def __init__(self, dim=1536, embeddings = None):
        """
        Args:
            dim (int): Dimension of the embeddings.
        """
        self.index = faiss.IndexFlatL2(dim)  # L2 = Euclidean distance
        self.metadata = []  # List of dicts storing info per vector
        self.embeddings = embeddings or OpenAIEmbeddings()

    def add_embeddings(self, embedded_chunks):
        """
        Adds a list of embedded chunks to the index.

        Each element in embedded_chunks must be:
        {"embedding": [...], "text": ..., "chunk_id": ...}
        """
        vectors = np.array([ec["embedding"] for ec in embedded_chunks]).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(embedded_chunks)

    def search(self, query_text, top_k=5, model="text-embedding-3-small"):
        """
        Embeds the query text, searches the index, returns top_k results.

        Returns:
            List of dicts: [{"text": ..., "score": ..., "chunk_id": ...}]
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
                    "score": float(dist)
                })
        return results

    def save(self, path):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "metadata.pkl"), "wb") as f:
            pickle.dump(self.metadata, f)
    
    @staticmethod
    def load_faiss_index(path, dim=1536, embeddings = None):
        store = VectorStore(dim, embeddings)
        store.index = faiss.read_index(os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "metadata.pkl"), "rb") as f:
            store.metadata = pickle.load(f)

        return store