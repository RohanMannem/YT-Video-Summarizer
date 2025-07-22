import faiss
import json
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer


class QASystem:
    def __init__(self, index_path: str, metadata_path: str, openai_api_key: str):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)

        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = OpenAI(api_key=openai_api_key)

    def embed_question(self, question: str) -> np.ndarray:
        embedding = self.embedding_model.encode([question])[0]
        return np.array([embedding], dtype=np.float32)

    def search_index(self, question_embedding: np.ndarray, top_k: int = 5):
        D, I = self.index.search(question_embedding, top_k)
        results = [self.metadata[str(idx)] for idx in I[0] if str(idx) in self.metadata]
        return results

    def build_prompt(self, question: str, context_chunks: list) -> str:
        context = "\n\n".join([
            f"[{chunk['start_time']}] {chunk['text']}"  # <-- timestamp-aware
            # f"{chunk['text']}"  # <-- uncomment this instead if no timestamps available
            for chunk in context_chunks
        ])

        prompt = f"""
        You are an assistant that answers questions about YouTube videos using their transcript.

        Context:
        {context}

        Question: {question}
        Answer concisely and cite timestamps where relevant.
        """
        return prompt

    def ask(self, question: str) -> str:
        embedding = self.embed_question(question)
        relevant_chunks = self.search_index(embedding)
        prompt = self.build_prompt(question, relevant_chunks)

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    qa = QASystem(
        index_path="vector_store/faiss.index",
        metadata_path="vector_store/metadata.json",
        openai_api_key="your-openai-api-key"
    )

    while True:
        q = input("Ask a question: ")
        print(qa.ask(q))
        print("---")