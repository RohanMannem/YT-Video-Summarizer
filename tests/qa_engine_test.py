from ..RAG.vector_store import VectorStore
from ..RAG.qa_engine import generate_answer

query = "What was said about pricing?"
results = store.search(query, top_k=5)

answer = generate_answer(query, results)
print(answer)
