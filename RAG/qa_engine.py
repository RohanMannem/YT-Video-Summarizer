# rag/qa_engine.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..RAG.vector_store import load_faiss_index
from openai import OpenAI
import json
import os

class QnAEngine:
    def __init__(self, store_dir, openai_client=None):
        self.index, self.embeddings = load_faiss_index(store_dir)
        metadata_path = os.path.join(store_dir, "metadata.json")
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)

        self.client = openai_client or OpenAI()

    def query(self, question, top_k=5):
        question_embedding = self.embeddings.embed_query(question)
        D, I = self.index.search([question_embedding], top_k)
        results = []
        for i in I[0]:
            if i < len(self.metadata):
                results.append(self.metadata[i])
        return results

    def answer(self, question, top_k=5, include_timestamps=True):
        context_chunks = self.query(question, top_k)
        context_text = "\n\n".join(
            f"[{chunk['start_time']:.2f}s] {chunk['text']}" if include_timestamps else chunk['text']
            for chunk in context_chunks
        )

        prompt = (
            "Answer the following question based on the context below.\n\n"
            f"Context:\n{context_text}\n\n"
            f"Question: {question}\nAnswer:"
        )

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

# This is the callable function you can use from anywhere
def answer_question(question, store_dir, top_k=5, include_timestamps=True):
    engine = QnAEngine(store_dir)
    return engine.answer(question, top_k=top_k, include_timestamps=include_timestamps)
